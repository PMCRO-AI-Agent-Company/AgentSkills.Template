# AgentSkills.Template — PMCR-O Architecture Audit

**Date:** 2026-09-06 (original audit) + **follow-up work same day**, see the addendum at the bottom of this document for what was actually changed after the user delegated the remaining decisions.
**Scope:** `C:\Users\org.tooensure\Downloads\AgentSkills.Template\AgentSkills.Template`, read-only inspection via the connected device bridge for the original audit below. No files were modified during that pass; the addendum documents a later, separate pass where real edits were made.
**Method:** Direct file reads (`.pmcro/`, `.agents/`, `plugins/`, `src/`, `mcp/`, `ui/`, root docs), plus cross-referencing every claim in the repo's own design docs against what is actually present on disk. Where a claim in a doc or registry could not be confirmed by a file that exists, it is marked accordingly below.

This repo already contains an extensive, largely honest self-audit trail (`.pmcro/design/AUDIT-pmcro-directory-2026-09-05.md`, `RECONCILIATION-*.md`, `pmcro-native-architecture.md`, sealed trails). I did not take those documents' conclusions on faith — I re-verified the load-bearing claims against the live filesystem. In most cases they held up; in a few places they are themselves now stale (documented below). One important negative finding up front: **the terms "Federation" and "Federation Board" do not appear anywhere in this repository's current documentation, code, or registries.** That concept exists only in your prior mental model (and possibly the superseded `P:\ProjectName` session) — not in this codebase. Section D addresses where it *would* map if reintroduced.

---

## 1. What is the current canonical PMCR-O architecture?

Two independent, **currently disconnected** systems both call themselves "PMCR-O," at different layers:

**(A) The governance/evidence layer — `.pmcro/`.** A five-role cycle — **Orchestrator → Planner → Maker → Checker → Reflector** — defined by `.pmcro/manifest.yaml`, `.pmcro/laws/laws.yaml`, and `.pmcro/policies/permissions.yaml`, all three mutually consistent. Cycles are recorded as "trails" (GUID-named folders under `.pmcro/trails/`, one JSON/JSONL file per phase, sealed by Reflector). A stdlib-only Python CLI, `.pmcro/runtime/trail_runtime.py`, mechanizes opening/advancing/sealing a trail and **enforces** two real gates in code: a Checker verdict must be `PASS`/`FAIL` (nothing else), and Reflector cannot `SEAL` unless the linked Checker verdict was `PASS`. This is real, tested, working software (self-test trail `7a2d2732-...`, sealed, confirms both gates fire).

**(B) The application runtime — `src/` + `mcp/`.** A .NET 11 / Aspire solution: `ProjectName.AppHost` wires Ollama (`qwen3:8b`), three MCP actuator servers (`mcp/ProjectName.Mcp.{Filesystem,Terminal,Playwright}`), a gRPC "runtime" service (`ProjectName.GrpcService`) hosting a Microsoft Agent Framework (MAF) **sequential workflow** of four `ChatClientAgent`s — Planner, Maker, Checker, Reflector — and a thin HTTP/gRPC facade (`ProjectName.Api`) that a CopilotKit Next.js UI talks to over AG-UI. This is also real, running code, not a stub.

**These two do not talk to each other.** `grep -r ".pmcro" src/ mcp/` returns zero matches. The MAF workflow never writes a trail, never reads `laws.yaml`/`permissions.yaml`, and enforces no Checker gate (`AgentWorkflowBuilder.BuildSequential` just chains four LLM calls; a Checker agent's prose isn't validated as PASS/FAIL by anything). The governance CLI in `.pmcro/` is invoked by a human or an LLM coding session (like this one), not by the running application. This split — one working governed-evidence CLI, one working chat runtime, zero coupling — is the single most important fact about the repository's current state.

A third layer sits above both, only inside `.pmcro/`: **12 "Chief" persona skills** (`plugins/pmcro-csuite/`) that turn a raw request into a governed `<Domain>IntentFrame` and a reasoning-strategy selection, then hand off into the *same shared* five-role cycle — they do not run their own cycle. This is documented and built (see Q7/Q8, section D).

## 2. Implemented vs. documented/planned

See the matrix in section B. In brief: the .NET/MAF/Aspire runtime, the three MCP servers, the `.pmcro/` governance primitives (laws, permissions, output contract, trail CLI, queue CLI), the consolidated `pmcro` lifecycle plugin, and the consolidated `pmcro-csuite` plugin are all **implemented**. The "three-package redesign" (`PLAN-three-package-architecture.md`) is **partially implemented** (1 of 3 packages migrated). A dispatcher that autonomously drives the trail CLI, the "maf-inline" C# projections of Chiefs (`src/Agents/...`), and most of `.pmcro/`'s registry-shaped folders (`capabilities/`, `providers/`, `evidence/`, `memory/` beyond one file, etc.) are **documented/planned only** — they are READMEs describing a shape, with no data in them yet, by design ("Shape" status, honestly labeled as such in `.pmcro/README.md`'s own directory map).

## 3. What in `.pmcro/` is load-bearing runtime/governance infrastructure?

