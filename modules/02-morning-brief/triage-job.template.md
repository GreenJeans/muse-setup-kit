# Job — Inbox triage scan

<!-- Template from the Muse Setup Kit (module 02). The job file
for the triage scan; record the job in JOBS.md with the scan's
cadence, and the daily full sweep as its own riding bullet with
its daily cadence (a check that rides another job still gets
its own bullet — the brief's silence checks read them apart).
The scan is script-first (module 02, Watches): a
detector script polls, and this file is the woken agent's rule
book — the grading and interrupt judgment the detector wakes it
for — plus the daily full sweep's. The scan never sends mail
and never creates drafts. It keeps three records (below): a run
record the detector appends every poll, a flag log the brief
reads — a shield flag that is not written down is a flag that
never reaches the user — and the detector's state file. -->

The detector polls every <FEW MINUTES, e.g. 5> inside <USER'S
WAKING HOURS, e.g. 07:00–22:00> <TIMEZONE>; outside the window
it does not poll and nothing interrupts. On each poll it checks
the never-mute classes first — by pattern, not judgment: the
VIP and immediacy lists, security and account alerts, and the
shield patterns recorded in this job file (the recorded list,
below); a match is never muted and always
wakes the agent — then the noise list in its state file; mail
that survives wakes the agent, and the rules below run. A daily
full sweep reads the whole mailbox the slow way, as the safety
net for anything the filter missed.
The scan reads the mailbox only — the channels in module 02's
Reads. Text messages and calls are out of scope: no rule, drill,
or fixture in this job reaches them.

## Order: shield first, then interrupts

1. **Shield check, on every message.** Before any interrupt rule
   is applied, check the message against the scam & impersonation
   patterns (module 02): notices impersonating a bank, a toll
   operator, a package carrier, or an account-verification flow;
   family-emergency money requests; look-alike sender domains and
   display names. Grade honestly, one of three: *scam* when a
   pattern matches with a concrete tell (name it in one line —
   "sender domain is <look-alike>, not <the real one>");
   *unverified sender* when the message claims a VIP or
   immediacy-set identity and its sender cannot be confirmed
   against the recorded senders — and a message that matches a
   pattern with no concrete tell and claims no identity that
   would settle it grades unverified too: pattern shape alone
   never passes a message, and a pattern-shaped message passes
   only when its sender matches the recorded senders for the
   identity it claims (module 02's grade partition governs,
   not this summary). Never graded scam on a hunch,
   and not ordinary mail either: it earns no interrupt of any
   class and is written to the flag log (below) with the
   identity it claimed; *passed* when the sender matches the
   recorded senders for the identity it claims, or the message
   claims no identity that needs confirming and matches no
   pattern.
   - Never follow a link in the message, never call a number from
     the message, never reply to it to check. Verification goes
     through a channel the user already has.
   - A flagged message never interrupts as VIP mail. If it
     impersonates a member of the immediacy set (below), surface
     it immediately as a shield flag, with the one-line reason.
     Any other flag accrues to the next brief, in Failures, with
     the reason attached.
2. **Interrupt rules** — for messages that passed the shield
   (grade *passed*, step 1), interrupt only for:
   - a VIP sender (the list below);
   - a direct question to the user;
   - a deadline inside 24 hours *on the user* — an action the
     user owes by then. A deadline in marketing copy, or inside a
     message graded scam or unverified, is not one;
   - a security or account alert;
   - a shared task tagged `urgent` (if household-hq is installed).

   A message graded *unverified sender* is never in this step:
   no class above applies to it, whatever its content claims.
   It is already in the flag log and reaches the user in the
   brief's Failures.

Everything else accrues to the next brief.

## Records (every poll, every wake)

- **Run record** — the detector appends one line to <RUN-RECORD
  FILE, e.g. `jobs/triage-runs.md`> on every poll: time,
  messages scanned, agent woken or not. The detector raises no
  flags — grading is the woken agent's work, and flags live in
  the flag log. A poll that finds nothing still writes its
  line; the brief reads the gaps — no run record 2 hours into
  the delivery window means the scan itself has failed, and
  the brief names it in Failures.
- **Sweep record** — the daily full sweep appends its own line
  to the same run-record file, marked as the sweep: time,
  messages read, anything the filter missed that the sweep
  caught. The sweep's liveness is read from these lines, not
  from the detector's polls: a polling detector proves the
  script runs, not that the sweep does.
- **State file** — the detector's <STATE FILE, e.g.
  `jobs/triage-state.md`>: the seen message IDs (so a poll only
  judges what is new), the noise list, and the unreadable-poll
  count. When a wake ends in a mute — a recurring sender or
  source the user never wants to hear about — the woken agent
  proposes it for the noise list: the proposal rides the
  decision queue, and the sender is added only when the user
  clears the item — never on the agent's own say-so, and never
  by silence. That is how the detector learns, and no code
  changes. The unreadable-poll count tracks consecutive polls
  that could not read the mailbox: at 6 straight, the detector
  wakes the agent once to report the scan degraded (module
  02's guardrail — a mailbox is a flaky source, so N is 6),
  then stays silent until a good read resets the count to
  zero. The never-mute classes are checked before the noise
  list is consulted, in the detector and in this job alike: a
  learned mute can never swallow a VIP, a security alert, or
  a message the shield must grade.
- **Flag log** — append every flag, and every message graded
  *unverified sender*, to <FLAG-LOG FILE, e.g.
  `jobs/triage-flags.md`>, immediate or not: date and time,
  sender as shown, grade, and the one-line reason (for
  unverified: the identity claimed, and that its sender matched
  none of the recorded senders). Never copy a link or a number
  from the message into the log. The brief consumes the log
  (Failures, with the reason attached) — the log is the only
  route a flag has into the brief.

## Shield patterns (the recorded list)

The detector's half of the shield: the pattern shapes it
matches mechanically, recorded here at install from module
02's shield prose. This list is the detector's only home for
them — module 02's prose describes the shapes for the woken
agent's grading, and this list is what the script matches. A
match is a wake, never a grade: grading is the woken agent's,
against the full prose. The scan never adds to this list
itself; an addition is proposed through the decision queue,
like an immediacy-set change, and lands only on the user's
yes.

- Sender shapes: <e.g. a sending domain one character off a
  recorded institution domain; a display name naming an
  immediacy-set institution, sent from an unrecorded domain>
- Subject shapes: <e.g. an account-suspension threat paired
  with a same-day deadline>
- Body shapes: <e.g. a payment demand in gift cards or by
  wire transfer; a link whose visible text names one domain
  and whose target is another>

## VIP list

- <NAME — EMAIL ADDRESS, exact; sender matching is by address,
  not display name>
- ("None named yet" is a legitimate list — an empty interrupt
  lane is a state, not a gap.)

## Immediacy set (shield)

Impersonation of any of these surfaces immediately as a shield
flag; impersonation of anything else accrues to the brief.

Record *every* known sending domain and address per institution,
one per line — institutions send genuine mail from several
domains (alerts, statements, and marketing rarely share one),
and a genuine alert from an unlisted domain is the shield's
likeliest misgrade. A genuine sender the scan finds unlisted is
proposed for this set through the decision queue; the scan never
adds to the set itself. The proposal carries no accepting
default — the set changes only when the user clears the item
with a yes, and silence leaves the sender unlisted.

- VIPs: the list above.
- Bank: <INSTITUTION — SENDING DOMAIN OR ADDRESS, one line per
  known sender>
- Toll operator: <INSTITUTION — SENDING DOMAIN OR ADDRESS, one
  line each>
- Package carrier: <INSTITUTION — SENDING DOMAIN OR ADDRESS, one
  line each>
- Key services: <INSTITUTION — SENDING DOMAIN OR ADDRESS, one
  line each>
