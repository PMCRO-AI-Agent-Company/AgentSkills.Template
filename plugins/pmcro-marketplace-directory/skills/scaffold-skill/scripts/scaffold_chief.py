#!/usr/bin/env python3
"""
PMCRO Chief plugin scaffolder (declarative, template-driven).

Generates the full 5-artifact bundle for a C-Suite persona plugin, matching
the hand-built pmcro-chief-{executive,technology,learning}-officer pattern:

  plugins/<id>/plugin.json
  plugins/<id>/omode.yaml
  plugins/<id>/skills/govern-<domain>-intent/SKILL.md
  plugins/<id>/skills/select-reasoning-strategy/SKILL.md
  .agents/skills/<id>/SKILL.md          (thin auto-load pointer)
  .pmcro/directory/agents.yaml          (appended entry)

Usage:
  python scaffold_chief.py --spec specs/csuite/cfo.spec.yaml --register

Refuses (exit 1) on schema violations, unknown reasoning-strategy ids, or
absolute/drive-letter paths. Writes nothing on refusal.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

DRIVE_LETTER_RE = re.compile(r"^[A-Za-z]:[\\/]")
VERSION = "0.2.0"


def load_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be a mapping")
    return data


def validate(data: dict[str, Any], catalog_dir: Path) -> list[str]:
    errors: list[str] = []
    if data.get("apiVersion") != "pmcro.ai/v1":
        errors.append("apiVersion must be pmcro.ai/v1")
    if data.get("kind") != "AgentScaffoldSpec":
        errors.append("kind must be AgentScaffoldSpec")
    meta = data.get("metadata") or {}
    for req in ("id", "kind", "display_name"):
        if req not in meta:
            errors.append(f"metadata.{req} required")
    spec = data.get("spec") or {}
    for req in ("description", "domain_word", "frame_shape", "omode",
                "default_reasoning_strategy"):
        if req not in spec:
            errors.append(f"spec.{req} required")
    valid_ids = {p.name for p in catalog_dir.iterdir() if p.is_dir()} if catalog_dir.is_dir() else set()
    for m in spec.get("omode", []):
        rid = m.get("reasoning_strategy")
        if valid_ids and rid not in valid_ids:
            errors.append(f"unknown reasoning_strategy id: {rid}")
    default_id = spec.get("default_reasoning_strategy")
    if valid_ids and default_id not in valid_ids:
        errors.append(f"unknown default_reasoning_strategy id: {default_id}")
    return errors


def render_plugin_json(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    gname = f"govern-{spec['domain_word']}-intent"
    skills_json = f"""  {{
      "name": "{gname}",
      "path": "skills/{gname}",
      "description": "{spec['skills'][0]['description'].strip()}"
    }},
    {{
      "name": "select-reasoning-strategy",
      "path": "skills/select-reasoning-strategy",
      "description": "{spec['skills'][1]['description'].strip()}"
    }}"""
    return f"""{{
  "id": "{meta['id']}",
  "name": "{meta['id']}",
  "version": "{VERSION}",
  "description": "{spec['description'].strip()}",
  "skills": [
{skills_json}
  ],
  "dependencies": {{
    "reasoning_catalog": ".agents/skills/reasoning"
  }},
  "notes": [
    "Auto-loaded as a persona plugin. Invoke via /{meta['id']}.",
    "Does not replace lifecycle plugins (orchestrate/plan/make/check/reflect/trail).",
    "All paths are repository-relative. No absolute paths.",
    "Governed by L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT."
  ]
}}
"""


def render_omode_yaml(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    lines = [
        "apiVersion: pmcro.ai/v1",
        "kind: ChiefOMode",
        f"chief_id: {meta['id']}",
        f"description: >",
        f"  Operating mode map for the {meta['display_name']}. Consulted by",
        "  select-reasoning-strategy to pick the right reasoning skill and frame shape",
        "  for each incoming domain seed before Planner handoff.",
        "",
        "modes:",
    ]
    for m in spec["omode"]:
        lines.append(f'  - trigger: "{m["trigger"]}"')
        lines.append(f'    reasoning_strategy: {m["reasoning_strategy"]}')
        lines.append(f'    frame_shape: {spec["frame_shape"]}')
        lines.append(f'    notes: "{m["notes"]}"')
        lines.append("")
    lines.append(f"default_reasoning_strategy: {spec['default_reasoning_strategy']}")
    lines.append(f"default_frame_shape: {spec['frame_shape']}")
    lines.append("reasoning_catalog_path: .agents/skills/reasoning")
    return "\n".join(lines) + "\n"


def render_govern_skill(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    dw = spec["domain_word"]
    gname = f"govern-{dw}-intent"
    fshape = spec["frame_shape"]
    desc = spec["skills"][0]["description"].strip()
    constraints = "\n".join(f"- {c}" for c in spec["constraints"])
    return f"""---
