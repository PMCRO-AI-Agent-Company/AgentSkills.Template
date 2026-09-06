---
name: hypothesis-testing
description: Form hypotheses and state what evidence would confirm or refute them. USE FOR investigative questions. DO NOT USE for pure generation.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive, deductive]
    operational_methods: [branching_search, iterative_self_reflective]
    domain_capabilities: [multi_hop_relational, strategic_agentic]
---

# hypothesis-testing

## Purpose
Treat claims as testable hypotheses rather than assertions.

## When to Use
- Research, debugging, causal questions, uncertain claims

## When Not to Use
- Tasks that only need a direct procedural answer

## Workflow
1. State the question.\n2. Propose 2–3 competing hypotheses.\n3. For each, list confirming and disconfirming evidence.\n4. Evaluate against available evidence.\n5. Rank hypotheses and state what would change the ranking.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
