---
id: goal-regression
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
  logical_paradigms: [deductive]
  operational_methods: [branching_search, linear_cot]
  domain_capabilities: [strategic_agentic]
---
# goal-regression

Migrated from `.agents/skills/reasoning/goal-regression/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Connect a high-level goal to concrete actions via goal regression.

## When to Use
- Action planning, procedure synthesis, agent task planning

## When Not to Use
- Descriptive or explanatory questions with no actions

## Workflow
1. State the top-level goal.
2. Choose an operator that achieves it.
3. Regress to the operator's preconditions.
4. Repeat until preconditions are currently true.
5. Reverse into an executable action sequence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "goal-regression"`, `steps` (the
regression chain, reversed into forward order), `result`.
