# policies

Configurable governance posture. Policies implement *how* the colony behaves under the fixed laws.

| File | Kind | Purpose |
|------|------|---------|
| `permissions.yaml` | PermissionPolicy | What each role may / may not do |
| `execution.yaml` | ExecutionPolicy | Defaults + capability execution rules + minimum evidence |
| `network.yaml` | NetworkPolicy | Default-deny network posture |
| `security.yaml` | SecurityPolicy | Trust, secrets, approvals, provenance |

Policies may be tightened or relaxed by humans. Laws may not.
