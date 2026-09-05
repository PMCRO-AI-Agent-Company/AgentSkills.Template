#!/usr/bin/env python3
"""
PMCRO Chief persona declarative scaffolder.

Reads a ChiefSpec YAML and renders all five Chief plugin artifacts.
Also supports --all <csuite.yaml> to scaffold the entire C-Suite in one pass.

Usage:
  python scaffold_chief.py --spec csuite/specs/pmcro-chief-financial-officer.yaml [--dry-run] [--register] [--output-root .]
  python scaffold_chief.py --all csuite/csuite.yaml [--dry-run] [--register] [--output-root .]

Refuses (exit 1) on:
  - Schema violations
  - Placeholder tokens (TODO/FIXME/XXX/CHANGEME/TBD/FILLME)
  - Absolute paths in spec
  - Missing reasoning strategy ids in .agents/skills/reasoning/
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

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b", re.IGNORECASE)
DRIVE_LETTER_RE = re.compile(r"^[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"^/(Users|home|tmp|var|etc)/")

TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"


# ---------------------------------------------------------------------------
# Loading & validation
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise SystemExit("PyYAML required. Run: pip install pyyaml")
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Root must be a mapping in {path}")
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


def check_abs_paths(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, str):
        if DRIVE_LETTER_RE.search(obj) or ABSOLUTE_UNIX_RE.search(obj):
            errors.append(f"absolute path at {path or 'root'}: {obj}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(check_abs_paths(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            errors.extend(check_abs_paths(v, f"{path}[{i}]"))
    return errors


def validate_spec(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("apiVersion") != "pmcro.ai/v1":
        errors.append("apiVersion must be 'pmcro.ai/v1'")
    if data.get("kind") != "ChiefSpec":
        errors.append("kind must be 'ChiefSpec'")
    meta = data.get("metadata") or {}
    for req in ("id", "abbreviation", "display_name", "version", "status"):
        if req not in meta:
            errors.append(f"metadata.{req} is required")
    aid = meta.get("id", "")
    if aid and not re.match(r"^pmcro-chief-[a-z0-9]+(-[a-z0-9]+)*$", str(aid)):
        errors.append(f"metadata.id must match pmcro-chief-<kebab>: {aid}")
    spec = data.get("spec") or {}
    for req in ("domain", "intent_frame_kind", "description", "omode", "packaging"):
        if req not in spec:
            errors.append(f"spec.{req} is required")
    desc = spec.get("description", "")
    if isinstance(desc, str) and len(desc.strip()) < 20:
        errors.append("spec.description must be at least 20 characters")
    omode = spec.get("omode") or {}
    modes = omode.get("modes") or []
    if len(modes) < 3:
        errors.append("spec.omode.modes must have at least 3 entries")
    if not omode.get("default_reasoning_strategy"):
        errors.append("spec.omode.default_reasoning_strategy is required")
    errors.extend(check_placeholders(data))
    errors.extend(check_abs_paths(data))
    return errors


def check_reasoning_strategies(data: dict[str, Any], output_root: Path) -> list[str]:
    """Verify all omode reasoning_strategy ids exist in .agents/skills/reasoning/."""
    errors: list[str] = []
    catalog = output_root / ".agents" / "skills" / "reasoning"
    if not catalog.is_dir():
        errors.append(f"reasoning catalog not found at {catalog}")
        return errors
    omode = data.get("spec", {}).get("omode", {})
    ids_to_check = set()
    for mode in omode.get("modes", []):
        ids_to_check.add(mode.get("reasoning_strategy", ""))
    ids_to_check.add(omode.get("default_reasoning_strategy", ""))
    ids_to_check.discard("")
    for sid in ids_to_check:
        if not (catalog / sid).is_dir():
            errors.append(f"reasoning strategy '{sid}' not found in {catalog}")
    return errors


# ---------------------------------------------------------------------------
# Template rendering (minimal Jinja2-like substitution, no external deps)
# ---------------------------------------------------------------------------

def build_ctx(data: dict[str, Any]) -> dict[str, Any]:
    meta = data["metadata"]
    spec = data["spec"]
    omode = spec.get("omode", {})
    return {
        "id": meta["id"],
        "abbreviation": meta["abbreviation"],
        "display_name": meta["display_name"],
        "version": meta.get("version", "0.1.0"),
        "status": meta.get("status", "experimental"),
        "domain": spec["domain"],
        "intent_frame_kind": spec["intent_frame_kind"],
        "description": spec.get("description", "").strip(),
        "when_to_use": spec.get("when_to_use") or [],
        "constraints": spec.get("constraints") or [
            "Never invent facts without evidence.",
            "Domain execution remains with Maker and Checker.",
            "All paths must be repository-relative.",
        ],
        "modes": omode.get("modes") or [],
        "default_reasoning_strategy": omode.get("default_reasoning_strategy", "plan-and-execute"),
    }


def render_tmpl(tmpl_path: Path, ctx: dict[str, Any]) -> str:
    """
    Simple template renderer. Supports:
      {{ var }}         — scalar substitution
      {% for x in xs %}...{% endfor %}   — loop (one level only)
      {{ x.field }}     — attribute lookup inside loop vars
      {{ x | default('y') }} — default filter
    """
    text = tmpl_path.read_text(encoding="utf-8")
    # Process for loops first
    loop_re = re.compile(
        r"\{%-?\s*for\s+(\w+)\s+in\s+(\w+)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}",
        re.DOTALL,
    )

    def expand_loop(m: re.Match) -> str:
        var, collection_name, body = m.group(1), m.group(2), m.group(3)
        items = ctx.get(collection_name, [])
        out_parts: list[str] = []
        for item in items:
            loop_ctx: dict[str, Any] = {"item": item}
            if isinstance(item, dict):
                loop_ctx.update(item)
            part = body
            # Substitute {{ var.field }} or {{ var }}
            def sub_expr(em: re.Match) -> str:
                expr = em.group(1).strip()
                # handle | default(...)
                default_match = re.match(r"^(.+?)\s*\|\s*default\(['\"]?(.*?)['\"]?\)$", expr)
                if default_match:
                    key, fallback = default_match.group(1).strip(), default_match.group(2)
                else:
                    key, fallback = expr, ""
                parts_key = key.split(".")
                val = loop_ctx
                for p in parts_key:
                    if isinstance(val, dict):
                        val = val.get(p, fallback)
                    else:
                        val = fallback
                        break
                return str(val) if val is not None else fallback
            part = re.sub(r"\{\{(.*?)\}\}", sub_expr, part)
            out_parts.append(part)
        return "".join(out_parts)

    text = loop_re.sub(expand_loop, text)

    # Simple {{ expr }} substitution in remainder
    def sub_scalar(m: re.Match) -> str:
        expr = m.group(1).strip()
        default_match = re.match(r"^(.+?)\s*\|\s*default\(['\"]?(.*?)['\"]?\)$", expr)
        if default_match:
            key, fallback = default_match.group(1).strip(), default_match.group(2)
        else:
            key, fallback = expr, ""
        parts_key = key.split(".")
        val: Any = ctx
        for p in parts_key:
            if isinstance(val, dict):
                val = val.get(p)
            else:
                val = None
                break
        return str(val) if val is not None else fallback

    text = re.sub(r"\{\{(.*?)\}\}", sub_scalar, text)

    # Strip leftover block tags
    text = re.sub(r"\{%-?.*?-?%\}", "", text)
    return text


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path}")


def scaffold_one(data: dict[str, Any], output_root: Path, dry_run: bool, register: bool, directory: Path) -> dict[str, Any]:
    ctx = build_ctx(data)
    agent_id = ctx["id"]
    domain = ctx["domain"]
    plugin_root = output_root / "plugins" / agent_id
    generated: list[str] = []

    # 1. plugin.json
    tmpl = TEMPLATES_DIR / "plugin.json.tmpl"
    content = render_tmpl(tmpl, ctx)
    # Validate JSON output
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        print(f"  WARN: rendered plugin.json is not valid JSON: {e}")
    out = plugin_root / "plugin.json"
    write_file(out, content, dry_run)
    generated.append(str(out))

    # 2. omode.yaml
    tmpl = TEMPLATES_DIR / "omode.yaml.tmpl"
    content = render_tmpl(tmpl, ctx)
    out = plugin_root / "omode.yaml"
    write_file(out, content, dry_run)
    generated.append(str(out))

    # 3. govern-<domain>-intent/SKILL.md
    tmpl = TEMPLATES_DIR / "govern-intent.SKILL.md.tmpl"
    content = render_tmpl(tmpl, ctx)
    out = plugin_root / "skills" / f"govern-{domain}-intent" / "SKILL.md"
    write_file(out, content, dry_run)
    generated.append(str(out))

    # 4. select-reasoning-strategy/SKILL.md
    tmpl = TEMPLATES_DIR / "select-reasoning.SKILL.md.tmpl"
    content = render_tmpl(tmpl, ctx)
    out = plugin_root / "skills" / "select-reasoning-strategy" / "SKILL.md"
    write_file(out, content, dry_run)
    generated.append(str(out))

    # 5. .agents/skills/<id>/SKILL.md (thin auto-load entry)
    tmpl = TEMPLATES_DIR / "agent-entry.SKILL.md.tmpl"
    content = render_tmpl(tmpl, ctx)
    out = output_root / ".agents" / "skills" / agent_id / "SKILL.md"
    write_file(out, content, dry_run)
    generated.append(str(out))

    # 6. agents.yaml registration
    directory_updated = False
    if register:
        directory_updated = register_agent(data, ctx, directory, dry_run)

    return {
        "status": "ok",
        "agent_id": agent_id,
        "generated": generated,
        "directory_updated": directory_updated,
    }


# ---------------------------------------------------------------------------
# agents.yaml registration
# ---------------------------------------------------------------------------

def register_agent(data: dict[str, Any], ctx: dict[str, Any], directory: Path, dry_run: bool) -> bool:
    agents_file = directory / "agents.yaml"
    if not agents_file.exists():
        print(f"  WARN: {agents_file} not found — skipping registration")
        return False
    text = agents_file.read_text(encoding="utf-8")
    agent_id = ctx["id"]
    if f"id: {agent_id}" in text:
        print(f"  directory already contains id={agent_id} — skipping (update manually if needed)")
        return False
    domain = ctx["domain"]
    description = ctx["description"].replace("\n", " ")
    entry = f"""
  - id: {agent_id}
    kind: persona
    display_name: {ctx["display_name"]}
    description: >
      {description}
    owner_role: reflector
    capabilities: []
    skills:
      - name: govern-{domain}-intent
        path: plugins/{agent_id}/skills/govern-{domain}-intent
        tier: DOMAIN
      - name: select-reasoning-strategy
        path: plugins/{agent_id}/skills/select-reasoning-strategy
        tier: DOMAIN
    packaging:
      - target: agentskills
        path: plugins/{agent_id}
      - target: maf-inline
        path: src/Agents/{agent_id}
    status: {ctx["status"]}
    marketplace_visible: true
