---
name: self-refine
description: Draft, critique, then revise iteratively. USE FOR writing, analysis, or any output that benefits from explicit self-criticism. DO NOT USE for simple lookups or strict single-pass constraints.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [inductive, abductive]
    operational_methods: [iterative_self_reflective]
    domain_capabilities: [multi_hop_relational, common_sense]
---

# self-refine

## Purpose
Produce an initial draft, explicitly critique it against defined criteria, then revise until quality thresholds are met.

## When to Use
- Writing, summarization, analysis, or code generation where quality matters
- High-stakes outputs that require explicit checking before delivery

## When Not to Use
- Simple factual lookups with deterministic answers
- Contexts where multiple passes are not permitted or too costly

## Workflow
1. Restate the goal and success criteria.
2. Produce an initial draft.
3. Critique the draft: identify specific weaknesses, gaps, or errors against the criteria.
4. Revise the draft to address each critique point.
5. Repeat steps 3–4 until no critical issues remain or a maximum iteration count is reached.
6. Deliver the final revised output.

## Validation
- At least one critique-and-revise cycle was completed
- Each critique point was addressed in the revision
- Final output satisfies all stated success criteria

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
