using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Extensions.AI;
using ProjectName.GrpcService.Governance;
using ProjectName.GrpcService.Mcp;

namespace ProjectName.GrpcService.Maf;

public sealed class MafWorkflowService
{
    private readonly AIAgent _workflowAgent;

    private readonly ILogger<MafWorkflowService>? _logger;

    public MafWorkflowService(IChatClient chatClient, McpNativeToolProvider mcp, ILogger<MafWorkflowService>? logger = null)
    {
        _logger = logger;
        var skillsProvider = CreateSkillsProvider();
        var planner = CreateAgent(chatClient, "planner", "Plan the requested work. Produce a concise, actionable plan.", skillsProvider);

        // MCP actuators remain attached only to the Maker. Skills are knowledge/context
        // providers and are available to every phase, but skill scripts are deliberately
        // filtered out here so execution remains behind the existing governed actuator path.
        var makerTools = mcp.GetMakerTools("filesystem-agent")
            .Concat(mcp.GetMakerTools("terminal-agent"))
            .Concat(mcp.GetMakerTools("playwright-agent"))
            .GroupBy(t => t.Name, StringComparer.OrdinalIgnoreCase)
            .Select(g => g.First())
            .ToArray();

        var maker = new ChatClientAgent(chatClient, new ChatClientAgentOptions
        {
            Name = "maker",
            AIContextProviders = [skillsProvider],
            ChatOptions = new ChatOptions
            {
                Instructions = "Execute the plan using at most one MCP tool call. Follow each tool safety contract exactly. TYPE1_PENDING is evidence that approval is required; never bypass it. Do not claim a side effect occurred unless the tool result proves it. Use an available skill when it matches the task.",
                Tools = makerTools,
                // Disable qwen3's thinking mode via Ollama's native "think" chat
                // parameter (Microsoft.Extensions.AI's documented weakly-typed
                // passthrough - OllamaSharp's IChatClient reads this key directly
                // off the /api/chat request, per microsoft/agent-framework#4089).
                // This governs every entry point uniformly (REST /chat AND
                // AG-UI/CopilotKit), unlike the previous "/no_think" prompt-prefix
                // hack in RunAsync below, which only /chat applied - the AG-UI
                // path drives these ChatClientAgent instances directly and never
                // saw that prefix, so its responses leaked raw <think> reasoning.
                AdditionalProperties = new AdditionalPropertiesDictionary { ["think"] = false }
            }
        });
        var checker = CreateAgent(chatClient, "checker",
            "Audit the preceding output for correctness, completeness, risks, and evidence gaps. " +
            "Do not silently accept defects. Begin your response with exactly one line, verbatim: " +
            "'VERDICT: PASS' or 'VERDICT: FAIL' (nothing else on that line), then your audit below it. " +
            "This line is parsed by .pmcro governance evidence and gates cycle completion (L-CHECKER-GATE) - " +
            "never omit it and never soften it into prose.",
            skillsProvider);
        var reflector = CreateAgent(chatClient, "reflector", "Reflect on the audited result. Summarize the verified outcome, unresolved issues, and next intent. Do not claim execution that did not occur.", skillsProvider);

        var workflow = AgentWorkflowBuilder.BuildSequential(
            "pmcro-lifecycle",
            chainOnlyAgentResponses: true,
            new[] { planner, maker, checker, reflector });

        _workflowAgent = workflow.AsAIAgent("pmcro-lifecycle", "PMCRO Lifecycle", "Planner, Maker, Checker, Reflector workflow with native MCP actuator tools and repository Agent Skills.");
    }

    public AIAgent Agent => _workflowAgent;

