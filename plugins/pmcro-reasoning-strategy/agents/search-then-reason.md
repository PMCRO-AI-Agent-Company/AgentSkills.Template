---
id: search-then-reason
package: reasoning-strategy
kind: strategy
family: "Family 6 — Interactive / Grounded"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [inductive, deductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational]
---
# search-then-reason

Migrated from `.agents/skills/reasoning/search-then-reason/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Ground reasoning in retrieved evidence to reduce hallucination.

## When to Use
- Questions needing up-to-date or document-grounded answers

## When Not to Use
- Pure logic/math that needs no retrieval

## Workflow
1. Formulate search/retrieval queries.
2. Collect relevant snippets/sources.
3. Reason strictly from those sources.
4. Cite which source supports each key claim.
5. Mark any claim not supported by retrieved evidence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "search-then-reason"`, `steps`
(queries, sources, and cited reasoning), `result`.

Note: `execute-provider-action` is outside this agent's permissions — actual
retrieval calls remain Maker's job under the governed cycle.
