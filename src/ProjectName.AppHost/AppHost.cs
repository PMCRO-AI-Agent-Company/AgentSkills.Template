using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// The repository is the runtime's authoritative workspace. Keep the value
// parameterized so the AppHost never embeds a machine-specific drive/path.
var repoRoot = builder.AddParameter("repoRoot", () => Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "..", "..")));

// Persistent local Ollama model service.
var ollama = builder
    .AddOllama("ollama-server")
    .WithGPUSupport(OllamaGpuVendor.Nvidia)
    .WithLifetime(ContainerLifetime.Persistent)
    .WithDataVolume("ollama-data")
    .WithEnvironment("OLLAMA_CONTEXT_LENGTH", "16384")
    .WithEnvironment("OLLAMA_FLASH_ATTENTION", "0");

var modelOrchestrator = ollama.AddModel("model-orchestrator", "qwen3:8b");

// MCP actuator servers remain separate process boundaries from the agent runtime.
var filesystem = builder.AddProject<Projects.ProjectName_Mcp_Filesystem>("projectname-mcp-filesystem")
    .WithEnvironment("Filesystem__SandboxRoot", repoRoot)
    .WithReference(modelOrchestrator)
    .WaitFor(modelOrchestrator);

var terminal = builder.AddProject<Projects.ProjectName_Mcp_Terminal>("projectname-mcp-terminal")
    .WithEnvironment("Terminal__WorkingRoot", repoRoot)
    .WithReference(modelOrchestrator)
    .WaitFor(modelOrchestrator);

var playwright = builder.AddProject<Projects.ProjectName_Mcp_Playwright>("projectname-mcp-playwright")
    .WithReference(modelOrchestrator)
    .WaitFor(modelOrchestrator);

// Runtime is the MAF agent/workflow boundary. Explicit MCP references enable
// Aspire service discovery for the native MCP client while preserving process isolation.
var runtime = builder.AddProject<Projects.ProjectName_GrpcService>("projectname-grpcservice")
    .WithReference(ollama)
    .WithReference(modelOrchestrator)
    .WithReference(filesystem)
    .WithReference(terminal)
    .WithReference(playwright)
    .WaitFor(modelOrchestrator)
    .WaitFor(filesystem)
    .WaitFor(terminal)
    .WaitFor(playwright);

// Thin HTTP/gRPC facade. HTTP chat calls cross the runtime boundary over gRPC.
var api = builder.AddProject<Projects.ProjectName_Api>("projectname-api")
    .WithReference(runtime)
    .WithReference(modelOrchestrator)
    .WithEnvironment("Workspace__RepoRoot", repoRoot)
    .WaitFor(runtime);

// CopilotKit is a UI boundary only; its server-side runtime talks to the API AG-UI proxy.
builder.AddJavaScriptApp("projectname-copilotkit", "../../ui/projectname-copilotkit")
    .WithHttpEndpoint(port: 3000, env: "PORT")
    .WithEnvironment("AGUI_BACKEND_URL", $"{api.GetEndpoint("https")}/ag-ui")
    .WithEnvironment("WORKSPACE_API_URL", $"{api.GetEndpoint("https")}/api/workspace/index")
    .WithReference(api)
    .WaitFor(api);

builder.Build().Run();
