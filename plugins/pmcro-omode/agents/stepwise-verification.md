---
id: stepwise-verification
package: pmcro-omode
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
  operational_methods: [linear_cot, iterative_self_reflective]
  domain_capabilities: [multi_hop_relational, mathematical_symbolic]
---
# stepwise-verification

Migrated from `.agents/skills/reasoning/stepwise-verification/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Verify each intermediate step before proceeding to ensure errors are caught early
and do not propagate.

## When to Use
- Multi-step math or logic where early mistakes invalidate the whole chain
- Safety-critical reasoning where each partial result must be trusted

## When Not to Use
- Simple single-step lookups
- Tasks where latency is critical and re-checking is too expensive

## Workflow
1. Restate the goal.
2. Produce the first intermediate step.
3. Verify step 1 against known facts, constraints, or by re-deriving it.
4. If step 1 fails verification, correct it before proceeding.
5. Repeat steps 2–4 for each subsequent step.
6. State the final answer only after all steps pass verification.

## Validation
- Every intermediate step was explicitly verified before continuation
- Any failed verification was corrected, not skipped
- Final answer is grounded in fully verified intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "stepwise-verification"`, `steps`
(one entry per step, each noted as verified/corrected), `result`.
