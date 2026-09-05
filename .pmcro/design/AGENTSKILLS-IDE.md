# AgentSkills IDE / Workspace

## Status

Implemented foundation: CopilotKit + AG-UI transport + Aspire-hosted Next.js workspace.

## Verified architecture

```text
AgentSkills Workspace (Next.js + CopilotKit)
        |
        v
ProjectName.Api /ag-ui (HTTP edge/proxy)
        |
        v
ProjectName.GrpcService /ag-ui (MAF AG-UI host)
        |
        v
Planner -> Maker -> Checker -> Reflector
        |
        +--> Maker-only MCP: Filesystem / Terminal / Playwright
```

MAF's `MapAGUIServer` exposes an `AIAgent` through AG-UI/SSE, which is the protocol boundary used by the CopilotKit runtime. This keeps the browser out of the orchestration and actuator trust boundary.

## IDE surfaces

| Surface | Purpose | Authoritative source |
|---|---|---|
| Agents | discover agent identities and capabilities | MAF/runtime manifests |
| Skills | browse manifests, assets, references, scripts | `.agents/` / marketplace |
| MCP | inspect tools, resources, prompts and safety contracts | MCP servers |
| Trails | inspect plans, actions, evidence, verdicts and baton state | `.pmcro/` trail artifacts |
| Command Center | conversational control surface | AG-UI + MAF |

## Next implementation increments

1. Add a read-only workspace index API for `.agents`, `plugins`, `.pmcro`, and `examples`.
2. Add skill detail/editor views that understand `SKILL.md`, `AGENTS.md`, assets, references, and scripts.
3. Add MCP catalog views backed by `tools/list`, `resources/list`, and `prompts/list`.
4. Add a trail inspector that renders typed phase artifacts and evidence lineage.
5. Surface human-in-the-loop approval requests in the CopilotKit UI; never approve sensitive actions in the browser without the server-side governance decision.
6. Add command palette / keyboard navigation so the workspace behaves like an IDE rather than a chat-only application.
7. Add governed file mutations through the existing filesystem MCP boundary instead of granting the browser direct filesystem access.

## Invariants

- MAF remains the execution/orchestration authority.
- PMCRO governance remains server-side.
- MCP side effects remain behind Maker and existing safety contracts.
- CopilotKit is optional UI infrastructure, not a replacement for the runtime.
- API remains the external HTTP edge.
