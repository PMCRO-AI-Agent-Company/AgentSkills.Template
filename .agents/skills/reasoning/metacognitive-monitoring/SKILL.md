---
name: metacognitive-monitoring
description: Track confidence and uncertainty explicitly while solving. USE FOR high-stakes or ambiguous answers. DO NOT USE when false confidence is required.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive, inductive]
    operational_methods: [iterative_self_reflective]
    domain_capabilities: [strategic_agentic, common_sense]
---

# metacognitive-monitoring

## Purpose
Make the model’s own uncertainty visible and actionable.

## When to Use
- High-stakes decisions, ambiguous evidence, advice under uncertainty

## When Not to Use
- Tasks where a single confident answer is mandatory and evidence is clear

## Workflow
1. Attempt the solution.\n2. Rate confidence (low/medium/high) with reasons.\n3. List what would raise or lower confidence.\n4. If confidence is low, propose what information is still needed.\n5. Deliver answer together with the confidence statement.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
