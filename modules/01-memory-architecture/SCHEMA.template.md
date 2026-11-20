# Memory Schema

<!-- Template from the Muse Setup Kit. Adapt names to your platform. -->

## Layers

- **Raw sources** — conversations, daily logs, documents, system outputs.
  Immutable once written; the authority for exact figures.
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
   as absent.
4. **Provenance header** on every compiled page:
   `schema_version`, `last_verified` (date), `sources`. A page without a
   header is legacy and untrusted until stamped.
5. **Verify pointers.** Precise claims gain `(verify: <where the original
   lives>)` opportunistically — when the claim is written or next touched.
6. **Tag uncertainty inline.** `[inference]` and `[hypothesis]` mark
   claims that are not established fact. Untagged means fact. No numeric
   confidence scores, no decay functions, no auto-archiving.
7. **Time-bound claims** carry `(review-by: YYYY-MM-DD)` instead of a
   score.
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

## The linter (deterministic, read-only)

Minimum checks: header presence; figures without pointers in live
sections; scheduled-job names in procedure documents vs. the live
scheduler; review-by dates passed. Every run writes a report and a run
receipt; a run that produces no report is a failure, not a pass.
