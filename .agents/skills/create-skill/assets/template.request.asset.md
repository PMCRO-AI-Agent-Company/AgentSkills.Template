# Template: request asset

Copy into a new skill's `assets/request.<name>.asset.md` when the skill
exposes a plugin-invocable command surface (`/plugin:skill ...`).

Supersedes `command.<name>.asset.md` — same job, renamed to pair with
`response.<name>.asset.md` (see sibling template) instead of the older
three-file command/run/reject split.

```markdown
# Request Contract — <skill-name>

## Invocation

\`\`\`text
/<plugin>:<skill-name> <subcommand> --<flag> <value>
\`\`\`

Optional flags:

- `--<flag>` — <what it does>

## Inputs

| Name | Required | Description |
|------|----------|--------------|
| `--<input-name>` | Yes/No | <description> |
```
