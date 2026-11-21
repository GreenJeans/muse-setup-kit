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

## Phase 5 — v0.3: adversarial-review fixes + module 09 — DONE 2026-11-20

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

## Phase 6 — v0.4: prove it, then make it easy — DONE 2026-11-20

Driven by a blind roadmap brainstorm (two outside models, same
packet method; their wild ideas converged on the Governance Test).
Adopted: the four verified defect fixes (kit_doctor reads every
pin, not the first; JOBS.md gains a canonical template both tools
parse; module 09 ships the bucket-register template it always
improvised; module 07's missing rehearsal is named, not implied);
docs/REHEARSALS.md, the rehearsal ledger, with `rehearsed_at`
labels in the manifest and the wizard stating rehearsal status at
selection time; tools/kit_selfcheck.py plus tool regression
fixtures in CI (the fixtures caught a real bug on their first run:
the curator's unseeded report was unreachable in both the kit and
the maintainer's live copy — fixed in both); starter profiles with
printed audit word counts; module 07 demoted to
docs/patterns/infra-patterns.md; the Governance Test
(docs/governance-test.md) as a standalone companion; release-notes
automation that drafts the release with the pin pre-filled.
Rehearsals for this release are recorded in docs/REHEARSALS.md
(rows 4–5). Held for v0.5: the module 08 restructure, the
installed-file upgrade baseline, UNINSTALL.md, install reports,
audit-first wizard mode, the full worked example.

## Ideas parking lot

- A "diff my setup" tool: compare an existing installation against the kit
  and report which patterns are present, missing, or drifted.
- Worked example (fully fictional) of a filled-in memory store and brief, so
  adopters can see the target state without any real data.
- Localization of the templates.

## Phase 7 — v0.5: the first stranger — DONE 2026-11-20

From the v0.4 synthesis's held list, in the order the lineup
adopted: module 08 restructured into tiers (Lite default, Full at
5+ skills); the installed-file baseline (hash lines in
SETUP-PLAN.md; accumulating files inventoried, never diffed) with
kit_doctor reporting edits since install; UNINSTALL.md, rehearsed;
the worked example in docs/examples/, generated from that
rehearsal's artifacts; the install-report issue form; and
audit-first wizard mode (Step 0, read-only). Three rehearsals
(runs 6–8 in docs/REHEARSALS.md): a Lite install, a cross-pin
upgrade whose planted edit the doctor caught exactly, and an
install → uninstall that left the workspace empty. Removal this
release: the README's Status narrative, which duplicated this
file's history, is now a pointer here.

## Phase 8 — v0.6: capability profiles + constitutional dedup — DONE 2026-11-20

The two remaining candidates from the roadmap brainstorm:
`docs/capability-profiles.md`, the matrix of what each platform
capability buys each module (required / degrades / unaffected),
generated from the manifest's `requires` and `degrades_without`
fields; and the constitutional-rule dedup — module 00 gained the
canonical-location table naming the one operative section per
rule, governing-text pointers were added where summaries live,
and the wizard's gating prose points at the matrix instead of
duplicating it. Rehearsal run 9 scored the matrix blind against
the manifest (27/27 cells, 26/27 verdicts; the misses fixed in
the release). Merged via PR #5.

## Phase 9 — v0.7: just paste it — DONE 2026-11-20

The quickstart became one sentence with nothing to substitute:
the wizard's pinned-source rule gained a tag-entry path — a
checkout sitting exactly on a release tag is a valid entry, and
the wizard resolves the full commit hash itself and states it in
the plan. (A user-supplied hash is still verified exactly, and a
checkout on no tag with no hash still stops.) Release-notes
automation prints the short prompt with the tag filled in;
UPGRADING.md names releases by tag. Rehearsal run 10 ran the new
prompt cold and reached a complete Starter plan; the same run
documents the released v0.6 wizard dead-stopping the new prompt
at the old rule. Merged via PR #6.

## Phase 10 — v0.8: vet the door — DONE 2026-11-20

Driven by the second blind dual review of the kit's direction
(the library brainstorm): both reviewers put the same item first
and demoted the maintainer's favorite, and the release follows
them. Module 06 gains the connector/MCP vetting pack (provenance
tiers, typosquat check, OAuth scope audit, tool-manifest hash
pinning with re-vet on change, walk-away criteria). Module 02
gains the money watch as an optional component (baseline from
user-supplied exports, never credentials). Module 00 gains the
sensitive-records rule (procedures §13), the continuity handover
template, and the extension-point anchor registry.
`docs/library.md` specifies the library design the next phases
implement. Repairs from the same round: the audit-word count now
covers every installed file (MODULE.md, VERIFY.md, templates,
tools) and the selfcheck asserts the README's figures equal the
manifest's; the memory linter gains the review-by check (check D)
its schema template always claimed; stale citations and the
REHEARSALS ledger are repaired. Rehearsals for the 06 pack and
the money watch are specified from the reviewers' pass bars and
run before tagging.

Review fixes (EX-018/019 — the blind dual review of this
release, run against the v0.8 tree before tagging): 39 distinct
findings, every one verified against the tree, the fixes in this
phase's tree. The scope audit now decides on the scopes as
observed at connection time (and audits token privilege where
there are no scopes); manifest pinning captures the presented
manifest in full — schemas, annotations, server instructions —
with a named capture method and a re-check cadence; money-watch
queue items can never resolve by silence; §13's review-by has a
surfacing path for local holdings, and the §13 pointers are
completed across modules 01, 04, 05, 08, and 09. Two findings
were maintainer decisions, since taken: a user may accept
excess scopes as a recorded decision — official tier only, in
their own words, naming each scope accepted — and an official
hosted connector whose source cannot be read is vetted on its
observable surface with the user's decision recorded, floored
by a full read of the presented manifest.

## Phase 11 — v0.9: everyday (this release)

The everyday release: modules for the user's own life rather than
the agent's machinery. Module 10, the deadlines & expiry register
— an accumulating register with per-item lead times and source
pointers, no raw ID numbers, surfacing through module 02's brief
(or a manual deferred check without one). It is the first module
designed under the library spec: its data class is declared in
its MODULE.md and its register's file class is named. Module 02
gains the promises & waiting-on ledger — verbatim quote plus
source as the record, overdue entries in the brief's Today
section, follow-ups as drafts under ticket rules — with the
return-window/refund tracker as its worked example. The
scam/impersonation shield joins module 02's triage, running
before the VIP interrupt rule, with a pointer from module 06:
rule 3 turned outward. Module 10 was rehearsed once at the v0.9
candidate (run 13, at abb9f86); changed since, it is unrehearsed
at this pin and labeled that way. Further rehearsals (Standard
installs, ledger and shield fixture runs) are specified from the
reviewers' pass bars and run before the library phase builds on
it.

Review fixes (EX-020/021 — the blind dual review of this
release, run against the v0.9 tree before tagging): 29 distinct
findings, every one verified against the tree, the fixes in this
phase's tree. Shield flags now have a route into the brief (the
triage flag log, consumed in Failures, and the scan's own
silence is a brief-visible failure); procedures §13 states the
identifiers rule module 10 cites, with module 10 in its
applications; the ledger's grade system is one system across
MODULE, template, and VERIFY, with a `Grade:` marker on every
entry; the immediacy set records every known sender per
institution and is collected as a plan question; module 10's
deferred checks all carry event-plus-fallback due dates. One
finding was a maintainer decision, since taken: a message
graded "unverified sender" earns no interrupt of any class on
its sender claim alone — it is written to the flag log and
surfaces in the brief's Failures.

## Phase 12 — the library (implemented on the library branch, 2026-11-20 — unreleased)

Implemented on a branch off v0.9 — a branch, not a release, and
the latest release remains v0.9. What landed: `module.yaml` per
module replaces the manifest fragments (strict flat subset,
fail-loud parser in `tools/module_yaml.py`, MODULE.md header
parity asserted by the selfcheck, which also fails on any
per-module field left in the manifest); the manifest keeps the
library id, the interface version, and the profiles. Qualified
ids (`core/<module>`) throughout. `tools/build_directory.py`
generates `directory.json` + `advisories.json` in the core repo
from the module.yaml files and `advisories.yaml`. The wizard
gains a lifecycle section defining the named verbs (list
installed / available / upgradable, add/remove library,
suspend, narrowed repair, inspect, rollback, reconfigure,
audit), each with its reads, writes, and ticket rule; installed-
file baseline lines now name each static file's class, and
kit_doctor accepts classed and pre-class lines alike. The
selfcheck prints rehearsal staleness against each module's
`rehearsed_at` pin as an informational report, not a finding.
A home-operations field library pilots the package format from
a separate local repository — unpublished; it was installed
through the lifecycle verbs in rehearsal run 15. The EX-022/023
blind review of the branch and the maintainer's four decisions
landed as a fix pass (2026-11-21): packages no longer carry
review fields, the parser's scalar edge cases fail loud, parity
binds the class fields, catalog generation enforces its pin
discipline, advisories validate and are never fabricated,
baselines attribute their files to a module, brief blocks are
delimited by qualified id, and the selfcheck gained a
field-library mode. Held for the next phase: rehearsal of the
verbs run 15 did not exercise (upgrade, uninstall, rollback,
reconfigure, remove library) and of the post-run-15 fixes,
field libraries entering the index by reviewed PR, and the
merge/release decision, which is the maintainer's.
