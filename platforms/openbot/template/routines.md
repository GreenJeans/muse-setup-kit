# Template contents — routine definitions

Each definition below is complete as an install would create
it: the schedule, and the saved instruction **verbatim**, in
the code block — the exact text to save, with
`<PLACEHOLDERS>` filled at creation from the user's answers.
Routines are created paused, their saved instructions read
back against this text before anything is enabled, and
enabling one is the user's act, after they have read its
instruction (battery Test 2, Pass: saved instructions read
back verbatim, runs execute with full tools, fires measured
at 0–3 seconds of drift).

Every instruction is self-contained, because a run is a fresh
context and `AGENTS.md` does not reach it (Test 1, Partial):
each instruction names the files it reads, the record it
appends, what it posts, and the rules it needs. Every routine
appends one line per run to the run-record — `<name> run at
<timestamp> — <one-line outcome>` — whether or not it posts.
A missing line is how a silent failure is detected; an
instruction that omits the append is a defect. Fires while
the host sleeps do not run; a missed window is surfaced as
missed by the brief, never silently caught up.

Silence is a token, not an instruction: a routine with
nothing to report answers `[[no-update]]` and appends its
run-record line. The token is vendor-documented and untested
(Test 10, Fail: instruction-only silence posted anyway; the
record line was written correctly) — the first silent run
after install is the probe, and a post where silence was
intended is a finding, not a pass.

## kit-morning-brief

- **Schedule:** daily at the user's brief time
  (`<TIMEZONE>`, `<TIME>` chosen at creation and read back
  from the routines store).

---BEGIN INSTRUCTION---
Read the workspace files `run-record.txt` and
`decision-queue.md`, and `SETUP-PLAN.md` if it exists. Post a
failures-first morning brief to this chat: first, any routine
with no run-record line inside its expected window (allow a
few minutes of drift before calling a run missing; a window
missed across a host sleep gap is named as missed, not
caught up), any run whose recorded outcome was a failure,
and any deferred check in `SETUP-PLAN.md` whose due date has
passed; then the open decision-queue items by number, oldest
first; then one line confirming what ran cleanly. Do not
decide queue items and do not act on failures — surface them.
If a file named above is missing, say so in the brief rather
than reporting that section as clear. Append one line to
`run-record.txt`: `kit-morning-brief run at <current date
and time> — <number of items surfaced> surfaced`.
---END INSTRUCTION---

## kit-watch-record

The silent-watch slot: one instance per thing watched,
renamed for what it watches. It is meant to post nothing
unless its condition trips; whether the `[[no-update]]`
token suppresses the post is untested, and the first silent
run is the probe — the run-record line is the proof it ran
either way. The target named at creation must exist
before the routine is first enabled; when it is a workspace
file, creating it is an install step (`template/workspace.md`),
because a watch over a missing file cannot tell "nothing to
report" from "nothing there". The match is pinned
**case-sensitive, the condition as written** — the
instruction says so, because a looser match nobody chose is
a defect. An installer who wants a case-insensitive match
changes the instruction deliberately and records the change
in `SETUP-PLAN.md`; nobody silently inherits a looser match.

- **Schedule:** daily (`<TIMEZONE>`, `<TIME>` chosen at
  creation and read back from the routines store).
- **Chosen at creation:** What to watch (the file or source
  to check, and the condition that counts as a trip).

---BEGIN INSTRUCTION---
Check <WATCH TARGET> for <TRIP CONDITION>. The condition is
matched exactly as written — the match is case-sensitive.
Append one line to `run-record.txt`: `kit-watch-record run
at <current date and time> — nothing to report`, or, if the
condition trips, `kit-watch-record run at <current date and
time> — TRIPPED: <one line naming what was found>`. If the
condition does not trip, answer `[[no-update]]` and post
nothing else. If it trips, post to this chat the same one
line. Do not fix, change, or clear anything you find;
reporting is the whole job.
---END INSTRUCTION---

## kit-memory-audit

- **Schedule:** weekly (`<TIMEZONE>`, `<TIME>` chosen at
  creation and read back from the routines store).

---BEGIN INSTRUCTION---
Run the memory-audit skill over the workspace memory files:
inventory the long-term memory file, the daily logs, and the
person and group pages; lint for contradictions, superseded
claims still standing as current, and precise figures
without verify pointers; sample claims and check them
against their sources in the workspace; and read
`SETUP-PLAN.md`, if it exists, for deferred checks whose due
date has passed. Post the audit report to this chat: findings
quoted on both sides, sampled claims marked confirmed,
contradicted, or unverifiable, and overdue deferred checks
named. Propose corrections as file edits — rewrite the live
claim, move the replaced claim to Superseded or History in
the same edit — and apply none of them: corrections wait for
the user's approval in conversation. Append one line to
`run-record.txt`: `kit-memory-audit run at <current date and
time> — <number of findings> findings`.
---END INSTRUCTION---
