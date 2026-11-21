Staged: 2026-11-20

# Proposal — patch `invoice-chaser`

## Signal
User correction (workflow / sequence): Alex changed the reminder
cadence the skill prescribes.

## Evidence
Verbatim, main chat, 2026-11-20: "stop sending the day 7 reminder —
clients hate being chased a week in. First reminder at day 14, and
make the last one flag me before it goes out."

## Preference-order justification
(1) The skill in play: the correction is about `invoice-chaser`'s own
cadence steps, so the patch lands there. (2) No umbrella skill covers
invoicing. (3) The change is to existing steps, not reference material,
so no support file. (4) No new skill — the class already exists.

## Change summary
+3/−3 lines in custom-skills/invoice-chaser/SKILL.md, step 2: the
day-7 reminder is removed; the first reminder moves to day 14
(friendly, invoice PDF attached); day 21 becomes the second reminder
(firmer, offer a call); a day-28 final reminder is added, flagged to
Alex before sending. Step 4 — no reminder is ever sent without Alex
seeing the draft first — is unchanged, so the human gate on every
actual send survives this patch; only the timing changes.

## Risk if wrong
Clients get chased later than Alex wants and a slow payer gets an
extra week of slack. Reversed by a follow-up patch restoring the old
cadence (the diff is small and the prior text is in this folder's
diff.patch).

## Routing note
None — the whole signal is a how-to rule for this skill; no fact
about Alex or any client belongs in memory from it.