"""
    if dry_run:
        print(f"  [dry-run] would register {agent_id} in {agents_file}")
        return True
    with agents_file.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  registered {agent_id} in {agents_file}")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="PMCRO Chief persona scaffolder")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--spec", help="Path to a single ChiefSpec YAML")
    group.add_argument("--all", metavar="CSUITE_YAML", help="Path to csuite.yaml manifest (scaffolds all listed specs)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--register", action="store_true", help="Append entry to agents.yaml if missing")
    parser.add_argument("--output-root", default=".", help="Repo root (default: cwd)")
    parser.add_argument("--directory", default=".pmcro/directory", help="Path to agent directory folder")
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()
    directory = output_root / args.directory

    spec_paths: list[Path] = []

    if args.spec:
        spec_paths.append(Path(args.spec))
    else:
        csuite_path = Path(args.all)
        if not csuite_path.is_file():
            print(f"FAIL: csuite manifest not found: {csuite_path}", file=sys.stderr)
            return 2
        csuite = load_yaml(csuite_path)
        for entry in (csuite.get("chiefs") or []):
            spec_rel = entry.get("spec")
            if spec_rel:
                spec_paths.append(csuite_path.parent / spec_rel)

    if not spec_paths:
        print("FAIL: no spec paths resolved", file=sys.stderr)
        return 2

    all_ok = True
    results: list[dict[str, Any]] = []

    for spec_path in spec_paths:
        print(f"\n--- {spec_path} ---")
        if not spec_path.is_file():
            print(f"  FAIL: not found: {spec_path}")
            all_ok = False
            continue

        try:
            data = load_yaml(spec_path)
        except Exception as exc:
            print(f"  FAIL: cannot load: {exc}")
            all_ok = False
            continue

        errors = validate_spec(data)
        strat_errors = check_reasoning_strategies(data, output_root)
        errors.extend(strat_errors)

        if errors:
            print("  REJECT")
            for e in errors:
                print(f"    - {e}")
            all_ok = False
            continue

        result = scaffold_one(data, output_root, args.dry_run, args.register, directory)
        results.append(result)

    print("\n=== Summary ===")
    print(json.dumps({"all_ok": all_ok, "results": results}, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
