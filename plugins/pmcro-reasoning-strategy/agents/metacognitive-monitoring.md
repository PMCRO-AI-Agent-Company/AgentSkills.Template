---
id: metacognitive-monitoring
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
  logical_paradigms: [abductive, inductive]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [strategic_agentic, common_sense]
---
# metacognitive-monitoring

Migrated from `.agents/skills/reasoning/metacognitive-monitoring/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Make the model's own uncertainty visible and actionable.

## When to Use
- High-stakes decisions, ambiguous evidence, advice under uncertainty

## When Not to Use
- Tasks where a single confident answer is mandatory and evidence is clear

## Workflow
1. Attempt the solution.
2. Rate confidence (low/medium/high) with reasons.
3. List what would raise or lower confidence.
4. If confidence is low, propose what information is still needed.
5. Deliver answer together with the confidence statement.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "metacognitive-monitoring"`,
`steps`, `result`, `confidence` (low/medium/high with reasons).
