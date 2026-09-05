using ModelContextProtocol.AspNetCore;
using ProjectName.Mcp.Filesystem.Configuration;
using ProjectName.Mcp.Filesystem.Prompts;
using ProjectName.Mcp.Filesystem.Resources;
using ProjectName.Mcp.Filesystem.Tools;

var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

builder.Services.AddSingleton<FilesystemConfig>();
builder.Services.AddSingleton<FilesystemTools>();
builder.Services.AddSingleton<FilesystemResources>();
builder.Services.AddSingleton<FilesystemPrompts>();

builder.Services.AddMcpServer()
    .WithHttpTransport(options => options.Stateless = true)
    .WithTools<FilesystemTools>()
    .WithResources<FilesystemResources>()
    .WithPrompts<FilesystemPrompts>();

var app = builder.Build();
app.MapDefaultEndpoints();
app.MapMcp("/mcp");
app.MapGet("/", (FilesystemConfig config) => new
{
    service = "ProjectName.Mcp.Filesystem",
    status = "ready",
    transport = "Streamable HTTP (Stateless=true)",
    mcpEndpoint = "/mcp",
    sandboxRoot = config.SandboxRoot,
    maxFileSizeBytes = config.MaxFileSizeBytes
});
app.Run();
