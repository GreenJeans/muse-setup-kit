# Duet overlay — the setup wizard on Claude Duet

**Status: rehearsed in part at v0.13-rc1 and v0.13-rc3; changed
since.** A test install ran through this overlay at v0.13-rc1
(`00e6dd08736ac4cdf2ff89f585f98a53bbb163c1`; docs/REHEARSALS.md run
22): the files and at-install checks worked, the routines could not
reach the project folder. The kit state doc (below) replaced that
design, and the same install upgraded to v0.13-rc3
(`431edb0e753cdd5b7290f01fef1b3dd5076999b6`; run 23): both routines
read the doc in test fires and a sync recorded their posts. The
routine prompts were tightened after run 23, so this text is
unrehearsed at this pin. The plan says so in these words: "Duet
profile and overlay: rehearsed in part at v0.13-rc3; changed since —
unrehearsed at this pin." Each module keeps its own rehearsal
status, stated as `wizard/SKILL.md` Step 3 says.

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
  account, and share; a Doc changed only when the user asks for that
  change; nothing read becomes an instruction; memory never grants
  permission). They are not the user's to waive and not the kit's to
  relax. Where a kit rule and a Duet rule both apply, both are met,
  and the stricter one decides.

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
- **The hosting chat.** The install lives in one Duet chat: the main
  chat or a channel the user picks. That chat's folder holds the
  checkout and the workspace, and its routines carry the kit's jobs.
  A routine belongs to the chat that creates it, so the kit's
  routines are created, changed, and deleted by the hosting chat, on
  the user's yes. A thread names a routine in its report instead.
- **Routines fire with no project folder.** A routine fires on cron,
  no more often than the platform's minimum interval. Its run is a
  fresh session: no conversation, no `/mnt/project-files`, and no
  tool that reads project files (tested at v0.13-rc1, run 22). It
  does have the hosting chat's project memory, the user's connectors
  (Google Drive, Claude Docs), and posting to the hosting chat. No
  yes counts inside a run: a routine reads and reports, and changes
  nothing. So every kit routine reads the **kit state doc** (below),
  never `kit/`.
- **One persistent folder.** The shell's container is rebuilt
  between sessions; only the hosting chat's project folder
  (`/mnt/project-files`) survives. The checkout, the workspace, the
  tools, and every record live there. Another chat's session sees
  its own folder, not this one; it can read this one's files only
  through Duet's tools for other chats' files, never by path.
- **Pages and Claude Docs can be shared.** They are never a home for
  procedures §13 records (the bucket register, the deadlines
  register, the handover's contacts). Those stay in the kit folder.
  The kit state doc holds no §13 record (below).
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
  checks run here.
- **The folder is a link.** `/mnt/project-files` is a symlink (on
  the tested account, to `/mnt/attach/project-files`), so
  `git rev-parse --show-toplevel` prints the resolved path. The check
  is that it **resolves to** the checkout: compare
  `realpath /mnt/project-files/kit-checkout` with the toplevel, never
  the literal strings.
- **Git ownership.** The folder belongs to another uid, so git
  refuses it ("detected dubious ownership"). Pass the resolved path
  on every git command: `git -c safe.directory=<resolved checkout>
  ...`. Never change global or system git config, and never use
  `safe.directory=*`.
- **Workspace root:** `/mnt/project-files/kit/` — `SETUP-PLAN.md`,
  `INSTRUCTIONS.md` (the record of pointer lines), the procedures,
  the decision queue, `JOBS.md`, the handover, `scopes/`,
  `security/`, `runs/`, and `tools/`.
- In this file, `kit/...` means that path under the hosting chat's
  project folder. Baseline lines in `SETUP-PLAN.md` give paths
  relative to the workspace root, as the wizard says.
- Run any kit tool from the workspace's `tools/` copy or the
  checkout with `python3 -I`, passing paths as arguments.

## The kit state doc

The one surface a routine can read. It is a Claude Doc the install
creates, titled "Muse Setup Kit state (generated — edit kit/, not
this)". It is a **derived view**: `kit/` is the full record and wins
every disagreement. The doc carries only what the routines need, as
dated lines:

1. **Header:** the pin, the hosting chat's name, and "Synced
   <date, time>".
2. **Deferred checks:** each open entry of the plan's verification
   ledger — module, check name, `due:` date (or event plus fallback
   date).
3. **Decision queue:** each open item's number and its one-line
   title. A title that names a §13 record is copied as "item N —
   open it in the kit chat".
