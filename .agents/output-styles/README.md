# Output Styles

Place project-scoped output style files here.

Each `.md` file defines a style applied by setting `outputStyle` in `settings.json`.

## Example

```json
// .agents/settings.json
{
  "outputStyle": "review"
}
```

```markdown
<!-- .agents/output-styles/review.md -->
---
description: Terse review mode — findings only, no filler
keep-coding-instructions: true
---

Respond with findings only. No preamble or summary unless asked.
Each finding: location, severity, and a one-line fix.
```

> Most output styles are personal and live in `~/.agents/output-styles/`.
> Only put styles here when the whole team should share them.
