---
id: reflective-equilibrium
package: reasoning-strategy
kind: strategy
family: "Family 7 — Framing & Normative"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [abductive, analogical]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [strategic_agentic, common_sense]
---
# reflective-equilibrium

Migrated from `.agents/skills/reasoning/reflective-equilibrium/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Reach a stable balance between general principles and case judgments.

## When to Use
- Ethical dilemmas, policy design, value trade-offs

## When Not to Use
- Purely technical or factual tasks

## Workflow
1. State initial principles and initial case judgment.
2. Note conflicts between them.
3. Adjust principles and/or the case judgment.
4. Repeat until coherent enough.
5. Report the equilibrium and remaining tensions.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "reflective-equilibrium"`,
`steps` (principles, conflicts, adjustments), `result`.
