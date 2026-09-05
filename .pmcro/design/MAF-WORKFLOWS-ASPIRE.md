# MAF Workflows + Aspire (no CopilotKit)

**User preference:** command-style agents; existing API chat is enough; skip CopilotKit UX.

## Mapping

| Aspire | MAF | PMCRO |
|--------|-----|--------|
| AppHost project graph | Host processes | Does not replace Directory |
| Runtime project | Agents + **Workflows** (sequential, concurrent, handoff) | Maker/Checker evidence still required for governed cycles |
| OrchestrationApi | HTTP edge → gRPC Runtime | Seed intents can enter via API later |
| ServiceDefaults / OTel | Agent OpenTelemetry | Trail correlation ids |

## Workflow patterns to use on Runtime (when you wire MAF)

1. **Sequential** — Plan-like stages when order matters  
2. **Handoff** — specialist agents (closest to Orchestrator → Planner → Maker)  
3. **Concurrent** — parallel research only when Checker can still gate merge  

Harness Agent (MAF GA) helps long multi-step runs; **Reflector seal** remains a PMCRO governance act, not a harness feature.

## CodeAct

Keep behind `hyperlight-codeact` capability flag (default off). Preview packages only when you opt in.

## Commands (product)

Keep `/api/chat` as primary UX. Optional later: POST seed intent → queue_runtime claim path.
