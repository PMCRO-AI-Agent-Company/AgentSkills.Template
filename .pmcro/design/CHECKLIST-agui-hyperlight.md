# Maker checklist — AG-UI endpoint + Hyperlight flag

Apply on the **real** `pmcr-o` repo. Do not run as a substitute for lifecycle plugins in the cloud seed.

## 1. Capability flag (default OFF)

- [ ] Copy or merge `.pmcro/capabilities/hyperlight-codeact.yaml` into repo `.pmcro/capabilities/`
- [ ] Appsettings (OrchestrationApi and/or Runtime):

```json
"Hyperlight": {
  "CodeAct": {
    "Enabled": false
  }
}
```

- [ ] Read flag at startup; if false, skip any `HyperlightCodeActProvider` / `execute_code` registration
- [ ] Log: `Hyperlight CodeAct capability disabled (default)`

## 2. AppHost alignment (comments only if code already correct)

File: `ProjectName.AppHost/AppHost.cs`

- [ ] Keep `repoRoot` parameter (no drive letters)
- [ ] Add short comment referencing ADR-pmcro-enterprise-hybrid-stack:
  - Runtime = MAF/agent boundary
  - OrchestrationApi = HTTP/gRPC edge (REST + future AG-UI)
  - CodeAct/Hyperlight = capability-gated, not always-on
- [ ] Do not add Hyperlight container unless flag design requires it later

## 3. One AG-UI endpoint (OrchestrationApi)

File: `ProjectName.OrchestrationApi/Program.cs`

Target pattern (adjust to installed MAF AG-UI package version on the machine):

```csharp
// AG-UI surface for CopilotKit — single endpoint; requires MAF Hosting.AGUI package when wired.
// app.MapAGUI("/ag-ui", agent);  // when Microsoft.Agents.AI.Hosting.AGUI.AspNetCore is referenced
```

Minimal interim (if package not yet referenced):

```csharp
app.MapGet("/ag-ui/health", () => Results.Ok(new {
    protocol = "ag-ui",
    status = "reserved",
    note = "Wire MapAGUI when MAF AG-UI hosting package is restored; CopilotKit points runtimeUrl here."
}));
```

- [ ] Preserve existing `/api/chat` and gRPC greeter
- [ ] Document CopilotKit `runtimeUrl` → this service’s public AG-UI base URL
- [ ] Dev: visible in OpenAPI/Scalar if using MapGet interim

**Package (when enabling for real):**  
`Microsoft.Agents.AI.Hosting.AGUI.AspNetCore` (version per current CopilotKit MAF quickstart — verify on NuGet at implement time).

## 4. CopilotKit (follow-up; not this cycle’s must)

- [ ] Next app with `@copilotkit/react-core` + runtime route proxying to OrchestrationApi AG-UI
- [ ] HITL approvals aligned with `.pmcro/policies` mutation approval

## 5. Parallel marketplace

- [ ] `git status` / path filter: **no** changes under any parallel `plugins/pmcro-marketplace/` tree owned by another session
- [ ] Scaffolder work stays `pmcro-marketplace-directory` or Directory-registered ids only

## 6. Checker

- [ ] Flag defaults false
- [ ] No invented Hyperlight provider in `providers/registry`
- [ ] No `P:\` or absolute paths in new content
- [ ] `/api/chat` still functions
- [ ] AG-UI route or health reserved path present

## 7. Reflector

- [ ] Seal trail only after Checker PASS on the real repo
- [ ] Optional next seed: “Stand up CopilotKit Next client against OrchestrationApi AG-UI”