    public Task<AgentResponse> RunAsync(string prompt, CancellationToken cancellationToken = default)
        // Thinking mode is disabled per-agent via ChatOptions.AdditionalProperties
        // ["think"] = false (native Ollama passthrough - see CreateAgent/maker's
        // ChatOptions above), not via a "/no_think" prompt prefix. That prefix
        // previously lived here and only covered this REST entry point; it never
        // reached the AG-UI/CopilotKit path, which drives _workflowAgent directly.
        => _workflowAgent.RunAsync(prompt, cancellationToken: cancellationToken);

    private static readonly Regex VerdictLineRegex = new(@"^\s*VERDICT:\s*(PASS|FAIL)\s*$", RegexOptions.IgnoreCase | RegexOptions.Multiline);

    /// <summary>
    /// Same as <see cref="RunAsync"/>, plus a best-effort attempt to record this
    /// turn as a real, gated .pmcro trail via <paramref name="trail"/> - see
    /// TrailRuntimeGateway's remarks for exactly what this does and does not cover.
    /// Evidence recording NEVER affects the returned response: any failure here
    /// (python3 missing, unparseable output, whatever) is logged and swallowed,
    /// never thrown, and never changes what the caller gets back. This method
    /// does not yet cover the AG-UI/CopilotKit path (see TrailRuntimeGateway).
    /// </summary>
    public async Task<AgentResponse> RunGovernedAsync(string prompt, TrailRuntimeGateway trail, CancellationToken cancellationToken = default)
    {
        var response = await RunAsync(prompt, cancellationToken);

        if (trail.IsAvailable)
        {
            try
            {
                await RecordTrailEvidenceAsync(prompt, response, trail, cancellationToken);
            }
            catch (Exception ex)
            {
                // Deliberately never rethrown - see remarks above and on TrailRuntimeGateway.
                _logger?.LogWarning(ex, "[TRAIL] evidence recording failed for this turn; chat response is unaffected.");
            }
        }

        return response;
    }

    private async Task RecordTrailEvidenceAsync(string prompt, AgentResponse response, TrailRuntimeGateway trail, CancellationToken ct)
    {
        var trailId = await trail.OpenAsync(prompt, "maf-runtime", ct);
        if (trailId is null)
            return;

        var plannerText = ExtractAgentText(response, "planner");
        var makerText = ExtractAgentText(response, "maker");
        var checkerText = ExtractAgentText(response, "checker");
        var reflectorText = ExtractAgentText(response, "reflector");
        var overallText = response.Text ?? string.Empty;

        await trail.PlanAsync(trailId, new
        {
            role = "planner",
            goal = Truncate(plannerText ?? prompt, 500),
            success_criteria = new[] { "Checker records an explicit PASS/FAIL verdict for this turn (L-CHECKER-GATE)" },
            steps = new[] { new { id = "1", action = "Run the pmcro-lifecycle MAF workflow (Planner->Maker->Checker->Reflector) for this chat turn" } },
        }, ct);

        await trail.MakeAsync(trailId, new
        {
            role = "maker",
            step = "Execute the pmcro-lifecycle MAF workflow for this chat request",
            result = string.IsNullOrWhiteSpace(overallText) ? "fail" : "ok",
            artifact = "chat-response",
            evidence = NonEmptyOr(Truncate(makerText ?? overallText, 2000), "(no maker output captured)"),
        }, ct);

        // Extract the Checker's explicit "VERDICT: PASS|FAIL" line (see its
        // instructions in the constructor). No line, or anything else, is
        // treated as FAIL - never fabricate a PASS the model didn't actually
        // state (output-contract.md rule 7: escalate/halt, don't fabricate).
        var verdictMatch = checkerText is null ? null : VerdictLineRegex.Match(checkerText);
        var explicitVerdictFound = verdictMatch is { Success: true };
        var verdict = explicitVerdictFound ? verdictMatch!.Groups[1].Value.ToUpperInvariant() : "FAIL";

        var (checkOk, _) = await trail.CheckAsync(trailId, new
        {
            role = "checker",
            verdict,
            criteria = new Dictionary<string, bool>
            {
                ["workflow_produced_response"] = !string.IsNullOrWhiteSpace(overallText),
                ["checker_emitted_explicit_verdict_line"] = explicitVerdictFound,
            },
            notes = explicitVerdictFound
                ? Truncate(checkerText!, 2000)
                : "No 'VERDICT: PASS|FAIL' line found in Checker output; recorded as FAIL per L-EVIDENCE (a result that cannot satisfy the contract must escalate/halt, never fabricate compliance).",
        }, ct);

        var seal = checkOk && verdict == "PASS";
        await trail.ReflectAsync(trailId, new
        {
            role = "reflector",
            disposition = seal ? "SEAL" : "RETRY",
            summary = NonEmptyOr(Truncate(reflectorText ?? overallText, 1000), "(no reflector output captured)"),
            earned_constraints = Array.Empty<string>(),
            next_seed = (string?)null,
            stop_reason = seal ? null : "Checker did not record an explicit PASS verdict for this turn.",
            @sealed = seal,
        }, ct);
    }

