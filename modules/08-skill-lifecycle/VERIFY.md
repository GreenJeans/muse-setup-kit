# Verify — Module 08: Skill Lifecycle

## At install

- [ ] The decision queue's header defines both item types —
      `[type: skill-write]` and `[type: skill-curator]` — and states
      that silence is never consent for a skill write: the only
      default is stay staged, then expire.
- [ ] The staging area exists (`staged/` plus `staged/applied/`), and
      the staged-proposal template is in place where a reviewer will
      find it.
- [ ] The usage ledger exists with one record per existing custom
      skill; created dates come from verifiable records only, and
      unverifiable counts are null or zero — nothing backfilled by
      guessing.
- [ ] The curator script runs once by hand and its report is shown to
      the user: it moved nothing, deleted nothing, and wrote nothing
      outside the ledger.
- [ ] Exemptions are computed from live sources in that first run
      (job records, procedures, instructions, other skills' files,
      managed review records) — at least one known exemption, if any
      exist in this install, is detected and named with its reason.
- [ ] The agent's main instruction file carries the pointer line:
      skill self-modification stages through this module; no live
      skill write without approval of the staged diff.
- [ ] Both jobs are recorded in `JOBS.md` with cadence and delivery —
      or, before the rollout is approved, recorded as not yet
      scheduled, with the approval that would schedule them named.

## Deferred

- [ ] **Shadow week** (due: 7 days after the sweep is scheduled): the
      sweep staged only to `staged/shadow-*`, filed no queue items,
      and reported only to the module's home. The user judges its
      precision and says whether shadow lifts; lifting it is a
      recorded job change, not a default.
- [ ] **First staged proposal** (due: first real signal after install):
      it carries verbatim evidence, a preference-order justification,
      and a `base.json` whose sha256 matches the live target at
      staging time. Approving it runs the apply procedure end to end —
      hash check, apply, verify, ledger update, queue item resolved.
- [ ] **Hash-drift drill** (due: first month): stage a proposal, then
      edit the target skill, then approve. The apply aborts on the
      mismatch, reports it, and restages fresh — nothing is applied
      over the drift.
- [ ] **First curator item** (due: first weekly run after scheduling):
      at most one batched item; each candidate is individually
      approvable; approving an archive moves the folder to
      `.archive/` and nothing is deleted. Restoring it is a move back
      plus a ledger update.
- [ ] **Expiry works** (due: 14 days after the first undecided item):
      an item left undecided past its expiry is auto-rejected and
      logged — never applied.
- [ ] **30-day review** (due: 30 days after the sweep goes live):
      acceptance rate (bar: at least half of staged items approved or
      edited), false-stale count (an archive restored within 7 days
      counts as one), restage rate, and queue load are reported to the
      user, who decides: keep, tighten the rubric, or drop the module.
