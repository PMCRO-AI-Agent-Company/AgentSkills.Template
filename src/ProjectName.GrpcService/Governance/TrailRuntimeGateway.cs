using System.Diagnostics;
using System.Text.Json;

namespace ProjectName.GrpcService.Governance;

/// <summary>
/// Shells out to this repo's existing <c>.pmcro/runtime/trail_runtime.py</c> CLI so the
/// MAF chat workflow can write real, gated PMCR-O trail evidence instead of running
/// entirely disconnected from <c>.pmcro/</c> (see
/// <c>.pmcro/design/AUDIT-claude-architecture-review-2026-09-06.md</c>, finding 15 -
/// "the governed evidence loop and the thing that actually serves requests are two
/// separate systems that happen to share vocabulary").
///
/// Deliberately reuses the existing, already self-tested Python gates
/// (Checker verdict must be PASS/FAIL; Reflector cannot SEAL without a PASS -
/// see trail_runtime.py's <c>cmd_check</c>/<c>cmd_reflect</c>) rather than
/// re-implementing the same two gates a second time in C#. A second
/// implementation of the same rule, in a second language, is exactly the kind
/// of duplication that produced most of the drift the audit above found.
///
/// Known, undischarged dependency: this requires <c>python3</c> on PATH in
/// whatever environment ProjectName.GrpcService actually runs in. If it is
/// not present (e.g. a slim container image), every call here fails and is
/// logged as a warning - by design this NEVER blocks or fails the underlying
/// chat response (see MafWorkflowService.RunGovernedAsync), it only means no
/// trail evidence gets written for that turn.
///
/// Coverage: both entry points now reach this gateway. RunGovernedAsync
/// covers the gRPC RuntimeChatService and the debug `GET /chat` endpoint.
/// The AG-UI protocol server (Microsoft.Agents.AI.Hosting.AGUI.AspNetCore,
/// mapped in Program.cs as `/ag-ui` and used by the CopilotKit UI via
/// AgUiProxyService) previously drove the workflow agent through its own
/// internal request handling with no path back to this gateway. That gap is
/// closed via MafWorkflowService.CreateGovernedAgent, which wraps the same
/// underlying agent with Microsoft Agent Framework's own documented
/// agent-middleware mechanism (AIAgent.AsBuilder().Use(...)) rather than a
/// guessed-at custom adapter - see that method's remarks for exactly how and
/// why. Evidence recording still never affects the response in either path;
/// only whether a trail gets written and whether it may later be sealed.
/// </summary>
public sealed class TrailRuntimeGateway
{
    private readonly string? _scriptPath;
    private readonly ILogger<TrailRuntimeGateway> _logger;

    public TrailRuntimeGateway(ILogger<TrailRuntimeGateway> logger)
    {
        _logger = logger;
        _scriptPath = ResolveScriptPath();
        if (_scriptPath is null)
            _logger.LogWarning("[TRAIL] .pmcro/runtime/trail_runtime.py not found by walking up from {BaseDir}; governed trail evidence will not be recorded until PMCRO_ROOT is set or the file is locatable.", AppContext.BaseDirectory);
    }

    /// <summary>True when trail_runtime.py was located and evidence recording can be attempted.</summary>
    public bool IsAvailable => _scriptPath is not null;

    private static string? ResolveScriptPath()
    {
        var configured = Environment.GetEnvironmentVariable("PMCRO_ROOT");
        if (!string.IsNullOrWhiteSpace(configured))
        {
            var candidate = Path.Combine(configured, "runtime", "trail_runtime.py");
            if (File.Exists(candidate))
                return Path.GetFullPath(candidate);
        }

        // Same walk-up-from-executable strategy MafWorkflowService.ResolveSkillsRoot()
        // already uses for .agents/skills, applied to .pmcro instead.
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null)
        {
            var candidate = Path.Combine(current.FullName, ".pmcro", "runtime", "trail_runtime.py");
            if (File.Exists(candidate))
                return candidate;
            current = current.Parent;
        }

