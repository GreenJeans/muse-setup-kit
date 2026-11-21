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
- [ ] If triage was installed: the triage job file exists, built
      from `triage-job.template.md`, with the VIP list, the
      interrupt rules, and the shield's immediacy set (the VIPs
      plus the institutions named at install) filled in; the
      shield check is ordered before the interrupt rules; and the
      delivery window matches the user's waking hours.
- [ ] If the money watch was installed: the baseline file exists in a
      local workspace file and was built from user-supplied exports
      (no credentials stored anywhere in the workspace); every
      baseline line carries a source pointer (export file, and date
      or line in it) and its figures spot-check against that export;
      the exclusion categories are named in the baseline file
      itself, each marked variability or sensitivity; the run-record
      file exists; and the job is recorded in `JOBS.md`.
- [ ] If the promises ledger was installed: the ledger file exists
      in its canonical shape (I owe / Waiting on sections); every
      seeded entry carries its grade — a verbatim quote with a
      source locator, the user's own record with its wording
      marked unverified, or unverified with the paraphrase
      recorded as a note, never as a quote; an entry with no date
      reads `Due: not set`; it is a local workspace file, not on
      any shared surface; and the brief job's instructions keep
      the template's `[IF promises ledger installed]` block,
      which names the ledger as a source.

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
- [ ] **Ledger surfacing** (due: first week; ledger installs only):
      an entry seeded with a past due date appears in the brief's
      Today section, quoted from the ledger with its due date; a
      follow-up draft, if one was prepared, exists as a draft —
      nothing was sent. A `Due: not set` entry, if any was
      seeded, is named in the first monthly pass after install.
- [ ] **Shield fixture drill** (due: first month; triage installs
      only): run the scan over five scam fixtures — an impersonated
      bank notice, a toll text, a package-fee notice, a
      family-emergency money request, a look-alike sender domain —
      and five legitimate look-alikes: a real bank alert, a real
      delivery notice, a genuine message from a new number, a real
      verification prompt, a newsletter carrying a deadline. Pass:
      all five scams flagged, each with its one-line reason; no
      legitimate message graded "scam" ("unverified sender" is an
      acceptable grade for the genuinely ambiguous); no fixture
      link followed and no fixture number called.
