---
id: self-consistency
package: reasoning-strategy
kind: strategy
family: "Family 2 — Search / Exploration"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, inductive]
  operational_methods: [test_time_compute, linear_cot]
  domain_capabilities: [mathematical_symbolic, multi_hop_relational]
---
# self-consistency

Migrated from `.agents/skills/reasoning/self-consistency/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Reduce single-trace brittleness via majority/consensus over independent
solutions.

## When to Use
- Math, logic, factual questions with a correct answer

## When Not to Use
- Creative tasks where diversity is the goal

## Workflow
1. Generate 3–5 independent traces.
2. Extract each final answer.
3. Cluster equivalents.
4. Select majority/highest-confidence.
5. Report vote count and notable dissent.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "self-consistency"`, `steps`
(each trace's answer plus the clustering/vote), `result`.
