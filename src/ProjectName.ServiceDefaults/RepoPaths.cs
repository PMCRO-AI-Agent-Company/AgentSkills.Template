namespace ProjectName.ServiceDefaults;

/// <summary>
/// Locates the repository root shared by every project in this solution.
///
/// Deliberately reuses the same "explicit env var override, else walk up
/// from the executable looking for known marker directories" strategy that
/// already exists twice in this repo (MafWorkflowService.ResolveSkillsRoot
/// for .agents/skills, TrailRuntimeGateway.ResolveScriptPath for
/// .pmcro/runtime) rather than adding a third, slightly different
/// implementation - see
/// .pmcro/design/AUDIT-claude-architecture-review-2026-09-06.md for how
/// much drift this repo has already accumulated from near-duplicate logic
/// that quietly diverges.
///
/// The AppHost already computes this exact value once (see
/// ProjectName.AppHost/AppHost.cs's `repoRoot` parameter, passed to the MCP
/// servers as Filesystem__SandboxRoot / Terminal__WorkingRoot) - callers
/// running under Aspire should be given it the same way, via the
/// <c>Workspace__RepoRoot</c> environment variable, rather than relying on
/// the walk-up fallback below (which only works when the process's
/// executable actually lives under the source tree, not in a published
/// container image).
/// </summary>
public static class RepoPaths
{
    public const string RepoRootEnvironmentVariable = "Workspace__RepoRoot";

    /// <summary>
    /// Returns the repository root, or null if it could not be located.
    /// Never throws - callers decide how to respond to an unresolved root
    /// (e.g. a 503 from an API endpoint), consistent with
    /// TrailRuntimeGateway's "never block the caller" contract.
    /// </summary>
    public static string? ResolveRepoRoot()
    {
        var configured = Environment.GetEnvironmentVariable(RepoRootEnvironmentVariable);
        if (!string.IsNullOrWhiteSpace(configured) && Directory.Exists(configured))
            return Path.GetFullPath(configured);

        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null)
        {
            if (Directory.Exists(Path.Combine(current.FullName, ".pmcro")) &&
                Directory.Exists(Path.Combine(current.FullName, ".agents")))
            {
                return current.FullName;
            }
            current = current.Parent;
        }

        return null;
    }
}
