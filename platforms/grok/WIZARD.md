# Grok Bot overlay — read after wizard/SKILL.md

This overlay adapts the wizard to Grok Bot. It governs the `grok`
profile in `wizard/manifest.yaml` (modules 00 and 01, in the forms
below). Where this overlay and the wizard differ, this overlay
governs on Grok; where this overlay is silent, the wizard governs.
Every platform claim below is a measured result from a ten-test
battery run on a live account (2026-11-23; 7 Pass, 2 Partial,
1 Fail), and the score is named where the claim is load-bearing.
Anything the battery did not measure is labeled unmeasured, here
and in the plan.

## The two warnings (state them in the plan, verbatim in effect)

1. **A second bot is not a sandbox.** One account is one computer,
   one filesystem, one skill library, one connector set (battery
   Test 6, Fail). A bystander bot read the working bot's files,
   fired its skills, and reached every connected account within
   minutes of being created. Only the conversation and each bot's
   private memory are per-bot.
2. **Every bot on the account can read everything every other bot
   can read** — including the account-level user profile, which
   any bot can write and every bot can read. The plan names every
   bot already on the account, because each one holds the access
   this install is about to use.

Warning 2 reaches past the files a bot chooses to write. Tool
results generally, not only connector reads, can persist as
files in the bot's agent asset store on the account's shared
computer, automatically, whether or not the bot copies or saves
anything. Measured, not conjectured (2026-11-23): a connector
read, a tool-catalog listing, and a spreadsheet read all
persisted. By warning 2, every bot on the account can read
those files. Treat any read as leaving a file behind; write
tasks and briefs that involve sensitive material on that
assumption.

## What Grok has instead of the kit's usual surfaces

- **No instruction file, no settings field for standing
  instructions** (Test 1). Standing rules live in the platform's
  memory, entered when the user states them in chat. There is
  nothing to point at, pin, or hash; the wizard's ground rule 2
  applies to the kit checkout the install is read from, not to
  anything on the platform side.
- **Memory is four typed stores, as the battery found them**
  (Test 3, Partial — strong): per-bot profile and journal, plus
  an account-level user profile and shared stores, all
  server-side. Facts are single dated sentences. Changes are
  add, or remove-by-exact-text; there is no in-place edit and no
  user-editable schema, and no inspectable history of removed
  facts. Retrieval was flawless in every probe. The type
  taxonomy is the platform's, not a fixed address space: it
  changed within a single day's session (the cleanup pass found
  a different set of types than the battery had, one store
  retired to read-only), so everything in this pack that touches
  memory — the audit procedures above all — keys on search and
  on paths (`/me/profile`), never on the tool's type names.
- **Routines are the scheduler** (Test 2, Pass): real cron,
  saved instructions that read back verbatim, runs executing in
  the bot's real workspace with working file tools. Timing is
  approximate — dailies drifted minutes inside their windows and
  an "exact" one-off fired about ten minutes late. Every job this
  pack installs tolerates at least ten minutes of drift.
- **Skills are account-shared; their content installs verbatim**
  (Test 8, Pass): a SKILL.md with name/description frontmatter in
  the account-level library; the body installs byte-for-byte.
  The library save rewrites frontmatter *formatting* (run 29,
  disclosed by the bot at save: description as a wrapped YAML
  block, the blank line after the closing `---` dropped) —
  library form ≠ repo form, semantically identical, so a
  formatting diff at read-back is not drift and content is the
  comparison. Invocation is by name; auto-discovery appeared
  after a list refresh, so discovery is a deferred check, never
  an at-install claim.
- **Approvals are Auto-review** (Test 5, Pass with a caveat):
  Always Ask and Allow without Asking rule lists, per-app
  permissions, rule changes drafted on a card and effective only
  on the user's click. Reversible in-scope work is done and
  reported afterwards by default. The caveat is the next section
  but one; it is not a footnote.

## Step 1 on Grok — capability answers

Recorded from the battery; the overlay's Step 1 still checks each
answer live, because accounts differ in what is connected:

- `scheduling`: yes — routines. A routine's own run history is
  not inspectable from inside the bot; the run-record pattern
  below is the history and the detector.
- `shell-python`: yes — a real shell and file tools on the hosted
  computer, in chat and in runs. Persistence caveat, volunteered
  by the platform and not falsified in a day of testing: the
  computer is occasionally swapped and some folders are cleared;
  multi-day file survival is unmeasured. Kit state that must
  survive lives in the workspace files the routines read, and the
  plan says which.
