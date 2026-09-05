# Figma / GitHub Design Contract

This directory documents how Figma Make should consume this repository.

## Start here
- `Guidelines.md` — concise repository-wide design/build rules for Figma Make.
- `.pmcro/design/FIGMA-MAKE-CONTEXT.md` — canonical AgentSkills Workspace product and UI context.
- `.pmcro/design/` — architecture/design authority.
- `ui/projectname-copilotkit/` — implementation target when the UI has been pushed to GitHub.

## Source-of-truth order
1. Existing implementation and repository structure.
2. `.pmcro/design/` architecture decisions.
3. `FIGMA-MAKE-CONTEXT.md` visual/product direction.
4. Figma design files as the visual specification.

Figma should design against the real AgentSkills Workspace concepts and existing runtime boundaries. It should not invent a replacement backend architecture.

## GitHub sync
The GitHub-connected Figma Make project should use the repository's current default branch and pull the latest committed UI before implementing changes. Local, uncommitted UI changes are invisible to GitHub-connected design tooling until committed and pushed.

## UI implementation location
```text
ui/projectname-copilotkit/
```

Expected stack: Next.js + React + CopilotKit/AG-UI, with the backend boundary remaining `ProjectName.Api` and `ProjectName.GrpcService`.
