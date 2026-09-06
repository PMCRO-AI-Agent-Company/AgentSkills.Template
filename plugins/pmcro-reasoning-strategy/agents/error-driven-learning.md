---
id: error-driven-learning
package: reasoning-strategy
kind: strategy
family: "Family 3 — Iterative / Reflective"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [inductive, abductive]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# error-driven-learning

Migrated from `.agents/skills/reasoning/error-driven-learning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Turn failures into explicit rules that prevent the same mistake.

## When to Use
- After a failed attempt, failed test, or wrong answer with feedback

## When Not to Use
- First-pass generation with no error signal

## Workflow
1. State the failed answer and the feedback/error.
2. Diagnose the specific mistake pattern.
3. Formulate a corrective rule.
4. Re-solve under the new rule.
5. Confirm the error no longer appears.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "error-driven-learning"`, `steps`
(the failure, diagnosis, rule, and re-solve), `result`.
