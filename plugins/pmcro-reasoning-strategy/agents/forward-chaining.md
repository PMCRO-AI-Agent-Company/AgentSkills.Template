---
id: forward-chaining
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
  logical_paradigms: [deductive, inductive]
  operational_methods: [linear_cot]
  domain_capabilities: [mathematical_symbolic, multi_hop_relational]
---
# forward-chaining

Migrated from `.agents/skills/reasoning/forward-chaining/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Derive consequences systematically from what is already known.

## When to Use
- Rule application, data-driven conclusions, simulation of effects

## When Not to Use
- Goal-directed tasks better solved by working backward

## Workflow
1. List known facts/rules.
2. Apply applicable rules to derive new facts.
3. Repeat until goal reached or no new facts.
4. Trace the derivation path.
5. State conclusions with supporting chain.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "forward-chaining"`, `steps` (the
derivation trace), `result`.
