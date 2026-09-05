# ProjectName Agent Workspace

CopilotKit UI boundary for the AgentSkills template.

## Architecture

```text
Browser
  -> CopilotKit /api/copilotkit
  -> ProjectName.Api /ag-ui
  -> ProjectName.GrpcService /ag-ui
  -> MAF Planner -> Maker -> Checker -> Reflector
  -> Maker-only MCP actuators
```

The UI does not own agent execution or MCP credentials. The .NET runtime remains authoritative.

## Local development

Run the Aspire AppHost from the repository root. Aspire starts this Next.js app as the `projectname-copilotkit` resource and injects `AGUI_BACKEND_URL`.

For standalone development, run `npm run dev` in this directory and set `AGUI_BACKEND_URL` to the API `/ag-ui` endpoint.

## Workspace direction

This shell is intentionally shaped like an AgentSkills IDE: Agents, Skills, MCP, and Trails are first-class navigation surfaces. The next increments can bind those surfaces to governed filesystem APIs, skill manifests, MCP discovery, and trail evidence without moving governance into the browser.
