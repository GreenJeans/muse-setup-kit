# Job — Money watch (weekly)

<!-- Template from the Muse Setup Kit (module 02). The job file
for the money watch; record the job in JOBS.md with the same
cadence. If the install chose other paths for the baseline or the
run records, this file names those paths instead. -->

Run weekly, on <DAY>. Compare the newest user-supplied export in
`finance/exports/` (or the folder the plan recorded) against
`finance/money-watch-baseline.md`, and append the run record to
`finance/money-watch-runs.md` either way.

- Data arrives only as exports the user supplies — never
  credentials, never a bank login (module 02). A run with no new
  export records "no new data" and stops. New data is judged by
  transaction date: rows dated inside the last run's covered
  period that match a covered row on date + merchant + amount are
  overlap, neither new nor duplicates.
- Flag only: a first sighting (NEW — a candidate, not yet in the
  baseline), a changed amount on a baseline charge, a duplicate.
  Amounts are compared as positive dollars, whatever sign the
  export uses. Excluded categories — named in the baseline file —
  narrow flags by kind: a variability exclusion silences amount
  changes (a first sighting still flags NEW); a sensitivity
  exclusion flags a first sighting as NEW with no merchant or
  amount printed.
- A flag becomes a decision-queue item. The watch never cancels,
  disputes, or contacts anyone, and it never edits the baseline:
  baseline lines change only when the user resolves the item or
  confirms the change directly, and the decision and its date are
  recorded on the line. A money-watch item never carries an
  accepting default — its only default is no action, and silence
  never changes the baseline.
- No run record within 48 hours past this cadence means the watch
  itself is the failure (detector silence, procedures §4).
