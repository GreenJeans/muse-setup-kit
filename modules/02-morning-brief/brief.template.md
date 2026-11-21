# Morning Brief — Job Instructions (template)

Run once daily at <HH:MM> <TIMEZONE>. Deliver to the main chat. Keep it
tight: the user reads this in two minutes. Failures first, always.

## Sources to read (name any you cannot read in Failures)

- Decision queue: <path>
- [IF calendar connected] Calendar: today and tomorrow
- [IF mailbox connected] Mailbox: since the last brief
- [IF a task app is connected] Task lists: <shared and personal lists>
- [IF household-hq installed] Agents' Notebook: entries in the *other*
  agent's "From ..." section since the last brief — surface them in a
  short Notebook block, attributed and dated
- [IF ai-exchange installed] AI Exchange: for each open queue row,
  check the owner's outbox for a matching output; flag a row with no
  output 72 hours after assignment (once, and again when the output
  lands)
- [IF watches exist] Watches: <each watch's state file / last run record>
- [IF triage scan installed] Triage flag log: <path> — shield
  flags logged since the last brief go to Failures (step 0), each
  with its one-line reason; the scan's run records ride the same
  file's sibling (step 0 reads the gaps, too)
- [IF deadlines register installed] Deadlines register: <path> —
  items past expiry go to Failures (step 0); items inside their
  lead window (today >= expiry − lead time) and not yet expired
  go to Today (step 3);
  items whose date is still unknown go to Today as a one-line
  chase item
- [IF promises ledger installed] Promises ledger: <path> — open
  entries overdue or due today go to Today (step 3), quoted from
  the ledger; open entries with no date set are named in the
  monthly pass (step 7)
- [IF memory-architecture installed] Memory: yesterday's daily log; the reconciliation rotation file
<!-- ext:brief-sources — extension anchor (registered in module
00's registry). A module whose surfacing rides this brief — a
field module, typically — registers its source lines between
these markers, and nowhere else in this file. Each registration
is a delimited block keyed by the module's qualified id:

  <!-- ext:brief-sources:block <library>/<module> -->
  - [IF <library>/<module> installed] <source lines>
  <!-- /ext:brief-sources:block <library>/<module> -->

and its uninstall removes exactly its delimited block. The
anchor comments are structural: they survive rendering and are
never dropped as template comments. -->
<!-- /ext:brief-sources -->

Blocks marked [IF ...] are conditional. The test is whether the
source exists in the user's setup, not whether it is connected
today: keep a block — marker and all — when the source exists or
the module is installed (a calendar the user has but has not
connected yet keeps its block; until it is connected, the brief
reports it unread, never clear). Drop a block when the source
does not exist for this install at all — the user has no
calendar, no task app, no second agent — and record the drops in
the plan, so the installed instructions and the plan agree about
what was left out. A section whose sources don't exist is
omitted — never reported as clear. The `ext:brief-sources`
anchor pair above is not a conditional block: it stays in every
rendering, empty until a module registers into it. The
`ext:brief-steps` anchor pair in Steps below is the same: it
stays in every rendering, and any re-render of this file carries
every registered block in both anchors across verbatim
(module 00's Registered blocks rule).

## Steps

<!-- ext:brief-steps — extension anchor (registered in module
00's registry). A module whose surfacing is an instruction to
the brief rather than a source to read — its items belong in a
named step, said in its block — registers a step block here, in
the same delimited form as ext:brief-sources:

  <!-- ext:brief-steps:block <library>/<module> -->
  - [IF <library>/<module> installed] <step text>
  <!-- /ext:brief-steps:block <library>/<module> -->

Registered blocks run where their text says, in registration
order. The anchor stays in every rendering. -->
<!-- /ext:brief-steps -->

0. **Failures.** (a) Jobs that owed output in the last 24h and produced
   none. (b) Sources above that could not be read — name them; do not
   report their sections as clear. (c) Watch anomalies and detector
   silence: any watch with no run record 48h past its cadence.
   (d) [IF shared lists exist] Past-due shared tasks (from the third
   consecutive flag, fold to a count). (e) [IF shared lists exist] Tasks
   tagged `urgent` — these also interrupt between briefs, like a triage
   item. (f) Deferred checks: SETUP-PLAN.md's verification ledger — any
   check due today or overdue is named here, with its owner. The
   ledger is also where review-by dates for local §13 holdings are
   recorded (procedures §13), so a holding past its review-by is
   named here like any other due check.
   (g) [IF deadlines register installed] Register items past their
   expiry — an expired document is a failure, not a deadline, and
   stays here until it is renewed or dropped. The transitions
   are this job's to write (module 10): mark each newly expired
   item's state expired in the register, with a dated note, and
   move an item whose register field reads "on expiry: lapse"
   to the register's History as lapsed once it has appeared
   here.
   (h) [IF triage scan installed] Shield flags from the triage flag
   log since the last brief, each with its one-line reason; and
   the scan's own liveness — no run record 2 hours into its
   delivery window is a failure of the scan, named here like any
   other dead detector.
1. **Watch findings.** Anything flagged since the last brief.
2. **Decision queue.** Print new, resurfacing, and firing-default items in
   full; count the rest. Never invent a default for an item; defaults are
   set only by the user or the agent in session.
3. **Today.** Calendar events, deadlines, arrivals. Flag anything the user
   is likely to have forgotten that matters today.
   [IF deadlines register installed] Register items inside their
   lead window and not yet expired, with the expiry quoted from
   the register (expired items are in Failures, step 0 — never
   here); register
   items whose date is still unknown, as a one-line chase item
   ("expiry unknown — the date needs reading") in every brief
   until the item is dated or dropped.
   [IF promises ledger installed] Ledger entries overdue or due
   today, quoted from the ledger with their due dates and their
   grade carried — a non-verbatim entry is named unverified, not
   quoted with a verbatim entry's authority — chased,
   not cleared by number. For a waiting-on entry that is due,
   prepare a follow-up draft where a channel exists: a real
   draft, never sent; sending one needs a ticket with a
   content-exclusion list (module 00).
4. **Waiting replies.** Up to two threads needing the user. Prepare draft
   replies as real drafts; never send. Drafts add no facts about money,
   health, legal matters, or other people that the thread doesn't contain.
5. **Systems.** One line per system from live reads (backups, storage,
   key services). Unknown is reported as unknown.
6. **Reconciliation.** [IF memory-architecture installed] Take the next one or two records from the rotation;
   verify against the live source; correct the compiled record in the same
   run and commit the correction attributed to the brief. Record any
   overflow (records due but not checked) in the rotation file and report
   the count in Failures.
7. **Monthly (1st only).** Standing-grants inventory; procedures-audit due
   check; room sweep — list workstreams failing the keep test (no live
   machinery, no open next action, no dated gate) as close-out candidates.
   [IF promises ledger installed] Ledger entries with no date set:
   name each one until it is dated or dropped.
   [IF cost-guardrails installed] Spend check: read usage for every
   bucket in the register against its cap (the user present for the
   usage read, per module 09); a bucket within 20% of its cap, or any
   unclassified surface in use, becomes a decision-queue item.

## Rules

- "The day is clear" is allowed only when every source was read.
- Numbers come from the sources read in this run, never from memory of
  previous briefs.
- If a step fails, the brief still ships, with the failure in section 0.
