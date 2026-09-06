using Grpc.Core;
using ProjectName.GrpcService.Governance;
using ProjectName.GrpcService.Maf;
using ProjectName.GrpcService;

namespace ProjectName.GrpcService.Services;

public sealed class RuntimeChatService(
    MafWorkflowService workflow,
    TrailRuntimeGateway trail,
    ILogger<RuntimeChatService> logger) : RuntimeChat.RuntimeChatBase
{
    private const string Model = "qwen3:8b";

    public override async Task<ChatReply> Chat(
        ChatRequest request,
        ServerCallContext context)
    {
        if (string.IsNullOrWhiteSpace(request.Prompt))
            throw new RpcException(new Status(StatusCode.InvalidArgument, "prompt is required"));

        logger.LogInformation("PMCRO MAF workflow request received for model {Model}", Model);

        try
        {
            var response = await workflow.RunGovernedAsync(request.Prompt, trail, context.CancellationToken);
            return new ChatReply { Model = Model, Response = response.ToString() };
        }
        catch (OperationCanceledException) when (context.CancellationToken.IsCancellationRequested)
        {
            logger.LogInformation("Runtime workflow request was canceled by the caller.");
            throw new RpcException(new Status(StatusCode.Cancelled, "The chat request was canceled by the caller."));
        }
        catch (OperationCanceledException ex)
        {
            logger.LogWarning(ex, "Runtime workflow request timed out or was canceled.");
            throw new RpcException(new Status(StatusCode.DeadlineExceeded, "The workflow request exceeded its deadline."));
        }
    }
}
