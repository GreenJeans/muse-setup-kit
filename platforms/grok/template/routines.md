# Template contents — routine definitions

Each definition below is complete as a template would carry it:
the schedule, the import-time parameter prompts (declared in the
template), and the saved instruction **verbatim**, in the code
block — the exact text to save, with `<PLACEHOLDERS>` the import
fills from the parameter answers. Two staging facts qualify
that shape (both measured, run 29; the overlay's front door
carries them in full): the declarations are parsed
heuristically — the prompts may not fire at import at all, and
staged values may carry silently into the child — and the
placeholder schedules cannot be stored literally, because
routine creation requires a valid cron expression, so real
schedule values are chosen and filled at staging. Read-backs
are the control for both: after import, a routine's saved
instruction should read as this text **plus two platform-added
lines** — its one-line description prepended and a closing line
naming where its results post — and anything beyond those two
lines is drift. Routines import **paused**; enabling one is the
user's act, after they have read its instruction.

Every instruction is self-contained, because a run is a fresh
context: it names the files it reads, the record it appends, and
what it posts. Every routine appends one line per run to the
run-record — `<name> run at <timestamp> — <one-line outcome>` —
whether or not it posts. A missing line is how a silent failure
is detected; an instruction that omits the append is a defect.

A pasted task brief's first read cannot obey the brief's own
tool rules: the bot reads the brief before it knows them.
Routine instructions that carry tool rules exempt the bootstrap
read explicitly — the first read of the brief itself, by
whatever tool reaches it, is not a violation of the brief's
tool rules — and briefs are written so that first read is safe
under any tool. A tool rule the first read cannot follow is a
rule stated one read too early; state it after the read it
governs, or exempt the read that delivers it.

Timing is the server's and it drifts: dailies run inside windows,
and even an "exact" schedule fired about ten minutes late in
testing. No routine here is time-critical inside ten minutes,
and the brief's overdue windows are set wider than the drift.

Every run counts against the account's weekly usage pool —
test runs included — and the pool's size is not a published
number (the overlay's jobs section carries the vendor's stated
position). Cadence is a budget decision: a routine that runs
daily spends daily, whether or not it posts.

## kit-morning-brief

- **Schedule:** daily at the user's brief time —
  `CRON_TZ=<TIMEZONE> <MINUTE> <HOUR> * * *`, plus the server's
  window.
- **Ask the importing user for:** Timezone; Brief time.

---BEGIN INSTRUCTION---
Read the workspace files `run-record.txt` and
`decision-queue.md`, and `SETUP-PLAN.md` if it exists. Post a
failures-first morning brief to this chat: first, any routine
with no run-record line inside its expected window (allow at
least fifteen minutes of drift before calling a run missing),
any run whose recorded outcome was a failure, and any deferred
check in `SETUP-PLAN.md` whose due date has passed; then the
open decision-queue items by number, oldest first; then one line
confirming what ran cleanly. Do not decide queue items and do
not act on failures — surface them. If a file named above is
missing, say so in the brief rather than reporting that section
as clear. Append one line to `run-record.txt`:
`kit-morning-brief run at <current date and time> — <number of
items surfaced> surfaced`.
---END INSTRUCTION---

## kit-watch-record

The silent-watch slot: one instance per thing watched, renamed
for what it watches. It posts nothing unless its condition
trips — silence is the success state, and the run-record line
is the proof it ran. The target named at import must exist
before the routine is first enabled; when it is a workspace
file, creating it is an install step (`template/workspace.md`),
because a watch over a missing file cannot tell "nothing to
report" from "nothing there". The match is pinned
**case-sensitive, the condition as written** — the instruction
says so, because the rehearsal's bot had to flag the ambiguity
unprompted (run 29). An installer who wants a case-insensitive
match changes the instruction deliberately and records the
change in `SETUP-PLAN.md`; nobody silently inherits a looser
match.

- **Schedule:** daily — `CRON_TZ=<TIMEZONE> 15 9 * * *`, plus the
  server's window.
- **Ask the importing user for:** Timezone; What to watch (the
  file or source to check, and the condition that counts as a
  trip).

---BEGIN INSTRUCTION---
Check <WATCH TARGET> for <TRIP CONDITION>. The condition is
matched exactly as written — the match is case-sensitive.
Append one line to
`run-record.txt`: `kit-watch-record run at <current date and
time> — nothing to report`, or, if the condition trips,
`kit-watch-record run at <current date and time> — TRIPPED:
<one line naming what was found>`. Post to this chat only if
the condition trips, with the same one line. Do not fix,
change, or clear anything you find; reporting is the whole job.
---END INSTRUCTION---

## kit-memory-audit

- **Schedule:** weekly — `CRON_TZ=<TIMEZONE> 0 10 * * 1`, plus
  the server's window.
- **Ask the importing user for:** Timezone.

---BEGIN INSTRUCTION---
Run the memory-audit skill: inventory this bot's memory stores,
the account-level user profile, and the shared stores; lint for
contradictions and superseded facts still standing; sample
facts and check them against their sources in the workspace;
and read `SETUP-PLAN.md`, if it exists, for deferred checks
whose due date has passed. Post the audit report to this chat:
findings quoted on both sides, sampled facts marked confirmed,
contradicted, or unverifiable, and overdue deferred checks
named. Propose corrections as remove/add pairs and apply none
of them — corrections wait for the user's approval in
conversation. Append one line to `run-record.txt`:
`kit-memory-audit run at <current date and time> — <number of
findings> findings`.
---END INSTRUCTION---
