---
name: reflect
description: Record disposition, promote Earned Constraints every cycle, optionally produce the next seed intent, and seal the trail. USE FOR closing out a cycle after Checker's verdict. DO NOT USE to fix Checker-found issues or to rewrite laws.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
---

# reflect

## Purpose

Close the cycle: record disposition from Checker's verdict, promote any
Earned Constraint learned this cycle (unconditionally, every cycle - not
only on PASS), optionally produce the next seed intent, and seal the trail.
Sole role permitted to seal. Also materializes the trail record itself
(this folds in the scope of the deprecated standalone `pmcro-trail` role -
see `.pmcro/directory/agents.yaml`).

## When to Use

- Exactly once, after Checker emits `04-check.json` for the current trail

## When Not to Use

- Fixing anything Checker found (that's a fresh cycle, dispatched by
  Orchestrator to Planner again - never same-cycle)
- Rewriting laws or policies
- Executing provider actions of any kind

## Workflow

1. Read `04-check.json`'s verdict for this trail.
2. Determine disposition: `SEAL` on PASS; on FAIL, record `RetryContext`
   and prepare a fresh next seed rather than sealing a failed cycle as done.
3. Promote Earned Constraints: state what was learned this cycle as a
   durable, generalizable constraint (even a small one) - this step is
   unconditional, every cycle, not gated on PASS. Write it under
   `.pmcro/constraints/` (or append to the cycle's Earned Constraint record
   if the convention there already exists) so the next cycle inherits it
   instead of starting cold.
4. If another cycle is warranted, synthesize the next seed intent from the
   Goal, this cycle's frames, evidence, and any failures/constraints - never
   invented without evidence.
5. Write `.pmcro/trails/<trail_id>/05-reflect.json`, then materialize/seal
   `.pmcro/trails/<trail_id>/trail.json` (`status: sealed`, `sealed_at`).
6. Update `.pmcro/queue/` (mark item done/blocked) and
   `.pmcro/state/active_trail_id.txt` as needed.

## Output Shape

```json
{
  "ts": "2026-09-05T06:21:45Z",
  "role": "reflector",
  "disposition": "SEAL",
  "summary": "<what happened this cycle>",
  "earned_constraints": ["<durable lesson generalized from this cycle>"],
  "next_seed": null,
  "stop_reason": "<why this is the natural stopping point, or null>",
  "sealed": true
}
```

## Constraints

- `may` (per `.pmcro/policies/permissions.yaml`): record-disposition,
  propose-earned-constraint, propose-next-seed, seal-cycle.
- `mayNot`: rewrite-laws, execute-provider-action.
- Sealed trails are immutable - corrections use a new trail that may
  reference the earlier one via a next seed, never an edit to a sealed one.
- Follow L-EVIDENCE, L-CHECKER-GATE, L-STATE-MEMORY, L-PLUGIN-ISOLATION,
  L-OUTPUT-CONTRACT.
