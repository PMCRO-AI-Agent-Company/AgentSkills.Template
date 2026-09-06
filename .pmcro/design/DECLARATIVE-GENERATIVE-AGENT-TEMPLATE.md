# PMCRO Generative Declarative Agent Template

**Status:** Base template
**Purpose:** Single declarative source for generating governed agent/persona/domain-skill packages.

## Design rule

Declare intent once. Generate projections. Do not hand-maintain runtime-specific copies.

```text
AgentScaffoldSpec
      │
      ├── validate against schema + PMCRO laws
      │
      ├── resolve capabilities / providers
      │
      ├── select agent template
      │
      └── render declared projections
             ├── Agent Skills / SKILL.md
             ├── MAF inline/class projection
             └── host/plugin projections
```

## Canonical source

`AgentScaffoldSpec` is the design-time contract. The Agent Directory records the resulting identity, ownership, capabilities, skills, packaging targets, and lifecycle state.

The scaffolder is a renderer, not an autonomous lifecycle engine. Orchestrator owns cycle dispatch; Planner defines work; Maker executes; Checker independently verifies; Reflector disposes and seals.

## Base declaration

```yaml
apiVersion: pmcro.ai/v1
kind: AgentScaffoldSpec
metadata:
  id: example-domain-agent
  kind: domain
  display_name: Example Domain Agent
spec:
  description: >
    Performs one well-defined domain responsibility and emits a structured,
    evidence-grounded result for downstream PMCR-O execution.
  owner_role: planner
  capabilities: []
  laws:
    - L-EVIDENCE
    - L-PLUGIN-ISOLATION
    - L-OUTPUT-CONTRACT
  permissions:
    may:
      - read-approved-input
      - emit-governed-result
    mayNot:
      - seal-cycle
      - rewrite-laws
  output:
    schema_ref: .pmcro/design/schemas/agent-output.schema.json
    contract: .pmcro/runtime/output-contract.md
  reasoning:
    allowed_families: []
    default: null
  skills:
    - name: execute-domain-task
      tier: DOMAIN
      description: Execute the declared domain responsibility.
  packaging:
    - target: agentskills
      path: .agents/skills/example-domain-agent
  constraints:
    - Never invent capabilities or providers.
    - Never emit absolute or drive-letter paths.
    - Preserve evidence for material claims and side effects.
    - Keep generated projections subordinate to this declaration.
  evaluation:
    must_pass:
      - schema-validation
      - capability-resolution
      - output-contract-validation
      - placeholder-refusal
      - absolute-path-refusal
```

## Template families

| `metadata.kind` | Generated form | Primary owner |
|---|---|---|
| `lifecycle` | PMCR-O role + command skill | lifecycle governance |
| `persona` | governed persona / Chief | named owner role |
| `domain` | domain skill / agent | declared owner role |
| `tool` | capability-facing skill | declared owner role |
| `marketplace-scaffold` | generator / registry skill | planner |
| `harness` | evaluation or red-team harness | checker |

## Generation contract

The renderer must execute these gates in order:

1. Parse the declaration.
2. Validate required structure and identifiers.
3. Reject placeholders and host-specific paths.
4. Resolve every declared capability against `.pmcro/capabilities/` or an explicitly declared planned state.
5. Validate laws and permission boundaries against the generated role.
6. Resolve the output schema and runtime output contract.
7. Render only the packaging targets explicitly requested by the declaration.
8. Register or update the Agent Directory only when requested.
9. Emit a machine-readable generation result suitable for a PMCR-O evidence frame.

No renderer step opens a cycle, executes domain work, judges its own output, or seals a trail.

## Projection invariant

```text
             ONE DECLARATION
                    │
          ┌─────────┴─────────┐
          │                   │
     Agent Directory      Generated package
          │                   │
     identity/state       host-specific form
          │                   │
          └─────────┬─────────┘
                    │
              PMCR-O governance
```

Generated content is disposable and reproducible. The declaration and governed directory state are authoritative; runtime projections are derived artifacts.

## PMCR-O placement

Use this template when the requested change is the **definition or packaging of an agent capability**. Use the lifecycle plugin when the request is the **execution of a governed change**.

```text
Seed Intent
   ↓
Orchestrator
   ↓
Planner ──→ AgentScaffoldSpec
               ↓
        scaffold / register
               ↓
             Maker
               ↓
            Checker
               ↓
           Reflector
               ↓
        sealed evidence
```

## Deliberate boundary

This template does not claim that every possible runtime projection is implemented. A target may be declared only when its renderer exists and its semantics are verified. Unknown host APIs stay unknown; the declaration must not manufacture them.

## Relationship to the existing repository

- Generic multi-target generation remains `plugins/pmcro-marketplace-directory/skills/scaffold-skill`.
- Fast skill-shape scaffolding remains `.agents/skills/create-skill`.
- Lifecycle execution remains `plugins/pmcro/`.
- Domain/persona definitions remain package-local under `plugins/pmcro-csuite/` or other declared packages.
- `.pmcro/` remains the governance, state, trail, policy, and evidence plane.
