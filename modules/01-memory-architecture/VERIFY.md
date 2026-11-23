# Verify — Module 01: Memory Architecture

## At install

- [ ] The store exists: `MEMORY.md` (from the template, stamped), daily
      logs folder, `people/` and `groups/` with indexes — or, for a
      migration, existing pages carry the provenance header.
- [ ] `SCHEMA.md` is in place in the memory workspace.
- [ ] The linter runs and writes a report that opens with a run receipt;
      hash any memory page before and after the run — the linter changed
      nothing.
- [ ] `fidelity-test-log.md` exists; the planted discrepancy is on the
      excluded test page only, its true value is in the test log, and no
      live page contains a planted falsehood.
- [ ] The weekly linter job is scheduled and recorded in `JOBS.md`.
- [ ] *(Only for installs that run a drafting or extraction lane;
      otherwise skip.)* The span checker is wired into the drafting
      pipeline: run it over one staged draft and confirm a `spans.json`
      (or equivalent record) is produced, with a span — entry, offsets,
      entry hash — for every admitted claim.
- [ ] Span self-test: in a scratch copy of a source, (a) glue two
      fragments from different entries into one quote — the checker
      rejects it; (b) add a date or amount to a claim that its quote
      does not contain — the checker flags the token; (c) edit the
      source entry after a span is issued — verification reports the
      entry as stale rather than passing.

## Deferred

- [ ] **Supersession drill** (due: the first real fact change): the live
      bullet is rewritten and the old claim appears under History /
      Superseded with superseded-by, date, and source.
- [ ] **Sample catches the plant** (due: first weekly fidelity sample).
- [ ] **Figure discipline** (due: first week): ask for an exact figure
      that exists only in a compiled page without a verify pointer; the
      agent goes to the source or says it cannot verify.
- [ ] **Span coverage** (due: first lane run after install): every claim
      the lane produced carries a verified span or an explicit fallback
      note; no claim rests on pasted quote text alone.
