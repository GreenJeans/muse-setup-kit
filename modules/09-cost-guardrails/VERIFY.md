# Verify — Module 09: Cost & Billing Guardrails

## At install

- [ ] The bucket register exists in the procedures, built from the
      module's template, and lists every model/provider surface the
      agent can reach — no surface in use is missing, and any
      unclassifiable surface is marked UNKNOWN. An UNKNOWN that
      nobody has flagged to the user as a finding fails this check.
- [ ] Every API key or org in the register has a hard cap recorded,
      or the user's explicit uncapped decision in their words. If
      the register lists no API-bucket surface at all, it says so
      in words ("no API key or org in use") — an absent row is not
      a pass, and no register row still contains a `<...>` token.
- [ ] The declare-before-heavy-work rule is in the procedures.
- [ ] The monthly spend check is recorded in `JOBS.md`.

## Deferred

- [ ] **First spend check** (due: 30 days after install): usage read
      for every bucket in the register, compared against caps; any
      surprise (new bucket, cap approached, unexplained spend) is in
      the decision queue.
- [ ] **Bucket-declaration sample** (due: with the first spend
      check): the month's heavy runs each show a bucket declaration
      in their plan or kickoff — a run with none is a finding against
      rule 2, recorded whether or not it cost anything.
