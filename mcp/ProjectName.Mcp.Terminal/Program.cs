using ModelContextProtocol.AspNetCore;
using ProjectName.Mcp.Terminal.Configuration;
using ProjectName.Mcp.Terminal.Prompts;
using ProjectName.Mcp.Terminal.Resources;
using ProjectName.Mcp.Terminal.Tools;

var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

var workingRoot = builder.Configuration["Terminal:WorkingRoot"]
    ?? Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "..", ".."));

builder.Services.AddSingleton(new TerminalConfig
{
    WorkingRoot = workingRoot,
    CommandTimeoutSeconds = int.TryParse(builder.Configuration["Terminal:CommandTimeoutSeconds"], out var t) ? t : 30,
    MaxOutputBytes = int.TryParse(builder.Configuration["Terminal:MaxOutputBytes"], out var m) ? m : 65536
});
builder.Services.AddSingleton<TerminalTools>();
builder.Services.AddSingleton<TerminalResources>();
builder.Services.AddSingleton<TerminalPrompts>();

builder.Services.AddMcpServer()
    .WithHttpTransport(options => options.Stateless = true)
    .WithTools<TerminalTools>()
    .WithResources<TerminalResources>()
    .WithPrompts<TerminalPrompts>();

var app = builder.Build();
app.MapDefaultEndpoints();
app.MapMcp("/mcp");
app.MapGet("/", () => new
{
    service = "ProjectName.Mcp.Terminal",
    status = "ready",
    workingRoot,
    transport = "Streamable HTTP (Stateless=true)",
    mcpEndpoint = "/mcp"
});
app.Run();
