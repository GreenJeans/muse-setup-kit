# Verify — Module 05: Evaluation Kit

## At install

- [ ] The audit cadence is written into the procedures (§11) and, if a
      reminder job is used, recorded in `JOBS.md`.
- [ ] A dry packet assembles cleanly from the current procedures,
      instructions, and brief instructions — verbatim, timestamped.
- [ ] The incident-seed format is understood and at least one seed is
      drafted with the user — a real one if any exist (facts only, no
      blame), otherwise a fictional seed from the module's library,
      labeled fictional.

## Deferred

- [ ] **First audit** (due: first cadence date): packet frozen, blind
      review(s) run, ingest compares findings against the live system,
      disputes recorded, and the user adopts or rejects each change
      explicitly. If only one reviewer ran, the record says
      "single-reviewer".
- [ ] **Canary result** (due: with the first audit): the planted
      staleness was caught by at least one reviewer — or the miss is
      recorded and the reviewer brief improved before the next audit.
- [ ] **Track B oracle** (due: before the first Track B job):
      `tools/run_eval.py --oracle` passes on every shipped seed task —
      each verifier fails on its seed and passes on its solution.
- [ ] **First comparison recorded** (due: first Track B adoption):
      the job record names the model (held fixed), runs at least 3
      trials per arm, and reports pass rate, human interventions, and
      wall time. Anything adopted without a comparison is labelled
      provisional in the adoption record.
