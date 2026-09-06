---
name: goal-regression
description: Regress goals through operators until reaching achievable starting conditions (classic planning). USE FOR action planning. DO NOT USE for pure descriptive questions.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive]
    operational_methods: [branching_search, linear_cot]
    domain_capabilities: [strategic_agentic]
---

# goal-regression

## Purpose
Connect a high-level goal to concrete actions via goal regression.

## When to Use
- Action planning, procedure synthesis, agent task planning

## When Not to Use
- Descriptive or explanatory questions with no actions

## Workflow
1. State the top-level goal.\n2. Choose an operator that achieves it.\n3. Regress to the operator’s preconditions.\n4. Repeat until preconditions are currently true.\n5. Reverse into an executable action sequence.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
