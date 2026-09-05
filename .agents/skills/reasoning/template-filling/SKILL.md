---
name: template-filling
description: Fill a fixed set of analysis slots systematically. USE FOR recurring structured reviews, domain advice, or policy questions with a known output shape. DO NOT USE for neutral factual lookups with no required structure.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, inductive]
    operational_methods: [linear_cot]
    domain_capabilities: [common_sense, strategic_agentic, multi_hop_relational]
---

# template-filling

## Purpose
Apply a predefined analytical template to ensure no critical slot is missed and outputs are consistently structured for downstream consumption.

## When to Use
- Recurring structured reviews (incident post-mortems, code reviews, risk assessments)
- Domain advice or policy analysis with a known required output shape
- Outputs consumed by automated pipelines that expect a fixed schema

## When Not to Use
- Open-ended creative tasks where rigid structure would constrain quality
- Simple factual lookups that do not benefit from templating

## Workflow
1. Identify or define the template: enumerate all required slots and their expected content type.
2. Restate the goal in terms of the template (what is being analyzed).
3. Fill each slot in order, clearly labeling each section.
4. If a slot cannot be filled due to missing information, mark it explicitly as `N/A — [reason]`.
5. Review: ensure all required slots are populated or explicitly marked.
6. Deliver the completed template as the output.

## Validation
- All required template slots are present in the output
- Missing slots are explicitly marked with a reason, not silently omitted
- Output labels match the template's defined slot names
