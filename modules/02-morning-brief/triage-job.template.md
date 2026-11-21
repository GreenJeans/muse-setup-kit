# Job — Inbox triage scan

<!-- Template from the Muse Setup Kit (module 02). The job file
for the triage scan; record the job in JOBS.md with the same
cadence. The scan never sends mail and never creates drafts. -->

Run every 30 minutes, <USER'S WAKING HOURS, e.g. 07:00–22:00>
<TIMEZONE>. Outside the window, do not scan and do not interrupt.

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

## VIP list

- <NAME — EMAIL ADDRESS, exact; sender matching is by address,
  not display name>
- ("None named yet" is a legitimate list — an empty interrupt
  lane is a state, not a gap.)

## Immediacy set (shield)

Impersonation of any of these surfaces immediately as a shield
flag; impersonation of anything else accrues to the brief.

- VIPs: the list above.
- Bank: <INSTITUTION — REAL DOMAIN>
- Toll operator: <INSTITUTION — REAL DOMAIN>
- Package carrier: <INSTITUTION — REAL DOMAIN>
- Key services: <INSTITUTION — REAL DOMAIN, one line each>
