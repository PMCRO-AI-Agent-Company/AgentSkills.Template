import re, json, yaml

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b", re.IGNORECASE)
DRIVE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"(?<![\w.])/(Users|home|tmp|var|etc)/")

files = [
    "plugins/pmcro-reasoning-strategy/schemas/reasoning-strategy-spec.schema.json",
    "plugins/pmcro-reasoning-strategy/scripts/render_strategy.py",
    "plugins/pmcro-reasoning-strategy/specs/chain-of-thought.spec.yaml",
    "plugins/pmcro-reasoning-strategy/specs/self-refine.spec.yaml",
    ".pmcro/design/DECLARATIVE-REASONING-STRATEGY-TEMPLATE.md",
]

problems = []
for fp in files:
    text = open(fp, encoding="utf-8").read()
    if PLACEHOLDER_RE.search(text):
        problems.append((fp, "placeholder token"))
    if DRIVE_LETTER_RE.search(text):
        problems.append((fp, "drive-letter path"))
    if ABSOLUTE_UNIX_RE.search(text):
        problems.append((fp, "absolute unix path"))

# schema itself must be valid JSON
with open(files[0], encoding="utf-8") as f:
    json.load(f)

# both specs must parse as YAML and be non-empty mappings
for spec_file in files[2:4]:
    with open(spec_file, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    assert isinstance(d, dict) and "id" in d, f"{spec_file}: invalid spec"

if problems:
    print("PROBLEMS FOUND:", problems)
else:
    print("All 5 new files: no placeholders, no absolute/drive-letter paths, schema+specs parse cleanly.")
