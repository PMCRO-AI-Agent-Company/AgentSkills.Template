# Reconciliation — Older "Application" Session (Gemini, `P:\ProjectName`)

**Status:** Informational reconciliation — no destructive action taken
**Date:** 2026-09-05
**Source:** User-uploaded Gemini chat export (`Building_a___1_.NET_CLI_Tool`), timestamped 2026-09-04
**Constraint:** `P:\ProjectName` is a superseded/older project location per user confirmation.
Canonical project going forward is `C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template`
(this repo). Do not port code verbatim from `P:\ProjectName` without a governed cycle.

---

## 1. What the older session actually validated (real, not hypothetical)

Working against `P:\ProjectName\.pmcro`, that session ran a **real, working PMCR-O engine**
using PowerShell scripts (`New-OrchestrateFrame`, `New-Trail.ps1`, `Complete-ReflectAndSeed.ps1`,
etc.) driven by six lifecycle plugins: `pmcro-orchestrator`, `pmcro-planner`, `pmcro-maker`,
`pmcro-checker`, `pmcro-reflector`, `pmcro-trail`. Two real, end-to-end cycles are documented:

- Trail `0aa1c59d-6941-4692-9d40-4b893eb9fe5d` — full 5-phase cycle; surfaced a genuine
  Planner defect (a success criterion asserting a Reflector-only outcome at Check-time) and a
  real script bug: `Complete-ReflectAndSeed.ps1`'s default `-QueueRoot` derivation walked up
  the wrong number of parent directories when `-PmcroRoot` was an absolute path, silently
  writing queue items to `P:\.pmcro\queue\` instead of the repo's own queue.
- Trail `fdd09c8b-6517-4858-a6d0-be15659aa649` — fixed the bug above by deriving `QueueRoot`
  from the already-resolved `$trailDir` ancestry instead of re-deriving from `$PmcroRoot`.
- Trail `b0088d9f-7dcb-4737-8de8-ac8ce7a2ca25` — added a permanent regression script
  (`Test-QueueRootDerivation.ps1`) and found a *second*, previously-unhit failure mode in the
  same code path (a hard `Join-Path` exception on the literal default relative path).

## 2. The architectural fork: two different C-Suite designs

That session then designed (conceptually, not yet fully implemented there) a
**"Chief IS the Orchestrator" cabinet model**: each Chief (`pmcro-ceo`, `pmcro-cto`,
`pmcro-ciso`, ...) owns its *own* full `planner.md` / `maker.md` / `checker.md` /
`reflector.md` cabinet and runs an independent PMCR-O cycle in its domain, cross-seeding
tasks into other Chiefs' queues via `.pmcro/artifacts/` and `.pmcro/evidence/` (signed
reports) or trail-to-trail citation.

**This repo instead implements a different, already-built model**: each of the 12 Chiefs
(see `.pmcro/directory/agents.yaml`) is a thin **intent-governance persona** — it has
exactly two skills (`govern-<domain>-intent`, `select-reasoning-strategy`), produces one
governed `<Domain>IntentFrame`, and hands off to the **same shared** five-role lifecycle
(Orchestrator → Planner → Maker → Checker → Reflector) rather than running its own cabinet.
See `plugins/pmcro-chief-*-officer/` for the pattern and
`plugins/pmcro-marketplace-directory/skills/scaffold-skill/scripts/scaffold_chief.py` for
the generator.

**These two models are not compatible as written** (shared-cycle vs. per-Chief cabinet).
No attempt has been made here to merge them — flagging the fork for a governed decision
rather than silently picking one. The intent-governance model is what's actually built and
registered; the cabinet model exists only as a design conversation in the uploaded chat log.

## 3. Concrete gap found while reconciling (not from the old session — found here)

`.pmcro/directory/agents.yaml` in **this** repo registers `pmcro-orchestrator`,
`pmcro-planner`, `pmcro-maker`, `pmcro-checker`, `pmcro-reflector`, and `pmcro-trail` as
`status: active`, `marketplace_visible: true`, pointing at `plugins/pmcro-orchestrator`,
`plugins/pmcro-planner`, etc. **None of those six directories exist under `plugins/` in
this repo** (verified via directory listing, 2026-09-05). Every Chief's
`govern-<domain>-intent` skill instructs "hand off to Orchestrator for cycle opening" —
but there is currently no Orchestrator to hand off to here. The only real, validated
implementation of these six lifecycle plugins that exists (in PowerShell, proven against
real bugs) lives in the superseded `P:\ProjectName` project, not in this one.

## 4. What this reconciliation does NOT do

- Does not copy any `.ps1` script from `P:\ProjectName` into this repo.
- Does not pick a C-Suite model (cabinet vs. intent-governance) on the user's behalf.
- Does not mark the `agents.yaml` lifecycle entries inactive — that's a real decision,
  not a cleanup, since the directory may be aspirational/planned rather than wrong.

## 5. Filed for governed follow-up

`.pmcro/queue/seed-close-lifecycle-plugin-gap.json` — proposes closing the gap in §3 as
its own PMCR-O cycle once a human or Reflector decision is made on scope (port a
.NET/PowerShell-equivalent lifecycle engine here vs. build one fresh vs. defer).
