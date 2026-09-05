# ADR: Production Enterprise Hybrid Stack — PMCRO AI Agent Company

**Status:** Target architecture (aligns existing repo + this governance seed)  
**Date:** 2026-09-05  
**Validated against:** MAF 1.x GA (Harness GA Aug 2026), Aspire 13.4+, Agent Skills stable (.NET Jul 2026), CopilotKit AG-UI + MAF, CodeAct + Hyperlight preview packages, agentskills.io  

---

## 1. Intent

Deliver a **production-ready, enterprise-grade** PMCRO AI Agent Company with:

| Layer | Technology | Maturity (2026) |
|-------|------------|-----------------|
| Orchestration host | **.NET Aspire** AppHost | GA (13.3/13.4; publish/deploy GA; `aspire agent` workflows) |
| Agent runtime | **Microsoft Agent Framework** (.NET + Python) | GA 1.0 (Apr 2026); Harness + Hosted Agents GA |
| Inter-agent / API | **gRPC** (backend) + **REST/OpenAPI** (edge) | Production standard |
| Frontend | **CopilotKit** + **AG-UI** | Documented MAF integration (React/Next) |
| Skills | **Agent Skills** (`SKILL.md`) + marketplace templates | Open standard + MAF Skills stable |
| Code execution | **CodeAct** via **Hyperlight** sandbox | MAF CodeAct docs GA-shaped; Hyperlight provider **preview** |
| Governance | **PMCRO** (Plan→Make→Check→Reflect→Orchestrate) + `.pmcro/` | Your model; stronger audit than typical demos |
| C-Suite | Persona skills (CEO, CTO, CLO, …) | Intent governance only; execution via lifecycle |

Your canonical repo (`PMCRO-AI-Agent-Company/pmcr-o`) already has Aspire projects, OrchestrationApi, Runtime, plugins, and `.pmcro/` — this ADR is the **target composition**, not a greenfield rewrite.

---

## 2. Reference architecture

```text
                    ┌─────────────────────────────────────┐
                    │  CopilotKit (React/Next)  REST/AG-UI │
                    │  HITL · generative UI · shared state │
                    └─────────────────┬───────────────────┘
                                      │ HTTPS / AG-UI
                    ┌─────────────────▼───────────────────┐
                    │  Edge API (ASP.NET)  REST + health   │
                    │  auth · rate limit · OpenAPI         │
                    └─────────────────┬───────────────────┘
                                      │ gRPC (internal)
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
┌─────────▼─────────┐     ┌───────────▼──────────┐     ┌──────────▼──────────┐
│ MAF Harness Agent │     │ PMCRO Orchestration  │     │ Python MAF workers  │
│ (batteries-incl.) │     │ gRPC  (Orchestrator  │     │ (skills, research,  │
│ long multi-step   │     │  lifecycle router)   │     │  CodeAct helpers)   │
└─────────┬─────────┘     └───────────┬──────────┘     └──────────┬──────────┘
          │                           │                           │
          │         ┌─────────────────▼─────────────────┐         │
          │         │  Lifecycle agents (ChatClientAgent │         │
          └────────►│  or workflow nodes): Planner Make  │◄────────┘
                    │  Checker Reflector + C-Suite personas│
                    └─────────────────┬─────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
     ┌────────▼────────┐    ┌─────────▼────────┐    ┌─────────▼────────┐
     │ Agent Skills    │    │ .pmcro/ trails   │    │ Hyperlight       │
     │ marketplace     │    │ Directory laws   │    │ CodeAct sandbox  │
     │ File/Inline/Class│    │ output contract │    │ (preview → gate) │
     └─────────────────┘    └──────────────────┘    └──────────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │ Aspire AppHost           │
                         │ local + deploy topology  │
                         │ OTel → Aspire dashboard  │
                         └─────────────────────────┘
```

---

## 3. Component contracts (honest maturity)

### 3.1 Aspire (host)
- **Use for:** process model, service discovery, dashboards, `aspire publish` / `deploy`, agent-oriented workflows (`aspire agent`, aspire-skills bundle).
- **Maps to repo:** `ProjectName.AppHost`, `ProjectName.ServiceDefaults`, env wiring.
- **Do:** keep all service URLs discovery-based; no hard-coded host paths in trails.

### 3.2 Microsoft Agent Framework
- **Use for:** agents, workflows (sequential / concurrent / handoff), middleware, OpenTelemetry, **Harness Agent** for long multi-step work, skills providers.
- **Hybrid:** .NET for OrchestrationApi + primary lifecycle agents; Python where research/CodeAct guest tooling fits.
- **Skills:** file-based `SKILL.md` (portable) + InlineSkill / ClassSkill in-process — matches this seed’s scaffolder targets (`agentskills`, `maf-inline`).

