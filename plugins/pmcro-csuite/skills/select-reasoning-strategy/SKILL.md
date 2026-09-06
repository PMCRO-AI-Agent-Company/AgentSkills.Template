---
name: select-reasoning-strategy
description: Parameterized version of the 12 near-identical per-Chief select-reasoning-strategy skills. Consults a given Chief's omode entry and delegates matching to pmcro-omode. USE BEFORE govern-domain-intent produces its frame. DO NOT invent strategy ids not present in the reasoning catalog.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: DOMAIN
  capability_class: DOMAIN
---

# select-reasoning-strategy

## Purpose

Single parameterized replacement for what used to be 12 duplicated
per-Chief copies of this skill (one per `pmcro-chief-*` plugin). Given a
Chief id and a seed, returns the best reasoning strategy id.

## Args

- `chief_id` (string, required) — one of `cco, cdo, ceo, cfo, chro, ciso,
  clo, cmo, coo, cpo, cro, cto` (matches a file under `agents/`).
- `seed` (string, required) — the incoming task description.

## When to Use

- Called by `govern-domain-intent` before producing that Chief's
  `<Domain>IntentFrame`

## When Not to Use

- Overriding a strategy already locked into an open trail

## Workflow

1. Read `agents/<chief_id>.md` for that Chief's `reasoning.allowed_families`
   and its Reasoning Modes table.
2. Read `assets/<chief_id>.yaml` for the same triggers in structured form.
3. Call `pmcro-omode:select-reasoning-strategy` with
   `task_description: seed`, `allowed_families` from step 1, and
   `caller_id: chief_id`.
4. Return that call's `StrategySelectionFrame` unchanged.

## Constraints

- Only return strategy ids that pmcro-omode confirms exist.
- Do not mutate `assets/<chief_id>.yaml` or any agent file.
- Follow L-EVIDENCE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT.
