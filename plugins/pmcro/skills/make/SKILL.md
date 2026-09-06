---
name: make
description: Execute one approved PlanFrame step at a time and emit execution evidence. USE FOR carrying out a single Planner step. DO NOT USE for planning, verification, or disposition, and never for a TYPE1 mutation without recorded human approval.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
---

# make

## Purpose

Execute exactly one `PlanFrame` step and produce a `MakeStep` evidence
record. Never plans, never judges its own success, never seals.

## When to Use

- A `PlanFrame` step (`.pmcro/trails/<trail_id>/02-plan.json`) is ready to
  execute and has not yet produced a MakeStep

## When Not to Use

- Deciding the plan or reordering steps (Planner's job)
- Judging whether the result actually passes (Checker's job)
- Any TYPE1 mutation (write/create/delete/move/commit/push) without a
  recorded human approval in this session

## Workflow

1. Read the next unexecuted step from `02-plan.json`.
2. If the step is a TYPE1 mutation, confirm explicit human approval is
   recorded for this cycle before acting - otherwise return `ESCALATE`, do
   not execute.
3. Execute the single step using the smallest suitable tool/capability
   (`.pmcro/capabilities/`, `.pmcro/providers/`) - never invent an
   integration for a missing one.
4. Append one line to `.pmcro/trails/<trail_id>/03-make.jsonl`:
   `{"ts","role":"maker","step":"<id>","result":"ok|fail","artifact","evidence"}`.
5. Do not proceed to Checker yourself - Checker picks up independently once
   all steps are logged (or a step fails).

## Output Shape

```json
{"ts":"2026-09-05T06:21:45Z","role":"maker","step":"S1","result":"ok","artifact":"<path or id>","evidence":"<what proves this actually happened>"}
```

## Constraints

- `may` (per `.pmcro/policies/permissions.yaml`): execute-approved-action,
  emit-execution-evidence.
- `mayNot`: approve-own-action, verify-outcome, seal-cycle.
- Completion without evidence is not completion (L-EVIDENCE). A missing
  capability returns null/ESCALATE, never a fabricated result.
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
