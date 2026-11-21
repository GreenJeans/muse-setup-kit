# Job — Inbox triage scan

<!-- Template from the Muse Setup Kit (module 02). The job file
for the triage scan; record the job in JOBS.md with the scan's
cadence. The scan is script-first (module 02, Watches): a
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
the never-mute classes first — VIP senders, security and account
alerts, anything the shield must grade — then the noise list in
its state file; mail that survives wakes the agent, and the
rules below run. A daily full sweep reads the whole mailbox the
slow way, as the safety net for anything the filter missed.
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
   against the recorded senders — never graded scam on a hunch,
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
  messages scanned, flags raised, agent woken or not. A poll
  that finds nothing still writes its line; the brief reads the
  gaps — no run record 2 hours into the delivery window means
  the scan itself has failed, and the brief names it in
  Failures.
- **State file** — the detector's <STATE FILE, e.g.
  `jobs/triage-state.md`>: the seen message IDs (so a poll only
  judges what is new) and the noise list. When a wake ends in a
  mute — a recurring sender or source the user never wants to
  hear about — the woken agent adds it to the noise list there;
  that is how the detector learns, and no code changes. The
  never-mute classes are checked before the noise list is
  consulted, in the detector and in this job alike: a learned
  mute can never swallow a VIP, a security alert, or a message
  the shield must grade.
- **Flag log** — append every flag, and every message graded
  *unverified sender*, to <FLAG-LOG FILE, e.g.
  `jobs/triage-flags.md`>, immediate or not: date and time,
  sender as shown, grade, and the one-line reason (for
  unverified: the identity claimed, and that its sender matched
  none of the recorded senders). Never copy a link or a number
  from the message into the log. The brief consumes the log
  (Failures, with the reason attached) — the log is the only
  route a flag has into the brief.

## VIP list

- <NAME — EMAIL ADDRESS, exact; sender matching is by address,
  not display name>
- ("None named yet" is a legitimate list — an empty interrupt
  lane is a state, not a gap.)

## Immediacy set (shield)

Impersonation of any of these surfaces immediately as a shield
flag; impersonation of anything else accrues to the brief.

Record *every* known sending domain and number per institution,
one per line — institutions send genuine mail from several
domains (alerts, statements, and marketing rarely share one),
and a genuine alert from an unlisted domain is the shield's
likeliest misgrade. A genuine sender the scan finds unlisted is
proposed for this set through the decision queue; the scan never
adds to the set itself.

- VIPs: the list above.
- Bank: <INSTITUTION — SENDING DOMAIN OR NUMBER, one line per
  known sender>
- Toll operator: <INSTITUTION — SENDING DOMAIN OR NUMBER, one
  line each>
- Package carrier: <INSTITUTION — SENDING DOMAIN OR NUMBER, one
  line each>
- Key services: <INSTITUTION — SENDING DOMAIN OR NUMBER, one
  line each>
