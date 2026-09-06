---
name: tree-of-thoughts
description: Explore several partial solutions in parallel, then select the best. USE FOR design, puzzles, or problems with brittle single-path answers. DO NOT USE when latency is critical.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [deductive, inductive]
    operational_methods: [branching_search]
    domain_capabilities: [strategic_agentic, multi_hop_relational]
---

# tree-of-thoughts

## Purpose
Generate and evaluate multiple partial solution paths before committing, selecting the most promising branch.

## When to Use
- Design, planning, or puzzles where one incorrect assumption derails the whole solution
- Problems where it is unclear which approach will succeed without partial exploration

## When Not to Use
- Latency-critical tasks
- Simple linear problems with a single obvious path

## Workflow
1. Restate the goal and identify the key decision points.
2. Generate 2–4 distinct partial solution paths (branches) for the first decision point.
3. Evaluate each branch: score feasibility, correctness, and alignment with the goal.
4. Prune weak branches; extend the 1–2 best branches to the next decision point.
5. Repeat steps 2–4 until one branch reaches a complete solution.
6. State the final answer from the winning branch; briefly note why it was selected.

## Validation
- At least two branches were explored before a path was selected
- Pruning decisions were justified against explicit evaluation criteria
- Final answer is traceable to the selected branch

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
