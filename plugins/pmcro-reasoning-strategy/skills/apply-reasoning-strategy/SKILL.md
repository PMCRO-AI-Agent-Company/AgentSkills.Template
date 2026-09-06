---
name: apply-reasoning-strategy
description: Apply a named reasoning strategy from the pmcro-reasoning-strategy catalog to a given input and return a ReasoningTraceFrame. USE FOR executing a strategy once select-reasoning-strategy (or a caller) has already chosen one. DO NOT USE to pick which strategy to use.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: DOMAIN
  capability_class: DOMAIN
---

# apply-reasoning-strategy

## Purpose

Dispatch to exactly one of the 35 strategy agents under `agents/` and run
its Workflow against the given input, producing a `ReasoningTraceFrame`.

## Args

- `strategy_id` (string, required) — must match a filename under `agents/`
  (e.g. `abductive-diagnosis`, `tree-of-thoughts`).
- `input` (string, required) — the task/content to reason over.
- `context` (object, optional) — any extra grounding the strategy's
  Workflow calls for (e.g. prior steps, constraints, evidence already
  gathered).

## When to Use

- A `strategy_id` has already been chosen (by `select-reasoning-strategy`
  or supplied directly by the caller) and needs to be executed

## When Not to Use

- Choosing which strategy to use (use `select-reasoning-strategy`)

## Workflow

1. Verify `strategy_id` exists as a file under `agents/`. If it does not,
   return a governed rejection — do not invent or substitute a strategy.
2. Load that agent file's Purpose / When to Use / When Not to Use /
   Workflow / Validation sections.
3. Run the Workflow steps against `input` and `context`.
4. Run the Validation checklist before returning.
5. Return a `ReasoningTraceFrame` (see
   `schemas/reasoning-trace-frame.schema.json`): `strategy_id`, `steps`
   (one entry per workflow step actually performed), `result`, and
   `confidence`/`validation` where the strategy defines them.

## Constraints

- Never substitute a different strategy than the one requested.
- Never skip that strategy's own Validation checklist.
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
