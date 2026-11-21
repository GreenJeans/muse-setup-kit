# Module 00 — Core Procedures

**Reads:** your existing agent instructions and workspace layout.
**Writes:** an operating-procedures file, a decision queue, SCOPE notes,
a JOBS.md, a continuity handover, and a pointer line in the agent's
main instruction file.
**Network:** none. **Jobs:** none.

## Purpose

Give the agent a constitution: what it may do on its own, what needs a
ticket, how decisions are batched, how it knows a fact, what it does when
reality doesn't match the record, and how workstreams are opened and
closed. Every other module assumes this one.

## Concepts

Summaries, for orientation. The operative text of every rule below
is the operating-procedures template this module installs; where a
summary here and the template differ, the template governs, and the
summary has a bug.

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
- **Done means verified.** Completion is checked against live state or the
  original record, never accepted from a worker's report alone.
- **Abort on mismatch.** Unexpected state from a live system — a wrong
  account, an unfamiliar screen, a balance that doesn't match — means stop
  and report, not improvisation. Before acting inside a signed-in system,
  canary-check whose session it is.
- **Room close-out.** When a workstream ends, audit its outstanding work,
  complete it or re-home it, repoint or retire its machinery, sync drifted
  copies, report once, then archive. Nothing open may live only in a
  transcript.
- **Continuity.** The agent accumulates access and context quietly. A
  one-page handover — where things are, who to call, what to stop, how
  to pause the agent itself — is written with the user for the person
  who would pick things up if the user were unavailable, and carries a
  review-by date like any other time-bound claim.

## Where each rule lives (canonical text)

Each constitutional rule has exactly one operative statement — in
the procedures template, at the section named here. Other modules
apply the rules to their own subject (module 08's gate applies the
ticket rule; module 02's watches apply the silence rules) and point
back rather than restating. Edit a rule in its home section only;
if an application elsewhere seems to disagree, the home section
governs and the application has a bug.

| Rule | Operative text |
|---|---|
| Homes and scope | procedures §1 |
| Ticket rule; one execution per ticket; content-exclusion lists | procedures §2 |
| Decision queue; silence never consents to an irreversible action | procedures §3 |
| Silence rules; detector silence is a failure | procedures §4 |
| The brief; "done" requires a verified deliverable | procedures §5 |
| Memory discipline (application: module 01) | procedures §6 |
| Ground truth; summaries are locators | procedures §7 |
| Abort on mismatch; session canary | procedures §8 |
| Room close-out | procedures §9 |
| Standing rules (grants, retitle-before-share, install-page instructions) | procedures §10 |
| Audit cadence | procedures §11 |
| Verify-before-install (application: module 06) | procedures §10 |
| Billing buckets; declare before heavy work (application: module 09) | procedures §12 |
| Sensitive records — where financial, health, and third-party data may live; document numbers never recorded (applications: modules 02, 03, 04, 06, 10, and this module's continuity handover) | procedures §13 |

## Extension points (anchors)

Core prose files that other modules amend carry **named anchors**:
HTML comments of the form `<!-- ext:<name> -->`. The rules:

- A module may amend a core file **only at a declared anchor** — it
  never appends wherever it likes, and it never renumbers sections.
- Completing a section's own canonical text in its home section is
  not an amendment and needs no anchor — module 06 confirming that
  §10 is present in full, for instance. The canonical-location rule
  above governs those edits. Anchors govern *inserted blocks*:
  content a module adds to a file another module owns.
- Each anchor has exactly **one owner** at a time. The owner's block
  runs from the anchor comment to the matching
  `<!-- /ext:<name> -->` marker. The install plan (SETUP-PLAN.md)
  records which module owns each anchor it uses.
- One anchor is a *registration* anchor: `ext:brief-sources` in
  the brief job file. Module 02 owns the anchor itself; each
  module that registers a block inside it owns that block,
  recorded in the plan like any other ownership. Registration
  there is the only way contributed surfacing enters the brief —
  a module never free-edits the brief job file.
- Uninstalling the owner removes its block, and nothing else.
- A new anchor is added by editing this registry and the target file
  in the same change. An anchor with no registry entry is a defect;
  so is a registry entry with no anchor.
- Anchor comments are never deleted as "template comments" — they
  are the mechanism, not commentary. The procedures template's
  header says so at its head.

Registry, as shipped:

| Anchor | File | Purpose | Owner |
|---|---|---|---|
| `ext:billing-buckets` | OPERATING_PROCEDURES.md (from this module's procedures template) | Module 09 inserts its bucket register and declare-before-heavy-work rule as §12 | module 09 (cost-guardrails), when installed |
| `ext:brief-sources` | The brief job file (from module 02's brief template) | Modules whose surfacing rides the brief register their source lines here, each in its own delimited block keyed by its qualified module id (see Registered blocks, below) | module 02 (host); each registered block is owned by the module that registered it |
| `ext:queue-header` | The decision queue (from this module's queue template) | Module 08 adds its queue item-type definitions (`[type: skill-write]`, `[type: skill-curator]`) between the markers | module 08 (skill-lifecycle), when installed |
| `ext:instruction-pointer` | The agent's main instruction file (the anchor pair is planted by this module's Install step 5 when the file is first created or amended) | Pointer lines other modules add: module 08's skill-lifecycle pointer, the wizard's session-start line. Each line inside is owned by the module that added it; uninstalling that module removes its line | module 00 (the anchor); lines as noted in Purpose |

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
   in OPERATING_PROCEDURES.md and govern daily work." Plant the
   `ext:instruction-pointer` anchor pair (see the registry above)
   around the line: later modules add their own pointer lines inside
   the same markers, each line owned by the module that added it.
6. Create `JOBS.md` at the workspace root from `templates/JOBS.template.md` — header and entry format, no jobs yet. The format is canonical: module 01's linter and module 08's curator both parse this file, and the brief's detector-silence check reads cadences from it. Do not improvise a different shape.
   Every later module records its scheduled jobs there; the morning
   brief and the memory linter read it. (This module's VERIFY checks
   for it — a step that creates what the check requires.)
7. Create the continuity handover from
   `templates/continuity-handover.template.md`, filled with the user:
   where things live, who to call, what to stop, how to pause the
   agent. It carries a review-by date. Its default home is
   `continuity-handover.md` at the workspace root — a file whose
   purpose is to be found later, by a stressed human or a fresh
   agent, gets a findable name. The user may name another home; the
   plan records the path and who the handover is for either way. A
   handover filled in part is a normal state, not a failure: the
   load-bearing fields — who picks things up if the user is
   unavailable, and how to pause the agent — are filled at install;
   the rest (account details, further contacts, the open-threads
   list) may be marked not-yet-supplied in the file, with the
   completion ledgered as a deferred check. An unfilled handover is
   ledgered as a deferred check, never silently skipped. Record
   the handover in the plan's installed-file baseline as
   `accumulating` — it is filled in and revised by design, and
   hashing it would make ordinary updates read as drift.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
