---
name: plan-and-execute
description: Create an explicit plan first, then execute it step by step. USE FOR multi-step tasks that need a roadmap. DO NOT USE for single-step answers.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, abductive]
    operational_methods: [linear_cot, strategic_agentic]
    domain_capabilities: [strategic_agentic]
---

# plan-and-execute

## Purpose
Separate planning from execution so the approach is visible and adjustable.

## When to Use
- Multi-step projects, coding tasks, research workflows

## When Not to Use
- Single-shot factual questions

## Workflow
1. Restate the goal and constraints.\n2. Produce a numbered plan of concrete steps.\n3. Execute steps in order, recording results.\n4. Adjust the plan only when a step fails or new information appears.\n5. Summarize outcome against the original plan.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
