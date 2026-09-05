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
        var planner = CreateAgent(chatClient, "planner", "Plan the requested work. Produce a concise, actionable plan.");

        // MCP tools are attached only to the Maker. Planner, Checker and Reflector
        // remain tool-free so governance/evaluation phases cannot mutate actuators.
        var makerTools = mcp.GetMakerTools("filesystem-agent")
            .Concat(mcp.GetMakerTools("terminal-agent"))
            .Concat(mcp.GetMakerTools("playwright-agent"))
            .GroupBy(t => t.Name, StringComparer.OrdinalIgnoreCase)
            .Select(g => g.First())
            .ToArray();

        var maker = new ChatClientAgent(chatClient, new ChatClientAgentOptions
        {
            Name = "maker",
            ChatOptions = new ChatOptions
            {
                Instructions = "Execute the plan using at most one MCP tool call. Follow each tool safety contract exactly. TYPE1_PENDING is evidence that approval is required; never bypass it. Do not claim a side effect occurred unless the tool result proves it.",
                Tools = makerTools
            }
        });
        var checker = CreateAgent(chatClient, "checker", "Audit the preceding output for correctness, completeness, risks, and evidence gaps. Do not silently accept defects.");
        var reflector = CreateAgent(chatClient, "reflector", "Reflect on the audited result. Summarize the verified outcome, unresolved issues, and next intent. Do not claim execution that did not occur.");

        var workflow = AgentWorkflowBuilder.BuildSequential(
            "pmcro-lifecycle",
            chainOnlyAgentResponses: true,
            new[] { planner, maker, checker, reflector });

        _workflowAgent = workflow.AsAIAgent("pmcro-lifecycle", "PMCRO Lifecycle", "Planner, Maker, Checker, Reflector workflow with native MCP actuator tools behind the Maker boundary.");
    }

    public AIAgent Agent => _workflowAgent;

    public Task<AgentResponse> RunAsync(string prompt, CancellationToken cancellationToken = default)
        => _workflowAgent.RunAsync($"/no_think\n{prompt}", cancellationToken: cancellationToken);

    private static AIAgent CreateAgent(IChatClient chatClient, string name, string instructions)
        => new ChatClientAgent(chatClient, instructions: instructions, name: name);
}



