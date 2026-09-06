# Product: Trail Player, and Declarative MAUI UI Generation

**Status:** Design captured, nothing built yet. Written from Shawn's live direction plus real
evidence recovered from his conversation export (`artifacts/claude-export-f58ab584`) - not invented.

## What the Trail Player actually is

Not a UI feature buried inside the workspace app - **a product the Company built**, whose job is to
replay and let a human watch a sealed PMCR-O trail happen, the way Windows's old **Steps Recorder**
(`psr.exe`) replayed a sequence of user actions as a step-by-step slideshow. Grounded in Shawn's own
prior design, recovered verbatim from the export:

- A dedicated trail convention already exists for this: `/cognition/trails/roundtable/RT-<timestamp>.json`
  - a distinct `RT-` id prefix and path, separate from ordinary PMCR-O trails.
- The stated design law for it, quoted directly: *"The replay must read the REAL trail files on disk;
  do not fabricate trail content."* - the Trail Player is a viewer over real evidence, never a
  simulation or a mockup of one.
- Prior UI shape (Next.js/CopilotKit era): a docked `CopilotChat`, a `canvas-pane` (hero form, domain
  selector, activity feed), a `PhaseRail`, and the trail player itself - rendering a trail's real
  Orchestrate → Plan → Make → Check → Reflect phases in sequence, sourced from the same phase files
  `WorkspaceController.cs`'s `GetTrailDetail` already serves today (`trail.json`, `01-orchestrate.jsonl`,
  `02-plan.json`, `03-make.jsonl`, `04-check.json`, `05-reflect.json`).
- A real, documented failure mode from that history: a trail written in a shape the reader didn't
  expect rendered as "No disposition" / "No plan entries" even though the trail was real and sealed.
  The lesson for any new implementation: verify against the actual current frame shapes
  (`.pmcro/runtime/output-contract.md`, the schemas under each plugin), not a remembered or assumed one.

**Today's implementation status:** `ui/projectname-copilotkit`'s workspace panel already has a basic
"Trails" section wired to the real backend (`WorkspaceController.GetTrailDetail`), but it is the plain
data view, not the PhaseRail/replay experience described above. The Trail Player as a *product* -
something the Company would ship, name, and put on a phone - does not exist yet.

## The declarative MAUI direction

Shawn's instruction: don't hand-build mobile screens one at a time. Once the .NET MAUI UI/UX exists in
a working, real form, extract a **declarative spec + generator** from it - the same "declare once,
generate the projection" principle this session already proved twice (`AgentScaffoldSpec` →
`scaffold.py` for agents; `ReasoningStrategySpec` → `render_strategy.py` for reasoning strategies) -
and package the generator itself as an AgentSkills asset (a real skill/plugin in this repo's existing
skill ecosystem, invokable the same way `scaffold-skill`/`scaffold-chief` are), so new MAUI screens can
be generated on demand instead of hand-coded per screen.

**Why this has to come after a real screen exists, not before it** - this is the one architectural
invariant that held both times the pattern was proven this session, and broke the one time it was
skipped: a declarative spec is only trustworthy when it is reverse-engineered from something real and
working. Writing a `MauiScreenSpec` schema now, before a single MAUI screen exists in this repo, would
mean guessing at a shape with nothing to check it against - exactly what "Incremental Progression"
(this repo's own architectural invariant) exists to prevent. The reasoning-strategy generator's own
history is the concrete warning: the first draft's `steps_description` field was wrong until a real
round-trip against real files caught it. There is no real file to round-trip against yet for MAUI.

## Recommended order (not yet started)

1. **Scaffold a minimal .NET MAUI project** in this solution. Technically viable now - `android`, `ios`,
   `maccatalyst`, and `maui-windows` workloads are all confirmed installed on this machine at SDK
   `11.0.100-preview.7`, verified via `dotnet workload list`, not assumed.
2. **Build ONE real screen by hand: the Trail Player**, reading actual `.pmcro/trails/*/`  content from
   this repo (via whatever the mobile app's own data-access path turns out to be - a local file read for
   a desktop-adjacent build, or a call to the existing `WorkspaceController` endpoints for a networked
   one; not decided here, a real question for that increment). Verify it renders a real sealed trail's
   phases correctly, including the historical failure mode above (a trail in an unexpected shape must
   fail visibly, not silently render as empty).
3. **Only then** reverse-engineer a `MauiScreenSpec` (or similarly named) declarative shape from that one
   real screen, the same way `chain-of-thought.md` and `self-refine.md` were read in full before
   `reasoning-strategy-spec.schema.json` was written - not the other way around.
4. **Prove the generator** the same way both prior ones were proven: generate from the spec, diff against
   the real hand-built screen, and treat any mismatch as a finding to fix, not a detail to gloss over.
5. **Package it as an AgentSkills asset** - a new skill (e.g. `plugins/pmcro-mobile-ui/skills/scaffold-screen`)
   once the pattern is proven, not before.

## Open questions this doc deliberately leaves open

- Whether the MAUI app talks to the existing `ProjectName.Api`/`WorkspaceController` over the network,
  reads repo files directly (only viable if the app and repo share a filesystem), or something else -
  a real architecture decision for step 1/2, not guessed here.
- Whether "Roundtable" trails (`RT-` prefix, `/cognition/trails/roundtable/`) get their own Trail Player
  variant or the same one - depends on whether a Roundtable trail's phase shape actually differs from an
  ordinary PMCR-O trail's, which has not been checked against real data yet.
- CopilotKit's role on MAUI specifically - the historical design used CopilotKit's React/web SDK; MAUI is
  not a web runtime, so the integration shape (a hosted web view, a native chat surface calling the same
  backend, or something else) needs its own real investigation before assuming continuity with the
  Next.js implementation.
