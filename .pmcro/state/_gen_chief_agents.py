from pathlib import Path

# (id, code, display_name, description) - description copied verbatim from
# .pmcro/directory/agents.yaml, read in full earlier this session.
CHIEFS = [
    ("pmcro-chief-executive-officer", "ceo", "Chief Executive Officer",
     "Macro-level intent governance for company-wide direction and cross-Chief prioritization. Selects operating mode and reasoning strategy before Planner handoff. Domain execution still runs through the five-role cycle."),
    ("pmcro-chief-technology-officer", "cto", "Chief Technology Officer",
     "Macro-level intent governance for platform architecture, host-capability decisions, and technology strategy. Selects operating mode and reasoning strategy before Planner handoff. Domain execution still runs through the five-role cycle."),
    ("pmcro-chief-learning-officer", "clo", "Chief Learning Officer",
     "Macro-level intent governance for learning, curriculum design, skill development, and educator-facing strategy across the AI Agent Company. Selects operating mode and reasoning strategy from the catalog before Planner handoff. Domain execution still runs through the Plan-Make-Check-Reflect cycle."),
    ("pmcro-chief-compliance-officer", "cco", "Chief Compliance Officer",
     "Macro-level intent governance for regulatory compliance, policy adherence, and audit-readiness decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step compliance decisions."),
    ("pmcro-chief-data-officer", "cdo", "Chief Data Officer",
     "Macro-level intent governance for data strategy, data-quality standards, and analytics/model-governance prioritization across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step data decisions."),
    ("pmcro-chief-financial-officer", "cfo", "Chief Financial Officer",
     "Macro-level intent governance for financial strategy, budget allocation, cost governance, and investment prioritization across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when evaluating multi-step financial decisions."),
    ("pmcro-chief-human-resources-officer", "chro", "Chief Human Resources Officer",
     "Macro-level intent governance for people strategy, org design, hiring prioritization, and culture/talent decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step people decisions."),
    ("pmcro-chief-information-security-officer", "ciso", "Chief Information Security Officer",
     "Macro-level intent governance for information security posture, threat response prioritization, and risk-acceptance decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step security decisions."),
    ("pmcro-chief-marketing-officer", "cmo", "Chief Marketing Officer",
     "Macro-level intent governance for brand strategy, positioning, campaign direction, and audience-facing narrative across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when shaping multi-step campaigns or messaging."),
    ("pmcro-chief-operating-officer", "coo", "Chief Operating Officer",
     "Macro-level intent governance for operational execution, process design, resource orchestration, and cross-team throughput across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step operational problems."),
    ("pmcro-chief-product-officer", "cpo", "Chief Product Officer",
     "Macro-level intent governance for product strategy, roadmap prioritization, and feature-scoping decisions across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when scoping multi-step product decisions."),
    ("pmcro-chief-revenue-officer", "cro", "Chief Revenue Officer",
     "Macro-level intent governance for revenue strategy, pricing decisions, and sales/partnership prioritization across the AI Agent Company. Domain execution still runs through the Plan-Make-Check-Reflect cycle. Selects reasoning strategies from the reasoning catalog when resolving multi-step revenue decisions."),
]

TEMPLATE = '''---
name: {id}
description: {description}
tools: Read, Grep, Glob, Bash
---

# {display_name} Agent

Composes `.agents/skills/{id}` (skill) and `plugins/pmcro-csuite/agents/{code}.md` +
`plugins/pmcro-csuite/omode/{code}.yaml` (governance contract and reasoning-mode map).
This file is the delegation layer — it does not restate the trigger-to-strategy table,
which lives in `omode/{code}.yaml` and would drift if copied here. Read
`plugins/pmcro-csuite/agents/{code}.md` for the full workflow.

## Economic Rationale

Selecting a reasoning strategy and scope at this layer, before Planner ever sees the
seed, is what keeps every cycle in this domain from re-deriving its own approach from
first principles. This is the same argument as the lifecycle Planner's rationale
(reject or scope a request before Maker spends real execution cost) applied one step
earlier: a Chief hands Planner an already-scoped `<Domain>IntentFrame` with a
`selected_reasoning_strategy` drawn from `omode/{code}.yaml`'s trigger table, instead of
an unscoped seed that Planner would otherwise have to interpret domain-blind.

## When to delegate here

{description}

## When not to

- Core lifecycle operations (orchestrate / plan / make / check / reflect).
- Domain tasks that belong to a different Chief — route to that Chief instead.
- Domain execution itself — that stays with Maker and Checker; this persona governs
  intent only.

## Constraints

`plugins/pmcro-csuite/agents/{code}.md` is the source of truth. In summary: may
`govern-domain-intent, select-reasoning-strategy`; may not `execute-provider-action,
seal-cycle, issue-disposition, rewrite-laws`. No Edit/Write tool access — this agent
governs intent only, never cross-Chief decisions or performance data invented without
evidence.
'''

out_dir = Path(".agents/agents")
written = []
for id_, code, display_name, description in CHIEFS:
    content = TEMPLATE.format(id=id_, code=code, display_name=display_name, description=description)
    out_path = out_dir / f"{id_}.md"
    out_path.write_text(content, encoding="utf-8")
    written.append(str(out_path))

print(f"Wrote {len(written)} files:")
for w in written:
    print(" -", w)
