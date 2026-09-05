---
name: case-based-reasoning
description: Retrieve similar past cases, adapt their solutions, and apply. USE FOR recurring problem types. DO NOT USE for one-off problems with no precedent.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [analogical, inductive]
    operational_methods: [linear_cot]
    domain_capabilities: [common_sense, multi_hop_relational]
---

# case-based-reasoning

## Purpose
Reuse and adapt solutions from similar prior situations.

## When to Use
- Recurring operational problems, support issues, design patterns

## When Not to Use
- Truly novel problems with no useful precedent

## Workflow
1. Describe the current problem features.\n2. Retrieve 1–3 similar past cases.\n3. Compare similarities and differences.\n4. Adapt the prior solution to the differences.\n5. Apply and note what to remember for next time.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
