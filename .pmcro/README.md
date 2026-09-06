# .pmcro — PMCR-O Colony Runtime Framework

This directory is the **authoritative governance and evidence layer** for a PMCR-O (Planner → Maker → Checker → Reflector → Orchestrator) colony.

It is intentionally portable: drop it into any repository that wants governed, self-correcting agent cycles with durable trails.

## Core Loop

```text
Human / Seed Intent
        ↓
   Orchestrator          (sole dispatch authority — opens cycle, mints/links trail)
        ↓
     Planner             (produces PlanFrame + success criteria)
        ↓
      Maker              (executes one step at a time → MakeStep evidence)
        ↓
     Checker             (independent evaluation against criteria)
        ↓
    Reflector            (disposition, optional next seed, SEAL — only role that seals)
        ↓
   next cycle (or done)
```

## Directory Map

| Path | Purpose | Status |
|------|---------|--------|
| `laws/` | Fixed, non-negotiable rule IDs (`L-EVIDENCE`, `L-CHECKER-GATE`, …) | Active |
| `policies/` | Configurable posture (permissions, execution, network, security) | Active |
| `runtime/` | Output contract, config toggles, deterministic validator | Active |
| `queue/` | Seed-intent inbox (durable) | Ready |
| `trails/` | Class-B GUID-folder evidence products (one JSONL per phase) | Ready |
| `capabilities/` | Stable capability contracts (not tool names) | Registry shape |
| `providers/` | Who implements a capability | Registry shape (empty until real) |
| `mcp/` | MCP-specific routing | Registry shape (empty until real) |
| `config/` | Runtime parameters | Shape |
| `secrets/` | Secret *references only* — never values | Shape |
| `state/` | Cross-cycle workflow state (not shared memory) | Shape |
| `memory/` | Promoted durable knowledge | Shape |
| `agent-memory/` | Per-agent scoped memory | Shape |
| `frames/` | Frame-type documentation | Shape |
| `evidence/` | Evidence artifacts | Shape |
| `artifacts/` | Build / output artifacts | Shape |
| `evaluation/` | Skill / cycle evaluation results | Shape |
| `workflows/` | Declarative workflow notes | Shape |
| `constraints/` | Earned / promoted constraints | Shape |

## Fixed Laws (summary)

- **L-EVIDENCE** — completion requires evidence
- **L-CHECKER-GATE** — checker must pass before completion
- **L-STATE-MEMORY** — workflow state is not shared memory
- **L-AGENT-MEMORY** — agent memory is scoped to agent
- **L-CAPABILITY** — agents use skills and tools for capabilities
- **L-ORCHESTRATION** — orchestrator owns routing, not domain implementation
- **L-RESEARCH** — version-sensitive decisions require current authoritative evidence
- **L-PLUGIN-ISOLATION** — plugin skills require active binding / open cycle before TYPE1 mutations
- **L-OUTPUT-CONTRACT** — governed results must satisfy the runtime output contract

## Conventions

1. No absolute, host-specific, or drive-letter paths in system-authored content. References are repository-relative.
2. **Trail-as-Product**: every durable trail frame is an instance of the declared trail-frame schema, never hand-typed prose.
3. Every phase file has exactly one owning role; nothing else appends to it.
4. Log incrementally as work happens, not as an end-of-cycle reconstruction.
5. Sealed trails are immutable. Corrections use a new trail that may reference the earlier one via a next seed.
6. Empty provider / capability registries are preferable to invented integrations.
7. Secrets are references only; never values inside `.pmcro/`.
8. Never trust a deterministic script without executing both success and failure paths.

## How to use

1. Place this `.pmcro/` at the root of your project (or under a known runtime root).
2. Install the consolidated `pmcro` lifecycle plugin (Orchestrator, Planner, Maker, Checker, Reflector in one package — see `plugins/pmcro/plugin.json`) or an equivalent skill set. `pmcro-trail` is deprecated: sealing/trail materialization is a Reflector permission (`seal-cycle`), not a separate plugin. *(Corrected 2026-09-06 — this line previously described 6 separate plugins, one of them deprecated.)*
3. Open cycles only through the Orchestrator.
4. Seal only through the Reflector after a Checker PASS.
5. Validate any claimed completion with `runtime/validate_output_contract.py`.

## Federation

Looking for "Federation" / "Federation Board"? Those terms are not used in this repo. The functional role they'd describe - domain governance above the shared five-role cycle - is already built as the C-Suite layer (`plugins/pmcro-csuite/`, 12 Chief personas). See `design/ADR-federation-csuite-decision-2026-09-06.md` for why that layer is staying as-is rather than being renamed, and where a Federation Board would attach if one is ever actually needed.

## Provenance

Generated as a clean, portable runtime framework derived from study of the canonical PMCR-O colony repository (PMCRO-AI-Agent-Company/pmcr-o). All laws, policy shapes, output contract, and conventions are preserved; stack-specific claims (MAF, Aspire, concrete providers) have been removed so the framework remains honest about what is not yet wired.
