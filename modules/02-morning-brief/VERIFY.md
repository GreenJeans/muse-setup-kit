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
      plus the institutions named at install, each with every
      known sending domain and number recorded) filled in; the
      shield check is ordered before the interrupt rules; the
      delivery window matches the user's waking hours; the
      detector script exists and polls on the stated cadence,
      checking the never-mute classes before its noise list; and
      the run-record, flag-log, and state files exist at the
      paths the job file names.
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
      seeded entry carries its `Grade:` marker — a verbatim quote
      with a source locator (the words themselves, read by the
      agent), the user's own record with its wording
      marked unverified, or unverified with the paraphrase
      recorded as a note, never as a quote; an entry with no date
      reads `Due: not set`; the file carries its `(review-by: ...)`
      date; it is inventoried in the plan's installed-file
      baseline as an accumulating file; it is a local workspace
      file, not on
      any shared surface; and the brief job's instructions keep —
      or, for a ledger installed after the brief, restore — all
      three of the template's `[IF promises ledger installed]`
      blocks (the ledger as a source, entries in Today, undated
      entries in the monthly pass).

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
- [ ] **Detector dry run, both ways** (due: first week; triage
      installs only): with unjudged mail in the mailbox, a poll
      wakes the agent; with every new message on the noise list,
      a poll stays silent and still writes its run record. A
      detector that only ever demonstrates one direction is
      unverified in the other.
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
- [ ] **Ledger surfacing** (due: first week; ledger installs only):
      an entry seeded with a past due date appears in the brief's
      Today section, quoted from the ledger with its due date; a
      follow-up draft, if one was prepared, exists as a draft —
      nothing was sent. A `Due: not set` entry, if any was
      seeded, is named in the first monthly pass after install.
      An unverified entry, if any was seeded, is named unverified
      in the brief — not quoted with a verbatim entry's authority.
- [ ] **Triage liveness and flag route** (due: first week; triage
      installs only): every scan run inside the delivery window
      has left a run record; a flag raised in the window appears
      in the next brief's Failures with its one-line reason; and
      with the scan paused for 2 hours inside the window (with
      the user's knowledge), the brief names the gap as a failure
      of the scan itself.
- [ ] **Shield fixture drill** (due: first month; triage installs
      only): run the scan over five scam fixtures in the mailbox
      it scans — an impersonated
      bank notice, a toll-charge notice, a package-fee notice, a
      family-emergency money request, a look-alike sender domain —
      and five legitimate look-alikes: a real bank alert, a real
      delivery notice, a genuine alert from a second, unlisted
      sending domain of an institution in the immediacy set, a real
      verification prompt, a newsletter carrying a deadline. Pass:
      all five scams flagged, each with its one-line reason; no
      legitimate message graded "scam" ("unverified sender" is an
      acceptable grade for the genuinely ambiguous); the
      unlisted-domain alert is graded unverified, not scam, does
      not interrupt in any class, is in the flag log, is
      proposed for the immediacy set through the decision queue,
      and the set itself is unchanged by the scan; every flag —
      immediate or not — is in the flag log; no fixture
      link followed and no fixture number called.