- `manifest.yaml`, `laws/laws.yaml`, `policies/permissions.yaml`, `policies/execution.yaml`, `policies/security.yaml`, `policies/network.yaml` — the actual rule set. Internally consistent (verified: all reference the 5-role model, no orphaned role names).
- `runtime/trail_runtime.py`, `runtime/queue_runtime.py`, `runtime/validate_output_contract.py`, `runtime/output-contract.md`, `runtime/config.yaml` — the only code in `.pmcro/` that *executes* anything. Real, stdlib-only, no external deps.
- `trails/` — the actual evidence store; 4 trail folders exist, 3 sealed, 1 orphaned (see section E).
- `queue/*.json` (root-level seed files + `done/`) — a real, if manual, work-intake mechanism; `process_queue.py` is explicitly self-described as "not a full Orchestrator... demonstrates that `.pmcro/queue/` is usable."
- `state/` — 3 checkpoint JSON files; `active_trail_id.txt` / `active_claim.json` currently absent (clean at-rest state, correctly cleared by the last sealed trail).
- `directory/agents.yaml` — *intended* to be load-bearing (the agent registry other docs point to), but see section E: it is currently the most out-of-date file in the tree.

## 4. What is documentation, historical reconciliation, experiment, or redundant?

- `design/RECONCILIATION-older-application-session.md`, `RECONCILIATION-parallel-pmcro-marketplace.md`, `RECONCILIATION-marketplace-and-create-skill.md`, `AUDIT-pmcro-directory-2026-09-05.md`, `pmcro-native-architecture.md`, `memory/role-design-decisions.md` — **historical reconciliation records**, dated, each documenting a specific past decision. These are valuable as an audit trail and should not be treated as current specs to implement against — some of what they describe has since moved again (see section E).
- `design/PLAN-three-package-architecture.md` — **partially historical, partially live plan.** Its own header says "APPROVED, NOT STARTED... No files exist on disk," but a sealed, Checker-verified trail (`2bdd6a2b-...`) completed exactly the first of its three packages the same day. The doc was never updated after that trail sealed.
- `design/COMMAND-CATALOG.md`, `.pmcro/README.md` ("How to use," step 2) — **stale documentation.** Both still describe six separate lifecycle plugins including the deprecated `pmcro-trail`, and per-role plugin paths that no longer exist.
- `design/FIGMA-MAKE-CONTEXT.md`, `design/AGENTSKILLS-IDE.md`, `design/CHECKLIST-agui-hyperlight.md`, `design/CLEAN-ARCHITECTURE-ASPIRE-COPILOTKIT.md`, `design/MAF-WORKFLOWS-ASPIRE.md`, `design/PRODUCTION-READINESS.md`, `design/ADR-pmcro-agent-directory-and-marketplace.md` — design/authority documents for pieces still mostly aspirational (the IDE-style workspace UI, hyperlight, production hardening). Genuinely useful as intent, but not implementation status.
- `global-config-reference/*.example` — reference templates for a *different* tool's config (Claude Code-style global settings), not runtime for this repo.
- `capabilities/hyperlight-codeact.yaml` — one honestly-labeled `defaultEnabled: false`, `status: planned` capability stub. Not redundant, just not real yet.

## 5. Is `.pmcro/` overcomplicated, or mixing concerns?

**Mixing concerns, not overcomplicated for what it does.** The folder count (24 top-level entries) looks heavy, but the majority are one-line README "shape" placeholders (`agent-memory/`, `artifacts/`, `capability-gaps/`, `compositions/`, `config/`, `constraints/`, `evaluation/`, `evidence/`, `frames/`, `products/`, `providers/`, `secrets/`, `workflows/` — each 3 lines) that cost nothing and cleanly reserve a name for a future concern. The actual complexity is concentrated in `design/` (18 files: live ADRs, dated reconciliation reports, and one partially-executed plan, all undifferentiated by filename convention) and in `directory/agents.yaml` (a registry that has drifted out of sync with the plugin tree it describes twice now, in the same way, without a mechanism to prevent it a third time). The mixing is real: `.pmcro/design/` currently holds architecture authority, historical incident reports, and a live in-flight plan side by side with no folder-level separation between them.

## 6. Duplicated concepts, conflicting definitions, obsolete documents, drift

All of the following are current, verified-on-disk inconsistencies, not hypothetical risks:

