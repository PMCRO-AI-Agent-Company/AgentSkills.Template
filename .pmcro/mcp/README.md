# MCP Actuator Architecture

The template exposes actuator capabilities as independent MCP server projects.

## Servers

- `ProjectName.Mcp.Filesystem` — sandboxed workspace file I/O, search, skill discovery, resources, and mission prompt.
- `ProjectName.Mcp.Terminal` — terminal status plus TYPE 1 execution boundaries with HIL-oriented pending/dispatch semantics.
- `ProjectName.Mcp.Playwright` — browser session, navigation, inspection, screenshots, downloads, and serial execution boundaries.

## Boundary

`ProjectName.Api` is the HTTP application edge. `ProjectName.GrpcService` owns MAF workflow execution. MCP servers are actuator boundaries and do not own orchestration or PMCRO governance.

```text
API -> gRPC Runtime -> MAF Workflow -> MCP actuator
                               |-> Filesystem
                               |-> Terminal
                               `-> Playwright
```

All servers use the official C# MCP SDK with Streamable HTTP and stateless transport. Aspire owns local process topology and service discovery.

## Governance

MCP tools are untrusted execution surfaces. Filesystem paths remain sandboxed; terminal TYPE 1 operations remain approval/dispatch boundaries; browser operations remain URL- and session-constrained. MCP implementation does not replace PMCRO evidence, HIL, trail, or deterministic gate logic.

The old `PMCRO-AI-Agent-Company/pmcro-runtime/mcp` implementation is a behavioral reference only; this template intentionally keeps implementation and governance concerns separate.
