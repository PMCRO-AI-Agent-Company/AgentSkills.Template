import subprocess, sys

with open(".pmcro/state/_seed_agent_layer.txt", encoding="utf-8") as f:
    seed = f.read().strip()

result = subprocess.run(
    [sys.executable, ".pmcro/runtime/trail_runtime.py", "open", "--seed", seed, "--host", "pmcr-o"],
    capture_output=True, text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
