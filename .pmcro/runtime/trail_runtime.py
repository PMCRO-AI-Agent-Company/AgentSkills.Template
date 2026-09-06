#!/usr/bin/env python3
"""PMCRO trail lifecycle runtime (governance seed).

Wires the mechanical half of the PMCR-O loop that was previously done by
hand each cycle: minting a trail, appending each role's phase frame in
order, validating the output contract at Check, and sealing at Reflect.
This does NOT decide plan/make/check/reflect content - an LLM (or future
agent) still supplies that. It only makes the disk mechanics for "open a
trail, record a phase, seal it" a single deterministic command instead of
copy-pasting JSON files by hand.

Commands:
  open    --seed "..." [--host NAME]
  plan    --trail ID   (reads plan JSON object from stdin)
  make    --trail ID   (reads one make JSON object from stdin, appended
                         as a line to 03-make.jsonl)
  check   --trail ID   (reads check JSON object from stdin; enforces
                         verdict field is PASS/FAIL before writing)
  reflect --trail ID   (reads reflect JSON object from stdin; on
                         disposition SEAL, seals the trail and, if an
                         active queue claim exists, completes it)
  status  [--trail ID] (defaults to the active trail)

Exit codes: 0 = ok, 1 = precondition/validation failure, 2 = usage/I/O error.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # .pmcro
TRAILS = ROOT / "trails"
STATE = ROOT / "state"
ACTIVE_TRAIL_FILE = STATE / "active_trail_id.txt"
QUEUE_RUNTIME = ROOT / "runtime" / "queue_runtime.py"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    TRAILS.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)


def read_stdin_json() -> dict:
    raw = sys.stdin.buffer.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    if not raw.strip():
        raise ValueError("expected a JSON object on stdin, got nothing")
    obj = json.loads(raw.decode("utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("stdin JSON must be an object")
    return obj


def trail_dir(trail_id: str) -> Path:
    d = TRAILS / trail_id
    if not d.exists():
        raise FileNotFoundError(f"no such trail: {trail_id}")
    return d


def get_active_trail() -> str | None:
    if ACTIVE_TRAIL_FILE.exists():
        v = ACTIVE_TRAIL_FILE.read_text(encoding="utf-8").strip()
        return v or None
    return None


def set_active_trail(trail_id: str | None) -> None:
    if trail_id is None:
        if ACTIVE_TRAIL_FILE.exists():
            ACTIVE_TRAIL_FILE.unlink()
        return
    ACTIVE_TRAIL_FILE.write_text(trail_id + "\n", encoding="utf-8")


def resolve_trail_arg(args: argparse.Namespace) -> str:
    trail_id = getattr(args, "trail", None) or get_active_trail()
    if not trail_id:
        raise ValueError("no --trail given and no active trail set")
    return trail_id


def cmd_open(args: argparse.Namespace) -> int:
    ensure_dirs()
    if not args.seed:
        print("error: --seed is required (verbatim messy seed intent)", file=sys.stderr)
        return 2
    trail_id = str(uuid.uuid4())
    d = TRAILS / trail_id
    d.mkdir(parents=True, exist_ok=False)

    (d / "trail.json").write_text(
        json.dumps(
            {
                "trail_id": trail_id,
                "trail_class": "B",
                "opened_at": now(),
                "seed_intent": args.seed,
                "status": "open",
                "host": args.host or "unspecified",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    open_frame = {
        "ts": now(),
        "role": "orchestrator",
        "action": "OPEN",
        "trail_id": trail_id,
        "seed": args.seed,
    }
    with (d / "01-orchestrate.jsonl").open("w", encoding="utf-8") as f:
        f.write(json.dumps(open_frame) + "\n")

    set_active_trail(trail_id)
    print(json.dumps({"status": "opened", "trail_id": trail_id}))
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    ensure_dirs()
    trail_id = resolve_trail_arg(args)
    d = trail_dir(trail_id)
    if not (d / "01-orchestrate.jsonl").exists():
        print("error: trail has no 01-orchestrate.jsonl - was it opened?", file=sys.stderr)
        return 1
    plan = read_stdin_json()
    plan.setdefault("role", "planner")
    (d / "02-plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "planned", "trail_id": trail_id}))
    return 0


def cmd_make(args: argparse.Namespace) -> int:
    ensure_dirs()
    trail_id = resolve_trail_arg(args)
    d = trail_dir(trail_id)
    if not (d / "02-plan.json").exists():
        print("error: trail has no 02-plan.json - plan before make", file=sys.stderr)
        return 1
    frame = read_stdin_json()
    frame.setdefault("role", "maker")
    frame.setdefault("ts", now())
    with (d / "03-make.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(frame) + "\n")
    print(json.dumps({"status": "make-frame-appended", "trail_id": trail_id}))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    ensure_dirs()
    trail_id = resolve_trail_arg(args)
    d = trail_dir(trail_id)
    if not (d / "03-make.jsonl").exists():
        print("error: trail has no 03-make.jsonl - make before check", file=sys.stderr)
        return 1
    verdict_frame = read_stdin_json()
    verdict_frame.setdefault("role", "checker")
    verdict_frame.setdefault("ts", now())
    verdict = verdict_frame.get("verdict")
    if verdict not in ("PASS", "FAIL"):
        print("error: check verdict must be 'PASS' or 'FAIL' (L-CHECKER-GATE)", file=sys.stderr)
        return 1
    (d / "04-check.json").write_text(json.dumps(verdict_frame, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "checked", "trail_id": trail_id, "verdict": verdict}))
    return 0


def cmd_reflect(args: argparse.Namespace) -> int:
    ensure_dirs()
    trail_id = resolve_trail_arg(args)
    d = trail_dir(trail_id)
    check_path = d / "04-check.json"
    if not check_path.exists():
        print("error: trail has no 04-check.json - check before reflect", file=sys.stderr)
        return 1
    check_data = json.loads(check_path.read_text(encoding="utf-8"))

    reflect_frame = read_stdin_json()
    reflect_frame.setdefault("role", "reflector")
    reflect_frame.setdefault("ts", now())
    disposition = reflect_frame.get("disposition")
    if disposition not in ("SEAL", "RETRY", "BLOCKED"):
        print("error: disposition must be SEAL, RETRY, or BLOCKED", file=sys.stderr)
        return 1
    if disposition == "SEAL" and check_data.get("verdict") != "PASS":
        print("error: cannot SEAL a trail whose Checker verdict was not PASS (L-CHECKER-GATE)", file=sys.stderr)
        return 1

    (d / "05-reflect.json").write_text(json.dumps(reflect_frame, indent=2) + "\n", encoding="utf-8")

    if disposition == "SEAL":
        trail_meta_path = d / "trail.json"
        trail_meta = json.loads(trail_meta_path.read_text(encoding="utf-8"))
        trail_meta["status"] = "sealed"
        trail_meta["sealed_at"] = now()
        trail_meta_path.write_text(json.dumps(trail_meta, indent=2) + "\n", encoding="utf-8")
        set_active_trail(None)

        # If a queue item is actively claimed, complete it - the trail
        # being sealed is the evidence that the claimed seed is done.
        active_claim = STATE / "active_claim.json"
        if active_claim.exists():
            import subprocess

            subprocess.run([sys.executable, str(QUEUE_RUNTIME), "complete"], check=False)

        print(json.dumps({"status": "sealed", "trail_id": trail_id}))
    else:
        print(json.dumps({"status": "reflected", "trail_id": trail_id, "disposition": disposition}))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    ensure_dirs()
    trail_id = getattr(args, "trail", None) or get_active_trail()
    if not trail_id:
        print("no active trail")
        return 0
    d = TRAILS / trail_id
    if not d.exists():
        print(f"active trail id set ({trail_id}) but directory missing")
        return 1
    phases = ["01-orchestrate.jsonl", "02-plan.json", "03-make.jsonl", "04-check.json", "05-reflect.json"]
    print(f"trail: {trail_id}")
    meta = json.loads((d / "trail.json").read_text(encoding="utf-8"))
    print(f"status: {meta.get('status')}")
    for p in phases:
        exists = (d / p).exists()
        print(f"  {'[x]' if exists else '[ ]'} {p}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PMCRO trail lifecycle runtime")
    sub = p.add_subparsers(dest="cmd", required=True)

    op = sub.add_parser("open")
    op.add_argument("--seed", required=True)
    op.add_argument("--host", default=None)

    for name in ("plan", "make", "check", "reflect"):
        sp = sub.add_parser(name)
        sp.add_argument("--trail", default=None)

    st = sub.add_parser("status")
    st.add_argument("--trail", default=None)

    args = p.parse_args()
    handlers = {
        "open": cmd_open,
        "plan": cmd_plan,
        "make": cmd_make,
        "check": cmd_check,
        "reflect": cmd_reflect,
        "status": cmd_status,
    }
    try:
        return handlers[args.cmd](args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
