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

## Excluded categories (never flagged)

- <CATEGORY> — variability (its amounts move normally)
- <CATEGORY> — sensitivity (not watched, not quoted)

## Baseline

- <MERCHANT, as it appears on the statement> — <0.00>,
  <monthly / annual / other cadence>. Source: <export file, date
  or line>.

<!-- A watch run never edits this file. When the user resolves a
flag's decision-queue item, the agent updates the affected line
and records the decision and its date on the line itself, e.g.:
"Updated <YYYY-MM-DD> per queue #<n>: price change accepted." -->
