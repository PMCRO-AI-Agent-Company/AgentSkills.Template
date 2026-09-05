# PlanFrame — Align AppHost / OrchestrationApi / AG-UI / Hyperlight

**Seed intent:**  
Align AppHost and OrchestrationApi to ADR-pmcro-enterprise-hybrid-stack; expose one AG-UI endpoint for CopilotKit; keep Hyperlight CodeAct behind an explicit capability flag; do not overwrite parallel marketplace work.

**Planner role only** — this document is the plan. Execution belongs on the real `pmcr-o` checkout (Maker). This seed workspace records the plan + capability contract only.

---

## Goal

Bring the existing Aspire AppHost + OrchestrationApi in line with the hybrid stack ADR so that:

1. Topology and comments match enterprise hybrid targets (MAF Harness path, CopilotKit edge, gated CodeAct).
2. **One** AG-UI-compatible endpoint is exposed for CopilotKit.
3. **Hyperlight CodeAct** is disabled by default via an explicit capability flag (no invented provider).
4. Parallel-session `plugins/pmcro-marketplace/` work is **not** modified.

---

## Current evidence (repo)

| Surface | Today |
|---------|--------|
| `ProjectName.AppHost/AppHost.cs` | Ollama + Runtime + OrchestrationApi; parameterized `repoRoot` |
| `ProjectName.OrchestrationApi/Program.cs` | HTTP + gRPC; `/api/chat` → Runtime gRPC; OpenAPI/Scalar in Dev |
| `ProjectName.Runtime` | Agent/model boundary, gRPC |
| Plugins | Lifecycle six + CEO/CTO + aspire; **no** overwrite of parallel marketplace |
| Hyperlight | Not wired; must stay capability-gated |

---

## Ordered steps

| # | subject_agent | action | success check |
|---|----------------|--------|----------------|
| 0 | human/maker | Work only on real repo checkout; do not edit parallel uncommitted marketplace trees | git status shows no touch of foreign marketplace paths |
| 1 | maker | Add capability contract `hyperlight-codeact` under `.pmcro/capabilities/` with `enabled: false` by default | File exists; Directory/policy can reference id; no provider invented |
| 2 | maker | Document AppHost alignment notes in AppHost (comment block or `aspire.config` note): MAF Harness, AG-UI edge, CodeAct flag | Comment or config key present; still no host-specific paths |
| 3 | maker | OrchestrationApi: add **one** AG-UI (or AG-UI-ready) map endpoint stub that forwards to Runtime/MAF agent surface; keep existing `/api/chat` | `Map*` endpoint exists; Dev OpenAPI lists it; does not remove gRPC chat path |
| 4 | maker | Config: `Hyperlight:CodeAct:Enabled` (or env `PMCRO_CAPABILITY_HYPERLIGHT_CODEACT=false`) read at startup; log clearly when disabled | Default false; enabling requires explicit config |
| 5 | maker | Wire optional package reference to Hyperlight **only** behind `#if` / feature flag / conditional registration — never register execute_code tool when flag false | No execute_code tool when flag false |
| 6 | checker | Verify: refuse absolute paths in new files; marketplace parallel paths untouched; flag default false; AG-UI route responds in Dev | Checklist PASS |
| 7 | reflector | Disposition: seal only after Checker PASS; next seed optional (CopilotKit Next app against AG-UI URL) | Trail sealed on real repo only |

---

## Success criteria (cycle)

- [ ] Capability id `hyperlight-codeact` documented; default **off**
- [ ] OrchestrationApi exposes **one** AG-UI-oriented endpoint for CopilotKit
- [ ] Existing `/api/chat` + gRPC Runtime path still works
- [ ] AppHost still uses parameterized `repoRoot` (no `P:\`)
- [ ] Zero edits to parallel-session marketplace plugin tree
- [ ] No fake MCP/provider entries

## Out of scope

- Full CopilotKit Next.js app (follow-up seed)
- Promoting Hyperlight packages to production dependency without flag
- Merging parallel marketplace scaffolder
- Sealing trails from this cloud seed (no lifecycle host here)

---

## Handoff

**Maker (on real machine):** execute steps 1–5 against `ProjectName.*` projects.  
**Checker:** step 6.  
**Reflector:** step 7.  

Capability stub and operator checklist for this seed follow in `.pmcro/capabilities/` and `CHECKLIST-agui-hyperlight.md`.
