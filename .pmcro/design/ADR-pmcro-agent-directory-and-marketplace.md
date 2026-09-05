# ADR: Agent Directory System + Generic Template-Driven Declarative AgentSkills Plugin Marketplace

**Status:** Proposed  
**Date:** 2026-09-05  
**Authors:** PMCRO Runtime Framework session (grounded in study of PMCRO-AI-Agent-Company/pmcr-o)  
**Supersedes / Relates to:**  
- Existing `.agents/skills/create-skill` (v0.2.0) — remains the narrow, lifecycle-plugin-only scaffolder.  
- Parallel Cowork session work on `plugins/pmcro-marketplace` / `scaffold-skill` (uncommitted at time of writing) — this ADR deliberately coexists rather than replaces.  
- `.pmcro/` governance layer (laws, policies, output contract).  

---

## 1. Context & Problem

PMCRO is evolving from a fixed set of six lifecycle plugins into a full **AI Agent Company**. That company needs:

1. **An Agent Directory System** — a durable, queryable catalog of every agent/persona/plugin that exists (or can be instantiated) inside the colony, with clear identity, capabilities, ownership, and lifecycle status.
2. **A Generic, Template-Driven, Declarative Design** for an **AgentSkills Plugin Marketplace** — so new plugins (personas, tools, domain skills, Chiefs, etc.) can be declared once and projected into multiple runtimes (Anthropic Agent Skills, Microsoft Agent Framework, Cursor, Claude Code, Codex, etc.) without hand-maintaining duplicate trees.

Current pain points observed across sessions:

- Multiple independent sessions invent overlapping scaffolders.
- `.agents/skills/create-skill` is correctly narrow (only the six core plugins) but people keep wanting to extend it.
- Marketplace manifests (`.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`, …) drift.
- No single source of truth for “what agents exist, what they may do, and how they are packaged.”
- Drive-letter / host-specific paths keep appearing; the trail contract forbids them.
- Persona / Chief concepts (CEO, CTO, …) are emerging but lack a uniform directory entry + packaging template.

## 2. Decision

We introduce two tightly-coupled but separable artifacts under the colony:

### 2.1 Agent Directory System (ADS)

A durable, schema-validated registry living at:

```text
.pmcro/directory/
  agents.yaml          # canonical list of all agents / personas / plugins
  agents.schema.json   # JSON Schema for the directory
  index.md             # human-readable generated view (optional)
```

Every entry answers:

| Field | Meaning |
|-------|---------|
| `id` | Stable kebab-case identifier (`pmcro-orchestrator`, `chief-executive-officer`, …) |
| `kind` | `lifecycle` \| `persona` \| `domain` \| `tool` \| `marketplace-scaffold` \| `harness` |
| `display_name` | Human title |
| `description` | One-paragraph purpose |
| `owner_role` | Which PMCR-O role (or human) owns evolution of this agent |
| `capabilities` | List of capability IDs from `.pmcro/capabilities/` |
| `skills` | List of skill entry points (`name`, `path`, `tier`) |
| `packaging` | How it is projected (`agentskills`, `maf-inline`, `maf-class`, `claude-plugin`, …) |
| `status` | `active` \| `experimental` \| `deprecated` \| `planned` |
| `trail_refs` | Optional list of sealed trail GUIDs that produced or last modified this entry |
| `marketplace_visible` | Boolean — appears in public marketplace catalog or not |

The directory is the **single source of truth**. Marketplace manifests and scaffolder allow-lists are *generated* from it, never hand-edited as the primary store.

### 2.2 Generic Template-Driven Declarative Marketplace

A new (or reconciled) plugin:

```text
plugins/pmcro-marketplace/
  skills/
    scaffold-skill/          # the declarative scaffolder
    register-agent/          # adds/updates an entry in the Agent Directory
    publish-projection/      # generates consumer-specific packaging
  assets/
    templates/               # archetype templates
      lifecycle-plugin/
      persona-chief/
      domain-skill/
      tool-skill/
      maf-inline-skill/
      maf-class-skill/
    schemas/
      agent-directory.schema.json
      scaffold-spec.schema.json
  references/
    packaging-conventions.md
    projection-matrix.md
```

#### Declarative Scaffold Spec (the key abstraction)

A user (or Planner) supplies a single YAML/JSON document:

