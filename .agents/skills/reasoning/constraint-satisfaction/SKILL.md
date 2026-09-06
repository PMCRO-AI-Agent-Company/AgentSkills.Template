---
name: constraint-satisfaction
description: Enumerate constraints first, then search for solutions that satisfy all of them. USE FOR problems with hard requirements. DO NOT USE for unconstrained creative tasks.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive]
    operational_methods: [branching_search, linear_cot]
    domain_capabilities: [mathematical_symbolic, strategic_agentic]
---

# constraint-satisfaction

## Purpose
Make constraints explicit so invalid candidates are eliminated early.

## When to Use
- Scheduling, configuration, design under requirements, puzzles

## When Not to Use
- Open-ended creative generation with no hard constraints

## Workflow
1. List all hard constraints.\n2. List soft preferences separately.\n3. Generate candidates that meet hard constraints.\n4. Rank by soft preferences.\n5. Return the best feasible solution and note any trade-offs.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
