# ADR — AG-UI/CopilotKit Trail-Evidence Wiring

**Status:** Decided and patched
**Date:** 2026-09-06
**Decided by:** Claude (Cowork), acting on explicit delegated autonomous authority ("leave all decisions to you... search online, figure out best practice") following `AUDIT-claude-architecture-review-2026-09-06.md`'s addendum, finding 15, and `TrailRuntimeGateway.cs`'s own previously-documented coverage gap.

## Question

`MafWorkflowService.RunGovernedAsync` records `.pmcro/` trail evidence (Plan/Make/Check/Reflect, gated by `trail_runtime.py`'s existing PASS/FAIL and SEAL-requires-PASS rules) for the gRPC `RuntimeChatService` and the debug `GET /chat` endpoint. The AG-UI/CopilotKit path (`Program.cs`: `app.MapAGUIServer("/ag-ui", workflowAgent)`) hands the same underlying agent directly to Microsoft's AG-UI ASP.NET Core hosting extension, which drives that agent's `RunAsync`/`RunStreamingAsync` internally and never calls back into `MafWorkflowService`. Result: the actual end-user-facing chat UI produced zero trail evidence for any turn, while the debug/gRPC paths produced full evidence for functionally the same underlying workflow.

## What research found

1. **The 5-role pipeline itself already runs identically on both paths.** `_workflowAgent` is `AgentWorkflowBuilder.BuildSequential(planner, maker, checker, reflector).AsAIAgent(...)` — a single `AIAgent` whose internal sequential execution (including the Checker step and its `VERDICT: PASS|FAIL` line) happens regardless of which entry point calls it. The gap was never "AG-UI skips governance computation" — it was "AG-UI's copy of that computation is never written to `.pmcro/trails/`."
2. **`trail_runtime.py`'s own gates govern trail sealing, not response delivery.** Neither `check` nor `reflect` in the existing Python CLI, nor `RunGovernedAsync`'s existing C# use of them, ever withholds a chat response on a FAIL verdict — a FAIL is recorded and the trail is left unsealed (`RETRY`), but the response still reaches the caller. This is a real, pre-existing design property, not something this change introduces or should quietly change.
3. **Microsoft Agent Framework has an official, documented extension point for exactly this shape of problem**: [agent middleware](https://learn.microsoft.com/agent-framework/agents/middleware/), via `AIAgent.AsBuilder().Use(runFunc:, runStreamingFunc:).Build()`. This wraps an existing `AIAgent` with pre/post logic around every call without needing framework internals, a custom `AIAgent` subclass, or protected-member guessing. The streaming variant's documented pattern (buffer `AgentResponseUpdate`s while yielding them through unchanged, then call the framework's own `updates.ToAgentResponse()` after the loop) is exactly the shape needed to record evidence from the already-known-complete response without delaying or altering what CopilotKit receives.
4. Two alternative, less-verifiable APIs were considered and rejected: subclassing `AIAgent` directly (protected `RunCoreAsync`/`RunCoreStreamingAsync` — verified via an official code sample, but a strictly larger, riskier surface than middleware for no added benefit here) and `DelegatingAIAgent` (a framework-provided decorator base class whose fetched documentation used different type names — `AgentRunResponse`/`AgentThread` — than the rest of this repo's already-compiling code, `AgentResponse`/`AgentSession`; likely a different preview-package version's docs. Given no compiler is available this session to resolve the discrepancy, the middleware API was preferred specifically because its verbatim example matched types already proven to compile in this repo.

## Decision

Added `MafWorkflowService.CreateGovernedAgent(TrailRuntimeGateway)`, which returns `_workflowAgent` wrapped with agent middleware that calls the same `RecordTrailEvidenceAsync` logic `RunGovernedAsync` already uses (extracted into a shared `TryRecordAsync` helper so the two entry points share one implementation rather than duplicating it). `Program.cs` now passes this governed agent to `MapAGUIServer` instead of the raw `workflowAgent`.

Evidence recording for the streaming case happens strictly *after* the `RunStreamingAsync` loop has already yielded every update to the caller — never before, never interleaved. This preserves the AG-UI path's real-time streaming UX unchanged and keeps the existing "evidence gates trail-sealing, not delivery" contract consistent across both entry points, rather than introducing a new, stricter, delivery-blocking behavior that only applies to one of the two paths.

## What this does NOT do

It does not make a FAIL verdict block or alter what CopilotKit's user sees — that would be a behavior change to the existing gRPC/REST contract too, not just an AG-UI fix, and was out of scope for closing an evidence-coverage gap. If synchronous pre-delivery gating is wanted later, it is a separate, larger decision affecting all three entry points uniformly, not something to bolt onto just the AG-UI path.

## Verification status

Not compiled. No .NET SDK was reachable from this session (neither the cloud container nor the bridged shell on the repo owner's machine, which runs in an isolated Linux VM separate from the Windows host's actual `dotnet` install). Every type and signature used here (`AIAgent.AsBuilder()`, `.Use(runFunc:, runStreamingFunc:)`, `AgentResponseUpdate`, `updates.ToAgentResponse()`, `[EnumeratorCancellation]`) was checked against an official Microsoft Learn documentation page with a complete, verbatim code sample rather than guessed, but **`dotnet build` on the repo owner's own machine is required before this is trusted**, per the standing caveat already on the rest of this session's C# changes.
