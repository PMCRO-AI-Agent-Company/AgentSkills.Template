---
id: decomposition-recomposition
package: pmcro-omode
kind: strategy
family: "Family 1 — Linear / Sequential"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive]
  operational_methods: [linear_cot, branching_search]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# decomposition-recomposition

Migrated from `.agents/skills/reasoning/decomposition-recomposition/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Manage complexity by solving modular pieces and carefully integrating them.

## When to Use
- Large analyses, system design, multi-part questions

## When Not to Use
- Single atomic questions

## Workflow
1. Decompose into non-overlapping parts.
2. Solve each part independently.
3. Check interfaces/dependencies between parts.
4. Recompose into a coherent whole.
5. Validate the integrated result.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "decomposition-recomposition"`,
`steps` (each part's solution plus the recomposition step), `result`.
