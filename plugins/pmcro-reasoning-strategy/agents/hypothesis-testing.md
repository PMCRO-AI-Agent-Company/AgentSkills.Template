---
id: hypothesis-testing
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
  logical_paradigms: [abductive, deductive]
  operational_methods: [branching_search, iterative_self_reflective]
  domain_capabilities: [multi_hop_relational, strategic_agentic]
---
# hypothesis-testing

Migrated from `.agents/skills/reasoning/hypothesis-testing/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Treat claims as testable hypotheses rather than assertions.

## When to Use
- Research, debugging, causal questions, uncertain claims

## When Not to Use
- Tasks that only need a direct procedural answer

## Workflow
1. State the question.
2. Propose 2–3 competing hypotheses.
3. For each, list confirming and disconfirming evidence.
4. Evaluate against available evidence.
5. Rank hypotheses and state what would change the ranking.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "hypothesis-testing"`, `steps`
(hypotheses and their evidence), `result`.