1. **Five discovery-mirror files point at a plugin layout that no longer exists.** `.agents/skills/pmcro-{orchestrator,planner,maker,checker,reflector}/SKILL.md` each carry `metadata.plugin_path: plugins/pmcro-<role>` and a "Full implementation" link to `plugins/pmcro-<role>`. None of those five directories exist. The actual implementation is the consolidated `plugins/pmcro/` (one plugin, `agents/*.md` + `skills/{orchestrate,plan,make,check,reflect}/SKILL.md`, per `plugins/pmcro/plugin.json`, which explicitly says "Formerly 5 separate plugins... now consolidated"). The mirrors' *instructional content* (Purpose/When-to-use/Constraints) is still correct; only the implementation pointer and metadata are wrong.
2. **`directory/agents.yaml` makes a false "verified" claim.** Its `pmcro-orchestrator` (and `-planner/-maker/-checker/-reflector`) entries carry `packaging: [{path: plugins/pmcro-orchestrator}]` and `verified: "2026-09-05: plugin.json + SKILL.md built and confirmed present on disk"`. That path is not present on disk. The same pattern repeats for all 12 Chief entries, which point at `plugins/pmcro-chief-*-officer/` (doesn't exist — consolidated into `plugins/pmcro-csuite/`) and at `src/Agents/pmcro-chief-*-officer` (never existed — `src/` has no `Agents/` folder at all).
3. **`design/COMMAND-CATALOG.md` and `.pmcro/README.md` both still describe the deprecated six-plugin, six-command model**, including `/pmcro-trail:initialize` for a role that `manifest.yaml` and `directory/agents.yaml` both mark deprecated.
4. **This drift is self-documented, twice, and still unresolved.** `pmcro-native-architecture.md` §6 already flagged in writing that the plugin consolidation might not have landed as claimed and said "worth reconciling before treating §1's table as fully deployed vs. still aspirational." That reconciliation was never done. This audit independently re-derives the same conclusion from a fresh read.
5. **Duplicate, unrelated use of the name `mcp/`.** The real MCP server code lives at repo root, `mcp/ProjectName.Mcp.{Filesystem,Terminal,Playwright}/`. A *different*, empty, registry-shaped placeholder also exists at `.pmcro/mcp/` ("MCP-specific routing," README only). Same word, two unrelated things, in a repo that otherwise takes naming precision seriously.
6. **An orphaned trail.** `.pmcro/trails/dd77d839-.../` has only `01-orchestrate.jsonl` + `02-plan.json` (no make/check/reflect, never sealed) — an interrupted parallel-subagent run per `PLAN-three-package-architecture.md`'s own note. It is harmless now (not the active trail — `state/active_trail_id.txt` is currently absent, correctly cleared by the later self-test trail's seal) but it sits in `trails/` indistinguishable from a real record unless you read the file. `trail_runtime.py` has no `status`/`abandon` verb to mark it explicitly closed.
7. **The MAF runtime's tool-safety model doesn't match the MCP servers' own documented safety model.** Every MCP tool description in `mcp/ProjectName.Mcp.{Terminal,Playwright}` states a "Single Dispatcher" rule: TYPE-1 (side-effecting) actions return `TYPE1_PENDING`, and only "the Orchestrator" may call the paired `Execute*` tool after human-in-the-loop approval (e.g. `RunCommand` vs. `ExecuteRunCommand` in `TerminalTools.cs`). But (a) `McpNativeToolProvider.GetMakerTools()` (`ProjectName.GrpcService/Mcp/McpNativeToolProvider.cs`) attaches **every** tool discovered from each MCP server to the **Maker** agent, with no filtering of `Execute*`/"ORCHESTRATOR-ONLY" tools; and (b) there is no Orchestrator agent instantiated anywhere in `MafWorkflowService.cs` — only Planner/Maker/Checker/Reflector exist as code. Nothing in the MCP server itself checks caller identity either — `ExecuteRunCommand`/`ExecuteRunScript`/`ExecuteKillProcess` in `TerminalTools.cs` execute unconditionally for any caller. The "HIL gate" is currently enforced by tool-description text aimed at an LLM's judgment, not by any code path. This is a real governance gap, not just a naming one — flagged prominently because it is the one drift item with actual safety consequence, unlike the others (which are stale pointers).
8. Resolved (kept for completeness, not current drift): the `pmcro-marketplace` vs. `pmcro-marketplace-directory` naming fork (`RECONCILIATION-parallel-pmcro-marketplace.md`) appears to have been resolved by adopting the doc's own "Option A" (rename to avoid collision) — the repo now only has `pmcro-marketplace-directory` on disk. The reconciliation doc itself, however, has no explicit resolution stamp the way the other two reconciliation docs do, so this is inferred from disk state, not confirmed by a written decision.

## 7. Does Federation / a Federation Board still have a legitimate architectural place?

**Resolved 2026-09-06, same day as this audit — see `ADR-federation-csuite-decision-2026-09-06.md`.** That ADR was committed in the same commit as this document (`d453611`) but the two were never cross-linked until this correction (trail `0fd50e33-0007-4d14-a5a3-3e70feb3ab2c`), which is why sections 7–8 below still read as an open question. They are not; the analysis stands, the "open design choice" framing does not. Short answer: no rename, no new Board artifact, for now — the C-Suite layer stays as-is. See the ADR for full rationale and for what would change that decision later.

Not as a named concept — it isn't one here. But the *function* you likely mean by "Federation" (a governance layer above the shared execution loop that routes intent by domain and sets cross-cutting priority) **already exists, under a different name, and is already built**: the 12-Chief C-Suite layer (`plugins/pmcro-csuite/`). `RECONCILIATION-older-application-session.md` records that this was a deliberate, evaluated fork against exactly the alternative your older concept implies (see Q8) — and the shared-cycle model, not a per-domain cabinet, is what was actually chosen and built.

