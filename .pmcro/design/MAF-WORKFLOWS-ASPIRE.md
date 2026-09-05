# MAF Workflows + Aspire (no CopilotKit)

**User preference:** command-style agents; existing API chat is enough; skip CopilotKit UX.

## Mapping

| Aspire | MAF | PMCRO |
|--------|-----|--------|
| AppHost project graph | Host processes | Does not replace Directory |
| ProjectName.GrpcService | Agents + **Workflows** (sequential, concurrent, handoff) | Maker/Checker evidence still required for governed cycles |
| ProjectName.Api | HTTP edge → gRPC ProjectName.GrpcService | Seed intents can enter via API later |
| ServiceDefaults / OTel | Agent OpenTelemetry | Trail correlation ids |

## Workflow patterns to use on ProjectName.GrpcService (wired)

1. **Sequential** — Plan-like stages when order matters  
2. **Handoff** — specialist agents (closest to Orchestrator → Planner → Maker)  
3. **Concurrent** — parallel research only when Checker can still gate merge  

Harness Agent (MAF GA) helps long multi-step runs; **Reflector seal** remains a PMCRO governance act, not a harness feature.

## CodeAct

Keep behind `hyperlight-codeact` capability flag (default off). Preview packages only when you opt in.

## Commands (product)

Keep `/api/chat` as primary UX. Optional later: POST seed intent → queue_runtime claim path.

## Current implementation (verified 2026-09-05)

`ProjectName.GrpcService` now uses the MAF .NET workflow API directly. `MafWorkflowService` creates four `ChatClientAgent` instances backed by the Aspire/Ollama `IChatClient`, then composes them with `AgentWorkflowBuilder.BuildSequential`:

`Planner -> Maker -> Checker -> Reflector`

The workflow is exposed through MAF's `AsAIAgent` surface and is invoked by both the gRPC `RuntimeChat` service and the existing `/chat` development endpoint. The API edge remains `ProjectName.Api -> gRPC -> ProjectName.GrpcService`.

This is intentionally the first MAF integration layer, not a claim that the template already implements the full PMCRO governance engine. Laws, evidence, trail sealing, and deterministic gates remain `.pmcro` responsibilities and must be integrated before this workflow is treated as a governed autonomous cycle.

## Design boundary

- **MAF owns execution composition:** agents, workflow topology, events, and workflow runtime behavior.
- **PMCRO owns governance:** laws, evidence requirements, approval policy, trail state, verdict/seal, and output contract.
- **Aspire owns service topology:** Ollama dependency, service discovery, health, telemetry, and process orchestration.
- **ProjectName.Api owns the HTTP edge:** REST/OpenAPI-facing product contract; it does not own agent orchestration.
- **Declarative workflows remain optional:** the package is present for future YAML-defined workflows, but programmatic MAF workflows are the default because they are the clearest typed foundation for the template.
- **Harness remains optional:** long-running execution can be layered on later without replacing the PMCRO Reflector/seal responsibility.
