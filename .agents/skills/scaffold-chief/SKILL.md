---
name: scaffold-chief
description: Generic template-driven declarative scaffolder for PMCRO Chief persona plugins. Reads a ChiefSpec YAML and renders all Chief plugin artifacts. USE FOR creating or re-rendering any C-Suite Chief plugin from spec. DO NOT USE for lifecycle core plugins (use scaffold-skill instead).
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: DOMAIN
  capability_class: DOMAIN
  plugin_path: .agents/skills/scaffold-chief
---

# scaffold-chief

## Purpose

Generic template-driven declarative scaffolder for PMCRO C-Suite Chief persona plugins.
Given a `ChiefSpec` YAML, renders all five artifacts for a Chief plugin without
any hand-coding. Adding a new Chief to the company = write one YAML spec, run the scaffolder.

## When to Use

- Creating a new Chief persona plugin from scratch
- Re-rendering an existing Chief plugin after spec changes
- Scaffolding the full C-Suite from `csuite/csuite.yaml`

## When Not to Use

- The six lifecycle core plugins (orchestrator, planner, maker, checker, reflector, trail) — use `scaffold-skill` instead
- Non-Chief persona scaffolding — use `scaffold-skill`
- Opening, sealing, or executing a PMCRO cycle

## Skills

### scaffold-chief (CLI: scaffold_chief.py)

Reads a `ChiefSpec` YAML file, validates against `chief-spec.schema.json`,
and renders five output files per Chief:

| Output | Template |
|---|---|
| `plugins/<id>/plugin.json` | `plugin.json.tmpl` |
| `plugins/<id>/omode.yaml` | `omode.yaml.tmpl` |
| `plugins/<id>/skills/govern-<domain>-intent/SKILL.md` | `govern-intent.SKILL.md.tmpl` |
| `plugins/<id>/skills/select-reasoning-strategy/SKILL.md` | `select-reasoning.SKILL.md.tmpl` |
| `.agents/skills/<id>/SKILL.md` | `agent-entry.SKILL.md.tmpl` |

CLI usage:
```bash
# Single spec
python .agents/skills/scaffold-chief/scripts/scaffold_chief.py \
  --spec csuite/specs/pmcro-chief-financial-officer.yaml \
  [--dry-run] [--register] [--output-root .]

# Entire C-Suite from manifest
python .agents/skills/scaffold-chief/scripts/scaffold_chief.py \
  --all csuite/csuite.yaml \
  [--dry-run] [--register] [--output-root .]
```

## ChiefSpec format

See `assets/schemas/chief-spec.schema.json` for the JSON Schema.
See `csuite/specs/` for canonical examples.

Key fields:
- `spec.domain` — single word; drives `govern-<domain>-intent` skill naming
- `spec.intent_frame_kind` — e.g. `FinancialIntentFrame`
- `spec.omode.modes[]` — list of trigger → reasoning_strategy → frame_shape mappings
- `spec.omode.default_reasoning_strategy` — fallback strategy id

## Constraints

- Refuses (exit 1) on placeholder tokens (TODO/FIXME/XXX/CHANGEME/TBD/FILLME).
- Refuses on absolute paths in spec.
- All output paths must be repository-relative.
- Never invent capabilities. All reasoning_strategy ids must exist in `.agents/skills/reasoning/`.
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.

## References

- Schema: `.agents/skills/scaffold-chief/assets/schemas/chief-spec.schema.json`
- Templates: `.agents/skills/scaffold-chief/assets/templates/`
- Script: `.agents/skills/scaffold-chief/scripts/scaffold_chief.py`
- C-Suite specs: `csuite/specs/`
- C-Suite manifest: `csuite/csuite.yaml`

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
