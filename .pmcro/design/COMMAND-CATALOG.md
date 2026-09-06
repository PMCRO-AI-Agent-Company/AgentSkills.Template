# Command catalog (command-style design)

Invoke by **plugin:skill** where the host supports plugins, or by **bare skill name**.

## Lifecycle (canonical repo plugin — reference)

**Corrected 2026-09-06:** the 5 lifecycle roles were consolidated into one
plugin, `plugins/pmcro` (formerly 5 separate plugins:
pmcro-orchestrator/-planner/-maker/-checker/-reflector — see
`plugins/pmcro/plugin.json`). Invoke as `/pmcro:<skill>`, not
`/pmcro-<role>:<skill>`.

| Command | Role |
|---------|------|
| `/pmcro:orchestrate` | Sole dispatch |
| `/pmcro:plan` | PlanFrame |
| `/pmcro:make` | Execute one step + evidence |
| `/pmcro:check` | Independent gate |
| `/pmcro:reflect` | Disposition + seal |

`pmcro-trail` is deprecated (2026-09-05, see `manifest.yaml` and
`directory/agents.yaml`) — sealing/trail materialization is a Reflector
permission (`seal-cycle`), not a separate role. There is no
`/pmcro-trail:initialize` command.

## This workspace (active)

| Command / name | What it does |
|----------------|--------------|
| `scaffold-skill` | Validate AgentScaffoldSpec → agentskills / maf-inline |
| `register-agent` | Upsert Agent Directory |
| `pmcro-chief-learning-officer` | Learning intent frames |
| `python .pmcro/runtime/queue_runtime.py list\|claim\|checkpoint\|complete\|status` | Queue + checkpoints |

## Marketplace style (when host has plugins)

```text
/pmcro-marketplace-directory:scaffold-skill --spec examples/...
/plugin marketplace add dotnet/skills
```

## MAF / Aspire workflows (runtime, not UI)

Prefer **Microsoft Agent Framework workflows** (sequential / concurrent / handoff) *inside Runtime*, composed with Aspire AppHost topology.  
Not CopilotKit. Chat stays on your existing OrchestrationApi.

## Seed intent form

```text
/[plugin]:[skill] [optional instructions]
```

or natural language that names the skill.
