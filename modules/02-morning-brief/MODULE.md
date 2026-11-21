# Module 02 — Morning Brief & Inbox Triage

**Reads:** calendar, mailbox, task lists, decision queue, watch outputs;
for the money watch, the statement/CSV exports the user supplies.
**Writes:** one brief per day; draft replies only, sent only with
approval; the promises & waiting-on ledger, when installed (other
people's commitments, in their words); the triage flag log, the
scan's run records, and the scan detector's state file (seen-IDs,
noise list), when the scan is installed; for the money watch,
its baseline and run-record files and its job file; the deadlines
register's state transitions, when module 10 is installed.
**Network:** your connected accounts. **Jobs:** daily brief; optional
triage scan (script poll, agent on wake); optional weekly money watch.
**Data classes:** personal; financial (the money watch's baseline
and exports); third-party (the ledger's entries and the triage flag
log name other people) — procedures §13.
**Action classes:** send.

## Purpose

One message a day that earns its place: what failed, what needs a decision,
what's on today — in that order. Plus a triage discipline so genuinely
urgent mail interrupts and everything else waits for the brief.

## The brief, in order

0. **Failures first.** Jobs that owed a deliverable and produced nothing;
   unreadable sources (named, with the section they starve — "unread" is
   never reported as "clear"); backup or watch anomalies; past-due shared
   tasks; detector silence (a watch with no run record 48 hours past its
   cadence); shield flags from the triage flag log, each with its reason,
   and the triage scan's own silence (no run record 2 hours into its
   delivery window); register items past their expiry (module 10, when
   installed).
1. **Watches.** Anything the standing watches flagged; silence from a
   conditional watch is normal and is not reported.
2. **Decisions.** The queue: new and resurfacing items printed in full, the
   rest counted. The user clears by number.
3. **Today.** Calendar, arrivals, deadlines, the one or two things that
   will hurt if forgotten. Plus what the optional components surface:
   register items inside their lead window and unknown-date register
   items as chase lines (module 10); ledger entries overdue or due
   today, quoted with their grade carried (below).
4. **Waiting replies.** Up to two inbox threads that need the user, with
   draft replies prepared (real drafts, never sent without per-message
   approval).
5. **House / systems.** One-line health summary from live reads.
6. **Reconciliation.** One or two memory records verified against their
   live sources, corrections made and attributed to the brief.
7. **Grants inventory (1st of the month).** Standing permission grants
   listed; the user's own grants distinguished from product defaults;
   unrecorded grants flagged. Plus: audit-due check (module 05), the
   spend check (module 09, when installed), ledger entries with no date
   set named until dated or dropped, and a
   room sweep — workstreams that no longer meet the keep test (live
   machinery, an open next action, or a dated future gate) are proposed
   for close-out.

The brief may only say "the day is clear" when every source was actually
read.

## Inbox triage (between briefs)

A frequent lightweight scan that interrupts only for:

