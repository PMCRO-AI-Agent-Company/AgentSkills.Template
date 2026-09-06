---
id: constraint-satisfaction
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
  logical_paradigms: [deductive]
  operational_methods: [branching_search, linear_cot]
  domain_capabilities: [mathematical_symbolic, strategic_agentic]
---
# constraint-satisfaction

Migrated from `.agents/skills/reasoning/constraint-satisfaction/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Make constraints explicit so invalid candidates are eliminated early.

## When to Use
- Scheduling, configuration, design under requirements, puzzles

## When Not to Use
- Open-ended creative generation with no hard constraints

## Workflow
1. List all hard constraints.
2. List soft preferences separately.
3. Generate candidates that meet hard constraints.
4. Rank by soft preferences.
5. Return the best feasible solution and note any trade-offs.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "constraint-satisfaction"`,
`steps` (constraints, candidates, ranking), `result`.
