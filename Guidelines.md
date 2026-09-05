# AgentSkills Template — Figma Make Guidelines

## Purpose
This repository is the canonical product/code context for the AgentSkills Workspace UI. Treat GitHub code as the implementation source of truth and the `.pmcro/design/` documents as architecture/design authority.

## Design goal
Build an AgentSkills Workspace / IDE-like environment for working with agents, skills, MCP capabilities, trails, and governed runs. The UI should feel like a serious developer tool rather than a generic chatbot.

## Canonical workspace concepts
- Agents: identities, personas, capabilities, lifecycle state.
- Skills: reusable Agent Skills packages and their manifests, assets, references, scripts, and examples.
- MCP: filesystem, terminal, and Playwright actuator capabilities exposed through the runtime.
- Trails: governed execution/evidence history.
- Command Center: conversational control surface for inspecting, planning, running, checking, and reflecting.

## Architecture boundaries
- UI is a presentation/workspace layer.
- MAF remains the agent/workflow runtime.
- MCP remains the actuator boundary.
- Aspire remains the host/topology layer.
- `.pmcro/` remains governance/design authority.
- Do not move side-effecting MCP authority into browser code.
- Do not replace existing runtime architecture with UI-specific business logic.

## UI implementation rules
- Prefer reusable components and design tokens over page-specific one-offs.
- Favor dense, information-rich IDE layouts: navigation, workspace/editor, inspector/activity surfaces, and command/chat areas.
- Make important state visible: running, waiting for approval, verified, failed, unavailable, and stale.
- Preserve keyboard-friendly and accessible interactions.
- Design for desktop first, with sensible responsive degradation.
- Use real repository concepts and filenames instead of placeholder product concepts.
- Avoid invented APIs, services, or integrations.

## Repository navigation priorities
Start by reading:
1. `README.md`
2. `.pmcro/design/README.md`
3. `.pmcro/design/ADR-pmcro-agent-directory-and-marketplace.md`
4. `.pmcro/design/CLEAN-ARCHITECTURE-ASPIRE-COPILOTKIT.md`
5. `.pmcro/design/MAF-WORKFLOWS-ASPIRE.md`
6. `.pmcro/design/AGENTSKILLS-IDE.md` when present
7. `.agents/` and `plugins/` for skill/marketplace structure
8. `ui/projectname-copilotkit/` for the actual workspace UI when present

## Important naming/boundary rule
Keep application project names `ProjectName.*`. Governance concepts belong under `.pmcro/`; do not rename .NET projects to PMCRO-prefixed names just to match governance terminology.

## Design review behavior
When changing UI, inspect existing code first. Reuse existing components and patterns. Keep architecture changes separate from visual changes. Do not fabricate backend data when a real repository artifact can be represented instead.
