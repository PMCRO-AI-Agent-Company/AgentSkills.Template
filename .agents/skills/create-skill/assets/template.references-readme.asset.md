# Template: references/README.md

Copy into a new skill's `references/README.md`, then replace the table
rows with real entries as `assets/` gains real content.

```markdown
# References — <skill-name>

Documents what lives in `../assets/` and how to use each item.

| Asset file | Type | Purpose |
|------------|------|---------|
| `template.<name>.asset.md` | template | <what an agent does with it> |
| `request.<name>.asset.md` | request | <invocation contract this defines> |
| `response.<name>.asset.md` | response | <success/failure contract this defines> |
| `schema.<name>.asset.md` | schema | <what contract this validates> |
| `checklist.<name>.asset.md` | checklist | <when to run through it> |

If this skill has no assets yet, leave the table empty and this file
as the stub — don't delete it.
```
