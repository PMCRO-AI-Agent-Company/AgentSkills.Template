#!/usr/bin/env python3
"""
validate_skill_md.py — deterministic SKILL.md compliance check.

Checks a skill's SKILL.md against two PMCRO drift patterns found
2026-08-26 (audit trail e7b4d2a9-...), updated 2026-09-05 for the
request/response asset rename (supersedes command/run/reject):

  1. Command Surface must not be embedded as a duplicated literal
     command list when assets/request.<name>.asset.md (or the legacy
     run.*.asset.md) already defines it. SKILL.md should only
     reference assets/, never re-list the commands.
  2. Every SKILL.md must end with the "## PMCRO Output Law" footer,
     verbatim, per L-OUTPUT-CONTRACT.

Exit code 0 = pass, 1 = fail (findings printed to stdout either way).
No reasoning required to run this — it's meant to be invoked directly.

Usage:
    python validate_skill_md.py <path-to-SKILL.md>
    python validate_skill_md.py <path-to-skill-dir>   # finds SKILL.md inside it
"""
import re
import sys
from pathlib import Path

OUTPUT_LAW_MARKER = "## PMCRO Output Law"
OUTPUT_LAW_TEXT = (
    "All governed results emitted by this skill must conform to "
    "L-OUTPUT-CONTRACT and the canonical contract at "
    ".pmcro/runtime/output-contract.md."
)

COMMAND_SURFACE_HEADING = re.compile(r"^##\s+Command Surface\s*$", re.MULTILINE)
FENCED_BLOCK = re.compile(r"```text\n(.*?)```", re.DOTALL)
SLASH_COMMAND_LINE = re.compile(r"^\s*/\S+:\S+")


def find_skill_md(target: Path) -> Path:
    if target.is_file():
        return target
    candidate = target / "SKILL.md"
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"No SKILL.md found at or under {target}")


def check_output_law_footer(text: str) -> list[str]:
    findings = []
    if OUTPUT_LAW_MARKER not in text:
        findings.append(
            "MISSING: '## PMCRO Output Law' footer not found. "
            "Every SKILL.md must end with it, copied from the template."
        )
    elif OUTPUT_LAW_TEXT not in text:
        findings.append(
            "DRIFTED: '## PMCRO Output Law' heading present but the body "
            "text doesn't match the canonical wording — check for reword."
        )
    return findings


def check_command_surface_duplication(skill_md: Path, text: str) -> list[str]:
    findings = []
    heading_match = COMMAND_SURFACE_HEADING.search(text)
    if not heading_match:
        return findings  # no Command Surface section — fine (e.g. activate)

    after_heading = text[heading_match.end():]
    fenced = FENCED_BLOCK.search(after_heading)
    if not fenced:
        return findings  # heading present but no fenced command list — fine

    body = fenced.group(1)
    has_slash_commands = any(
        SLASH_COMMAND_LINE.match(line) for line in body.splitlines()
    )
    if not has_slash_commands:
        return findings

    assets_dir = skill_md.parent / "assets"
    has_request_asset = assets_dir.exists() and (
        any(assets_dir.glob("request.*.asset.md"))
        or any(assets_dir.glob("run.*.asset.md"))  # legacy, still accepted
    )
    if has_request_asset:
        findings.append(
            "DUPLICATED: '## Command Surface' embeds a literal command "
            "list AND assets/request.*.asset.md (or legacy run.*.asset.md) "
            "already defines it. SKILL.md should reference assets/, not "
            "duplicate it."
        )
    else:
        findings.append(
            "WARNING: '## Command Surface' embeds a literal command list "
            "but no assets/request.*.asset.md exists to be the source of "
            "truth. Either add the request/response asset pair, or "
            "confirm this skill genuinely has no asset-based command "
            "definition."
        )
    return findings


def check_request_response_pairing(skill_md: Path) -> list[str]:
    """New 2026-09-05 check: a request asset without its response
    sibling (or vice versa) is drift — they're always authored as a
    pair."""
    findings = []
    assets_dir = skill_md.parent / "assets"
    if not assets_dir.exists():
        return findings

    requests = {p.name.split(".", 1)[1] for p in assets_dir.glob("request.*.asset.md")}
    responses = {p.name.split(".", 1)[1] for p in assets_dir.glob("response.*.asset.md")}

    for missing_response in requests - responses:
        findings.append(
            f"UNPAIRED: assets/request.{missing_response} has no matching "
            f"assets/response.{missing_response}."
        )
    for missing_request in responses - requests:
        findings.append(
            f"UNPAIRED: assets/response.{missing_request} has no matching "
            f"assets/request.{missing_request}."
        )
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    target = Path(sys.argv[1])
    try:
        skill_md = find_skill_md(target)
    except FileNotFoundError as e:
        print(f"FAIL: {e}")
        return 1

    text = skill_md.read_text(encoding="utf-8")
    findings = []
    findings += check_output_law_footer(text)
    findings += check_command_surface_duplication(skill_md, text)
    findings += check_request_response_pairing(skill_md)

    print(f"Validated: {skill_md}")
    if not findings:
        print("PASS — no drift found.")
        return 0

    print(f"FAIL — {len(findings)} finding(s):")
    for f in findings:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
