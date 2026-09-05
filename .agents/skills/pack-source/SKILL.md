---
name: pack-source
description: >-
  Packages repository files into a single text dump for third-party LLMs that
  lack file-system access. Walks a directory, skips junk/binary files, and
  stitches everything together into an LLM-friendly text file using XML-style
  <file> tags. USE when bridging a local codebase (plugins, create-skill
  scaffold, etc.) to another LLM via text upload only. DO NOT use for
  massive directories (gigabytes) that would blow out an LLM's context window.
license: Apache-2.0
metadata:
  version: "0.1.0"
  tier: UTILITY
  capability_class: TOOLING
  plugin_path: .agents/skills/pack-source
---

# Pack Source for LLMs

## Purpose

Generates a single, consolidated text file containing the contents of a directory.
This bridges complex projects (like the Plugin Marketplace and `create-skill`
architectures) to third-party LLMs that don't have file-system access. It walks
the target directory, ignores junk and binary files, and stitches every readable
file together into one LLM-friendly text file using XML-style `<file>` tags,
which LLMs parse exceptionally well.

## When to Use

- When you need to share multiple files, a module, or a plugin (e.g. the Plugin
  Marketplace) with another LLM that only accepts text.
- When you need to create a "source dump" of a specific directory that another
  agent can consume as a single `.txt` attachment or prompt.
- Whenever a downstream task says "paste the file here" but the relevant code
  spans many files.

## When Not to Use

- When working entirely within an agent that already has local file-system
  access.
- When the requested directory is massive (e.g. gigabytes of data) which would
  blow out an LLM's context window.
- When only a single, well-known file is needed — use a direct read instead.

## Inputs

| Field | Description | Default |
|---|---|---|
| `target_dir` (`--dir`) | The directory to package. | `.` (current directory) |
| `output_file` (`--out`) | Where to save the text dump (e.g. `source_dump.txt`). | _required_ |
| `ignore` (`--ignore`) | Comma-separated list of extra extensions or folders to ignore. Prefixes with `.` are treated as extensions, otherwise as directory names. | `""` |

## Workflow

1. Identify the directory the user wants to package.
2. Run the `pack_source.py` script against that directory.

```bash
python3 .agents/skills/pack-source/scripts/pack_source.py \
  --dir <target_dir> \
  --out <output_file> \
  [--ignore ".log,build,temp"]
```

3. Inspect the result.

```bash
# Confirm the output exists and is populated with <file path="..."> tags.
ls -la <output_file>
head -n 20 <output_file>
```

4. Inform the user of the output file location and size.

## Validation

- The script exits with code `0` and prints a summary such as
  `Successfully packed N files into <output_file>`.
- The output file exists and is populated with XML-style `<file path="...">`
  tags.
- The ignored directories (`node_modules`, `.git`, `dist`, `build`, etc.) and
  binary extensions (`.png`, `.pdf`, `.exe`, etc.) are not present inside any
  `<file>` block.

## Examples

```bash
# Dump the marketplace plugin from the repo root.
python3 .agents/skills/pack-source/scripts/pack_source.py \
  --dir plugins/pmcro --out marketplace-dump.txt

# Dump the create-skill structure, ignoring an extra dir.
python3 .agents/skills/pack-source/scripts/pack_source.py \
  --dir .agents/skills/create-skill --out createskill-dump.txt \
  --ignore "node_modules,.tmp"
```

You can now upload `marketplace-dump.txt` to any LLM and it will have
file-delimited context of the plugin architecture.

## PMCRO Output Law

All governed results emitted by this skill must conform to L-OUTPUT-CONTRACT and the canonical contract at .pmcro/runtime/output-contract.md.