### 3.3 gRPC backend + REST frontend
- **gRPC:** internal agent-to-agent and OrchestrationApi (typed, versioned protos under Runtime).
- **REST:** external clients, health, OpenAPI, CopilotKit runtime bridge.
- **Rule:** REST does not bypass PMCRO gates; mutating calls become Seed Intents → Orchestrator.

### 3.4 CopilotKit
- **Use for:** operator UX — chat, generative UI, shared state, human-in-the-loop approvals (TYPE1 mutations).
- **Integration path:** MAF agent exposes **AG-UI**; CopilotKit Runtime (Node) fronts it; Next/React UI.
- **PMCRO fit:** approval UI = policy `requireApprovalForMutation`; Checker still independent.

### 3.5 Harness
- **MAF Harness Agent (GA):** plan/todo, context compaction, file memory, tool approval, OTel — use for long C-Suite or Maker sessions.
- **Not** a replacement for PMCRO Reflector seal; harness helps *run*; Reflector *disposes and seals*.

### 3.6 CodeAct + Hyperlight
- **CodeAct (MAF):** single `execute_code` tool; model writes code instead of many tool round-trips ([Learn](https://learn.microsoft.com/en-us/agent-framework/agents/code-act)).
- **Hyperlight:** microVM/Wasm isolation for untrusted code; `Microsoft.Agents.AI.Hyperlight` is **preview** (e.g. 1.17.0-preview.*).
- **Production rule:**  
  - Dev/staging: Hyperlight CodeAct behind explicit capability + approval.  
  - Prod: only after package stable + policy allowlist; until then escalate missing capability (never invent).

### 3.7 PMCRO + C-Suite + Marketplace
- **Lifecycle six:** sole execution path for governed cycles.  
- **C-Suite personas:** CEO / CTO / CLO — intent only; Directory `kind: persona`.  
- **Marketplace template system:** `pmcro-marketplace-directory` scaffolder + Agent Directory; parallel session path reserved (Option A).  
- **Laws:** L-EVIDENCE, L-CHECKER-GATE, L-ORCHESTRATION, L-OUTPUT-CONTRACT remain mandatory.

---

## 4. Mapping to *your* repo (already somewhat configured)

| Repo surface | Stack role |
|--------------|------------|
| `ProjectName.AppHost` | Aspire topology |
| `ProjectName.Api` | gRPC/API orchestration edge |
| `ProjectName.GrpcService` | Protos, agent services |
| `plugins/pmcro-*` | Lifecycle + personas + aspire evidence plugin |
| `.pmcro/` | Laws, trails, queue, policies |
| This seed’s `.pmcro/directory` + scaffolder | Portable Directory + template system to merge carefully |

**Do not** duplicate lifecycle plugins into the cloud seed; **do** keep governance contracts identical.

---

## 5. Production readiness gates

| Gate | Requirement |
|------|-------------|
| P0 | Checker PASS + evidence on trail before any SEAL |
| P0 | No absolute/drive-letter paths in frames or skills |
| P0 | Empty provider registry preferred to fake MCP entries |
| P1 | OTel traces from MAF → Aspire dashboard / App Insights |
| P1 | CopilotKit HITL bound to `requireApprovalForMutation` |
| P1 | Skills progressive disclosure (name/description first) |
| P2 | Hyperlight CodeAct only behind capability + non-preview dependency policy |
| P2 | CI runs scaffold-skill eval fixtures |
| P2 | gRPC contract tests + REST OpenAPI publish |

---

## 6. Suggested build sequence (on the real repo)

1. **Stabilize Aspire AppHost** — all services discoverable; dashboard green.  
2. **Wire MAF agents** to existing plugins (Orchestrator first).  
3. **Expose AG-UI** from one agent; attach CopilotKit starter (dotnet sample).  
4. **Enforce `.pmcro` output contract** on completions (validator already in this seed).  
5. **Marketplace:** register scaffolder; generate personas via Directory.  
6. **CodeAct:** enable in non-prod with Hyperlight preview; promote when stable.  
7. **C-Suite:** CEO/CTO/CLO skills as intent routers into Seed Intent queue.

---

## 7. What is *not* claimed

- Hyperlight CodeAct is **not** declared production-stable in this ADR (preview packages).  
- This cloud workspace is **not** the full Aspire host (no AppHost processes here).  
- Parallel-session marketplace work is **not** overwritten.  

---

## 8. Decision

**Adopt** this hybrid stack as the company target architecture:  
**Aspire + MAF (Harness) + gRPC core + REST/AG-UI/CopilotKit edge + Agent Skills marketplace + PMCRO governance**, with **CodeAct/Hyperlight** behind explicit maturity gates.

Next governed action on the real machine: open a PMCRO cycle with seed  
*“Align AppHost and OrchestrationApi to ADR-pmcro-enterprise-hybrid-stack; expose one AG-UI endpoint for CopilotKit; keep Hyperlight CodeAct behind capability flag.”*
