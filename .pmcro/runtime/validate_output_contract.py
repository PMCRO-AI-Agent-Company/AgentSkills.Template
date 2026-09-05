#!/usr/bin/env python3
"""Deterministic validator for the PMCR-O governed output contract.

Usage:
  python validate_output_contract.py <file.json>
  echo '{"action":"..."}' | python validate_output_contract.py -

Exit codes:
  0 = PASS
  1 = FAIL (contract violations)
  2 = usage / I/O error
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "frame_id",
    "trail_id",
    "workflow_id",
    "action",
    "state_transition",
    "required_evidence",
    "next_gate",
    "halt_reason",
]


def load(path: str) -> Any:
    if path == "-":
        raw = sys.stdin.buffer.read()
    else:
        raw = Path(path).read_bytes()
    # Tolerate UTF-8 BOM (common from PowerShell)
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return json.loads(raw.decode("utf-8"))


def validate(obj: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]

    for field in REQUIRED_FIELDS:
        if field not in obj:
            errors.append(f"missing required field: {field}")

    if "required_evidence" in obj and not isinstance(obj["required_evidence"], list):
        errors.append("required_evidence must be an array")

    action = obj.get("action")
    if action in ("COMPLETE", "SEAL", "DONE"):
        evidence = obj.get("required_evidence")
        if not evidence:
            errors.append("completion requires non-empty required_evidence (L-EVIDENCE)")
        # Checker gate: expect a checker object or a checker_status field
        checker = obj.get("checker") or obj.get("checker_result")
        status = None
        if isinstance(checker, dict):
            status = checker.get("status") or checker.get("verdict")
        elif isinstance(obj.get("checker_status"), str):
            status = obj["checker_status"]
        if status not in ("PASS", "pass", "PASSED"):
            errors.append("completion requires checker status PASS (L-CHECKER-GATE)")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_output_contract.py <file.json> | -", file=sys.stderr)
        return 2
    try:
        data = load(sys.argv[1])
    except Exception as exc:
        print(f"I/O or JSON error: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
