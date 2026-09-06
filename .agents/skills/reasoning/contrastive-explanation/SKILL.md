---
name: contrastive-explanation
description: Explain why P rather than Q (contrastive why). USE FOR explanatory questions. DO NOT USE for pure how-to procedures.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [causal_counterfactual, abductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational, common_sense]
---

# contrastive-explanation

## Purpose
Give explanations that answer the implicit foil, not just a causal story.

## When to Use
- Why-questions, post-hoc explanations, diagnosis narratives

## When Not to Use
- Pure procedural how-to without a contrast

## Workflow
1. Identify the fact P to explain.\n2. Identify the contrast Q (why P not Q).\n3. Find factors that differentiate P from Q.\n4. Explain using those differentiating factors.\n5. Avoid listing causes that also apply to Q.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
