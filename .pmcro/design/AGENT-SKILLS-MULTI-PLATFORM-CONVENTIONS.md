# Agent Skills Multi-Platform Conventions (PMCRO)

**Status:** Normative for the company marketplace and projections  
**Aligns with:** [agentskills.io](https://agentskills.io), [dotnet/skills](https://github.com/dotnet/skills), Claude Code, GitHub Copilot, Cursor, Codex, Grok, MAF Skills  

---

## 1. One skill, many hosts

Canonical authoring form is always:

```text
skill-name/
  SKILL.md          # required: YAML frontmatter + instructions
  scripts/          # optional
  references/       # optional
  assets/           # optional
```

Frontmatter **required**: `name` (kebab-case, matches folder), `description` (what + when, ≤1024 chars).  
Optional: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental).

Hosts load via **progressive disclosure**: advertise name/description → load body → resources → scripts.

PMCRO **scaffolder** emits this shape for `agentskills` target. MAF-inline is an *additional* projection, not a replacement.

---

## 2. Where skills live (project vs user)

| Platform | Project (repo) path | User (global) path |
|----------|---------------------|--------------------|
| **Claude Code** | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| **GitHub Copilot** | `.github/skills/<name>/` or `.github/copilot/skills/` | `~/.copilot/skills/` |
| **Cursor** | `.cursor/skills/<name>/` | `~/.cursor/skills/` |
| **OpenAI Codex** | `.codex/skills/` or `.agents/skills/` | `~/.codex/skills/` |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` |
| **Grok** | `.agents/skills/` · `.grok/skills/` | `~/.grok/skills/` (session-dependent) |
| **MAF (.NET/Python)** | App `skills/` dir or provider paths | Packaged / toolbox / Foundry Skills API |
| **Windsurf / Cline / etc.** | Tool-specific under `.windsurf/skills/`, … | Matching home dirs |

**PMCRO convention:**  
- **Canonical source** in repo: `plugins/<plugin>/skills/<skill>/` and/or `.agents/skills/<skill>/`  
- **Projections** (copy or symlink) into host dirs as needed — never hand-maintain duplicates as source of truth  
- **Agent Directory** records packaging targets and paths

---

## 3. Marketplace / plugin install patterns

### 3.1 Claude Code / Copilot CLI style (dotnet/skills model)

```text
/plugin marketplace add dotnet/skills
/plugin marketplace browse dotnet-agent-skills
/plugin install <plugin>@dotnet-agent-skills
/dotnet-diag:analyzing-dotnet-performance    # plugin:skill slash form
```

Also: `npx skills add owner/repo`, `dnx skills add owner/repo --agent claude-code`.

**PMCRO should ship:**

```text
/plugin marketplace add PMCRO-AI-Agent-Company/pmcr-o
/plugin install pmcro-marketplace-directory@pmcro-skills
/pmcro-marketplace-directory:scaffold-skill
```

Manifests: `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` (already started in this seed).

### 3.2 VS Code Copilot

Add marketplace URL `https://github.com/dotnet/skills` (or your PMCRO marketplace repo) in Copilot settings → browse extensions → install → slash invoke.

### 3.3 Codex / Cursor / multi-agent CLIs

```text
npx skills add microsoft/skills
npx @agentskill.sh/cli setup
ags install <skill> --platform cursor
```

Project folders per table in §2.

### 3.4 External catalogs to **import** (not reinvent)

| Repo | Use |
|------|-----|
| [dotnet/skills](https://github.com/dotnet/skills) | Official .NET platform skills (Blazor, diagnostics, .NET 11, …) |
| [microsoft/skills](https://github.com/microsoft/skills) | Broad language plugins (`*-dotnet`, `*-py`, …) |
| [MicrosoftDocs/agent-skills](https://github.com/MicrosoftDocs/agent-skills) | Azure service skills |
| Anthropic / community skill repos | General coding workflows |
| **This company** | PMCRO lifecycle, C-Suite, marketplace scaffolder, reasoning catalog |

**Rule:** Import upstream skills via marketplace add / `skills add`; register **company-owned** skills in Agent Directory. Do not fork entire upstream trees into `.pmcro/`.

---

## 4. Slash / invoke conventions

| Context | Form |
|---------|------|
| Claude plugin skill | `/plugin-name:skill-name` |
| Claude project skill | `/skill-name` (folder name) |
| Copilot after plugin install | `/plugin:skill` or skill picker |
| Grok (this environment) | Skill **name** in natural language once under `.grok/skills/` |
| MAF runtime | Provider discovery by description; no slash required |
| Codex | `/skills` or product-specific mention |

PMCRO lifecycle skills should document both **plugin-qualified** and **bare** names in command assets.

---

## 5. Authoring rules (match upstream quality)

From dotnet/skills `create-skill` + agentskills.io:

1. `name` = directory name = kebab-case  
2. `description` leads with **what** and **when** (trigger-rich)  
3. Sections: Purpose, When to Use, When Not to Use, Workflow, References  
4. Keep `SKILL.md` lean; put long material in `references/`  
5. Scripts deterministic; never trust without success **and** failure path tests  
6. No drive-letter or absolute host paths in skill text  
7. PMCRO extras: respect L-EVIDENCE, L-CHECKER-GATE; personas do not seal  

---

## 6. Projection matrix (company template system)

| Source of truth | Projection targets |
|-----------------|-------------------|
| `plugins/pmcro-*/skills/*` | `.agents/skills/`, `.claude/skills/`, `.github/skills/`, `.cursor/skills/`, `.codex/skills/`, MAF file provider path |
| `.agents/skills/reasoning/*` | Same host dirs (or single `reasoning-catalog` meta-skill that points at catalog) |
| `scaffold-skill` output | Declared `packaging[].path` only |

**Automate later:** a `publish-projection` skill that reads Agent Directory and syncs to host folders (symlink preferred on Unix).

---

## 7. Grok / Claude.ai / Copilot feature parity checklist

| Feature | How PMCRO supports it |
|---------|------------------------|
| Portable SKILL.md | Scaffolder + Directory |
| Marketplace add | `marketplace.json` + documented `/plugin marketplace add` |
| Slash plugin:skill | Plugin-qualified names in command assets |
| Progressive disclosure | Short descriptions; body on demand |
| Multi-agent install | Document paths for Claude, Cursor, Codex, Copilot, Grok |
| Import dotnet/skills | Document as **recommended external marketplace**, not vendored |
| MAF Skills API / toolbox | maf-inline projection + Foundry toolbox later |
| HITL | CopilotKit + policy approvals (hybrid stack ADR) |

---

## 8. Immediate operator commands (real repo)

```bash
# Upstream .NET skills
# Claude Code / Copilot CLI:
/plugin marketplace add dotnet/skills
/plugin install <plugin>@dotnet-agent-skills

# CLI alternative
npx skills add dotnet/skills
# or
dnx skills add dotnet/skills --agent claude-code

# Company marketplace (when published from pmcr-o)
/plugin marketplace add PMCRO-AI-Agent-Company/pmcr-o
/plugin install pmcro-marketplace-directory@pmcro-skills
```

---

## 9. Decision

PMCRO **follows** the open Agent Skills standard and host-specific install paths used by Claude Code, GitHub Copilot, Cursor, Codex, Grok, and MAF.  
Company skills are authored once, registered in the Agent Directory, and **projected** to host directories.  
External catalogs (**dotnet/skills**, **microsoft/skills**, Azure agent-skills) are **imported via marketplace**, not copied into governance as source of truth.
