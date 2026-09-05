# References — create-skill

Documents what lives in `../assets/` and how to use each item.

| Asset file | Type | Purpose |
|------------|------|---------|
| `template.skill-md.asset.md` | template | Copy into every new skill's `SKILL.md` |
| `template.references-readme.asset.md` | template | Copy into every new skill's `references/README.md` |
| `template.scripts-readme.asset.md` | template | Copy into every new skill's `scripts/README.md` |
| `template.checklist.asset.md` | template | Copy into `assets/checklist.<name>.asset.md` when the new skill needs one |
| `template.request.asset.md` | template | Copy into `assets/request.<name>.asset.md` when the new skill exposes a plugin command |
| `template.response.asset.md` | template | Copy into `assets/response.<name>.asset.md` alongside the request asset — success/failure contract |

`create-skill`'s Workflow (see `../SKILL.md`) copies from these
templates rather than inlining them in prose — keep both in sync if
either changes.

## Migration note (2026-09-05)

`template.command.asset.md` (invocation-only) plus separate
`run.<name>.asset.md` / `reject.<name>.asset.md` files is the retired
predecessor of `template.request.asset.md` / `template.response.asset.md`.
New skills use request/response. Existing skills built on the old triad
(e.g. `scaffold-skill`) are being migrated — see that skill's own assets/
for its current state.
