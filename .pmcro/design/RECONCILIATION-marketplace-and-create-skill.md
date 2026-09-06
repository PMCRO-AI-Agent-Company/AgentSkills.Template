# Reconciliation — pmcro-marketplace zips + skill-forge create-skill

**Status:** In progress — see `.pmcro/queue/seed-finish-create-skill-and-marketplace-reconciliation.json`
**Date:** 2026-09-05
**Inputs:** 4 user-uploaded zips: `pmcro-marketplace-delivery.zip` (01:10),
`pmcro-followup-update.zip` (01:38-40), `pmcro-marketplace-agentskills-native.zip` (03:26,
confirmed superset/latest), `Skill_forge-0_1_0-v1.zip` (00:44-45, unrelated maintainer plugin
by Shawn/Tooensure LLC).

## Finding 1: `.agents/skills/create-skill` did not exist

`ADR-pmcro-agent-directory-and-marketplace.md` assumed `.agents/skills/create-skill` (v0.2.0)
already existed as "the narrow, lifecycle-plugin-only scaffolder." It did not exist anywhere
in this repo. `skill-forge`'s `skills/create-skill/` fills that path — **partially installed**:
`SKILL.md` and all 4 archetype templates (`workflow.yaml`, `reference.yaml`,
`script-driven.yaml`, `composite.yaml`) are in place. `scripts/scaffold.py`,
`references/spec-schema.md`, `references/maf-architecture.md`, the 4 MAF code-templates, and
`evals/evals.json` are **not yet transferred** — filed in the queue item above.

## Finding 2: create-skill and scaffold-skill are NOT cleanly separated by scope

The ADR's conflict-resolution table (§6) assumed `create-skill` = narrow/six-lifecycle-plugins,
`pmcro-marketplace/scaffold-skill` = generic/multi-archetype/multi-runtime. In reality,
skill-forge's `create-skill` is *itself* generic and multi-archetype/multi-runtime (same four
archetypes: workflow/reference/script-driven/composite; same SKILL.md + MAF C#/Python targets).
**This is a real, unresolved overlap**, not something this reconciliation silently picked a
side on. Left for the queued follow-up / a human decision.

## Finding 3: All 3 marketplace zips are snapshots; native is the latest

`pmcro-marketplace-agentskills-native.zip` (03:26) is a strict superset of the other two —
it adds `agentskills-native-target-design.md`, `references/agentskills-native-target.md`, and
an `agentskills-native` example spec on top of everything in `followup` (deploy-cloudflare
example, dotnet packaging refs) and `delivery` (`.claude-plugin/plugin.json`,
`marketplace-architect.md`). Plugin identity: `pmcro-marketplace`, v0.1.1. **Not yet installed**
into `plugins/` — this repo's `plugins/pmcro-marketplace-directory` (v0.2.0, Python-based MVP)
is untouched and still the only marketplace scaffolder actually present on disk.

## Applied fix while transferring

Every file under `.agents/skills/` is shared across `.claude/`, `.gemini/`, `.grok/` per this
repo's multi-platform convention — the skill-forge source text addressed "Claude" directly in
several places (e.g. "steps Claude should follow"). Genericized to "the agent" throughout the
files actually transferred so far. Apply the same check to any remaining files transferred
under the queued follow-up.

## Resolution — 2026-09-06

Both open items closed, on re-verified evidence (not the zip files, which are not reachable from this
environment):

1. **Finding 1/2 (create-skill scope overlap):** already resolved independently on 2026-09-05 — see
   `.agents/skills/create-skill/SKILL.md` `metadata.revision_note` (v0.3.0). `create-skill` dropped the
   scaffold.py/JSON-spec/MAF-codegen pipeline entirely in favor of template-copy + archetype-selection +
   `scripts/validate_skill_md.py` drift-checking. Its own description now explicitly routes multi-target
   (agentskills + MAF-inline) codegen work to `scaffold-skill` instead. The queue item's premise ("scaffold.py
   still needs to be transferred from the skill-forge zip") is stale — that plan was abandoned, not merely
   incomplete.
2. **Finding 3 (marketplace zip reconciliation):** resolved as **supersede**, recorded in
   `ADR-pmcro-agent-directory-and-marketplace.md` §11. `plugins/pmcro-marketplace-directory/skills/scaffold-skill`
   already implements and evaluates what the zip-only `pmcro-marketplace-agentskills-native` (v0.1.1) proposed;
   nothing from the zip was installed, since its content is not accessible from this session.

`seed-finish-create-skill-and-marketplace-reconciliation.json` moved to `.pmcro/queue/done/` accordingly.
