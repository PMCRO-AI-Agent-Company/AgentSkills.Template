---
id: tree-of-thoughts
package: reasoning-strategy
kind: strategy
family: "Family 2 — Search / Exploration"
output_schema:
  $ref: ../schemas/reasoning-trace-frame.schema.json
laws: [L-EVIDENCE, L-CHECKER-GATE, L-PLUGIN-ISOLATION, L-OUTPUT-CONTRACT]
permissions:
  may: [apply-reasoning-strategy]
  mayNot: [execute-provider-action, seal-cycle, issue-disposition, rewrite-laws, select-reasoning-strategy]
reasoning:
  logical_paradigms: [deductive, inductive]
  operational_methods: [branching_search]
  domain_capabilities: [strategic_agentic, multi_hop_relational]
---
# tree-of-thoughts

Migrated from `.agents/skills/reasoning/tree-of-thoughts/SKILL.md` (v1.0.0) into
the single-file `reasoning-strategy/` convention.

## Purpose
Generate and evaluate multiple partial solution paths before committing,
selecting the most promising branch.

## When to Use
- Design, planning, or puzzles where one incorrect assumption derails the
  whole solution
- Problems where it is unclear which approach will succeed without partial
  exploration

## When Not to Use
- Latency-critical tasks
- Simple linear problems with a single obvious path

## Workflow
1. Restate the goal and identify the key decision points.
2. Generate 2–4 distinct partial solution paths (branches) for the first
   decision point.
3. Evaluate each branch: score feasibility, correctness, and alignment with
   the goal.
4. Prune weak branches; extend the 1–2 best branches to the next decision point.
5. Repeat steps 2–4 until one branch reaches a complete solution.
6. State the final answer from the winning branch; briefly note why it was
   selected.

## Validation
- At least two branches were explored before a path was selected
- Pruning decisions were justified against explicit evaluation criteria
- Final answer is traceable to the selected branch

## Output
Return a `ReasoningTraceFrame`: `strategy_id: "tree-of-thoughts"`, `steps`
(branches generated, evaluated, pruned, and the winning path), `result`.
