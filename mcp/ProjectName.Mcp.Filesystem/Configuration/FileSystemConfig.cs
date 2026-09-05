// PROJECTNAME — MCP.FILESYSTEM
// Identity: Sandbox Enforcer & Path Resolver
// Law Anchor: FS-LAW-001

using System;
using System.IO;
using Microsoft.Extensions.Configuration;

namespace ProjectName.Mcp.Filesystem.Configuration;

/// <summary>Defines the filesystem sandbox and file-size boundary.</summary>
public sealed class FilesystemConfig
{
    public string SandboxRoot { get; }
    public int MaxFileSizeBytes { get; }

    public FilesystemConfig(IConfiguration config)
    {
        var configuredPath = config["Filesystem:SandboxRoot"]
            ?? Path.Combine(Directory.GetCurrentDirectory(), "Workspace");
        SandboxRoot = Path.GetFullPath(configuredPath);
        if (!Directory.Exists(SandboxRoot)) Directory.CreateDirectory(SandboxRoot);

        MaxFileSizeBytes = int.TryParse(config["Filesystem:MaxFileSizeBytes"], out var size)
            ? size
            : 10 * 1024 * 1024;
        if (MaxFileSizeBytes <= 0)
            throw new InvalidOperationException("Filesystem:MaxFileSizeBytes must be greater than zero.");
    }

    /// <summary>Resolves a relative path and rejects traversal outside the sandbox.</summary>
    public string ResolveAndValidatePath(string relativePath)
    {
        if (string.IsNullOrWhiteSpace(relativePath)) return SandboxRoot;
        relativePath = relativePath.TrimStart('/', '\\');
        if (string.IsNullOrWhiteSpace(relativePath)) return SandboxRoot;

        var absolutePath = Path.GetFullPath(Path.Combine(SandboxRoot, relativePath));
        var prefix = SandboxRoot.EndsWith(Path.DirectorySeparatorChar.ToString())
            ? SandboxRoot
            : SandboxRoot + Path.DirectorySeparatorChar;
        var candidate = absolutePath.EndsWith(Path.DirectorySeparatorChar.ToString())
            ? absolutePath
            : absolutePath + Path.DirectorySeparatorChar;

        if (!candidate.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            throw new UnauthorizedAccessException("FS-LAW-001: path resolves outside the sandbox.");
        return absolutePath;
    }
}
