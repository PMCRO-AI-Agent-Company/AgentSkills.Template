---
id: plan-and-execute
package: reasoning-strategy
kind: strategy
family: "Family 1 — Linear / Sequential"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, abductive]
  operational_methods: [linear_cot, strategic_agentic]
  domain_capabilities: [strategic_agentic]
---
# plan-and-execute

Migrated from `.agents/skills/reasoning/plan-and-execute/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Separate planning from execution so the approach is visible and adjustable.

## When to Use
- Multi-step projects, coding tasks, research workflows

## When Not to Use
- Single-shot factual questions

## Workflow
1. Restate the goal and constraints.
2. Produce a numbered plan of concrete steps.
3. Execute steps in order, recording results.
4. Adjust the plan only when a step fails or new information appears.
5. Summarize outcome against the original plan.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "plan-and-execute"`, `steps` (the
plan plus execution notes for each step), `result`.
