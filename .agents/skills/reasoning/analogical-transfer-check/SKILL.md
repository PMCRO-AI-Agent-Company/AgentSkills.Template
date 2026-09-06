---
name: analogical-transfer-check
description: After using an analogy, explicitly test where it fails. USE FOR any analogical argument. DO NOT USE when no analogy was used.
license: Apache-2.0
metadata:
  version: "1.0.0"
  reasoning:
    logical_paradigms: [analogical, causal_counterfactual]
    operational_methods: [iterative_self_reflective]
    domain_capabilities: [common_sense, multi_hop_relational]
---

# analogical-transfer-check

## Purpose
Prevent over-transfer by stress-testing the analogy’s limits.

## When to Use
- After any solution or explanation that relied on analogy

## When Not to Use
- Direct solutions that did not use analogy

## Workflow
1. Restate the analogy mapping.\n2. List critical assumptions of the source domain.\n3. Check each assumption in the target domain.\n4. Mark broken mappings.\n5. Adjust or discard the conclusion accordingly.

## Validation
- Steps above were followed in order
- Final answer is grounded in the produced intermediate work

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
