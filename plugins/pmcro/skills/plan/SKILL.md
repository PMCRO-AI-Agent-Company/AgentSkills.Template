---
name: plan
description: Produce a PlanFrame (goal, ordered steps, success criteria, out-of-scope) from an Orchestrator-opened cycle, grounded in validated/dated resources. USE FOR turning an opened cycle into an executable plan. DO NOT USE for execution, verification, or disposition.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
---

# plan

## Purpose

Turn the current cycle's seed intent (or Chief-governed IntentFrame) into a
`PlanFrame`: the bare minimum plan needed to satisfy real, checkable success
criteria - never more. Propose only; do not execute.

## When to Use

- Immediately after Orchestrator's OPEN frame, once per cycle

## When Not to Use

- Executing steps (Maker's job)
- Judging whether Maker's output passed (Checker's job)
- Issuing a disposition or sealing (Reflector's job)

## Workflow

1. Read the Orchestrator's `01-orchestrate.jsonl` OPEN frame for this trail.
2. Ground every step and success criterion in currently-verified resources
   (live filesystem/config state, not recalled/assumed prior state -
   L-RESEARCH: version-sensitive decisions require current authoritative
   evidence).
3. Write `.pmcro/trails/<trail_id>/02-plan.json`:
   `{"role":"planner","goal","success_criteria":[...],"steps":[{"id","action"}...]}`.
4. Keep steps minimal - each step must be traceable to a success criterion.
   Do not add speculative or nice-to-have steps.
5. Hand off to Maker. Do not execute any step yourself.

## Output Shape

```json
{
  "role": "planner",
  "goal": "<one-sentence outcome>",
  "success_criteria": ["<checkable condition>", "..."],
  "steps": [{"id": "S1", "action": "<concrete, single-owner action>"}]
}
```

## Constraints

- `may` (per `.pmcro/policies/permissions.yaml`): propose-plan,
  define-success-criteria, select-validated-resource.
- `mayNot`: execute-provider-action, issue-disposition, seal-cycle.
- A missing capability or unconfirmed provider returns null/ESCALATE - never
  invent a result, resource, or capability (L-CAPABILITY).
- Follow L-EVIDENCE, L-RESEARCH, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
