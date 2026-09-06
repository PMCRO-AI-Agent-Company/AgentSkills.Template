---
name: select-reasoning-strategy
description: Given a task description and an optional allowed-families filter, recommend one reasoning strategy id from the pmcro-reasoning-strategy catalog. USE FOR any caller (a pmcro-csuite Chief, Orchestrator, or a human) that needs to pick a strategy before applying one. DO NOT USE to apply the strategy itself.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: DOMAIN
  capability_class: DOMAIN
---

# select-reasoning-strategy

## Purpose

Canonical, parameterized selector for the whole `pmcro-reasoning-strategy`
catalog. Replaces per-caller duplicated copies of this logic: any plugin
(most notably each `pmcro-csuite` Chief) calls this one skill instead of
carrying its own.

## Args

- `task_description` (string, required) — the seed or sub-task to route.
- `allowed_families` (array of strings, optional) — narrows the candidate
  set to specific families (see `agents/selector.md`'s Families list). If
  omitted, all 35 strategies are eligible.
- `caller_id` (string, optional) — id of the calling Chief or plugin, for
  the rationale trail only. Never changes the selection logic itself.

## When to Use

- Any plugin needs a reasoning strategy id and does not want to duplicate
  the selection logic locally

## When Not to Use

- Applying the selected strategy (use `apply-reasoning-strategy`)
- Overriding a strategy already locked into an open trail

## Workflow

1. Read `task_description` and, if present, `allowed_families`.
2. Delegate matching to `agents/selector.md`'s Quick Selection Guide,
   restricted to `allowed_families` when given.
3. Verify the selected id exists as a file under `agents/`. If not, fall
   back to `chain-of-thought` and note the fallback in `rationale`.
4. Return a `StrategySelectionFrame` (see
   `schemas/strategy-selection-frame.schema.json`): `selected_strategy`,
   `family`, `reasoning_catalog_path`, `rationale`, optionally
   `alternatives_considered`.

## Constraints

- Only return strategy ids that exist as files under `agents/`.
- Never apply the strategy — selection only.
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