name: {gname}
description: {desc} USE FOR any incoming {dw} task. DO NOT USE for core lifecycle operations.
license: Apache-2.0
metadata:
  version: "{VERSION}"
  tier: DOMAIN
  capability_class: DOMAIN
---

# {gname}

## Purpose

Translate an underspecified {dw} seed into a fully governed `{fshape}`: a structured artifact with a clear goal, audience/stakeholders, success criteria, out-of-scope boundaries, and a selected reasoning strategy — ready for Planner handoff.

## When to Use

- Any incoming request that touches {dw} strategy or decision-making for the AI Agent Company
- Before handing off to the Planner for PMCR cycle execution

## When Not to Use

- Core lifecycle operations (orchestrate / plan / make / check / reflect / trail initialize)
- Requests outside this Chief's domain — route to the appropriate Chief persona instead

## Workflow

1. Read the incoming seed (user request or queue item).
2. Call `select-reasoning-strategy` to determine the OMode for this seed.
3. Produce a `{fshape}`:
   - `goal`: one-sentence statement of what is to be achieved
   - `stakeholders`: who is affected or accountable
   - `success_criteria`: 2-5 measurable conditions that define done
   - `out_of_scope`: explicit exclusions to prevent scope creep
   - `selected_reasoning_strategy`: the strategy id returned by select-reasoning-strategy
   - `selected_frame_shape`: the frame shape to use in the trail
4. Emit the frame as a governed result satisfying `L-OUTPUT-CONTRACT`.
5. Hand off to Orchestrator for cycle opening.

## Output Shape

```yaml
kind: {fshape}
chief_id: {meta['id']}
goal: "..."
stakeholders:
  - "..."
success_criteria:
  - "..."
out_of_scope:
  - "..."
selected_reasoning_strategy: {spec['default_reasoning_strategy']}
selected_frame_shape: {fshape}
```

## Constraints

{constraints}
"""


def render_select_reasoning_skill(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    dw = spec["domain_word"]
    return f"""---
name: select-reasoning-strategy
description: Consult the {meta['display_name']}'s omode.yaml and the reasoning catalog to select the appropriate reasoning skill id for a given {dw} task. USE BEFORE govern-{dw}-intent produces its frame. DO NOT invent strategy ids not present in the reasoning catalog.
license: Apache-2.0
metadata:
  version: "{VERSION}"
  tier: DOMAIN
  capability_class: DOMAIN
---

# select-reasoning-strategy ({meta['display_name']})

## Purpose

Given an incoming {dw}-domain seed, match it against this Chief's `omode.yaml` trigger list and return the best reasoning strategy id from `.agents/skills/reasoning/`.

## When to Use

- Called by `govern-{dw}-intent` before producing a `{spec['frame_shape']}`
- Any time this Chief needs to declare which reasoning approach to apply to a task

## When Not to Use

- Selecting strategies for other Chiefs' domains — each Chief has its own instance
- Overriding a strategy that has already been locked into an open trail

## Workflow

1. Read `plugins/{meta['id']}/omode.yaml`.
2. Read the incoming seed description.
3. Match the seed against the `modes[].trigger` entries (first match wins; use semantic similarity).
4. If no trigger matches, use `default_reasoning_strategy`.
5. Verify the selected strategy id exists as a folder under `.agents/skills/reasoning/`.
6. Return:
   ```yaml
   selected_strategy: <skill-id>
   frame_shape: <frame-shape>
   matched_trigger: "<trigger text or 'default'>"
   catalog_path: .agents/skills/reasoning/<skill-id>
   ```
7. If the skill id does not exist in the catalog, return a governed rejection — do not invent a fallback.

## Constraints

- Only return strategy ids that exist in `.agents/skills/reasoning/` as folders.
- Do not mutate `omode.yaml` or the reasoning catalog.
- All paths repository-relative.
"""


def render_thin_pointer(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    dw = spec["domain_word"]
    gname = f"govern-{dw}-intent"
    constraints = "\n".join(f"- {c}" for c in spec["constraints"])
    return f"""---
