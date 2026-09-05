# Reconciliation Plan — Parallel-Session `pmcro-marketplace` Work

**Status:** Proposed (do not execute overwrite)  
**Date:** 2026-09-05  
**Constraint:** Leave the parallel Cowork session’s uncommitted work untouched until an explicit, governed decision.

---

## 1. What exists in this workspace (this session)

| Artifact | Location | Role |
|----------|----------|------|
| ADR | `.pmcro/design/ADR-pmcro-agent-directory-and-marketplace.md` | Design authority |
| Agent Directory | `.pmcro/directory/` | Source of truth for agents |
| MVP Marketplace plugin | `plugins/pmcro-marketplace/` | `scaffold-skill` + `register-agent` |
| Scaffolder | `…/scripts/scaffold.py` | agentskills + **maf-inline (C#)** |
| Eval suite | `…/eval/eval.yaml` + fixtures | Refuse + accept cases |
| Sample outputs | `.agents/skills/sample-domain-analyst`, eval fixtures under `src/Agents/` when run |

This work is intentionally a **new, parallel tree**. It does not modify:

- `.agents/skills/create-skill`
- Any files that the other session already created under `plugins/pmcro-marketplace/` in the real repo
- `.claude-plugin/marketplace.json` / `.agents/plugins/marketplace.json` in the real repo

## 2. What the parallel session is reported to own (from prior context)

From the conversation history (not re-verified against the live Windows tree in this cloud session):

- `plugins/pmcro-marketplace/` with a more developed `scaffold-skill`
- Design doc: `.pmcro/design/pmcro-marketplace-declarative-scaffolding-design.md` (or similar)
- Archetype assets, 9-trial `eval.yaml`, .NET Aspire marketplace runtime template, Cloudflare deploy example
- Explicit decision in that design doc: **`scaffold-skill` is not a replacement for `.agents/skills/create-skill`**

That body of work is **uncommitted** (or partially committed) on the real machine and must not be clobbered.

## 3. Non-overlapping principle

```text
create-skill          →  narrow, fast path for the 6 lifecycle plugins only
parallel scaffold-skill →  richer, multi-archetype, already evaluated in the other session
this MVP scaffold-skill →  portable reference implementation + Agent Directory integration + maf-inline C#
```

All three can coexist if we treat them as **different IDs / different paths** until a reconciliation trail decides otherwise.

## 4. Recommended reconciliation options (choose one in a governed cycle)

### Option A — Side-by-side keep (lowest risk)

- Rename **this** plugin to `pmcro-marketplace-directory` or `pmcro-scaffold-mvp` so it never collides on disk with the parallel session’s `plugins/pmcro-marketplace/`.
- Keep the Agent Directory (`.pmcro/directory/`) as the shared catalog both scaffolders may register into.
- Document both scaffolders in the directory as `kind: marketplace-scaffold`.
- No code merge required.

### Option B — Adopt parallel session as canonical scaffolder

- Treat the other session’s `scaffold-skill` as the production implementation.
- Port only the **Agent Directory** integration and the **maf-inline** renderer from this MVP into that tree (via a proper Make phase).
- Archive or delete this cloud `plugins/pmcro-marketplace/` after the port is trail-evidenced.
- Still leave `create-skill` untouched.

### Option C — Merge into a single plugin (highest coordination cost)

- Open a dedicated reconciliation cycle.
- Diff both trees, keep the stronger eval suite, the stronger templates, and the Directory integration.
- Produce one `plugins/pmcro-marketplace/` that both sessions agree on.
- Requires the parallel session’s working tree to be available and a human decision on each conflicting file.

**Default recommendation while the other session’s tree is not present here: Option A.**

## 5. Concrete next steps (safe)

1. **Do not** copy or overwrite anything into a real-repo path that the other session already owns.
2. If/when the real repo is linked:
   - Run `git status` and `git log --oneline -5 -- plugins/pmcro-marketplace .pmcro/design`
   - If the parallel files exist and are uncommitted, stop and present the diff; do not `git add` this session’s files on top.
3. Register both scaffolders in `.pmcro/directory/agents.yaml` under distinct ids once both trees are visible.
4. Only after a Reflector disposition of `reconcile-adopt` / `reconcile-side-by-side` / `reconcile-merge` should any deletion or rename of the other session’s files occur.

## 6. Success criteria for reconciliation

- [ ] `create-skill` still exists and behaves as before
- [ ] Parallel session’s uncommitted work is either preserved intact or deliberately merged under a sealed trail
- [ ] Agent Directory remains the single catalog
- [ ] No drive-letter or absolute paths introduced
- [ ] Eval refuse cases still pass on the surviving scaffolder

## 7. Seed intent for the reconciliation cycle (when ready)

> “Reconcile this-session plugins/pmcro-marketplace (Directory + maf-inline MVP) with the parallel-session pmcro-marketplace work without overwriting uncommitted files. Prefer side-by-side (Option A) unless evidence shows the parallel scaffolder already covers Directory registration and maf-inline C#.”

---

## Applied (2026-09-05)

Option A executed in the cloud workspace:

1. Renamed `plugins/pmcro-marketplace/` → `plugins/pmcro-marketplace-directory/`
2. Registered distinct directory entries:
   - `pmcro-marketplace-directory` (this session, experimental)
   - `pmcro-marketplace-parallel` (parallel session, planned, path reserved, not overwritten)
3. Moved `reasoning-skills/` → `.agents/skills/reasoning/` for a single skills tree
4. Added workspace `README.md` map for educators
5. No parallel-session files were deleted or modified (none were present in this workspace)

