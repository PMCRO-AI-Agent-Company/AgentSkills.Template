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

    /// <summary>
    /// AGENTSKILLS-IDE.md increment 2: full detail for one skill (SKILL.md
    /// content, AGENTS.md if present, and a listing of every other file in
    /// its directory - assets/references/scripts/whatever a given skill
    /// actually uses, discovered generically). <paramref name="id"/> is the
    /// same posix-style relative id ReadSkills produces (e.g.
    /// "reasoning/chain-of-thought"), url-decoded by the framework's
    /// catch-all route parameter.
    /// </summary>
    [HttpGet("skills/{*id}")]
    [ProducesResponseType(typeof(WorkspaceSkillDetail), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status503ServiceUnavailable)]
    public ActionResult<WorkspaceSkillDetail> GetSkillDetail(string id)
    {
        var repoRoot = RepoPaths.ResolveRepoRoot();
        if (repoRoot is null)
        {
            return StatusCode(StatusCodes.Status503ServiceUnavailable,
                new ApiError($"Could not resolve the repository root. Set the {RepoPaths.RepoRootEnvironmentVariable} environment variable."));
        }

        var skillsRoot = Path.Combine(repoRoot, ".agents", "skills");
        var skillDir = ResolveSkillDirectory(skillsRoot, id);
        if (skillDir is null)
            return NotFound(new ApiError($"No skill '{id}' with a SKILL.md was found."));

        var detail = ReadSkillDetail(skillDir, id);
        return Ok(detail);
    }

    /// <summary>
    /// AGENTSKILLS-IDE.md increment 4 (partial): full phase-file detail for
    /// one trail. There is no fixed C# schema for a phase's content - each
    /// role's frame shape varies by what that cycle actually needed (see
    /// trail_runtime.py's own frames, which are opaque JSON as far as the
    /// runtime is concerned) - so phases are returned as raw parsed JSON,
    /// not bound to strongly-typed records. A trail that hasn't reached a
    /// later phase yet (e.g. open, only orchestrate+plan written) returns
    /// null for the phases that don't exist rather than erroring.
    /// </summary>
    [HttpGet("trails/{id}")]
    [ProducesResponseType(typeof(WorkspaceTrailDetail), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ApiError), StatusCodes.Status503ServiceUnavailable)]
    public ActionResult<WorkspaceTrailDetail> GetTrailDetail(string id)
    {
        var repoRoot = RepoPaths.ResolveRepoRoot();
        if (repoRoot is null)
        {
            return StatusCode(StatusCodes.Status503ServiceUnavailable,
                new ApiError($"Could not resolve the repository root. Set the {RepoPaths.RepoRootEnvironmentVariable} environment variable."));
        }

        var trailsRoot = Path.Combine(repoRoot, ".pmcro", "trails");
        var trailDir = ResolveTrailDirectory(trailsRoot, id);
        if (trailDir is null)
            return NotFound(new ApiError($"No trail '{id}' was found."));

        return Ok(ReadTrailDetail(trailDir, id));
    }

    /// <summary>Same path-traversal posture as ResolveSkillDirectory: refuses anything that would resolve outside trailsRoot.</summary>
    private static string? ResolveTrailDirectory(string trailsRoot, string id)
    {
        if (string.IsNullOrWhiteSpace(id))
            return null;

        var normalizedRoot = Path.GetFullPath(trailsRoot);
        var candidate = Path.GetFullPath(Path.Combine(normalizedRoot, id));
        if (!candidate.StartsWith(normalizedRoot + Path.DirectorySeparatorChar, StringComparison.Ordinal))
            return null;

        return Directory.Exists(candidate) ? candidate : null;
    }

    private WorkspaceTrailDetail ReadTrailDetail(string trailDir, string id)
    {
        object? trailMeta = ReadJsonObjectOrNull(Path.Combine(trailDir, "trail.json"), id);
        var orchestrate = ReadJsonLinesOrNull(Path.Combine(trailDir, "01-orchestrate.jsonl"), id);
        var plan = ReadJsonObjectOrNull(Path.Combine(trailDir, "02-plan.json"), id);
        var make = ReadJsonLinesOrNull(Path.Combine(trailDir, "03-make.jsonl"), id);
        var check = ReadJsonObjectOrNull(Path.Combine(trailDir, "04-check.json"), id);
        var reflect = ReadJsonObjectOrNull(Path.Combine(trailDir, "05-reflect.json"), id);

        return new WorkspaceTrailDetail(id, trailMeta, orchestrate, plan, make, check, reflect);
    }

    private object? ReadJsonObjectOrNull(string path, string trailId)
    {
        if (!System.IO.File.Exists(path))
            return null;
        try
        {
            return JsonSerializer.Deserialize<JsonElement>(System.IO.File.ReadAllText(path));
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to parse {Path} for trail detail {TrailId}", path, trailId);
            return null;
        }
    }

    private List<object>? ReadJsonLinesOrNull(string path, string trailId)
    {
        if (!System.IO.File.Exists(path))
            return null;
        var frames = new List<object>();
        try
        {
            foreach (var line in System.IO.File.ReadAllLines(path))
            {
                if (string.IsNullOrWhiteSpace(line))
                    continue;
                frames.Add(JsonSerializer.Deserialize<JsonElement>(line));
            }
            return frames;
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to parse {Path} for trail detail {TrailId}", path, trailId);
            return frames.Count > 0 ? frames : null;
        }
    }

    /// <summary>
    /// Resolves a caller-supplied skill id to a real directory under
    /// <paramref name="skillsRoot"/> that contains a SKILL.md, refusing
    /// anything that would resolve outside of it (no "../" traversal,
    /// however encoded). See also <see cref="ResolveTrailDirectory"/> for
    /// the equivalent check on trail ids.
    /// </summary>
    private static string? ResolveSkillDirectory(string skillsRoot, string id)
    {
        if (string.IsNullOrWhiteSpace(id))
            return null;

        var normalizedRoot = Path.GetFullPath(skillsRoot);
        var candidate = Path.GetFullPath(Path.Combine(normalizedRoot, id));
        if (!candidate.StartsWith(normalizedRoot + Path.DirectorySeparatorChar, StringComparison.Ordinal))
            return null;

        return System.IO.File.Exists(Path.Combine(candidate, "SKILL.md")) ? candidate : null;
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

        // Skills can nest (e.g. .agents/skills/reasoning/chain-of-thought/SKILL.md
        // is a real, separate skill, not a subfolder of a "reasoning" skill) - walk
        // every directory under the root, bounded to a sane depth, and treat any
        // directory that directly contains a SKILL.md as one skill. This previously
        // only checked the immediate children of skillsRoot, which made the entire
        // 35-strategy reasoning/ catalog invisible and surfaced "reasoning" itself
        // as a bogus nameless/descriptionless skill.
        foreach (var skillDir in FindSkillDirectories(skillsRoot, maxDepth: 4))
        {
            var id = ToSkillId(skillsRoot, skillDir);
            string? name = null;
            string? description = null;
            try
            {
                var frontmatter = ExtractFrontmatter(System.IO.File.ReadAllText(Path.Combine(skillDir, "SKILL.md")));
                if (frontmatter is not null)
                {
                    var meta = YamlDeserializer.Deserialize<SkillFrontmatterYaml>(frontmatter);
                    name = meta.Name;
                    description = meta.Description;
                }
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "[WORKSPACE] failed to parse SKILL.md frontmatter under {Dir}", skillDir);
            }
            result.Add(new WorkspaceSkillSummary(id, name, description));
        }

        result.Sort((a, b) => string.CompareOrdinal(a.Id, b.Id));
        return result;
    }

    /// <summary>Yields every directory under <paramref name="root"/> (root itself included) that directly contains a SKILL.md, walking at most <paramref name="maxDepth"/> levels deep.</summary>
    private static IEnumerable<string> FindSkillDirectories(string root, int maxDepth)
    {
        if (System.IO.File.Exists(Path.Combine(root, "SKILL.md")))
            yield return root;

        if (maxDepth <= 0)
            yield break;

        IEnumerable<string> children;
        try
        {
            children = Directory.GetDirectories(root);
        }
        catch (Exception)
        {
            yield break;
        }

        foreach (var child in children.OrderBy(c => c, StringComparer.Ordinal))
            foreach (var found in FindSkillDirectories(child, maxDepth - 1))
                yield return found;
    }

    /// <summary>Converts an absolute skill directory path to a stable, posix-style id relative to the skills root (e.g. "reasoning/chain-of-thought").</summary>
    private static string ToSkillId(string skillsRoot, string skillDir) =>
        Path.GetRelativePath(skillsRoot, skillDir).Replace(Path.DirectorySeparatorChar, '/').Replace('\\', '/');

    private const int MaxSkillDetailFiles = 300;

    private WorkspaceSkillDetail ReadSkillDetail(string skillDir, string id)
    {
        string? name = null;
        string? description = null;
        var content = "";
        try
        {
            content = System.IO.File.ReadAllText(Path.Combine(skillDir, "SKILL.md"));
            var frontmatter = ExtractFrontmatter(content);
            if (frontmatter is not null)
            {
                var meta = YamlDeserializer.Deserialize<SkillFrontmatterYaml>(frontmatter);
                name = meta.Name;
                description = meta.Description;
            }
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to read SKILL.md for skill detail {Id}", id);
        }

        string? agentsMd = null;
        var agentsMdPath = Path.Combine(skillDir, "AGENTS.md");
        if (System.IO.File.Exists(agentsMdPath))
        {
            try { agentsMd = System.IO.File.ReadAllText(agentsMdPath); }
            catch (Exception ex) { logger.LogWarning(ex, "[WORKSPACE] failed to read AGENTS.md for skill detail {Id}", id); }
        }

        var files = new List<string>();
        try
        {
            foreach (var file in Directory.EnumerateFiles(skillDir, "*", SearchOption.AllDirectories)
                         .OrderBy(f => f, StringComparer.Ordinal))
            {
                var relative = Path.GetRelativePath(skillDir, file).Replace(Path.DirectorySeparatorChar, '/').Replace('\\', '/');
                if (relative is "SKILL.md" or "AGENTS.md")
                    continue;
                files.Add(relative);
                if (files.Count >= MaxSkillDetailFiles)
                    break;
            }
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "[WORKSPACE] failed to list files for skill detail {Id}", id);
        }

        return new WorkspaceSkillDetail(id, name, description, content, agentsMd, files);
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

public sealed record WorkspaceSkillDetail(
    string Id,
    string? Name,
    string? Description,
    string Content,
    string? AgentsMd,
    IReadOnlyList<string> Files);

public sealed record WorkspaceMcpServerSummary(string Name, string Description);

public sealed record WorkspaceTrailSummary(string Id, string Status, string? OpenedAt, string? SealedAt, string? SeedIntent);

/// <summary>
/// Full phase content for one trail. Each phase is raw parsed JSON (object
/// or, for the two .jsonl phases, an array of objects) rather than a typed
/// record - this repo's trail_runtime.py treats phase content as opaque,
/// role-authored JSON with no fixed schema, and this endpoint preserves
/// that rather than inventing a schema that would drift from reality.
/// Any phase not yet written for an in-progress trail is null.
/// </summary>
public sealed record WorkspaceTrailDetail(
    string Id,
    object? TrailMeta,
    List<object>? Orchestrate,
    object? Plan,
    List<object>? Make,
    object? Check,
    object? Reflect);

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
