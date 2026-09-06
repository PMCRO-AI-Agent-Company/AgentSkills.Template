---
id: react-loop
package: pmcro-omode
kind: strategy
family: "Family 6 — Interactive / Grounded"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [abductive, deductive]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [strategic_agentic]
---
# react-loop

Migrated from `.agents/skills/reasoning/react-loop/SKILL.md` (v1.0.0) into the
single-file `reasoning-strategy/` convention.

## Purpose
Interleave thinking, actions, and real observations until the goal is met.

## When to Use
- Tool use, web search, code execution, APIs

## When Not to Use
- Pure reasoning with no external actions

## Workflow
1. Thought: current sub-goal.
2. Action: one concrete tool/command.
3. Observation: record real result.
4. Repeat until done or limit hit.
5. Final answer grounded only in observations.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "react-loop"`, `steps` (each
thought/action/observation triple), `result`.

Note: `execute-provider-action` is explicitly outside this agent's
permissions — the Thought/Action/Observation loop above is descriptive of the
reasoning shape only. Actual tool invocation remains Maker's job under the
governed cycle.
