# Production Readiness Assessment — PMCRO Colony Workspace

**Date:** 2026-09-05  
**Scope:** This cloud workspace (`artifacts/`) as a portable colony seed for autonomous operations  
**Validated against:** Agent Skills open standard (agentskills.io), Microsoft Agent Framework Agent Skills for .NET (stable July 2026), Microsoft Foundry skills progressive disclosure

---

## Executive verdict

| Dimension | Grade | Notes |
|-----------|-------|-------|
| Governance model (laws, checker-gate, trail-as-product) | **Strong** | Matches enterprise need for auditability and sealed evidence |
| Agent Directory as SoT | **Strong** | Single catalog; marketplace manifests should stay derived |
| Portable Agent Skills packaging | **Aligned** | SKILL.md + progressive disclosure matches agentskills.io + MAF 2026 |
| MAF-inline C# stubs | **Honest MVP** | Stable MAF Skills API exists (2026); stubs still mark unconfirmed host wiring as TODO |
| Lifecycle plugins in this workspace | **Absent (by design)** | Core six live in the real repo; this tree is governance + marketplace + reasoning |
| Capability/provider registries | **Honest empty** | Correct: empty > invented integrations |
| Autonomous loop readiness | **Partial** | Orchestrator→…→Reflector requires the six plugins + runtime host |
| Eval / refuse gates on scaffolder | **Good** | 9 cases; refuse on paths, placeholders, schema |
| Workspace hygiene | **Good (post-cleanup)** | Eval clutter removed; reasoning under `.agents/skills/reasoning/` |

**Bottom line:** This workspace is a **production-grade governance and packaging seed**, not a full running multi-agent host. For autonomous operations you still need the lifecycle plugins + a host (MAF / Claude Code / colony runtime) that actually executes the loop.

---

## What is state-of-the-art (validated 2026)

1. **Agent Skills open standard** — folder + `SKILL.md` (name + description required); progressive disclosure (advertise → load body → resources → scripts). Portable across Claude Code, Cursor, Codex, Foundry, MAF.
2. **Microsoft Agent Framework Agent Skills for .NET** — **stable** (experimental attribute removed July 2026). File-based, inline, and class skills; composable providers; toolbox / MCP delivery in Foundry.
3. **Progressive disclosure** — only names/descriptions at startup; full body on demand — required for enterprise token budgets.
4. **Sealed evidence + independent checker** — PMCRO’s L-EVIDENCE / L-CHECKER-GATE is stronger than most demo multi-agent stacks and is the right pattern for regulated / autonomous ops.
5. **No invented integrations** — empty provider registries until wired is the correct enterprise posture.

---

## What was cleaned in this pass

| Removed / tightened | Why |
|---------------------|-----|
| `.agents/skills/eval-*` generated packages | Eval artifacts, not product |
| `src/Agents/eval-*` generated C# | Same |
| Top-level `reasoning-skills/` | Already moved under `.agents/skills/reasoning/` |
| Plugin name collision | Renamed to `pmcro-marketplace-directory` (Option A) |

Kept: eval **fixtures** under the plugin (quality gates), all laws/policies/contracts, directory, design ADRs, reasoning catalog, sample domain skill.

---

## Architecture for autonomous operations (target)

```text
Human / Seed Intent
        ↓
  Orchestrator          ← sole dispatch (plugin, real repo)
        ↓
  Planner  (+ optional reasoning skill id)
        ↓
  Maker
        ↓
  Checker               ← independent gate
        ↓
  Reflector             ← sole sealer; next seed
        ↓
  Trail (Class B) + Agent Directory updates
```

**This workspace supplies:** Directory, laws, policies, output contract, scaffolder, reasoning catalog, design authority.  
**Real repo / host must supply:** Six lifecycle plugins, execution runtime, real capability providers.

---

## Gaps before “full autonomous enterprise”

1. **Lifecycle plugins not vendored here** — link or submodule from `PMCRO-AI-Agent-Company/pmcr-o` rather than duplicating.
2. **MAF host project** — add a real .NET project that loads skills via stable Agent Skills API (not only stubs).
3. **Capability providers** — wire real MCP / tools only when attested; keep registries empty until then.
4. **CI eval** — run `scaffold-skill/eval/eval.yaml` in pipeline on every change to the scaffolder.
5. **Trail automation** — scripts that append frames must stay deterministic and role-owned.
6. **Secrets** — references only; integrate a real secret store outside `.pmcro/secrets/`.

---

## Recommendations (ordered)

1. Treat this tree as the **governance + marketplace + reasoning** plane; keep lifecycle plugins in the canonical repo.
2. Register reasoning skills only as **`reasoning-catalog`** (done) — not 35 directory rows.
3. When implementing MAF, prefer official `AgentInlineSkill` / file skill providers from current MAF docs over hand-rolled type names.
4. Promote scaffolder eval into CI; fail the build on refuse-case regressions.
5. Do not fill `providers/` or `mcp/` with placeholder services — escalate missing capability instead.

---

## PMCRO loop status on this workspace

| Phase | Status here |
|-------|-------------|
| Trail initialize | Shape + README only (no live GUID trails in this seed) |
| Orchestrate | Spec + directory entry for parallel/real plugins |
| Plan / Make / Check / Reflect | Requires lifecycle plugins from canonical repo |
| Directory + scaffold | **Active** |
| Reasoning strategies | **Active** (catalog) |
| Output contract validator | **Active** (`runtime/validate_output_contract.py`) |

To “activate PMCRO” end-to-end, run cycles against a checkout that includes `plugins/pmcro-{trail,orchestrator,planner,maker,checker,reflector}` and point `.pmcro/` at that repo root.
