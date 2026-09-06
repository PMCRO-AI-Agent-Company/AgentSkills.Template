---
id: counterfactual-reasoning
package: pmcro-omode
kind: strategy
family: "Family 4 — Causal & Explanatory"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [causal_counterfactual]
  operational_methods: [linear_cot]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# counterfactual-reasoning

Migrated from `.agents/skills/reasoning/counterfactual-reasoning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Isolate causal contribution by comparing actual vs alternative worlds.

## When to Use
- Post-mortems, decision reviews, what-if questions

## When Not to Use
- Questions that only need actual facts

## Workflow
1. State actual outcome and factor of interest.
2. Construct a clear counterfactual.
3. Hold other conditions fixed.
4. Reason about the alternative outcome.
5. Contrast to isolate the factor's contribution.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "counterfactual-reasoning"`,
`steps` (actual vs counterfactual comparison), `result`.
