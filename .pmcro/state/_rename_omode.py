import re
from pathlib import Path

ROOT = Path(".")

LIVE_FILES = []

def add_glob(pattern):
    LIVE_FILES.extend(sorted(ROOT.glob(pattern)))

# Everything that moved (self-references inside the renamed package)
add_glob("plugins/pmcro-omode/**/*.md")
add_glob("plugins/pmcro-omode/**/*.json")
add_glob("plugins/pmcro-omode/**/*.yaml")
add_glob("plugins/pmcro-omode/**/*.yml")
add_glob("plugins/pmcro-omode/**/*.py")

# Live cross-references elsewhere
CODES = ["ceo", "cto", "clo", "cco", "cdo", "cfo", "chro", "ciso", "cmo", "coo", "cpo", "cro"]
IDS = [
    "pmcro-chief-executive-officer", "pmcro-chief-technology-officer", "pmcro-chief-learning-officer",
    "pmcro-chief-compliance-officer", "pmcro-chief-data-officer", "pmcro-chief-financial-officer",
    "pmcro-chief-human-resources-officer", "pmcro-chief-information-security-officer",
    "pmcro-chief-marketing-officer", "pmcro-chief-operating-officer", "pmcro-chief-product-officer",
    "pmcro-chief-revenue-officer",
]
for i in IDS:
    LIVE_FILES.append(Path(f".agents/agents/{i}.md"))
    LIVE_FILES.append(Path(f".agents/skills/{i}/SKILL.md"))
LIVE_FILES.append(Path(".agents/skills/scaffold-chief/SKILL.md"))
LIVE_FILES.append(Path(".agents/skills/scaffold-chief/assets/schemas/chief-spec.schema.json"))
LIVE_FILES.append(Path("examples/chief-learning-officer.spec.yaml"))
for c in CODES:
    LIVE_FILES.append(Path(f"plugins/pmcro-csuite/agents/{c}.md"))
    sf = Path(f"specs/csuite/{c}.spec.yaml")
    if sf.exists():
        LIVE_FILES.append(sf)
LIVE_FILES.append(Path("plugins/pmcro-csuite/skills/govern-domain-intent/SKILL.md"))
LIVE_FILES.append(Path("plugins/pmcro-csuite/skills/select-reasoning-strategy/SKILL.md"))
LIVE_FILES.append(Path("plugins/pmcro-csuite/plugin.json"))
LIVE_FILES.append(Path(".pmcro/directory/agents.yaml"))
LIVE_FILES.append(Path(".pmcro/design/DECLARATIVE-REASONING-STRATEGY-TEMPLATE.md"))

changed = []
missing = []
for fp in LIVE_FILES:
    if not fp.exists():
        missing.append(str(fp))
        continue
    text = fp.read_text(encoding="utf-8")
    orig = text

    text = text.replace("plugins/pmcro-reasoning-strategy", "plugins/pmcro-omode")
    text = text.replace("package: reasoning-strategy", "package: pmcro-omode")
    text = re.sub(r"pmcro-reasoning-strategy:", "pmcro-omode:", text)
    text = text.replace("pmcro-reasoning-strategy", "pmcro-omode")
    text = text.replace("plugins/pmcro-csuite/omode/", "plugins/pmcro-csuite/skills/select-reasoning-strategy/assets/")

    if fp == Path("plugins/pmcro-csuite/skills/select-reasoning-strategy/SKILL.md"):
        text = text.replace("omode/<chief_id>.yaml", "assets/<chief_id>.yaml")

    if text != orig:
        fp.write_text(text, encoding="utf-8")
        changed.append(str(fp))

print(f"Changed {len(changed)} files:")
for c in changed:
    print(" -", c)
if missing:
    print(f"\nMissing (not found, skipped): {len(missing)}")
    for m in missing:
        print(" -", m)
