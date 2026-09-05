# Command catalog (command-style design)

Invoke by **plugin:skill** where the host supports plugins, or by **bare skill name**.

## Lifecycle (canonical repo plugins — reference)

| Command | Role |
|---------|------|
| `/pmcro-trail:initialize` | Open Class-B trail |
| `/pmcro-orchestrator:orchestrate` | Sole dispatch |
| `/pmcro-planner:plan` | PlanFrame |
| `/pmcro-maker:make` | Execute one step + evidence |
| `/pmcro-checker:check` | Independent gate |
| `/pmcro-reflector:reflect` | Disposition + seal |

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
