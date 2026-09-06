---
id: progressive-deepening
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
  logical_paradigms: [abductive, deductive]
  operational_methods: [branching_search, test_time_compute]
  domain_capabilities: [strategic_agentic]
---
# progressive-deepening

Migrated from `.agents/skills/reasoning/progressive-deepening/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Allocate depth where it pays off instead of uniform deep analysis.

## When to Use
- Broad design spaces, research, option evaluation

## When Not to Use
- Problems that require uniform full detail on every part

## Workflow
1. Survey the space at a shallow level.
2. Identify the most promising 1–3 branches.
3. Deepen only those branches.
4. Reassess and deepen further if needed.
5. Deliver the best-supported conclusion.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "progressive-deepening"`, `steps`
(shallow survey, then deepened branches), `result`.