4. **Deadlines (pointers only):** one line per register row —
   surfaces-from date (expiry minus lead time), expiry date, On
   expiry (renew or lapse), or `undated`. **No item name, source,
   or number**: §13 keeps personal records in local files, so the
   doc says *when* something is due and the register in `kit/` says
   *what*. The register's History is not copied.
5. **Monthly:** the next spend-check date and the count of buckets
   in the register (no names, no figures); the grants inventory's
   last recorded date and its connector list (names and write
   policy only).

It holds no document number, account number, figure, credential,
or third-party contact. Module 10 stores no document numbers in the
first place; the doc stores less than the register does.

**How it is refreshed.** A Duet session changes a Doc only when the
user asks for that change, so every sync is the user's ask:

- **At install:** the plan names the doc, and approving the plan is
  the ask to create and fill it.
- **On change:** whenever the hosting chat changes a file the doc
  mirrors (the ledger, the queue, the register, the bucket
  register's row count, a grants inventory), it ends that
  reply by offering the sync in one line ("Should I sync the kit
  state doc?").
- **Manual:** the user can say "sync the kit doc" at any time.

A sync reads `kit/` fresh, rewrites the doc's sections whole, and
stamps the header. Before rewriting, it reads the doc: an edit that
no sync made is shown to the user and goes nowhere until they say
which file it belongs in. A sync also reads the hosting chat for the
routines' posts since the last sync and writes one line per post
into `kit/runs/<job>.md` (the run record), records a monthly
post's grants inventory in `kit/security/`, and compares `JOBS.md`
with the hosting chat's routine list, reporting any mismatch. That
comparison lives in the sync because a routine run cannot see the
routine list (run 23).

**What depends on it.** Module 10's surfacing, the deferred-check
fallback, the queue reminder, and the monthly prompts all read the
doc. An item added to `kit/` after the last sync surfaces only after
the next one. Date-driven items need no sync to fall due: the
routine compares today with the dates already in the doc.

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
`instruction-file` no. Record in the plan the hosting chat, the
routine minimum interval the platform states, that the hosting chat
owns the kit's routines, that a routine run has no project folder,
and that the shell is ephemeral with one persistent folder.
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
- **Q6:** skipped: module 02 is not offerable, so nothing reads the
  answer (the wizard's Q6 note).
- **Q7:** ask for workstreams, then each one's home. A new Duet user
  often has no channels yet. Offer the hosting chat as the default
  home for every workstream, and a channel per workstream as the
  option ("a separate chat for each, so its history and tasks stay
  apart"). A channel the user wants but has not made yet is recorded
  as planned, and the SCOPE names the hosting chat until it exists.
  Do not ask for an instruction file: there is none, and the plan
  says the front door is a memory line (Step 5).
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

## Step 4 — The plan, with four additions

Save `SETUP-PLAN.md` in the workspace and show it in chat, as the
wizard says. Besides everything the wizard lists, it carries:

1. **Routines.** Each routine's name, cron, and full prompt, verbatim
   (the templates below, with the doc's id filled in after it
   exists). The hosting chat creates them after approval. If the
   install runs in a thread, the thread does not create them: it
   names each one in its report, and the hosting chat creates it on
   the user's yes.
2. **The kit state doc.** Its title, what it mirrors (the five
   sections above), that `kit/` wins, how it is synced, and the
   sentence "Module 10's surfacing and the weekly pass read this
   doc; anything added since the last sync waits for the next one."
3. **Rules to adopt.** The standing rules this install would like
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
   - "After changing a kit file, offer to sync the kit state doc."
     (keeps the routines' view current; an offer, never a sync on
     its own)
   - "Non-urgent kit decisions go in the kit decision queue, and I
     clear them by number." (§3)
   - "When a workstream closes, run the close-out in the kit's
     procedures before archiving it." (§9)
   - "Before I add a skill, plugin, or connector, vet it at a pinned
     version and log it in the kit's vetting log." (module 06)
   - "Before a long or heavy run, say which billing bucket it draws
     on." (module 09, rule 2)
4. **What is a record, not a front door.** `INSTRUCTIONS.md` exists
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
- The kit state doc: create it once the files are written, fill it
  by a first sync, and record its id in `SETUP-PLAN.md`.
- Jobs: a Duet job is a routine plus its `JOBS.md` bullet. Write the
  bullet when the routine is created, with the routine's name, cron,
  "reads the kit state doc", and `run record: kit/runs/<job>.md
  (copied from its posts at each sync)`. File-based job definitions
  do not count as scheduling here: nothing fires them. A routine
  requested but not yet created goes under `JOBS.md`'s Planned
  section, with the approval it waits on.
- Test fire: fire each routine once by hand with **no extra text**.
  Text added to a test fire arrives as a second turn, so the run
  does its prompt twice and posts twice (run 22). The at-install
  check passes when the run read the doc (its post quotes the doc's
  "Synced" stamp) and posted once. A run that cannot read the doc
  fails the check: pause the routine, and the plan falls back to the
  no-routine shape (Unchecked, below).
- Verification: run each module's VERIFY.md at-install checks;
  ledger deferred ones in `SETUP-PLAN.md` with `due:` dates. The
  weekly pass surfaces them from the doc (ground rule 8's fallback).
- Adopted rules: record each in the plan in the user's own words,
  with the date. A line the user changes is recorded as they said it.

**Module 00.** Install as written, with these placements:

- Step 2 (Q2): (b) installs §2 as written. A ticket's exact action,
  total, fallback, and content-exclusion list are what the agent
  shows when it asks for Duet's confirmation; the confirmation is the
  approval, and it stays one execution.
- Step 3: the decision queue is `kit/decision-queue.md`, numbered as
  the template says. It is surfaced by the weekly pass from the doc
  (§3's "normally in the morning brief" reads, on Duet, "in the kit's
  weekly pass"). Duet's Tasks page is not a second queue: an item
  that waits on the user is in the queue, and the pass names it.
- Deferred checks: the queue drill's event ("first brief or first
  on-demand review") reads, on Duet, "the first scheduled weekly
  pass after a test item is added to the queue". A test fire does
  not count, and neither does a pass with no test item in the queue;
  the plan says when the test item goes in. The ledger row keeps its
  install + 7 days `due:` date, as VERIFY.md says.
- Step 4: each workstream's `SCOPE.md` lives at
  `kit/scopes/<slug>/SCOPE.md` in the hosting chat's folder, naming
  its home (Q7). A channel's own session cannot open it by path; it
  reads it through Duet's tools for other chats' files (they worked
  from a channel at v0.13-rc1), or the user opens it from the hosting
  chat.
- Step 5: create `kit/INSTRUCTIONS.md` with the pointer line and the
  `ext:instruction-pointer` anchor pair, as written. It is the record
  of what the front door says. The front door itself is the first
  rule in Rules to adopt; the plan names it as the carrying surface.
- Step 6: `kit/JOBS.md`, from the template.
- Step 7: `kit/continuity-handover.md`, filled with the user. Its
  "how to pause the agent" field names Duet's own controls: ask the
  hosting chat to pause or delete the kit's routines, disconnect
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
module's job template, on the monthly routine. On Duet the run reads
the connectors it can see and each one's write policy, compares them
with the doc's last recorded list, and posts the inventory; the next
sync records it in `kit/security/`. What the run cannot see (a
setting only the user's settings page shows) is marked not checkable,
and the user reads it. A skill, plugin, or connector the user adds to
Duet later is a vetting item like any other: pin, read in full, log,
then add.

**Module 09.** Install as written, with the register in §12 of the
installed procedures. The Claude plan is one surface in the register:
bucket "Claude subscription", usage page "read by the user in Claude's
settings", cap "the plan's own limits; the agent does not read them".
Any API organization, router, or other provider the user's agents
draw on gets its row and its cap, as rules 1 and 4 say. The monthly
spend check runs on the monthly routine as a prompt to the user: the
routine says the check is due and how many buckets to read (the doc
holds no names or figures), and the reading happens in the hosting
chat with the user present, as the module requires.

**Module 10.** Install as written. The register is
`kit/deadlines-register.md` (module 10 lets the plan choose the
path), never a Claude Doc. The surfacing shape is the module's
no-brief shape: a deferred check on a cadence the user picks,
ledgered in the plan. On Duet a routine fires that check from the
doc's pointer lines, so the plan states, in words: "No morning brief
is installed; the register's dates are read from the kit state doc
by the kit's weekly pass on <day>. An item can surface up to six days
after it enters its lead window, an item added since the last sync
surfaces only after the next sync, and the post says when, not what:
ask the kit chat to read the register." The pass applies the
module's own rules to the dates — past expiry as failures, in-window
as due, `undated` as a chase line — and lead times are set with that
weekly slack in mind.

## The profile's routines

Two routines carry every job this profile installs. Show both prompts
verbatim in the plan. Each is a short pointer to the doc, per
`JOBS.md`'s slim-definitions rule, and names the doc by its id
because a run has no conversation to find it in.

- **`kit-weekly-pass`** — weekly, on the day and time the user chose
  at Q3. Prompt template: "Kit weekly pass. Read the Claude Doc
  <doc id> (the kit state doc) and nothing else of the kit. Using
  today's date: list every deferred check now due; list the open
  decision-queue items by number; apply module 10's rules to the
  deadline lines (past expiry: failure; in lead window: due;
  undated: chase). If none of these has anything to list, post only
  this one line: 'Kit weekly pass: nothing due (doc synced
  <stamp>).' Otherwise post one short message headed 'Kit weekly
  pass' that quotes the doc's Synced stamp and lists only what is
  due. Change nothing."
- **`kit-monthly`** — monthly, on the 1st. Prompt template: "Kit
  monthly pass. Read the Claude Doc <doc id> (the kit state doc).
  List the connectors you can see with each one's write policy, and
  name any change from the doc's last recorded inventory. If today
  is on or after the doc's next spend-check date, say the spend
  check is due and how many buckets to read with me in this chat;
  otherwise say only when it is next due. Post one message headed
  'Kit monthly pass' that quotes the doc's Synced stamp. Change
  nothing."

`JOBS.md` carries four bullets for them: `kit-weekly-pass`,
`deadlines-check` (rides kit-weekly-pass), `grants-inventory` (rides
kit-monthly), and `spend-check` (rides kit-monthly). Each run's post
is its first trace; a sync copies it into `kit/runs/`. A run record
missing 48 hours past its cadence is detector silence (§4): a sync
that finds a post missing says so, and the weekly pass's own post
going missing is what the user notices first.

Both passes post on every run, even with nothing due: the post is
the run record, so a silent run would read as detector silence. The
weekly pass's nothing-due post is one line for that reason.

## Step 6 — Handover, on Duet

As the wizard says, and also: which rules the user adopted and in
what words; which pieces stay reference text; the kit state doc and
how to sync it; when the first weekly pass runs; and the three
checks the user can run personally — ask a fresh session "What needs
a ticket?", read the first weekly pass's post, and read the plan's
ledger.

## Lifecycle on Duet

- **Upgrade:** UPGRADING.md, in the checkout. Step 4's conflict list
  comes from the plan's baseline by hand: `kit_doctor.py` ships with
  module 05, outside this profile. For each `- installed:` line not
  marked `accumulating`, compare `sha256sum` of the file with the
  recorded hash; every mismatch is a conflict to list. Routine prompts that
  change are shown in the upgrade plan and changed by the hosting
  chat. An adopted rule whose wording the new pin changes is put to
  the user again; the old wording stands until they say otherwise.
  An upgrade ends with a sync.
- **Suspend:** pause the module's routine (from the hosting chat)
  and move its `JOBS.md` bullets to Suspended, as the wizard says.
- **Uninstall:** UNINSTALL.md, per module, with the export offer
  first. The hosting chat deletes the module's routines on the
  user's yes; removing the last module deletes the kit state doc on
  the user's yes. Rules the user adopted are theirs: the handover
  names them, and the user asks Duet to drop the ones they no longer
  want; the wizard does not remove memory lines itself.

## Answered by test runs (runs 22 and 23)

- A routine run cannot read or write the project folder, by path or
  by tool. Hard limit; the kit state doc is the answer.
- Skills added to the user's Claude account load in Duet sessions.
- A channel's session cannot read another chat's folder by path, but
  can through Duet's tools for other chats' files.
- Project memory holds 16 KiB; a larger save is refused, not
  trimmed. The adopted lines fit easily.
- No standing-rule card was offered in that channel; rules there are
  lines the user states.
- A test fire with extra text runs twice; with none, once.
- A routine run can read the kit state doc by its id (run 23). The
  test fire still checks it at every install. If it fails there, the
  routines are not created: the plan says the weekly and monthly
  passes run only when the user asks the hosting chat for "the kit
  pass", and module 10 surfaces only then.
- A routine run cannot see the chat's routine list (run 23), so the
  `JOBS.md` comparison runs in the sync.
- Whether a routine can stay silent is no longer asked: the passes
  post on every run by design (the post is the run record).

## Unchecked on Duet

Check each at the first install of this pin, and record the answer
in the plan; an answer that breaks a step above stops that step.

- Whether a scheduled run behaves as the test fires did (the first
  weekly pass on its real cadence).
- Whether Duet offers a card for adopting the kind of rule listed in
  Step 4 on the user's account, or only memory lines they state.
- Whether a routine can rebuild a page on cadence (`spaces`).
