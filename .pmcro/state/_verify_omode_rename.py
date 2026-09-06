import re, subprocess

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b", re.IGNORECASE)
DRIVE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"(?<![\w.])/(Users|home|tmp|var|etc)/")

# Get the full list of files this trail touched (staged + moved), from git status
out = subprocess.run(["git", "status", "--porcelain=v1"], capture_output=True, text=True).stdout
files = []
for line in out.splitlines():
    status = line[:2]
    path = line[3:]
    if "->" in path:
        path = path.split("->")[-1].strip()
    if status.strip() in {"M", "A", "R", "??"} or "R" in status:
        if path.startswith(".pmcro/state/") or path.startswith(".pmcro/trails/"):
            continue
        files.append(path)

problems = []
for fp in files:
    try:
        text = open(fp, encoding="utf-8").read()
    except Exception as e:
        problems.append((fp, f"read error: {e}"))
        continue
    if PLACEHOLDER_RE.search(text):
        problems.append((fp, "placeholder token"))
    if DRIVE_LETTER_RE.search(text):
        problems.append((fp, "drive-letter path"))
    if ABSOLUTE_UNIX_RE.search(text):
        problems.append((fp, "absolute unix path"))

print(f"Checked {len(files)} files.")
if problems:
    print("PROBLEMS FOUND:")
    for p in problems:
        print(" -", p)
else:
    print("No placeholders, no absolute/drive-letter paths.")
