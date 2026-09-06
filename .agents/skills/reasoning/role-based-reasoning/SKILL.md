---
name: role-based-reasoning
description: Adopt a specific expert role to shape perspective and priorities. USE FOR domain-specialized advice. DO NOT USE when a neutral general answer is better.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [analogical, deductive]
    operational_methods: [linear_cot]
    domain_capabilities: [strategic_agentic, common_sense]
---

# role-based-reasoning

## Purpose
Use a coherent professional perspective to improve relevance and priorities.

## When to Use
- Domain advice (security, product, legal-style analysis, etc.)

## When Not to Use
- Neutral factual lookup with no domain framing needed

## Workflow
1. Name the role and its primary goals/constraints.\n2. Restate the problem from that role’s view.\n3. Reason using that role’s typical methods and priorities.\n4. Give recommendations consistent with the role.\n5. Optionally note how a different role might disagree.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
