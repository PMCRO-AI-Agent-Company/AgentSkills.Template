# Scripts — create-skill

Deterministic validation lives here — run directly, no reasoning
required.

| Script | Purpose | How to invoke |
|--------|---------|----------------|
| `validate_skill_md.py` | Checks a SKILL.md for two known drift patterns: embedded/duplicated Command Surface text (should reference `assets/request.*.asset.md`/`response.*.asset.md` instead) and a missing or reworded `## PMCRO Output Law` footer. | `python validate_skill_md.py <path-to-SKILL.md-or-skill-dir>` |
