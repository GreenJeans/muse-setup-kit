# Setup Plan — Robin (Starter profile) — EVALUATION

Status: PRESENTED → APPROVED as presented ("approve Starter: 00, 02, 09")
→ installing. Install log, verification ledger, and the installed-file
baseline are appended below as Step 5 proceeds.

**EVALUATION install.** This plan is labeled EVALUATION per wizard
ground rule 2 and UPGRADING.md step 1: the source is a local working
tree with uncommitted changes (branch `v0.5`, unreleased), handed to
the installer for a release-candidate rehearsal. A production install
never proceeds this way. Source state, recorded verbatim:

- HEAD: `bed2cfbeb0177c02c033426b595faa62c378a9fd`
- `git status --porcelain`:

```
 M UPGRADING.md
 M modules/05-evaluation-kit/tools/kit_doctor.py
 M modules/08-skill-lifecycle/MODULE.md
 M modules/08-skill-lifecycle/VERIFY.md
 M tools/tests/test_tools.py
 M wizard/SKILL.md
 M wizard/manifest.yaml
?? .github/ISSUE_TEMPLATE/
?? UNINSTALL.md
```

- `git diff --stat HEAD`:

```
 UPGRADING.md                                  |  11 +-
 modules/05-evaluation-kit/tools/kit_doctor.py |  28 +++++
 modules/08-skill-lifecycle/MODULE.md          | 152 ++++++++++++++++----------
 modules/08-skill-lifecycle/VERIFY.md          | 121 +++++++++++---------
 tools/tests/test_tools.py                     |  35 +++++++
 wizard/SKILL.md                               |  44 +++++++-
 wizard/manifest.yaml                          |  15 ++-
 7 files changed, 287 insertions(+), 119 deletions(-)
```

Note: `UNINSTALL.md` — the document the uninstall phase of this
rehearsal follows — is itself untracked (`??`) in this tree; it is
part of the EVALUATION source state above, not of any release.

