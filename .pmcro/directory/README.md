# Agent Directory System

Canonical, schema-validated catalog of every agent, persona, plugin, and harness known to the colony.

- **Source of truth**: `agents.yaml`
- **Schema**: `agents.schema.json`
- **Design authority**: `../design/ADR-pmcro-agent-directory-and-marketplace.md`

Marketplace manifests (`.agents/plugins/marketplace.json`, Claude/Cursor/Codex plugin catalogs, etc.) are **generated views** of this directory. Do not hand-edit them as the primary store.

Directory mutations are TYPE1 and must be evidenced inside a sealed PMCR-O trail.
