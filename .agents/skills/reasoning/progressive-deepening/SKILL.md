---
name: progressive-deepening
description: Start shallow, then deepen only the promising branches. USE FOR large search spaces. DO NOT USE for problems that need full exhaustive detail immediately.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive, deductive]
    operational_methods: [branching_search, test_time_compute]
    domain_capabilities: [strategic_agentic]
---

# progressive-deepening

## Purpose
Allocate depth where it pays off instead of uniform deep analysis.

## When to Use
- Broad design spaces, research, option evaluation

## When Not to Use
- Problems that require uniform full detail on every part

## Workflow
1. Survey the space at a shallow level.\n2. Identify the most promising 1–3 branches.\n3. Deepen only those branches.\n4. Reassess and deepen further if needed.\n5. Deliver the best-supported conclusion.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
