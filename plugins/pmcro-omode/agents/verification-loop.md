---
id: verification-loop
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
  logical_paradigms: [deductive, inductive]
  operational_methods: [iterative_self_reflective, linear_cot]
  domain_capabilities: [multi_hop_relational, mathematical_symbolic]
---
# verification-loop

Migrated from `.agents/skills/reasoning/verification-loop/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Decouple generation from verification: produce an answer, then verify it
against stated criteria as a separate independent step.

## When to Use
- Math, logic, or factual claims where generation and verification can be
  done independently
- Outputs where self-consistency matters (same method arriving at the same
  result)

## When Not to Use
- Simple lookups with no verifiable structure
- Contexts that cannot afford multiple passes

## Workflow
1. Restate the goal and explicit verification criteria.
2. Generate a candidate answer using the most direct reasoning path.
3. Switch to a verification stance: treat the candidate as an unverified claim.
4. Check the candidate against each criterion independently (re-derive, check
   constraints, or test cases).
5. If verification fails, identify the failure and generate a corrected
   candidate.
6. Repeat steps 3–5 until the answer passes all criteria.
7. Deliver the verified answer.

## Validation
- Generation and verification steps were kept conceptually separate
- Each criterion was explicitly checked
- Any failed verification resulted in a new generation, not a skip

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "verification-loop"`, `steps`
(generation and verification passes), `result`.