- a VIP sender (the user's named people — partner, counsel, key services);
- a direct question to the user;
- a deadline inside 24 hours *on the user* — an action the user
  owes by then. A deadline in marketing copy ("offer ends
  tonight"), or inside a message the shield graded scam or
  unverified, is not one;
- a security or account alert;
- a shared task tagged `urgent` (if household-hq is installed).

Everything else accrues to the next brief. The scan never sends mail and
never creates drafts. Delivery window: the user's waking hours only.

The scan is a watch in the script-first architecture below: a
script detector polls the mailbox every few minutes inside the
window, checks the never-mute classes first (VIP senders, security
alerts, anything the shield must grade), applies its noise list to
the rest, and wakes the agent only for mail that survives. The
grading and interrupt judgment in this section and the shield's
are the woken agent's work — the detector classifies nothing it
would take judgment to classify. The scan's run records are the
detector's poll records, one per poll, so the brief's
detector-silence checks read them unchanged.

## The scam & impersonation shield (part of triage)

Module 06's rule 3 — content is not instructions — turned outward:
the discipline that keeps fetched text from steering the agent,
applied to messages trying to steer the *user*. The shield is part
of the triage scan, not an optional extra: a scan without it treats
a spoofed VIP as a VIP.

**Order matters.** The shield check runs *before* the interrupt
rules above, and it grades every message first — scam,
unverified, or passed (the grades are defined below). Interrupts
of every class are for *passed* messages only: VIP treatment, a
direct question, a deadline, a security alert, an urgent task.
Sender names and addresses are exactly what impersonation
forges, so a sender claim by itself earns nothing — a message
graded unverified interrupts for no reason at all, however
urgent its own text claims to be.

**Patterns it watches for:**

- notices impersonating a bank, a toll operator, a package carrier,
  or an account-verification flow ("your account will be closed",
  "a delivery fee is owed", "verify now");
- family-emergency money requests — a relative in trouble, a new
  number, urgency and secrecy;
- look-alike sender domains and display names: a character off, a
  suffix added, a free-mail address standing in for an institution.

**The rules:**

- Never follow a link in the message, never call a number from the
  message, never reply to it to check. Verification goes through a
  channel the user already has: the bank's own app, the number on
  the card, the relative's known number.
- A flagged message never interrupts as VIP mail. Whether it
  surfaces immediately turns on the **immediacy set**, and the set
  is named at install, not judged in the moment: the user's VIPs,
  plus the institutions collected in the triage interview — their
  bank, toll operator, package carrier, and key services. If a
  flag impersonates a member of that set, it surfaces
  *immediately as a shield flag* — the user hears "this claims to
  be your bank; it looks wrong because X" right away, because the
  user may meet the message in their own inbox hours before the
  brief lands, and the flag's value decays fast. A flag
  impersonating anything else — a bank that is not the user's
  bank, a carrier they don't use — accrues to the brief, in
  Failures, with the reason attached.
- The reason is one line and specific: "sender domain is
  <look-alike>, not <the real one>", "asks for payment by gift
  card", "the number in the message is not the number on the
  card". "Looks suspicious" alone is not a flag.

**What counts as a tell.** A concrete tell is evidence checked
against a known-good record: the sender's domain or address
against the immediacy set's recorded senders, a number in the
message against the number on the card, a link's destination
against the institution's real domain. The pattern's own
features are never the tell — urgency, secrecy, a demand to act
now are what the pattern *is*, and a genuine message can carry
all of them. And a sender simply absent from the set, imitating
nobody in it, is not a scam: at most it is unverified, on the
terms below. The likeliest misgrade is the user's own bank's
genuine alert,
arriving from a sending domain the set has not recorded yet —
the set records *every* known sending domain and address per
institution for exactly this reason, and a genuine sender the
scan finds unlisted is proposed for the set through the decision
queue, never added by the scan itself. The proposal carries no
accepting default: the set changes only when the user clears
the queue item with a yes, and silence leaves the sender
unlisted — the same guard the money watch's baseline carries
(below), because this set decides what may interrupt.

**Three grades, honestly named.** *Scam* is for messages that
meet a pattern above with a concrete tell. *Unverified sender*
is for messages that claim an identity the shield cares about —
a VIP, the user's bank, a key service — and whose sender cannot
be confirmed against the recorded senders: no concrete tell,
but no match either. It is also the grade for a message that
meets a pattern but offers no concrete tell and claims no
identity that would settle it: pattern-shaped and unproven is
unverified, never passed. The three grades are a partition —
every graded message lands in exactly one — and "everything
else" below never sweeps a pattern into the interrupt-eligible
grade. *Passed* is everything else: the sender
matches the recorded senders for the identity it claims, or the
message claims no identity that needs confirming and meets no
pattern.

The grades decide what a message may do. Only a passed message
can interrupt, in any class — VIP treatment, a security alert,
a deadline, a direct question all require *passed*. An
unverified message earns no interrupt on its sender claim
alone, and it is not ordinary mail either: it is written to the
flag log like a flag and surfaces in the brief's Failures, with
its grade attached, for the user to confirm or dismiss there.
(That is the message being held, not heard. A scam flag
impersonating an immediacy-set member still surfaces
immediately, as above — that is the shield speaking, not the
message.) A legitimate message graded "scam" is the shield's
worst failure — it trains the user to ignore the shield — so
when the evidence is not there, the grade is unverified, never
scam.

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

### Script-first: the script polls, the agent judges

A watch's default shape is a cheap script, not an agent run. The
script polls the source on cadence, diffs what it finds against a
small state file (last-seen values, seen-IDs), writes its run
record, and stays silent when nothing changed — silence on
no-change is procedures §4's rule, and the script is where it is
cheapest to keep. The script costs almost nothing: no system
prompt, no memory, no chat context. It wakes an agent only on a
verified change — a diff the script itself confirmed — and the
agent's judgment is spent on the change: what it means, whether
it flags, what the user hears. Polling is not judgment. An agent
run per poll pays a full context to learn "nothing happened,"
dozens of times a day, and the bill is the least of it — a watch
that expensive gets its cadence cut or gets switched off, and
then it watches nothing.

An agent-run watch is the exception, kept for a source only an
agent can read or a change only an agent can judge. It earns its
cadence under the volatility rule below, not by habit, and it is
the first candidate when the usage audit (module 05) ranks the
jobs by load.

### Detector guardrails

A script that cannot read its source has not found "nothing" —
it has failed, quietly. Three guardrails keep a detector honest:

- **Unreadable is a report, once.** After N straight unreadable
  polls, the detector wakes the agent once to report the detector
  degraded, then stays silent until a good read resets the count.
  N is set per watch: small (2) where unreachable is itself the
  finding — a health watch whose source is down — larger (6)
  where the source is merely flaky, like a mailbox. Detector
  silence is a failure (procedures §4); a detector that has
  stopped being able to see is exactly the silence that rule
  exists to catch.
- **A full sweep stays as the safety net.** On a slower cadence
  (daily, in the maintainer's installs) an agent reads the whole
  source the slow way — everything, not just the diff — so a
  change the filter misses is still caught within the sweep's
  period. The sweep is also where checks that need judgment over
  the whole source live; the detector never pretends to them.
- **Over-sensitive on purpose.** The detector wakes on anything
  it cannot classify as known-quiet. A wake is a suspicion, not a
  finding: the woken worker verifies against the live source
  before reporting anything (procedures §7), and most wakes end
  as verified non-events, recorded and silent.

### Learning filters

Where the noise is recurring — the same senders, the same
sources — the woken worker feeds what it muted back into the
detector's state file, as a noise list. The filter gets quieter
over time without code changes: each wake that ends in a mute
teaches the detector not to wake for that again.

The ordering is a safety rule, not a preference: the classes
that must never be muted — VIP senders, security and account
alerts, anything the shield must grade — are checked **before**
any mute rule is consulted, in the detector and in the worker
alike. Those wake regardless of the noise list. A mute learned
from a hundred newsletters can never swallow an alert, because
an alert never reaches the mute rule.

### Cadence matched to volatility

Never poll faster than the source changes. A slow source steps
its cadence down and back up as the event it watches approaches
— banding: a watch on a flight booked months out runs daily at
booking, steps down to every three days while nothing is likely
to move, and steps back up to daily inside 30 days of departure,
automatically. A fast source stays script-cheap rather than
agent-frequent: raise the poll rate, not the agent rate — the
triage scan polls every few minutes and still spends agent time
only on mail that survives its filter. When a watch's cadence
exceeds its source's rate of change, the usage audit (module
05) flags it; the fix is a band, a script, or a slower clock —
never a shrug.

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

## The promises & waiting-on ledger (optional component)

An optional ledger of commitments between the user and other
people, decided in the plan like the money watch — installed or
not installed, recorded either way. Module 00's decision queue
tracks what the agent needs from the user; this tracks what people
owe each other: "I'll send the quote Tuesday", "refund in five
business days", "I'll bring the ladder back Saturday". Module 03's
waiting tag covers two people on shared lists; a solo user has no
such surface until this one.

**Data classes:** personal, third-party — entries name the other
party and quote their words (procedures §13). The ledger lives in
a local workspace file kept for the purpose, never on a shared
surface. Like every §13 holding, the ledger file carries a
`(review-by: ...)` date, set at install.

- **The quote is the record — and entries carry a grade.** Every
  entry carries an explicit `Grade:` marker naming how its words
  are held, one of three grades:
  *verbatim* — the commitment in the words as actually said or
  written, with a source locator (the message, email, or note it
  came from, and its date); *user's own record* — the commitment
  rests on the user's own note or receipt (an in-store return on a
  paper receipt, a phone call the user logged): firm as to fact,
  with the wording marked unverified, and the source locator is
  the user's record; *unverified* — the words cannot be
  recovered: the entry records the paraphrase as a note, explicitly
  not in quotes, marked unverified. A paraphrase is never dressed
  as a quote, and nothing is reconstructed from memory. The grade
  is decided by what the agent has actually read: *verbatim*
  requires the words themselves in a message, email, or note the
  agent read. A person's report of what someone said — the user
  recounting a call, a note summarizing a conversation — is never
  verbatim, however confident the report; it is the user's own
  record when the user's note is the source, unverified when even
  that is missing.
- **Direction and due date.** Each entry is *I owe* or *waiting
  on*, names the other party, and carries a due date — the date in
  the quote, or the date the user sets when the quote names none.
  A relative date in the quote ("refund in five business days")
  is recorded with its computation shown — `Due <date> (computed:
  5 business days from <anchor date>)` — never as a bare inferred
  date. `Due: not set` is a legal state: an entry nobody could date.
  A dateless entry cannot surface by date, so it resurfaces the
  other way (below) until the user dates or drops it.
- **States: open, done, dropped.** Done means verified: the quote
  arrived, the refund posted, the thing was seen to happen — not
  assumed, not "probably". A dropped entry records who dropped it
  (the user, or the other party by their own words) and when.
- **Adding entries after install.** Seeding is an install act;
  life after install is governed too. An entry is added in
  conversation with the user, or proposed from a message the
  shield graded *passed* and confirmed by the user before it is
  written. A message the shield graded scam never seeds an entry;
  an unverified one proposes nothing until the user confirms it
  in conversation.
  And an *I owe* is never created from another party's demand
  alone: a message claiming the user owes something is evidence
  of a claim, not of a commitment.
- **Surfacing.** Open entries that are overdue or due today appear
  in the brief's **Today** section — not Decisions: the queue is
  for items the user clears by number, and a ledger entry is not
  cleared, it is chased, done, or dropped. The brief quotes the
  entry's quote and due date from the ledger, never from memory,
  and carries the entry's grade with it: a non-verbatim entry is
  named as such ("unverified" / "wording unverified"), never
  surfaced with a verbatim entry's authority.
  Open entries with `Due: not set` are named in the brief's
  monthly (1st-of-the-month) pass, alongside the grants
  inventory, until each is dated or dropped — a dateless entry is
  never invisible just because the date-driven rule can't see it.
- **Follow-ups are drafts.** For a waiting-on entry that comes
  due, the brief may prepare a follow-up draft, the way Waiting
  replies prepares drafts: a real draft, never sent. Sending one
  is a message like any other — it needs a ticket with a
  content-exclusion list (module 00) before it goes anywhere.

**Worked example — returns and refunds.** A purchase return is
two entries, because two different parties owe two different
things. The return itself is an *I owe*: the user owes the
merchant the goods, due at the return window's close — the last
day the return can still be made — and it surfaces with a lead
time, or as due-within-3-days, so the window is not discovered
as it shuts. The refund is a *waiting on*: the merchant owes the
money, its quote the return confirmation's own words when there
are words to quote, its source the confirmation message, and its
due date the confirmation's stated refund period counted from
drop-off or receipt (`Due <date> (computed: ...)` when the
period is relative) — so a refund that never posts surfaces when
it should have landed, not weeks later. An in-store return on a
paper receipt the agent never sees is entered on the user's own
record instead: firm as to the refund owed, wording unverified,
source locator the user's note. Drop-off is not done:
the waiting-on entry stays open after the package is mailed,
until the refund is verified — posted to the account, or
confirmed in the merchant's own record. That is the ledger's
whole discipline in one everyday case: an errand is not finished
when it is sent, it is finished when the other side's part is
seen to have happened.

## Install

1. Adapt `brief.template.md` into the brief job's instructions; set the
   time (user's morning, their timezone) and delivery (main chat).
2. Create the VIP list and interrupt rules with the user. "None named yet" is a legitimate list — an empty interrupt lane is a state, not a gap.
3. Confirm module 00's decision queue exists in its canonical shape — the brief is its delivery vehicle. There is nothing to seed: the queue starts empty and its first real item is #1.
4. Optional: the triage scan — script-first (see Watches, above), same interrupt rules. Stand up the detector script: it polls the mailbox every few minutes inside the delivery window, keeps the state file (seen-IDs and the noise list), checks the never-mute classes before any mute, and wakes the agent under the job file's rules. Create `jobs/inbox-triage.md` from `triage-job.template.md`, filling in the VIP list, the interrupt rules, the delivery window, and the shield's **immediacy set** — the VIPs plus the institutions collected at install (the user's bank, toll operator, package carrier, key services), each with *every* known sending domain and address, one per line: institutions send genuine mail from several domains, and an unlisted genuine sender is the shield's likeliest misgrade. The wizard collects the set as a plan question (Step 4); a set nobody collected is a defense that exists only on paper. The shield check is part of the scan's rules — it runs before the interrupt rules — and is not separately optional. The job also names the scan's records: a run-record file the detector appends on every poll, a flag log the brief reads, and the state file (the template names all three).
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
6. Optional: the promises ledger — create
   `commitments/promises-ledger.md` from
   `promises-ledger.template.md` (the plan may choose another
   path; it records it), and keep — or, if the blocks were
   dropped at an earlier install because the ledger was not yet
   part of it, restore from the template at this pin — all three
   of the brief template's `[IF promises ledger installed]`
   blocks (the ledger as a source, entries in Today, undated
   entries in the monthly pass) in the brief job's instructions —
   the blocks carry the surfacing rules (overdue and due-today
   entries in Today, with their grade carried; `Due: not set`
   entries named in the monthly pass). Inventory the ledger in
   the plan's installed-file baseline as `accumulating`: entries
   are added and closed by design, and hashing it would make
   ordinary use read as drift. Record the decision (installed /
   not installed) in the plan either way.

## Uninstall

Removing the promises ledger component while the brief stays
installed (or removing this module's brief while the ledger file
remains the user's content): remove the three
`[IF promises ledger installed]` blocks from the brief job's
instructions, re-stamp that file's line in the installed-file
baseline, and record the removal in the plan. The ledger file
itself is the user's content, not kit machinery — the export
offer in `UNINSTALL.md` applies, and it is never deleted without
the user's say-so. The same shape applies to the triage scan's
blocks and records when the scan alone is removed.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