    /// <summary>
    /// Best-effort extraction of one agent's own text from the chained response.
    /// Relies on ChatMessage.AuthorName being set to the agent's Name (planner/
    /// maker/checker/reflector, per ChatClientAgentOptions.Name above) - a
    /// stable Microsoft.Extensions.AI property, not a Microsoft Agent Framework
    /// preview API. If a framework version doesn't populate it for this
    /// orchestration mode, this returns null and callers fall back to the
    /// overall chained response text instead of failing.
    /// </summary>
    private static string? ExtractAgentText(AgentResponse response, string agentName) =>
        response.Messages
            ?.Where(m => string.Equals(m.AuthorName, agentName, StringComparison.OrdinalIgnoreCase))
            .Select(m => m.Text)
            .Where(t => !string.IsNullOrWhiteSpace(t))
            .LastOrDefault();

    private static string Truncate(string text, int maxLength) =>
        text.Length <= maxLength ? text : text[..maxLength] + "...[truncated]";

    private static string NonEmptyOr(string text, string fallback) =>
        string.IsNullOrWhiteSpace(text) ? fallback : text;

    private static AIAgent CreateAgent(IChatClient chatClient, string name, string instructions, AgentSkillsProvider skillsProvider)
        => new ChatClientAgent(chatClient, new ChatClientAgentOptions
        {
            Name = name,
            AIContextProviders = [skillsProvider],
            ChatOptions = new ChatOptions
            {
                Instructions = instructions,
                // See the maker's ChatOptions above for why this lives here
                // (native "think" passthrough) rather than as a prompt prefix.
                AdditionalProperties = new AdditionalPropertiesDictionary { ["think"] = false }
            }
        });

    private static AgentSkillsProvider CreateSkillsProvider()
    {
        var skillsRoot = ResolveSkillsRoot();
        return new AgentSkillsProvider(
            skillsRoot,
            scriptRunner: null,
            fileOptions: new AgentFileSkillsSourceOptions
            {
                SearchDepth = 2,
                ScriptFilter = _ => false
            },
            options: new AgentSkillsProviderOptions
            {
                DisableLoadSkillApproval = true,
                DisableReadSkillResourceApproval = true,
                DisableRunSkillScriptApproval = false
            });
    }

    private static string ResolveSkillsRoot()
    {
        var configured = Environment.GetEnvironmentVariable("AGENT_SKILLS_ROOT");
        if (!string.IsNullOrWhiteSpace(configured) && Directory.Exists(configured))
            return Path.GetFullPath(configured);

        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null)
        {
            var candidate = Path.Combine(current.FullName, ".agents", "skills");
            if (Directory.Exists(candidate))
                return candidate;
            current = current.Parent;
        }

        throw new DirectoryNotFoundException(
            "Could not locate .agents/skills. Set AGENT_SKILLS_ROOT to an explicit skills directory.");
    }
}
