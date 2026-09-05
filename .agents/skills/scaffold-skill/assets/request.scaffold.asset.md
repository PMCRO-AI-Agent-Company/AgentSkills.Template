# Request Contract — scaffold-skill

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
|------|----------|--------------|
| `--spec` | yes | Path to an AgentScaffoldSpec YAML or JSON file (repo-relative) |
