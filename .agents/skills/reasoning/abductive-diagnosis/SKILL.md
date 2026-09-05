---
name: abductive-diagnosis
description: Infer the most likely explanation from incomplete evidence. USE FOR debugging and root-cause. DO NOT USE for pure deduction.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive]
    operational_methods: [branching_search, iterative_self_reflective]
    domain_capabilities: [multi_hop_relational, strategic_agentic]
---

# abductive-diagnosis

## Purpose
Find the best current explanation when information is incomplete.

## When to Use
- Error diagnosis, incident analysis, why-is-this-happening

## When Not to Use
- Full premises that allow pure deduction

## Workflow
1. List observations exactly.\n2. Generate 2–4 candidate explanations.\n3. Note what each explains and misses.\n4. Rank by power, simplicity, consistency.\n5. State leading hypothesis + needed evidence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
