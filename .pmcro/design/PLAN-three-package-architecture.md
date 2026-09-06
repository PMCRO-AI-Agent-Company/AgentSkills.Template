# PLAN — Three-Package Architecture Redesign

Status: **COMPLETE.** *(Corrected 2026-09-06 — see
`.pmcro/design/AUDIT-claude-architecture-review-2026-09-06.md`. The line
below this note is the ORIGINAL status text, left for the historical
record; it was accurate when written and then went stale as the work
below was actually completed, across more than one session, without this
document being updated.)*

~~Status: **APPROVED, NOT STARTED.** Parallel subagent execution was launched
in a prior session to build all three packages simultaneously, then
cancelled by the user before any package was completed. No files exist on
disk for this redesign. No trail was opened or sealed for it.~~

**Verified state, 2026-09-06:** all three packages exist on disk in the
single-file `agents/*.md` + `output_schema` convention described below.

| Package | On disk as | Status |
|---|---|---|
| `pmcro/` (lifecycle core) | `plugins/pmcro/agents/{orchestrator,planner,maker,checker,reflector}.md` | Complete. Has trail evidence: sealed, Checker-verified trail `2bdd6a2b-ef29-4f66-b0db-3eb339907e87`. |
| `pmcro-csuite/` (12 Chiefs) | `plugins/pmcro-csuite/agents/{ceo,cto,...}.md` | Complete. **No trail evidence found** for this migration/consolidation - it exists correctly on disk, but nothing in `.pmcro/trails/` documents it going through Orchestrator->Planner->Maker->Checker->Reflector. Not retroactively fabricating a trail for already-completed work; noting the gap here instead. |
| `dynamic-reasoning/` (35 strategies + selector) | `plugins/pmcro-reasoning-strategy/agents/*.md` | Complete, under a **different final name** than this doc originally proposed. `plugins/pmcro-reasoning-strategy/plugin.json` says so directly: "Renamed from the interim 'reasoning-strategy' / 'dynamic-reasoning' folder names." **No trail evidence found** for this one either. |

Open questions below are resolved in practice as follows (verified against
the actual code/files, not re-decided here):

- **Q1 (top-level vs nested):** top-level, as built (`plugins/pmcro/`, not
  `.agents/packages/pmcro/`).
- **Q2 (src/Agents C# stubs):** not built. `src/` has no `Agents/` folder.
  `.pmcro/directory/agents.yaml` was, until this same audit pass, wrongly
  claiming these existed - now corrected to `status: planned-not-yet-built`.
- **Q3 (selector always vs conditional):** always invoked, as part of a
  Chief's `select-reasoning-strategy` step (`plugins/pmcro-csuite/skills/
  select-reasoning-strategy/SKILL.md` delegates to `agents/selector.md`
  every time it runs). The five lifecycle roles never select a reasoning
  family at all - each one's frontmatter sets `reasoning.allowed_families: []`.
- **Q4 (AgentSkillsProvider roots):** one parent root, not per-package.
  `MafWorkflowService.CreateSkillsProvider()` resolves a single
  `.agents/skills` directory (via `AGENT_SKILLS_ROOT` or by walking up from
  the executable) for all four MAF agents, `SearchDepth = 2`. There is no
  per-package root in the actual runtime.

## Objective

Restructure `AgentSkills.Template` from the current flat/mixed skill layout
into three top-level packages:

- `pmcro/` — lifecycle core (Orchestrator → Planner → Maker → Checker →
  Reflector)
- `pmcro-csuite/` — all 12 Chiefs consolidated (CEO, CTO, CLO, CCO, CDO,
  CFO, CHRO, CISO, CMO, COO, CPO, CRO)
- `dynamic-reasoning/` — all 35 reasoning strategies as invokable agents,
  plus a selector agent

## Core design idea — `agents/*.md` as single source of truth

Every role becomes one self-contained markdown file. Frontmatter combines
what is currently split across `agents.yaml`, `laws.yaml`, and
`permissions.yaml`:

```yaml
---
id: planner
package: pmcro
kind: lifecycle
output_schema:
  $ref: schemas/plan-frame.schema.json   # structured output, not prose
laws: [L-EVIDENCE, L-RESEARCH, L-OUTPUT-CONTRACT]
permissions:
  may: [propose-plan, define-success-criteria]
  mayNot: [execute-provider-action, seal-cycle]
reasoning:
  allowed_families: []        # lifecycle roles don't select strategies
---
# Planner
## System Prompt
...returns ONLY valid JSON matching schemas/plan-frame.schema.json...
```

`output_schema` tells the LLM host the agent must return JSON validating
against a schema — not free-form prose. Replaces convention-based parsing
with deterministic frame parsing, type-safe .NET deserialization in MAF, and
a one-line CI check (`jsonschema.validate()`).

## Open questions (unresolved)

1. Should `pmcro/` be top-level (alongside `src/`, `ui/`) or nested under
   `.agents/packages/pmcro/`?
2. Keep `src/Agents/pmcro-chief-*/` C# stubs in `src/`, or generate them
   from the new frontmatter?
3. Should `dynamic-reasoning/agents/selector.md` always be invoked, or only
   when no C-Suite chief is in the loop?
4. Does MAF `AgentSkillsProvider` need explicit roots for each package, or
   one parent root?

## Blocking issue found on disk — do not build on top of this silently

`.pmcro/state/active_trail_id.txt` still points to
`dd77d839-4df3-401e-a920-b21726b15a88`. That trail directory contains only
`01-orchestrate.jsonl` and `02-plan.json` — no make/check/reflect phases,
no `disposition.json`. It is stale/orphaned, not sealed. This was already
flagged in the original implementation plan as needing user confirmation
before any new trail work proceeds. Resolve (audit + reset, or confirm live
work) before opening a new trail for this redesign.

## Related existing gaps (from `.pmcro/design/AUDIT-pmcro-directory-2026-09-05.md`)

The 6 lifecycle plugin directories (`pmcro-trail`, `pmcro-orchestrator`,
`pmcro-planner`, `pmcro-maker`, `pmcro-checker`, `pmcro-reflector`) are
registered in `agents.yaml` as `status: active` but do not exist under
`plugins/`. Only the 12 chief persona plugins and
`pmcro-marketplace-directory` exist. This three-package redesign would
subsume and close that gap rather than fix it separately — worth sequencing
together.
