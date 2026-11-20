#!/usr/bin/env python3
"""Reference memory linter for the Muse Setup Kit (module 01).

Deterministic and read-only: it writes only its report. Three checks:

  A. Every compiled page carries a provenance header
     (schema_version + last_verified within the first 40 lines).
  B. Live-section bullets that state a figure (money, dates, counts)
     carry a source: a "(verify: ...)" pointer or a "Source:" note.
     "Live" means above the page's History/Superseded section.
  C. Jobs named in the operating procedures exist in JOBS.md (the
     scheduler-of-record): a backticked name on a procedures line that
     mentions "job" is treated as a job name and must have a JOBS.md
     entry. (One direction only — operational jobs in JOBS.md need not
     be named in the procedures.)

Exclusions: files under logs/, reports/, or tools/ directories, files
with "fidelity-test" in the name (schema-mandated fixtures, not compiled
pages), and anything matching a glob in a `.lintignore` file in the
memory directory are not treated as compiled pages.

Every report opens with a run receipt: timestamp, files scanned, checks
run, findings count. Exit code 0 = no high-severity findings, 1 = some.

Usage:
  memory_lint.py --memory-dir ~/memory --procedures ~/OPERATING_PROCEDURES.md \
                 --jobs ~/JOBS.md --report ~/memory/reports/lint-report.md
All arguments optional; defaults suit a kit-style workspace layout.
This is a starting point — adapt the heuristics to your store.
"""

import argparse
import datetime
import os
import re
import sys

FIGURE = re.compile(r"(\$\s?\d|\b\d{4}-\d{2}-\d{2}\b|\b\d+\s?(mg|kg|km|mi|%|percent)\b)")
HISTORY_HEAD = re.compile(r"^##\s+(History|Superseded)\b", re.M)
BACKTICK = re.compile(r"`([a-z0-9][a-z0-9\-_]{2,})`")


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def check_headers(pages):
    findings = []
    for path, text in pages:
        head = "\n".join(text.splitlines()[:40])
        if "schema_version" not in head or "last_verified" not in head:
            findings.append(("high", f"A: {path}: missing provenance header"))
    return findings


def check_figures(pages):
    findings = []
    for path, text in pages:
        live = HISTORY_HEAD.split(text)[0]
        for i, line in enumerate(live.splitlines(), 1):
            if line.lstrip().startswith("- ") and FIGURE.search(line):
                if "(verify:" not in line and "Source:" not in line:
                    findings.append(
                        ("med", f"B: {path}:{i}: figure without a verify pointer"))
    return findings


def check_jobs(procedures_path, jobs_path):
    findings = []
    proc = read(procedures_path)
    jobs = read(jobs_path)
    if proc is None or jobs is None:
        missing = procedures_path if proc is None else jobs_path
        return [("med", f"C: cannot read {missing}; check skipped")]
    job_names = set()
    for line in jobs.splitlines():
        m = re.match(r"\s*[-|]\s*`?([a-z0-9][a-z0-9\-_]{2,})`?", line)
        if m:
            job_names.add(m.group(1))
    for line in proc.splitlines():
        if "job" in line.lower():
            for name in BACKTICK.findall(line):
                if name not in job_names:
                    findings.append(
                        ("med", f"C: job '{name}' named in procedures has no JOBS.md entry"))
    return findings


def main():
    ap = argparse.ArgumentParser()
    home = os.path.expanduser("~")
    ap.add_argument("--memory-dir", default=os.path.join(home, "memory"))
    ap.add_argument("--procedures", default=os.path.join(home, "OPERATING_PROCEDURES.md"))
    ap.add_argument("--jobs", default=os.path.join(home, "JOBS.md"))
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    import fnmatch

    ignore = []
    ignore_text = read(os.path.join(args.memory_dir, ".lintignore"))
    if ignore_text:
        ignore = [ln.strip() for ln in ignore_text.splitlines()
                  if ln.strip() and not ln.startswith("#")]

    def excluded(path):
        rel = os.path.relpath(path, args.memory_dir)
        parts = rel.split(os.sep)
        if any(p in ("logs", "reports", "tools") for p in parts[:-1]):
            return True
        if "fidelity-test" in parts[-1]:
            return True
        if parts[-1] == "INDEX.md":
            return True  # generated listings, stamped by the tools that rebuild them
        if parts[-1] == "lint-report.md":
            return True  # this tool's own output, wherever the user keeps it
        if args.report and os.path.abspath(path) == os.path.abspath(args.report):
            return True  # never lint the report this run is writing
        return any(fnmatch.fnmatch(rel, pat) for pat in ignore)

    pages = []
    for root, _dirs, files in os.walk(args.memory_dir):
        for name in sorted(files):
            if name.endswith(".md"):
                path = os.path.join(root, name)
                if excluded(path):
                    continue
                text = read(path)
                if text is not None:
                    pages.append((path, text))
    main_memory = os.path.join(os.path.dirname(args.memory_dir.rstrip("/")), "MEMORY.md")
    if os.path.exists(main_memory):
        text = read(main_memory)
        if text is not None:
            pages.append((main_memory, text))

    findings = []
    findings += check_headers(pages)
    findings += check_figures(pages)
    findings += check_jobs(args.procedures, args.jobs)

    high = sum(1 for sev, _ in findings if sev == "high")
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        f"run_receipt: {now} files_scanned={len(pages)} checks=A,B,C findings={len(findings)} high={high}",
        "",
        "# Memory lint report",
        "",
    ]
    if findings:
        lines += [f"- [{sev}] {msg}" for sev, msg in findings]
    else:
        lines.append("No findings.")
    report = "\n".join(lines) + "\n"

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(report)
    sys.stdout.write(report)
    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())
