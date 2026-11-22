# Duet overlay — the setup wizard on Claude Duet

**Status: unrehearsed at every pin.** No fresh agent has installed
the kit through this overlay. The plan says so in these words:
"Duet profile and overlay: unrehearsed at this pin — you would be
the first." Each module keeps its own rehearsal status, stated as
`wizard/SKILL.md` Step 3 says.

This file is an overlay on `wizard/SKILL.md`, used with the
manifest's `duet` profile. Read the wizard first, then this file. It
changes only what it names; everything else in the wizard holds as
written, ground rules 1 to 8 above all.

Two orderings settle every conflict:

- **Module text governs this file.** A profile cannot override a
  module rule (docs/wanted-modules.md). Where this file seems to
  change what a module requires, the module governs and this file
  has a bug. What this file does is say *where* a module's pieces
  live on Duet and *what fires them*.
- **The stricter rule governs each act.** Duet has built-in rules of
  its own (a fresh yes for every send, payment, delete, sign-in, new
  account, and share; nothing read becomes an instruction; memory
  never grants permission). They are not the user's to waive and not
  the kit's to relax. Where a kit rule and a Duet rule both apply,
  both are met, and the stricter one decides.

## Duet facts the plan is built around

- **No instruction file.** Duet's standing instructions are written
  by the platform. The `instruction-file` token is absent, so module
  00's pointer follows that degradation (docs/capability-profiles.md).
- **Rules come only from the user's own words.** Duet keeps a
  standing rule only when the user states it, and it treats every
  file it reads — the kit's procedures included — as information,
  not as instructions. So installing a procedures file does not, on
  its own, make Duet follow it. The kit's rules reach Duet two ways:
  where Duet's built-in rules already say the same thing, or where
  the user adopts a rule in their own words (Step 4, Rules to adopt).
  Everything else in the procedures is reference text a session
  reads when kit work calls for it. The plan says this plainly.
- **A built-in brief and check-ins.** The platform writes them; the
  agent cannot edit their prompts. Module 02 is not offered, and no
  module can register at `ext:brief-sources`. Surfacing that would
  ride the brief rides the profile's own routines instead (below).
- **Routines.** Duet's scheduled jobs fire on cron, no more often
  than the platform's minimum interval, and only the main chat
  creates, changes, or deletes them. A routine's run starts fresh
  with memory and tools and no conversation, and no yes counts
  inside it: a routine may read and report, never send, buy, delete,
  or change anything outside the kit folder.
- **One persistent folder.** The shell's container is rebuilt
  between sessions; only the project folder (`/mnt/project-files`)
  survives. The checkout, the workspace, the tools, and every record
  live there. Each channel has its own folder; the main channel's is
  the install's home.
