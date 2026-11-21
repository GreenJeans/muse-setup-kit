#!/usr/bin/env python3
"""Reference curator for the Muse Setup Kit (module 08).

Deterministic, stdlib only, no network, no LLM. It:

  - rescans the custom-skills folder (new skills get ledger records),
  - recomputes exemptions from live sources (the jobs record, the
    procedures and instruction files, other skills' files, managed
    review records in skill.yaml, and the pinned flag in the ledger),
  - updates lifecycle states in the ledger: stale at 14 days without
    activity, archive candidate at 30 days (grace floor: a never-used
    skill is not a candidate until it is at least 14 days old),
  - prints a JSON report.

It NEVER moves or deletes a folder and NEVER writes the decision
queue. Archive moves happen only in the module's apply procedure,
after the user approves a [type: skill-curator] queue item.

Usage:
  curator.py --skills-dir <dir> --ledger <path> \
             [--jobs-file <JOBS.md>] \
             [--reference-file <procedures-or-instructions.md>] ...

All arguments optional; defaults suit a kit-style workspace layout
(./custom-skills and ./skill-lifecycle/skill-usage.json). Counts in the
ledger are best-effort and under-report by design; that is why this
script proposes and never acts.
"""

import argparse
import re
import json
import sys
from datetime import date, datetime
from pathlib import Path

STALE_DAYS = 14
ARCHIVE_DAYS = 30
GRACE_DAYS = 14


def parse(d):
    return datetime.strptime(d, "%Y-%m-%d").date() if d else None


def read_text(path):
    try:
        return Path(path).read_text(errors="ignore")
    except OSError:
        return ""


def mentions(text, name):
    # Whole-token match: a skill named "brief" must not exempt itself
    # off every prose use of the word.
    return re.search(r"(?<![A-Za-z0-9_-])" + re.escape(name) +
                     r"(?![A-Za-z0-9_-])", text) is not None


def job_mentions(jobs_text, name, all_names=()):
    # A job reference means a job *entry* whose name is the skill's
    # name, or the skill's name plus a suffix (tax-docs-prep runs
    # tax-docs — a job named for the skill's task is a reference).
    # When two skill names could claim one job, the longest wins, so
    # tax-docs-prep never exempts a skill named tax. A prose mention
    # inside a job's description is not a reference.
    for line in jobs_text.splitlines():
        s = line.strip().lstrip("-|* ").rstrip("*")
        token = re.split(r"[\s:]", s, maxsplit=1)[0].strip("*`|")
        if token == name:
            return True
        if token.startswith(name + "-"):
            longer = [o for o in all_names if o != name and len(o) > len(name)
                      and (token == o or token.startswith(o + "-"))]
            if not longer:
                return True
    return False


def exemptions_for(name, rec, jobs_text, reference_texts, skill_texts, skills_dir, all_names=()):
    ex = set()
    if rec.get("pinned"):
        ex.add("pinned")
    if job_mentions(jobs_text, name, all_names):
        ex.add("job-ref")
    if any(mentions(text, name) for text in reference_texts):
        ex.add("procedures-ref")
    for other, txt in skill_texts.items():
        if other != name and mentions(txt, name):
            ex.add(f"skill-ref:{other}")
    # Managed review cycle: a skill.yaml whose review is owned elsewhere.
    # The exemption lapses with the cycle: a review_after date in the
    # past means nobody owns the review anymore and the curator resumes.
    sy = skills_dir / name / "skill.yaml"
    if sy.exists():
        y = read_text(sy)
        if "managed: true" in y:
            m = re.search(r"review_after:\s*(\d{4}-\d{2}-\d{2})", y)
            if not m or parse(m.group(1)) >= datetime.now().date():
                ex.add("managed-review-cycle")
    return sorted(ex)


