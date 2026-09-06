import yaml
d = yaml.safe_load(open(".pmcro/directory/agents.yaml", encoding="utf-8"))
print("agents.yaml OK, count:", len(d["agents"]))
