using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using ProjectName.ServiceDefaults;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace ProjectName.Api.Controllers;

/// <summary>
/// AGENTSKILLS-IDE.md increment 1: a read-only index over this repository's
/// governance/skill/agent surface, so the workspace UI's four previously
/// inert nav buttons (Agents/Skills/MCP/Trails - see
/// ui/projectname-copilotkit/src/app/page.tsx) have real data to render.
///
/// Deliberately read-only. Governed file mutations are a later increment
/// (7) that must go through the existing filesystem MCP boundary, never a
/// direct filesystem write from this HTTP-facing controller - see
/// .pmcro/design/AGENTSKILLS-IDE.md invariants.
///
/// The MCP section below is a static list of registered server projects,
/// not a live tools/list catalog - that is increment 3
/// (AgentSkillsProvider/MCP catalog wiring) and is intentionally not built
/// here. Do not extend this section to imply live discovery without
/// actually wiring McpNativeToolProvider.GetCatalog.
/// </summary>
[ApiController]
[Route("api/workspace")]
public sealed class WorkspaceController(ILogger<WorkspaceController> logger) : ControllerBase
{
    private static readonly IDeserializer YamlDeserializer = new DeserializerBuilder()
        .WithNamingConvention(UnderscoredNamingConvention.Instance)
        .IgnoreUnmatchedProperties()
        .Build();

    [HttpGet("index")]
    [ProducesResponseType(typeof(WorkspaceIndexResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status503ServiceUnavailable)]
    public ActionResult<WorkspaceIndexResponse> GetIndex()
    {
        var repoRoot = RepoPaths.ResolveRepoRoot();
        if (repoRoot is null)
        {
            return StatusCode(StatusCodes.Status503ServiceUnavailable,
                new ApiError($"Could not resolve the repository root. Set the {RepoPaths.RepoRootEnvironmentVariable} environment variable."));
        }

        return Ok(new WorkspaceIndexResponse(
            RepoRoot: repoRoot,
            Agents: ReadAgents(repoRoot),
            Skills: ReadSkills(repoRoot),
            McpServers: ReadMcpServers(repoRoot),
            Governance: ReadGovernance(repoRoot),
            Examples: ReadExamples(repoRoot)));
    }

    private List<WorkspaceAgentSummary> ReadAgents(string repoRoot)
    {
        var result = new List<WorkspaceAgentSummary>();
        var path = Path.Combine(repoRoot, ".pmcro", "directory", "agents.yaml");
        if (!System.IO.File.Exists(path))
            return result;

        try
        {
            var text = System.IO.File.ReadAllText(path);
            var doc = YamlDeserializer.Deserialize<AgentDirectoryYaml>(text);
            foreach (var a in doc.Agents ?? [])
            {
                var packaging = (a.Packaging ?? [])
                    .Select(p => new WorkspacePackagingTarget(p.Target ?? "", p.Path, p.Status))
                    .ToList();
                result.Add(new WorkspaceAgentSummary(
                    Id: a.Id ?? "",
                    Kind: a.Kind ?? "",
                    DisplayName: a.DisplayName ?? a.Id ?? "",
                    Description: a.Description ?? "",
                    OwnerRole: a.OwnerRole ?? "",
                    Status: a.Status ?? "",
                    MarketplaceVisible: a.MarketplaceVisible,
                    SkillCount: a.Skills?.Count ?? 0,
                    Packaging: packaging));
            }
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to parse {Path}", path);
        }

        return result;
    }

    private List<WorkspaceSkillSummary> ReadSkills(string repoRoot)
    {
        var result = new List<WorkspaceSkillSummary>();
        var skillsRoot = Path.Combine(repoRoot, ".agents", "skills");
        if (!Directory.Exists(skillsRoot))
            return result;

        foreach (var dir in Directory.GetDirectories(skillsRoot).OrderBy(d => d, StringComparer.Ordinal))
        {
            var id = Path.GetFileName(dir);
            string? name = null;
            string? description = null;
            try
            {
                var skillMdPath = Path.Combine(dir, "SKILL.md");
                if (System.IO.File.Exists(skillMdPath))
                {
                    var frontmatter = ExtractFrontmatter(System.IO.File.ReadAllText(skillMdPath));
                    if (frontmatter is not null)
                    {
                        var meta = YamlDeserializer.Deserialize<SkillFrontmatterYaml>(frontmatter);
                        name = meta.Name;
                        description = meta.Description;
                    }
                }
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "[WORKSPACE] failed to parse SKILL.md frontmatter under {Dir}", dir);
            }
            result.Add(new WorkspaceSkillSummary(id, name, description));
        }

        return result;
    }

