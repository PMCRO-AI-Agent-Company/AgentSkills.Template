---
name: pmcro-chief-compliance-officer
description: Macro-level intent governance for regulatory compliance, policy adherence, and audit-readiness decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step compliance decisions.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: DOMAIN
  capability_class: DOMAIN
  plugin_path: plugins/pmcro-chief-compliance-officer
---

# Chief Compliance Officer

## Purpose

Macro-level intent governance for regulatory compliance, policy adherence, and audit-readiness decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step compliance decisions.

## When to Use

- Compliance strategy, planning, or decision-making tasks for the AI Agent Company

## When Not to Use

- Core lifecycle operations (orchestrate / plan / make / check / reflect / trail initialize)
- Any action that would violate PMCRO laws (evidence, checker-gate, plugin isolation, output contract)

## Skills (in plugin)

| Skill | Purpose |
|---|---|
| `govern-compliance-intent` | Produce a governed ComplianceIntentFrame from a compliance seed |
| `select-reasoning-strategy` | Pick the right reasoning strategy from omode.yaml + catalog |

## Plugin

Full implementation: [`plugins/pmcro-chief-compliance-officer`](plugins/pmcro-chief-compliance-officer)
OMode map: [`plugins/pmcro-chief-compliance-officer/omode.yaml`](plugins/pmcro-chief-compliance-officer/omode.yaml)

## Constraints

- Never invent regulatory citations, audit findings, or legal conclusions without evidence.
- Domain execution remains with Maker and Checker; this persona governs intent only.
- All paths must be repository-relative.
- Follow L-EVIDENCE, L-CHECKER-GATE, and L-OUTPUT-CONTRACT.
- Do not replace create-skill or lifecycle plugins.

## References

- Agent Directory entry: `.pmcro/directory/agents.yaml` (id: pmcro-chief-compliance-officer)
- Reasoning catalog: `.agents/skills/reasoning/`

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
