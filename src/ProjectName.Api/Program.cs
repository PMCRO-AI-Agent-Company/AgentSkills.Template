using Microsoft.AspNetCore.Server.Kestrel.Core;
using ProjectName.Api.Services;
using ProjectName.GrpcService;
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.ConfigureKestrel(options => options.ConfigureEndpointDefaults(endpoint => endpoint.Protocols = HttpProtocols.Http1AndHttp2));
builder.AddServiceDefaults();

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddGrpc();
builder.Services.AddHttpClient("runtime-agui", client => client.BaseAddress = new Uri("https://projectname-grpcservice"));
builder.Services.AddGrpcClient<RuntimeChat.RuntimeChatClient>(options =>
{
    options.Address = new Uri("https://projectname-grpcservice");
});
builder.Services.AddScoped<RuntimeGatewayService>();
builder.Services.AddSingleton<AgUiProxyService>();

var app = builder.Build();
app.MapDefaultEndpoints();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference(options =>
    {
        options.Title = "ProjectName API";
        options.Theme = ScalarTheme.Mars;
    });
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.MapMethods("/ag-ui", new[] { "POST", "GET", "OPTIONS" }, async (HttpContext context, AgUiProxyService proxy, CancellationToken cancellationToken) =>
{
    await proxy.ProxyAsync(context, cancellationToken);
});
app.MapGrpcService<GreeterService>();

app.MapGet("/", () => Results.Ok(new
{
    service = "ProjectName.Api",
    transport = "HTTP/1.1 + HTTP/2",
    grpcService = "projectname-grpcservice",
    modelPath = "API -> gRPC Service -> MAF/IChatClient -> Ollama"
}));

app.Run();
