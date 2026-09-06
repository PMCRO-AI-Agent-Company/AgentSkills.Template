import re

path = "artifacts/claude-export-f58ab584/extracted/conversations/conversations.json"
with open(path, encoding="utf-8") as f:
    text = f.read()

print(f"File size: {len(text)} chars")

for term, pattern in [("ROUNDTABLE", r"roundtable"), ("TRAIL PLAYER", r"trail.{0,3}player")]:
    print(f"\n{'='*20} {term} {'='*20}")
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    print(f"Total occurrences: {len(matches)}")
    # Print context for first 5 and last 2 occurrences, deduped by rough position
    shown = 0
    last_pos = -10000
    for m in matches:
        if m.start() - last_pos < 200:
            continue
        last_pos = m.start()
        start = max(0, m.start() - 150)
        end = min(len(text), m.end() + 150)
        snippet = text[start:end].replace("\\n", " ").replace("\\t", " ")
        print(f"\n--- occurrence at char {m.start()} ---")
        print(snippet)
        shown += 1
        if shown >= 6:
            break
