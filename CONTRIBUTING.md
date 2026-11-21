# Contributing to the Muse Setup Kit

Contributions are welcome. They are also read carefully, in
full, before anything merges. That is not a barrier. It is the
same rule the kit applies to everything else: nothing lands
unread.

The ways to contribute, ranked by value to the project:

## 1. Rehearsal reports

The most useful contribution there is. A rehearsal is a fresh
agent installing a module at a pinned commit in a sandbox,
under an invented persona, and recording what happened: the
shape of the install, at-install pass/fail counts, and the
friction it hit. The format is `docs/REHEARSALS.md`; a report
that matches that shape can be pasted into an issue or sent as
a pull request adding a row.

How to run one:

1. Pick the pin: the full commit hash of a release tag, or of
   a branch for lifecycle work. A rehearsal is of a pin, not
   of a branch name.
2. Start a fresh agent session in an empty workspace, with no
   access to real accounts, mail, or files. That isolation is
   the shape the kit's own evaluation runs used (runs 11 to
   15 in the ledger).
3. Invent the persona first: who they are, what they run, what
   they would plausibly ask for. Write it down before the run
   starts.
4. Paste the README quickstart with the exact pin, and let
   the agent work.
5. Record, per module, the at-install pass/fail counts, and
   every hesitation, guess, or question the agent had.
   Friction is the data; a clean run with no friction notes
   is a run nobody believes.
6. Note the billing bucket the run drew on, and its rough
   cost.
7. Scrub the report (see the ground rules), then file it.

A contributed run is recorded as adopter-reported, with its
evidence (a scrubbed transcript or sandbox log) linked from
the report. It backs a module's `rehearsed_at` only after the
maintainer has read that evidence.

Rehearsals find what authors cannot see in their own text.
Most of what changed in this kit's early releases came from
them.

**Standing wanted run:** the repair verb's restore path has
never been rehearsed. The one repair drill so far (run 15)
ran against installs holding no static-verbatim file, so
repair correctly restored nothing, and its class gates were
exercised while the restore itself was not. A run that
installs a module with a static-verbatim file, deletes that
file, and repairs it at the recorded checkout pin closes a
named gap in the ledger.

## 2. Install reports

Installed the kit, or tried to? The install-report issue form
asks a short, fixed set of questions: profile, modules, what
passed, what did not. A report from a setup that failed is
worth as much as one that sailed through. File it even if you
fixed the problem yourself; the friction is the data.

## 3. Field modules and field libraries

This is the real door. The kit is a library, not a single
product: core modules live in this repository, and anyone can
publish a **field library**, their own repository of modules
in the same package format, under their own maintainer.

Field libraries are new. One pilot, written by the core
maintainer, has proved the format. No outside library has
been onboarded yet. If you start one, you are the first real
test: expect to work through it with the maintainer, and
expect the rules to get fixes from what you hit.

The full spec is `docs/library.md`. The short version:

- A package is a directory: `MODULE.md` with the
  Reads/Writes/Network/Jobs header, `VERIFY.md`, templates and
  tools as needed, and a `module.yaml`, the single authored
  metadata source, in a strict flat subset of YAML that fails
  loud on anything outside it.
- Modules carry qualified ids (`<library>/<module>`), a named
  maintainer (a person or agent, not a library and not an org
  label), and a license.
- Every installed file is declared in `module.yaml` with its
  class: static-verbatim, static-rendered, or accumulating.
  Data classes and action classes are declared too, judged by
  effect, not file type.
- `module.yaml` also carries `kit_compat` and `rehearsed_at`.
  Its `audit_words` figure is computed by the tooling on the
  all-files basis, never hand-written; a hand-written figure
  would flow straight into the generated catalog.
- Field modules amend core files only at declared anchors.
  Nothing writes outside its anchor.

The gates that apply to any module, core or field:

- **Reading cost.** Budgets bind per profile, counted on the
  all-files basis, never the library total. Per-module
  figures are printed at selection time as disclosure; no
  per-module budget is set. The printed figure is a cost
  disclosure, not a promise that a human read every word.
- **Rehearsal at a pin.** A module is rehearsed only if a
  fresh agent installed it at that commit and the run is
  recorded. Unrehearsed modules cannot enter the default
  profiles and are labeled at selection time. If the module
  changed after the run, the honest label is "rehearsed at
  <tag>; changed since." Profiles need their own install
  rehearsals, because cross-module amendments are where
  breakage lives.
- **Named maintainer.** Someone reachable, who answers
  issues. The staleness signals are rehearsal staleness,
  unanswered issues, and a maintainer who cannot be reached,
  not an idle timer: a stable module is not a decaying one.
  *Archived* is a catalog label that `list upgradable` and
  `audit` surface; it never reaches into anyone's install.
