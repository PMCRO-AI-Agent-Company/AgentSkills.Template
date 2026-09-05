# Template: checklist asset

Copy into a new skill's `assets/checklist.<name>.asset.md`. One
checklist per distinct verification concern — don't merge unrelated
concerns into one file.

```markdown
# Checklist: <what this verifies>

Used during: <which workflow step or phase this checklist belongs to>

- [ ] <Concrete, observable check>
- [ ] <Concrete, observable check>
- [ ] <Concrete, observable check>

## If any item fails

<What to do — retry, escalate, or which role/skill owns the fix>
```
