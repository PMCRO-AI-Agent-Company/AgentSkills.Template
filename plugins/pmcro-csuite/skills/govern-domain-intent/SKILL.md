---
name: govern-domain-intent
description: Parameterized version of the 12 per-Chief govern-<domain>-intent skills. Turns a seed into a governed <Domain>IntentFrame for the named Chief, suitable for Planner handoff. USE FOR any single-domain or cross-domain request that names (or implies) a specific Chief. DO NOT USE for core lifecycle operations.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: DOMAIN
  capability_class: DOMAIN
---

# govern-domain-intent

## Purpose

Single parameterized replacement for what used to be 12 duplicated
per-Chief `govern-<domain>-intent` skills. Given a Chief id and a seed,
produces that Chief's governed intent frame, ready for Planner handoff.

## Args

- `chief_id` (string, required) — one of `cco, cdo, ceo, cfo, chro, ciso,
  clo, cmo, coo, cpo, cro, cto` (matches a file under `agents/`).
- `seed` (string, required) — the incoming request.

## When to Use

- An incoming request touches a specific Chief's domain, before handing
  off to the Planner for PMCR cycle execution

## When Not to Use

- Core lifecycle operations (orchestrate / plan / make / check / reflect)
- A request spanning multiple Chiefs with no single owner — route each
  affected domain separately, or escalate to `ceo`

## Workflow

1. Read `agents/<chief_id>.md` for that Chief's System Prompt and its
   frame's field shape (e.g. `stakeholders`, or CEO's
   `cross_chief_dependencies`, or CTO's `capability_constraints` /
   `architecture_decisions`).
2. Call `select-reasoning-strategy` with `chief_id` and `seed`.
3. Produce the `<Domain>IntentFrame` per `schemas/chief-intent-frame.schema.json`,
   populating `goal`, `stakeholders` (or that Chief's equivalent field),
   `success_criteria`, `out_of_scope`, `selected_reasoning_strategy`
   (from step 2), and `selected_frame_shape`.
4. Emit the frame as a governed result satisfying `L-OUTPUT-CONTRACT`.
5. Hand off to Orchestrator for cycle opening.

## Constraints

- Never invent domain findings, metrics, or commitments without evidence
  (see the Constraints section of the relevant `agents/<chief_id>.md`).
- Domain execution remains with Maker and Checker; this skill governs
  intent only.
- Follow L-EVIDENCE, L-CHECKER-GATE, L-OUTPUT-CONTRACT.
