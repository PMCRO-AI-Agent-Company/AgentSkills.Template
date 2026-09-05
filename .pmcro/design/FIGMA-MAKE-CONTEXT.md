# Figma Make Context — AgentSkills Workspace

## Canonical source
Repository: `PMCRO-AI-Agent-Company/AgentSkills.Template`
Branch: `master`
Purpose: design and evolve the AgentSkills Workspace UI without creating a second architecture.

## Product
The UI is an IDE-like **AgentSkills Workspace**. It is not primarily a chat application. Chat/command interaction is one surface inside a workspace that lets a developer understand and operate an agent colony.

## Primary information architecture
```text
AgentSkills Workspace
├── Agents
├── Skills
├── MCP
├── Trails
└── Command Center
```

### Agents
Show agent identity, persona/kind, lifecycle state, capabilities, skills, packaging targets, and ownership. The Agent Directory design lives in `.pmcro/design/ADR-pmcro-agent-directory-and-marketplace.md`.

### Skills
Treat repository skill packages as first-class artifacts. A skill may contain `SKILL.md`, `assets/`, `references/`, `scripts/`, and `examples/`. The filesystem/repository is the source of truth; do not invent a separate UI database as the authoritative store.

### MCP
Represent the real actuator boundary: Filesystem, Terminal, and Playwright. Surface tool availability and execution state, but do not move actuator authority into the browser.

### Trails
Represent governed execution history, evidence, verdicts, and succession. Trails are evidence, not decorative activity logs.

### Command Center
Provide a command/chat surface for asking agents to inspect, plan, execute, verify, and reflect. It should expose state and approvals clearly rather than hiding governance behind chat.

## Visual direction
- Developer-tool / IDE quality.
- Dense but calm information hierarchy.
- Desktop-first.
- Strong persistent navigation and clear current-context selection.
- Workspace/editor surface is primary; inspector/activity panels are secondary.
- Command Center can be persistent or docked, but must not dominate the entire application.
- Use restrained surfaces, borders, typography, spacing, and status indicators.
- Favor semantic state indicators over decorative gradients or excessive marketing visuals.
- Support dark mode as a first-class experience.
- Keyboard navigation and accessible contrast are required.

## Key screens to design
1. **Workspace overview** — agents, skills, MCP, trails, recent activity, health.
2. **Agent detail** — identity + capabilities + skills + packaging + run history.
3. **Skill detail/editor** — manifest, files, references/assets/scripts, validation state.
4. **MCP inspector** — servers, tools, resources/prompts, connection/execution status.
5. **Trail viewer** — lifecycle phases, evidence, approvals, verdict, next-seed/succession.
6. **Command Center** — governed agent interaction with visible execution state.

## Architecture constraints
The intended request path is:
`UI → ProjectName.Api → ProjectName.GrpcService → MAF/model`

MCP is reached by the runtime as the side-effect boundary. Aspire owns topology. `.pmcro/` owns governance and design authority. Skills and plugins remain portable repository artifacts.

Do not:
- put model/provider credentials in browser code;
- make CopilotKit the source of truth;
- create a parallel agent/skill database;
- bypass the API/runtime boundary for governed actions;
- rename application projects to PMCRO-prefixed names;
- replace the existing MAF/PMCRO execution architecture for visual convenience.

## Existing design authority
Read these before making architectural UI decisions:
- `.pmcro/design/README.md`
- `.pmcro/design/ADR-pmcro-agent-directory-and-marketplace.md`
- `.pmcro/design/CLEAN-ARCHITECTURE-ASPIRE-COPILOTKIT.md`
- `.pmcro/design/MAF-WORKFLOWS-ASPIRE.md`
- `.pmcro/design/AGENTSKILLS-IDE.md` if present

## Implementation target
The current web UI lives under `ui/projectname-copilotkit/` when that directory has been pushed to GitHub. The UI uses Next.js/React and CopilotKit as an interface layer over AG-UI. Adapt the design to the existing implementation rather than replacing working runtime contracts.

## Design-to-code rule
A Figma design is a visual specification, not permission to rewrite architecture. Reuse existing project components/tokens where possible, keep real repository concepts, and preserve the boundaries above.
