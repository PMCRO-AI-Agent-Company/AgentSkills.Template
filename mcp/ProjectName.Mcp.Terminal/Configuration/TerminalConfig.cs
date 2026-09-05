// src/Mcps/ProjectName.Mcp.Terminal/Configuration/TerminalConfig.cs
// PROJECTNAME — MCP.TERMINAL
// Identity: Terminal Actuator Boundary & Execution Limits
// Law Anchor: EC-002, MAAI-001, SAFETY-003

using System;
using System.IO;

namespace ProjectName.Mcp.Terminal.Configuration;

/// <summary>
/// Defines the boundaries and limits for terminal command execution.
/// TYPE 1 execution is always approval-gated by the Orchestrator.
/// </summary>
public sealed class TerminalConfig
{
    /// <summary>Absolute root under which terminal working directories are confined.</summary>
    public required string WorkingRoot { get; set; }

    /// <summary>Maximum wall-clock time for one command.</summary>
    public int CommandTimeoutSeconds { get; set; } = 30;

    /// <summary>Maximum combined stdout/stderr bytes captured per command.</summary>
    public int MaxOutputBytes { get; set; } = 65536;

    /// <summary>
    /// Resolves a caller-supplied path under WorkingRoot and rejects traversal.
    /// Null or empty resolves to WorkingRoot.
    /// </summary>
    public string ResolveAndValidatePath(string? relativePath)
    {
        var root = Path.GetFullPath(WorkingRoot);
        if (string.IsNullOrWhiteSpace(relativePath)) return root;

        relativePath = relativePath.TrimStart('/', '\\');
        if (string.IsNullOrWhiteSpace(relativePath)) return root;

        var absolute = Path.GetFullPath(Path.Combine(root, relativePath));
        var rootPrefix = root.EndsWith(Path.DirectorySeparatorChar.ToString())
            ? root
            : root + Path.DirectorySeparatorChar;

        if (!absolute.StartsWith(rootPrefix, StringComparison.OrdinalIgnoreCase)
            && !string.Equals(absolute, root, StringComparison.OrdinalIgnoreCase))
        {
            throw new UnauthorizedAccessException(
                $"SAFETY-003 violation: path traversal attempt detected for '{relativePath}'.");
        }

        return absolute;
    }
}
