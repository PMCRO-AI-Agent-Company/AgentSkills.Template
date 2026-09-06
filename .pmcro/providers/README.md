# providers

Registry of who implements a capability.

**Convention:** one flat YAML file per provider (matches `capabilities/`'s
pattern — see `capabilities/hyperlight-codeact.yaml`), not a single
aggregate `registry.yaml`. Add a summary table here (id | capability |
status | file) once a real provider file exists.

Missing provider capability must produce an escalated governed result, never an invented integration.
