# Memory Schema

<!-- Template from the Muse Setup Kit. Adapt names to your platform. -->

## Layers

- **Raw sources** — conversations, daily logs, documents, system outputs.
  Immutable once written; the authority for exact figures — with one
  carve-out: for sensitive records (procedures §13), the holding file
  is the authority, and a log is not a second home for the figures
  (rule 12).
- **Compiled pages** — the memory the agent loads: a curated long-term
  file, one page per person and per group. Compiled pages are derived and
  may be wrong; sources outrank them.

## Rules

1. **Current state at top.** Live sections contain only what is true now.
   When a fact changes, rewrite its bullet in place.
2. **Supersession in the same edit.** The replaced claim moves to
   `## History` (person/group pages) or `## Superseded` (the long-term
   file) with: superseded-by, date, and source. One home per claim — never
   leave the old and new versions both stated as current.
3. **Exact numbers, dates, amounts, and IDs** are answered and acted on
   from the daily log or the live source, never from a compiled page
   alone. A compiled figure without a `(verify: ...)` pointer is treated
   as absent. Sensitive figures are stricter still — rule 12: a compiled
   page records a holding's existence and pointer, never the figure.
4. **Provenance header** on every compiled page:
   `schema_version`, `last_verified` (date), `sources`. A page without a
   header is legacy and untrusted until stamped.
5. **Verify pointers.** Precise claims gain `(verify: <where the original
   lives>)` opportunistically — when the claim is written or next touched.
6. **Tag uncertainty inline.** `[inference]` and `[hypothesis]` mark
   claims that are not established fact. Untagged means fact. No numeric
   confidence scores, no decay functions, no auto-archiving.
7. **Time-bound claims** carry a review-by date instead of a
   score (format: `review-by: YYYY-MM-DD`, the marker in
   parentheses).
8. **One identity, several writers.** Other agents and background jobs
   produce *sources* (verbatim quotes, attributed). One identity verifies
   and writes the compiled store. Background write paths are attributed in
   version control (e.g. `[in-session]`, `[brief]`,
   `[background-unattributed]`).
9. **Hash-check before rewriting.** Before editing a compiled file in a
   session, confirm it hasn't changed since it was read; re-read if it has.
10. **Lint proposes, never auto-resolves.** Mechanical checks produce
    findings; supersession and contradiction decisions are made by a mind
    and recorded with provenance.
11. **Dates on compiled pages** use the user's home timezone.
12. **Sensitive records stay in their holdings** (procedures §13).
    Figures and details from financial, health, or third-party
    personal records are never copied into compiled pages *or* daily
    logs. What memory records is that a holding exists, where it
    lives, a `(verify: ...)` pointer to it, and its
    review-by date — the linter's review-by check reads
    compiled pages, which is what makes a local holding's review-by
    surface. Exact figures are read from the holding at need.

## The linter (deterministic, read-only)

**Compiled pages** — the files the linter checks — are the curated
long-term file and the person/group pages. Daily logs, lint reports, and
test fixtures (the fidelity test page and log) live alongside them but
are not compiled pages and are excluded, as is anything matched by a
`.lintignore` file in the memory directory.

Minimum checks: header presence on compiled pages; figures without
pointers in live sections; jobs named in the procedures exist in
`JOBS.md` (the scheduler-of-record the wizard maintains); review-by
dates passed. A reference implementation ships with this module
(`tools/memory_lint.py`). Every run writes a report that opens with a
run receipt — timestamp, files scanned, checks run, findings count —
and a run that produces no report is a failure, not a pass. Findings are
candidates for a mind to adjudicate, never auto-fixes. A healthy store
lints quiet: persistent findings mean the linter or the store is wrong,
and either way the discrepancy gets fixed, not tolerated.

## The fidelity test case

One planted discrepancy is kept as a standing test of the weekly sample:
it lives on a dedicated test page that is excluded from the memory the
agent loads, and its true value is recorded in
`memory/fidelity-test-log.md`. It is never planted in a live page — live
sections state only what is true now (rules 1–2 admit no exceptions).
