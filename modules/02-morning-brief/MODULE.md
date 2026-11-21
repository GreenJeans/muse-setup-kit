# Module 02 — Morning Brief & Inbox Triage

**Reads:** calendar, mailbox, task lists, decision queue, watch outputs;
for the money watch, the statement/CSV exports the user supplies.
**Writes:** one brief per day; draft replies only, sent only with
approval; for the money watch, its baseline and run-record files and
its job file.
**Network:** your connected accounts. **Jobs:** daily brief; optional
30-minute triage scan; optional weekly money watch.

## Purpose

One message a day that earns its place: what failed, what needs a decision,
what's on today — in that order. Plus a triage discipline so genuinely
urgent mail interrupts and everything else waits for the brief.

## The brief, in order

0. **Failures first.** Jobs that owed a deliverable and produced nothing;
   unreadable sources (named, with the section they starve — "unread" is
   never reported as "clear"); backup or watch anomalies; past-due shared
   tasks; detector silence (a watch with no run record 48 hours past its
   cadence).
1. **Watches.** Anything the standing watches flagged; silence from a
   conditional watch is normal and is not reported.
2. **Decisions.** The queue: new and resurfacing items printed in full, the
   rest counted. The user clears by number.
3. **Today.** Calendar, arrivals, deadlines, the one or two things that
   will hurt if forgotten.
4. **Waiting replies.** Up to two inbox threads that need the user, with
   draft replies prepared (real drafts, never sent without per-message
   approval).
5. **House / systems.** One-line health summary from live reads.
6. **Reconciliation.** One or two memory records verified against their
   live sources, corrections made and attributed to the brief.
7. **Grants inventory (1st of the month).** Standing permission grants
   listed; the user's own grants distinguished from product defaults;
   unrecorded grants flagged. Plus: audit-due check (module 05) and a
   room sweep — workstreams that no longer meet the keep test (live
   machinery, an open next action, or a dated future gate) are proposed
   for close-out.

The brief may only say "the day is clear" when every source was actually
read.

## Inbox triage (between briefs)

A frequent lightweight scan that interrupts only for:

