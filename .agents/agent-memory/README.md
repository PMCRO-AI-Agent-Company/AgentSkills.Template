# Agent Memory

This directory is **auto-generated** at runtime by PMCR-O.

Subagents with `memory: project` in their frontmatter get a dedicated memory directory here:

```
agents-memory/
  <agent-name>/
    MEMORY.md      ← loaded into the subagent's system prompt on each run
```

## What lives here

- Each subagent reads and writes its own `MEMORY.md` — separate from the main session's auto memory
- The agent creates and maintains this file; do not edit it manually unless correcting stale information
- Commit this directory so team members share the accumulated knowledge

## Example entry

```
agents-memory/
  code-reviewer/
    MEMORY.md
```

```markdown
# code-reviewer memory

## Patterns seen
- Project uses custom Result<T, E> type, not exceptions
- Auth middleware expects Bearer token in Authorization header

## Recurring issues
- Missing null checks on API responses (src/api/*)
```
