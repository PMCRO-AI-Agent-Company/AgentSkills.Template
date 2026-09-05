#!/usr/bin/env python3
"""Minimal PMCRO queue lever — claims seed JSON files and prints Plan handoff.

Not a full Orchestrator. Demonstrates that .pmcro/queue/ is usable in this workspace.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUEUE = Path(__file__).resolve().parent


def main() -> int:
    seeds = sorted(QUEUE.glob("seed-*.json"))
    if not seeds:
        print("queue empty (no seed-*.json)")
        return 0
    for path in seeds:
        data = json.loads(path.read_text(encoding="utf-8"))
        spec = data.get("spec") or {}
        print("--- claim ---")
        print("file:", path.name)
        print("id:", (data.get("metadata") or {}).get("id"))
        print("intent:", spec.get("intent", "")[:200])
        print("plan_ref:", spec.get("plan_ref"))
        print("checklist_ref:", spec.get("checklist_ref"))
        print("capabilities:", spec.get("capability_flags"))
        print("status: claimed-for-plan (no seal in this seed host)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
