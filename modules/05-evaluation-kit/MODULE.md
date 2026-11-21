# Module 05 — Evaluation Kit

**Reads:** your procedures and memory, frozen into an audit packet.
**Writes:** packets, findings, adoption records. **Network:** a second
model if used for blind review. **Jobs:** an audit reminder on cadence.

## Purpose

The procedures and memory that govern the agent were written by the agent
and its user, in the flow of work, with shared blind spots. This module is
how the setup reviews *itself*: scheduled, blind, evidence-based audits
whose findings the user adopts or rejects one by one.

## The audit method

1. **Freeze a packet.** Copy the governing documents (procedures, agent
   instructions, the brief's instructions) verbatim, timestamped, into one
   packet document. Add **incident seeds**: short, factual accounts of
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

## Standing evaluations (cheap, continuous)

- **Memory fidelity sample** (module 01): weekly random claims checked
  against sources, plus one planted discrepancy as a test case.
- **Backup verify pass** (infra patterns, `docs/patterns/infra-patterns.md`): archives are test-read, not assumed.
- **Wizard dry run** (for this kit): run the setup wizard in a fresh,
  memory-free session and confirm it produces a coherent setup.
- **Kit doctor** (this module's `tools/kit_doctor.py`): a read-only
  drift check — plan, jobs, and procedures files present, install
  commit recorded, deferred checks not overdue.

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
never runs one inside the brief.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