    /// <summary>Extracts the YAML frontmatter block between the first pair of "---" lines, or null if absent.</summary>
    private static string? ExtractFrontmatter(string markdown)
    {
        var lines = markdown.Replace("\r\n", "\n").Split('\n');
        if (lines.Length == 0 || lines[0].Trim() != "---")
            return null;

        var end = Array.FindIndex(lines, 1, l => l.Trim() == "---");
        if (end < 1)
            return null;

        return string.Join('\n', lines[1..end]);
    }

    private List<WorkspaceMcpServerSummary> ReadMcpServers(string repoRoot)
    {
        var result = new List<WorkspaceMcpServerSummary>();
        var mcpRoot = Path.Combine(repoRoot, "mcp");
        if (!Directory.Exists(mcpRoot))
            return result;

        foreach (var dir in Directory.GetDirectories(mcpRoot, "ProjectName.Mcp.*").OrderBy(d => d, StringComparer.Ordinal))
        {
            result.Add(new WorkspaceMcpServerSummary(
                Name: Path.GetFileName(dir),
                Description: "Registered MCP server (static listing only - live tool/resource/prompt discovery is AGENTSKILLS-IDE.md increment 3, not yet built)."));
        }

        return result;
    }

    private List<string> ReadExamples(string repoRoot)
    {
        var examplesRoot = Path.Combine(repoRoot, "examples");
        if (!Directory.Exists(examplesRoot))
            return [];

        try
        {
            return Directory.GetFileSystemEntries(examplesRoot)
                .Select(Path.GetFileName)
                .Where(n => n is not null)
                .Select(n => n!)
                .OrderBy(n => n, StringComparer.Ordinal)
                .ToList();
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to list {Path}", examplesRoot);
            return [];
        }
    }

    private WorkspaceGovernanceSummary ReadGovernance(string repoRoot)
    {
        var trails = ReadTrails(Path.Combine(repoRoot, ".pmcro", "trails"));
        var pendingQueue = ReadPendingQueue(Path.Combine(repoRoot, ".pmcro", "queue"));

        return new WorkspaceGovernanceSummary(
            TrailsSealedCount: trails.Count(t => t.Status == "sealed"),
            TrailsOpenCount: trails.Count(t => t.Status == "open"),
            TrailsAbandonedCount: trails.Count(t => t.Status == "abandoned"),
            TrailsOtherCount: trails.Count(t => t.Status is not ("sealed" or "open" or "abandoned")),
            RecentTrails: trails.Take(15).ToList(),
            PendingQueue: pendingQueue);
    }

    private List<WorkspaceTrailSummary> ReadTrails(string trailsRoot)
    {
        if (!Directory.Exists(trailsRoot))
            return [];

        var trails = new List<(WorkspaceTrailSummary Summary, DateTime SortKey)>();
        foreach (var dir in Directory.GetDirectories(trailsRoot))
        {
            var trailJsonPath = Path.Combine(dir, "trail.json");
            var dirInfo = new DirectoryInfo(dir);
            if (!System.IO.File.Exists(trailJsonPath))
            {
                trails.Add((new WorkspaceTrailSummary(dirInfo.Name, "unknown-no-trail-json", null, null, null), dirInfo.LastWriteTimeUtc));
                continue;
            }

            try
            {
                using var doc = JsonDocument.Parse(System.IO.File.ReadAllText(trailJsonPath));
                var root = doc.RootElement;
                var summary = new WorkspaceTrailSummary(
                    Id: GetStringOrDefault(root, "trail_id") ?? dirInfo.Name,
                    Status: GetStringOrDefault(root, "status") ?? "unknown",
                    OpenedAt: GetStringOrDefault(root, "opened_at"),
                    SealedAt: GetStringOrDefault(root, "sealed_at") ?? GetStringOrDefault(root, "abandoned_at"),
                    SeedIntent: Truncate(GetStringOrDefault(root, "seed_intent") ?? GetStringOrDefault(root, "abandoned_reason"), 240));
                trails.Add((summary, dirInfo.LastWriteTimeUtc));
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "[WORKSPACE] failed to parse {Path}", trailJsonPath);
                trails.Add((new WorkspaceTrailSummary(dirInfo.Name, "unparseable", null, null, null), dirInfo.LastWriteTimeUtc));
            }
        }