- a VIP sender (the user's named people — partner, counsel, key services);
- a direct question to the user;
- a deadline inside 24 hours;
- a security or account alert;
- a shared task tagged `urgent` (if household-hq is installed).

Everything else accrues to the next brief. The scan never sends mail and
never creates drafts. Delivery window: the user's waking hours only.

## Watches (the pattern)

A watch is a small scheduled check with three properties: it is **silent
when nothing changed**, it **always writes a run record** (so its own
silence is detectable), and it **flags failed runs**. Build watches for
recurring-charge changes, shared-list changes, backup health, and anything
else where "no news" is the common case and "something changed" is the
only thing worth a message. Host-level watches (backup jobs, disk
tripwires, dead-man's switches) follow the same pattern; the
maintainer's recipes live in docs/patterns/infra-patterns.md, a
reference document the wizard does not install.

## The money watch (optional component)

An optional watch over recurring charges, decided in the plan like
the triage scan — installed or not installed, recorded either way.

- **The baseline comes from data the user supplies**: statement or
  CSV exports the user downloads, or alert emails the user forwards.
  Never credentials, never a bank login, never a scraped banking
  session. If a source cannot be exported, the watch does not run
  on it (procedures §13).
- **Exclusion categories** are named with the user at install, and
  the installer *offers* the examples here — an exclusion the user
  never hears about is one they will never choose. Two different
  kinds share the one mechanism, and the baseline names which kind
  each exclusion is: *variability* exclusions (charges whose
  amounts move normally — variable utilities, groceries, fuel) and
  *sensitivity* exclusions (categories the user does not want
  watched or quoted at all — veterinary and medical care, in the
  maintainer's own install). An exclusion narrows what is flagged;
  it never makes a charge invisible. A first sighting in a
  variability-excluded category still flags NEW — the exclusion
  silences its later amount changes, not its existence. A first
  sighting in a sensitivity-excluded category flags as NEW with no
  merchant or amount printed: the user learns a charge exists in
  that category, and nothing more. Which category a charge belongs
  to comes only from the baseline's exclusion listing or the
  export's own category field — never from the agent's inference
  about a merchant. Exclusions change only on the user's explicit
  instruction, and the change is recorded in the baseline with its
  date.
- **"Recurring" is a baseline property, not a guess.** A charge is
  in scope when it is in the baseline. A charge sighted for the
  first time is flagged NEW — a candidate, nothing more. It enters
  the baseline only when the user confirms it, directly or by
  clearing the flag's decision-queue item. No number of sightings
  enrolls a charge on its own.
- **Amounts are positive dollars in the baseline**, whatever sign
  convention an export uses, and every comparison normalizes the
  same way first. A baseline that copies an export's negative
  signs flags a phantom change on every line the day the source
  changes convention.
- **It flags three things only**: a first sighting (NEW), a changed
  amount on a baseline charge, a duplicate. Everything else is
  silence, and every run writes a run record — the detector-silence
  rule applies to this watch like any other (no run record 48 hours
  past cadence means the watch is the failure).
- **It never acts.** The watch does not cancel, dispute, or contact
  anyone. A flag that warrants action becomes a decision-queue
  item; cancelling or disputing then needs a ticket, like any
  irreversible action.
- **Silence never settles a money-watch flag.** A decision-queue
  item from this watch never carries an accepting default: its
  only printed default is no action — the charge stays flagged and
  the baseline stays unchanged. Procedures §3 lets silence consent
  to a printed low-stakes default, and enrolling or repricing a
  charge in the baseline is exactly the quiet change that consent
  must not reach here. A money-watch item is resolved by the
  user's word, or it is not resolved.
- **A run never edits the baseline.** When a flag is raised — a
  price change, a confirmed new charge, a refunded duplicate — the
  baseline keeps reading the old state until the user resolves the
  flag's decision-queue item (by their word — never by silence;
  see above). On resolution, the agent updates the affected line
  and records the decision and its date on the line itself. Until
  then, the same change flags again on the next run that brings
  new data — that repetition is the mechanism working, not spam:
  the flag is unresolved.
- **Cadence is weekly; data may not be.** A run with no new export
  since the last run records "no new data" in the run record and
  stays silent — it does not re-compare the old export. Flags are
  computed only on new data. The run record is written either way.
- **"New data" is judged by transaction date, not by file.** An
  export whose period overlaps the last run's re-delivers old
  rows. A row dated inside the period the last run already covered
  that matches a covered row on date + merchant + amount is
  neither new nor a duplicate — it is the overlap, and it is
  ignored. Only transactions dated after the last run's covered
  period are new data, whatever file they arrived in.
- **A cancelled charge retires; it is not deleted.** When the user
  confirms a baseline charge is cancelled, its line moves to a
  Retired section of the baseline file, carrying the cancellation
  date and the number of the queue item that resolved it. A
  retired line no longer flags; if that merchant charges again,
  the charge is a first sighting (NEW), like any other.
- **The baseline is a financial record** (procedures §13 — the
  rule lives there; this is its money-watch application). Like
  every §13 holding it carries a `(review-by: ...)` date: the
  baseline template has the field, and §13 names where the date
  is ledgered so the brief surfaces it. The exports it was built
  from are holdings too: they live in the exports folder
  (Install step 5), and the plan records that folder with its own
  review-by date.

## Install

1. Adapt `brief.template.md` into the brief job's instructions; set the
   time (user's morning, their timezone) and delivery (main chat).
2. Create the VIP list and interrupt rules with the user. "None named yet" is a legitimate list — an empty interrupt lane is a state, not a gap.
3. Confirm module 00's decision queue exists in its canonical shape — the brief is its delivery vehicle. There is nothing to seed: the queue starts empty and its first real item is #1.
4. Optional: the triage scan job, 30-minute cadence, same interrupt rules.
5. Optional: the money watch — weekly cadence. Build the baseline
   with the user from their exports into
   `finance/money-watch-baseline.md`, from
   `money-watch-baseline.template.md`: every line carries its
   source pointer (export file, and date or line in it), and the
   exclusion categories — each marked variability or sensitivity —
   are named in the baseline file itself. Create the run-record
   file `finance/money-watch-runs.md` from
   `money-watch-runs.template.md` and the job file
   `jobs/money-watch.md` from `money-watch-job.template.md`, and
   record the job in `JOBS.md`. Statement exports live in
   `finance/exports/` — the folder the job file reads as "the
   newest user-supplied export"; the plan records the folder as a
   §13 holding with a review-by date. Record the baseline and
   run-record files in the plan's installed-file baseline as
   `accumulating`: resolutions rewrite baseline lines and runs
   append records by design, and hashing either would make
   ordinary use read as drift. (The plan may choose other paths;
   it records them, and the job file names them.) The decision
   (installed / not installed) goes in the plan either way.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
