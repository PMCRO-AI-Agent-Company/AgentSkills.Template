---
name: scaffold-skill
description: Generic template-driven declarative scaffolder for AgentSkills plugins and personas. Accepts an AgentScaffoldSpec, validates it, refuses on violation, then renders agentskills and maf-inline (C#) packaging targets. USE FOR creating new domain/persona/tool skills from a single declarative spec. DO NOT USE for the six core lifecycle plugins (use create-skill instead) or for opening/sealing cycles.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: GOVERNANCE
  capability_class: MARKETPLACE
---

# scaffold-skill (MVP)

## Purpose

Turn a single declarative `AgentScaffoldSpec` into one or more packaged skills while enforcing PMCRO invariants:

- Validate before any write
- Refuse cleanly on placeholder tokens, unevidenced capabilities, or absolute/drive-letter paths
- Render only the requested packaging targets
- Optionally register the new agent in the Agent Directory
- Never touch `.agents/skills/create-skill` or any parallel-session marketplace work

## When to Use

- You have a clear declarative spec for a new persona, domain skill, or tool skill
- You want multi-target packaging (Agent Skills first; MAF later)

## When Not to Use

- Scaffolding the six core lifecycle plugins → use the existing `create-skill`
- Opening a cycle or sealing a trail → use orchestrator / reflector
- Inventing capabilities that do not exist in `.pmcro/capabilities/`

## Command

```text
/pmcro-marketplace-directory:scaffold-skill run --spec <path-to-AgentScaffoldSpec.yaml>
```

See `assets/command.scaffold.asset.md` for the full contract.

## Workflow

1. Load and parse the AgentScaffoldSpec.
2. Validate against `assets/schemas/scaffold-spec.schema.json` (and the directory schema rules).
3. Refuse if any of the following are true:
   - Spec fails schema validation
   - `id` or skill names contain placeholder tokens (`TODO`, `FIXME`, `xxx`, `changeme`, …)
   - Any path contains a drive letter or absolute host path
   - Declared capabilities are not present in `.pmcro/capabilities/` (or explicitly allowed as “planned”)
4. For each requested packaging target (agentskills | maf-inline), render the corresponding template.
5. Write outputs only under the paths declared in the spec (repository-relative).
6. Optionally upsert the Agent Directory entry via `register-agent`.
7. Emit a governed result that satisfies the runtime output contract.

## Validation Rules (MVP)

- `metadata.id` must match `^[a-z0-9]+(-[a-z0-9]+)*$`
- No absolute paths, no `P:\`, no `C:\`, no `/Users/…` style host paths
- `spec.description` ≥ 20 characters
- At least one packaging target
- Capabilities must be empty or resolve to known entries (MVP allows empty)

## References

- `assets/command.scaffold.asset.md`
- `assets/run.scaffold.asset.md`
- `assets/reject.scaffold.asset.md`
- `assets/schemas/scaffold-spec.schema.json`
- `assets/templates/agentskills/`
- `scripts/scaffold.py`
- `../../../../.pmcro/design/ADR-pmcro-agent-directory-and-marketplace.md`