- **Pages and Claude Docs can be shared.** They are never a home for
  procedures §13 records (the bucket register, the deadlines
  register, the handover's contacts). Those stay in the kit folder.
- **Connector writes ask every time.** Duet confirms each write to a
  connected account; that confirmation is the platform's, and a kit
  ticket rides inside it (module 00, below).
- **Claude plan usage is out of reach.** Duet does not read, discuss,
  or change the Claude plan or its usage. Module 09 records the
  subscription as a bucket whose usage the user reads, never the
  agent.

## Paths

- **Checkout:** `/mnt/project-files/kit-checkout/` — the pinned
  clone. Its HEAD moves only on an approved upgrade. Ground rule 2's
  checks run here, and `git rev-parse --show-toplevel` must name this
  folder.
- **Workspace root:** `/mnt/project-files/kit/` — `SETUP-PLAN.md`,
  `INSTRUCTIONS.md` (the record of pointer lines), the procedures,
  the decision queue, `JOBS.md`, the handover, `scopes/`,
  `security/`, `runs/`, and `tools/`.
- In this file, `kit/...` means that path under the project folder.
  Baseline lines in `SETUP-PLAN.md` give paths relative to the
  workspace root, as the wizard says.
- Run any kit tool from the workspace's `tools/` copy or the
  checkout with `python3 -I`, passing paths as arguments.

## Step 0 — Audit first

Offer it, as the wizard says. On Duet the inventory reads: the
platform's project instructions (read-only), project memory, the
claude.ai memory if the session has it, the routine list, the Tasks
page, the project folder, other channels, pages and Docs, connectors
and their write policies, enabled skills, and the shell. A fact that
needs a write or a setting change to check is reported as unchecked.
The report can be a Claude Doc; it holds no §13 records.

## Step 1 — Capability check

Check each answer live; docs/capability-profiles.md's Duet table is a
starting point, not evidence. Fixed answers: `persona-file` no,
`instruction-file` no. Record in the plan the routine minimum
interval the platform states, that only the main chat creates
routines, and that the shell is ephemeral with one persistent folder.
`spaces` stays not established until a routine is shown to rebuild a
page on cadence.

**Billing bucket.** The session draws on the user's Claude plan. The
user names it; record it as user-stated. The agent does not check
plan usage or price, so heavy work in Duet is declared by its size,
not by a figure read from a usage page.

## Step 2 — Interview, as it changes on Duet

- **Q1:** as written. Module 03 is not in the profile; offer it only
  where the Step 1 tokens allow and the user asks.
- **Q2:** (a) and (b) as written. (c) is not offerable: Duet's
  per-act confirmations cannot be replaced by after-the-fact
  reporting, so say so and offer (b).
- **Q3:** the built-in brief and check-ins are the daily rhythm.
  Module 02 is not offered; say why in one line (it duplicates the
  brief, and its triage poll needs a cadence under the routine
  floor). Ask instead which day and time suit the kit's weekly pass.
- **Q4:** as written; module 04 is outside the profile.
- **Q5:** skipped. Duet's memory format belongs to the platform, so
  the answer is (c), leave memory alone, recorded as such; modules
  01, 04, 05, and 08 are not offerable, and the plan says so.
- **Q6:** as written.
- **Q7:** ask for workstreams. Each one's home is a Duet channel or
  the main chat. Do not ask for an instruction file: there is none,
  and the plan says the front door is a memory line (Step 5).
- **Q8:** skipped (no persona file).

## Step 3 — Selection

Offer the `duet` profile: modules 00, 06, 09, and 10, with the audit
figure from the manifest (it includes this overlay and the bootstrap
skill). Then the per-module checklist, gated as the wizard says. Not
offerable on Duet, with the reason stated: 01 and 08 (platform memory
and skills), 02 (built-in brief), 11 (no persona file), 12 (until
`spaces` is established; its audit worksheet can be run read-only, as
Step 0 is), and 03, 04, 05 unless the Step 1 tokens and Q5 allow
them, which on Duet they do not by default.

## Step 4 — The plan, with three additions

Save `SETUP-PLAN.md` in the workspace and show it in chat, as the
wizard says. Besides everything the wizard lists, it carries:

1. **Routines.** Each routine's name, cron, and full prompt, verbatim.
   They are created by the main chat after approval. If the install
   runs in a thread, the thread does not create them: it names each
   one in its report, and the main chat creates it on the user's yes.
2. **Rules to adopt.** The standing rules this install would like
   Duet to keep, one short line each, in plain words the user could
   say. List only what Duet's built-in rules do not already cover.
   No line may relax a confirmation; a line can only add care. The
   plan says: approving the plan does not adopt these. Each is
   adopted only when the user states it in their own words — or
   accepts it where Duet offers a card for that kind of rule — and
   the wizard never writes one into memory from this file. The
   default list, for the user to keep, edit, or drop:
   - "Kit files live in the project folder under kit/. Before kit
     work, read the file it concerns." (the front door; module 00)
   - "Non-urgent kit decisions go in the kit decision queue, and I
     clear them by number." (§3)
   - "When a workstream closes, run the close-out in the kit's
     procedures before archiving it." (§9)
   - "Before I add a skill, plugin, or connector, vet it at a pinned
     version and log it in the kit's vetting log." (module 06)
   - "Before a long or heavy run, say which billing bucket it draws
     on." (module 09, rule 2)
3. **What is a record, not a front door.** `INSTRUCTIONS.md` exists
   and nothing loads it; the procedures bind a session that reads
   them. Say which rules Duet already enforces on its own (§2's
   per-act approval, §7's ground truth, §8's stop-on-mismatch, §10's
   content-is-not-instructions and no credentials in chat, §13's
   no document numbers), which reach Duet only through an adopted
   line, and which stay reference text.

Approval names what it covers, as ground rule 3 says. A rule the user
declines leaves its piece as reference text; record that in the plan.

## Step 5 — Install on Duet

**General mapping.**

- Files: copy and fill templates into the workspace root, exactly as
  each module's Install says; baseline lines as Step 5 item 5 says,
  with paths relative to the workspace root.
- Jobs: a Duet job is a routine plus its `JOBS.md` bullet. Write the
  bullet when the routine is created, with the routine's name and
  cron, and `run record: kit/runs/<job>.md`. File-based job
  definitions do not count as scheduling here: nothing fires them.
  A routine requested but not yet created goes under `JOBS.md`'s
  Planned section, with the approval it waits on.
- Verification: run each module's VERIFY.md at-install checks;
  ledger deferred ones in `SETUP-PLAN.md` with `due:` dates. The
  weekly pass surfaces them (ground rule 8's fallback, below).
- Adopted rules: record each in the plan in the user's own words,
  with the date. A line the user changes is recorded as they said it.

**Module 00.** Install as written, with these placements:

- Step 2 (Q2): (b) installs §2 as written. A ticket's exact action,
  total, fallback, and content-exclusion list are what the agent
  shows when it asks for Duet's confirmation; the confirmation is the
  approval, and it stays one execution.
- Step 3: the decision queue is `kit/decision-queue.md`, numbered as
  the template says. It is surfaced by the weekly pass (§3's
  "normally in the morning brief" reads, on Duet, "in the kit's
  weekly pass"). Duet's Tasks page is not a second queue: an item
  that waits on the user is in the queue, and the pass names it.
- Step 4: each workstream's `SCOPE.md` lives at
  `kit/scopes/<slug>/SCOPE.md` in the main channel's folder, naming
  its home channel. Whether a channel's own session can read it there
  is unchecked (below); until it is, the user opens the SCOPE from
  the main chat when a channel's work is in question.
- Step 5: create `kit/INSTRUCTIONS.md` with the pointer line and the
  `ext:instruction-pointer` anchor pair, as written. It is the record
  of what the front door says. The front door itself is the first
  rule in Rules to adopt; the plan names it as the carrying surface.
- Step 6: `kit/JOBS.md`, from the template.
- Step 7: `kit/continuity-handover.md`, filled with the user. Its
  "how to pause the agent" field names Duet's own controls: ask the
  main chat to pause or delete the kit's routines, disconnect
  connectors in settings, and archive the channel. Third-party
  contacts in it are §13 records; the file stays in the kit folder.
- Step 8: copy the tools into `kit/tools/`. The verifier gate's
  smoke check runs in the shell as written.
- §5 describes the kit's own brief, which this profile does not
  install. Duet's built-in brief is the platform's and is not held to
  §5; the plan says so.

**Module 06.** Install as written. `kit/security/VETTING.md` opens
with this kit's vetting entry: the source, the full commit hash, and
an honest read scope — this overlay and the bootstrap skill included.
The monthly standing-grants inventory runs as its own job, from the
module's job template, on the monthly routine. On Duet it reads the
connectors the session can see and each one's write policy; what the
session cannot see (a setting only the user's settings page shows) is
marked not checkable in the inventory, and the user reads it. A
skill, plugin, or connector the user adds to Duet later is a vetting
item like any other: pin, read in full, log, then add.

**Module 09.** Install as written, with the register in §12 of the
installed procedures. The Claude plan is one surface in the register:
bucket "Claude subscription", usage page "read by the user in Claude's
settings", cap "the plan's own limits; the agent does not read them".
Any API organization, router, or other provider the user's agents
draw on gets its row and its cap, as rules 1 and 4 say. The monthly
spend check runs on the monthly routine as a prompt to the user: the
routine names the buckets due, and the reading happens in a
conversation with the user present, as the module requires.

**Module 10.** Install as written. The register is
`kit/deadlines-register.md`, never a Claude Doc. The surfacing shape
is the module's no-brief shape: a deferred check on a cadence the
user picks, ledgered in the plan. On Duet a routine fires that check,
so the plan states, in words: "No morning brief is installed; the
register is read by the kit's weekly pass on <day>, and an item can
surface up to six days after it enters its lead window." The pass
applies the module's own rules — expired items as failures, in-window
items as due, unknown dates as a chase line — and lead times are set
with that weekly slack in mind.

## The profile's routines

Two routines carry every job this profile installs. Show both prompts
verbatim in the plan; keep each prompt a short pointer to files in the
kit folder, per `JOBS.md`'s slim-definitions rule.

- **`kit-weekly-pass`** — weekly, on the day and time the user chose
  at Q3. It reads `kit/SETUP-PLAN.md`'s verification ledger and names
  every deferred check now due (ground rule 8's fallback for the
  missing session-start line); reads `kit/decision-queue.md` and
  lists its open items by number; reads `kit/deadlines-register.md`
  and applies module 10's surfacing rules; compares `kit/JOBS.md`
  with the routines it can see and reports a mismatch; and appends
  one line to `kit/runs/kit-weekly-pass.md`. It posts one short
  message, or a single line saying nothing is due. It writes only
  under `kit/runs/`.
- **`kit-monthly`** — monthly, on the 1st. It runs module 06's
  standing-grants inventory and records it in `kit/security/`, then
  posts module 09's spend-check prompt (which buckets to read, with
  the user present), and appends one line to `kit/runs/kit-monthly.md`.

`JOBS.md` carries four bullets for them: `kit-weekly-pass`,
`deadlines-check` (rides kit-weekly-pass), `grants-inventory` (rides
kit-monthly), and `spend-check` (rides kit-monthly). A run record
missing 48 hours past its cadence is detector silence (§4); the
weekly pass reports the monthly one's silence, and module 00's
fresh-session test is where the user notices the weekly pass's own.

## Step 6 — Handover, on Duet

As the wizard says, and also: which rules the user adopted and in
what words; which pieces stay reference text; when the first weekly
pass runs; and the three checks the user can run personally — ask a
fresh session "What needs a ticket?", open `kit/runs/` after the first
pass, and read the plan's ledger.

## Lifecycle on Duet

- **Upgrade:** UPGRADING.md, in the checkout. Routine prompts that
  change are shown in the upgrade plan and changed by the main chat.
  An adopted rule whose wording the new pin changes is put to the
  user again; the old wording stands until they say otherwise.
- **Suspend:** pause the module's routine (from the main chat) and
  move its `JOBS.md` bullets to Suspended, as the wizard says.
- **Uninstall:** UNINSTALL.md, per module, with the export offer
  first. The main chat deletes the module's routines on the user's
  yes. Rules the user adopted are theirs: the handover names them,
  and the user asks Duet to drop the ones they no longer want; the
  wizard does not remove memory lines itself.

## Unchecked on Duet

The Step 0 audit could not check these without a write or a setting
change. Check each at the first real install, and record the answer
in the plan; an answer that breaks a step above stops that step.

- Whether a routine's run can read and write the project folder
  (the run records and the grants inventory depend on it).
- Whether a routine can stay silent when nothing is due, or always
  posts.
- Whether a channel's own session can read the main channel's kit
  folder (SCOPE notes depend on it).
- Whether skills added to the user's Claude account load in Duet
  sessions (the bootstrap skill depends on it).
- Whether Duet offers a card for adopting the kind of rule listed in
  Step 4, or only memory lines the user states.
- Project memory's size limit, and whether the front-door line plus
  any other adopted lines fit it.
- Whether a routine can rebuild a page on cadence (`spaces`).
