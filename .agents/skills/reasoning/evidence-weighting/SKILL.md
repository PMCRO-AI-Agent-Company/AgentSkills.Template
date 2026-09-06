---
name: evidence-weighting
description: List evidence for and against a claim and weight it explicitly. USE FOR contested factual claims. DO NOT USE for pure preference questions.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive, abductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational]
---

# evidence-weighting

## Purpose
Make the evidential balance visible instead of jumping to a conclusion.

## When to Use
- Disputed facts, research synthesis, due-diligence questions

## When Not to Use
- Pure taste or preference questions

## Workflow
1. State the claim.\n2. List supporting evidence with strength.\n3. List opposing evidence with strength.\n4. Weigh and justify the balance.\n5. Conclude with confidence calibrated to the weights.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
