---
name: decomposition-recomposition
description: Break a problem into parts, solve parts, then recompose the whole. USE FOR large or composite problems. DO NOT USE for already atomic tasks.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive]
    operational_methods: [linear_cot, branching_search]
    domain_capabilities: [strategic_agentic, multi_hop_relational]
---

# decomposition-recomposition

## Purpose
Manage complexity by solving modular pieces and carefully integrating them.

## When to Use
- Large analyses, system design, multi-part questions

## When Not to Use
- Single atomic questions

## Workflow
1. Decompose into non-overlapping parts.\n2. Solve each part independently.\n3. Check interfaces/dependencies between parts.\n4. Recompose into a coherent whole.\n5. Validate the integrated result.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
