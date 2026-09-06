---
id: socratic-questioning
package: pmcro-omode
kind: strategy
family: "Family 6 — Interactive / Grounded"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [inductive, abductive]
  operational_methods: [iterative_self_reflective]
  domain_capabilities: [common_sense, multi_hop_relational]
---
# socratic-questioning

Migrated from `.agents/skills/reasoning/socratic-questioning/SKILL.md`
(v1.0.0) into the single-file `reasoning-strategy/` convention.

## Purpose
Surface hidden ambiguities and underspecified requirements through targeted,
minimal questions before committing to a solution.

## When to Use
- User requests that are vague, contradictory, or missing critical constraints
- Problems where answering the wrong question wastes significant effort
- Tool or API interactions where incorrect parameters have high cost

## When Not to Use
- Well-specified problems where all necessary information is present
- Time-critical situations where any answer is better than asking

## Workflow
1. Restate the problem as currently understood.
2. Identify the 2–4 most critical ambiguities or missing pieces of
   information.
3. Formulate one precise, non-leading question per ambiguity.
4. Ask only the most critical questions (avoid overwhelming the user).
5. Incorporate the answers to update the problem statement.
6. Proceed to solve once the problem is sufficiently specified.

## Validation
- Questions were precise and non-leading
- Each question targeted a distinct ambiguity
- The solution phase began only after critical ambiguities were resolved

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "socratic-questioning"`, `steps`
(restatement, questions asked, updated problem statement), `result`.
