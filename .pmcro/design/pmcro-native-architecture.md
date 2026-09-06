
# PMCR-O ↔ Native `.agents/` Architecture Mapping

**Status:** Resolves the command-taxonomy question raised in the 2026-09-05
Gemini/AI Studio session (trails a1b2c3.., b2c3d4.., c3d4e5f6..). That
session got as far as Step S1 (analysis) before a rate limit stopped it at
Step S2 (this document). Written from a live read of the actual repo via
Desktop Commander, not from the Gemini session's assumptions — several of
its working hypotheses are corrected below.

## 1. Command taxonomy — RESOLVED (plugin:skill, not verbs)

The Gemini session floated three options: `/pmcro:orchestrate`,
verb-based (`/activate`, `/govern`, `/trail`), or `/pmcro-csuite:seed-intent`.

**Actual answer, already live in this repo** (`.pmcro/design/COMMAND-CATALOG.md`):

| Command | Role |
|---------|------|
| `/pmcro-orchestrator:orchestrate` | Sole dispatch, opens a cycle |
| `/pmcro-planner:plan` | Produces a PlanFrame |
| `/pmcro-maker:make` | Executes one step + evidence |
| `/pmcro-checker:check` | Independent gate |
| `/pmcro-reflector:reflect` | Disposition + seal |

Invocation form is **`/plugin:skill`**, matching the dotnet/skills and
Claude Code plugin convention — not bare verbs, not a `csuite` namespace.
Natural language naming the skill also works as a fallback.

## 2. `.agents/` mapping — CORRECTED

The Gemini session hypothesized a four-way split: personas → `.agents/agents/`,
loop skills → `.agents/skills/`, verb commands → `.agents/commands/`,
laws → `.agents/rules/`.

**Reality, confirmed by live directory listing:** only two of those exist.

| Gemini hypothesis | Actually exists? | What's really there |
|---|---|---|
| `.agents/agents/` (personas) | **No** | Personas are `.agents/skills/pmcro-chief-*-officer/SKILL.md` — skills, not a separate agents/ folder |
| `.agents/skills/` (loop + reasoning) | **Yes** | Holds all 12 Chief skills, 5 lifecycle skills (pmcro-orchestrator/planner/maker/checker/reflector), 33 reasoning skills, plus scaffold-skill/scaffold-chief/register-agent/pack-source/create-skill |
| `.agents/commands/` (verbs) | **No** | Does not exist. No verb-command layer at all — invocation is plugin:skill only |
| `.agents/rules/` (laws) | **No** | Laws/policies live only in `.pmcro/laws/laws.yaml` and `.pmcro/policies/*.yaml`, never projected into `.agents/` |
| `.agents/plugins/` | **Yes** (Gemini didn't predict this) | `marketplace.json` — the actual plugin registry |

So the real split is **two folders, not four**: `.agents/plugins/` (marketplace
registry) and `.agents/skills/` (every skill, personas and lifecycle and
reasoning alike, undifferentiated by folder — differentiated by name prefix
and by the Agent Directory's `owner_role`/`status` metadata instead).

## 3. State, trails, queue, laws — unchanged, `.pmcro/`-only

Confirmed still correct from prior analysis: `.pmcro/state/`, `.pmcro/trails/`,
`.pmcro/queue/`, `.pmcro/laws/`, `.pmcro/policies/` are workspace-runtime
constructs and are **never** projected into `.agents/`. This matches the
existing portability principle (`.agents/` = shareable across hosts,
`.pmcro/` = this workspace's own state).

## 4. Role count — RESOLVED at 5, not 6

`manifest.yaml`'s `active_roles` previously listed 6 (including `trail`);
patched 2026-09-05 to 5 (orchestrator/planner/maker/checker/reflector).
Sealing a trail is a Reflector permission (`seal-cycle` in
`policies/permissions.yaml`), not a standalone role or skill. See
`AUDIT-pmcro-directory-2026-09-05.md` §2 for the four-source conflict this
resolved (manifest vs. laws vs. agents.yaml vs. this repo's own
`role-design-decisions.md` — all four now agree).

## 5. "What is a command skill" — answered

A "command skill" in this repo is not a distinct artifact type. It is a
normal `SKILL.md` (frontmatter: `name`, `description`, optional
`allowed-tools`) registered under a `plugins/<plugin>/skills/<name>/` source
of truth and projected into `.agents/skills/<name>/`. There is no separate
single-file "command" format the way `.claude/commands/*.md` works in some
other tooling — PMCRO's plugin:skill model absorbs that role.

## 6. Open items (not resolved by this document)

- No automated dispatcher yet invokes the lifecycle loop on its own —
  `.pmcro/runtime/trail_runtime.py` provides the mechanical
  open/plan/make/check/reflect CLI, but something (human, Claude session,
  or a future .NET host) still has to drive each phase call.
- `.pmcro/directory/agents.yaml`'s six lifecycle-plugin entries were
  pointing at plugin directories that didn't exist as of 2026-09-05 morning;
  fixed same day per the audit (§1/§5) by scaffolding
  `plugins/pmcro-{orchestrator,planner,maker,checker,reflector}/` — worth a
  fresh directory listing to confirm this write actually landed, since this
  document is based on a read taken after that fix was recorded but the
  plugins/ listing above only showed `pmcro`, `pmcro-csuite`,
  `pmcro-marketplace-directory`, `pmcro-reasoning-strategy` — not the five
  individual lifecycle plugin dirs the audit says it created. Worth
  reconciling before treating §1's table as fully deployed vs. still
  aspirational.
