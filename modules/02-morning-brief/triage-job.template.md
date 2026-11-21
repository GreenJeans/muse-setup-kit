# Job — Inbox triage scan

<!-- Template from the Muse Setup Kit (module 02). The job file
for the triage scan; record the job in JOBS.md with the same
cadence. The scan never sends mail and never creates drafts. It
keeps two records (below): a run record, appended every run, and
a flag log the brief reads — a shield flag that is not written
down is a flag that never reaches the user. -->

Run every 30 minutes, <USER'S WAKING HOURS, e.g. 07:00–22:00>
<TIMEZONE>. Outside the window, do not scan and do not interrupt.
The scan reads the mailbox only — the channels in module 02's
Reads. Text messages and calls are out of scope: no rule, drill,
or fixture in this job reaches them.

## Order: shield first, then interrupts

1. **Shield check, on every message.** Before any interrupt rule
   is applied, check the message against the scam & impersonation
   patterns (module 02): notices impersonating a bank, a toll
   operator, a package carrier, or an account-verification flow;
   family-emergency money requests; look-alike sender domains and
   display names. Grade honestly: *scam* when a pattern matches
   with a concrete tell (name it in one line — "sender domain is
   <look-alike>, not <the real one>"); *unverified sender* when it
   cannot be confirmed either way — handled as ordinary mail,
   never graded scam on a hunch.
   - Never follow a link in the message, never call a number from
     the message, never reply to it to check. Verification goes
     through a channel the user already has.
   - A flagged message never interrupts as VIP mail. If it
     impersonates a member of the immediacy set (below), surface
     it immediately as a shield flag, with the one-line reason.
     Any other flag accrues to the next brief, in Failures, with
     the reason attached.
2. **Interrupt rules** — for messages that passed the shield,
   interrupt only for:
   - a VIP sender (the list below);
   - a direct question to the user;
   - a deadline inside 24 hours *on the user* — an action the
     user owes by then. A deadline in marketing copy, or inside a
     flagged message, is not one;
   - a security or account alert;
   - a shared task tagged `urgent` (if household-hq is installed).

Everything else accrues to the next brief.

## Records (every run)

- **Run record** — append one line to <RUN-RECORD FILE, e.g.
  `jobs/triage-runs.md`> on every run: time, messages scanned,
  flags raised. A run that finds nothing still writes its line;
  the brief reads the gaps — no run record 2 hours into the
  delivery window means the scan itself has failed, and the
  brief names it in Failures.
- **Flag log** — append every flag to <FLAG-LOG FILE, e.g.
  `jobs/triage-flags.md`>, immediate or not: date and time,
  sender as shown, grade, and the one-line reason. Never copy a
  link or a number from the message into the log. The brief
  consumes the log (Failures, with the reason attached) — the
  log is the only route a flag has into the brief.

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
