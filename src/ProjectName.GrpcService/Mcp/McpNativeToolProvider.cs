using System.Collections.Concurrent;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

namespace ProjectName.GrpcService.Mcp;

/// <summary>
/// Native MCP client boundary. MCP owns transport/protocol; runtime owns
/// subject-agent routing and the policy boundary around side effects.
/// </summary>
public sealed class McpNativeToolProvider(
    IHttpClientFactory httpClientFactory,
    ILogger<McpNativeToolProvider> logger)
{
    private readonly ConcurrentDictionary<string, IReadOnlyList<AITool>> _tools = new(StringComparer.OrdinalIgnoreCase);
    private readonly ConcurrentDictionary<string, McpClient> _clients = new(StringComparer.OrdinalIgnoreCase);

    public IReadOnlyList<AITool> GetMakerTools(string subjectAgent)
    {
        if (_tools.TryGetValue(subjectAgent, out var cached))
            return cached;

        var server = subjectAgent switch
        {
            "filesystem-agent" => "mcp-filesystem",
            "terminal-agent" => "mcp-terminal",
            "playwright-agent" => "mcp-playwright",
            _ => null
        };

        if (server is null)
            return [];

        var client = GetOrCreateClient(server);
        var discovered = client.ListToolsAsync().GetAwaiter().GetResult().Cast<AITool>().ToArray();

        // Governance boundary (L-ORCHESTRATION; EC-002 "Single Dispatcher" per the
        // mcp-terminal/mcp-playwright tool descriptions): TYPE1 side-effecting
        // actions are exposed as a pending "Request" tool (e.g. RunCommand) plus a
        // privileged "Execute*" tool (e.g. ExecuteRunCommand) that those servers'
        // own docs say only the Orchestrator may dispatch, after HIL approval.
        // This workflow has no Orchestrator agent, and until one - or a real
        // approval step - exists, Maker must not hold the Execute* tools directly;
        // the MCP servers themselves do not check caller identity, so this was
        // previously enforced only by tool-description text aimed at the LLM.
        // See .pmcro/design/AUDIT-claude-architecture-review-2026-09-06.md finding 6.7.
        var tools = discovered
            .Where(t => !t.Name.StartsWith("Execute", StringComparison.Ordinal))
            .ToArray();
        var withheldCount = discovered.Length - tools.Length;

        _tools[subjectAgent] = tools;
        logger.LogInformation(
            "[MCP-NATIVE] {SubjectAgent}: discovered {ToolCount} tools from {Server} ({WithheldCount} ORCHESTRATOR-ONLY Execute* tool(s) withheld from Maker pending a real approval path)",
            subjectAgent, tools.Length, server, withheldCount);
        return tools;
    }

    public IReadOnlyList<(string Name, string Description)> GetCatalog(string subjectAgent) =>
        GetMakerTools(subjectAgent).Select(t => (t.Name, t.Description)).ToArray();

    private McpClient GetOrCreateClient(string serverName)
    {
        if (_clients.TryGetValue(serverName, out var existing))
            return existing;

        var httpClient = httpClientFactory.CreateClient(serverName);
        var baseAddress = httpClient.BaseAddress
            ?? throw new InvalidOperationException($"MCP client '{serverName}' has no BaseAddress.");

        var transport = new HttpClientTransport(new HttpClientTransportOptions
        {
            Endpoint = new Uri(baseAddress, "/mcp"),
            TransportMode = HttpTransportMode.StreamableHttp,
            ConnectionTimeout = TimeSpan.FromSeconds(30),
        }, httpClient);

        var created = McpClient.CreateAsync(transport).GetAwaiter().GetResult();
        if (_clients.TryAdd(serverName, created))
            return created;

        created.DisposeAsync().AsTask().GetAwaiter().GetResult();
        return _clients[serverName];
    }
}
