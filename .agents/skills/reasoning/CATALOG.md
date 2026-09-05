# Reasoning Skills Catalog

**Version:** 1.0.0  
**Format:** Open Agent Skills (`SKILL.md`)  
**Count:** 35 skills across 7 families  
**Install:** Drop any skill folder into `.agents/skills/`, `.claude/skills/`, `.gemini/skills/`, or equivalent.

Each skill is a minimal portable package containing only `SKILL.md` (plus reasoning metadata in frontmatter).

---

## Family 1 — Linear / Sequential

Ordered intermediate steps. Best default for multi-step problems that do not need heavy exploration.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **chain-of-thought** | Force explicit ordered intermediate steps | linear_cot |
| **stepwise-verification** | Verify each intermediate step before continuing | linear_cot + iterative_self_reflective |
| **plan-and-execute** | Write a plan first, then execute it | linear_cot + strategic_agentic |
| **goal-regression** | Work backward from goal to achievable actions | branching_search + linear_cot |
| **backward-chaining** | Derive required premises/actions from the goal | linear_cot + branching_search |
| **forward-chaining** | Derive consequences from known facts/rules | linear_cot |
| **least-to-most** | Solve easier sub-questions before the hard target | linear_cot + branching_search |
| **decomposition-recomposition** | Split → solve parts → recombine | linear_cot + branching_search |
| **recursive-summarization** | Hierarchical compression of long material | linear_cot |

**Use when:** Multi-step math, logic, planning, long documents.  
**Avoid when:** The problem needs broad exploration of alternatives or tool interaction.

---

## Family 2 — Search / Exploration

Generate and evaluate multiple paths or candidates before committing.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **tree-of-thoughts** | Explore several partial solutions, then select | branching_search |
| **progressive-deepening** | Survey shallow, then deepen only promising branches | branching_search + test_time_compute |
| **constraint-satisfaction** | Satisfy hard constraints first, then optimize soft ones | branching_search + linear_cot |
| **self-consistency** | Sample many independent traces and take consensus | test_time_compute + linear_cot |

**Use when:** Design, planning, puzzles, brittle single-path answers.  
**Avoid when:** Latency is critical or the problem is already linear.

---

## Family 3 — Iterative / Reflective

Draft, critique, revise, or monitor one's own reasoning.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **self-refine** | Draft → critique → revise | iterative_self_reflective |
| **verification-loop** | Generate then independently verify against criteria | iterative_self_reflective + linear_cot |
| **error-driven-learning** | Extract a rule from a failure and re-solve | iterative_self_reflective |
| **metacognitive-monitoring** | Track and report confidence/uncertainty explicitly | iterative_self_reflective |
| **uncertainty-decomposition** | Separate knowns, unknowns, and assumptions | linear_cot |
| **debate-reasoning** | Steel-man multiple sides, then synthesize | branching_search + iterative_self_reflective |
| **multi-agent-critique** | Simulate distinct perspectives that critique each other | branching_search + iterative_self_reflective |

**Use when:** Writing, analysis, high-stakes answers, contested topics.  
**Avoid when:** Simple lookups or strict single-pass constraints.

---

## Family 4 — Causal & Explanatory

Explain why something happened, or what would have happened otherwise.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **abductive-diagnosis** | Best explanation under incomplete evidence | branching_search + iterative_self_reflective |
| **hypothesis-testing** | Form testable hypotheses and state confirming/refuting evidence | branching_search + iterative_self_reflective |
| **counterfactual-reasoning** | What would have happened if a factor differed | linear_cot (causal_counterfactual) |
| **contrastive-explanation** | Explain why P rather than Q | linear_cot (causal_counterfactual + abductive) |
| **evidence-weighting** | Explicit weighted list of evidence for and against | linear_cot |

**Use when:** Debugging, post-mortems, “why” questions, disputed claims.  
**Avoid when:** Pure procedural how-to with no explanatory need.

---

## Family 5 — Analogical & Case-Based

Reuse structure or solutions from similar situations.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **analogical-reasoning** | Map relational structure from a known domain | linear_cot (analogical) |
| **analogical-transfer-check** | Stress-test an analogy for broken mappings | iterative_self_reflective |
| **case-based-reasoning** | Retrieve similar past cases and adapt their solutions | linear_cot (analogical + inductive) |

**Use when:** Novel problems that resemble known ones; recurring operational issues.  
**Avoid when:** A direct algorithm exists or the analogy would be forced.

---

## Family 6 — Interactive / Grounded

Reasoning that depends on external actions, retrieval, or clarification.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **react-loop** | Thought → Action → Observation loop | iterative_self_reflective |
| **search-then-reason** | Retrieve evidence first, then reason only on it | linear_cot |
| **socratic-questioning** | Clarify underspecified problems with precise questions | iterative_self_reflective |

**Use when:** Tools, APIs, web/docs, or ambiguous user requests.  
**Avoid when:** Pure offline reasoning with complete information.

---

## Family 7 — Framing & Normative

Change perspective, process, or value framing before solving.

| Skill | One-line purpose | Primary methods |
|-------|------------------|-----------------|
| **role-based-reasoning** | Adopt a coherent expert role and its priorities | linear_cot |
| **dual-process** | Fast intuitive answer, then slow deliberate check | linear_cot + iterative_self_reflective |
| **reflective-equilibrium** | Iterate between principles and case judgments | iterative_self_reflective |
| **template-filling** | Fill a fixed set of analysis slots systematically | linear_cot |

**Use when:** Domain advice, ethical/policy questions, recurring structured reviews.  
**Avoid when:** Neutral factual lookup with no framing needed.

---

## Quick selection guide

| Situation | Start with |
|-----------|------------|
| Multi-step math / logic | `chain-of-thought` → `stepwise-verification` |
| Brittle answers | `self-consistency` or `verification-loop` |
| Planning / design | `plan-and-execute` or `tree-of-thoughts` |
| Tool use / environment | `react-loop` |
| Writing / analysis quality | `self-refine` |
| Debugging / “why” | `abductive-diagnosis` or `hypothesis-testing` |
| Post-mortem / impact | `counterfactual-reasoning` |
| Long documents | `recursive-summarization` |
| Ambiguous request | `socratic-questioning` |
| Contested topic | `debate-reasoning` or `multi-agent-critique` |
| High-stakes under uncertainty | `metacognitive-monitoring` + `uncertainty-decomposition` |
| Recurring structured analysis | `template-filling` |

---

## Reasoning metadata dimensions (used in every skill)

Every skill declares:

- **logical_paradigms** — deductive · inductive · abductive · analogical · causal_counterfactual  
- **operational_methods** — linear_cot · branching_search · test_time_compute · iterative_self_reflective  
- **domain_capabilities** — mathematical_symbolic · multi_hop_relational · common_sense · spatial_temporal · strategic_agentic  

These are declarative labels for routing and review, not runtime claims about model internals.

---

## Install locations (portable)

| Scope | Common paths |
|-------|----------------|
| Project | `.agents/skills/`, `.claude/skills/`, `.gemini/skills/`, `.github/skills/`, `.maf/skills/` |
| User | `~/.agents/skills/`, `~/.claude/skills/`, `~/.gemini/skills/`, `~/.copilot/skills/` |

Prefer `.agents/skills/` for maximum cross-tool compatibility.

---

*Catalog generated for the open Agent Skills format. Companion zip: `reasoning-skills-full.zip` (35 skills).*
