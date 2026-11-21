# Module 02 — Morning Brief & Inbox Triage

**Reads:** calendar, mailbox, task lists, decision queue, watch outputs.
**Writes:** one brief per day; draft replies only, sent only with approval.
**Network:** your connected accounts. **Jobs:** daily brief; optional
30-minute triage scan.

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
- **Exclusion categories** are named with the user at install —
  charges whose variation is normal (variable utilities, groceries,
  fuel) — and recorded in the watch's instructions. Excluded
  categories are never flagged.
- **It flags three things only**: a new recurring charge, a changed
  amount on a known charge, a duplicate. Everything else is
  silence, and every run writes a run record — the detector-silence
  rule applies to this watch like any other (no run record 48 hours
  past cadence means the watch is the failure).
- **It never acts.** The watch does not cancel, dispute, or contact
  anyone. A flag that warrants action becomes a decision-queue
  item; cancelling or disputing then needs a ticket, like any
  irreversible action.
- **The baseline is a financial record** (procedures §13): it lives
  in a local workspace file kept for the purpose, never on a shared
  surface, and figures from it are quoted from the file, not from
  memory.

## Install

1. Adapt `brief.template.md` into the brief job's instructions; set the
   time (user's morning, their timezone) and delivery (main chat).
2. Create the VIP list and interrupt rules with the user. "None named yet" is a legitimate list — an empty interrupt lane is a state, not a gap.
3. Confirm module 00's decision queue exists in its canonical shape — the brief is its delivery vehicle. There is nothing to seed: the queue starts empty and its first real item is #1.
4. Optional: the triage scan job, 30-minute cadence, same interrupt rules.
5. Optional: the money watch — weekly cadence; build the baseline
   with the user from their exports, record the exclusion
   categories in the watch's instructions, and record the job in
   `JOBS.md`. The decision (installed / not installed) goes in the
   plan either way.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
