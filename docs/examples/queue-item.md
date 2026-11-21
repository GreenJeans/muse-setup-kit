## Open

1. **Skill write (staged) — patch `invoice-chaser`** [type: skill-write]
   Signal: user correction (workflow), 2026-11-20, main chat —
   "stop sending the day 7 reminder — clients hate being chased a
   week in." (full evidence in staged/1-invoice-chaser/proposal.md).
   Change: +3/−3 lines in custom-skills/invoice-chaser/SKILL.md —
   first reminder moves from day 7 to day 14; cadence becomes
   14/21/28, with the final reminder flagged to Alex before sending.
   Diff sha256: 95e413… (full hash in base.json).
   Diff:
   --- a/custom-skills/invoice-chaser/SKILL.md
   +++ b/custom-skills/invoice-chaser/SKILL.md
   @@ -6,9 +6,9 @@
    
    1. List invoices past their due date from the invoicing sheet.
    2. Send reminder emails on this cadence, counted from the due date:
   -   - Day 7: first reminder, friendly.
   -   - Day 14: second reminder, firmer; attach the invoice PDF.
   -   - Day 21: final reminder; offer a call.
   +   - Day 14: first reminder, friendly; attach the invoice PDF.
   +   - Day 21: second reminder, firmer; offer a call.
   +   - Day 28: final reminder; flag it to Alex before sending.
    3. Log every reminder in the invoice tracker the same day.
    4. Never send a reminder without showing Alex the draft first.
   Base hash: matches the live file as of staging (sha256 492a8c).
   Void if the target changes before approval.
   Risk if wrong: clients chased later than Alex wants; reversible
   by a follow-up patch restoring the old cadence.
   Default if no reply: stays staged, nothing applied. Resurface
   2026-12-04; staging expires after 14 days undecided.
   Smallest ask: "1: approve" / "1: reject" / "1: edit: <change>".

