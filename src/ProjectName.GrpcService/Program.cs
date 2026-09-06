using Microsoft.Agents.AI;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI.Hosting.AGUI.AspNetCore;
using ProjectName.GrpcService.Governance;
using ProjectName.GrpcService.Maf;
using ProjectName.GrpcService.Mcp;
using ProjectName.GrpcService.Services;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.ConfigureKestrel(options => options.ConfigureEndpointDefaults(endpoint => endpoint.Protocols = HttpProtocols.Http1AndHttp2));
builder.AddServiceDefaults();
builder.AddOllamaApiClient("model-orchestrator").AddChatClient();
builder.Services.AddGrpc();
builder.Services.AddAGUIServer();
builder.Services.AddSingleton<McpNativeToolProvider>();

builder.Services.AddHttpClient("mcp-filesystem", client => client.BaseAddress = new Uri("http://projectname-mcp-filesystem"));
builder.Services.AddHttpClient("mcp-terminal", client => client.BaseAddress = new Uri("http://projectname-mcp-terminal"));
builder.Services.AddHttpClient("mcp-playwright", client => client.BaseAddress = new Uri("http://projectname-mcp-playwright"));
builder.Services.AddSingleton<MafWorkflowService>();
builder.Services.AddSingleton<TrailRuntimeGateway>();

var app = builder.Build();
app.MapDefaultEndpoints();
app.MapGrpcService<RuntimeChatService>();
var workflowAgent = app.Services.GetRequiredService<MafWorkflowService>().Agent;
app.MapAGUIServer("/ag-ui", workflowAgent);

const string ollamaModel = "qwen3:8b";

app.MapGet("/", () => Results.Ok(new
{
    service = "ProjectName.GrpcService",
    transport = "gRPC",
    provider = "ollama",
    model = ollamaModel,
    workflow = "MAF AgentWorkflowBuilder: Planner -> Maker -> Checker -> Reflector",
    status = "ready"
}));

app.MapGet("/chat", async (string prompt, MafWorkflowService workflow, TrailRuntimeGateway trail, CancellationToken cancellationToken) =>
{
    if (string.IsNullOrWhiteSpace(prompt))
        return Results.BadRequest(new { error = "prompt is required" });

    var response = await workflow.RunGovernedAsync(prompt, trail, cancellationToken);
    return Results.Ok(new { model = ollamaModel, response = response.ToString() });
});

app.Run();
