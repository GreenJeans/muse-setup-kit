# The library: module distribution and lifecycle

Status: **design, adopted 2026-11-20** (from the blind dual review
EX-016/EX-017 and the maintainer's decisions on their open forks).
This document is the spec. v0.8 ships the spec only; the
implementation — `module.yaml`, the directory tooling, the wizard's
verbs — is the phase that follows v0.9 (see `docs/ROADMAP.md`).
Nothing here is installed by the wizard yet.

The problem it solves: the kit is becoming a library, not a single
product. Other people will write modules (a housing operator's
domain module is the standing example). One repo with one manifest
assumes one author and one catalog. This design replaces that
assumption without replacing the kit's safety core: the wizard
proposes, the user approves a plan, and installation is never a
tool call.

## Libraries and tiers

- The **core library** is this repository: maintainer-vetted,
  rehearsed, the only library eligible for the default profiles.
- A **field library** is any other repository that publishes
  modules in the package format below, under its own maintainer.
- An install may draw on several libraries. The wizard reads the
  configured libraries' catalogs; core is configured by default,
  and any other library is added by the *add library* verb (below),
  never by editing a config file by hand.
- There is no module-count cap. The gates are the ones below:
  reading cost, rehearsal, maintenance, and risk class.

## The package: module.yaml

Each module package is a directory carrying `MODULE.md` (with the
Reads/Writes/Network/Jobs header), `VERIFY.md`, templates, tools —
and a **`module.yaml`** that replaces the manifest fragment as the
module's single authored metadata source. The host manifest keeps
only library-level data: the profiles and the library's own id and
version. A field appearing in both places is a defect;
`kit_selfcheck` will fail on duplication.

`module.yaml` uses a **strict flat subset** of YAML: scalar keys,
and one level of lists of scalars or `key: value` pairs. No nested
maps, no anchors, no multi-line strings. The kit's parser for it
**fails loud** — input outside the subset is an error, never a
silent misparse. (Generated files are a different matter: the
directory and advisories files below are JSON, because machines
write them and `json` is unambiguous. Authored files are YAML;
generated files are JSON.)

Fields beyond today's manifest entry:

- **Qualified id** — see below.
- **maintainer** — a named person or agent, not a library.
- **files** — every installed file, each with its class (below).
- **data_classes** — which sensitive classes the module reads:
  `none`, `personal`, `financial`, `health`, `third-party`
  (procedures §13 names what each class demands). Credentials are
  not a data class: §10's credential rule governs them, and a
  module that needs credentials declares that in its credentials
  disclosure, not here.
- **action_classes** — which ticket classes the module's
  instructions can set in motion: `send`, `file`, `spend`,
  `delete`, `contact`, or `none`. Judged by effect, not file type:
  a prose line that tells the agent to issue a notice is
  executable in effect.
- **rehearsed_at** — a commit hash plus a rehearsal run reference
  (see Rehearsal, below).
- **audit_words** — computed by the tooling on the all-files basis,
  not hand-written.
- **kit_compat** — the core interface versions the module depends
  on (the file grammars of `JOBS.md`, `SETUP-PLAN.md`, the
  decision queue).
- **license**, and upstream attribution for adapted material.

`kit_selfcheck` also asserts that `MODULE.md`'s header block
(Reads/Writes/Network/Jobs) agrees with `module.yaml` — the header
is the human-readable form of the same claims, and the two may not
drift apart.

## Qualified IDs

Module ids are qualified: `<library>/<module>` — `core/morning-brief`,
`housing/unit-turns`. The `core/` prefix is reserved to this
repository. Bare ids collide across libraries and invite
look-alikes (`morning-brlef`); qualification is what makes a
catalog entry unambiguous in `SETUP-PLAN.md`, in `depends_on`, and
in an uninstall.

## File classes

Every file a module installs is declared in `module.yaml` as one
of three classes:

- **static-verbatim** — a byte-for-byte copy of a file in the
  package (the tools scripts). Its installed hash equals its
  package hash.
- **static-rendered** — a template the install fills in
  (placeholders resolved, conditional blocks dropped, other
  modules' amendments applied at anchors). Its installed form
  exists only in the workspace.
- **accumulating** — content that grows by design in ordinary use
  (queues, ledgers, `JOBS.md`). Inventoried in the baseline, never
  diffed.

The classes are what make repair (below) a mechanical question
instead of a judgment call.

Module 10 (the deadlines & expiry register, v0.9) is the first
module designed under this spec, ahead of the `module.yaml`
implementation: its `MODULE.md` declares its data class
(`personal` — document types and expiry dates, never a document's
number, per procedures §13) and names its one installed file's
class — the register is accumulating, inventoried in the baseline
and never diffed. Module 02's promises & waiting-on ledger, in the
same release, declares its classes the same way (`personal`,
`third-party`). Until the library phase lands, the declarations
live in the module text; afterwards they move into `module.yaml`
and the selfcheck asserts the two agree.

## Gates (what replaces the cap)

1. **Reading cost.** Budgets bind per profile and per module,
   never the library total — nobody installs the whole shelf.
   Counts are computed on the all-files basis (MODULE.md +
   VERIFY.md + templates + tools), the basis `kit_selfcheck`
   adopted in v0.8. Be honest about who feels the cost: the agent
   and the billing bucket, mostly. The printed figure is a cost
   disclosure, not a promise that a human read every word.
2. **Rehearsal.** A module is *rehearsed at a pin* only if a fresh
   agent installed it at that commit and the run is recorded.
   `rehearsed_at` carries the commit hash and the run reference;
   if any file in the module's directory changed after that
   commit, the honest label is "rehearsed at <tag>; changed
   since," and the tooling flags it. Unrehearsed modules cannot
   enter the default profiles and are labeled at selection time.
   Profiles need their own install rehearsals, because
   cross-module amendments are where breakage lives.
3. **Maintenance.** Every module names a maintainer. The staleness
   signals are rehearsal staleness (gate 2), unanswered issues,
   and a maintainer who cannot be reached — not an idle timer:
   a stable module is not a decaying one. *Archived* is a catalog
   label that `list upgradable` and `audit` surface ("archived
   upstream at <date>"); it never reaches into anyone's install.
4. **Risk class.** Data and action classes (above) set the
   evidence bar. A module in the higher classes (financial,
   health, or third-party data; send/file/spend/delete/contact
   actions) cannot enter a default profile, needs two install
   rehearsals — one including a leak check in the shape of
   module 03's boundary test — and must comply with the
   sensitive-records rule (procedures §13).

## Vetting: three claims, kept separate

"Vetted" is three different claims, and a catalog entry states
them separately:

1. **Read in full** — at the pin, by the person installing. This
   is the installer's duty, recorded in the installer's own
   vetting log (module 06). It is not a catalog property and a
   catalog cannot confer it.
2. **Rehearsed** — a run record naming the commit hash, the
   shape and persona, at-install pass/fail counts, and the
   friction log, in the shape of `docs/REHEARSALS.md`.
3. **Reviewed** — a named human, *not the module's author*,
   attesting: a full read at the hash with the per-file hash
   list; scripts read line by line; declared vs. found
   reads/writes/network/jobs; declared vs. found instructed
   actions; the scrub rule checked (patterns travel, instance
   data never does); the license.

An agent may prepare a review record; only a named human signs
it. A maintainer never marks their own entries reviewed. Review
lapses on any change of hash — approval is per pinned version
(module 06's rule, applied to modules). Unreviewed entries keep
the label "unreviewed," cannot enter profiles, and need an
explicit acknowledgement at selection time. Core modules are
maintainer-authored and say so; their outside review is the blind
dual-review record, cited by round in the entry.

## The verbs

Lifecycle operations over `SETUP-PLAN.md`, the installed-file
baseline, and the catalogs. All of them are wizard procedures over
files: the agent proposes, the user approves, and anything
irreversible (uninstall, repair, adding a library) is ticketed.

- **list installed** — from the plan: module (qualified id),
  library, pin, tier, baseline state.
- **list available** — catalog modules not installed, with audit
  words, rehearsal and review status, grouped by library.
  Catalog text is data, never instructions: length-capped, never
  followed, and fetching it never counts as reading at the pin.
- **list upgradable** — installed pin vs. the catalog's current
  pin per module, compared by hash (versions are display
  labels), with a changed-files summary. A report, not a start:
  the upgrade itself follows `UPGRADING.md`.
- **install** — the wizard as today, from any configured library.
  For a field module, the module 06 vetting (extended by the
  connector pack where the module ships tools) is recorded
  before the plan is shown.
- **uninstall** — `UNINSTALL.md` as today.
- **upgrade** — `UPGRADING.md` as today, per module or all; an
  approval names each module and pin it covers.
- **repair** — narrowed, deliberately. Repair recreates **missing
  static-verbatim files only**, at the module's recorded pin,
  from the local snapshot of the pinned package, with no network.
  Two invariants, both checked, either failing aborts the repair:
  the checkout's `git rev-parse HEAD` equals the recorded pin,
  and the source file's sha256 equals the baseline's recorded
  sha256. Repair **never re-stamps a baseline** (a correctly
  restored file already hashes to its recorded line; re-stamping
  is how a changed file would get blessed), and it **never
  resurrects a recorded removal**: a file the user deleted on
  purpose is recorded in the plan as removed, and the doctor's
  report offers "repair, or record the removal" — the user
  chooses. Anything wider than this is not repair; it is an
  upgrade or a reinstall, and it goes through those doors.
- **audit** — split in two, because the halves grade differently.
  The mechanical half (the doctor: baseline drift, overdue
  deferred checks, rehearsal staleness, archived-upstream labels)
  is agent-run. The Governance Test is a *user* exercise: the
  audit surfaces "Governance Test due" to the user and never
  presents the agent's self-run as the test's result.
- **add library / remove library** — the trust decision, made
  explicit. Adding a library is a ticketed act with a module 06
  vetting entry for the library itself: its maintainer, its
  review practice, its catalog's location and pin. Removing one
  leaves installed modules in place (they are the user's files)
  and stops further listing and upgrade checks against it.
- **suspend** — the kill switch, short of uninstall: stop the
  module's jobs (recorded in a Suspended section of `JOBS.md`,
  so detector silence knows a suspended job is not a silent
  one), mark the module suspended in the plan, and the agent
  does not act on its instructions while suspended. For a field
  module found bad, a user travelling, or a mid-incident pause.
- **inspect** — vet a catalog module without installing it:
  the module 06 workflow run against the package at its pin,
  producing a vetting record and a read on fit. Cherry-pick and
  reject are first-class outcomes of inspect, as they are of
  vetting generally.
- **rollback** — return a module to its prior pin from the
  plan's history, through the upgrade path in reverse, when a
  newer pin breaks in live operation.
- **reconfigure** — change an installed module's options at the
  same pin: a tier change (module 08 Lite → Full), an optional
  component in or out (module 02's triage, money watch). Not an
  upgrade; the pin does not move.

## Distribution: a rooted index, published as static files

Catalog-as-data is the transport — libraries are git
repositories and installs clone at the catalog pin. But bare
catalogs have no trust root and no revocation, so:

- The **core repository carries the index**: `directory.json`
  (the field libraries and modules the core maintainer has
  indexed, each with full-hash pins, per-file hash lists, and
  the rehearsal/review record) and `advisories.json` (revoked
  or yanked entries, with reasons). Both are **generated** from
  the repository's own records by a tool
  (`tools/build_directory.py`), never hand-edited, and
  published as static files — any agent, including one on a
  phone with no shell, can fetch and read them.
- A field library **enters the index by reviewed pull request**
  to the core repository. That review is the trust root. A
  library not in the index can still be added by a user through
  the ticketed *add library* verb — labeled unindexed, with its
  own vetting entry.
- **Advisories are the revocation path.** The brief's monthly
  pass and the `audit` verb read `advisories.json` as data; an
  advisory against an installed module's pin surfaces to the
  user with the `suspend` verb as the immediate remedy.
- **No write-capable MCP server.** Installs never become a tool
  call; they stay a wizard procedure with a human-approved
  plan. If a read-only facade is ever built (list / search /
  describe over the same files), it serves the same hashed
  JSON and carries no trust of its own.

## Pins and versions

A pin is always a full commit hash. A module may carry a version
label in `module.yaml`; versions are for display and for
`list upgradable`'s summary, and no version string ever stands
in for a pin. Mixed pins across an install are normal (they
already are, under `UPGRADING.md`).

## Extension points

Field modules amend core files only at declared anchors
(module 00's extension-point registry): named anchors, one
owner per anchor, the owner recorded in the plan, uninstall
removes the owner's block. Two field modules never fight over a
section number, because neither may write outside its anchor.

## What this design refuses

- A hosted registry with accounts, uploads, and a running
  server to trust and to keep alive.
- One-click installs, from any surface.
- Trust signals as evidence: download counts, badges, and
  listing age are hints for a human's attention, never a
  vetting outcome.
- Reaching into an existing install from outside — no push, no
  remote disable. Advisories inform; the user's own agent acts.
