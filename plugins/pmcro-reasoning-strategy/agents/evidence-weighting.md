---
id: evidence-weighting
package: reasoning-strategy
kind: strategy
family: "Family 4 — Causal & Explanatory"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [inductive, abductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational]
---
# evidence-weighting

Migrated from `.agents/skills/reasoning/evidence-weighting/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Make the evidential balance visible instead of jumping to a conclusion.

## When to Use
- Disputed facts, research synthesis, due-diligence questions

## When Not to Use
- Pure taste or preference questions

## Workflow
1. State the claim.
2. List supporting evidence with strength.
3. List opposing evidence with strength.
4. Weigh and justify the balance.
5. Conclude with confidence calibrated to the weights.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "evidence-weighting"`, `steps`
(supporting and opposing evidence), `result`, `confidence`.
