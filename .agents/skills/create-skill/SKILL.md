---
name: create-skill
description: >-
  Scaffolds new agent skills (SKILL.md packages) from copy-paste templates plus a deterministic
  drift validator — for the six core PMCR-O lifecycle plugins and for any new skill's SKILL.md,
  references/README.md, scripts/README.md, and request/response command assets. Use this whenever
  the user wants to create, scaffold, or draft a new skill or SKILL.md — even if they just
  describe a capability and don't name the file format. Also use it to pick the right *shape*
  for a new skill (workflow / reference / script-driven / composite) before writing anything.
  DO NOT use this for generic domain/persona/tool skills needing multi-target (agentskills +
  MAF-inline) code generation from a declarative spec — use scaffold-skill instead. DO NOT use
  this for fixing a skill that already fails its evaluation (use improve-skill-quality), or for
  writing an eval.yaml (use create-skill-test).
metadata:
  version: "0.3.0"
  revision_note: >-
    2026-09-05: replaced an undocumented, never-implemented scaffold.py/JSON-spec/MAF-codegen
    pipeline (referenced scripts/references paths that did not exist in this skill) with the
    simpler template+validator system that was already proven live in scaffold-skill's own
    assets/. The archetype-selection step (workflow/reference/script-driven/composite) is
    unchanged — it was real and useful. MAF C#/Python code generation is scaffold-skill's job,
    not this skill's.
---

# create-skill

This skill scaffolds new agent skills by **copying templates from `assets/`** and filling in
placeholders — no declarative JSON spec, no code generator. `references/README.md` documents
every template; `scripts/validate_skill_md.py` deterministically checks the result for known
drift patterns before you call the skill done.


## Step 1: Pick the archetype — this is the decision that matters most

Four archetypes exist as `templates/<archetype>.yaml`. Getting this wrong produces a
structurally valid but useless skill (e.g., a 40-step "workflow" that's actually a lookup
table, which nobody will read past step 3). Read the matching template file before writing
anything — it carries the exact section list and validation rules for that archetype.

| If the ask is... | Archetype | Signal |
|---|---|---|
| "do these steps every time" / a repeatable procedure with judgment calls | `workflow` | The value is in the sequence and stop-conditions, not in stored facts. |
| "what is X" / "look up the rule for X" | `reference` | The value is in bundled knowledge; there's no procedure to run. |
| "compute/transform/validate this" with one correct answer | `script-driven` | Correctness depends on running the same code every time, not on reasoning it out fresh. |
| the same intent forks into genuinely different procedures per variant (cloud provider, file format, framework) | `composite` | Two or more variants exist; forcing this into `workflow` means duplicating branches inline instead of routing to them. |

Don't default to `composite` to hedge — a composite spec with fewer than two real variants
should be a plain `workflow` or `reference` skill instead (see that archetype's validation
rules). If the request is ambiguous between two archetypes, ask one direct question rather
than guessing — the archetype changes the file layout, not just the wording.


## Step 2: Copy the templates

For the chosen archetype's `skill_md_sections`, build `SKILL.md` from
`assets/template.skill-md.asset.md`, filling every `<placeholder>` — don't invent sections the
archetype didn't call for. Then:

- If the skill bundles reference material (docs, schemas, lookup tables — anything a `reference`
  or `composite` archetype typically needs), copy `assets/template.references-readme.asset.md` →
  new skill's `references/README.md`. Skip this entirely for a skill with no reference material —
  an empty `references/` folder with a placeholder README is worse than no folder at all.
- If the skill has scripts (present now, or clearly planned before this skill is used), copy
  `assets/template.scripts-readme.asset.md` → new skill's `scripts/README.md`. Skip this for a
  skill that is pure instructions with no code to run — don't create `scripts/` "just in case."
- If the skill exposes a plugin-invocable command (`/plugin:skill ...`), copy
  `assets/template.request.asset.md` → `assets/request.<name>.asset.md` AND
  `assets/template.response.asset.md` → `assets/response.<name>.asset.md`. These are always
  authored as a pair — never add one without the other.
- If the skill needs a standalone verification checklist, copy
  `assets/template.checklist.asset.md` → `assets/checklist.<name>.asset.md`

## Step 3: Validate

```bash
python .agents/skills/create-skill/scripts/validate_skill_md.py <path-to-new-SKILL.md>
```

Checks: the `## PMCRO Output Law` footer is present verbatim, `## Command Surface` isn't
duplicating what an `assets/request.*.asset.md` already defines, and every
`assets/request.*.asset.md` has its matching `assets/response.*.asset.md` (and vice versa).
Exit code 0 = pass; findings are printed either way — fix them before calling the skill done.

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
