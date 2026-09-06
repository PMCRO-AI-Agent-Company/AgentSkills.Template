---
name: recursive-summarization
description: Summarize chunks, then summarize the summaries (hierarchical compression). USE FOR long contexts. DO NOT USE for short inputs.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational]
---

# recursive-summarization

## Purpose
Preserve important information while compressing long material hierarchically.

## When to Use
- Long documents, large logs, multi-file summaries

## When Not to Use
- Short texts that fit in one pass

## Workflow
1. Split material into coherent chunks.\n2. Summarize each chunk.\n3. Summarize the chunk summaries.\n4. Optionally repeat another level.\n5. Produce final summary with traceable key points.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
