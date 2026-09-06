---
id: chain-of-thought
package: pmcro-omode
kind: strategy
family: "Family 1 — Linear / Sequential"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, inductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational, mathematical_symbolic]
---
# chain-of-thought

Migrated from `.agents/skills/reasoning/chain-of-thought/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Force explicit ordered intermediate steps so the answer is grounded in visible work.

## When to Use
- Multi-step math, logic, or factual questions

## When Not to Use
- Tasks needing multiple alternative paths

## Workflow
1. Restate the goal.
2. Break into ordered sub-steps.
3. Solve each sub-step with intermediate results.
4. Carry forward only needed results.
5. State the final answer after the last step.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "chain-of-thought"`, `steps` (one
entry per step actually performed), `result`.
