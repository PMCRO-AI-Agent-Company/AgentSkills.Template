# Global `~/.claude/` Config Reference

This directory documents the **personal `~/.claude/` structure** every team member should configure on their local machine. These files live **outside the repo** and are never committed — this folder is the committed reference template.

## Directory map

```
~/.claude/
├── CLAUDE.md                    ← personal preferences loaded in every project
├── settings.json                ← default settings for all projects
├── keybindings.json             ← custom keyboard shortcuts
├── themes/                      ← custom color themes
│   └── <theme-name>.json
├── projects/                    ← auto memory, keyed by repo path (autogen)
│   └── <project>/
│       └── memory/
│           ├── MEMORY.md        ← index, loaded at session start (200 lines / 25KB cap)
│           └── <topic>.md       ← topic file, read on demand
├── rules/                       ← user-level rules applied to every project
├── skills/                      ← personal skills available in every project
├── commands/                    ← personal single-file commands
├── output-styles/               ← personal output styles
│   └── teaching.md              ← example: explain reasoning, leave small changes to user
├── agents/                      ← personal subagents available in every project
├── workflows/                   ← personal workflow scripts
└── agent-memory/                ← cross-project subagent memory (memory: user)
```

## Mapping to this project

| `~/.claude/` path | Role in this project |
|---|---|
| `CLAUDE.md` | → `AGENTS.md` at project root |
| `.claude/` | → `.agents/` at project root |
| `~/.claude/` global | → `.pmcro/` (runtime + global state) |
| `.claude/agent-memory/` | → `.agents/agent-memory/` |

## Getting started

Copy the example files from this directory and place them in `~/.claude/` on your machine:

| File here | Destination |
|---|---|
| `CLAUDE.md.example` | `~/.claude/CLAUDE.md` |
| `settings.json.example` | `~/.claude/settings.json` |
| `keybindings.json.example` | `~/.claude/keybindings.json` |
| `output-styles/teaching.md.example` | `~/.claude/output-styles/teaching.md` |

## Precedence rules

- `~/.claude/` loads **before** the project `.agents/` — project config takes precedence on conflicts
- **Array** settings (e.g. `permissions.allow`) **combine** across global + project + local scopes
- **Scalar** settings (e.g. `model`) use the **most specific** value: local > project > global
- Auto memory in `projects/` is written by the runtime; do not edit by hand
