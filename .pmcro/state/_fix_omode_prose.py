from pathlib import Path

CODES = ["ceo", "cto", "clo", "cco", "cdo", "cfo", "chro", "ciso", "cmo", "coo", "cpo", "cro"]
IDS = [
    "pmcro-chief-executive-officer", "pmcro-chief-technology-officer", "pmcro-chief-learning-officer",
    "pmcro-chief-compliance-officer", "pmcro-chief-data-officer", "pmcro-chief-financial-officer",
    "pmcro-chief-human-resources-officer", "pmcro-chief-information-security-officer",
    "pmcro-chief-marketing-officer", "pmcro-chief-operating-officer", "pmcro-chief-product-officer",
    "pmcro-chief-revenue-officer",
]

files = [Path(f"plugins/pmcro-csuite/agents/{c}.md") for c in CODES]
files += [Path(f".agents/skills/{i}/SKILL.md") for i in IDS]

changed = []
for fp in files:
    if not fp.exists():
        continue
    text = fp.read_text(encoding="utf-8")
    orig = text
    # Only the bare, generic "omode.yaml" prose mentions - not any already-full-path
    # reference (those were already fixed in the rename trail).
    text = text.replace(
        "## Reasoning Modes (from `omode.yaml`)",
        "## Reasoning Modes (from its select-reasoning-strategy trigger table)",
    )
    text = text.replace(
        "from omode.yaml + catalog",
        "from its select-reasoning-strategy trigger table + catalog",
    )
    if text != orig:
        fp.write_text(text, encoding="utf-8")
        changed.append(str(fp))

print(f"Changed {len(changed)} files:")
for c in changed:
    print(" -", c)
