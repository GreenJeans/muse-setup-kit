# Money watch — baseline

<!-- Template from the Muse Setup Kit (module 02). One line per
recurring charge, built with the user from their own exports
(module 02, "The money watch"). Amounts are positive dollars,
whatever sign the export used. Every line carries a source
pointer: the export file it came from, and the date or line in
it. This file is a financial record (procedures §13): it lives
in a local workspace file, never on a shared surface, and its
figures are quoted from this file, not from memory. -->

Built: <YYYY-MM-DD>, from <EXPORT FILE(S)>
Review-by: <YYYY-MM-DD> (procedures §13 — this file is a holding;
the plan ledgers this date so the brief surfaces it)

## Excluded categories

Exclusions narrow what is flagged; they never make a charge
invisible. They change only on the user's explicit instruction,
recorded here with its date.

- <CATEGORY> — variability (amount changes never flag; a first
  sighting still flags NEW)
- <CATEGORY> — sensitivity (a first sighting flags as NEW with no
  merchant or amount printed; never quoted)

## Baseline

- <MERCHANT, as it appears on the statement> — <0.00>,
  <monthly / annual / other cadence>. Source: <export file, date
  or line>.

## How this file changes

A watch run never edits this file. When the user resolves a
flag's decision-queue item — or confirms a change directly — the
agent updates the affected line and records the decision and its
date on the line itself, e.g.: "Updated <YYYY-MM-DD> per queue
#<n>: price change accepted." A money-watch queue item never
resolves by silence: it carries no accepting default, and its
only default is no action.

## Retired

- <MERCHANT> — retired <YYYY-MM-DD> per queue #<n>: user
  confirmed cancellation.
