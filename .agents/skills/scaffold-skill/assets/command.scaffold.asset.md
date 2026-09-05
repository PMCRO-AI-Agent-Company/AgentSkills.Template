# Command Contract — scaffold-skill

## Invocation

```text
/pmcro-marketplace-directory:scaffold-skill run --spec <path>
```

Optional flags (MVP):

- `--register` — also upsert the Agent Directory entry
- `--dry-run` — validate and show planned writes without writing
- `--output-root <rel-path>` — override the root for generated packages (must stay repo-relative)

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `--spec` | yes | Path to an AgentScaffoldSpec YAML or JSON file (repo-relative) |

## Success Result Shape

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

## Rejection Shape

```json
{
  "status": "reject",
  "reason": "schema-validation | placeholder-token | absolute-path | unevidenced-capability",
  "details": ["…"]
}
```
