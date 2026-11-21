# Rehearsals

The kit's claim is "done means verified." This ledger is where
that claim is cashed: every rehearsal a fresh agent has run
against the kit, what it covered, and what it found. A module with
no row here is **unrehearsed**, and the wizard says so at selection
time ("unrehearsed at this pin — you would be the first"), from
the manifest's `rehearsed_at` field, which this ledger backs.

Kept honestly, including the gaps. Early runs predate this ledger
and did not record per-module check counts; those rows say what is
known and no more.

| # | Date | Kit state | Shape | Modules installed | At-install checks | Findings |
|---|---|---|---|---|---|---|
| 1 | 2026-11-20 | pre-v0.1 tree | Solo user, no second person, no host, no other agents; wizard end to end into a sandbox | Core set (00, 01, 02, 06 exercised; 03, 04, 07 withheld by gating). Per-module list not recorded — the gap this ledger exists to close | Not recorded per module | 16 friction findings (3 high), all fixed in the hardening phase: module 06 gained its Install section, module 01 its fresh-store path and shipped linter, verification split into at-install vs deferred |
| 2 | 2026-11-20 | pre-v0.1 tree | Two-person household; modules 03–04 exercised end to end | 03, 04 (07 withheld) | Not recorded per module | 16 friction findings (3 high), all fixed: notebook writer-named sections, partner setup-prompt template + checkpoint, Exchange Work/ and Snapshots/, one canonical queue, linter exclusions so a textbook install lints quiet |
| 4 | 2026-11-20 | v0.4 candidate | Solo user (scripted persona), cold install from the README via the wizard, Starter profile | 00, 02, 09 | 00: 6/6; 02: 2/2 applicable; 09: 4/4 — no failures | 14 friction items, all fixed in v0.4 before tagging: the pin rule gains the EVALUATION exception; the brief template's memory lines are gated and its monthly step gains the spend check and a deferred-checks surfacing step; SCOPE.md's home, the VIP "none named yet" fill, the plan-time question round, and the file-based job artifact are now defined; module 09's register placement (§12) is marked in the procedures template |
| 3 | 2026-11-20 | v0.3 candidate | Module 08 installed via the UPGRADING path into a sandbox with 00+01 pre-installed; six invented skills | 08 | 6 of 7 passed | 16 friction items (F-01..F-16). The one failure was the kit's own job-matching rule (a job named for a skill's task was invisible as a reference); fixed and fixture-tested, but **not re-run** until run 5 |

| 5 | 2026-11-20 | v0.4 candidate | Module 08 re-run: run 3's setup replicated (00+01 pre-installed, six invented skills incl. the F-04 trap pair) via the UPGRADING path | 08 | 6 of 7 — check 5 (first-run exemptions) failed | The F-04 matcher was right in isolation but wired wrong: it received the ledger-so-far as its name list, so on a first run `tax` wrongly claimed the `tax-docs-prep` job before `tax-docs` existed in the ledger; a second run self-corrected. Fixed (the matcher now receives every skill on disk), covered by a new first-run regression fixture, and the run's diagnostic evidence is in the sandbox log. Also fixed from this run: ledger seeding is defined as the hand run itself, VERIFY names `staged/expired/`, JOBS.md gains a Planned section, and the EVALUATION dirty-state form is specified |

## What has never been rehearsed (as of v0.4)

- A fresh **full** install (all nine modules) at any single pin.
- The wizard on a **small-group (Q1c)** interview.
- A module 05 **install** (its method — blind dual review — has
  been run against the kit itself four times; the install path
  has not).
- An **uninstall** of any profile.
- A real **upgrade** of an existing install to a new pin
  (run 3 rehearsed the upgrade *path* for one module's install;
  no install has yet been carried across pins).
