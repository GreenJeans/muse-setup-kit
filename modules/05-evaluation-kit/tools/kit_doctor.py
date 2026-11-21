#!/usr/bin/env python3
"""kit_doctor.py — read-only drift check for a Muse Setup Kit install.

Mechanical checks only; a mind decides what to do about findings.
Checks, in the workspace:
  1. SETUP-PLAN.md exists and records the kit commit(s) it installed
     from — per module where the plan names them. Mixed pins are
     normal (UPGRADING.md); hidden mixed pins are not, so every pin
     found is listed, not just the first. A line explicitly labeled
     as the pin ("pin: <hash>", or a "commit <hash>" line) is
     preferred: when any labeled pin exists, the looser scan for
     bare hashes is skipped, so a hash a plan mentions only to
     disclaim it ("this hash was NOT used") is never counted.
  2. JOBS.md exists (the scheduler-of-record).
  3. OPERATING_PROCEDURES.md exists.
  4. Deferred checks ledgered in SETUP-PLAN.md: a line marked
     DEFERRED whose "due: YYYY-MM-DD" field names a date that has
     passed is overdue. The wizard's ledger format carries the due
     date in that field; a DEFERRED line without it falls back to
     any date the line carries.
  5. Installed-file baseline: SETUP-PLAN.md lines of the form
     "- installed: <relpath> sha256:<hex>" record the hash of every
     file the wizard installed. A baselined file whose current hash
     differs is reported as edited since install (a note — editing
     is legitimate; UPGRADING.md consumes the list as its conflict
     list). A baselined file that no longer exists is a problem.
     Lines ending in "accumulating" name files that grow by design
     (the queue, JOBS.md, ledgers): inventoried, never diffed.
     A hashed line may carry a trailing file class —
     "static-verbatim" or "static-rendered" (docs/library.md);
     lines written before the class vocabulary existed carry none
     and are read the same way. The class is what the wizard's
     repair verb reads: only static-verbatim lines are repairable.

Usage:
    python3 kit_doctor.py [--workspace ~/workspace] [--json]

Exit code: 0 = no problems found, 1 = problems found, 2 = bad arguments.
Nothing is written, ever.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
COMMIT_RE = re.compile(r"\bcommit[:\s]+([0-9a-f]{7,40})\b", re.I)
PIN_LABEL_RE = re.compile(r"\bpin\s*[:=]\s*([0-9a-f]{7,40})", re.I)
DUE_RE = re.compile(r"\bdue:?\s*(20\d{2}-\d{2}-\d{2})", re.I)


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
        for m in PIN_LABEL_RE.finditer(plan_text):
            if m.group(1) not in pins:
                pins.append(m.group(1))
        # Older plans also record pins as a bare 40-hex hash on a line
        # naming the pin or HEAD ("installed from HEAD <hash>"). That
        # loose scan runs only when no labeled pin exists: a plan may
        # mention a hash precisely to disclaim it, and a disclaimed
        # hash is not a pin. A baseline line is not a pin either:
        # skip any line carrying sha256:.
        if not pins:
            for line in plan_text.splitlines():
                if "sha256:" in line:
                    continue
                low = line.lower()
                if "pin" in low or "head" in low:
                    for h in re.findall(r"\b[0-9a-f]{40}\b", line):
                        if h not in pins:
                            pins.append(h)
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

    base_re = re.compile(r"^-\s+installed:\s+(\S+)\s+sha256:([0-9a-f]{64})(?:\s+(?:static-verbatim|static-rendered))?\s*$")
    acc_re = re.compile(r"^-\s+installed:\s+(\S+)\s+accumulating\s*$")
    baselined = 0
    accumulating = 0
    for line in plan_text.splitlines():
        if acc_re.match(line.strip()):
            accumulating += 1
            continue
        m = base_re.match(line.strip())
        if not m:
            continue
        baselined += 1
        rel, want = m.group(1), m.group(2)
        fp = os.path.join(ws, rel)
        if not os.path.isfile(fp):
            problems.append(f"baselined file missing: {rel}")
            continue
        got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if got != want:
            notes.append(f"edited since install: {rel}")
    if baselined or accumulating:
        notes.append(f"installed-file baseline: {baselined} hashed, "
                     f"{accumulating} accumulating (not diffed)")
    elif plan_text:
        notes.append("no installed-file baseline recorded (pre-v0.5 "
                     "install, or the wizard has not stamped one yet)")

    today = datetime.date.today()
    overdue = []
    for line in plan_text.splitlines():
        if "DEFERRED" in line.upper():
            # The ledger format carries the due date in an explicit
            # "due: YYYY-MM-DD" field; when it is present it governs,
            # and other dates in the row (a note, a status) are not
            # due dates. Without the field, fall back to any date
            # the line carries.
            dm = DUE_RE.search(line)
            dates = [dm.group(1)] if dm else DATE_RE.findall(line)
            for ds in dates:
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
