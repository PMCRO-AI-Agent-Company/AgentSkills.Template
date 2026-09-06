---
name: error-driven-learning
description: When an answer fails, extract the error pattern and apply the lesson. USE FOR iterative improvement after failures. DO NOT USE on the first attempt with no feedback.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive, abductive]
    operational_methods: [iterative_self_reflective]
    domain_capabilities: [strategic_agentic, multi_hop_relational]
---

# error-driven-learning

## Purpose
Turn failures into explicit rules that prevent the same mistake.

## When to Use
- After a failed attempt, failed test, or wrong answer with feedback

## When Not to Use
- First-pass generation with no error signal

## Workflow
1. State the failed answer and the feedback/error.\n2. Diagnose the specific mistake pattern.\n3. Formulate a corrective rule.\n4. Re-solve under the new rule.\n5. Confirm the error no longer appears.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
