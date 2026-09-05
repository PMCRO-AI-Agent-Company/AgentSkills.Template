# Clean architecture — Aspire + Orchestration API + CopilotKit

**Tone:** practical, not exaggerated. Your Aspire stack already runs (synth/chat via API). This doc is the thin alignment layer.

---

## What you already have (keep)

```text
AppHost
  ├── Runtime          (gRPC, models / agents)
  └── OrchestrationApi (HTTP + gRPC client → Runtime)
        └── GET /api/chat  (works today)
```

Parameterized `repoRoot`, Ollama (or your model path), ServiceDefaults — leave that working path alone.

---

## Clean layering (no extra drama)

| Layer | Responsibility | Avoid |
|-------|----------------|--------|
| **AppHost** | Topology, references, env | Business logic, agent prompts |
| **OrchestrationApi** | HTTP/REST edge, auth later, AG-UI bridge | Model calls directly (prefer Runtime) |
| **Runtime** | MAF / IChatClient / gRPC contracts | UI concerns |
| **.pmcro/** | Laws, Directory, trails, capability flags | AppHost process code |
| **plugins / .agents/skills** | Portable skills & personas | Hard-coded into AppHost |
| **CopilotKit (frontend)** | Chat UI, HITL, generative UI | Bypassing OrchestrationApi |

Rule: **UI → OrchestrationApi → Runtime → model**. Don’t skip layers “because it’s faster.”

---

## Aspire integrations (measured)

Add only when you need them:

1. **OpenTelemetry → Aspire dashboard** — already natural with ServiceDefaults; keep traces on chat path.
2. **AG-UI endpoint on OrchestrationApi** — one route family for CopilotKit (`/ag-ui`), not a second chat stack.
3. **Config flags** — e.g. `Hyperlight:CodeAct:Enabled` default `false` until you intentionally adopt preview isolation.
4. **Service discovery** — keep `https://projectname-runtime` style names; no machine paths in config.

Skip until required: extra containers, dual frontends, reinvented queues inside AppHost.

---

## CopilotKit (minimal path)

1. OrchestrationApi exposes AG-UI-compatible base (or interim `/ag-ui/message` → same Runtime gateway as `/api/chat`).
2. Next (or your SPA) hosts CopilotKit with `runtimeUrl` pointing at that base.
3. HITL approvals = your policy for mutations; chat-only can stay simple.

Official path: CopilotKit docs for **Microsoft Agent Framework** + AG-UI. Use package versions from NuGet/npm at implement time — don’t pin fantasy versions here.

---

## PMCRO without ceremony

| Use | Don’t use for |
|-----|----------------|
| Directory = who agents are | Replacing Aspire |
| Skills = how agents behave | Blocking `/api/chat` that already works |
| Capability flags = risky features off by default | Inventing providers |
| Trails = audit when you run governed cycles | Mandatory for every synth token |

Your working API is the product. PMCRO is governance **around** it, not a rewrite.

---

## Suggested next small steps (autonomous backlog)

1. Add `/ag-ui/health` (+ optional message bridge to existing Runtime gateway) on OrchestrationApi.
2. `appsettings`: `Hyperlight:CodeAct:Enabled: false`.
3. CopilotKit sample app pointed at OrchestrationApi — only when you want UI.
4. Keep `plugins/pmcro-marketplace` parallel work untouched if it exists on your PC.

No need to clone GitHub into this cloud folder again.