- `second-person`, `shared-docs`, `shared-tasks`,
  `shared-storage`: not used by this profile. The pack is
  single-bot and single-user; connected accounts exist on the
  platform, but no kit surface in this pack shares through them.
- `other-agents`: present on the platform in the worst way — every
  bot sees every bot — and module 04 is excluded anyway (below).
- `persona-file`: no. The bot's description is server-side text,
  edited by asking the bot — not a settings field, and not the
  on-computer `profile.json`, which is a lagging mirror (R1,
  2026-11-23). It doubles as the template instructions field; it
  is not a persona file the agent reads as standing instructions,
  and module 11 is not offered.
- `spaces`: no.
- Billing bucket (wizard Step 1's stop condition) applies
  unchanged: name the bucket in the plan, user-stated.

## Module 00 on Grok — reference text + a memory-seed list

Module 00's procedures are the kit's constitution, and on Grok
they install in two parts:

**Reference text.** The procedures template is copied into the
workspace as a file the bot reads when a routine or the user
points it at it. Measured (Test 4b): file content binds in a fresh
routine run that is told to read the file — its listing followed a
rule planted in a workspace file it had never seen in
conversation. Measured the other way (Test 4, Partial): in chat, a
planted file rule bound only through conversation recall of the
user's own dictation message, not through the file. So: files
steer runs that read them; files do not steer chat by themselves.
Nothing in the plan may claim otherwise.

**The memory-seed list.** The standing rules that must bind in
chat *and* in runs are stated by the user, in the user's own
words, in chat, on install day — one fact at a time, each
confirmed when the bot quotes it back with its provenance. A
memory-saved rule was measured (Test 1, Pass) binding immediately
in chat and again in an unattended scheduled run the same day.
The seed list is a script for that conversation, not text the
agent pastes anywhere: the agent proposes each seed, the user
states it (or corrects and states it), the agent records the
quote-back. Seeds are phrased as facts about the user, because
that is the form the store holds:

1. The user's name for the agent, and the agent's job in one
   sentence, as the user states them.
2. The ticket rule as a fact: "The user requires approval before
   the agent sends, deletes, purchases, books, files, cancels, or
   submits anything — the exact action, the exact total, and the
   fallback stated first."
3. The reporting format the user wants, if any. Worked example:
   "The user wants every status report to end with a one-line
   count of the open decision-queue items." The example is
   illustrative, not the battery's rule: the battery proved the
   mechanism with a format rule of its own (Test 1, Pass — saved
   to memory, quoted back with provenance, followed in chat, and
   followed by an unattended run the same day), and this list
   deliberately does not reuse that rule as its example. An
   example that doubles as a test canary makes seed and leftover
   indistinguishable — if a report follows the format, behaviour
   alone cannot prove whether the user's seed or an old test
   fact is doing the work. What is actually stored is verified
   through the audit inventory (module 01, below), never
   inferred from behaviour. The user's own format, if they want
   one, takes the example's place.
4. The decision-queue fact: "The user clears non-urgent decisions
   from a numbered queue in the workspace file <QUEUE FILE>, and
   silence is never approval for an irreversible action."
5. The correction fact: "When the user corrects a memory fact,
   remove the old fact by its exact text and add the corrected
   one; never leave both standing."
6. The brief fact, if the brief routine is installed: "The user
   wants a failures-first morning brief at <TIME> in <TIMEZONE>,
   posted by routine, built from the workspace run-record and
   decision queue."

**Phrase every seed as a fact or a rule — never as an
instruction to act.** A seed is stored only when it is stated as
a statement about the user, as the six above are. Dictated as an
imperative ("every morning, post a brief…"), it is *actioned
instead of stored* (measured, run 29: the brief seed, phrased as
an instruction, made the bot enable the brief routine on the
spot rather than save a fact — disclosed and reversible there,
and still not a stored seed). The installer warns the user
before the seed conversation starts: state each seed as what
you want standing, not as a command to do it now; if a dictation
comes out as an imperative, restate it as a fact before moving
on, and record in the seed log any seed that was actioned rather
than stored.

**Seed carefully — a seed can become untakeable-back.** The
correction mechanism (seed 5: remove the old fact by its exact
text, then add the corrected one) was measured working (Test 3)
— through a memory store the tool offered at the time. A later
cleanup pass on the same account measured the failure mode: a
fact in the account-level user profile (`/me/profile`) was
removed cleanly, while two facts saved earlier under a
"(profile)" store refused exact-text removal — the tool
reported that no fact with exactly that text was recorded. The
platform had changed its memory tool's surface mid-session: the
tool no longer offers that store at all, and lists it read-only.
Facts saved under a store the tool later retires are orphaned
by the change, and no user-facing removal surface for them was
found. So treat every seed as potentially permanent: state, in
your own words, only rules you mean to keep, and check the
quote-back before the conversation moves on — a seed's
removability depends on the platform's tool surface, not on
anything the user or the bot controls.

One measured subtlety belongs in the plan: **the write target is
phrasing-sensitive.** A fact dictated as a fact about the user
landed in the account-level user profile — readable by every bot
— while setup-conversation facts sat in the bot's private store.
Seeds the user intends as private to this bot must not be phrased
as user-profile facts, and the plan records which store each seed
was confirmed in, from the bot's quote-back, not from assumption.

Chat-granted standing permission is conversation-scoped and does
not carry to routine runs (Test 5). A routine that needs an
approval carries it in its saved instruction — the instruction
counts as the ask — or it stops and waits when Auto-review blocks
a step mid-run. No seed may claim a permission a routine will not
actually hold.

## Module 01 on Grok — the audit half only

**What ships: the audits.** Grok's stores are legible — dated,
single-sentence, searchable — so module 01's lint and fidelity
discipline runs against them:

- *Inventory.* Search each store and list what it holds, with
  dates: per-bot profile, per-bot journal, the account-level user
  profile, and the shared stores. The audit names which store
  each fact sits in; a fact in the wrong store (a private fact in
  the account-level profile) is a finding, per the phrasing
  subtlety above. Stores are identified by search and by path,
  never by the memory tool's type names — the taxonomy changed
  within a single day's session, so a type name is not a stable
  address and an audit keyed on one would silently miss whatever
  the platform has renamed or retired. The dates in the inventory
  are the store's stamps, and **the store dates facts in UTC**
  (run 29, two observations): a fact stated in the user's
  afternoon is stamped the next day, while the fact's own text
  keeps the date as stated. Read a stamp as the store's clock,
  not the user's — the stamp/text difference is the platform's
  dating, not a contradiction, and not a fact to correct.
- *Lint.* Deterministic checks over the inventory: facts that
  contradict each other, facts superseded by a later dated fact
  still standing beside it, facts whose date makes them stale
  against the workspace record, journal entries claiming work no
  run-record line supports. Findings are candidates; a mind
  decides each one — module 01's rule, unchanged.
- *Fidelity.* Sample facts at random and check each against its
  source: the workspace file, the run-record, the user's own
  correction. A fact with no checkable source is reported as
  unverifiable, never passed over in silence.
- *Correction.* The platform's only edit is remove-by-exact-text
  plus add. Removal was verified real at the search layer (a
  corrected test fact was replaced, not duplicated — the count
  proved it). Facts saved under a memory store the tool later
  retired refused the same removal (see the seed caution under
  module 00), so a correction the platform refuses is reported
  as refused, never as applied. Whether the server retains removed facts is not
  inspectable; the audit says so rather than claiming a deletion
  it cannot see. Every correction is proposed to the user first
  and applied on approval, as a remove/add pair the report shows
  verbatim.

**What does not ship: the architecture.** Module 01's schema —
current state at the top, superseded claims kept in a History
section, verify pointers on precise claims, a user-editable
schema file — has no Grok form. The schema is fixed by the
platform, removed facts leave no visible history, and there are
no verify pointers. The pack does not pretend otherwise, and no
plan may describe the platform stores as the kit's memory
architecture. Where kit-grade history is wanted, it lives in
workspace files the bot maintains (a dated log, corrections
appended, nothing rewritten), with platform memory as the index
that points at them.

## Module 04 — excluded, and the plan says why

Module 04 (AI Exchange) is not in the profile and is not offered
per-module on Grok. The battery's isolation test failed (Test 6):
a coordination layer designed on assumed isolation would be
designed on a fiction, and the shared stores that look like a
coordination channel are readable by every bot on the account,
which is precisely the property a coordination layer must not
assume away. If a future battery re-measures isolation and it
passes, the exclusion is revisited then — on evidence, not on a
platform announcement.

## The jobs layer — routines

Jobs install as routines from `template/routines.md`. Three
disciplines, all measured:

- **Verbatim saved instructions.** A routine's saved instruction
  is read back from storage after creation and compared with the
  approved text (the battery's routines matched). Judge the
  comparison against what import actually delivers (run 29):
  a routine saved directly holds the approved text word for
  word, but an *imported* routine's saved instruction is the
  template text **plus two platform-added lines** — the
  routine's one-line description prepended, and a closing line
  naming where its results post. Those two lines are the
  platform's, disclosed by the bot at read-back; anything
  beyond them is drift. The instruction is self-contained: it
  names the workspace files it reads, the record it appends,
  and what it posts — because a run is a fresh context that
  holds only its instruction, the memory that reaches it, and
  the files it is told to read.
- **The run-record pattern.** Every routine appends one line per
  run to a workspace record file — name, timestamp, one-line
  outcome — whether or not it posts anything. A silent routine
  that appends its line is detectable; a missing line is the
  detector's signal (Test 10, Pass: the silent run posted nothing
  and left exactly its specified line; the record showed both of
  the day's runs, in order). The morning brief reads the record
  the way module 02 reads a jobs file: a job with no line inside
  its window is a failure to surface, not a quiet success.
- **Timing tolerance.** Schedules are the server's: dailies carry
  windows, and even an "exact" one-off fired about ten minutes
  late (Test 4b's run). No routine in this pack is time-critical
  inside ten minutes, and the brief's detector windows are set
  wider than the drift.

## Approvals — Auto-review recipes, and the warning

The ticket rule (module 00, procedures §2) maps onto Auto-review
like this:

- **Always Ask:** sends of every kind, deletes, purchases, form
  submissions — the ticket classes. The install sets these rules
  with the user present; a rule change is drafted on a card and
  takes effect only on the user's click, and the plan records the
  lists as the user confirmed them, not as the agent proposed
  them. The record step is necessarily **user-mediated**: a bot
  cannot read its own Auto-review settings (measured, run 29 —
  asked to record them, the bot left the section empty rather
  than guess), so the user reads the lists in the app and
  dictates the values, and the bot records them labeled as
  stated by the user. The bot's account of *where* settings live
  in the app is likewise unreliable (same run: it named the
  wrong settings section against the app's actual page) —
  verify settings locations against the app itself, never the
  bot's say-so.
- **Allow without Asking:** reads, searches, and workspace file
  writes inside the install's scope — the reversible tier the
  ticket rule pre-authorizes.
- **Report-afterwards** is the platform default for that tier;
  the kit's brief and run-record make the reporting checkable
  rather than conversational.

One scope question is **unmeasured: whether the Auto-review
lists are per-bot or account-wide.** The battery set and read
the lists on one bot (Test 5); nothing measured what a second
bot on the same account would show, and this pack does not
guess. Until that is measured, the install records the lists
**as found, before changing them**, in `SETUP-PLAN.md` — so a
later reading (a second bot's settings, a post-install check)
can be compared against the as-found state instead of against
the install's intention.

**The warning, at full strength, because the battery measured it
in the kit's own release flow:** Auto-review governs connector
calls. **The shell path is unreviewed — a push is a send.** In
Test 7, a branch push and an annotated tag push over shell `git`
ran with no confirmation card at all, in an act class the bot
itself had listed as stop-first; the only approvals in the flow
were the code host's own sign-in pages. No Always Ask rule fixes
this, because the review surface does not see shell actions. The
pack's release guidance is therefore procedural, not
configurational: pushes and tags are ticketed in the workspace
record before they run, the ticket is the control, and the plan
must never state that the platform will card a push.

The vendor's own docs describe an approval card for terminal
commands; in measured sessions on 2026-11-23 that card never
appeared — do not rely on the documented card.

The same test priced the egress path: shell git access required
a device-code sign-in whose token (scopes: gist, read:org, repo)
is stored in plain text in the `gh` config on the shared
computer — account-wide, not repo-scoped, and readable by every
bot on the account, per the warnings at the top. The plan names
the token's location and blast radius, recommends signing in only
when a release is actually being made and revoking afterwards,
and records the user's decision either way. An install that does
not need egress does not sign in.

## The template front door

A Grok template carries the bot's **description (= its
instructions field), its skills (content verbatim; the library
save normalizes frontmatter formatting — see the surfaces
section), and its routines** — imported **paused**, with
import-time parameter prompts the template declares (measured:
"Ask the importing user for: Timezone"). It does not carry the
title, any memory, or any workspace file. **Declarations are
advisory, not declarative** (run 29): the platform parses them
heuristically — one declared parameter never became a parameter
at all, another was pattern-matched into an unrelated platform
variable — import prompts may not fire, and staged values may
carry silently into the child. The manifest inspection at
staging and the read-backs after import are the control; the
declaration is not. `template/` in this pack holds the
contents, prepared in the repo:

- `template/description.md` — the description text, which is the
  instructions an imported bot starts with.
- `template/skills/` — the skill set, one SKILL.md per skill,
  in the form the account library holds them.
- `template/routines.md` — the routine definitions, each with its
  schedule, its parameter prompts, and its saved instruction
  verbatim.
- `template/workspace.md` — the starter contents for the
  workspace files a template cannot carry (run-record, decision
  queue, setup plan), in the formats the routines and skills
  read, plus the install step that creates the watch routine's
  target when its answer names a workspace file.

Publishing the template in the app is a separate ticketed step,
outside this install; the repo remains the source of truth, and
file-based kit state still ships by the workspace route — a
template import delivers skills, routines, and instructions, and
the plan then creates the workspace files (procedures reference,
decision queue, run-record) the routines read.

**A published template dies with its source bot** (measured,
run 29: the template link stopped working the day the source
bot was deleted). Publishing is therefore not the end of the
source bot's life: it stays alive for as long as the template
must live, and deleting it retires the template. An install
that publishes a template records that dependency in the plan;
an install that does not publish one owes the source bot no
such afterlife.

**Choose the imported bot's name before staging.** The
description's `<AGENT NAME>` is filled at staging, with the name
the imported bot will carry, and a template carries no title —
the name cannot ride the template and be decided later. The
battery's probe measured the wrinkle (§6): a template propagates
the *source* bot's name into the child's name and title at
instantiation, the import flow renames the bot, and the source's
actual title does not carry — the description is the only role
text that survives intact. So the filled description is the one
piece of naming that reaches the imported bot exactly as
written; settle the name first.

### Staging — how the contents become a template

A template on this platform is a copy of a bot (measured, §6
probe: Share → "Create a copy — Share a template link"). The
repo contents therefore become a template by being loaded onto
a source bot and staged from it. The battery's probe ran this
sequence end to end; steps below are its shape, and anything it
did not isolate is labeled unmeasured rather than asserted.

1. **Create a scratch source bot** on the account. It is staging
   scaffolding — and it is not a sandbox: from the moment it
   exists it shares the account's computer, skill library, and
   connectors (the two warnings). It is deleted when the
   install closes *only if no published template depends on
   it*: a template published from it dies with it (front door,
   above), so a source bot whose template must live stays
   alive, and the plan records which case the install is in.
2. **Set the source bot's description** to the text in
   `template/description.md`, placeholders filled — the agent
   name chosen above, the user's name. Role text is set by
   asking the bot in chat. The description lives server-side;
   the bot is the editor (R1, 2026-11-23). There is no
   settings field for a human to view or edit it — a personal
   bot's settings nav has no profile or description section —
   and the on-computer `profile.json` is a lagging mirror, not
   the source. Verify by asking the bot to quote the
   description back, not by opening Settings and not by
   reading `profile.json`. What
   survives staging differs by placeholder: the agent name
   reaches the child exactly as written, but **user-name
   references do not — staging generalizes them** (measured,
   run 29: the source's "<USER NAME>'s personal agent" was
   staged as "the user's personal agent", the only substitution
   in an otherwise verbatim text), and the generalized text is
   what the imported bot carries. For a shareable template the
   generalization is arguably correct; for this install it
   means the child's description will not carry the user's
   name, and the plan does not claim otherwise.
3. **Skills need no loading onto the bot.** The skill library is
   account-level: a skill staged into a template is one that
   exists in the library, its content installed verbatim
   (Test 8). If a pack skill is not yet in the library, add it
   there first, in the form `template/skills/` holds it. The
   library save normalizes frontmatter *formatting* (measured,
   run 29, disclosed by the bot at save: the description is
   rewritten as a wrapped YAML block, and the blank line after
   the closing `---` is dropped) — the library form is not the
   repo form, and it is semantically identical; a formatting
   diff at read-back is not drift.
4. **Create the three routines on the source bot** from
   `template/routines.md`, saved instructions verbatim, left
   paused — with **real schedule values filled in**: routine
   creation requires a valid cron expression, so the
   definitions' placeholder schedules (`<TIMEZONE> <MINUTE>
   <HOUR>`) cannot be stored literally (measured, run 29 — the
   staging bot rejected them and filled real values). Choose
   the timezone and the times with the user at staging; the
   staged values are what the child will hold unless an import
   prompt overrides them, and per the front door, it may not.
   State each routine's parameter declaration ("Ask the
   importing user for: …", as the definition lists it) with the
   routine as you create it — the pack's definitions carry the
   declaration as a separate line for exactly this purpose —
   and expect the declaration to be unverifiable from the
   routine's saved view (run 29: it attached as the routine's
   note, which the saved view does not show). Step 6's manifest
   inspection is where its presence is confirmed.
5. **Ask the source bot to stage a template from itself.**
   Measured: the bot inventoried its own components and made
   stated inclusion calls — it kept its skill and routine, and
   excluded a fact from the account-level user profile on the
   ground that user-profile facts are not template payload. The
   staged template appears as an unpublished card showing the
   description, offering Publish and View Details; it goes live
   only when the user confirms on the review card.
6. **Inspect before publishing.** View Details shows the whole
   manifest (measured): Context — the Instructions field holding
   the description text; Skills — each SKILL.md in full, in its
   library form (step 3's formatting note applies — compare
   content, not formatting); Routines — each routine's full text
   and cron, **and its parsed parameter declaration**. There is
   no files section and no memory section; their absence is
   correct, not a gap. Three checks, all load-bearing: the
   description shown is the *staged* text — user-name references
   generalized (step 2) — so check it as the text the child will
   actually carry, not against the source bot's; every routine
   shows a declaration, because whether the declaration attaches
   automatically when a routine is created, or only when it is
   stated as in step 4, is **unmeasured** — the battery observed
   the declaration present in a staged manifest and the prompt
   asked at import, and did not isolate the mechanism; and each
   parsed declaration names the parameters the definition
   intends, because the parsing is heuristic (run 29: one
   routine's "Brief time" never parsed as a parameter, and the
   watch's trip placeholder was pattern-matched into an
   unrelated platform variable in both the instruction text and
   the ask-list — a directed restage did not repair it, and the
   defect shipped in the template; the importing bot later
   repaired the text itself and disclosed the repair). A
   routine whose text or declaration is wrong in the manifest
   is not ready, whatever the cause; publish only when the
   manifest passes, or record the deviation and name who fixes
   the child after import.
7. **Publish (the user's click, ticketed as above) and import.**
   Instantiating the template creates the new bot; the routines
   arrive paused (measured). The declared parameters **may** be
   asked at import — in run 29 no prompts fired at all, and the
   staged schedules and values carried silently into the child;
   where a value did not carry (the watch's target), the
   imported bot said so on arrival. After import, read back
   every routine's saved instruction and schedule before
   enabling anything: the read-back, not the declaration, is
   the control. Enabling each routine afterwards is the user's
   act, per the jobs section.

## Deferred checks on Grok

There is no instruction file to carry the wizard's session-start
surfacing line, so deferred checks live in `SETUP-PLAN.md` in the
workspace, and the weekly memory-audit routine's instruction
includes reading it and surfacing any check whose due date has
passed — a routine is a fresh context that reads the files it is
told to read, which is the measured route. A deferred check with
no routine to surface it is a failed check, as the wizard says;
if the user declines the audit routine, the plan names what
surfaces the checks instead, or the install does not close.

## Verify (this pack)

*At install:* the seed conversation completed, each seed quoted
back with provenance and its store recorded; the Auto-review
lists recorded as found before the install changed them, and
read back as the user confirmed them — recorded from the user's
dictation, since the bot cannot read its own settings (see
Approvals); each routine created paused-then-enabled per the
plan, its saved instruction read back against the approved text
(the two platform-added lines on an imported routine allowed;
anything beyond them is drift — see the jobs layer); the
run-record file created with its header; the procedures
reference and decision queue in the workspace, created from the
`template/workspace.md` starters; the watch routine's target in
place as its import answer describes it, before the watch is
enabled; the egress decision recorded (signed in, with the
token warning shown — or not signed in).

*Deferred:* the first brief run lands inside its window and
appends its line; the first silent-watch line appears with no
post; the first memory audit runs and its findings are decided;
skill auto-discovery confirmed after the platform's list refresh
(invocation by name is the at-install evidence; discovery is
not). Each is ledgered in `SETUP-PLAN.md` with a due date, as the
wizard requires.
