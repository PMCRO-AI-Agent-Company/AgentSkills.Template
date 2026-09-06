---
id: backward-chaining
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
  logical_paradigms: [deductive]
  operational_methods: [linear_cot, branching_search]
  domain_capabilities: [strategic_agentic, mathematical_symbolic]
---
# backward-chaining

Migrated from `.agents/skills/reasoning/backward-chaining/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Derive what must be true or done by working from the goal backward.

## When to Use
- Planning to a known goal, proof-style tasks, requirements derivation

## When Not to Use
- Open exploration with no fixed goal

## Workflow
1. State the goal precisely.
2. Ask what must be true immediately before the goal.
3. Recursively expand prerequisites.
4. Stop at known facts or feasible actions.
5. Reverse the chain into a forward plan.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "backward-chaining"`, `steps` (the
prerequisite chain, reversed into forward order), `result`.
