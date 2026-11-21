# Module 00 — Core Procedures

**Reads:** your existing agent instructions and workspace layout.
**Writes:** an operating-procedures file, a decision queue, SCOPE notes.
**Network:** none. **Jobs:** none.

## Purpose

Give the agent a constitution: what it may do on its own, what needs a
ticket, how decisions are batched, how it knows a fact, what it does when
reality doesn't match the record, and how workstreams are opened and
closed. Every other module assumes this one.

## Concepts

- **One home per topic.** Each workstream lives in exactly one place (a
  chat, a workspace folder) with a `SCOPE.md`: what it owns, what it must
  never do, what done looks like, its source of truth, and a Closed list of
  things already tried and rejected — so dead ends stay dead.
- **The ticket rule.** Reversible work inside scope is pre-authorized:
  finish it, don't re-ask. Irreversible or externally visible actions —
  sends, purchases, bookings, filings, cancellations, deletions,
  submissions — need a *ticket*: the exact action, the exact total, the
  exact fallback, and a content-exclusion list for messages, approved by the
  user in the topic's home. A ticket authorizes exactly one execution and
  is void if any detail changes.
- **The decision queue.** Non-urgent decisions go into a numbered queue
  file. The user clears them by number in one reply ("3: yes, 7: park").
  An item may print a low-stakes default; silence is consent only to that
  printed default, never to an irreversible action. Time-sensitive,
  security, money-deadline, and key-person items bypass the queue and
  interrupt.
- **Ground truth.** Every fact has an address. Claims come from the live
  source or the original record; summaries are locators only. Anything the
  agent will act on is re-read at the original in the same session, or it
  stays marked unverified. In document work: quote ambiguous passages
  verbatim, and mark unread sections "not verified", never summarized.
- **Abort on mismatch.** Unexpected state from a live system — a wrong
  account, an unfamiliar screen, a balance that doesn't match — means stop
  and report, not improvisation. Before acting inside a signed-in system,
  canary-check whose session it is.
- **Room close-out.** When a workstream ends, audit its outstanding work,
  complete it or re-home it, repoint or retire its machinery, sync drifted
  copies, report once, then archive. Nothing open may live only in a
  transcript.
- **Done means verified.** Completion is checked against live state or the
  original record, never accepted from a worker's report alone.

## Install

1. Copy `templates/OPERATING_PROCEDURES.template.md` to the workspace as
   `OPERATING_PROCEDURES.md`; fill the Local configuration placeholders
   with the user (names, timezone, brief time, VIP list).
2. Apply the interview's autonomy answer (wizard Q2) to §2: (b) installs
   as written; (a) adds the user-named classes to the ticket list; (c)
   replaces pre-approval with a same-day reporting duty for the named
   classes, recorded in the plan in the user's words.
3. Create the decision queue from `templates/decision-queue.template.md`
   (its example item is an HTML comment — the first real item is #1).
4. For each workstream named in the interview (wizard Q7), create a
   `SCOPE.md` from `templates/SCOPE.template.md`, in the workstream's
   home folder — create `workspace/<workstream-slug>/` when it has
   none; the plan names each home. The SCOPE's fields are drafted with
   the user and approved as part of the plan, not invented after it.
5. Add a pointer line to the agent's main instruction file (wizard Q7;
   create `INSTRUCTIONS.md` if none exists): "Operating procedures live
   in OPERATING_PROCEDURES.md and govern daily work."
6. Create `JOBS.md` at the workspace root from `templates/JOBS.template.md` — header and entry format, no jobs yet. The format is canonical: module 01's linter and module 08's curator both parse this file, and the brief's detector-silence check reads cadences from it. Do not improvise a different shape.
   Every later module records its scheduled jobs there; the morning
   brief and the memory linter read it. (This module's VERIFY checks
   for it — a step that creates what the check requires.)

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
