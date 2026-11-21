# Verify — Module 08: Skill Lifecycle

## At install — Lite

- [ ] The decision queue's header defines the `[type: skill-write]`
      item type and states that silence is never consent for a
      skill write: the only default is stay staged, then expire.
- [ ] The staging area exists (`staged/` plus `staged/applied/` and
      `staged/expired/`), and the staged-proposal template is in
      place where a reviewer will find it.
- [ ] The agent's main instruction file carries the pointer line:
      skill self-modification stages through this module; no live
      skill write without approval of the staged diff.
- [ ] Nothing else was created: no ledger, no tools copied, no jobs
      scheduled or recorded. (If any exist, the install is Full —
      check it against the Full list instead.)

## At install — Full (in addition, at the Lite → Full upgrade)

- [ ] The queue header also defines `[type: skill-curator]`.
- [ ] The usage ledger exists with one record per existing custom
      skill; created dates come from verifiable records only, and
      unverifiable counts are zero (never null) — nothing
      backfilled by guessing.
- [ ] The curator script runs once by hand and its report is shown
      to the user: it moved nothing, deleted nothing, and wrote
      nothing outside the ledger.
- [ ] Exemptions are computed from live sources in that first run
      (job records, procedures, instructions, other skills' files,
      managed review records) — at least one known exemption, if
      any exist in this install, is detected and named with its
      reason.
- [ ] Both jobs are recorded in `JOBS.md` with cadence and
      delivery — or, before the rollout is approved, recorded as
      not yet scheduled, with the approval that would schedule
      them named.

## Deferred — both tiers

- [ ] **First staged proposal** (due: first real signal after
      install): it carries verbatim evidence, a preference-order
      justification, and a `base.json` whose sha256 matches the
      live target at staging time.
- [ ] **First apply** (due: first approval): approving a staged
      proposal runs the apply procedure end to end — hash check,
      apply, verify, queue item resolved. (At Full, the apply also
      updates the ledger.)
- [ ] **Hash-drift drill** (due: first month): stage a proposal,
      then edit the target skill, then approve. The apply aborts
      on the mismatch, reports it, and restages fresh — nothing is
      applied over the drift.
- [ ] **Expiry works** (due: 14 days after the first undecided
      item): an item left undecided past its expiry is
      auto-rejected and logged — never applied. (At Lite the check
      happens at the next filing or apply, per the Tiers section;
      the log line is the evidence either way.)

## Deferred — Full only

- [ ] **Shadow week** (due: 7 days after the sweep is scheduled):
      the sweep staged only to `staged/shadow-*`, filed no queue
      items, and reported only to the module's home. The user
      judges its precision and says whether shadow lifts; lifting
      it is a recorded job change, not a default.
- [ ] **First curator item** (due: first weekly run after shadow
      lifts — Rollout phase 3; weekly runs during shadow file
      nothing): at most one batched item; each candidate is
      individually approvable; approving an archive moves the
      folder to `.archive/` and nothing is deleted. Restoring it
      is a move back plus a ledger update.
- [ ] **30-day review** (due: 30 days after shadow lifts):
      acceptance rate (bar: at least half of staged items approved
      or edited), false-stale count (an archive restored within 7
      days counts as one), restage rate, and queue load are
      reported to the user, who decides: keep, tighten the rubric,
      or drop the module.
