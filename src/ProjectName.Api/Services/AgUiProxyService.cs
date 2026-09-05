namespace ProjectName.Api.Services;

public sealed class AgUiProxyService(IHttpClientFactory httpClientFactory)
{
    public async Task ProxyAsync(HttpContext context, CancellationToken cancellationToken)
    {
        using var request = new HttpRequestMessage(new HttpMethod(context.Request.Method), "/ag-ui");
        request.Content = new StreamContent(context.Request.Body);

        if (!string.IsNullOrWhiteSpace(context.Request.ContentType))
            request.Content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");

        foreach (var header in context.Request.Headers)
        {
            if (string.Equals(header.Key, "Content-Type", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(header.Key, "Content-Length", StringComparison.OrdinalIgnoreCase))
                continue;

            if (!request.Headers.TryAddWithoutValidation(header.Key, header.Value.ToArray()))
                request.Content.Headers.TryAddWithoutValidation(header.Key, header.Value.ToArray());
        }

        using var response = await httpClientFactory.CreateClient("runtime-agui")
            .SendAsync(request, HttpCompletionOption.ResponseHeadersRead, cancellationToken);

        context.Response.StatusCode = (int)response.StatusCode;
        foreach (var header in response.Headers)
            context.Response.Headers[header.Key] = header.Value.ToArray();
        foreach (var header in response.Content.Headers)
            context.Response.Headers[header.Key] = header.Value.ToArray();

        context.Response.Headers.Remove("transfer-encoding");
        await response.Content.CopyToAsync(context.Response.Body, cancellationToken);
    }
}
