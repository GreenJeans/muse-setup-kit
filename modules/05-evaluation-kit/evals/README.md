# Eval set — measured setup changes (Harbor pattern)

Purpose: stop shipping setup changes on judgment plus one rehearsal.
A change is measured by running the SAME tasks, model fixed, under
the old setup and the new setup, and comparing verifier results.

The rules for a comparison — model fixed and named, trial counts,
the oracle rule, what a verifier may inspect, the provisional
label — live in module 05's Track B section. This file is the
directory layout and the runner's usage; it does not restate them.

## Shape (borrowed from Harbor, deliberately smaller)
- A **task** is a directory: `instruction.md` (what the agent gets),
  verify.py (deterministic checker; exits 0 = pass, prints reasons),
  optional `seed/` (starting files copied into a fresh work dir per
  trial) and `solution/` (a known-good end state).
- A **trial** = one agent run in a fresh copy of `seed/`, then
  verify.py against what the agent left behind.
- A **job** = N trials x tasks for one variant. Record each trial
  with the runner's `--verify`, passing `--variant` and `--trial`
  so the record names its arm; records land in `results/` and are
  never overwritten. The job record adds the model, human
  interventions, and wall time.
- An **oracle** check: each task's verify.py must FAIL on the
  untouched seed and PASS on the solution — run
  `tools/run_eval.py --oracle` after adding a task, before
  trusting it. A task with no `solution/` reports UNVERIFIED and
  fails the run. The runner finds its tasks relative to its own
  file; if it is copied into a shared tools folder, pass
  `--evals-dir` pointing at this folder.

## Preparing an arm

Arm differences are setup, applied by the harness before the trial,
never by the agent mid-run. Example: for a gated arm on task 002,
the harness copies the seed and runs module 00's
`tools/verify_done.py init` on the copy first, so the feature list
carries its verifier hashes when the agent starts.

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
before you run (for example: adopt B if it passes in at least 2
more trials than A out of the same number of trials, or passes
equally with fewer human interventions). A negative result is a
result: record it and drop the change.
