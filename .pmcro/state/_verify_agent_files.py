import re

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b", re.IGNORECASE)
DRIVE_LETTER_RE = re.compile(r"[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"(?<![\w.])/(Users|home|tmp|var|etc)/")

files = [
    ".agents/agents/orchestrator.md",
    ".agents/agents/planner.md",
    ".agents/agents/maker.md",
    ".agents/agents/checker.md",
    ".agents/agents/reflector.md",
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
    # frontmatter sanity
    assert text.startswith("---\n"), f"{fp}: missing frontmatter"
    end = text.index("\n---\n", 4)
    fm = text[4:end]
    assert "name:" in fm and "description:" in fm and "tools:" in fm, f"{fp}: incomplete frontmatter"

if problems:
    print("PROBLEMS FOUND:", problems)
else:
    print("All 5 files: no placeholders, no absolute/drive-letter paths, frontmatter complete.")
