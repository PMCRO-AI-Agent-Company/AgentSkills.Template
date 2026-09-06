---
id: analogical-transfer-check
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
  logical_paradigms: [analogical, causal_counterfactual]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [common_sense, multi_hop_relational]
---
# analogical-transfer-check

Migrated from `.agents/skills/reasoning/analogical-transfer-check/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Prevent over-transfer by stress-testing the analogy's limits.

## When to Use
- After any solution or explanation that relied on analogy

## When Not to Use
- Direct solutions that did not use analogy

## Workflow
1. Restate the analogy mapping.
2. List critical assumptions of the source domain.
3. Check each assumption in the target domain.
4. Mark broken mappings.
5. Adjust or discard the conclusion accordingly.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "analogical-transfer-check"`,
`steps` (assumption checks and any adjustment), `result`.
