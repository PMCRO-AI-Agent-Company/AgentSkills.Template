# Template: SKILL.md

Copy this verbatim into `plugins/<plugin>/skills/<skill-name>/SKILL.md`
(or `.agents/skills/<skill-name>/SKILL.md`) and fill in every `<placeholder>`.

```markdown
---
name: <skill-name>
description: <1-1024 char description: what it does, when to use it, USE FOR / DO NOT USE FOR against same-plugin siblings only>
---

# <Skill Title>

<One paragraph describing the skill's purpose and outcome.>

## Command Surface

<If this skill has a user-facing command surface (e.g. `/plugin:skill-name <subcommand>`),
do NOT embed the literal command list here. Reference the request/response
assets instead, e.g.:>

Request/response contracts are defined in `assets/` — see
`request.<skill-name>.asset.md` and `response.<skill-name>.asset.md` for
the canonical invocation syntax and success/failure shapes. This section
is a pointer, not a duplicate — the asset files are the single source
of truth.

<If this skill takes no arguments (like activate), omit this section entirely.>
## When to Use

- <Scenario 1>
- <Scenario 2>

## When Not to Use

- <Exclusion 1 — name the same-plugin sibling that owns it, if any>

## Inputs

| Input | Required | Description |
|-------|----------|--------------|
| <input-name> | Yes/No | <description> |

## Workflow

### Step 1: <Action>

<Instructions>

## Validation

- [ ] <Verification step>

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| <Problem> | <Fix> |

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md. Return the PMCRO governance envelope; domain-specific payloads are subordinate to it. Do not claim completion without the required evidence and Checker gate.
```
