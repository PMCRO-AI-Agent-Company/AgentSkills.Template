---
name: react-loop
description: Reason-Act-Observe loop for tool-using tasks. USE FOR tools/search/environment. DO NOT USE for pure offline reasoning.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [abductive, deductive]
    operational_methods: [iterative_self_reflective]
    domain_capabilities: [strategic_agentic]
---

# react-loop

## Purpose
Interleave thinking, actions, and real observations until the goal is met.

## When to Use
- Tool use, web search, code execution, APIs

## When Not to Use
- Pure reasoning with no external actions

## Workflow
1. Thought: current sub-goal.\n2. Action: one concrete tool/command.\n3. Observation: record real result.\n4. Repeat until done or limit hit.\n5. Final answer grounded only in observations.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work
