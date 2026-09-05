#!/usr/bin/env python3
"""
PMCRO declarative scaffolder (agentskills + maf-inline C#).

Usage:
  python scaffold.py --spec path/to/spec.yaml [--register] [--dry-run] [--output-root .]

Refuses (exit 1) on schema/placeholder/absolute-path violations.
Writes nothing on refusal.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

PLACEHOLDER_RE = re.compile(
    r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b",
    re.IGNORECASE,
)
DRIVE_LETTER_RE = re.compile(r"^[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"^/(Users|home|tmp|var|etc)/")

REQUIRED_SPEC_KEYS = {"apiVersion", "kind", "metadata", "spec"}


def load_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise SystemExit("PyYAML is required for YAML specs. pip install pyyaml")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be a mapping")
    return data


def check_placeholders(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, str):
        if PLACEHOLDER_RE.search(obj):
            errors.append(f"placeholder token at {path or 'root'}: {obj[:80]}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(check_placeholders(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            errors.extend(check_placeholders(v, f"{path}[{i}]"))
    return errors


def check_paths(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, str):
        if DRIVE_LETTER_RE.search(obj) or ABSOLUTE_UNIX_RE.search(obj):
            errors.append(f"absolute or drive-letter path at {path or 'root'}: {obj}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(check_paths(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            errors.extend(check_paths(v, f"{path}[{i}]"))
    return errors


def basic_schema_check(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_SPEC_KEYS - set(data.keys())
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")
    if data.get("apiVersion") != "pmcro.ai/v1":
        errors.append("apiVersion must be 'pmcro.ai/v1'")
    if data.get("kind") != "AgentScaffoldSpec":
        errors.append("kind must be 'AgentScaffoldSpec'")

    meta = data.get("metadata") or {}
    if not isinstance(meta, dict):
        errors.append("metadata must be an object")
    else:
        for req in ("id", "kind", "display_name"):
            if req not in meta:
                errors.append(f"metadata.{req} is required")
        aid = meta.get("id", "")
        if aid and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(aid)):
            errors.append(f"metadata.id must be kebab-case: {aid}")

    spec = data.get("spec") or {}
    if not isinstance(spec, dict):
        errors.append("spec must be an object")
    else:
        desc = spec.get("description", "")
        if not isinstance(desc, str) or len(desc) < 20:
            errors.append("spec.description must be a string of at least 20 characters")
        packaging = spec.get("packaging")
        if not isinstance(packaging, list) or len(packaging) < 1:
            errors.append("spec.packaging must be a non-empty array")
    return errors


def render_agentskills(spec_data: dict[str, Any], target_path: Path, dry_run: bool) -> Path:
    meta = spec_data["metadata"]
    spec = spec_data["spec"]
    skills = spec.get("skills") or []
    constraints = spec.get("constraints") or []

    # Minimal template rendering (no external jinja dependency for MVP)
    skill_blocks = []
    for s in skills:
        skill_blocks.append(
            f"### {s.get('name', 'unnamed')}\n\n{s.get('description', '')}\n"
        )
    constraints_block = "\n".join(f"- {c}" for c in constraints) if constraints else (
        "- Follow all PMCRO laws and the runtime output contract.\n"
        "- Never invent capabilities or providers.\n"
        "- All paths must be repository-relative."
    )

    content = f"""---
name: {meta['id']}
description: {spec['description']}
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: DOMAIN
  capability_class: DOMAIN
---

# {meta['display_name']}

## Purpose

{spec['description']}

## When to Use

- Tasks that match the purpose above.

## When Not to Use

- Core lifecycle operations (orchestrate / plan / make / check / reflect / trail initialize).
- Any action that would violate PMCRO laws (evidence, checker-gate, plugin isolation, output contract).

## Skills

{chr(10).join(skill_blocks) if skill_blocks else "_No skill entry points declared yet._"}

## Constraints

{constraints_block}

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: {meta['id']})
- Scaffolded by: `pmcro-marketplace-directory:scaffold-skill`
"""

    out_file = target_path / "SKILL.md"
    if dry_run:
        print(f"[dry-run] would write {out_file}")
    else:
        target_path.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        print(f"wrote {out_file}")
    return out_file



def to_csharp_identifiers(agent_id: str, display_name: str) -> tuple[str, str]:
    """Derive a C# class name and namespace segment from the agent id."""
    parts = [p.capitalize() for p in agent_id.split("-") if p]
    class_name = "".join(parts) or "Generated"
    if not class_name.endswith("Skill"):
        class_name += "Skill"
    ns = "".join(parts) or "Generated"
    return class_name, ns


