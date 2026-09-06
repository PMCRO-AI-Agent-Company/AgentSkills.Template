# runtime

- `validate_output_contract.py` — result envelope validation
- `queue_runtime.py` — command-style queue + checkpoints
- `trail_runtime.py` — trail lifecycle CLI (open/plan/make/check/reflect/status)

```bash
python .pmcro/runtime/queue_runtime.py status
python .pmcro/runtime/queue_runtime.py claim
python .pmcro/runtime/queue_runtime.py checkpoint --note "..."
python .pmcro/runtime/queue_runtime.py complete
```

```bash
python .pmcro/runtime/trail_runtime.py open --seed "..." [--host NAME]
echo '{...plan...}'    | python .pmcro/runtime/trail_runtime.py plan
echo '{...make...}'    | python .pmcro/runtime/trail_runtime.py make
echo '{"verdict":"PASS"|"FAIL", ...}' | python .pmcro/runtime/trail_runtime.py check
echo '{"disposition":"SEAL"|"RETRY"|"BLOCKED", ...}' | python .pmcro/runtime/trail_runtime.py reflect
python .pmcro/runtime/trail_runtime.py status [--trail ID]
```

`trail_runtime.py` is mechanical only — it does not decide plan/make/check/
reflect *content*, an LLM or agent still supplies that. It replaces hand-
copying trail JSON files with a single command per phase, and enforces two
real gates: `check` rejects any verdict other than `PASS`/`FAIL`, and
`reflect` refuses to `SEAL` unless the trail's own `04-check.json` verdict
is `PASS` (L-CHECKER-GATE). On `SEAL` it also auto-completes the active
queue claim, if one exists, via `queue_runtime.py complete`.
