---
id: template-filling
package: pmcro-omode
kind: strategy
family: "Family 7 — Framing & Normative"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, inductive]
  operational_methods: [linear_cot]
  domain_capabilities: [common_sense, strategic_agentic, multi_hop_relational]
---
# template-filling

Migrated from `.agents/skills/reasoning/template-filling/SKILL.md` (v1.0.0)
into the single-file `reasoning-strategy/` convention.

## Purpose
Apply a predefined analytical template to ensure no critical slot is missed
and outputs are consistently structured for downstream consumption.

## When to Use
- Recurring structured reviews (incident post-mortems, code reviews, risk
  assessments)
- Domain advice or policy analysis with a known required output shape
- Outputs consumed by automated pipelines that expect a fixed schema

## When Not to Use
- Open-ended creative tasks where rigid structure would constrain quality
- Simple factual lookups that do not benefit from templating

## Workflow
1. Identify or define the template: enumerate all required slots and their
   expected content type.
2. Restate the goal in terms of the template (what is being analyzed).
3. Fill each slot in order, clearly labeling each section.
4. If a slot cannot be filled due to missing information, mark it explicitly
   as `N/A — [reason]`.
5. Review: ensure all required slots are populated or explicitly marked.
6. Deliver the completed template as the output.

## Validation
- All required template slots are present in the output
- Missing slots are explicitly marked with a reason, not silently omitted
- Output labels match the template's defined slot names

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "template-filling"`, `steps`
(one entry per slot filled or marked N/A), `result`.
