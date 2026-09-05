---
name: backward-chaining
description: Start from the desired goal and work backward to required premises or actions. USE FOR goal-driven planning. DO NOT USE when only forward data is available.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive]
    operational_methods: [linear_cot, branching_search]
    domain_capabilities: [strategic_agentic, mathematical_symbolic]
---

# backward-chaining

## Purpose
Derive what must be true or done by working from the goal backward.

## When to Use
- Planning to a known goal, proof-style tasks, requirements derivation

## When Not to Use
- Open exploration with no fixed goal

## Workflow
1. State the goal precisely.\n2. Ask what must be true immediately before the goal.\n3. Recursively expand prerequisites.\n4. Stop at known facts or feasible actions.\n5. Reverse the chain into a forward plan.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
