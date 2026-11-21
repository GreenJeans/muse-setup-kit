#!/usr/bin/env python3
"""stage_check.py — staged-proposal expiry check for module 08.

The module's rule: staging expires undecided after 14 days; expiry
auto-rejects (never applies). This script is the runner for that rule.

Report-only by default: lists staged proposals older than the expiry
(from the `Staged: YYYY-MM-DD` line in proposal.md, falling back to
the folder's mtime). With --apply it moves expired folders into
staged/expired/ — a move the module pre-authorizes, since expiry is a
rejection, not an application. It never touches queue files or skills.

Usage:
  stage_check.py [--staged-dir <dir>] [--days 14] [--apply] [--json]

Exit code: 0 = nothing expired, 1 = expired items found (or moved),
2 = bad arguments.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

DATE_RE = re.compile(r"Staged:\s*(20\d{2}-\d{2}-\d{2})")
SKIP = ("expired", "applied")


def staged_date(folder):
    prop = os.path.join(folder, "proposal.md")
    try:
        m = DATE_RE.search(open(prop, encoding="utf-8", errors="replace").read())
        if m:
            return datetime.date.fromisoformat(m.group(1)), "proposal.md"
    except OSError:
        pass
    ts = os.path.getmtime(folder)
    return datetime.datetime.fromtimestamp(ts).date(), "folder mtime"


def main():
    ap = argparse.ArgumentParser(description="Staged-proposal expiry check (module 08).")
    ap.add_argument("--staged-dir", default="staged")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--apply", action="store_true",
                    help="move expired folders into staged/expired/")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.staged_dir))
    if not os.path.isdir(root):
        print(f"error: staged dir not found: {root}", file=sys.stderr)
        return 2

    today = datetime.date.today()
    expired, current = [], []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path) or name in SKIP or name.startswith("shadow-"):
            continue
        d, source = staged_date(path)
        age = (today - d).days
        entry = {"name": name, "staged": str(d), "age_days": age, "date_source": source}
        (expired if age > args.days else current).append(entry)

    moved = []
    if args.apply and expired:
        dest_root = os.path.join(root, "expired")
        os.makedirs(dest_root, exist_ok=True)
        for e in expired:
            shutil.move(os.path.join(root, e["name"]), os.path.join(dest_root, e["name"]))
            moved.append(e["name"])

    receipt = (f"run_receipt: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')} "
               f"staged={root} expired={len(expired)} current={len(current)} applied={len(moved)}")
    if args.json:
        print(json.dumps({"receipt": receipt, "expired": expired,
                          "current": current, "moved": moved}, indent=2))
    else:
        print(receipt)
        for e in expired:
            verb = "MOVED to expired/" if e["name"] in moved else "EXPIRED (report only)"
            print(f"- {verb}: {e['name']} staged {e['staged']} ({e['age_days']}d, via {e['date_source']})")
        if not expired:
            print("nothing expired")
    return 1 if expired else 0


if __name__ == "__main__":
    sys.exit(main())