```yaml
apiVersion: pmcro.ai/v1
kind: AgentScaffoldSpec
metadata:
  id: example-domain-analyst
  kind: domain
  display_name: Domain Analyst
spec:
  description: >
    Reads business requirements and produces structured analysis frames.
  owner_role: planner
  capabilities: [filesystem.read, memory.read]
  packaging:
    - target: agentskills
      path: .agents/skills/example-domain-analyst
    - target: maf-inline
      language: csharp
  skills:
    - name: analyze
      tier: DOMAIN
      description: Produce an AnalysisFrame from a seed intent fragment
  constraints:
    - no invented integrations
    - evidence required for any claim
  evaluation:
    trials: 3
    must_refuse: [unevidenced-capability, placeholder-tokens]
```

The `scaffold-skill` does **exactly** this sequence (and nothing else):

1. Validate the spec against `scaffold-spec.schema.json`.
2. Refuse cleanly if validation fails or if the spec claims a capability that is not present in `.pmcro/capabilities/`.
3. Render the chosen templates into the declared packaging targets.
4. Optionally call `register-agent` to upsert the Agent Directory entry.
5. Emit a governed result that satisfies the runtime output contract (trail-linked).

This is deliberately **not** a replacement for `.agents/skills/create-skill`.  
`create-skill` stays the fast, opinionated path for the six core lifecycle plugins.  
`scaffold-skill` is the generic, multi-archetype, multi-runtime path.

## 3. Architecture Principles (non-negotiable)

Derived directly from existing PMCRO laws and conventions:

1. **L-ORCHESTRATION** — the marketplace scaffolder never opens cycles or seals trails; it only produces artifacts and directory entries.
2. **L-PLUGIN-ISOLATION** — new plugins require an open cycle / binding envelope before TYPE1 mutations.
3. **L-CAPABILITY** — a scaffold may only declare capabilities that already exist (or are simultaneously registered) in the capability registry.
4. **No invented integrations** — empty provider/capability leaves are preferred to fabricated ones.
5. **Repository-relative paths only** — never `P:\…`, never absolute host paths inside any generated frame, SKILL.md, or directory entry.
6. **Trail-as-Product** — every scaffold run that mutates the directory or produces a new plugin package must be evidence inside a real trail.
7. **Separation of concerns**  
   - Directory = identity & catalog  
   - Marketplace plugin = generation & projection  
   - Lifecycle plugins = execution  
   - `.pmcro/laws` + policies = governance

## 4. Agent Directory System – Detailed Design

