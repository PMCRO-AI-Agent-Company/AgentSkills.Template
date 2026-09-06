# Project conventions

## Commands
- Build: `dotnet build`
- Test: `dotnet test`
- Lint: `dotnet format`

## Stack
- .NET with C# (strict nullable enabled)
- AgentSkills plugin architecture
- PMCR-O lifecycle: Orchestrator → Planner → Maker → Checker → Reflector

## Rules
- Named exports only; no wildcard re-exports
- Tests live next to source: `Foo.cs` → `Foo.Tests.cs`
- All agent skill outputs use structured frames (PlanFrame, MakeStep, CheckFrame, ReflectFrame)
- Skills live under `.agents/skills/<skill-name>/SKILL.md`
- PMCRO lifecycle plugins live under `.agents/skills/`
- Use `.pmcro/` for all runtime state, trails, and evidence

## Conventions
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`
- PR titles match the commit subject line
- Every new skill must have a `SKILL.md` with YAML frontmatter (`name`, `description`)
