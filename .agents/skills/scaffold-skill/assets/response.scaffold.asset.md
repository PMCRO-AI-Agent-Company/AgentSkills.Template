# Response Contract — scaffold-skill

## Success (status: ok)

```json
{
  "status": "ok",
  "action": "SCAFFOLD",
  "agent_id": "example-domain-analyst",
  "generated": [
    { "target": "agentskills", "path": ".agents/skills/example-domain-analyst" }
  ],
  "directory_updated": false,
  "trail_id": null
}
```

Steps 1–8 that produce this result:

1. Read the spec file.
2. Parse as YAML or JSON.
3. Validate against the scaffold-spec schema.
4. Run the refuse checks (placeholders, paths, capabilities) — see Failure below.
5. If any check fails → emit the Failure result and stop. No files written.
6. For each packaging target: select the template set, render with the spec values, write only
   under the declared (repo-relative) path.
7. If `--register` was given, call the register-agent logic to upsert
   `.pmcro/directory/agents.yaml`.
8. Return this success result envelope.

## Failure (status: reject)

```json
{
  "status": "reject",
  "reason": "schema-validation | placeholder-token | absolute-path | unevidenced-capability",
  "details": ["…"]
}
```

The skill must refuse (and write nothing) when:

| Condition | Reason code |
|-----------|-------------|
| Spec fails JSON Schema validation | `schema-validation` |
| `id` or skill name contains placeholder tokens (`TODO`, `FIXME`, `xxx`, `changeme`, `placeholder`, `tbd`) | `placeholder-token` |
| Any path contains a drive letter (`P:\`, `C:\`) or absolute host path | `absolute-path` |
| Declared capability does not exist in the capability registry and is not explicitly marked planned | `unevidenced-capability` |
| Packaging target is unknown | `unknown-target` |
| Output path would escape the repository root | `path-escape` |

Refusal is a successful execution of the skill's contract; it is not an error in the runtime
sense. The caller receives this structured reject result, same envelope shape as Success above,
discriminated by `status`.
