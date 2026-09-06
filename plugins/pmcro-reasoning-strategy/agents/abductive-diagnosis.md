---
id: abductive-diagnosis
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
  logical_paradigms: [abductive]
  operational_methods: [branching_search, iterative_self_reflective]
  domain_capabilities: [multi_hop_relational, strategic_agentic]
---
# abductive-diagnosis

Migrated from `.agents/skills/reasoning/abductive-diagnosis/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Find the best current explanation when information is incomplete.

## When to Use
- Error diagnosis, incident analysis, why-is-this-happening

## When Not to Use
- Full premises that allow pure deduction

## Workflow
1. List observations exactly.
2. Generate 2–4 candidate explanations.
3. Note what each explains and misses.
4. Rank by power, simplicity, consistency.
5. State leading hypothesis and needed evidence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "abductive-diagnosis"`, `steps`
(observations, candidates, ranking), `result`.
