---
id: recursive-summarization
package: reasoning-strategy
kind: strategy
family: "Family 1 — Linear / Sequential"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [inductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational]
---
# recursive-summarization

Migrated from `.agents/skills/reasoning/recursive-summarization/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Preserve important information while compressing long material hierarchically.

## When to Use
- Long documents, large logs, multi-file summaries

## When Not to Use
- Short texts that fit in one pass

## Workflow
1. Split material into coherent chunks.
2. Summarize each chunk.
3. Summarize the chunk summaries.
4. Optionally repeat another level.
5. Produce final summary with traceable key points.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "recursive-summarization"`, `steps`
(each compression level performed), `result`.
