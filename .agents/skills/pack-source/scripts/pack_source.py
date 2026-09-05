#!/usr/bin/env python3
"""Pack source code into a single text file for third-party LLMs.

Walks a target directory, skips junk and binary files, and stitches every
readable file together into one LLM-friendly text file using XML-style
``<file path="...">`` tags.

Usage:
    python3 pack_source.py --out dump.txt [--dir .] [--ignore ".log,build"]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Directories to ignore by default -- keeps the dump focused and small.
DEFAULT_IGNORE_DIRS = {
    ".git",
    ".svn",
    "node_modules",
    "pycache",
    "dist",
    "build",
    "venv",
    ".venv",
    ".env",
    # Never pack the packer itself.
    ".agents/skills/pack-source",
    # Skip build artifacts produced by this project.
    "artifacts",
    "obj",
    "bin",
}

# Binary / non-text extensions to ignore by default.
DEFAULT_IGNORE_EXTS = {
    ".pyc",
    ".pyo",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".zip",
    ".tar",
    ".gz",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".mp4",
    ".mp3",
    ".ttf",
    ".woff",
    ".woff2",
    ".eot",
    ".otf",
    ".class",
    ".jar",
    ".war",
}


def is_text_file(filepath: Path) -> bool:
    """Return True if ``filepath`` looks like a UTF-8 decodable text file."""
    try:
        with open(filepath, "tr", encoding="utf-8") as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False


def pack_directory(
    target_dir: str,
    output_file: str,
    extra_ignores: list[str] | None = None,
) -> int:
    """Walk ``target_dir`` and write a text dump of readable files to ``output_file``.

    Returns the number of files packed.
    """
    target_path = Path(target_dir).resolve()

    ignore_dirs = set(DEFAULT_IGNORE_DIRS)
    ignore_exts = set(DEFAULT_IGNORE_EXTS)

    if extra_ignores:
        for item in extra_ignores:
            item = item.strip()
            if not item:
                continue
            if item.startswith("."):
                ignore_exts.add(item)
            else:
                ignore_dirs.add(item)

    if not target_path.is_dir():
        print(f"FAIL: target dir is not a directory: {target_path}", file=sys.stderr)
        return 1

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    file_count = 0
    bytes_written = 0

    with open(out_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"<!-- Source code dump of: {target_dir} -->\n\n")

        for root, dirs, files in os.walk(target_path):
            # Filter directories in-place so os.walk does not descend into them.
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                ext = Path(file).suffix.lower()
                if ext in ignore_exts:
                    continue

                full_path = Path(root) / file
                try:
                    rel_path = full_path.relative_to(target_path)
                except ValueError:
                    continue

                if not full_path.is_file() or not is_text_file(full_path):
                    continue

                try:
                    content = full_path.read_text(encoding="utf-8", errors="strict")
                except Exception as e:
                    print(f"Skipping {rel_path} due to error: {e}", file=sys.stderr)
                    continue

                block = f'<file path="{rel_path}">\n{content}'
                if not content.endswith("\n"):
                    block += "\n"
                block += "</file>\n\n"
                outfile.write(block)

                file_count += 1
                bytes_written += len(block.encode("utf-8"))

    size_kb = (bytes_written / 1024) if bytes_written else 0
    print(
        f"Successfully packed {file_count} files "
        f"({size_kb:.1f} KB) into {output_file}"
    )
    return 0


def parse_ignore_arg(ignore: str) -> list[str]:
    return [item for item in ignore.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pack source code into a single text file for LLMs.",
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory to pack (default: current dir).",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output file path (e.g. dump.txt).",
    )
    parser.add_argument(
        "--ignore",
        default="",
        help="Comma-separated extra dirs (.ext) to ignore.",
    )
    args = parser.parse_args()

    extra = parse_ignore_arg(args.ignore)
    return pack_directory(args.dir, args.out, extra)


if __name__ == "__main__":
    sys.exit(main())
