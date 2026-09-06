# NOTE — Federation Board, original vision (captured verbatim-ish from Shawn)

**Status: NOT a decision. NOT an ADR. Do not build from this alone.**
Captured 2026-09-06 from a live, unstructured voice note so it isn't lost
before the next real discussion ("we can worry about that another time" -
Shawn's own words). This directly contradicts
`ADR-federation-csuite-decision-2026-09-06.md`'s resolution (leave
Federation as unused legacy vocabulary, C-Suite stays as-is) - see
"Tension with the existing ADR" below. A future session must not silently
pick a side; surface this to Shawn again if it comes up before he's
weighed in properly.

## What Shawn described

Federation Board was never meant to be a static classifier that runs once
and hands off. The mechanism was:

- A raw, "messy seed" intent enters the Federation Board, not the
  Orchestrator directly.
- Agents refine it iteratively through explicit, addressed, natural-language
  references to each other - e.g. Maker saying "Hey Planner, ..." - rather
  than a fixed pipeline call. The reference itself IS the dependency edge:
  "when you see that reference, it's like a dependency... a language type
  of thing." The chain/workflow still exists, but it's expressed and
  discovered through language, not hard-wired routing.
- This refinement loops on the messy seed - "keep iterating over that messy
  seed intent" - until it's resolved enough to pass onward.
- The one hard invariant Shawn repeated: Federation Board's iteration
  "never touches the orchestrator" while it's still messy. Orchestrator
  only sees the resolved result.

This is a materially different shape from what `plugins/pmcro-csuite/`
actually does today (a Chief classifies domain + selects a reasoning
strategy in one pass, then hands a governed `IntentFrame` to Orchestrator).
Shawn's description is an iterative, self-referential, multi-turn
negotiation among agents *before* anything domain-scoped is even settled -
closer to a discussion than a classification.

## Tension with the existing ADR

`ADR-federation-csuite-decision-2026-09-06.md` concluded "no rename, no new
artifact, C-Suite already fills this role" and recorded that as decided
"on explicit delegated authority from the repo owner." The
increment-1/2 sessions on 2026-09-06 already flagged that authority claim
as unverifiable from inside a session and worth Shawn's own confirmation.
This note is evidence pointing the other way: Shawn's own live description
of Federation Board does not match "C-Suite already does this" - the
C-Suite layer doesn't iterate on a messy seed through inter-agent language
references at all. Whether that means the ADR's authority claim was wrong,
or Shawn's thinking has evolved since whatever session produced it, or
both are compatible in some way not yet spelled out - none of that is
resolved here. Don't silently supersede the ADR from this note alone.

## Adjacent ideas mentioned in the same note (not decisions, just recorded so they aren't lost)

- **Trail replay / "trail player":** a UI concept - sealed trails (or even
  simulated ones) as replayable artifacts, not just static evidence
  records. Framed around a concrete example: managing resource
  access/scripts for an external target (Cloudflare DNS/site config,
  Firebase) through trail frames, then being able to replay a trail to
  demonstrate/simulate the workflow for a business stakeholder ("pendant"
  in the transcript is likely a mis-transcription - probably "client" or
  similar) regardless of how it was originally run.
- **Earned-constraint example he likes:** told an agent to go earn money on
  Upwork, it got blocked by bot detection, and that failure becomes an
  earned constraint feeding the next reflect/reseed cycle. This is already
  exactly what `reflect`'s `earned_constraints`/`next_seed` fields are for
  - a good validating example for the existing mechanism, not a new
  feature request.
- **Model fine-tuning:** open question, not a plan - whether PMCRO
  Orchestrator (and other lifecycle/Chief roles) should eventually be
  fine-tuned models rather than prompted personas on a shared base model,
  given .NET Aspire's Python integration path. Explicitly floated as "I
  don't know if that's what we're missing," not a request to start this.
- **MCP server wrapping riff:** enthusiasm about how far Terminal +
  Playwright + Filesystem MCP access already goes toward autonomy: no
  concrete ask attached.
- **Trello-as-product angle:** a board/kanban-style view of this system
  has commercial appeal ("nice, especially selling to someone"). Product
  framing, not architecture.

## What NOT to do with this note

- Don't start building a new Federation Board mechanism from this alone -
  it's a first-pass verbal description, not a spec.
- Don't treat this as grounds to silently overturn
  `ADR-federation-csuite-decision-2026-09-06.md` either.
- If Federation Board comes up again before Shawn has explicitly revisited
  it, surface both this note and the existing ADR together and ask him
  directly which one reflects his current thinking.
