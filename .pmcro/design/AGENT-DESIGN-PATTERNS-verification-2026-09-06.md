# Agent design pattern alignment + API verification pass — 2026-09-06

**Trail:** `6ea3bd04-b697-4856-abf3-bcb8cfae57a5` (sealed)
**Why:** the repo owner asked that ongoing autonomous work draw on Microsoft Agent Framework (MAF) and
Anthropic agent-design best practices, and separately, trail `6ea25a3f-acf4-4dcf-ac62-4db1fb62aaf7` remains
open (Checker verdict FAIL) because four C# files were hand-edited with no compiler reachable from either
the cloud container or the bridged device shell. This trail does not close that gap — only a real
`dotnet build` can — but it does everything short of that: it checks the specific, novel API calls those
edits depend on against real primary sources, not training-data recall.

## Part 1 — Anthropic pattern mapping

Per Anthropic's ["Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents),
the named workflow patterns are: **prompt chaining** (fixed sequential steps with programmatic gates),
**routing** (classify then dispatch), **parallelization** (sectioning or voting), **orchestrator-workers**
(dynamic decomposition + delegation), and **evaluator-optimizer** (generator + iterative critic loop), with
plain **autonomous agents** as the more open-ended alternative. Guidance: use the simplest pattern that
works; add complexity only when it demonstrably improves outcomes; prioritize transparency in planning
steps.

This repo's PMCR-O lifecycle is not an ad hoc invention against these patterns — it is a composition of two
of them, already correctly identified as such by its own design:

- **Prompt chaining**: Planner → Maker → Checker → Reflector is a fixed sequence with a programmatic gate
  between Checker and Reflector (`VERDICT: PASS|FAIL` must parse; L-CHECKER-GATE refuses `SEAL` without an
  explicit `PASS`). This is close to Anthropic's chaining diagram verbatim, gate included.
- **Evaluator-optimizer**: Checker (evaluator) and Reflector (decides `SEAL` vs `RETRY`, i.e. whether to
  loop back) form exactly the generator/critic loop the pattern describes, with the loop boundary being a
  new trail rather than an in-process retry.

Anthropic's "start simple" principle also retroactively validates a decision already made in this repo:
`create-skill`'s 2026-09-05 redesign (v0.3.0) replaced a heavier scaffold.py/JSON-spec/MAF-codegen pipeline
with a plain template-copy + validator — i.e. dropped complexity that wasn't earning its keep, in favor of
the simpler mechanism, exactly the direction Anthropic's guidance points.

**Not currently used, and not obviously needed:** orchestrator-workers (would apply if Maker's single step
needed dynamic fan-out to an unknown number of sub-tasks — not the case today) and parallelization (no
independent subtasks currently run concurrently in the lifecycle). Worth reconsidering only if a future
Maker step genuinely needs either.

## Part 2 — API verification (trail `6ea25a3f` risk reduction, not resolution)

Three API surfaces used in the untested C# changes were the highest-risk unknowns, because they use MAF
preview packages (`Microsoft.Agents.AI*` 1.20.0 / 1.20.0-preview.260831.1 per `Directory.Packages.props`)
and the MCP C# SDK (`ModelContextProtocol` 2.2.0). Each was checked against a primary source, not memory:

1. **`AgentWorkflowBuilder.BuildSequential("pmcro-lifecycle", chainOnlyAgentResponses: true, new[] {...})`**
   (`MafWorkflowService.cs`, constructor). Verified against the actual source of
   `dotnet/src/Microsoft.Agents.AI.Workflows/AgentWorkflowBuilder.cs` on the `microsoft/agent-framework`
   `main` branch: an overload `BuildSequential(string workflowName, bool chainOnlyAgentResponses, params
   IEnumerable<AIAgent> agents)` exists verbatim. Match confirmed.

2. **`_workflowAgent.AsBuilder().Use(runFunc:, runStreamingFunc:).Build()`** (`MafWorkflowService.cs`,
   `CreateGovernedAgent`). Verified two ways: (a) the raw source of
   `dotnet/src/Microsoft.Agents.AI/AIAgentBuilder.cs` (same repo/branch) defines exactly
   `AIAgentBuilder Use(Func<IEnumerable<ChatMessage>, AgentSession?, AgentRunOptions?, AIAgent,
   CancellationToken, Task<AgentResponse>>? runFunc, Func<..., IAsyncEnumerable<AgentResponseUpdate>>?
   runStreamingFunc)`, whose parameter order matches `RunWithEvidenceAsync`'s/
   `RunStreamingWithEvidenceAsync`'s actual signatures exactly; (b) the official
   [middleware doc](https://learn.microsoft.com/en-us/agent-framework/agents/middleware/) — the same page
   `TrailRuntimeGateway.cs`'s own comment already cites — shows the identical
   `originalAgent.AsBuilder().Use(runFunc: ..., runStreamingFunc: ...).Build()` pattern. Match confirmed
   both ways.

3. **`new HttpClientTransport(new HttpClientTransportOptions {...}, httpClient)` +
   `McpClient.CreateAsync(transport)`** (`McpNativeToolProvider.cs`). Verified against
   `modelcontextprotocol/csharp-sdk`'s own
   [transports doc](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/transports/transports.md)
   (Streamable HTTP client sample uses `HttpClientTransport(HttpClientTransportOptions)` +
   `McpClient.CreateAsync(transport)`) and the raw source of
   `src/ModelContextProtocol.Core/Client/HttpClientTransport.cs`, which defines the 2-arg constructor
   `HttpClientTransport(HttpClientTransportOptions transportOptions, HttpClient httpClient,
   ILoggerFactory? loggerFactory = null, bool ownsHttpClient = false)` used here to reuse the DI-injected
   named `HttpClient`. Match confirmed.

**What this does and does not establish.** All three of the most novel API calls in the blocked files match
real, current, primary-source APIs exactly — this is real evidence, not a guess, and substantially lowers
the probability that `dotnet build` fails because of these specific calls. It does **not** rule out: a
trivial typo elsewhere in the ~660 lines touched, a version mismatch between the pinned preview packages and
what's actually restorable, or an issue in a part of the files not covered by this check (e.g.
`AgentSkillsProvider`/`AgentFileSkillsSourceOptions` in `MafWorkflowService.CreateSkillsProvider`, not
checked this pass). Per L-EVIDENCE, this is recorded as risk-reduction, not as a substitute for actually
running `dotnet build ProjectName.slnx` on a machine with the pinned `11.0.100-preview.7.26381.103` SDK —
trail `6ea25a3f` remains open.

## Sources

- https://www.anthropic.com/research/building-effective-agents
- https://raw.githubusercontent.com/microsoft/agent-framework/main/dotnet/src/Microsoft.Agents.AI.Workflows/AgentWorkflowBuilder.cs
- https://raw.githubusercontent.com/microsoft/agent-framework/main/dotnet/src/Microsoft.Agents.AI/AIAgentBuilder.cs
- https://learn.microsoft.com/en-us/agent-framework/agents/middleware/
- https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/transports/transports.md
- https://raw.githubusercontent.com/modelcontextprotocol/csharp-sdk/main/src/ModelContextProtocol.Core/Client/HttpClientTransport.cs
