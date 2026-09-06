---
name: dual-process
description: Fast intuitive answer first, then slow deliberate check (System-1 then System-2). USE FOR problems where intuition helps but must be verified. DO NOT USE when only careful analysis is appropriate.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive, deductive]
    operational_methods: [linear_cot, iterative_self_reflective]
    domain_capabilities: [common_sense, mathematical_symbolic]
---

# dual-process

## Purpose
Combine speed of intuition with reliability of deliberate checking.

## When to Use
- Everyday problems, estimates, first-pass diagnoses

## When Not to Use
- Safety-critical tasks that forbid intuitive first answers

## Workflow
1. Give a fast intuitive answer (mark it as provisional).\n2. Switch to slow analysis: assumptions, steps, checks.\n3. Compare intuitive vs deliberate results.\n4. Prefer the deliberate result when they conflict.\n5. Report both if educational.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