        return trails.OrderByDescending(t => t.SortKey).Select(t => t.Summary).ToList();
    }

    private List<WorkspaceQueueItemSummary> ReadPendingQueue(string queueRoot)
    {
        var result = new List<WorkspaceQueueItemSummary>();
        if (!Directory.Exists(queueRoot))
            return result;

        // Top-level *.json only - "done/" holds resolved seeds and is
        // deliberately excluded from "pending".
        foreach (var file in Directory.GetFiles(queueRoot, "*.json").OrderBy(f => f, StringComparer.Ordinal))
        {
            try
            {
                using var doc = JsonDocument.Parse(System.IO.File.ReadAllText(file));
                var root = doc.RootElement;
                var id = root.TryGetProperty("metadata", out var metadata) ? GetStringOrDefault(metadata, "id") : null;
                int? priority = metadata.ValueKind == JsonValueKind.Object && metadata.TryGetProperty("priority", out var p) && p.ValueKind == JsonValueKind.Number
                    ? p.GetInt32()
                    : null;
                var intent = root.TryGetProperty("spec", out var spec) ? Truncate(GetStringOrDefault(spec, "intent"), 240) : null;
                result.Add(new WorkspaceQueueItemSummary(id ?? Path.GetFileNameWithoutExtension(file), priority, intent));
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "[WORKSPACE] failed to parse queue seed {Path}", file);
            }
        }

        return result.OrderBy(q => q.Priority ?? int.MaxValue).ToList();
    }

    private static string? GetStringOrDefault(JsonElement element, string property) =>
        element.ValueKind == JsonValueKind.Object && element.TryGetProperty(property, out var value) && value.ValueKind == JsonValueKind.String
            ? value.GetString()
            : null;

    private static string? Truncate(string? text, int maxLength) =>
        string.IsNullOrEmpty(text) || text.Length <= maxLength ? text : text[..maxLength] + "...";
}

public sealed record WorkspaceIndexResponse(
    string RepoRoot,
    IReadOnlyList<WorkspaceAgentSummary> Agents,
    IReadOnlyList<WorkspaceSkillSummary> Skills,
    IReadOnlyList<WorkspaceMcpServerSummary> McpServers,
    WorkspaceGovernanceSummary Governance,
    IReadOnlyList<string> Examples);

public sealed record WorkspaceAgentSummary(
    string Id,
    string Kind,
    string DisplayName,
    string Description,
    string OwnerRole,
    string Status,
    bool MarketplaceVisible,
    int SkillCount,
    IReadOnlyList<WorkspacePackagingTarget> Packaging);

public sealed record WorkspacePackagingTarget(string Target, string? Path, string? Status);

public sealed record WorkspaceSkillSummary(string Id, string? Name, string? Description);

public sealed record WorkspaceMcpServerSummary(string Name, string Description);

public sealed record WorkspaceTrailSummary(string Id, string Status, string? OpenedAt, string? SealedAt, string? SeedIntent);

public sealed record WorkspaceQueueItemSummary(string Id, int? Priority, string? Intent);

public sealed record WorkspaceGovernanceSummary(
    int TrailsSealedCount,
    int TrailsOpenCount,
    int TrailsAbandonedCount,
    int TrailsOtherCount,
    IReadOnlyList<WorkspaceTrailSummary> RecentTrails,
    IReadOnlyList<WorkspaceQueueItemSummary> PendingQueue);

/// <summary>Mirrors the top-level shape of .pmcro/directory/agents.yaml. Unmatched YAML fields are ignored (IgnoreUnmatchedProperties).</summary>
internal sealed class AgentDirectoryYaml
{
    public List<AgentYaml>? Agents { get; set; }
}

internal sealed class AgentYaml
{
    public string? Id { get; set; }
    public string? Kind { get; set; }
    public string? DisplayName { get; set; }
    public string? Description { get; set; }
    public string? OwnerRole { get; set; }
    public string? Status { get; set; }
    public bool MarketplaceVisible { get; set; }
    public List<object>? Skills { get; set; }
    public List<PackagingYaml>? Packaging { get; set; }
}

internal sealed class PackagingYaml
{
    public string? Target { get; set; }
    public string? Path { get; set; }
    public string? Status { get; set; }
}

/// <summary>Mirrors just the fields this endpoint displays from a SKILL.md's YAML frontmatter.</summary>
internal sealed class SkillFrontmatterYaml
{
    public string? Name { get; set; }
    public string? Description { get; set; }
}
