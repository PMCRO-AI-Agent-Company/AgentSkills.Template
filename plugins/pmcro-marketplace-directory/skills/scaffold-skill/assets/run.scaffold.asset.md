# Run Contract — scaffold-skill

1. Read the spec file.
2. Parse as YAML or JSON.
3. Validate against the scaffold-spec schema.
4. Run the refuse checks (placeholders, paths, capabilities).
5. If any check fails → emit reject result and stop. No files written.
6. For each packaging target:
   - Select the template set
   - Render with the spec values
   - Write only under the declared (repo-relative) path
7. If `--register` was given, call the register-agent logic to upsert `.pmcro/directory/agents.yaml`.
8. Return the success result envelope.
