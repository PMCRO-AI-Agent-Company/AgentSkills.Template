---
id: case-based-reasoning
package: reasoning-strategy
kind: strategy
family: "Family 5 — Analogical & Case-Based"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [analogical, inductive]
  operational_methods: [linear_cot]
  domain_capabilities: [common_sense, multi_hop_relational]
---
# case-based-reasoning

Migrated from `.agents/skills/reasoning/case-based-reasoning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Reuse and adapt solutions from similar prior situations.

## When to Use
- Recurring operational problems, support issues, design patterns

## When Not to Use
- Truly novel problems with no useful precedent

## Workflow
1. Describe the current problem features.
2. Retrieve 1–3 similar past cases.
3. Compare similarities and differences.
4. Adapt the prior solution to the differences.
5. Apply and note what to remember for next time.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "case-based-reasoning"`, `steps`
(retrieved cases and the adaptation), `result`.
