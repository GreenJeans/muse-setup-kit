# Module 05 — Evaluation Kit

**Reads:** your procedures and memory, frozen into an audit packet.
**Writes:** packets, findings, adoption records, eval results. **Network:** a second
model if used for blind review. **Jobs:** an audit reminder on cadence.
**Data classes:** personal, third-party. **Action classes:** none.

## Purpose

The procedures and memory that govern the agent were written by the agent
and its user, in the flow of work, with shared blind spots. This module is
how the setup reviews *itself*: scheduled, blind, evidence-based audits
whose findings the user adopts or rejects one by one.

The module has two tracks. The audit method below (Track A) reviews the
governing documents. Track B, after it, runs the agent itself on
measured tasks, so a proposed change to the setup can be compared
instead of argued.

## The audit method

1. **Freeze a packet.** Copy the governing documents (procedures, agent
   instructions, the brief's instructions) verbatim, timestamped, into one
   packet document. Before freezing, scrub the packet against
   procedures §13: a packet is a copy that travels, so sensitive
   figures and details that live in the governing documents are
   redacted to existence pointers — reviewers audit the rules, and
   §13 records do not travel with them. Add **incident seeds**:
   short, factual accounts of
   real failures (a false "done", a decision taken from a summary instead
   of the source, a job that silently stopped). Seeds are what turn a
   style review into a systems review.
2. **Plant a canary.** Include one known staleness in the packet — a
   reference to a job or rule that has since been retired. A reviewer who
   doesn't catch the canary wasn't reading closely; weight their findings
   accordingly.
3. **Review blind, twice.** Two independent reviewers — ideally two
   different models (the Exchange, module 04, is the natural channel) —
   get the identical packet and brief: find contradictions, stale
   references, gates that don't bind, rules the documents claim but the
   machinery doesn't implement. Neither sees the other's work. *Degraded
   mode:* with only one reviewer available (no second model, no
   Exchange), run a single blind review and record the audit as
   single-reviewer in the adoption record — the convergence signal is
   lost, and the user should know the audit was weaker.
4. **Ingest and adjudicate.** The maintainer compares the reviews against
   the *live* system (some findings will be artifacts of the packet —
   export mangling, stale copies; verify before crediting). Convergent
   findings are the high-confidence set. Disputes are recorded with the
   evidence on both sides.
5. **Adopt explicitly.** The user approves changes one by one or as a
   numbered list ("adopt 1–12"). Each adopted change is applied, and the
   adoption is recorded with date and source. Nothing is adopted by
   default, by silence, or by the reviewers' say-so.

## Track B — task runs (measured)

The audit method reviews the documents. This track runs the agent.
When a change to the setup is proposed — a new rule, a new tool, a
different way of declaring work done — judgment plus one rehearsal is
how most setups decide, and it is not measurement. Track B borrows
its shape from Harbor's task runs, deliberately smaller:

- A **task** is a directory: `instruction.md` (what the agent gets),
  a verifier script (verify.py, a deterministic checker), optional
  `seed/` (the
  starting files) and `solution/` (a known-good end state). The
  verifier judges the final state the agent leaves behind, never its
  final message.
- **The oracle rule.** A task is trustworthy only if its verifier
  FAILS on the untouched seed and PASSES on the solution. Run the
  oracle check (`tools/run_eval.py`, run with `--oracle`) after
  adding or
  changing a task, before trusting anything it reports.
- A **comparison** is the same tasks under the old setup and the new
  one, the model held fixed and named in the job record, at least 3
  trials per arm. Report pass rate, human interventions, and wall
  time. A single run is a smoke test, not a measurement.
- Decide the adoption rule before running, and record negative
  results with the same care as positive ones. A change adopted
  without a comparison is labelled **provisional** wherever it is
  recorded, until a comparison replaces the label.
- No task may require a ticket, a send, money, or a live account.

The module ships three fictional seed tasks and the runner, in
`evals/` and `tools/run_eval.py`: a memory-supersede task (module
01), a feature-gate task (module 00's verifier-gated done), and an
error-compaction task (module 00). They are worked examples and a
starting set; the tasks that matter most are the ones written from
your own work. The fuller treatment of the pattern is the Learn
Harness Engineering course (walkinglabs), named in module 00's
further reading.

The kit's first recorded comparison is a negative, kept on
purpose: the maintainer ran module 00's verifier gate against
prose records (module 00 tells the story and gives the numbers;
the job records are not shipped with the kit), and the mechanism
was reclassified on the strength of what the run did measure.
The comparison also missed this track's own reporting standard:
the model was named only to runtime level, wall time was not
instrumented, and interventions were unavailable by design, so
the adoption bar's intervention clause could never bite.
Recorded anyway, shortfalls named — a comparison that misses
the standard and says so is worth more than one that quietly
rounds up.

## Standing evaluations (cheap, continuous)

- **Memory fidelity sample** (module 01): weekly random claims checked
  against sources, plus one planted discrepancy as a test case.
- **Backup verify pass** (infra patterns, `docs/patterns/infra-patterns.md`): archives are test-read, not assumed.
- **Wizard dry run** (for this kit): run the setup wizard in a fresh,
  memory-free session and confirm it produces a coherent setup.
- **Kit doctor** (this module's `tools/kit_doctor.py`): a read-only
  drift check — plan, jobs, and procedures files present, install
  commit recorded, deferred checks not overdue.

## The usage audit (part of the audit)

Once a month, folded into the audit cycle above, inventory every
scheduled job and hook — `JOBS.md` is the register — and rank
them by **estimated load**: runs per week × context weight. A
full agent run is the heavy unit; a refresh or partial run
weighs less; a script poll (module 02's detectors) weighs
almost nothing. The ranking is the deliverable. It flags the
jobs whose cadence exceeds their source's rate of change — a
daily agent run watching a source that moves monthly — and
names the fix for each: band the cadence, convert the watch to
script-first, or retire it.

Rankings only, never figures. Per-run token numbers circulate
in field reports and blog posts, and they are unreliable —
self-reported, method-free, and usually inflated; an audit that
quotes them has invented its evidence. Relative load is enough
to act on: the heaviest job is the heaviest job whether or not
anyone can price its runs to the token. Money is the spend
check's question (module 09); load is this one's.

## Install

1. Write the audit cadence into the procedures (the audit-cadence
   section; module 00's template carries one) and record the audit
   reminder in `JOBS.md` — a scheduled job if scheduling exists,
   otherwise an on-demand chore with a named owner.
2. Assemble a dry packet from the current procedures, instructions,
   and brief instructions — verbatim, timestamped — to prove the
   freeze works before the first real audit depends on it.
3. Draft incident seeds with the user: real ones if any exist (facts
   only, no blame). A fresh install has none, and that is expected —
   start from `templates/fictional-seeds.md`, label them fictional in
   every packet that uses them, and replace them with real seeds as
   incidents happen.
4. If shell/python is available, copy `tools/kit_doctor.py` into the
   workspace tools folder. It is the mechanical half of an audit —
   missing plan/jobs/procedures files, an install commit of record,
   overdue deferred checks — run before a packet is frozen so the
   reviewers spend their attention on judgment, not bookkeeping.
5. Agree the reviewer channel: the Exchange (module 04) if installed,
   or single-reviewer degraded mode — recorded as such in the plan,
   so the first audit's strength is known in advance.

## Cadence

Monthly on the 1st while the procedures are changing; quarterly once
stable; out-of-cycle when a new incident class appears or a gate rule is
edited. The brief's monthly pass reports whether an audit is due — it
never runs one inside the brief. The usage audit stays monthly even
once the procedures audit goes quarterly: jobs accumulate faster
than rules change.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
