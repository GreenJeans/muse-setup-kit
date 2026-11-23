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

   **Weighted down, defined.** Every finding carries a basis, one of
   four, strongest first: **measured** (a number from an actual run),
   **reproduced** (someone made it happen again), **reviewed** (an
   independent second check agrees — convergence in step 4 is the
   usual case), **reasoned** (argued from the material, unchecked).
   A finding is *weighted down* when its basis is reasoned only. A
   weighted-down finding is reported in full, like any other; it is
   never prioritized ahead of a better-based one. The canary rule
   above is the standing example: a reviewer who missed the canary
   has shown their reading was not close, so their solo findings
   stand at reasoned until something checks them.
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

**Judges advise; they do not gate.** Where a reviewer is a model,
its verdict enters this method as a finding with a basis, never as
a decision. The measurement behind that stance is recent and
stark: Rosset et al. (Microsoft Research and Browserbase, Apr
2026; the Universal Verifier work, arXiv:2604.06240) scored
bundled benchmark judges against human gold labels and found
false-positive rates of at least 45% for WebVoyager's judge and
at least 22% for WebJudge — and the same agent scored 74% under
WebVoyager's official judge and 38% under their stricter
verifier. A judge that passes that many wrong runs is a lens,
not a gate: deterministic checks run first where they exist
(below), and adoption stays with the user (step 5).

**Measure a judge by defect class, not in aggregate.** When a
judge's error rates are measured — and an unmeasured judge is a
lens of unknown strength — report the false-positive and
false-negative rates split by defect class, because the
aggregate conceals the class the judge is blind to. The
maintainer measured one deterministic judge this way, a
quote-verification gate in a memory ingest lane, on a held-out
set written for the trial: aggregate false positives 13.3%,
false negatives 20% — and both numbers lied by averaging.
Split by class, the same gate caught every fabrication (0 of
26 passed) and passed every misleading truncation (4 of 4): a
quote that is a genuine substring but drops a negation or a
hedge sitting just outside it passes an existence check by
construction, so that class is uncatchable by that gate and
belongs to a different layer of the design. Every false
negative sat in a single formatting class. The aggregate said
"a fairly good gate"; the split said which failures it will
never see — the second statement is the one a design can use.

**One snapshot per round.** A review under this method runs against
one recorded snapshot: the frozen packet for a document audit, a
named commit or tree for code. The snapshot is recorded before the
review starts, and findings cite it. Anything that lands after the
snapshot is a new round, not a silent amendment to the one under
review. A finding is a claim about a specific state of the work;
made against a moving target, it cannot be checked afterward, and
neither reviewer nor maintainer can say which version it belongs
to. The benchmark literature learned the same lesson the hard
way: scores are comparable only within a pinned version of a
task set — Terminal-Bench's maintainers warn against comparing
across its own versions, which churned four times in a year —
and a result quoted without its task-set version is not a
measurement. A review is a measurement; this rule is its pin.

**When the packet is code.** The same method reviews a large code
change, with one ordering rule: deterministic checks first. Every
mechanical check the repository has — type checker, lint, the test
suite — runs before any agent review, and its output is the
reviewers' first input, ahead of the diff. Agent reviewers then
work named lenses, one lens each — security, simplicity, edge
cases, scope — on what the tools cannot check. The lens evidence
is old and human: Porter, Votta & Basili (1995, *IEEE
Transactions on Software Engineering* 21(6)) showed that
reviewers assigned specific fault scenarios detected roughly
35% more faults in requirements inspections than reviewers
sharing one general checklist. That is evidence about human
inspection of requirements documents, not a measurement of
agent reviewers; the kit adopts the shape, not the number. The
ordering needs no
citation: a change can pass several agent reviewers and still
ship what a type checker would have caught, when nobody ran it.

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
- **Coverage is not a pass rate.** Repeated-sampling gains are
  usually pass@k coverage — the share of tasks solved by *any*
  sample. Brown et al. (2024, arXiv:2407.21787), sampling a
  code model on SWE-bench Lite, report issues solved rising
  from 15.9% with one sample to 56% at 250; that 56% is
  coverage, reachable only under an oracle — a perfect verifier
  that picks the winning sample every time. A real gate lands
  below it, and without a gate that can reject, selection
  plateaus. Cap N by gate strength: a
  weak gate earns small N plus a human skim, not large N
  trusted blind.
- A **comparison** is the same tasks under the old setup and the new
  one, the model held fixed and named in the job record, at least 3
  trials per arm. Report pass rate, human interventions, and wall
  time. A single run is a smoke test, not a measurement. Where the
  arms differ in shape — one agent against several — hold the spend
  roughly equal across arms, or record plainly that the comparison
  is not equal-spend: token usage alone explained about 80% of the
  performance variance in Anthropic's BrowseComp decomposition
  (Jun 2025), so an unequal-spend comparison measures the budget,
  not the shape.
- **Report reliability, not just the headline rate.** Alongside
  pass rate, report **pass^k** — the share of tasks that succeed
  in *all* k trials (the τ-bench lineage) — and **cost per
  success**: the total spend across every trial divided by the
  tasks passed, never cost per attempt. A setup passing 90% of
  tasks once and 40% across three trials is a different setup
  from one passing 70% and 65%, and the headline rate hides
  which. Published production evals (2026) treat the pass@1 to
  pass^k drop as the harness's reliability signature — 9 to 16
  points on one data-engineering bench — and price a harness by
  what a success costs in it, because the same model can cost
  several times more in one harness than in another.
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
