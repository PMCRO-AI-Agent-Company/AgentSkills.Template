---
name: uncertainty-decomposition
description: Explicitly separate knowns, unknowns, and assumptions before reasoning. USE FOR high-stakes or contested decisions where unstated assumptions cause errors. DO NOT USE for routine lookups with full information.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, abductive]
    operational_methods: [linear_cot]
    domain_capabilities: [multi_hop_relational, common_sense, strategic_agentic]
---

# uncertainty-decomposition

## Purpose
Make uncertainty explicit by separating what is known, what is unknown, and what is assumed before attempting a solution.

## When to Use
- High-stakes decisions with incomplete information
- Analysis where hidden assumptions could invalidate conclusions
- Situations where stakeholders need to understand confidence levels

## When Not to Use
- Complete-information problems with deterministic answers
- Simple factual lookups where uncertainty is negligible

## Workflow
1. Restate the goal.
2. List **Knowns**: facts that are established and reliable.
3. List **Unknowns**: information that is missing and would change the answer if known.
4. List **Assumptions**: beliefs being treated as true for the purpose of this analysis, with an explicit confidence level (high / medium / low).
5. Reason to a conclusion using only the knowns and stated assumptions.
6. Flag which assumptions most critically affect the conclusion and what evidence would upgrade or invalidate them.

## Validation
- Knowns, Unknowns, and Assumptions were listed separately before reasoning began
- Conclusion is explicitly conditional on stated assumptions
- Key assumptions affecting the conclusion are flagged with confidence levels