**Libraries configured:** core only (this repository). Modules
carry qualified ids (`core/<module>`) throughout this plan.
**Pins:** per module, the checkout pin is the EVALUATION tree
above (HEAD `bed2cfbeb0177c02c033426b595faa62c378a9fd` + the
recorded dirty state); the catalog pin is *none* — the source
tree carried no generated catalog, so the listing verbs do not
speak for this install, and no baseline line here is repairable
(an EVALUATION install is never repair's object).

## 1. Vetting entry (kit) — plan item 1, approved with the plan

- **What:** Muse Setup Kit (wizard + modules core/core-procedures,
  core/morning-brief, core/cost-guardrails for this install). Source: the kit repository, local checkout, branch `v0.5`
  working tree at HEAD bed2cfb (see EVALUATION note above).
- **Read in full by the installing agent:** wizard/SKILL.md,
  wizard/manifest.yaml, docs/DESIGN.md, docs/REHEARSALS.md,
  UPGRADING.md, UNINSTALL.md, and for each selected module its
  MODULE.md and VERIFY.md, plus every template rendered from
  (module 00: OPERATING_PROCEDURES, decision-queue, SCOPE, JOBS;
  module 02: brief.template.md; module 09: bucket-register).
- **Reads (selected modules, per module.yaml):** Robin's existing agent
  instructions and workspace layout (00); calendar, mailbox, task
  lists, watch outputs — whatever is connected (02); model/provider
  usage and billing pages, with Robin present (09).
- **Writes:** an OPERATING_PROCEDURES.md, a decision queue file,
  SCOPE.md files per workstream (00); one brief message per day,
  draft replies only, sent only with approval (02); a bucket register
  in the procedures, spend-check entries in the decision queue when a
  cap is approached (09).
- **Network:** none (00); Robin's connected accounts only (02);
  providers' billing pages only, with Robin present (09).
- **Jobs created:** daily morning brief; monthly spend check riding
  it (02, 09).
- **Third-party software installed by the kit:** none. The Starter
  modules ship no scripts.

## 2. Externally visible items

None. No shares or invites, no account connections, no job that
messages anyone but Robin (the brief delivers to Robin's own main
chat). Nothing leaves Robin's workspace.

## 3. Capability check (wizard Step 1)

- Scheduling: yes → `scheduling`
- Mailbox: connected. Calendar: connected. Task app: none.
- Cloud storage with sharing: not connected (not needed by Starter)
- Host the user controls: no
- Second participating person: no
- Other AI agents: no
- Shell / Python 3: yes → `shell-python`
- **Billing bucket for this session: Muse subscription** (Robin
  confirmed; wizard Step 1 stop condition satisfied — the bucket is
  named, per module 09's rule 2 applied to the kit itself)

Step 0 (audit-first) was offered and declined: Robin has no existing
setup to inventory — this is a fresh workspace.

## 4. Interview answers (wizard Step 2)

1. Who: (a) Just me.
2. Autonomy: (b) reversible work on its own; irreversible actions
   need approval each time → §2 installs as written.
3. Rhythm: (a) a morning brief. Triage scan: **not installed**
   (recorded explicitly, per wizard Step 4).
4. Other agents: (b) Not now.
5. Memory: (c) Leave my memory alone → ai-exchange, evaluation-kit,
   and skill-lifecycle are **not offerable** (they depend on the
   memory schema); said plainly at selection.
6. Infrastructure: (b) Cloud only. (No module gates on this; noted
   per the wizard.)
7. Existing work: one workstream, "Freelance projects". No existing
   main instruction file → install creates `INSTRUCTIONS.md`.

## 5. Selection (wizard Step 3)

Profiles offered first: **Starter** (00 + 02 + 09, audit cost
~5,100 words), then Standard (~7,100). Robin took Starter — the
sensible default for a first install. Modules can be added later,
one at a time (UPGRADING.md).

Rehearsal status, stated at selection (each module.yaml's
`rehearsed_at`, backed by docs/REHEARSALS.md):

- core/core-procedures — rehearsed: "v0.1 wizard dry runs"
- core/morning-brief — rehearsed: "v0.1 wizard dry runs"
- core/cost-guardrails — rehearsed: "v0.4 Starter dry run"

Not offerable for Robin: 03 household-hq (no second person, no
shared docs/tasks), 04 ai-exchange (no shared storage, no other
agents, memory left alone), 05 evaluation-kit and 08 skill-lifecycle
(memory left alone). Offerable but not selected: 01
memory-architecture, 06 security-pack (both are in Standard; addable
later).

Optional components, decided explicitly: module 02's triage scan —
**not installed**. Watches — none exist and none are created by
Starter. Module 03's food layer and change detector — not applicable
(module not offerable).

## 6. Placeholder answers (collected before approval)

- User name: **Robin**
- Agent name: **Muse** (supplied at plan time, per wizard Step 4)
- Timezone: **America/Los_Angeles**
- Brief time: **07:30** local
- VIP / interrupt-lane people: **None named yet** — an empty lane is
  a legitimate fill; the interrupt rules bind the brief only, since
  triage is not installed
- Decision queue path: `decision-queue.md` (workspace root)
- Main instruction file: `INSTRUCTIONS.md` (created by this install)
- SCOPE contents for Freelance projects: drafted with Robin and
  approved as part of this plan

## 7. Files and jobs, in dependency order

### Module core/core-procedures
- Create `OPERATING_PROCEDURES.md` from
  `templates/OPERATING_PROCEDURES.template.md`, Local configuration
  filled from §6; template comments deleted per the template's own
  instruction; §2 as written (autonomy answer (b)). §6 stays inert
  (module 01 not installed; the template's applicability note says
  so). The §12 marker comment stays until module 09 appends §12.
- Create `decision-queue.md` from
  `templates/decision-queue.template.md` (example item is a comment;
  first real item will be #1).
- Create `freelance-projects/SCOPE.md` from
  `templates/SCOPE.template.md`, in the workstream's home folder
  `freelance-projects/` (created by this install; the plan names
  each home, per module 00 Install step 4).
- Create `INSTRUCTIONS.md` carrying the pointer line: "Operating
  procedures live in OPERATING_PROCEDURES.md and govern daily work."
  It also carries ground rule 8's line — "At session start, check
  SETUP-PLAN.md for overdue deferred checks." — because whether a
  file-based brief job will actually run is unclear in this
  workspace; the rule calls the line harmless when a brief also
  surfaces them (see FRICTION F-01).
- Create `JOBS.md` from `templates/JOBS.template.md` (canonical
  format, no jobs yet).
- Jobs: none. Network: none.
- Disclosure (module.yaml): reads Robin's existing agent instructions
  and workspace layout (to merge, not overwrite); writes an
  OPERATING_PROCEDURES.md, a decision queue file, SCOPE.md files per
  workstream; network none; jobs none.

### Module core/morning-brief
- Create `jobs/morning-brief.md`: the brief job's instructions,
  adapted from `brief.template.md` — daily 07:30
  America/Los_Angeles, delivered to the main chat. Adaptations:
  calendar and mailbox source lines active (both connected, markers
  kept); task-app, household-hq, ai-exchange, and watches source
  lines dropped (conditions don't hold); Step 0 items (d) and (e)
  dropped (no shared lists); Step 6 stays gated `[IF
  memory-architecture installed]` and is inert; Step 7's spend-check
  line stays gated `[IF cost-guardrails installed]` and is live
  (module 09 is in this plan).
- Create the job: file-based workspace, so the job is the pair
  `jobs/morning-brief.md` + its `JOBS.md` entry (wizard Step 5
  item 3).
- VIP list / interrupt rules: as in §6 (no VIPs named). Triage scan:
  not installed.
- Jobs: `morning-brief` (daily). Network: Robin's connected
  accounts only.
- Disclosure (module.yaml): reads calendar, mailbox, task lists, watch
  outputs (whatever Robin connects); writes one brief message per
  day, draft replies only; network Robin's connected accounts only;
  jobs: one daily brief, optional triage (declined).

### Module core/cost-guardrails
- Append §12 "Cost & billing guardrails" to
  `OPERATING_PROCEDURES.md` at the template's marker: rule 2
  (declare-before-heavy-work) and the bucket register built from
  `templates/bucket-register.template.md`, including the template's
  heavy-run declaration snippet.
- Register content (built with Robin): one surface — this agent
  (Muse), bucket: subscription; hard cap: "none — deliberate"
  (a subscription has no per-token billing to cap; recorded as the
  register's own wording for a cap-less surface); usage page: the
  provider's subscription usage page; key scope: n/a; last verified
  2026-11-20. No API keys, orgs, routers, or local models are
  reachable, so no UNKNOWN rows and no caps to set (module 09
  Install step 2 satisfied vacuously — no uncapped API surface
  exists).
- Record `spend-check` in `JOBS.md` as its own bullet, marked
  "(rides morning-brief)", in the canonical shape the JOBS template
  gives as its example.
- Jobs: `spend-check` (monthly on the 1st, rides morning-brief).
  Network: billing pages only, with Robin present.
- Disclosure (module.yaml): reads model/provider usage and billing
  pages (with Robin present) and the plan's bucket register; writes
  a bucket register in the procedures and queue entries when a cap
  is approached; network providers' billing pages only, with Robin
  present; jobs: one monthly spend check (rides the brief).

## 8. Conflicts with existing setup

None — the workspace was empty. Nothing to merge or overwrite.

---

## Install log (Step 5)

Installed 2026-11-20, in dependency order: 00, 02, 09. Source for
every file: the EVALUATION tree named at the top of this plan (HEAD
bed2cfbeb0177c02c033426b595faa62c378a9fd + the recorded dirty state).

- **core/core-procedures** — files created as listed in §7; §2 as
  written (autonomy (b)); JOBS.md created empty of jobs. Baseline
  stamped for all five files.
- **core/morning-brief** — job pair created (`jobs/morning-brief.md` +
  `JOBS.md` entry); triage not installed. Baseline stamped for the
  job file; JOBS.md is baselined `accumulating` — it grows by
  design and is never re-stamped.
- **core/cost-guardrails** — §12 appended to OPERATING_PROCEDURES.md at
  the template marker (rule 2 + register + declaration snippet);
  `spend-check` bullet added to JOBS.md. OPERATING_PROCEDURES.md
  re-stamped after its edit (wizard Step 5 item 5: the baseline
  always describes the last approved state); JOBS.md stays
  `accumulating`.

## Verification ledger — deferred checks

Owner for all: Robin (surfaced by the brief's Step 0(f) via this
plan, and by the session-start line in INSTRUCTIONS.md).

| Module | Deferred check | Due | Status |
|---|---|---|---|
| core/core-procedures | Fresh-session test ("What needs a ticket?") | Robin's next new conversation | DEFERRED |
| core/core-procedures | Queue drill (test item numbered, clears by number) | First brief or first on-demand review | DONE 2026-11-20 — item 1 was planted, printed in full in briefs/brief-2026-11-20.md, and cleared by Robin's reply "1: yes"; it sits in the queue's Resolved section with its number kept |
| core/morning-brief | First brief (arrives on time, failures first, queue numbered) | 2026-11-21 07:30 | DEFERRED — an on-demand instance was generated 2026-11-20 as a worked example; scheduled arrival itself is unverifiable in a file-based workspace with no live scheduler |
| core/morning-brief | Interrupt test | First week | NOT APPLICABLE — triage not installed |
| core/morning-brief | Detector-silence drill | First month | NOT APPLICABLE — no watches exist |
| core/cost-guardrails | First spend check (usage vs register and caps; surprises to the queue) | 2026-12-20 (30 days after install) | DEFERRED |
| core/cost-guardrails | Bucket-declaration sample (with the first spend check) | 2026-12-20 | DEFERRED |

## Verification results (at-install, run 2026-11-20)

**Module 00 — 6/6 at-install checks passed**
- OPERATING_PROCEDURES.md exists; Local configuration filled;
  placeholder scan (`<[A-Z]` tokens): 0 remain.
- §2 carries the ticket rule as written = autonomy answer (b).
- decision-queue.md exists; the template's example item is an HTML
  comment; numbered items: 0 (first real item will be #1).
- freelance-projects/SCOPE.md: all five fields present (grep: 5/5),
  plus a `## Closed` section.
- INSTRUCTIONS.md carries the pointer line verbatim (grep: 1).
- JOBS.md built from the module's JOBS template, canonical entry
  format, empty of jobs at module 00's install.

**Module 02 — 2/2 applicable at-install checks passed**
- Brief job exists: `jobs/morning-brief.md` states daily 07:30
  America/Los_Angeles, delivery to the main chat; `JOBS.md` carries
  its canonical entry.
- Brief instructions name every source for this install (decision
  queue, calendar, mailbox, gated memory line), mark conditional
  blocks `[IF ...]` (6 markers), and carry the rule that an unread
  source is reported as unread — never as clear.
- Triage check: not applicable — triage was not installed.

**Module 09 — 4/4 at-install checks passed**
- Bucket register exists in OPERATING_PROCEDURES.md §12, built from
  the module's template; it lists every surface the agent can reach
  (one: Muse, subscription). No surface is unclassifiable, so no
  UNKNOWN row is owed and none is missing (grep UNKNOWN: 0).
- API keys/orgs in the register: none exist, so the cap check is
  satisfied vacuously — there is no uncapped API surface.
- Declare-before-heavy-work rule present in §12 (grep: 1).
- `spend-check` recorded in JOBS.md as its own bullet, marked
  "(rides morning-brief)".

## Installed files (baseline)

Stamped per wizard Step 5 item 5 — every file this install created
or copied from the kit, at its last approved state:

- installed: OPERATING_PROCEDURES.md sha256:ae60268d4ea687de73031bd9e73d6a4a7f873b10e1c96753326e2fbf42191325 static-rendered core/core-procedures
- installed: decision-queue.md accumulating core/core-procedures
- installed: freelance-projects/SCOPE.md sha256:924f04d778492a2e81f87660686a9e9cc11d68726b1c9f7c5a82ba9cc92d2146 static-rendered core/core-procedures
- installed: INSTRUCTIONS.md accumulating core/core-procedures
- installed: JOBS.md accumulating core/core-procedures
- installed: jobs/morning-brief.md sha256:fe04f4f756638b4570bac0e1242c26c81aa5a6688d54f0de95de5d4d7c21bb13 static-rendered core/morning-brief
