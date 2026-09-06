import subprocess, sys
from pathlib import Path

SPECS = sorted(Path("plugins/pmcro-omode/specs").glob("*.spec.yaml"))
SCRATCH = Path(".pmcro/state/_scratch_omode_rt")

results = []
for spec in SPECS:
    r = subprocess.run(
        [sys.executable, "plugins/pmcro-omode/scripts/render_strategy.py",
         "--spec", str(spec), "--output-root", str(SCRATCH)],
        capture_output=True, text=True,
    )
    strategy_id = spec.name.replace(".spec.yaml", "")
    real_file = Path(f"plugins/pmcro-omode/agents/{strategy_id}.md")
    gen_file = SCRATCH / f"{strategy_id}.md"
    if r.returncode != 0 or not gen_file.exists():
        results.append((strategy_id, "GENERATE_FAIL", r.stdout + r.stderr))
        continue
    diff = subprocess.run(
        ["git", "diff", "--no-index", "--stat", str(real_file), str(gen_file)],
        capture_output=True, text=True,
    )
    results.append((strategy_id, "OK", diff.stdout.strip()))

fails = [r for r in results if r[1] != "OK"]
print(f"Total specs: {len(results)}")
print(f"Generate failures: {len(fails)}")
for sid, status, detail in results:
    line_count = 0
    if status == "OK" and detail:
        # parse "1 file changed, N insertions(+), M deletions(-)"
        line_count = detail
    print(f"{status:15s} {sid:35s} {line_count if status=='OK' else detail[:200]}")
