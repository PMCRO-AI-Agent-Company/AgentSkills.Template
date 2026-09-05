#!/usr/bin/env python3
"""PMCRO lightweight queue + checkpoint runtime (governance seed).

Commands:
  list | claim | checkpoint | complete | status
"""
from __future__ import annotations

import argparse
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # .pmcro
QUEUE = ROOT / "queue"
CLAIMED = QUEUE / "claimed"
DONE = QUEUE / "done"
CHECKPOINTS = ROOT / "state" / "checkpoints"
STATE = ROOT / "state"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    for p in (QUEUE, CLAIMED, DONE, CHECKPOINTS, STATE):
        p.mkdir(parents=True, exist_ok=True)


def list_seeds() -> list[Path]:
    return sorted(QUEUE.glob("seed-*.json"))


def cmd_list(_: argparse.Namespace) -> int:
    ensure_dirs()
    seeds = list_seeds()
    claimed = sorted(CLAIMED.glob("seed-*.json"))
    print(f"pending={len(seeds)} claimed={len(claimed)}")
    for p in seeds:
        data = json.loads(p.read_text(encoding="utf-8"))
        print(f"  PENDING  {p.name}  id={(data.get('metadata') or {}).get('id')}")
    for p in claimed:
        print(f"  CLAIMED  {p.name}")
    return 0


def cmd_claim(_: argparse.Namespace) -> int:
    ensure_dirs()
    seeds = list_seeds()
    if not seeds:
        print("nothing to claim")
        return 0
    src = seeds[0]
    data = json.loads(src.read_text(encoding="utf-8"))
    claim_id = str(uuid.uuid4())
    data["_claim"] = {"claim_id": claim_id, "claimed_at": now()}
    dest = CLAIMED / src.name
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    src.unlink()
    active = STATE / "active_claim.json"
    active.write_text(json.dumps({"file": dest.name, "claim_id": claim_id, "at": now()}, indent=2) + "\n")
    print(json.dumps({"status": "claimed", "file": dest.name, "claim_id": claim_id}))
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    ensure_dirs()
    active_trail = STATE / "active_trail_id.txt"
    trail_id = active_trail.read_text().strip() if active_trail.exists() else "none"
    payload = {
        "checkpoint_id": str(uuid.uuid4()),
        "ts": now(),
        "trail_id": trail_id,
        "note": args.note or "",
        "active_claim": None,
    }
    claim_path = STATE / "active_claim.json"
    if claim_path.exists():
        payload["active_claim"] = json.loads(claim_path.read_text(encoding="utf-8"))
    out = CHECKPOINTS / f"cp-{payload['checkpoint_id']}.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "checkpoint", "path": str(out.relative_to(ROOT.parent))}))
    return 0


def cmd_complete(_: argparse.Namespace) -> int:
    ensure_dirs()
    claim_path = STATE / "active_claim.json"
    if not claim_path.exists():
        print("no active claim")
        return 1
    meta = json.loads(claim_path.read_text(encoding="utf-8"))
    src = CLAIMED / meta["file"]
    if not src.exists():
        print("claimed file missing:", src)
        return 1
    data = json.loads(src.read_text(encoding="utf-8"))
    data["_complete"] = {"completed_at": now(), "claim_id": meta.get("claim_id")}
    dest = DONE / src.name
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    src.unlink()
    claim_path.unlink()
    print(json.dumps({"status": "completed", "file": dest.name}))
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    ensure_dirs()
    trail = STATE / "active_trail_id.txt"
    print("active_trail:", trail.read_text().strip() if trail.exists() else "none")
    print("pending:", len(list_seeds()))
    print("claimed:", len(list(CLAIMED.glob("seed-*.json"))))
    print("done:", len(list(DONE.glob("seed-*.json"))))
    print("checkpoints:", len(list(CHECKPOINTS.glob("cp-*.json"))))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PMCRO queue/checkpoint runtime")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("claim")
    cp = sub.add_parser("checkpoint")
    cp.add_argument("--note", default="")
    sub.add_parser("complete")
    sub.add_parser("status")
    args = p.parse_args()
    return {
        "list": cmd_list,
        "claim": cmd_claim,
        "checkpoint": cmd_checkpoint,
        "complete": cmd_complete,
        "status": cmd_status,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
