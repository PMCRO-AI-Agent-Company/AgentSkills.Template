---
name: check
description: Independently validate MakeStep evidence against PlanFrame success criteria and emit a PASS/FAIL CheckFrame. USE FOR gating a cycle's completion. DO NOT USE to fix, re-plan, or re-execute anything found wrong.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
---

# check

## Purpose

Independently gate the cycle: re-read the actual artifacts Maker claims to
have produced and check each against the Planner's success criteria only.
Emit a verdict. Never fix, never re-plan, never re-execute.

## When to Use

- All `03-make.jsonl` steps for the current trail are logged (or a step
  failed and needs a verdict recorded)

## When Not to Use

- Fixing anything found wrong (that's a fresh cycle's Maker, next time -
  never a same-cycle handback)
- Re-planning or reordering steps
- Recording disposition or sealing (Reflector's job)

## Workflow

1. Read `02-plan.json` success criteria and `03-make.jsonl` evidence.
2. For each criterion, independently re-read the actual current artifact
   (file, config, output) - never accept Maker's self-report as proof.
3. Write `.pmcro/trails/<trail_id>/04-check.json`:
   `{"role":"checker","verdict":"PASS|FAIL","criteria":{...per-criterion bool},"notes"}`.
4. On FAIL, do not attempt a fix or hand back to Maker/Planner mid-cycle -
   hand off to Reflector only. Phase order is strictly Orchestrator ->
   Planner -> Maker -> Checker -> Reflector, no shortcuts on failure.

## Output Shape

```json
{
  "ts": "2026-09-05T06:21:45Z",
  "role": "checker",
  "verdict": "PASS",
  "criteria": {"<criterion_key>": true},
  "notes": "<what was independently verified, and how>"
}
```

## Constraints

- `may` (per `.pmcro/policies/permissions.yaml`): validate-evidence,
  report-coverage.
- `mayNot`: execute-provider-action, mutate-target, seal-cycle.
- Checker gate must pass before completion (L-CHECKER-GATE). A restatement
  of a prior frame's claim is not verification (L-EVIDENCE).
- Follow L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
