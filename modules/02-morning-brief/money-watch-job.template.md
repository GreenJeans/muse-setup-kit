# Job — Money watch (weekly)

<!-- Template from the Muse Setup Kit (module 02). The job file
for the money watch; record the job in JOBS.md with the same
cadence. If the install chose other paths for the baseline or the
run records, this file names those paths instead. -->

Run weekly, on <DAY>. Compare the newest user-supplied export
against `finance/money-watch-baseline.md`, and append the run
record to `finance/money-watch-runs.md` either way.

- Data arrives only as exports the user supplies — never
  credentials, never a bank login (module 02). A run with no new
  export records "no new data" and stops.
- Flag only: a first sighting (NEW — a candidate, not yet in the
  baseline), a changed amount on a baseline charge, a duplicate.
  Amounts are compared as positive dollars, whatever sign the
  export uses. Excluded categories — named in the baseline file —
  are never flagged.
- A flag becomes a decision-queue item. The watch never cancels,
  disputes, or contacts anyone, and it never edits the baseline:
  baseline lines change only when the user resolves the item, and
  the decision and its date are recorded on the line.
- No run record within 48 hours past this cadence means the watch
  itself is the failure (detector silence, procedures §4).
