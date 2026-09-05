---
name: least-to-most
description: Decompose into easier sub-problems and solve in order. USE FOR complex multi-hop questions. DO NOT USE for atomic questions.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive]
    operational_methods: [linear_cot, branching_search]
    domain_capabilities: [strategic_agentic, multi_hop_relational]
---

# least-to-most

## Purpose
Reduce difficulty by solving easier sub-questions that build toward the target.

## When to Use
- Multi-hop questions, layered analysis, complex planning

## When Not to Use
- Single-hop factual or arithmetic questions

## Workflow
1. State the hard target.\n2. List ordered easier sub-questions.\n3. Answer easiest → hardest, using prior answers.\n4. Only then solve the original.\n5. Make dependencies explicit.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
