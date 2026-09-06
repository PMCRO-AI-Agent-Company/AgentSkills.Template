# Declarative Reasoning-Strategy Template

**Status:** Proven prototype (2 of 35 strategies), not yet applied to the full catalog.
**Purpose:** Apply the same "declare once, generate the projection" principle as
`DECLARATIVE-GENERATIVE-AGENT-TEMPLATE.md`, to a genuinely different file convention:
`plugins/pmcro-reasoning-strategy/agents/<id>.md`.

## Why this is a separate system, not an extension of AgentScaffoldSpec

`AgentScaffoldSpec` (the existing declarative system) renders `.agents/skills/<id>/SKILL.md`
(Agent Skills convention) and `src/Agents/<id>/*.cs` (MAF-inline). A reasoning strategy is a
different shape entirely: no `skills`/`packaging` list, no capability resolution - instead
`family`, `logical_paradigms`/`operational_methods`/`domain_capabilities`, and a fixed
Purpose/When-to-Use/When-Not-to-Use/Workflow/Validation/Output body. Forcing this into
`scaffold.py`'s `render_agentskills()` would mean branching one function on incompatible
shapes. A small, dedicated generator is the correct scope boundary.

## What was verified, not assumed

Read `chain-of-thought.md` and `self-refine.md` (2 of the 34 non-selector strategies) in
full before writing anything. Confirmed:

- `laws` and `permissions` (`may`/`mayNot`) are byte-identical across both files - and,
  per `selector.md`'s own frontmatter, the same `mayNot` list minus
  `select-reasoning-strategy` plus `apply-reasoning-strategy` swapped, consistent with
  "every strategy may apply itself, may not select for others; the selector is the
  inverse." Not verified against all 34 - a real risk if this generator is ever pointed
  at the full catalog: confirm this holds for all of them first, don't assume from 2.
- The body has an identical six-section skeleton in both files, in the same order.
- **One real assumption that turned out to be wrong, caught by the round-trip check
  itself, not asserted away:** the `## Output` section's parenthetical describing what a
  `steps` entry means is *per-strategy content*, not boilerplate -
  chain-of-thought says "one entry per step actually performed", self-refine says "each
  draft/critique/revision cycle". The first draft of this generator hardcoded the
  chain-of-thought wording as a universal default; the self-refine round-trip diff caught
  the mismatch immediately. The schema and generator now require a `steps_description`
  field per spec instead. This is exactly the kind of thing "prove it before claiming it
  works" catches that "it looks obviously mechanical" does not.

## Round-trip proof

`plugins/pmcro-reasoning-strategy/specs/{chain-of-thought,self-refine}.spec.yaml`, rendered
via `plugins/pmcro-reasoning-strategy/scripts/render_strategy.py` and diffed against the
real committed files. Remaining diff on both, after the `steps_description` fix:

1. The generated file omits the one-time `Migrated from ... (v1.0.0) into the single-file
   reasoning-strategy/ convention.` line. Intentional: that sentence describes a specific
   historical event (the 2026-09-05 migration), not a property of the strategy itself. A
   repeatable generator re-run in the future should not keep re-asserting a one-time
   migration note. If this generator is ever used to *regenerate* the real files, that
   line would need to move to a git commit message / trail record instead of living in
   the file body.
2. Prose line-wrap width differs (hand-written files wrap around ~76 columns; the
   generator emits single logical lines per paragraph/step). No semantic difference -
   Markdown renders a soft-wrapped paragraph identically to one long line. Not fixed,
   because matching hand-chosen wrap points mechanically isn't worth the complexity for a
   cosmetic-only difference; flagging it here rather than silently ignoring it.

No other differences. This is real, checked evidence for both strategies - not "structure
looks similar so it probably works."

## Explicitly not done this trail

- **Not regenerating any of the 34 real, currently-working strategy files.** This trail
  only proves the generator against two files via a side-by-side diff; it does not
  touch `plugins/pmcro-reasoning-strategy/agents/` itself.
- **Not writing specs for the remaining 32 strategies.** Two was enough to prove (and, in
  the `steps_description` case, disprove a wrong assumption about) the pattern. Writing
  32 more specs is mechanical reverse-engineering work, not a design question - a good
  next increment, not a design risk.
- **Not touching `selector.md`.** Its Families-by-family list *is* mechanically derivable
  from the full spec set once all 35 specs exist (group by `family`, preserve the same
  ordering `CATALOG.md` already uses). Its Quick Selection Guide table ("Situation ->
  Start with") is curated editorial judgment, not a projection of any single spec's
  fields - generating it would need an explicit new field (e.g. `quick_selection_hints:
  [{situation, note}]` per spec) and a decision about whether cross-strategy editorial
  judgment belongs in individual specs at all. Left as an open question, not decided here.

## Next step, if this is worth continuing

1. Verify the `laws`/`permissions` invariant against all 34 non-selector files (not just
   the 2 read so far) before treating it as universal.
2. Write specs for the remaining 32 strategies, reverse-engineered from their real files
   the same way, with the same before/after diff discipline used here - not assumed
   correct because the pattern held for 2.
3. Only after 1-2, decide whether to actually regenerate the real files from specs (moving
   the one-time migration note out of the file body per the point above) or keep the specs
   as a parallel, currently-unused declarative source.
