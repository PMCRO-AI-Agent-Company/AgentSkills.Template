---
name: pmcro-orchestrator
description: Sole dispatch authority for the PMCR-O cycle. Opens/claims a trail, routes to a Chief persona for domain scope, hands off to Planner. USE FOR opening a cycle. DO NOT USE for planning, execution, checking, or sealing.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
  plugin_path: plugins/pmcro
---

# Orchestrator

## Purpose

Sole dispatch authority. Claims/accepts a task, mints-or-links a trail, logs
its OPEN frame, hands off to Planner. Never domain work, never seals.

## When to Use

- New seed intent, or a claimable queue item, needs a cycle opened

## When Not to Use

- Planning, executing, checking, or sealing - those belong to Planner,
  Maker, Checker, Reflector

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `orchestrate` | Open a trail cycle and dispatch to Planner |

## Plugin

Full implementation: [`plugins/pmcro`](../../../plugins/pmcro) (consolidated plugin; skill: `skills/orchestrate`, agent: `agents/orchestrator.md`)

## Constraints

- Only role permitted to dispatch (L-ORCHESTRATION).
- Routes to a Chief for domain scope; does not run the Chief's own loop -
  one shared cycle only.
- Follow L-EVIDENCE, L-ORCHESTRATION, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: pmcro-orchestrator)
- Priority scale: `0 stop-the-line -> 1 CEO/CoS -> 2 domain critical -> 3 normal -> 4 backlog`

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
