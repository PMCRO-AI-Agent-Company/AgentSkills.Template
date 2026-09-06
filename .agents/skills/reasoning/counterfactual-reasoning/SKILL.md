---
name: counterfactual-reasoning
description: Reason about what would have happened if a factor differed. USE FOR post-mortems and impact analysis. DO NOT USE for pure factual lookup.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [causal_counterfactual]
    operational_methods: [linear_cot]
    domain_capabilities: [strategic_agentic, multi_hop_relational]
---

# counterfactual-reasoning

## Purpose
Isolate causal contribution by comparing actual vs alternative worlds.

## When to Use
- Post-mortems, decision reviews, what-if questions

## When Not to Use
- Questions that only need actual facts

## Workflow
1. State actual outcome and factor of interest.\n2. Construct a clear counterfactual.\n3. Hold other conditions fixed.\n4. Reason about the alternative outcome.\n5. Contrast to isolate the factor’s contribution.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
