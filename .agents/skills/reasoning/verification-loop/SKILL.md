---
name: verification-loop
description: Generate a candidate answer then independently verify it against explicit criteria. USE FOR answers where generation and checking are separable. DO NOT USE when a single-pass answer is sufficient.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, inductive]
    operational_methods: [iterative_self_reflective, linear_cot]
    domain_capabilities: [multi_hop_relational, mathematical_symbolic]
---

# verification-loop

## Purpose
Decouple generation from verification: produce an answer, then verify it against stated criteria as a separate independent step.

## When to Use
- Math, logic, or factual claims where generation and verification can be done independently
- Outputs where self-consistency matters (same method arriving at the same result)

## When Not to Use
- Simple lookups with no verifiable structure
- Contexts that cannot afford multiple passes

## Workflow
1. Restate the goal and explicit verification criteria.
2. Generate a candidate answer using the most direct reasoning path.
3. Switch to a verification stance: treat the candidate as an unverified claim.
4. Check the candidate against each criterion independently (re-derive, check constraints, or test cases).
5. If verification fails, identify the failure and generate a corrected candidate.
6. Repeat steps 3–5 until the answer passes all criteria.
7. Deliver the verified answer.

## Validation
- Generation and verification steps were kept conceptually separate
- Each criterion was explicitly checked
- Any failed verification resulted in a new generation, not a skip

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
