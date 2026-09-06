# Role Design Decisions

## Lifecycle skills (decided)

Only 5 lifecycle skills needed — no separate `pmcro-trail` skill. Trail sealing
is owned by Reflector, per this repo's own `.pmcro/README.md` contract.

- **orchestrator** — opens trail cycles; owns the high-level goal for the cycle;
  dispatches into the macro loop (routes to the relevant Chief).
- **planner** — plans the bare minimum, grounded in validated/dated resources
  (not stale assumptions).
- **maker** — executes one step at a time, produces evidence.
- **checker** — independently gates Maker's output against Planner's success
  criteria only (no re-planning, no re-doing the work).
- **reflector** — dispositions the cycle, seals the trail, and promotes
  Earned Constraints **unconditionally, every cycle** (not gated on PASS or on
  a Checker flag).

## Macro layer

The 12 Chiefs are not a 6th lifecycle role. They are the macro-loop domain
executors. Flow: Orchestrator opens a cycle around a high-level goal ->
routes to the relevant Chief (CFO, CTO, whichever domain the goal touches) ->
that Chief's own inner Plan->Make->Check->Reflect cycle runs using the 5
lifecycle skills -> Reflector's Earned Constraints feed forward so the next
macro cycle inherits what was learned instead of starting cold.

## Manifest conflict (open — needs a fix)

`.pmcro/manifest.yaml` currently lists
`active_roles: [orchestrator, planner, maker, checker, reflector, trail]` —
six entries, with `trail` still listed separately. Per the "only 5 skills"
decision above, `trail` should be dropped from `active_roles` (or explicitly
annotated as "folded into reflector," not a standalone role) so the manifest
doesn't imply a 6th skill needs building.

## Naming-rule conflict (RESOLVED — rule is outdated)

Resolved: the "PMCRO must never appear" rule below is outdated. This project
(AgentSkills.Template) is the upgraded/current version and supersedes it.
`.pmcro/` and `pmcro-chief-*` naming stays as-is — no rename pass needed.

Original conflict, kept for record:

A separate prior Claude.ai project memory (Agent Skills Project Template,
project id `01a041e6-b55c-7659-9a22-bdaadbcde7cf`) states as an explicit,
already-agreed rule:

> "PMCRO" must never appear in the `AgentSkills.Template` scaffold or related
> work — use "agents" / "AGENTS" / "AGENTS runtime spec" instead.

This repo's actual disk state contradicts that rule throughout: `.pmcro/`
folder name, 12 `pmcro-chief-*` plugin/skill folders, `pmcro-marketplace-directory`,
etc. Either:
(a) that naming rule was superseded/abandoned and this repo is the intentional
    exception, or
(b) this repo needs a rename pass (`.pmcro/` -> something like `.agents-runtime/`,
    `pmcro-chief-*` -> `agents-chief-*`) to comply with the rule.

Do not rename anything until the user explicitly picks (a) or (b).

## Export audit (full read, 2026-09-05) — no macro/micro found, but a correction surfaced

Read every file in the four uploaded Claude.ai export zips in full:
`conversations.json` is empty (`[]`). The memories export contains two
project-memory summaries (Z:\pmcro-skills/pmcro-runtime "PMCRO Framework",
and P:\agent-skills "Agent Skills") plus 6 project docs/prompt_templates.
Grepped everything for "macro"/"micro" — the only hits are false positives
(substrings of "Microsoft", "mcro-runtime"). No prior session actually used
macro/micro terminology in the exported data; that framing came from this
conversation only.

**Correction, sourced from this Claude session's own installed
`pmcro-skills:orchestrate` / `pmcro-loop` skill content (not the export) —
applying Anthropic's orchestrator-workers / routing agentic design
patterns** — one line there directly overrides what we tentatively agreed
earlier in this file:

> "C-suite plugins supply domain scope (Owns / Does-not-own), never their
> own loop." / "Orchestrator is the only role that dispatches."

So the "macro/micro" framing needs a correction: **there is only one loop**
(Orchestrator -> Planner -> Maker -> Checker -> Reflector), dispatched
centrally by Orchestrator every time. A Chief is not a nested independent
PMCR-O cycle-runner — a Chief is domain **scope** (an Owns/Does-Not-Own
boundary + reasoning-strategy set) that Planner/Maker/Checker consult for
*that* cycle, selected by Orchestrator's routing step (classic
"routing"/orchestrator-workers pattern: classify the work, route to the
smallest suitable specialist scope). Earlier wording in this file ("that
Chief's own inner Plan->Make->Check->Reflect cycle runs") should be read as
superseded by this.

Other reusable detail pulled from the same installed skill content:
Orchestrator's priority scale is `0 stop-the-line -> 1 CEO/CoS -> 2 domain
critical -> 3 normal -> 4 backlog`; only Reflector policy or CEO/CoS may
reorder it, never invented ad hoc.

## Source

Distilled from a Claude.ai chat session on 2026-09-05, cross-referenced
against a separate uploaded project-memory export (Claude.ai privacy export,
projects-000.zip / memories-000.zip) covering two related but distinct
repos: `Z:\pmcro-skills` / `pmcro-runtime` (PMCR-O Colony framework) and
`P:\agent-skills` (Agent Skills Marketplace, home of the PMCRO-naming-ban rule
above). Neither of those repos is the same path as this one
(`C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template`).