### 4.1 Schema sketch (`agents.schema.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["apiVersion", "kind", "agents"],
  "properties": {
    "apiVersion": { "const": "pmcro.ai/v1" },
    "kind": { "const": "AgentDirectory" },
    "agents": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "kind", "display_name", "description", "status"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$" },
          "kind": { "enum": ["lifecycle", "persona", "domain", "tool", "marketplace-scaffold", "harness"] },
          "display_name": { "type": "string" },
          "description": { "type": "string" },
          "owner_role": { "type": "string" },
          "capabilities": { "type": "array", "items": { "type": "string" } },
          "skills": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "path"],
              "properties": {
                "name": { "type": "string" },
                "path": { "type": "string" },
                "tier": { "type": "string" }
              }
            }
          },
          "packaging": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["target"],
              "properties": {
                "target": { "enum": ["agentskills", "maf-inline", "maf-class", "claude-plugin", "cursor-plugin", "codex-plugin"] },
                "path": { "type": "string" },
                "language": { "type": "string" }
              }
            }
          },
          "status": { "enum": ["active", "experimental", "deprecated", "planned"] },
          "marketplace_visible": { "type": "boolean" },
          "trail_refs": { "type": "array", "items": { "type": "string", "format": "uuid" } }
        }
      }
    }
  }
}
```

### 4.2 Bootstrap entries (the six lifecycle + current Chiefs)

The directory is seeded with the real plugins that already exist in the colony so the first `register-agent` runs are updates, not inventions.

## 5. Marketplace Projection Matrix

| Target | Output shape | When to use |
|--------|--------------|-------------|
| `agentskills` | `SKILL.md` + optional `assets/`, `references/`, `scripts/` | Claude Code, Cursor, Codex, generic Agent Skills hosts |
| `maf-inline` | C# / Python `InlineSkill` class | Microsoft Agent Framework (in-process) |
| `maf-class` | Full `ClassSkill` + DI registration | MAF production agents |
| `claude-plugin` | Claude marketplace plugin layout | Claude plugin marketplace |
| `cursor-plugin` | Cursor rules / skills layout | Cursor |
| `codex-plugin` | Codex-compatible skill package | OpenAI Codex |

A single declarative spec can request multiple projections; the scaffolder renders each independently and records the generated paths in the directory entry.

## 6. Relationship to Existing Artifacts (conflict resolution)

| Artifact | Decision |
|----------|----------|
| `.agents/skills/create-skill` | **Keep untouched.** Narrow, fast path for the six core lifecycle plugins. |
| Parallel session’s `plugins/pmcro-marketplace/scaffold-skill` | **Reconcile.** Adopt its stronger parts (eval.yaml, archetype assets, MAF awareness) into the design above; do not overwrite until a governed trail decides. |
| `.agents/plugins/marketplace.json` etc. | Become **generated views** of the Agent Directory, not the source of truth. |
| Persona / Chief plugins already present | Registered as `kind: persona` entries. |

## 7. Implementation Plan (ordered)

1. **Directory foundation**  
   - Create `.pmcro/directory/` with schema + initial `agents.yaml` seeded from current plugins.  
   - Add `L-DIRECTORY` law (optional) or treat directory mutations as TYPE1 under existing `L-PLUGIN-ISOLATION`.

2. **Scaffold skill (MVP)**  
   - Implement `scaffold-skill` that accepts an `AgentScaffoldSpec`, validates, renders one archetype (`agentskills` only first), and registers the agent.

3. **Projection expansion**  
   - Add MAF-inline and MAF-class templates (grounded in real MAF docs; unconfirmed surfaces stay as honest TODOs).

4. **Marketplace publish**  
   - `publish-projection` skill that regenerates all `marketplace.json` files from the directory.

5. **Evaluation harness**  
   - `eval.yaml` with refuse cases (placeholder tokens, unevidenced capabilities, drive-letter paths).

6. **Governed rollout**  
   - Every change to the directory or marketplace plugin itself runs through a full PMCR-O cycle (Orchestrate → Plan → Make → Check → Reflect) and leaves a sealed trail.

## 8. Success Criteria

- [ ] A new persona can be declared in a single YAML spec and appear correctly packaged under `.agents/skills/` **and** (when requested) as a MAF InlineSkill, with zero hand-written duplication.
- [ ] The Agent Directory is the only place a human or agent needs to look to answer “what agents exist and what may they do?”
- [ ] Existing `create-skill` continues to work unchanged for the six lifecycle plugins.
- [ ] No generated content contains absolute or drive-letter paths.
- [ ] Every directory mutation is evidenced in a sealed trail.
- [ ] Validation refuses unevidenced capability claims and placeholder tokens.

## 9. Open Questions (for the next Reflector / human decision)

1. Should the Agent Directory itself be versioned inside git, or treated as a runtime store that is only snapshotted into trails?
2. Do we want a public vs private visibility flag that also controls whether a plugin is pushed to an external marketplace?
3. How aggressively should the scaffolder enforce the “no invented integrations” rule when a capability is declared but no provider is wired yet?
4. Reconciliation protocol with the parallel Cowork session’s uncommitted `pmcro-marketplace` work — merge, supersede, or keep both under different IDs?

## 10. References

- Canonical repo: `PMCRO-AI-Agent-Company/pmcr-o`
- Existing laws: `.pmcro/laws/laws.yaml`
- Output contract: `.pmcro/runtime/output-contract.md`
- Current marketplace manifests: `.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`
- Prior design intent expressed in parallel session: declarative scaffolding, archetype assets, MAF skill types, reasoning-strategy taxonomy

---

**Next recommended action (PMCR-O style):**  
Open a governed cycle with seed intent:

> “Implement the Agent Directory System foundation and the MVP of the generic declarative scaffold-skill according to ADR-pmcro-agent-directory-and-marketplace.md, preserving create-skill untouched and leaving parallel-session marketplace work untouched until explicit reconciliation.”

That cycle should be linked to a new trail under `.pmcro/trails/`.
