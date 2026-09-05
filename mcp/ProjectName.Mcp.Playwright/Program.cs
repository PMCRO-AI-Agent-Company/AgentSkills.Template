using ModelContextProtocol.AspNetCore;
using ProjectName.Mcp.Playwright.Configuration;
using ProjectName.Mcp.Playwright.Prompts;
using ProjectName.Mcp.Playwright.Resources;
using ProjectName.Mcp.Playwright.Tools;

var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

builder.Services.AddSingleton<PlaywrightConfig>();
builder.Services.AddSingleton<PlaywrightSessionManager>();
builder.Services.AddSingleton<PlaywrightTools>();
builder.Services.AddSingleton<PlaywrightResources>();
builder.Services.AddSingleton<PlaywrightPrompts>();

builder.Services.AddMcpServer()
    .WithHttpTransport(options => options.Stateless = true)
    .WithTools<PlaywrightTools>()
    .WithResources<PlaywrightResources>()
    .WithPrompts<PlaywrightPrompts>();

var app = builder.Build();
app.MapDefaultEndpoints();
app.MapMcp("/mcp");
app.MapGet("/", () => new
{
    service = "ProjectName.Mcp.Playwright",
    status = "ready",
    transport = "Streamable HTTP (Stateless=true)",
    mcpEndpoint = "/mcp",
    browser = "Patchright"
});
app.Run();
