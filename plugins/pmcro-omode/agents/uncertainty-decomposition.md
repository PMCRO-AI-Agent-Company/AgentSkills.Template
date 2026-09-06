---
id: uncertainty-decomposition
package: pmcro-omode
kind: strategy
family: "Family 3 — Iterative / Reflective"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, abductive]
  operational_methods: [linear_cot]
  domain_capabilities: [multi_hop_relational, common_sense, strategic_agentic]
---
# uncertainty-decomposition

Migrated from `.agents/skills/reasoning/uncertainty-decomposition/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Make uncertainty explicit by separating what is known, what is unknown, and
what is assumed before attempting a solution.

## When to Use
- High-stakes decisions with incomplete information
- Analysis where hidden assumptions could invalidate conclusions
- Situations where stakeholders need to understand confidence levels

## When Not to Use
- Complete-information problems with deterministic answers
- Simple factual lookups where uncertainty is negligible

## Workflow
1. Restate the goal.
2. List Knowns: facts that are established and reliable.
3. List Unknowns: information that is missing and would change the answer
   if known.
4. List Assumptions: beliefs treated as true for this analysis, with an
   explicit confidence level (high/medium/low).
5. Reason to a conclusion using only the knowns and stated assumptions.
6. Flag which assumptions most critically affect the conclusion and what
   evidence would upgrade or invalidate them.

## Validation
- Knowns, Unknowns, and Assumptions were listed separately before reasoning
- Conclusion is explicitly conditional on stated assumptions
- Key assumptions affecting the conclusion are flagged with confidence levels

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "uncertainty-decomposition"`,
`steps` (knowns/unknowns/assumptions and the conditional conclusion), `result`.
