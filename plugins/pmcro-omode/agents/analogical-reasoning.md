---
id: analogical-reasoning
package: pmcro-omode
kind: strategy
family: "Family 5 — Analogical & Case-Based"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [analogical]
  operational_methods: [linear_cot]
  domain_capabilities: [common_sense, multi_hop_relational]
---
# analogical-reasoning

Migrated from `.agents/skills/reasoning/analogical-reasoning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Transfer relational structure from a well-understood source to the target
problem.

## When to Use
- Novel situations that share structure with a known one

## When Not to Use
- Problems with a direct algorithmic solution

## Workflow
1. State the target.
2. Retrieve 1–2 analogous source situations.
3. Map roles and relations.
4. Transfer the solution pattern.
5. Check where the analogy breaks.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "analogical-reasoning"`, `steps`
(source, mapping, transfer, and break-check), `result`.
