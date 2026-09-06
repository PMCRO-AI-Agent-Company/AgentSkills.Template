---
name: orchestrate
description: Open a trail cycle for a seed intent, route to a Chief persona for domain scope when applicable, and dispatch to Planner. USE FOR opening/claiming any PMCRO cycle. DO NOT USE for planning, execution, checking, or sealing - those belong to other roles.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: GOVERNANCE
  capability_class: LIFECYCLE
---

# orchestrate

## Purpose

Sole dispatch authority for the PMCR-O cycle. Receives a seed intent (human
message, queued item, or a Reflector-produced next seed), mints or links a
trail, logs the OPEN frame, and hands off to Planner. Never does domain work.

## When to Use

- A new human seed intent needs a cycle opened
- The queue has a claimable item (see `.pmcro/queue/`)
- Reflector produced a next seed and another cycle is warranted

## When Not to Use

- Planning, executing, checking, or sealing a cycle - those are Planner /
  Maker / Checker / Reflector's jobs, never Orchestrator's
- Domain implementation of any kind (L-ORCHESTRATION: orchestrator owns
  routing, not domain implementation)

## Workflow

1. Preserve the raw human/queue input verbatim as Messy Seed Intent - never
   silently rephrase it into a claimed verbatim quote.
2. Read `.pmcro/state/active_trail_id.txt`, `.pmcro/queue/`, and
   `.pmcro/laws/laws.yaml` before acting.
3. If the seed touches a specific domain, route to the matching Chief
   persona (`.pmcro/directory/agents.yaml`, `kind: persona`) to get its
   governed `<Domain>IntentFrame` - the Chief supplies scope only, it does
   not run its own loop (one shared cycle, always).
4. Mint a new trail (Class B, per `manifest.yaml`) or link to an existing
   open one. Write `.pmcro/trails/<trail_id>/01-orchestrate.jsonl`:
   `{"ts", "role":"orchestrator", "action":"OPEN", "trail_id", "seed"}`.
5. Update `.pmcro/state/active_trail_id.txt` to the new/linked trail id.
6. Hand off to Planner. Do not execute, plan, or judge anything further
   this turn.

## Output Shape

```json
{"ts":"2026-09-05T06:20:40Z","role":"orchestrator","action":"OPEN","trail_id":"<uuid>","seed":"<verbatim or Chief-governed intent>"}
```

## Constraints

- `mayNot` (per `.pmcro/policies/permissions.yaml`): execute-provider-action,
  verify-outcome, mutate-governed-artifact, seal-cycle.
- Priority scale for queue claims: `0 stop-the-line -> 1 CEO/CoS -> 2 domain
  critical -> 3 normal -> 4 backlog`. Never invent a priority; only
  Reflector policy or CEO/CoS may reorder.
- A failed cycle (Checker `fail`) is never handed back mid-cycle. Reflector
  closes it and Orchestrator opens a fresh cycle next, dispatched to
  Planner again from the top.
- Follow L-EVIDENCE, L-ORCHESTRATION, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
