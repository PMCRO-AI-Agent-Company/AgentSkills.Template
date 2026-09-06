---
id: dual-process
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
  logical_paradigms: [inductive, deductive]
  operational_methods: [linear_cot, iterative_self_reflective]
  domain_capabilities: [common_sense, mathematical_symbolic]
---
# dual-process

Migrated from `.agents/skills/reasoning/dual-process/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Combine speed of intuition with reliability of deliberate checking.

## When to Use
- Everyday problems, estimates, first-pass diagnoses

## When Not to Use
- Safety-critical tasks that forbid intuitive first answers

## Workflow
1. Give a fast intuitive answer (mark it as provisional).
2. Switch to slow analysis: assumptions, steps, checks.
3. Compare intuitive vs deliberate results.
4. Prefer the deliberate result when they conflict.
5. Report both if educational.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "dual-process"`, `steps`
(intuitive answer, deliberate analysis, comparison), `result`.
