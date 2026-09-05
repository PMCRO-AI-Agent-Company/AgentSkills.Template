---
name: register-agent
description: Upsert an agent entry into the PMCRO Agent Directory (.pmcro/directory/agents.yaml). USE FOR recording a newly scaffolded or adopted agent. DO NOT USE for creating skill packages (use scaffold-skill) or for lifecycle core plugins.
metadata:
  version: "0.1.0-mvp"
  tier: GOVERNANCE
---

# register-agent (MVP)

## Purpose

Keep the Agent Directory as the single source of truth. Called by `scaffold-skill --register` or directly when adopting an existing agent.

## Rules

- Never invent capabilities.
- Never write absolute or drive-letter paths.
- Prefer update-in-place over duplicate entries (MVP currently appends only if missing).
- Directory mutations are TYPE1 and should be evidenced in a trail.
