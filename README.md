# ProjectName (root solution) + governance seed

## .NET / Aspire (matches your real stack)

| Item | Value |
|------|--------|
| SDK | **11.0.100-preview** (`global.json`) — not net9 |
| TFM | **net11.0** |
| Packages | **Central Package Management** → `Directory.Packages.props` |
| Shared props | `Directory.Build.props` / `Directory.Build.targets` |
| Solution | `ProjectName.slnx` |

```text
ProjectName.AppHost/           Aspire host (Ollama + Runtime + OrchestrationApi)
ProjectName.Runtime/           gRPC agent/model boundary (MAF packages referenced)
ProjectName.OrchestrationApi/  HTTP + gRPC edge, /api/chat
ProjectName.ServiceDefaults/   OTel / service discovery
Directory.*.props|targets      CPM + shared build
global.json
```

Build on a machine with the **.NET 11 preview SDK** (this cloud image may only have 9.x):

```bash
dotnet restore ProjectName.slnx
dotnet build ProjectName.slnx
dotnet run --project ProjectName.AppHost
```

Project names are **ProjectName.*** — not Pmcro-prefixed application projects. Governance stays under `.pmcro/` separately.

## Governance (unchanged)

`.pmcro/`, `plugins/`, `.agents/skills/`, `examples/` — laws, Directory, queue, scaffolder.
