---
id: contrastive-explanation
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
  logical_paradigms: [causal_counterfactual, abductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational, common_sense]
---
# contrastive-explanation

Migrated from `.agents/skills/reasoning/contrastive-explanation/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Give explanations that answer the implicit foil, not just a causal story.

## When to Use
- Why-questions, post-hoc explanations, diagnosis narratives

## When Not to Use
- Pure procedural how-to without a contrast

## Workflow
1. Identify the fact P to explain.
2. Identify the contrast Q (why P not Q).
3. Find factors that differentiate P from Q.
4. Explain using those differentiating factors.
5. Avoid listing causes that also apply to Q.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "contrastive-explanation"`,
`steps` (P, Q, and the differentiating factors), `result`.
