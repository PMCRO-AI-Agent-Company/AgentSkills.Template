---
id: multi-agent-critique
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
  domain_capabilities: [strategic_agentic]
---
# multi-agent-critique

Migrated from `.agents/skills/reasoning/multi-agent-critique/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Reduce single-viewpoint blind spots by adversarial or complementary
perspectives.

## When to Use
- Policy, safety, design review, contested analysis

## When Not to Use
- Simple factual or procedural questions

## Workflow
1. Define 2–3 named perspectives (e.g. optimist, skeptic, operator).
2. Let each produce an initial view.
3. Let each critique the others.
4. Synthesize a balanced conclusion.
5. Record residual disagreements.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "multi-agent-critique"`, `steps`
(each perspective's view, critiques, and synthesis), `result`.