def render_maf_inline(spec_data: dict[str, Any], target_path: Path, dry_run: bool) -> Path:
    meta = spec_data["metadata"]
    spec = spec_data["spec"]
    class_name, ns = to_csharp_identifiers(meta["id"], meta["display_name"])

    content = f"""// <auto-generated>
// Scaffolded by pmcro-marketplace-directory:scaffold-skill (maf-inline target)
// Agent id: {meta['id']}
// Do not invent capabilities. All paths must remain repository-relative.
// </auto-generated>

using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

// NOTE: Namespaces and base types follow common Microsoft Agent Framework
// patterns. Unconfirmed API surface is marked TODO and must be verified
// against the MAF version in use before production.

namespace Pmcro.Agents.{ns};

/// <summary>
/// {meta['display_name']}
/// </summary>
/// <remarks>
/// {spec['description'].strip()}
/// </remarks>
public sealed class {class_name}
{{
    public string Id => "{meta['id']}";
    public string DisplayName => "{meta['display_name']}";

    /// <summary>
    /// Primary entry point for this domain/persona skill.
    /// </summary>
    public async Task<IDictionary<string, object?>> ExecuteAsync(
        IDictionary<string, object?> input,
        CancellationToken cancellationToken = default)
    {{
        // TODO(maf): Replace with real MAF InlineSkill / ChatClientAgent invocation
        // once the host project references the confirmed MAF package version.
        // Do not claim a specific MAF type name until it is verified.

        cancellationToken.ThrowIfCancellationRequested();

        var result = new Dictionary<string, object?>
        {{
            ["agent_id"] = Id,
            ["status"] = "executed",
            ["note"] = "Scaffolded stub — wire to real MAF runtime before use."
        }};

        return await Task.FromResult(result).ConfigureAwait(false);
    }}
}}
"""

    out_file = target_path / f"{class_name}.cs"
    if dry_run:
        print(f"[dry-run] would write {out_file}")
    else:
        target_path.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        print(f"wrote {out_file}")
    return out_file


def register_agent(spec_data: dict[str, Any], directory_path: Path, dry_run: bool) -> bool:

    """Append or update entry in agents.yaml (MVP: simple append if missing)."""
    meta = spec_data["metadata"]
    spec = spec_data["spec"]
    agents_file = directory_path / "agents.yaml"
    if not agents_file.exists():
        print(f"WARNING: {agents_file} not found — skip register")
        return False

    text = agents_file.read_text(encoding="utf-8")
    if f"id: {meta['id']}" in text:
        print(f"directory already contains id={meta['id']} — leave untouched (MVP)")
        return False

    packaging = spec.get("packaging") or []
    packaging_lines = []
    for p in packaging:
        packaging_lines.append(f"      - target: {p.get('target')}")
        if p.get("path"):
            packaging_lines.append(f"        path: {p['path']}")

    entry = f"""
  - id: {meta['id']}
    kind: {meta['kind']}
    display_name: {meta['display_name']}
    description: >
      {spec['description']}
    owner_role: {spec.get('owner_role', 'planner')}
    capabilities: {spec.get('capabilities') or []}
    skills: []
    packaging:
{chr(10).join(packaging_lines) if packaging_lines else "      []"}
    status: experimental
    marketplace_visible: true
"""
    if dry_run:
        print("[dry-run] would append directory entry for", meta["id"])
        return True

    with agents_file.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"registered {meta['id']} in {agents_file}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="PMCRO MVP scaffold-skill")
    parser.add_argument("--spec", required=True, help="Path to AgentScaffoldSpec")
    parser.add_argument("--register", action="store_true", help="Upsert Agent Directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-root", default=".", help="Repo-relative root for outputs")
    parser.add_argument(
        "--directory",
        default=".pmcro/directory",
        help="Path to Agent Directory folder",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"FAIL: spec not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        data = load_spec(spec_path)
    except Exception as exc:
        print(f"FAIL: cannot load spec: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    errors.extend(basic_schema_check(data))
    errors.extend(check_placeholders(data))
    errors.extend(check_paths(data))

    if errors:
        print("REJECT")
        for e in errors:
            print(f"  - {e}")
        return 1

    meta = data["metadata"]
    spec = data["spec"]
    output_root = Path(args.output_root)
    generated = []

    for pkg in spec.get("packaging") or []:
        target = pkg.get("target")
        if target == "agentskills":
            rel = pkg.get("path") or f".agents/skills/{meta['id']}"
            if DRIVE_LETTER_RE.search(rel) or rel.startswith("/"):
                print(f"REJECT: packaging path must be repo-relative: {rel}")
                return 1
            target_path = output_root / rel
            render_agentskills(data, target_path, args.dry_run)
            generated.append({"target": target, "path": rel})
        elif target == "maf-inline":
            lang = (pkg.get("language") or "csharp").lower()
            if lang not in {"csharp", "cs", "c#"}:
                print(f"REJECT: maf-inline currently supports only csharp, got language={lang}")
                return 1
            rel = pkg.get("path") or f"src/Agents/{meta['id']}"
            if DRIVE_LETTER_RE.search(rel) or rel.startswith("/"):
                print(f"REJECT: packaging path must be repo-relative: {rel}")
                return 1
            target_path = output_root / rel
            render_maf_inline(data, target_path, args.dry_run)
            generated.append({"target": target, "path": rel, "language": "csharp"})
        else:
            print(f"SKIP unsupported target in this version: {target}")
            continue

    directory_updated = False
    if args.register:
        directory_updated = register_agent(
            data, Path(args.directory), args.dry_run
        )

    result = {
        "status": "ok",
        "action": "SCAFFOLD",
        "agent_id": meta["id"],
        "generated": generated,
        "directory_updated": directory_updated,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
