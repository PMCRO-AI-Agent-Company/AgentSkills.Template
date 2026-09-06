---
id: self-refine
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
  logical_paradigms: [inductive, abductive]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [multi_hop_relational, common_sense]
---
# self-refine

Migrated from `.agents/skills/reasoning/self-refine/SKILL.md` (v1.0.0) into the
single-file `reasoning-strategy/` convention.

## Purpose
Produce an initial draft, explicitly critique it against defined criteria,
then revise until quality thresholds are met.

## When to Use
- Writing, summarization, analysis, or code generation where quality matters
- High-stakes outputs that require explicit checking before delivery

## When Not to Use
- Simple factual lookups with deterministic answers
- Contexts where multiple passes are not permitted or too costly

## Workflow
1. Restate the goal and success criteria.
2. Produce an initial draft.
3. Critique the draft: identify specific weaknesses, gaps, or errors against
   the criteria.
4. Revise the draft to address each critique point.
5. Repeat steps 3–4 until no critical issues remain or a maximum iteration
   count is reached.
6. Deliver the final revised output.

## Validation
- At least one critique-and-revise cycle was completed
- Each critique point was addressed in the revision
- Final output satisfies all stated success criteria

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "self-refine"`, `steps` (each
draft/critique/revision cycle), `result`.
