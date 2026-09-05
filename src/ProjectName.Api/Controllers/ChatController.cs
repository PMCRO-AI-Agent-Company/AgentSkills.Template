using Grpc.Core;
using Microsoft.AspNetCore.Mvc;
using ProjectName.Api.Services;

namespace ProjectName.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class ChatController(RuntimeGatewayService runtime) : ControllerBase
{
    [HttpPost]
    [ProducesResponseType(typeof(ChatResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status502BadGateway)]
    public async Task<ActionResult<ChatResponse>> Post(
        [FromBody] ChatRequest request,
        CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Prompt))
            return BadRequest(new ApiError("prompt is required"));

        try
        {
            var response = await runtime.ChatAsync(request.Prompt, cancellationToken);
            return Ok(new ChatResponse(response.Model, response.Response));
        }
        catch (RpcException ex)
        {
            return StatusCode(ex.StatusCode switch
            {
                Grpc.Core.StatusCode.InvalidArgument => StatusCodes.Status400BadRequest,
                Grpc.Core.StatusCode.Unavailable => StatusCodes.Status503ServiceUnavailable,
                _ => StatusCodes.Status502BadGateway
            }, new ApiError(ex.Status.Detail));
        }
    }

    [HttpGet]
    [ProducesResponseType(typeof(ChatResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status502BadGateway)]
    public async Task<ActionResult<ChatResponse>> Get(
        [FromQuery] string prompt,
        CancellationToken cancellationToken)
    {
        return await Post(new ChatRequest(prompt), cancellationToken);
    }
}

public sealed record ChatRequest(string Prompt);

public sealed record ChatResponse(string Model, string Response);

public sealed record ApiError(string Error);
