---
name: search-then-reason
description: Gather external or retrieved evidence first, then reason only on that evidence. USE FOR knowledge-intensive questions. DO NOT USE when pure parametric knowledge is enough.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive, deductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational]
---

# search-then-reason

## Purpose
Ground reasoning in retrieved evidence to reduce hallucination.

## When to Use
- Questions needing up-to-date or document-grounded answers

## When Not to Use
- Pure logic/math that needs no retrieval

## Workflow
1. Formulate search/retrieval queries.\n2. Collect relevant snippets/sources.\n3. Reason strictly from those sources.\n4. Cite which source supports each key claim.\n5. Mark any claim not supported by retrieved evidence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