name: {meta['id']}
description: {spec['description'].strip()}
license: Apache-2.0
metadata:
  version: "{VERSION}"
  tier: DOMAIN
  capability_class: DOMAIN
  plugin_path: plugins/{meta['id']}
---

# {meta['display_name']}

## Purpose

{spec['description'].strip()}

## When to Use

- {dw.capitalize()} strategy, planning, or decision-making tasks for the AI Agent Company

## When Not to Use

- Core lifecycle operations (orchestrate / plan / make / check / reflect / trail initialize)
- Any action that would violate PMCRO laws (evidence, checker-gate, plugin isolation, output contract)

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `{gname}` | Produce a governed {spec['frame_shape']} from a {dw} seed |
| `select-reasoning-strategy` | Pick the right reasoning strategy from omode.yaml + catalog |

## Plugin

Full implementation: [`plugins/{meta['id']}`](plugins/{meta['id']})
OMode map: [`plugins/{meta['id']}/omode.yaml`](plugins/{meta['id']}/omode.yaml)

## Constraints

{constraints}

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: {meta['id']})
- Reasoning catalog: `.agents/skills/reasoning/`
"""


def render_directory_entry(data: dict[str, Any]) -> str:
    meta, spec = data["metadata"], data["spec"]
    dw = spec["domain_word"]
    gname = f"govern-{dw}-intent"
    return f"""
  - id: {meta['id']}
    kind: persona
    display_name: {meta['display_name']}
    description: >
      {spec['description'].strip()}
    owner_role: {spec.get('owner_role', 'reflector')}
    capabilities: []
    skills:
      - name: {gname}
        path: plugins/{meta['id']}/skills/{gname}
        tier: DOMAIN
      - name: select-reasoning-strategy
        path: plugins/{meta['id']}/skills/select-reasoning-strategy
        tier: DOMAIN
    packaging:
      - target: agentskills
        path: plugins/{meta['id']}
      - target: maf-inline
        path: src/Agents/{meta['id']}
    status: experimental
    marketplace_visible: true
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-root", default=".")
    parser.add_argument("--directory", default=".pmcro/directory")
    parser.add_argument("--catalog", default=".agents/skills/reasoning")
    args = parser.parse_args()

    root = Path(args.output_root)
    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"FAIL: spec not found: {spec_path}", file=sys.stderr)
        return 2

    data = load_spec(spec_path)
    errors = validate(data, root / args.catalog)
    if errors:
        print("REJECT")
        for e in errors:
            print(f"  - {e}")
        return 1

    meta, spec = data["metadata"], data["spec"]
    dw = spec["domain_word"]
    gname = f"govern-{dw}-intent"
    plugin_dir = root / "plugins" / meta["id"]
    thin_dir = root / ".agents" / "skills" / meta["id"]

    files = {
        plugin_dir / "plugin.json": render_plugin_json(data),
        plugin_dir / "omode.yaml": render_omode_yaml(data),
        plugin_dir / "skills" / gname / "SKILL.md": render_govern_skill(data),
        plugin_dir / "skills" / "select-reasoning-strategy" / "SKILL.md": render_select_reasoning_skill(data),
        thin_dir / "SKILL.md": render_thin_pointer(data),
    }

    for out_path, content in files.items():
        if DRIVE_LETTER_RE.search(str(out_path)) and not str(out_path).startswith(str(root)):
            print(f"REJECT: path escapes output root: {out_path}")
            return 1
        if args.dry_run:
            print(f"[dry-run] would write {out_path}")
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8")
            print(f"wrote {out_path}")

    if args.register:
        agents_file = root / args.directory / "agents.yaml"
        if agents_file.is_file():
            text = agents_file.read_text(encoding="utf-8")
            if f"id: {meta['id']}" in text:
                print(f"directory already contains id={meta['id']} — skip")
            elif args.dry_run:
                print(f"[dry-run] would register {meta['id']}")
            else:
                with agents_file.open("a", encoding="utf-8") as f:
                    f.write(render_directory_entry(data))
                print(f"registered {meta['id']} in {agents_file}")
        else:
            print(f"WARNING: {agents_file} not found — skip register")

    print(f"OK: {meta['id']} scaffolded ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
