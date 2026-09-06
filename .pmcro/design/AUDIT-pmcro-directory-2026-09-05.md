# .pmcro/ Structural Audit — 2026-09-05

Full read of `.pmcro/` (all subfolders + key files) to answer: does the
directory structure need upgrading/optimizing/refining? Findings below.
No changes made — this is an audit, not a fix.

## 1. Real, load-bearing gap already self-identified in this repo — FIXED 2026-09-05 (option a)

`.pmcro/directory/agents.yaml` marks `pmcro-trail`, `pmcro-orchestrator`,
`pmcro-planner`, `pmcro-maker`, `pmcro-checker`, `pmcro-reflector` all as
`status: active`, `marketplace_visible: true`, pointing at
`plugins/pmcro-orchestrator` etc. **None of those 6 plugin directories exist
under `plugins/`.** Only the 12 `pmcro-chief-*-officer` persona plugins and
`pmcro-marketplace-directory` actually exist. This is already flagged by this
repo's own `.pmcro/design/RECONCILIATION-older-application-session.md` and a
matching queued seed, `.pmcro/queue/seed-close-lifecycle-plugin-gap.json`
(priority 20, still open/unclaimed) — not a new finding, but the single
biggest real gap in the directory.

## 2. Three-way conflict on whether `trail` is its own role — FIXED 2026-09-05

- `.pmcro/manifest.yaml` -> `active_roles` lists 6: orchestrator, planner,
  maker, checker, reflector, **trail**.
- `.pmcro/laws/laws.yaml` + `.pmcro/policies/permissions.yaml` -> only 5
  roles defined; no `trail` role anywhere; Reflector is `may: [..., seal-cycle]`.
- `.pmcro/directory/agents.yaml` -> registers `pmcro-trail` as its own
  **lifecycle** agent, distinct scope from Reflector ("Class-B durable trail
  materializer and link verifier. Owns the evidence-store shape every cycle
  writes into" vs. Reflector's "Records disposition ... seals the trail").
- This chat's own decision (see `role-design-decisions.md`) -> only 5 skills,
  no separate trail skill, sealing folded into Reflector.

Four sources, two different answers.

**Fix applied:** `manifest.yaml` `active_roles` now lists 5 (trail removed,
with an inline comment pointing here). `agents.yaml`'s `pmcro-trail` entry
is now `status: deprecated`, `marketplace_visible: false`, `owner_role:
reflector`, with its description redirected to Reflector's seal-cycle
permission. `laws.yaml`/`permissions.yaml` needed no change — already
5-role. All governing files now agree.

## 3. Registry convention vs. reality — FIXED 2026-09-05 (providers/README.md)

`.pmcro/README.md`'s directory map and this repo's own reference lists
(e.g. the PMCRO Framework project's old instructions) expect
`capabilities/registry.yaml`, `providers/registry.yaml`, `mcp/registry.yaml`
as aggregate files. What actually exists: `capabilities/` has one real file
(`hyperlight-codeact.yaml`, a single capability, well-formed and honestly
marked `status: planned` / `defaultEnabled: false`) plus a README; `providers/`
and `mcp/` have only README placeholders, no registry file at all. Not
broken, but worth a decision: adopt a flat-file-per-capability convention
(current pattern, arguably cleaner) and update the README to say so
explicitly, rather than leaving a "registry.yaml" naming expectation that
nothing on disk follows.

## 4. What's already good (don't touch)

- `laws.yaml` / `permissions.yaml` / `runtime/config.yaml` /
  `runtime/output-contract.md` are internally consistent, honest about
  status, and match the 5-role model.
- One real sealed trail exists (`trails/f050979c-.../`), 5 phase files +
  `trail.json`, `status: sealed` — proves the trail-write mechanics work
  even without a built Orchestrator plugin (this one was hand-driven this
  session, per `seed_intent`: "Autonomous PMCRO loop: command-style design,
  runtime .pmcro updates...").
- `queue/` already has real done items and one real open seed, using the
  actual `SeedIntent` schema, not placeholders.
- `capabilities/hyperlight-codeact.yaml` is a good example of the honesty
  convention working as intended: preview package, `defaultEnabled: false`,
  empty `providers: []` until real, explicit escalate-don't-invent rule.

## 5. Recommended order of operations — DONE 2026-09-05, all three fixed

All three items above are now resolved. Order followed: #2 (small, no
dependencies) -> #1 (the real blocker, option (a): built
plugins/pmcro-{orchestrator,planner,maker,checker,reflector}/ fresh, each
with plugin.json + SKILL.md, plus `.agents/skills/pmcro-<role>/SKILL.md`
discovery mirrors matching the existing Chief-plugin pattern; grounded in
this repo's own laws.yaml/permissions.yaml/output-contract.md and the real
sealed trail's frame shapes, not copied from P:\ProjectName's PowerShell)
-> #3 (cosmetic). Resolution recorded in
`.pmcro/queue/done/seed-close-lifecycle-plugin-gap.json`.

Not yet done, out of scope for this pass: no actual runtime/CLI that
dispatches these skills automatically exists yet (Orchestrator still needs
something - a human, Claude session, or later a .NET host - to invoke
`/pmcro-orchestrator:orchestrate` and walk the chain). The skills are real
and complete; the automation loop around them is not.

## 6. Trail lifecycle CLI added — 2026-09-05 (later same day)

`.pmcro/runtime/trail_runtime.py` now exists: a stdlib-only CLI with
`open`/`plan`/`make`/`check`/`reflect`/`status` subcommands that mints a
trail, appends each phase's frame in order, and seals on Reflect. It is
mechanical only - it does not decide plan/make/check/reflect *content*,
an LLM or agent still supplies that - but it replaces hand-copying trail
JSON files each cycle with one command per phase, and it enforces two real
gates in code rather than by convention: `check` rejects any verdict other
than `PASS`/`FAIL`, and `reflect` refuses `SEAL` unless the trail's own
`04-check.json` verdict is `PASS` (L-CHECKER-GATE). Verified end-to-end via
a real self-test trail (`7a2d2732-9203-43dd-af15-2a80e66ee889`, sealed):
confirmed the invalid-verdict rejection fires, confirmed seal-before-PASS
is blocked, then confirmed a real PASS -> SEAL path writes all five phase
files, seals `trail.json`, and clears `state/active_trail_id.txt`.

This closes the CLI-plumbing half of the gap noted in section 5 above.
Still open, unchanged: no automated *dispatcher* invokes the loop on its
own initiative (queue-watching, scheduling, or a .NET host driving it) -
something still has to run each `trail_runtime.py` command and supply
each phase's actual content.

## Source

Full listing + read of `.pmcro/` on 2026-09-05, cross-referenced against
`role-design-decisions.md` (same folder) and this repo's own
`design/RECONCILIATION-older-application-session.md`.
