# Roadmap

## Phase 1 — scaffold (this commit)

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

## Phase 3 — publication (separate decision)

- Final scrub + license review.
- Publish as a public git repository; tag v0.1.0.
- Optional: submit the wizard to community skill directories, following the
  kit's own verify-before-install discipline in reverse — publish the pinned
  commit hash alongside any listing.

## Ideas parking lot

- A "diff my setup" tool: compare an existing installation against the kit
  and report which patterns are present, missing, or drifted.
- Worked example (fully fictional) of a filled-in memory store and brief, so
  adopters can see the target state without any real data.
- Localization of the templates.
