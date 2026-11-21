# Eval set — measured setup changes (Harbor pattern)

Purpose: stop shipping setup changes on judgment plus one rehearsal.
A change is measured by running the SAME tasks, model fixed, under the
old setup and the new setup, and comparing verifier results.

## Shape (borrowed from Harbor, deliberately smaller)
- A **task** is a directory: `instruction.md` (what the agent gets),
  verify.py (deterministic checker; exits 0 = pass, prints reasons),
  optional `seed/` (starting files copied into a fresh work dir per
  trial) and `solution/` (a known-good end state).
- A **trial** = one agent run in a fresh copy of `seed/`, then
  verify.py against what the agent left behind.
- A **job** = N trials x tasks for one variant. The runner records
  each trial's result in `results/`; the job record adds the variant
  label, the model, human interventions, and wall time.
- An **oracle** check: each task's verify.py must FAIL on the
  untouched seed and PASS on the solution — run
  `tools/run_eval.py` with `--oracle`, run from the module's folder,
  after adding a task, before trusting it.

## Rules
- Model held fixed within a comparison. Name the model in the job
  record.
- 3 trials per variant minimum (agents are stochastic; 1 run proves
  little). A single run is a smoke test, not a measurement.
- Verifiers inspect what the agent left behind, never its final
  message.
- No task may require a ticket, a send, money, or a live account.
- A change adopted without a comparison is labelled provisional
  wherever it is recorded.

## Seed tasks
- 001-memory-supersede — move a superseded claim correctly
  (module 01's memory schema).
- 002-feature-list-gate — complete a feature without editing its
  verifier (module 00's verifier-gated done).
- 003-error-compaction — fix a config using only the compact error
  block (module 00's error compaction).

## Your first comparison
Pick the next change you are tempted to adopt on judgment alone.
Run it as arm B against your current setup as arm A, on the seed
tasks plus one task from your own work. Decide the adoption rule
before you run (for example: adopt B if it passes at least 2 of 3
more trials than A, or passes equally with fewer human
interventions). A negative result is a result: record it and drop
the change.
