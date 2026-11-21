# Verify — Module 10: Deadlines & Expiry Register

## At install

- [ ] The register file exists at the path the plan records, is
      built from the module's template, and is inventoried in the
      baseline as an accumulating file — adding a row later
      produces no baseline-drift note.
- [ ] Every row carries a source pointer (where the original
      lives). A row without one fails this check.
- [ ] Every item the user named at seeding is present — including
      any item whose expiry is marked `unknown`. An omitted item
      fails this check; an unknown date does not.
- [ ] No row, and no other text in the register, contains a
      document number: no passport, policy, licence, or ID numbers
      anywhere in the file. Document types and dates only.
- [ ] Every dated row has a lead time, set with the user and
      recorded on the row.
- [ ] If the seed includes an item already past its expiry, its
      state reads expired — not current, not clear.
- [ ] Surfacing is wired as the plan states: the brief job's
      sources name the register (brief installs), or the manual
      deferred check is recorded in the plan's verification ledger
      with its cadence (no-brief installs) — and the plan says in
      words which of the two is true.

## Deferred

- [ ] **Lead-time crossing** (due: the first item's lead-time date
      after install): the item surfaces in the brief's Today
      section on the day it crosses, carrying the expiry date as
      recorded in the register — and, before anything is acted on,
      the date is re-read from the source document. For a no-brief
      install, the manual check is what fires, on its recorded
      cadence.
- [ ] **Renewal drill** (due: the first renewal after install): the
      renewed item's row shows the new expiry as current state,
      the old expiry sits in History with the renewal date, and
      the item stops surfacing.
- [ ] **Expired handling** (due: the first item to expire after
      install): the expired item appears in the brief's Failures
      section — never in Today, never described as clear — and
      keeps appearing until it is renewed or dropped.
