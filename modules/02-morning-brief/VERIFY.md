# Verify — Module 02: Morning Brief & Inbox Triage

Checks scope to what was installed: a brief-only install has no triage or
watch checks.

## At install

- [ ] The brief job exists — scheduler entry, or a job file at `jobs/morning-brief.md` plus its `JOBS.md` entry where the workspace is file-based — with the chosen time, timezone, and delivery,
      and is recorded in `JOBS.md`.
- [ ] The brief instructions name every source; kept conditional blocks
      are marked `[IF ...]`; blocks dropped because their source does
      not exist for this install are recorded as dropped in the plan;
      and the instructions contain the rule that an unread source is
      reported as unread — never as clear.
- [ ] If triage was installed: the VIP list and interrupt rules are
      filled in, and the delivery window matches the user's waking hours.
- [ ] If the money watch was installed: the baseline file exists in a
      local workspace file and was built from user-supplied exports
      (no credentials stored anywhere in the workspace); every
      baseline line carries a source pointer (export file, and date
      or line in it) and its figures spot-check against that export;
      the exclusion categories are named in the baseline file
      itself, each marked variability or sensitivity; the run-record
      file exists; and the job is recorded in `JOBS.md`.

## Deferred

- [ ] **First brief** (due: first scheduled morning): arrives on time,
      failures section first, decision-queue items numbered. In a
      file-based workspace where nothing fires jobs, scheduled
      arrival is unverifiable there: read the check as "the brief is
      produced at the first session on or after that morning", and
      the plan records the caveat.
- [ ] **Interrupt test** (due: first week; triage installs only): a test
      message from a VIP address with a direct question interrupts; a
      newsletter does not.
- [ ] **Detector-silence drill** (due: first month; only if watches
      exist): with the user's knowledge, pause one watch past 48 hours;
      the brief flags the silence.
- [ ] **Money-watch first run** (due: first scheduled week; money
      watch installs only): the run's flags match a hand-check of the
      same period's exports, and a no-change week produces a run
      record and no flag.
- [ ] **Baseline untouched by runs** (due: after the first flagged
      money-watch run): the baseline's sha256 before the run equals
      its sha256 after — a run never edits it. After the first
      resolution, exactly the affected line has changed, and it
      carries the decision and its date.
