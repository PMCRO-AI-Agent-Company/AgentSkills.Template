#!/usr/bin/env python3
"""
Render a ReasoningStrategySpec into the real agents/<id>.md convention used by
plugins/pmcro-omode. Declarative source -> generated projection,
the same principle as .pmcro/design/DECLARATIVE-GENERATIVE-AGENT-TEMPLATE.md,
applied to a genuinely different rendering convention (this one, not the
AgentScaffoldSpec/SKILL.md one scaffold.py already covers).

Usage:
  python render_strategy.py --spec specs/chain-of-thought.spec.yaml [--dry-run]

Refuses (exit 1) on schema violations. Writes nothing on refusal.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "schemas" / "reasoning-strategy-spec.schema.json"

# Every real strategy file (non-selector) shares this exact laws/permissions
# block - confirmed by reading chain-of-thought.md and self-refine.md in
# full. Never re-derive this per spec; a spec that wants something different
# is not this generator's job (it would be a new kind, not a bug here).
SHARED_LAWS = ["L-EVIDENCE", "L-CHECKER-GATE", "L-PLUGIN-ISOLATION", "L-OUTPUT-CONTRACT"]
SHARED_MAY = ["apply-reasoning-strategy"]
SHARED_MAY_NOT = [
    "execute-provider-action", "seal-cycle", "issue-disposition",
    "rewrite-laws", "select-reasoning-strategy",
]


def load_spec(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise SystemExit("PyYAML is required. pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be a mapping")
    return data


def validate_spec(data: dict[str, Any]) -> list[str]:
    if jsonschema is None:
        return []
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft7Validator(schema)
    return [f"{'.'.join(str(p) for p in e.path)}: {e.message}" for e in validator.iter_errors(data)]


def render(spec: dict[str, Any]) -> str:
    r = spec["reasoning"]

    def bullets(items):
        return "\n".join(f"- {x}" for x in items)

    def numbered(items):
        return "\n".join(f"{i + 1}. {x}" for i, x in enumerate(items))

    steps_desc = spec.get("steps_description")
    steps_part = f"`steps` ({steps_desc.strip()})" if steps_desc else "`steps`"

    frontmatter = f"""---
id: {spec['id']}
package: pmcro-omode
kind: strategy
family: "{spec['family']}"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [{', '.join(SHARED_LAWS)}]
permissions:
  may: [{', '.join(SHARED_MAY)}]
  mayNot: [{', '.join(SHARED_MAY_NOT)}]
reasoning:
  logical_paradigms: [{', '.join(r['logical_paradigms'])}]
  operational_methods: [{', '.join(r['operational_methods'])}]
  domain_capabilities: [{', '.join(r['domain_capabilities'])}]
---"""

    body = f"""# {spec['id']}

## Purpose
{spec['purpose'].strip()}

## When to Use
{bullets(spec['when_to_use'])}

## When Not to Use
{bullets(spec['when_not_to_use'])}

## Workflow
{numbered(spec['workflow'])}

## Validation
{bullets(spec['validation'])}

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "{spec['id']}"`, {steps_part}, `result`{spec.get('output_extra_fields', '').strip()}."""

    trailing_note = spec.get("trailing_note", "").strip()
    if trailing_note:
        body += f"\n\n{trailing_note}"

    return frontmatter + "\n" + body + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a ReasoningStrategySpec")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output-root", default="plugins/pmcro-omode/agents")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"FAIL: spec not found: {spec_path}", file=sys.stderr)
        return 2

    data = load_spec(spec_path)
    errors = validate_spec(data)
    if errors:
        print("REJECT")
        for e in errors:
            print(f"  - {e}")
        return 1

    content = render(data)
    out_path = Path(args.output_root) / f"{data['id']}.md"

    if args.dry_run:
        print(f"[dry-run] would write {out_path}")
        print(content)
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"wrote {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
