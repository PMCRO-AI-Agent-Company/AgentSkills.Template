---
name: forward-chaining
description: Start from known facts and apply rules forward until a goal or fixed point. USE FOR data-driven inference. DO NOT USE when the goal should drive the search.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, inductive]
    operational_methods: [linear_cot]
    domain_capabilities: [mathematical_symbolic, multi_hop_relational]
---

# forward-chaining

## Purpose
Derive consequences systematically from what is already known.

## When to Use
- Rule application, data-driven conclusions, simulation of effects

## When Not to Use
- Goal-directed tasks better solved by working backward

## Workflow
1. List known facts/rules.\n2. Apply applicable rules to derive new facts.\n3. Repeat until goal reached or no new facts.\n4. Trace the derivation path.\n5. State conclusions with supporting chain.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
