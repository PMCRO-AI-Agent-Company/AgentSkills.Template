# runtime

- `validate_output_contract.py` — result envelope validation
- `queue_runtime.py` — command-style queue + checkpoints

```bash
python .pmcro/runtime/queue_runtime.py status
python .pmcro/runtime/queue_runtime.py claim
python .pmcro/runtime/queue_runtime.py checkpoint --note "..."
python .pmcro/runtime/queue_runtime.py complete
```
