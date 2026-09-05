# PMCR-O Canonical Output Contract

> Governed by `L-OUTPUT-CONTRACT` in `../laws/laws.yaml`.  
> Enforced by [`validate_output_contract.py`](./validate_output_contract.py).

All governed PMCRO outputs must identify the execution context and return a structured runtime result. Domain-specific payloads may be included, but they must not replace the governance envelope.

## Required envelope

| Field | Meaning |
|-------|---------|
| `frame_id` | Normalized intent frame identifier |
| `trail_id` | Governed cycle trail identifier |
| `workflow_id` | Execution workflow identifier when a workflow runs |
| `action` | Operation or decision being returned |
| `state_transition` | Explicit current-to-next lifecycle transition |
| `required_evidence` | Evidence required to support the result (array) |
| `next_gate` | Next governance gate, or `none` when sealed |
| `halt_reason` | Required when the result halts or escalates |

## Conformance rules

1. Never return a governed completion as unstructured prose alone.
2. Never omit required governance fields merely because the domain operation succeeded.
3. Domain payloads are subordinate to the governance envelope.
4. A result claiming completion must also satisfy `L-EVIDENCE` and `L-CHECKER-GATE`.
5. `trail_id` must resolve to the governed cycle Trail, and completion Evidence must be attached to that Trail before `SEAL`.
6. Checker acceptance must be recorded against the same `trail_id` before completion is emitted.
7. A result that cannot satisfy the contract must return `ESCALATE` or `HALT`, not fabricate compliance.
8. Human-facing presentation may render the envelope differently, but the underlying governed result remains contract-compliant.

## Validator

`validate_output_contract.py` is the deterministic conformance check for this envelope. It is pure Python standard library and stack-neutral.
