---
name: analogical-reasoning
description: Map structure from a familiar domain to the target. USE FOR novel problems with known structure. DO NOT USE when a direct procedure exists.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [analogical]
    operational_methods: [linear_cot]
    domain_capabilities: [common_sense, multi_hop_relational]
---

# analogical-reasoning

## Purpose
Transfer relational structure from a well-understood source to the target problem.

## When to Use
- Novel situations that share structure with a known one

## When Not to Use
- Problems with a direct algorithmic solution

## Workflow
1. State the target.\n2. Retrieve 1–2 analogous source situations.\n3. Map roles and relations.\n4. Transfer the solution pattern.\n5. Check where the analogy breaks.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
