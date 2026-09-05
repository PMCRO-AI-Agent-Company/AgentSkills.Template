# Template: response asset

Copy into a new skill's `assets/response.<name>.asset.md`. Pairs with
`request.<name>.asset.md`. Replaces the old two-file `run.<name>.asset.md`
+ `reject.<name>.asset.md` split — PASS and FAIL are two branches of one
response contract, not two different artifacts, matching this repo's own
Checker-gate PASS/FAIL discipline (L-CHECKER-GATE) applied one layer down.

```markdown
# Response Contract — <skill-name>

## Success (status: ok)

\`\`\`json
{
  "status": "ok",
  "action": "<ACTION_NAME>",
  "...": "..."
}
\`\`\`

## Failure (status: reject)

\`\`\`json
{
  "status": "reject",
  "reason": "<reason-code-1> | <reason-code-2>",
  "details": ["…"]
}
\`\`\`

## Rejection Conditions table (put this in the skill's body or in this asset)

| Condition | Reason code |
|-----------|-------------|
| <condition 1> | `<reason-code-1>` |
| <condition 2> | `<reason-code-2>` |

Refusal is a successful execution of the skill's contract, not a runtime
error — the caller receives this structured reject result, not an exception.
```
