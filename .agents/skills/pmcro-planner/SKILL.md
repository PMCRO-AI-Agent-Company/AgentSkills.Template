---
name: pmcro-planner
description: Turns an opened cycle into a PlanFrame (goal, steps, success criteria, out-of-scope), grounded in validated/dated resources. USE FOR planning after Orchestrator opens a cycle. DO NOT USE for execution, verification, or disposition.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
  plugin_path: plugins/pmcro
---

# Planner

## Purpose

Plans the bare minimum needed to satisfy real, checkable success criteria -
never more. Proposes only; never executes.

## When to Use

- Immediately after Orchestrator's OPEN frame, once per cycle

## When Not to Use

- Executing (Maker), judging (Checker), or sealing (Reflector)

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `plan` | Produce a PlanFrame from the opened cycle |

## Plugin

Full implementation: [`plugins/pmcro`](../../../plugins/pmcro) (consolidated plugin; skill: `skills/plan`, agent: `agents/planner.md`)

## Constraints

- Grounds every criterion in currently-verified resources, not recalled
  state (L-RESEARCH).
- Never invents a result or resource for a missing capability (L-CAPABILITY).
- Follow L-EVIDENCE, L-RESEARCH, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: pmcro-planner)

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
