import subprocess, sys, yaml

base = "plugins/pmcro-marketplace-directory/skills/scaffold-skill"
with open(f"{base}/eval/eval.yaml", encoding="utf-8") as f:
    ev = yaml.safe_load(f)

script = f"{base}/scripts/scaffold.py"
results = []
for t in ev["spec"]["trials"]:
    fixture = f"{base}/eval/{t['fixture']}"
    proc = subprocess.run(
        [sys.executable, script, "--spec", fixture, "--dry-run"],
        capture_output=True, text=True,
    )
    exp = t["expect"]
    ok = proc.returncode == exp["exit_code"]
    for s in exp.get("stdout_contains", []):
        if s not in proc.stdout:
            ok = False
    results.append((t["id"], ok, proc.returncode, proc.stdout.strip()[:200]))

all_ok = all(r[1] for r in results)
for tid, ok, rc, out in results:
    print(("PASS " if ok else "FAIL "), tid, "rc=", rc)
print()
print("ALL PASS" if all_ok else "SOME FAILED")
