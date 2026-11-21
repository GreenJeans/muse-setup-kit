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
- [ ] Every row has a lead time, set with the user and recorded
      on the row. On an `unknown` row the lead time is the
      provisional window that applies the day the date is read —
      required, not decorative.
- [ ] If the seed includes an item already past its expiry, its
      state reads expired — not current, not clear.
- [ ] Surfacing is wired as the plan states: the brief job's
      sources name the register and its instructions keep — or,
      for a module installed after the brief, restore — all three
      `[IF deadlines register installed]` blocks (brief installs),
      or the manual deferred check is recorded in the plan's
      verification ledger with its cadence (no-brief installs) —
      and the plan says in words which of the two is true.
- [ ] Every row carries its On expiry field (renew or lapse),
      set with the user or recorded as the module's default.

## Deferred

- [ ] **Lead-time crossing** (due: the first item's lead-time date
      after install; if an item is already inside its window at
      install, due at the first brief after install instead — the
      ledger row names the event and `due:` carries the operative
      date): the item surfaces in the brief's Today
      section on the day it crosses, carrying the expiry date as
      recorded in the register — and, before anything is acted on,
      the date is re-read from the source document. For a no-brief
      install, the manual check is what fires, on its recorded
      cadence.
- [ ] **Renewal drill** (due: the first renewal after install, or
      install + 6 months, whichever comes first — the ledger row
      names the event and `due:` carries the earlier date): the
      renewed item's row shows the new expiry as current state,
      the old expiry sits in History with the renewal date, and
      the item stops surfacing.
- [ ] **Expired handling** (due: the first item to expire after
      install, or install + 12 months, whichever comes first —
      the ledger row names the event and `due:` carries the
      operative date; an item already expired at install makes it
      due at the first brief after install): the expired item
      appears in the brief's Failures
      section — never in Today, never described as clear — and
      keeps appearing until it is renewed or dropped (a lapse
      item appears once, then sits in History as lapsed).
- [ ] **Unknown-date chase** (due: the first brief after install,
      or install + 7 days, whichever comes first — the ledger row
      names the event and `due:` carries the operative date;
      brief installs only, and only when the seed holds an
      `unknown` item): the item appears in the brief's Today
      section as a one-line chase item, and keeps appearing in
      every brief until it is dated or dropped.