        return null;
    }

    private async Task<(int ExitCode, string Stdout, string Stderr)> InvokeAsync(string[] args, string? stdinJson, CancellationToken ct)
    {
        if (_scriptPath is null)
            return (2, "", "trail_runtime.py path not resolved");

        var psi = new ProcessStartInfo
        {
            FileName = "python3",
            WorkingDirectory = Path.GetDirectoryName(_scriptPath),
            RedirectStandardInput = stdinJson is not null,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        };
        psi.ArgumentList.Add(_scriptPath);
        foreach (var a in args)
            psi.ArgumentList.Add(a);

        using var process = new Process { StartInfo = psi };
        try
        {
            process.Start();
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "[TRAIL] failed to start python3 for trail_runtime.py {Args} - is python3 on PATH in this environment?", string.Join(' ', args));
            return (2, "", ex.Message);
        }

        if (stdinJson is not null)
        {
            await process.StandardInput.WriteAsync(stdinJson);
            process.StandardInput.Close();
        }

        var stdoutTask = process.StandardOutput.ReadToEndAsync(ct);
        var stderrTask = process.StandardError.ReadToEndAsync(ct);
        await process.WaitForExitAsync(ct);
        return (process.ExitCode, await stdoutTask, await stderrTask);
    }

    /// <summary>Opens a new trail. Returns the trail_id, or null if opening failed (logged, never throws).</summary>
    public async Task<string?> OpenAsync(string seed, string host, CancellationToken ct)
    {
        var (exit, stdout, stderr) = await InvokeAsync(["open", "--seed", seed, "--host", host], null, ct);
        if (exit != 0)
        {
            _logger.LogWarning("[TRAIL] open failed (exit {Exit}): {Stderr}", exit, stderr);
            return null;
        }
        try
        {
            using var doc = JsonDocument.Parse(stdout);
            return doc.RootElement.GetProperty("trail_id").GetString();
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "[TRAIL] could not parse open response: {Stdout}", stdout);
            return null;
        }
    }

    public Task<bool> PlanAsync(string trailId, object frame, CancellationToken ct) => WritePhaseAsync("plan", trailId, frame, ct);

    public Task<bool> MakeAsync(string trailId, object frame, CancellationToken ct) => WritePhaseAsync("make", trailId, frame, ct);

    /// <summary>Records the Checker's verdict. Returns (Ok, Verdict) - Ok is false if trail_runtime.py rejected the frame (e.g. verdict wasn't PASS/FAIL).</summary>
    public async Task<(bool Ok, string? Verdict)> CheckAsync(string trailId, object frame, CancellationToken ct)
    {
        var json = JsonSerializer.Serialize(frame);
        var (exit, stdout, stderr) = await InvokeAsync(["check", "--trail", trailId], json, ct);
        if (exit != 0)
        {
            _logger.LogWarning("[TRAIL] check rejected (exit {Exit}): {Stderr}", exit, stderr);
            return (false, null);
        }
        try
        {
            using var doc = JsonDocument.Parse(stdout);
            return (true, doc.RootElement.GetProperty("verdict").GetString());
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "[TRAIL] could not parse check response: {Stdout}", stdout);
            return (false, null);
        }
    }

    /// <summary>Records the Reflector's disposition. Returns true only if the trail actually sealed (false on RETRY/BLOCKED, or if trail_runtime.py refused a SEAL without a PASS - L-CHECKER-GATE).</summary>
    public async Task<bool> ReflectAsync(string trailId, object frame, CancellationToken ct)
    {
        var json = JsonSerializer.Serialize(frame);
        var (exit, stdout, stderr) = await InvokeAsync(["reflect", "--trail", trailId], json, ct);
        if (exit != 0)
        {
            _logger.LogWarning("[TRAIL] reflect rejected (exit {Exit}): {Stderr}", exit, stderr);
            return false;
        }
        try
        {
            using var doc = JsonDocument.Parse(stdout);
            return doc.RootElement.TryGetProperty("status", out var status) && status.GetString() == "sealed";
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "[TRAIL] could not parse reflect response: {Stdout}", stdout);
            return false;
        }
    }

    private async Task<bool> WritePhaseAsync(string verb, string trailId, object frame, CancellationToken ct)
    {
        var json = JsonSerializer.Serialize(frame);
        var (exit, _, stderr) = await InvokeAsync([verb, "--trail", trailId], json, ct);
        if (exit != 0)
        {
            _logger.LogWarning("[TRAIL] {Verb} rejected (exit {Exit}): {Stderr}", verb, exit, stderr);
            return false;
        }
        return true;
    }
}
