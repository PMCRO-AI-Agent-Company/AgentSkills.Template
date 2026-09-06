---
name: multi-agent-critique
description: Simulate multiple perspectives that critique each other before answering. USE FOR high-stakes or biased-risk answers. DO NOT USE for simple lookups.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive, analogical]
    operational_methods: [branching_search, iterative_self_reflective]
    domain_capabilities: [strategic_agentic]
---

# multi-agent-critique

## Purpose
Reduce single-viewpoint blind spots by adversarial or complementary perspectives.

## When to Use
- Policy, safety, design review, contested analysis

## When Not to Use
- Simple factual or procedural questions

## Workflow
1. Define 2–3 named perspectives (e.g. optimist, skeptic, operator).\n2. Let each produce an initial view.\n3. Let each critique the others.\n4. Synthesize a balanced conclusion.\n5. Record residual disagreements.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
