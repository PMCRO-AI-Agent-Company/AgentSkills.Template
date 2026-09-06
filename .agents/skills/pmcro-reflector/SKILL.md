---
name: pmcro-reflector
description: Records disposition, promotes Earned Constraints every cycle, optionally produces the next seed intent, and seals the trail. Also owns trail materialization. USE FOR closing a cycle after Checker's verdict. DO NOT USE to fix findings or rewrite laws.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
  plugin_path: plugins/pmcro
---

# Reflector

## Purpose

Closes the cycle: disposition from Checker's verdict, unconditional Earned
Constraint promotion every cycle, optional next seed, and sealing the
trail. Sole role permitted to seal. Folds in the scope of the deprecated
standalone `pmcro-trail` role (see `.pmcro/directory/agents.yaml`).

## When to Use

- Exactly once, right after Checker emits its verdict

## When Not to Use

- Fixing anything Checker found (fresh cycle, Orchestrator dispatches to
  Planner again), rewriting laws, executing provider actions

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `reflect` | Disposition, Earned Constraints, next seed, seal |

## Plugin

Full implementation: [`plugins/pmcro`](../../../plugins/pmcro) (consolidated plugin; skill: `skills/reflect`, agent: `agents/reflector.md`)

## Constraints

- Earned Constraints are promoted every cycle, not gated on PASS.
- Sealed trails are immutable - corrections use a new trail, never an edit.
- Follow L-EVIDENCE, L-CHECKER-GATE, L-STATE-MEMORY, L-PLUGIN-ISOLATION,
  L-OUTPUT-CONTRACT.

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: pmcro-reflector)

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
