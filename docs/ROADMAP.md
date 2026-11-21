# Roadmap

## Phase 1 — scaffold (the scaffold commit)

- Repo skeleton, README, design notes.
- Wizard skill + module manifest.
- Modules 00–04 distilled with templates; 05–07 as full method outlines.
- Scrub pass: no instance data anywhere (grep-verified against a denylist
  kept *outside* this repo).

## Phase 2 — hardening (completed 2026-11-20)

- Dry run executed: a fresh, memory-free agent persona (solo user, no
  second person, no host, no other agents) ran the wizard end to end into
  a sandbox. Gating was correct (household-hq, ai-exchange, and
  infra-patterns withheld), the leak check passed, and the run produced
  16 friction findings (3 high, 5 medium, 8 low), all fixed in this
  phase: module 06 gained an Install section and a vetting-log template;
  module 01 gained a fresh-store install path, a memory template, and a
  shipped reference linter; verification is now split at-install vs.
  deferred with a ledger in the plan; the procedures template gained a
  Local configuration section; the brief template marks conditional
  blocks; the wizard gained a capability→token mapping, a workstreams
  question, and degraded-mode offers; the fidelity plant now lives on an
  excluded test page, reconciling it with the schema's truthfulness rule.
- `VERIFY.md` added per module: at-install and deferred checks (the kit's
  own "done means verified" rule, applied to itself).
- Second dry run (same day): a two-person household persona exercised
  modules 03–04 end to end — notebook cross-note surfaced in the
  partner's brief, Exchange canary round-tripped, and a blind dual
  review converged while ingest rejected one reviewer's confident
  misreading with the verbatim text. Gating correct again (only
  infra-patterns withheld); leak check passed. Its 16 findings
  (3 high, 6 medium, 7 low) are fixed: notebook sections are named for
  their writer ("From <AGENT>"); a partner setup-prompt template ships
  with a partner-review checkpoint in the wizard; the brief template
  gained the notebook source block and module 03 now amends the brief
  at install; the Exchange gained `Work/` and `Snapshots/` with ingest
  memos, one canonical 13-column queue (with Group), and the canary as
  an at-install check; the linter learned exclusions and a one-direction
  jobs check, so a textbook install can lint quiet.

## Phase 3 — publication — DONE 2026-11-20

- Final scrub + license review: done (denylist-verified; MIT).
- Published as a public git repository:
  https://github.com/GreenJeans/muse-setup-kit — tagged **v0.1**
  (commit 171781064ce1fddde4f97478adebb0500953a39b).
- Optional: submit the wizard to community skill directories, following the
  kit's own verify-before-install discipline in reverse — publish the pinned
  commit hash alongside any listing.

## Phase 5 — v0.3: adversarial-review fixes + module 09 (this release)

Blind dual review of the v0.2 kit (two outside models, identical
packet, one planted canary — both caught it) produced 36 findings.
The convergent set is fixed here: the quickstart pin is real (the
wizard refuses a hashless install); module 08 escalates by effect,
binds approval to the diff's hash, and gives its shadow week a pass
bar and its staging expiry a runner; the curator matches job
references by job name (longest match wins) instead of substrings
and anchors dateless records instead of immortalizing them; the
memory linter no longer flags a textbook install; module 00 creates
the JOBS.md its VERIFY checks for; module 05 gained the Install
section it never had, a fictional-seed library, and a drift checker;
module 04's outputs are actually polled; module 03 shares nothing
before the partner checkpoint; the manifest declares scheduling and
shell/python degradation honestly. Module 09 (cost & billing
guardrails) is new, and UPGRADING.md covers pinned updates. Module
08 was rehearsed before tagging: a fresh agent installed it via the
upgrade path in a sandbox (6 of 7 at-install checks passed; the one
failure was the kit's own job-matching rule, fixed above). Not yet
rehearsed: a fresh full install including module 09, and the wizard
on a small-group (Q1c) interview.

## Phase 4 — Module 08: Skill Lifecycle — DONE 2026-11-20

- Module 08 added via PR #1 (merged the same day it opened): a
  session-review rubric that stages skill lessons instead of writing
  them live, staged-diff approval through the decision queue
  (`[type: skill-write]` / `[type: skill-curator]`, base-hash voiding,
  14-day staging expiry), and a deterministic curator (stale 14d,
  archive candidate 30d, never deletes) — adapted from Hermes Agent
  with the gates-on divergence, plus a shadow-week rollout. Ships the
  staged-proposal and queue-item templates and a reference curator
  script (fixture-tested).
- Manifest, README (module table, layout, attribution), and the
  wizard's gating list updated in the same PR.
- Tagged **v0.2** at the merge commit
  (7e15e075b3873e019357f9fddde0df8c7a80478e).

## Ideas parking lot

- A "diff my setup" tool: compare an existing installation against the kit
  and report which patterns are present, missing, or drifted.
- Worked example (fully fictional) of a filled-in memory store and brief, so
  adopters can see the target state without any real data.
- Localization of the templates.
