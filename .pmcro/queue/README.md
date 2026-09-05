# queue

Durable Seed Intent inbox.

- Claim policy is defined in `runtime/config.yaml` (default: highest-priority-then-FIFO).
- Queue items use a declared schema and remain separate from skill packages.
- Orchestrator is the only role that claims items and opens cycles from them.
