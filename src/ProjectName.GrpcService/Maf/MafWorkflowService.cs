using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Extensions.AI;
using ProjectName.GrpcService.Mcp;

namespace ProjectName.GrpcService.Maf;

public sealed class MafWorkflowService
{
    private readonly AIAgent _workflowAgent;

    public MafWorkflowService(IChatClient chatClient, McpNativeToolProvider mcp)
    {
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
                Tools = makerTools
            }
        });
        var checker = CreateAgent(chatClient, "checker", "Audit the preceding output for correctness, completeness, risks, and evidence gaps. Do not silently accept defects.", skillsProvider);
        var reflector = CreateAgent(chatClient, "reflector", "Reflect on the audited result. Summarize the verified outcome, unresolved issues, and next intent. Do not claim execution that did not occur.", skillsProvider);

        var workflow = AgentWorkflowBuilder.BuildSequential(
            "pmcro-lifecycle",
            chainOnlyAgentResponses: true,
            new[] { planner, maker, checker, reflector });

        _workflowAgent = workflow.AsAIAgent("pmcro-lifecycle", "PMCRO Lifecycle", "Planner, Maker, Checker, Reflector workflow with native MCP actuator tools and repository Agent Skills.");
    }

    public AIAgent Agent => _workflowAgent;

    public Task<AgentResponse> RunAsync(string prompt, CancellationToken cancellationToken = default)
        => _workflowAgent.RunAsync($"/no_think\n{prompt}", cancellationToken: cancellationToken);

    private static AIAgent CreateAgent(IChatClient chatClient, string name, string instructions, AgentSkillsProvider skillsProvider)
        => new ChatClientAgent(chatClient, new ChatClientAgentOptions
        {
            Name = name,
            AIContextProviders = [skillsProvider],
            ChatOptions = new ChatOptions { Instructions = instructions }
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
