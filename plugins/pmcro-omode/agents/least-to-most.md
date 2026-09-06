---
id: least-to-most
package: pmcro-omode
kind: strategy
family: "Family 1 — Linear / Sequential"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive]
  operational_methods: [linear_cot, branching_search]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# least-to-most

Migrated from `.agents/skills/reasoning/least-to-most/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Reduce difficulty by solving easier sub-questions that build toward the target.

## When to Use
- Multi-hop questions, layered analysis, complex planning

## When Not to Use
- Single-hop factual or arithmetic questions

## Workflow
1. State the hard target.
2. List ordered easier sub-questions.
3. Answer easiest to hardest, using prior answers.
4. Only then solve the original.
5. Make dependencies explicit.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "least-to-most"`, `steps` (each
sub-question and its answer, in order), `result`.
