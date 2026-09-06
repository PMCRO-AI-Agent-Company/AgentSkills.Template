import re
PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|CHANGEME|TBD|FILLME)\b", re.IGNORECASE)
DRIVE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
ABSOLUTE_UNIX_RE = re.compile(r"(?<![\w.])/(Users|home|tmp|var|etc)/")
text = open(".pmcro/design/PRODUCT-trail-player-and-declarative-maui-ui.md", encoding="utf-8").read()
problems = []
if PLACEHOLDER_RE.search(text): problems.append("placeholder")
if DRIVE_LETTER_RE.search(text): problems.append("drive-letter")
if ABSOLUTE_UNIX_RE.search(text): problems.append("absolute-unix")
print("PROBLEMS:", problems if problems else "none - clean")