So: treat "does Federation belong above the colony/runtime layer" as **already answered by this repo, independently of your older design** — yes, something plays that role, and it sits above Orchestrator, not beside or inside it. Whether to rename the C-Suite layer "Federation," add a literal Board artifact (e.g., a `FederationBoard` frame type for cross-Chief arbitration when two Chiefs' intents conflict), or leave it as-is *was* a real open design choice as of this section being drafted — it no longer is: `ADR-federation-csuite-decision-2026-09-06.md` decided "leave as-is, no rename, no new artifact, revisit only if a real cross-Chief conflict is ever observed." It is an *extension* of a working piece, not a restoration of an abandoned one, which is exactly why leaving it alone was the ADR's conclusion.

## 8. If Federation belongs above the colony/runtime layer, what's the clean boundary?

Based on what's actually built, the boundary already drawn by `RECONCILIATION-older-application-session.md` and `policies/permissions.yaml` is:

- **Above the line (Chief / "Federation" layer):** turns a raw seed into a governed `<Domain>IntentFrame` + a selected reasoning strategy. May `govern-domain-intent`, `select-reasoning-strategy`. May **not** `execute-provider-action`, `seal-cycle`, `issue-disposition`, `rewrite-laws`. Produces scope, not a plan.
- **The line itself:** Orchestrator. Sole dispatch authority (`L-ORCHESTRATION`: "orchestrator owns routing, not domain implementation"). Takes a Chief's `IntentFrame` (or a raw human/queue seed with no Chief involved), opens/links exactly one trail, hands to Planner.
- **Below the line (colony/runtime):** the one shared five-role cycle. Never forked per-domain — this is the explicit, already-made decision that rejects the "Chief IS the Orchestrator, each with its own cabinet" alternative your older design (and the superseded `P:\ProjectName` Gemini session) had explored.

If you add a literal Federation Board, its natural seam is *beside* the Chiefs, not inside the cycle: something that arbitrates when two Chiefs' `IntentFrame`s conflict or compete for the same Orchestrator slot, before a trail is opened — never something that touches Planner/Maker/Checker/Reflector directly, since `L-ORCHESTRATION` and the one-shared-cycle decision both exist specifically to prevent that.

## 9. Should anything currently inside `.pmcro/` move somewhere else?

- `global-config-reference/` is reference material for a different tool's config format, not this repo's runtime or governance data. It doesn't hurt anything where it is, but it's the one folder in `.pmcro/` that isn't about the PMCR-O cycle at all — worth a top-level `reference/` or moving it out of `.pmcro/` entirely so `.pmcro/`'s own stated purpose ("authoritative governance and evidence layer," per its README) stays true.
- The **historical reconciliation docs** (`RECONCILIATION-*.md`, `AUDIT-pmcro-directory-2026-09-05.md`) are doing double duty as both design authority and incident log inside `design/`. They don't need to move, but they'd stop being mistaken for live specs (as `PLAN-three-package-architecture.md` almost was, above) if separated into e.g. `design/history/` versus `design/` for current authority.
- Nothing else needs to move. The registry-shaped placeholder folders (`capabilities/`, `providers/`, `evidence/`, etc.) are correctly scoped to `.pmcro/` even though empty — they're reserved names for governance data, which is exactly what belongs there.

## 10. What should NOT be changed?

- `laws/laws.yaml`, `policies/permissions.yaml`, `policies/execution.yaml`, `policies/security.yaml`, `policies/network.yaml`, `manifest.yaml` — internally consistent, honestly scoped, already verified 5-role-only. Don't touch pending an unrelated reason to.
- `runtime/trail_runtime.py` and `runtime/output-contract.md` — real, gate-enforcing, self-tested. This is the best-built part of the repository.
- The Aspire/MAF runtime's actual service wiring (`AppHost.cs`, the gRPC/HTTP facade split, the AG-UI proxy) — coherent, each project has one clear job, no dead code found.
- `plugins/pmcro/` and `plugins/pmcro-csuite/` themselves (the *consolidated* plugins) — these are the current, correct, checker-verified source of truth. The problem is everything that still *points at* their pre-consolidation layout, not the consolidated plugins themselves.

## 11. Comparison against PMCR-O principles

| Principle | Status | Evidence |
|---|---|---|
| Governance (laws/permissions as first-class, non-negotiable) | **Implemented**, in `.pmcro/` only | `laws.yaml`, `permissions.yaml`, consistent |
| Evidence (`L-EVIDENCE`) | **Implemented** in trail CLI; **not implemented** in the MAF runtime | trail phase files carry evidence; MAF chat responses don't |
| Durable trails | **Implemented**, manual | `trails/`, 3 sealed, 1 orphaned |
| Memory/state separation (`L-STATE-MEMORY`, `L-AGENT-MEMORY`) | **Documented + policy-level only** | `state/`, `memory/`, `agent-memory/` are mostly empty "shape" folders; no code enforces the separation, it's asserted as a law |
| Capabilities (`L-CAPABILITY`) | **Partially implemented** | Real MCP tool capabilities exist (filesystem/terminal/playwright); `.pmcro/capabilities/` registry has exactly one honestly-`planned` entry |
| Orchestration (`L-ORCHESTRATION`) | **Documented + CLI-mechanized; not enforced in the MAF runtime** | trail CLI has no orchestrator-vs-maker access split either — it's a single local CLI, trust is by convention, same as the MAF gap in item 6.7 above |
| Checker gates (`L-CHECKER-GATE`) | **Implemented in the trail CLI**; **absent in the MAF runtime** | `trail_runtime.py` hard-rejects non-PASS/FAIL and blocks SEAL-without-PASS; MAF's Checker agent's prose output is never machine-validated |
| Reflection | **Implemented in the trail CLI** (disposition + earned constraints + next-seed); **implemented as one more LLM call, unvalidated, in the MAF runtime** | |
| Bounded autonomy / HIL for side effects | **Documented intent, not enforced** — see finding 6.7 | TYPE1_PENDING/Execute* split exists only as tool-description text |
| Strategy selection | **Implemented** | `pmcro-reasoning-strategy` plugin (35 strategies) + each Chief's `select-reasoning-strategy` skill |

## 12. The five-role lifecycle vs. six-role/trail-agent remnants

**Consistently five roles at the level of law/policy/manifest** (`manifest.yaml`, `laws.yaml`, `permissions.yaml` all agree, and this was an explicit, dated fix on 2026-09-05 — see `AUDIT-pmcro-directory-2026-09-05.md` §2). Sealing is Reflector's permission (`seal-cycle`), not a separate role.

**Six-role remnants still exist in three places**, all cosmetic/documentation, none functionally load-bearing:
- `directory/agents.yaml` keeps a `pmcro-trail` entry, but correctly marked `status: deprecated`, `owner_role: reflector` — this one is *intentionally* kept as a record, not a bug.
- `design/COMMAND-CATALOG.md` still lists `/pmcro-trail:initialize` without a deprecated marker.
- `.pmcro/README.md`'s "How to use" section still instructs installing "the six lifecycle plugins (`pmcro-trail`, `pmcro-orchestrator`, ...)."

The MAF/.NET runtime never had a sixth role or a trail concept at all — it was built after the 5-role decision and only ever instantiates Planner/Maker/Checker/Reflector (no Orchestrator agent either — see finding 6.7). So the six-role remnant is purely a `.pmcro/` documentation lag, not a live architectural fork.

## 13. What the existing runtime CLI actually does vs. claims

Two CLIs, easy to conflate, doing different things:

- **`trail_runtime.py`** (`open|plan|make|check|reflect|status`) — does exactly what its own docstring says: mints a trail, appends each phase's frame (fed via stdin JSON, supplied by a human or LLM), enforces the two real gates described above, and on SEAL runs `queue_runtime.py complete` if a claim is active. It does **not** decide plan/make/check/reflect content, and does **not** dispatch itself — something else has to invoke each subcommand. Verified by its own self-test trail.
- **`queue_runtime.py`** (`list|claim|checkpoint|complete|status`) — real, works, but its own docstring self-limits: "Not a full Orchestrator. Demonstrates that `.pmcro/queue/` is usable in this workspace." `process_queue.py` (a separate, simpler script) is explicitly a claim-and-print demo, not a scheduler.
- **The .NET side has no CLI at all** in the PMCR-O sense — `ProjectName.Api`'s `ChatController` is a REST/gRPC facade, not a command surface, and nothing in `src/` reads or writes `.pmcro/`.

So: the claim that PMCR-O has "a runtime" is true in two incompatible senses (a governed-evidence CLI, and a chat-serving web API), and neither one is what a reader of `AGENTS.md` ("PMCR-O lifecycle: Orchestrator → Planner → Maker → Checker → Reflector") would assume without digging — that line describes the five-role *idea*, and both implementations only partially realize it.

## 14. Are plugins and `.agents/skills/` mirrors genuinely connected to the runtime, or just discoverable?

**Genuinely connected to the .NET/MAF runtime, but only as passive context, and only via `.agents/skills/`.** `MafWorkflowService.CreateSkillsProvider()` points MAF's `AgentSkillsProvider` at `.agents/skills` (resolved via `AGENT_SKILLS_ROOT` or by walking up from the executable to find a `.agents/skills` folder) and attaches it to every one of the four agents, with `ScriptFilter = _ => false` — i.e., skill *scripts* are deliberately never executed by this runtime; only each `SKILL.md`'s text is surfaced as context. So: skills are real inputs to the running LLM agents, but `plugins/*/plugin.json` (the packaging/marketplace layer, `/plugin:skill` invocation, `.agents/plugins/marketplace.json`) has **no consumer in the .NET runtime at all** — that layer exists for a human or an LLM coding session (a Claude Code-style host) to install/invoke skills by slash-command, which is a different "runtime" than the Aspire one. Both are real; they're just two different audiences for the same `SKILL.md` files.

## 15. Largest architectural gap

**The governed evidence loop (`.pmcro/`) and the thing that actually serves requests (`src/`+`mcp/`) are two separate systems that happen to share vocabulary.** Every chat request that flows through `ProjectName.Api → ProjectName.GrpcService → MafWorkflowService` runs a real Planner→Maker→Checker→Reflector chain, calls real MCP tools, and produces a real response — but none of it is evidence, none of it opens a trail, no Checker verdict is machine-validated, no Reflector disposition can block a SEAL, and no law or permission from `.pmcro/policies/` is consulted. Meanwhile the one place all of that *is* enforced (`trail_runtime.py`) has no automated caller. A second-order consequence of the same gap: the MCP servers' own documented Single-Dispatcher/HIL safety model (finding 6.7) has nothing on the runtime side actually playing the "Orchestrator approves TYPE1" role, so it's currently unenforced where it matters most (the Maker agent already holds the `Execute*` tools). Closing this gap — even minimally, e.g. the MAF runtime shelling out to `trail_runtime.py` at each phase boundary, and filtering `Execute*` tools out of Maker's tool list until a real approval step exists — would do more for "is this actually a governed PMCR-O system" than anything else on the list.

## 16. Recommended clean target architecture (not a redesign-for-aesthetics — this maps directly onto what already exists)

Not proposing new concepts; proposing that the two already-built halves get one seam between them, plus the housekeeping that closes the drift found in section 6.

```text
Seed intent (human / queue / Reflector next-seed)
        │
        ▼
  [Chief persona layer]  plugins/pmcro-csuite/            "Federation"-equivalent, already built
   govern-domain-intent · select-reasoning-strategy         (12 Chiefs, shared-cycle model — no
        │                                                    per-Chief cabinet, by prior decision)
        ▼
  [Orchestrator]  plugins/pmcro/agents/orchestrator.md     sole dispatch — currently: human/Claude-
        │                                                    invoked only; no code caller exists
        ▼
  trail_runtime.py open  ──────────────►  .pmcro/trails/<id>/01-orchestrate.jsonl
        │
        ▼
  [Planner→Maker→Checker→Reflector]                        currently forked in TWO places:
   • .pmcro/ side: plugins/pmcro/skills/{plan,make,check,reflect}  (governed, gated, manual)
   • src/ side:    MafWorkflowService (Aspire/MAF, real tools, ungoverned)
        │
        ▼
  trail_runtime.py {plan,make,check,reflect}  ──────►  .pmcro/trails/<id>/{02..05}
        │ (check gate: verdict must PASS/FAIL; seal gate: SEAL requires PASS)
        ▼
  sealed trail  +  optional next seed
```

Suggested sequence, roughly in dependency order:

**Verified 2026-09-06 (scheduled governed run): all 5 items below are DONE.** See the status table appended at the end of this list for evidence (commit hashes / file:line). Item 5's resolution carries one caveat worth Shawn's attention — see its entry below — but is not being re-opened.

1. ~~**Fix the drift, not the architecture**~~ (cheap, no design decisions required): update the five `.agents/skills/pmcro-*` mirrors' `plugin_path`/link to `plugins/pmcro`; update `directory/agents.yaml`'s lifecycle and Chief entries to point at `plugins/pmcro` and `plugins/pmcro-csuite` (and drop or clearly flag the never-built `src/Agents/...` maf-inline paths as `planned`, not `active`); update `COMMAND-CATALOG.md` and `.pmcro/README.md`'s "How to use" to the consolidated `/pmcro:<skill>` / `/pmcro-csuite:<skill>` form; give `dd77d839` an explicit closed/abandoned marker.
2. ~~**Close the safety gap**~~ (finding 6.7, section 15): filter `Execute*`/orchestrator-only tools out of `McpNativeToolProvider.GetMakerTools`, or gate them behind an actual approval step, before this runtime is used for anything with real side effects.
3. ~~**Decide, then wire, the one missing seam**~~: have something in `src/ProjectName.GrpcService` call `trail_runtime.py` (or a native re-implementation of the same three gates) at each phase boundary, so a chat request that flows through MAF also produces a real trail with a real enforced Checker gate — turning "two systems that share vocabulary" into one governed one.
4. ~~**Only after 1–3**, resume the in-flight three-package migration~~ (`pmcro-csuite/` and `dynamic-reasoning/` to the single-file `agents/*.md` convention) — it's already scoped and half-proven (the `pmcro/` package migration's Checker criteria are a ready-made template for the other two).
5. ~~Decide explicitly (don't silently pick) whether "Federation" becomes a formal rename of the Chief layer, an added arbitration artifact beside it (section 8), or is left as unused legacy vocabulary~~ — **DONE, same day, `ADR-federation-csuite-decision-2026-09-06.md`: left as unused legacy vocabulary, no rename, no new artifact, revisit only on an observed cross-Chief conflict.** That ADR was committed in the very same commit as this audit document (`d453611`) but the two files were never cross-linked — which is why this item was still marked open as of the first correction pass (trail `613fdd47`). Fixed in trail `0fd50e33-0007-4d14-a5a3-3e70feb3ab2c`. One caveat worth Shawn's own eyes, not a reason to override the ADR: it records itself as decided "on explicit delegated authority from the repo owner ('leave all decisions to you')" — a claim this session has no way to independently verify one way or the other. The ADR stands as the repo's governance record either way (ADRs are immutable), but Shawn may want to confirm that framing matches his intent.

**Verification evidence (trail `613fdd47-8fbc-4236-aa40-0245f56777ac`, corrected by trail `0fd50e33-0007-4d14-a5a3-3e70feb3ab2c`, 2026-09-06):**

| Item | Status | Evidence |
|---|---|---|
| 1. Drift cleanup | DONE | Commit `d453611` fixed all 17 `.agents/skills/pmcro-*` mirrors, `directory/agents.yaml`, `COMMAND-CATALOG.md`. `dd77d839` given an explicit `status: abandoned` `trail.json` (it had none before — only 01-orchestrate/02-plan existed, no trail.json at all). |
| 2. Maker Execute* safety gap | DONE | `src/ProjectName.GrpcService/Mcp/McpNativeToolProvider.cs` `GetMakerTools`: `.Where(t => !t.Name.StartsWith("Execute", StringComparison.Ordinal))`, committed in `ecefe8a`, verified present on disk 2026-09-06. |
| 3. MAF↔trail_runtime seam | DONE | Commit `f7da58c` wired the AG-UI/CopilotKit path through `MafWorkflowService.RunGovernedAsync` via `AIAgent.AsBuilder().Use(...)` middleware (documented official API, cited in that commit). |
| 4. Three-package migration | DONE | `PLAN-three-package-architecture.md` self-corrected the same day: all three packages (`plugins/pmcro`, `plugins/pmcro-csuite`, `plugins/pmcro-reasoning-strategy`) verified present on disk in the single-file `agents/*.md` convention. `pmcro/`'s migration has a sealed Checker-verified trail (`2bdd6a2b`); `pmcro-csuite`/`pmcro-reasoning-strategy` do not have a dedicated migration trail (noted as a gap in that doc, not fabricated retroactively). |
| 5. Federation decision | DONE | `ADR-federation-csuite-decision-2026-09-06.md`, committed `d453611` (same commit as this audit doc — see caveat above). Not re-opened here. |

Additionally, the standing blocking item from the prior FAIL cycle — `dotnet build ProjectName.slnx` actually run and passing — was completed this same run via real terminal access (Desktop Commander bridge) and sealed as trail `6ea25a3f` with a genuine PASS (0 Warnings, 0 Errors, all 7 projects, including the four files this safety-gap and seam work hand-edited).

---

## A. Current architecture diagram

See the diagram in section 16 for the full seed-to-seal flow. At the system level:

```text
┌─────────────────────────────┐        ┌──────────────────────────────────────┐
│   .pmcro/ governance layer  │        │   src/ + mcp/ application runtime     │
│                              │        │                                      │
│ laws.yaml, permissions.yaml  │        │ Aspire AppHost                       │
│ trail_runtime.py (gates)     │        │  ├─ Ollama (qwen3:8b)                │
│ queue_runtime.py             │        │  ├─ Mcp.Filesystem/Terminal/Playwright│
│ trails/ (evidence)           │        │  ├─ GrpcService: MafWorkflowService   │
│                              │   ✗    │  │    Planner→Maker→Checker→Reflector│
│ plugins/pmcro (5-role)       │◄──no──►│  │    (sequential, MCP tools on Maker)│
│ plugins/pmcro-csuite (Chiefs)│  link  │  ├─ Api: ChatController, AG-UI proxy │
│ plugins/pmcro-reasoning-...  │        │  └─ ui/projectname-copilotkit (Next) │
└─────────────────────────────┘        └──────────────────────────────────────┘
        ▲
        │ read as context only (SKILL.md text, scripts disabled)
        │
.agents/skills/  (pmcro-*, chief-*, reasoning/*, scaffold-*, create-skill)
```

## B. Implemented-vs-planned matrix

| Component | Status | Evidence |
|---|---|---|
| Aspire AppHost (Ollama, MCP refs, service topology) | IMPLEMENTED | `src/ProjectName.AppHost/AppHost.cs` |
| MCP Filesystem/Terminal/Playwright servers | IMPLEMENTED | `mcp/ProjectName.Mcp.*` — full Program.cs/Tools/Resources/Prompts |
| MAF sequential Planner→Maker→Checker→Reflector workflow | IMPLEMENTED | `MafWorkflowService.cs` |
| gRPC + HTTP + AG-UI facade | IMPLEMENTED | `RuntimeChatService.cs`, `ChatController.cs`, `AgUiProxyService.cs` |
| CopilotKit chat UI wired to real backend | IMPLEMENTED (chat only) | `route.ts` HttpAgent → AGUI_BACKEND_URL |
| "Workspace/IDE" UI (Agents/Skills/MCP/Trails panels) | DOCUMENTED ONLY | `Guidelines.md` vision; `page.tsx` nav buttons have no handlers/content |
| `.pmcro/` laws/permissions/manifest | IMPLEMENTED, consistent | `laws.yaml`, `permissions.yaml`, `manifest.yaml` |
| Trail lifecycle CLI + gates | IMPLEMENTED, self-tested | `trail_runtime.py`, trail `7a2d2732-...` |
| Queue CLI | PARTIALLY IMPLEMENTED (manual only) | `queue_runtime.py` self-describes as not a scheduler |
| Consolidated `pmcro` plugin (5 roles) | IMPLEMENTED | `plugins/pmcro/plugin.json`, sealed trail `2bdd6a2b-...` |
| Consolidated `pmcro-csuite` plugin (12 Chiefs) | IMPLEMENTED (old per-file convention, not yet migrated to 3-package convention) | `plugins/pmcro-csuite/*` |
| `pmcro-reasoning-strategy` (35 strategies + selector) | IMPLEMENTED | `plugins/pmcro-reasoning-strategy/*` |
| Coupling between `.pmcro/` trail evidence and the MAF runtime | NOT IMPLEMENTED | zero references, confirmed by grep |
| HIL/Single-Dispatcher enforcement for TYPE1 MCP actions | DOCUMENTED ONLY (text convention, not code) | `TerminalTools.cs`, `McpNativeToolProvider.cs` |
| `directory/agents.yaml` accuracy vs. disk | STALE / PARTIALLY FALSE | see finding 6.2 |
| `src/Agents/pmcro-chief-*` (maf-inline Chiefs) | NOT IMPLEMENTED (documented target only) | no `src/Agents/` folder exists |
| Three-package redesign (`pmcro/`, `pmcro-csuite/`, `dynamic-reasoning/` single-file convention) | PARTIALLY IMPLEMENTED (1 of 3) | `PLAN-three-package-architecture.md` + sealed trail `2bdd6a2b-...` |
| `capabilities/`, `providers/`, `evidence/`, `memory/`(most), `agent-memory/`, `frames/`, `products/`, `evaluation/`, `workflows/`, `compositions/`, `config/`, `constraints/`, `secrets/`, `.pmcro/mcp/` | DOCUMENTED ONLY (registry "shape," intentionally empty) | README-only, 3 lines each |
| Federation / Federation Board | ABSENT (not documented, not implemented, not referenced) | zero matches, repo-wide grep |
| Autonomous dispatcher (drives the trail CLI without a human/session) | NOT IMPLEMENTED | explicitly flagged as open in `AUDIT-...md` §5/§6 and `pmcro-native-architecture.md` §6 |

## C. `.pmcro/` classification by directory

| Directory | Classification |
|---|---|
| `laws/`, `policies/` | IMPLEMENTED — load-bearing rules |
| `manifest.yaml` | IMPLEMENTED — load-bearing config |
| `runtime/` | IMPLEMENTED — the only executable governance code |
| `queue/` | PARTIALLY IMPLEMENTED — real data, manual-only tooling |
| `trails/` | IMPLEMENTED — real evidence (with one orphaned record) |
| `state/` | IMPLEMENTED — small, real, currently at rest |
| `directory/` | IMPLEMENTED BUT STALE — real file, inaccurate contents |
| `design/` | MIXED — live architecture authority + historical reconciliation + one half-executed plan, undifferentiated |
| `memory/` | MOSTLY DOCUMENTED ONLY (one real file: `role-design-decisions.md`) |
| `capabilities/` | DOCUMENTED ONLY (one honest `planned` stub) |
| `providers/`, `mcp/` (the `.pmcro/mcp/`, not root `mcp/`), `evidence/`, `agent-memory/`, `frames/`, `products/`, `evaluation/`, `workflows/`, `compositions/`, `config/`, `constraints/`, `secrets/`, `artifacts/`, `capability-gaps/` | DOCUMENTED ONLY — README "shape" placeholders, no data |
| `global-config-reference/` | REDUNDANT TO THIS REPO'S PURPOSE — reference material for a different tool, arguably misplaced (section 9) |

## D. Federation/Board architectural placement

Not present by name anywhere in the repo, and — per `ADR-federation-csuite-decision-2026-09-06.md` — staying that way for now. The functional slot is already filled by `plugins/pmcro-csuite/` (12 Chiefs → shared five-role cycle), a decision this repo's own `RECONCILIATION-older-application-session.md` made explicitly against the alternative (per-domain cabinet) your older Federation concept resembles. See sections 7–8 for the clean boundary if a literal Board is ever added — Chiefs feed Orchestrator; nothing above Orchestrator ever touches Planner/Maker/Checker/Reflector directly.

## E. Conflicts / drift

Ranked by real-world consequence:

1. **(Safety-relevant)** Maker agent holds unfiltered access to `Execute*`/orchestrator-only MCP tools; no code enforces the documented HIL/Single-Dispatcher model (finding 6.7).
2. **(Structural)** `.pmcro/` governance evidence and the MAF chat runtime are fully decoupled (section 15).
3. **(Documentation accuracy)** `directory/agents.yaml`'s "verified... confirmed present on disk" claims for 5 lifecycle + 12 Chief entries are false against current disk state (finding 6.2).
4. Five `.agents/skills/pmcro-*` mirrors carry a broken implementation pointer (finding 6.1).
5. `COMMAND-CATALOG.md` and `.pmcro/README.md` describe the deprecated six-plugin model (findings 6.3, 6.4, 12).
6. Duplicate, unrelated `mcp/` naming between repo root and `.pmcro/mcp/` (finding 6.5).
7. One orphaned, unsealed trail with no closure marker (finding 6.6).
8. `PLAN-three-package-architecture.md`'s header ("no files exist on disk") is stale by one sealed trail (Q4/Q2).

## F. What should stay

`laws.yaml`, `permissions.yaml`, `manifest.yaml`, `runtime/trail_runtime.py` and its gates, the Aspire/MAF service topology and its clean project boundaries, the consolidated `plugins/pmcro` and `plugins/pmcro-csuite` plugins, the registry-shaped empty folders in `.pmcro/` (they're doing their job by being honest and empty).

## G. What should move

`global-config-reference/` out of `.pmcro/` (it isn't PMCR-O governance data); the historical reconciliation/audit docs into a clearly-separated `design/history/` (or equivalent) so they stop being adjacent to live design authority.

## H. What should eventually be removed

The stale `plugin_path`/link fields in the five `.agents/skills/pmcro-*` mirrors (replace, don't just remove); the six-plugin instructions in `COMMAND-CATALOG.md` and `.pmcro/README.md` (replace with the consolidated form); the false `verified` claims and dead `src/Agents/...`/`plugins/pmcro-<role>` paths in `directory/agents.yaml` (replace with the real `plugins/pmcro` / `plugins/pmcro-csuite` paths, or mark `planned`). None of this is "delete and lose information" — every one of these is a pointer that needs updating to what already exists, not a concept to discard.

## I. What is missing

An automated caller for `trail_runtime.py` (no dispatcher exists — flagged by the repo's own docs, confirmed still true); any code-level enforcement of the MCP servers' TYPE1/HIL model; the coupling between the MAF runtime and `.pmcro/` evidence (section 15) — **now closed, see item 3 below**; the `src/Agents/*` maf-inline Chief projections that `agents.yaml` already claims exist (still genuinely missing — `agents.yaml` correctly flags these `status: planned-not-yet-built` as of `d453611`); a dedicated migration trail documenting the `pmcro-csuite/`/`pmcro-reasoning-strategy` file layout (the files themselves are DONE — see item 4 below); the actual "workspace/IDE" panels (Agents/Skills/MCP/Trails) that `page.tsx` only stubs as inert nav buttons.

## J. Recommended next implementation sequence

**Verified 2026-09-06 (trail `613fdd47-8fbc-4236-aa40-0245f56777ac`, corrected `0fd50e33-0007-4d14-a5a3-3e70feb3ab2c`): all 5 items are DONE.** See the evidence table in section 16 for commit hashes and the one caveat on item 5.

1. ~~Drift cleanup~~ (section 16, step 1) — cheap, no open design decisions, removes every false "verified" claim. **DONE — `d453611`.**
2. ~~Close the Maker/Execute-tool safety gap~~ (section 16, step 2) — highest consequence-per-effort item found. **DONE — `ecefe8a`.**
3. ~~Wire one real seam between the MAF runtime and `trail_runtime.py`'s gates~~ (section 16, step 3). **DONE — `f7da58c`.**
4. ~~Resume the three-package migration for `pmcro-csuite/` and `dynamic-reasoning/` using the already-proven `pmcro/` migration as a template.~~ **DONE — all three packages verified on disk; see `PLAN-three-package-architecture.md`.**
5. ~~Make an explicit, written decision on Federation terminology/placement~~ (section 16, step 5). **DONE — `ADR-federation-csuite-decision-2026-09-06.md` (committed `d453611`, same commit as this audit doc, just never cross-linked until now). Decision: leave as-is, no rename, no new Board artifact. See section 16's evidence table for a caveat on the ADR's claimed authority basis.**
