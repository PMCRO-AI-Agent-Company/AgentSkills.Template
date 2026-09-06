---
id: role-based-reasoning
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
  logical_paradigms: [analogical, deductive]
  operational_methods: [linear_cot]
  domain_capabilities: [strategic_agentic, common_sense]
---
# role-based-reasoning

Migrated from `.agents/skills/reasoning/role-based-reasoning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Use a coherent professional perspective to improve relevance and priorities.

## When to Use
- Domain advice (security, product, legal-style analysis, etc.)

## When Not to Use
- Neutral factual lookup with no domain framing needed

## Workflow
1. Name the role and its primary goals/constraints.
2. Restate the problem from that role's view.
3. Reason using that role's typical methods and priorities.
4. Give recommendations consistent with the role.
5. Optionally note how a different role might disagree.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "role-based-reasoning"`, `steps`
(the role and reasoning from its perspective), `result`.