def main():
    ap = argparse.ArgumentParser(description="Skill lifecycle curator (report-only).")
    ap.add_argument("--skills-dir", default="custom-skills")
    ap.add_argument("--ledger", default="skill-lifecycle/skill-usage.json")
    ap.add_argument("--jobs-file", default="JOBS.md")
    ap.add_argument("--reference-file", action="append", default=[],
                    help="Procedures/instructions file scanned for references; repeatable.")
    args = ap.parse_args()

    skills_dir = Path(args.skills_dir)
    ledger_path = Path(args.ledger)
    today = date.today()

    ledger = json.loads(read_text(ledger_path) or "{}") or {"version": 1, "skills": {}}
    skills = ledger.setdefault("skills", {})

    on_disk = []
    if skills_dir.is_dir():
        on_disk = sorted(p.name for p in skills_dir.iterdir()
                         if p.is_dir() and p.name != ".archive")

    skill_texts = {}
    for name in on_disk:
        parts = []
        for f in (skills_dir / name).rglob("*"):
            if f.is_file() and f.suffix in (".md", ".yaml"):
                parts.append(read_text(f))
        skill_texts[name] = "\n".join(parts)

    jobs_text = read_text(args.jobs_file)
    reference_texts = [read_text(p) for p in args.reference_file]

    report = {"date": str(today), "skills": {}, "stale": [],
              "archive_candidates": [], "new": [], "unseeded": []}

    # all_names for exemption matching is on_disk (every skill that
    # exists), never the ledger-so-far: on a first run the ledger is
    # still being built, and a partial name list breaks longest-match.
    for name in on_disk:
        if name not in skills:
            skills[name] = {"created": str(today), "seeded_on": str(today),
                            "pinned": False,
                            "last_viewed": None, "last_used": None,
                            "last_patched": None, "views": 0, "uses": 0,
                            "patches": 0, "exemptions": [], "state": "active"}
            report["new"].append(name)
        rec = skills[name]
        # Unseeded check comes BEFORE the stamp below: a record with
        # no verifiable created date is reported on the run that
        # first seeds it. (Checking after stamping makes this branch
        # unreachable — the stamp guarantees an anchor.)
        if parse(rec.get("created")) is None and not rec.get("seeded_on"):
            report["unseeded"].append(name)
        if not rec.get("seeded_on"):
            rec["seeded_on"] = str(today)
        rec["exemptions"] = exemptions_for(name, rec, jobs_text,
                                           reference_texts, skill_texts,
                                           skills_dir, on_disk)

        activity = [parse(rec.get(k)) for k in ("last_viewed", "last_used", "last_patched")]
        activity = [d for d in activity if d]
        # Anchor: the created date if a verifiable one exists, else the
        # day the ledger first seeded the record. A record with neither
        # anchors to today AND is reported unseeded — it must surface,
        # not silently idle at 0 forever.
        anchor = parse(rec.get("created")) or parse(rec.get("seeded_on")) or today
        last_activity = max(activity) if activity else anchor
        idle = (today - last_activity).days
        age = (today - anchor).days
        # Counts are seeded as zero, never null — but coerce anyway:
        # a null count must not read as "used" and defeat the grace floor.
        never_used = not activity and (rec.get("uses") or 0) == 0 and (rec.get("views") or 0) == 0

        if rec["exemptions"]:
            state = "active (exempt)"
        elif idle >= ARCHIVE_DAYS and not (never_used and age < ARCHIVE_DAYS + GRACE_DAYS):
            state = "archive-candidate"
            report["archive_candidates"].append(name)
        elif idle >= STALE_DAYS:
            state = "stale"
            report["stale"].append(name)
        else:
            state = "active"
        rec["state"] = "active" if state.startswith("active") else state
        report["skills"][name] = {
            "state": state, "idle_days": idle, "age_days": age,
            "exemptions": rec["exemptions"],
            "last_activity": str(last_activity) if last_activity else None,
        }

    ledger["last_curator_run"] = str(today)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
