# ADR — Federation / C-Suite Naming and Placement

**Status:** Decided
**Date:** 2026-09-06
**Decided by:** Claude (Cowork), acting on explicit delegated authority from the repo owner ("leave all decisions to you") following `.pmcro/design/AUDIT-claude-architecture-review-2026-09-06.md` §7–8.
**Supersedes:** nothing — this is the first written decision on this question. The terms "Federation" and "Federation Board" previously existed only in the owner's own prior mental model (and possibly the superseded `P:\ProjectName` session), never in this repository.

## Question

The repo owner's older PMCR-O concept included a "Federation" layer with "Federation Boards" for cross-domain governance and coordination. Does that concept have a legitimate place in this repository's current architecture, and if so, where?

## Decision

**No rename, no new artifact, for now.** The 12-Chief C-Suite layer (`plugins/pmcro-csuite/`) already occupies the architectural slot a "Federation" would occupy — a governance layer above the shared five-role cycle that turns a raw request into governed, domain-scoped intent before Orchestrator ever opens a trail. It is built, checker-verified in its current form, and already the thing every Chief-facing skill and every lifecycle doc points at. Federation is **not** being introduced as a rename of this layer, and a literal "Federation Board" artifact is **not** being built at this time.

## Rationale

1. **The function already exists.** `RECONCILIATION-older-application-session.md` records a deliberate, evaluated choice between two models: a per-Chief "cabinet" (each Chief runs its own full Orchestrator→Planner→Maker→Checker→Reflector loop — closer to what a literal Federation-of-domains might imply) versus a shared-cycle "intent-governance" model (Chiefs produce scope only, one cycle for everyone). The shared-cycle model was chosen and built. Re-opening that as a Federation question would be re-litigating an already-made, already-implemented decision without new evidence that it's wrong.
2. **Renaming has a real, recently-demonstrated cost.** The bulk of `AUDIT-claude-architecture-review-2026-09-06.md`'s findings (section 6) are cross-reference drift left behind by the *last* consolidation/rename (12 separate Chief plugins → `pmcro-csuite`; 5 separate lifecycle plugins → `pmcro`): `directory/agents.yaml`, discovery mirrors, and `COMMAND-CATALOG.md` all silently fell out of sync and stayed that way for weeks. Renaming C-Suite to "Federation" now would touch the same files (`agents.yaml`, 12 `.agents/skills/pmcro-chief-*` mirrors, `plugin.json`, every Chief's own agent file) purely for vocabulary, with no functional gain, and a demonstrated risk of reintroducing exactly the drift that was just cleaned up.
3. **No observed need for a Board yet.** A Federation Board's distinguishing job would be arbitrating when two Chiefs' `IntentFrame`s conflict or compete for the same Orchestrator slot. Nothing in `.pmcro/trails/`, `.pmcro/queue/`, or the Chief skill definitions shows this has ever actually happened. Building an arbitration artifact ahead of a real, observed conflict is speculative complexity — exactly the kind of thing the audit's own finding (§5) warns `.pmcro/` already has too much of in `design/`.
4. **Findability matters even without a rename.** The audit found zero references to "Federation" anywhere in the repo, meaning a future reader (including a future session working from the owner's older notes) would find nothing. This ADR, plus the pointer added to `.pmcro/README.md`, fixes that without touching any working code or registry path.

## What this decision does NOT foreclose

If cross-Chief conflict becomes a real, evidenced problem — two Chiefs producing incompatible `IntentFrame`s for the same seed, or contention for Orchestrator's attention that the current priority scale (`0 stop-the-line → 1 CEO/CoS → 2 domain critical → 3 normal → 4 backlog`) doesn't resolve — the natural seam for a Federation Board is:

- **Beside** the Chiefs, never inside the cycle: a new skill/artifact that runs *before* Orchestrator, consuming multiple Chiefs' `IntentFrame`s and producing one arbitrated seed.
- Never touching Planner, Maker, Checker, or Reflector directly — `L-ORCHESTRATION` ("orchestrator owns routing, not domain implementation") and the shared-cycle decision both exist specifically to keep domain/arbitration logic out of the lifecycle roles.
- Evidenced the same way everything else is: a real trail, opened only once there's a real conflict to arbitrate, not built speculatively.

## Action taken alongside this decision

Added one sentence to `.pmcro/README.md` pointing "Federation" searches at this ADR and at `plugins/pmcro-csuite/`, so the vocabulary gap is closed for findability without any path, registry, or plugin being renamed.
