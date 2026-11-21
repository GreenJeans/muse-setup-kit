#!/usr/bin/env python3
"""kit_doctor.py — read-only drift check for a Muse Setup Kit install.

Mechanical checks only; a mind decides what to do about findings.
Checks, in the workspace:
  1. SETUP-PLAN.md exists and records the kit commit(s) it installed
     from — per module where the plan names them. Mixed pins are
     normal (UPGRADING.md); hidden mixed pins are not, so every pin
     found is listed, not just the first.
  2. JOBS.md exists (the scheduler-of-record).
  3. OPERATING_PROCEDURES.md exists.
  4. Deferred checks ledgered in SETUP-PLAN.md: any line marked
     DEFERRED carrying a YYYY-MM-DD date that has passed is overdue.

Usage:
    python3 kit_doctor.py [--workspace ~/workspace] [--json]

Exit code: 0 = no problems found, 1 = problems found, 2 = bad arguments.
Nothing is written, ever.
"""
import argparse
import datetime
import json
import os
import re
import sys

DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
COMMIT_RE = re.compile(r"\bcommit[:\s]+([0-9a-f]{7,40})\b", re.I)


def main():
    ap = argparse.ArgumentParser(description="Read-only drift check for a kit install.")
    ap.add_argument("--workspace", default=".", help="workspace root (default: cwd)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    ws = os.path.abspath(os.path.expanduser(args.workspace))
    if not os.path.isdir(ws):
        print(f"error: workspace not a directory: {ws}", file=sys.stderr)
        return 2

    problems, notes = [], []

    plan_path = os.path.join(ws, "SETUP-PLAN.md")
    plan_text = ""
    if not os.path.isfile(plan_path):
        problems.append("SETUP-PLAN.md missing — no install plan of record")
    else:
        plan_text = open(plan_path, encoding="utf-8", errors="replace").read()
        pins = []
        for m in COMMIT_RE.finditer(plan_text):
            if m.group(1) not in pins:
                pins.append(m.group(1))
        if not pins:
            problems.append("SETUP-PLAN.md records no kit commit hash")
        elif len(pins) == 1:
            notes.append(f"install commit of record: {pins[0]}")
        else:
            notes.append(f"mixed pins (normal per UPGRADING.md): "
                         f"{len(pins)} distinct commits recorded")
            for line in plan_text.splitlines():
                ms = COMMIT_RE.findall(line)
                if ms:
                    label = line.strip().lstrip("-| ").strip()
                    notes.append(f"  pin {ms[0]}: {label[:80]}")
            notes.append("if a module's pin is not attributable to a "
                         "plan line above, record it per module")

    if not os.path.isfile(os.path.join(ws, "JOBS.md")):
        problems.append("JOBS.md missing — jobs have no scheduler-of-record")
    if not os.path.isfile(os.path.join(ws, "OPERATING_PROCEDURES.md")):
        problems.append("OPERATING_PROCEDURES.md missing")

    today = datetime.date.today()
    overdue = []
    for line in plan_text.splitlines():
        if "DEFERRED" in line.upper():
            for ds in DATE_RE.findall(line):
                try:
                    d = datetime.date.fromisoformat(ds)
                except ValueError:
                    continue
                if d < today:
                    overdue.append({"due": ds, "line": line.strip()[:120]})
    for o in overdue:
        problems.append(f"overdue deferred check (due {o['due']}): {o['line']}")

    receipt = (f"run_receipt: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')} "
               f"workspace={ws} problems={len(problems)}")
    if args.json:
        print(json.dumps({"receipt": receipt, "problems": problems, "notes": notes}, indent=2))
    else:
        print(receipt)
        for n in notes:
            print(f"- note: {n}")
        for pr in problems:
            print(f"- PROBLEM: {pr}")
        if not problems:
            print("no problems found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
