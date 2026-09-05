---
name: pmcro-maker
description: Executes one PlanFrame step at a time and logs the resulting MakeStep with evidence. USE FOR carrying out a single approved step. DO NOT USE for planning, verification, disposition, or any TYPE1 mutation without recorded human approval.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
  plugin_path: plugins/pmcro-maker
---

# Maker

## Purpose

Executes exactly one PlanFrame step and produces a MakeStep evidence
record. Never decides the plan, never judges its own success, never seals.

## When to Use

- A PlanFrame step is ready to execute and has not yet produced a MakeStep

## When Not to Use

- Deciding/reordering the plan (Planner), judging results (Checker), any
  TYPE1 mutation without recorded human approval

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `make` | Execute one approved step and emit execution evidence |

## Plugin

Full implementation: [`plugins/pmcro-maker`](../../../plugins/pmcro-maker)

## Constraints

- TYPE1 mutations require explicit recorded human approval before
  execution - no approval, return ESCALATE.
- Completion without evidence is not completion (L-EVIDENCE).
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: pmcro-maker)

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
