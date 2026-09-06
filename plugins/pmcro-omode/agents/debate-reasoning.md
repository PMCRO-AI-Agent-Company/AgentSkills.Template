---
id: debate-reasoning
package: pmcro-omode
kind: strategy
family: "Family 3 — Iterative / Reflective"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [abductive, analogical]
  operational_methods: [branching_search, iterative_self_reflective]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# debate-reasoning

Migrated from `.agents/skills/reasoning/debate-reasoning/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Surface strongest arguments on more than one side before concluding.

## When to Use
- Policy, design trade-offs, ethical or strategic questions

## When Not to Use
- Straightforward factual or coding tasks

## Workflow
1. Frame the question and decision axes.
2. Strongest case for Side A.
3. Strongest case for Side B (and C if needed).
4. Points of agreement and conflict.
5. Synthesize with trade-offs and uncertainties.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "debate-reasoning"`, `steps`
(each side's case plus the synthesis), `result`.
