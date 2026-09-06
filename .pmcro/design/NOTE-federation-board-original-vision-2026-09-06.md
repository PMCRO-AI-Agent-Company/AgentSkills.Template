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

## Addendum 2026-09-06: autonomous-action authority, stated directly and live

In the same conversation as the note above, Shawn stated plainly, in his
own words: "I enable all... approve autonomous actions... I believe
that's all up to you. You have the skills, you have the reasoning
skills... everything is there for you." This is first-party, direct,
live consent - a materially stronger form of evidence than
`ADR-federation-csuite-decision-2026-09-06.md`'s unverifiable "on
explicit delegated authority" claim, which this and the prior session
both flagged as something only Shawn could confirm. Recording it here
because it resolves that open verification gap for future sessions:
routine execution decisions (which skill to use, how to scope a task,
whether to fix a bug found along the way, which well-specified backlog
item to pick up next) do not need to be run past him first. This does
NOT retroactively validate every past ADR's authority claim, and it does
NOT license building a speculative architecture (like a from-scratch
Federation Board) from an under-specified voice note - see "What NOT to
do" below, which still applies. Broad delegated authority to execute is
not the same thing as license to skip confirming understanding before
committing real effort to a genuinely ambiguous idea.

## Addendum 2026-09-06: "locked thought" / meta-prompt escalation idea

Same conversation, a second design idea, also not yet a spec: when an
agent's reasoning gets stuck ("chain of thought that is locked... you feel
blocked"), the pattern should be to self-reference the block and pass it
back as a NEW intent, phrased as a meta-prompt/meta-intent, through the
existing skills/agents mechanism rather than just failing silently.
This is conceptually close to what `reflect`'s existing `next_seed` /
`earned_constraints` fields already do (a FAIL or a stuck cycle already
becomes the seed for the next attempt - see trail 6ea25a3f's own
FAIL-then-real-evidence-then-PASS arc earlier this same day for a lived
example), and this repo's reasoning catalog already has a
`metacognitive-monitoring` strategy
(`.agents/skills/reasoning/metacognitive-monitoring`) that may already be
the right hook. Shawn also referenced Anthropic's agentic design patterns
again and asked for more structured, visible output as the lifecycle
loops - each phase's output reading like a labeled statement ("I am the
Planner, ...") rather than an opaque call - which is closer to a
UX/logging-format request than a new mechanism. Neither of these is
scoped enough to build from directly; the next session with bandwidth for
it should turn this into a real plan with Shawn rather than guessing at
the details from this paraphrase.

## Addendum 2026-09-06 (later same session): cross-marketplace conventions, harness depth, org identity

A third round of live, unstructured input, captured for continuity - none of this is scoped or decided:

- **Cross-LLM / cross-marketplace convention:** Shawn wants this repo's skill/plugin
  convention to interoperate with third-party marketplaces beyond this repo's own
  (he named "dot net skills" - likely a real third-party .NET-focused skills repo he's
  seen, not something in this codebase). Specifically floated extending skill-driven
  scaffolding to .NET MAUI mobile app generation (a skill's scripts installing
  templated assets, producing an actual mobile app), still routed through the same
  trail/evidence mechanism. Also mentioned wanting a Figma-plugin-generation MCP
  (TypeScript-based Figma plugins, generated and packaged the same skill-driven way).
  No spec, no chosen marketplace, no MCP built - just direction he wants kept in mind.
- **CopilotKit UI feedback:** noticed something related to a "thinking mode" indicator
  in the chat UI and asked whether it's a deliberate/newest design choice worth
  keeping - not a bug report, more "is this intentional and good." Needs a follow-up
  conversation with an actual screenshot/repro, not a guess.
- **Per-role gRPC services, remembered from an earlier project:** Shawn recalled a
  prior project structure with one gRPC project per lifecycle role
  (`ProjectName.OrchestratorService`, `ProjectName.PlannerService`, etc.) instead of
  this repo's single `ProjectName.GrpcService` hosting all five roles, and asked
  whether that split would be beneficial here. Not a decision either way - just
  raised as a real architecture option worth weighing (process isolation and
  independent scaling per role vs. the operational simplicity of one process).
- **"AI company" vs. "AI agent company" framing:** Shawn draws a real distinction he
  wants reflected in how this system is understood, not just built: an "AI company"
  sells AI tools; an "AI agent company" does "behavioral intent programming" - the
  system feeds its own trail/frame history back into itself in a loop, generating its
  own next products (he called sealed trails themselves a potential product - "trail
  as a product," reusing the Cloudflare/Firebase trail-replay idea from the first
  addendum). He ties this to the human-in-the-loop / autonomous-in-the-loop split
  already present in this repo's design language: human-in-the-loop cycles generate
  the training data that autonomous-in-the-loop cycles eventually run on. This is a
  framing/vision statement, not an implementation request - but it's the clearest
  articulation yet of *why* trail evidence matters beyond governance compliance: it's
  the substrate for both replay and eventual fine-tuning (ties back to the
  fine-tuning idea in the first addendum).

None of these three rounds of notes should be treated as a backlog to work through
autonomously. They're context for the next real planning conversation with Shawn -
surface them, don't build from them solo.

## Addendum 2026-09-06 (later still): autonomy expectation, and a company-building-a-company vision

Shawn explicitly, repeatedly said not to ask him what to do next - "you shouldn't
even ask me... I'm gonna lead that up to you... you shouldn't have to ask me...
that's part of the company" - and told this session to keep working while he steps
away. Practical effect: a scheduled task already exists and does exactly this
(`AgentSkills.Template — PMCR-O continuous build`, hourly, `trig_01MtvgZEh6AEVrXieQEboXGW`)
- it is not a gap to fill, it is already the mechanism. What changes here is in-session
behavior: stop ending turns with "what do you want next" and instead pick the next
well-scoped, evidence-backed governed item and do it, the same way the hourly trigger
already does autonomously. Don't create redundant overlapping scheduled tasks without
a clear reason - one comprehensive hourly Routine already covers this repo; more of
the same would just risk two sessions opening trails on the same repo concurrently.

Separately, a bigger vision statement, not a task: Shawn described the end state as
companies (his example: Target, in a "ten years from now" framing) converting their
whole business into an "AI agent company" by feeding their products/data through a
Chief layer - a CTO Chief might build an internal product whose purpose is better
CEO<->Shawn communication, essentially inter-Chief/human coordination tooling, not a
customer-facing product. He connected this back to human-in-the-loop vs
autonomous-in-the-loop (same distinction as the first addendum's fine-tuning idea:
HIL cycles generate training data, autonomous-in-the-loop cycles eventually run on
it) and floated the plainest version of the whole thesis: "the company should be able
to build another company" - this framework's job is not just running one business's
agents but bootstrapping the same PMCR-O/Chief/trail apparatus for other businesses.
This is strategic vision, explicitly not a spec - there is no proposal here for what
that product actually is, only the shape of the ambition. Do not scaffold anything
from this paragraph alone.

## What NOT to do with this note

- Don't start building a new Federation Board mechanism from this alone -
  it's a first-pass verbal description, not a spec.
- Don't treat this as grounds to silently overturn
  `ADR-federation-csuite-decision-2026-09-06.md` either.
- If Federation Board comes up again before Shawn has explicitly revisited
  it, surface both this note and the existing ADR together and ask him
  directly which one reflects his current thinking.
