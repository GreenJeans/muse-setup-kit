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
- [IF deadlines register installed] Deadlines register: <path> —
  items past expiry go to Failures (step 0); items inside their
  lead window (today >= expiry − lead time) go to Today (step 3);
  items whose date is still unknown go to Today as a one-line
  chase item
- [IF promises ledger installed] Promises ledger: <path> — open
  entries overdue or due today go to Today (step 3), quoted from
  the ledger; open entries with no date set are named in the
  monthly pass (step 7)
- [IF memory-architecture installed] Memory: yesterday's daily log; the reconciliation rotation file

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
omitted — never reported as clear.

## Steps

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
   stays here until it is renewed or dropped.
1. **Watch findings.** Anything flagged since the last brief.
2. **Decision queue.** Print new, resurfacing, and firing-default items in
   full; count the rest. Never invent a default for an item; defaults are
   set only by the user or the agent in session.
3. **Today.** Calendar events, deadlines, arrivals. Flag anything the user
   is likely to have forgotten that matters today.
   [IF deadlines register installed] Register items inside their
   lead window, with the expiry quoted from the register; register
   items whose date is still unknown, as a one-line chase item
   ("expiry unknown — the date needs reading") in every brief
   until the item is dated or dropped.
   [IF promises ledger installed] Ledger entries overdue or due
   today, quoted from the ledger with their due dates — chased,
   not cleared by number.
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