- **Risk class.** Two bars, kept separate. The evidence bar
  binds on data: a module holding financial, health, or
  third-party data needs two install rehearsals, one
  including a leak check in the shape of module 03's boundary
  test, and must comply with the sensitive-records rule
  (procedures §13), whether or not it sits in a default
  profile. The profile bar binds on outward action: a module
  whose declared actions are outward-acting — send/file/
  spend/delete/contact directed at third parties or external
  systems — cannot enter a default profile. A send whose only
  recipient is the user (a module that delivers the user's
  own brief and reports to the user, module 02's shape) is
  not outward-acting and does not trip the profile bar; the
  module's data, if higher-class, still answers to the
  evidence bar.

Field modules never enter the default profiles; core is the
only library that can.

Vetting vocabulary matters here, because the three words are
three different claims:

- **Read in full**: someone read the whole package at the pin.
  This is the installer's duty, recorded in the installer's
  own vetting log. A catalog cannot confer it.
- **Rehearsed**: a run record exists, at a named hash, in the
  shape above.
- **Reviewed**: a named human, not the module's author, read
  it in full at a pinned hash and attested to it: the full
  read with the per-file hash list, scripts read line by
  line, declared reads/writes/network/jobs checked against
  what the package actually does, the scrub rule checked, the
  license checked. An agent may prepare a review record; only
  a named human signs it. Review is conferred, never
  self-asserted: packages carry no review fields, and a
  maintainer never marks their own work reviewed. Review
  lapses on any change of hash.

The field author's starting kit:

- Run `tools/kit_selfcheck.py --field <your-library-id>`
  against your checkout before publishing. It runs the same
  package checks the core library runs on itself.
- Generate your catalog with `tools/build_directory.py
  --repo <checkout> --library <id>`, from a clean tree at its
  HEAD.
- Minimum layout: one directory per module, holding
  `module.yaml`, `MODULE.md`, `VERIFY.md`, and templates or
  tools as needed. A field library ships no wizard and no
  manifest of its own.
- The sensitive-records rule (§13) lives in
  `modules/00-core-procedures/templates/OPERATING_PROCEDURES.template.md`;
  the leak check's shape lives in `modules/03-household-hq/`.
- Pick the library id with care: it prefixes every module id
  you publish, and `core/` is reserved.

For a field module, the review record lives in the
reviewer's own vetting log. It does not travel with the
library, and there is no shared field review list yet.

`docs/wanted-modules.md` lists modules the project would like
to see built. `docs/known-libraries.md` explains how a field
library gets onto the discovery list.

## 4. Patterns

`docs/patterns/` holds reference practice that is not
installed: sound, written down, never rehearsed as an
install. A pattern from your own running setup belongs there
if it is useful and does not need the wizard to install it.
Patterns are prose. Keep them scrubbed (see the ground rules)
and say plainly what they assume. Merged patterns are
reference text the maintainer has read, not practice the kit
has tested. Each says who contributed it and what it assumes.

## 5. Fixes and documentation

Corrections, clarifications, and small fixes are welcome as
pull requests. One topic per pull request. If a change alters
what a module instructs an agent to do, say so in the
description; wording in this repository is behavior.

## What it costs

Reading: the profiles run about 24,200 words (Starter) and
31,300 (Standard), counted on the all-files basis. No
per-module word budget is set yet; each module's
`audit_words` is printed at selection time, and that printed
figure is the disclosure. Money: a rehearsal or an install
runs an agent, and the run draws on a billing bucket. Know
which bucket before a long run, and set a cap. Waiting: there
is one maintainer, everything is read in full, and
contributions are read in arrival order. There is no
response-time promise; a careful, slow answer is the deal.

## What happens after you submit

- **Rehearsal report:** the maintainer reads the report and
  its evidence. If it holds up, it becomes a row in
  `docs/REHEARSALS.md` and, where it covers the current pin,
  updates the module's `rehearsed_at`. Either way, you get a
  reply in the issue.
- **Install report:** read in full. The friction goes into
  the maintainer's fix list, and you get a reply saying what
  it changed or why it did not.
- **Listing pull request:** checked against the entry rules
  in `docs/known-libraries.md` (the entry, not your modules);
  merged, or answered with what does not check out.
- **Fix or pattern pull request:** read in full at the pin;
  merged, merged in part, or answered with the reason.

## Ground rules

- **Patterns travel, instance data never does.** No real
  names, addresses, account details, figures, or anyone's
  personal data in any contribution: not in code, not in
  templates, not in examples, not in a rehearsal report. The
  rule covers metadata too: file paths with usernames,
  hostnames, internal addresses, screenshots, agent
  transcripts (they capture tool output verbatim), and your
  own commit name and email. Personas are invented. Examples
  are fictional; fictional figures are fine, real ones are
  not. Scrub before you commit, and review the full diff
  before pushing or posting. A credential posted by mistake
  must be rotated: editing the post or force-pushing does
  not erase it.
- **No credentials, ever.** Not in a contribution, not in an
  issue, not in a screenshot. A contribution that needs a
  credential to make sense needs rethinking, not the
  credential.
- **Issues and pull requests are public on arrival.** The
  read-in-full promise covers merges, not posts: anything in
  an issue or a pull request is public the moment it lands,
  so a report from a real setup needs the same scrub as
  everything else. Security problems, and personal data or a
  credential found in any contribution, do not go in a public
  issue. Use the private channel named in `SECURITY.md`.
- **Everything is read in full before merge**, per item, at a
  pin. Approval of one version never covers the next. A large
  contribution may be read in parts and merged in parts.
- **License.** The kit is MIT. Contributions are accepted
  under the same license; by submitting, you confirm you
  have the right to contribute the material under MIT.
  Adapted material must come from a source whose license
  allows it in an MIT project, keeps its upstream
  attribution, and the module says where it came from.

Questions that are not bugs: open an issue anyway. A short,
honest "I tried this and got stuck here" is a contribution
too.
