import re, yaml

path = ".pmcro/directory/agents.yaml"
with open(path, encoding="utf-8") as f:
    text = f.read()

ids_to_fix = [
    "pmcro-orchestrator", "pmcro-planner", "pmcro-maker", "pmcro-checker", "pmcro-reflector",
    "pmcro-chief-executive-officer", "pmcro-chief-technology-officer", "pmcro-chief-learning-officer",
    "pmcro-chief-compliance-officer", "pmcro-chief-data-officer", "pmcro-chief-financial-officer",
    "pmcro-chief-human-resources-officer", "pmcro-chief-information-security-officer",
    "pmcro-chief-marketing-officer", "pmcro-chief-operating-officer", "pmcro-chief-product-officer",
    "pmcro-chief-revenue-officer",
]

starts = [m.start() for m in re.finditer(r"^  - id: \S+", text, re.MULTILINE)]
bounds = starts + [len(text)]
prefix = text[:starts[0]]

blocks = [text[bounds[i]:bounds[i + 1]] for i in range(len(starts))]

changed = []
new_blocks = []
for block in blocks:
    m = re.match(r"  - id: (\S+)", block)
    aid = m.group(1)
    if aid in ids_to_fix:
        mirror_entry = (
            "      - target: agentskills\n"
            f"        path: .agents/skills/{aid}\n"
            "        note: >\n"
            "          Claude Code skill-invocation mirror (per-role SKILL.md), used when\n"
            "          this repo itself is opened as a Claude Code / Cowork project. Real,\n"
            "          on-disk, separate from the plugins/ marketplace packaging below.\n"
        )
        new_block = block.replace("    packaging:\n", "    packaging:\n" + mirror_entry, 1)
        if new_block == block:
            raise SystemExit(f"FAILED to find packaging: marker for {aid}")
        new_blocks.append(new_block)
        changed.append(aid)
    else:
        new_blocks.append(block)

text = prefix + "".join(new_blocks)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("Changed:", len(changed))
for aid in changed:
    print(" -", aid)

with open(path, encoding="utf-8") as f:
    d = yaml.safe_load(f)
print("Post-edit parse OK, agent count:", len(d["agents"]))
for a in d["agents"]:
    if a["id"] in ids_to_fix:
        paths = [p["path"] for p in a["packaging"]]
        assert f".agents/skills/{a['id']}" in paths, a["id"]
print("All", len(ids_to_fix), "ids now carry their mirror packaging pointer.")
