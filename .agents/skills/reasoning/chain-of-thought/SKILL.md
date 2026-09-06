---
name: chain-of-thought
description: Linear step-by-step Chain-of-Thought reasoning. USE FOR multi-step problems. DO NOT USE for branching exploration.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, inductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational, mathematical_symbolic]
---

# chain-of-thought

## Purpose
Force explicit ordered intermediate steps so the answer is grounded in visible work.

## When to Use
- Multi-step math, logic, or factual questions

## When Not to Use
- Tasks needing multiple alternative paths

## Workflow
1. Restate the goal.\n2. Break into ordered sub-steps.\n3. Solve each sub-step with intermediate results.\n4. Carry forward only needed results.\n5. State the final answer after the last step.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
