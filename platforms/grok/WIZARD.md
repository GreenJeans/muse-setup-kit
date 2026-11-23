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

## What Grok has instead of the kit's usual surfaces

- **No instruction file, no settings field for standing
  instructions** (Test 1). Standing rules live in the platform's
  memory, entered when the user states them in chat. There is
  nothing to point at, pin, or hash; the wizard's ground rule 2
  applies to the kit checkout the install is read from, not to
  anything on the platform side.
- **Memory is four fixed stores** (Test 3, Partial — strong):
  per-bot profile and journal, plus an account-level user profile
  and shared stores, all server-side. Facts are single dated
  sentences. Changes are add, or remove-by-exact-text; there is no
  in-place edit and no user-editable schema, and no inspectable
  history of removed facts. Retrieval was flawless in every probe.
- **Routines are the scheduler** (Test 2, Pass): real cron,
  saved instructions that read back verbatim, runs executing in
  the bot's real workspace with working file tools. Timing is
  approximate — dailies drifted minutes inside their windows and
  an "exact" one-off fired about ten minutes late. Every job this
  pack installs tolerates at least ten minutes of drift.
- **Skills are account-shared and install verbatim** (Test 8,
  Pass): a SKILL.md with name/description frontmatter in the
  account-level library; the body installs byte-for-byte, and any
  platform-added frontmatter is disclosed. Invocation is by name;
  auto-discovery appeared after a list refresh, so discovery is a
  deferred check, never an at-install claim.
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
- `persona-file`: no. The bot's description is editable text and
  doubles as the template instructions field; it is not a persona
  file the agent reads as standing instructions, and module 11 is
  not offered.
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

**Seed carefully — removal is real only before consolidation.**
The correction mechanism (seed 5: remove the old fact by its
exact text, then add the corrected one) was measured working on
a fact minutes old (Test 3). A later cleanup pass on the same
account measured the limit: a fact in the account-level user
profile was removed cleanly, while two facts that had
consolidated into the bot's per-bot [profile] store refused
exact-text removal — the tool reported that no fact with exactly
that text was recorded — and no user-facing removal surface for
that store was found. So treat every seed as effectively
permanent once it has consolidated: state, in your own words,
only rules you mean to keep, and check the quote-back before
the conversation moves on. The moment to fix a seed is while it
is still new; a consolidated seed may not be takeable back.

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
  subtlety above.
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
  proved it). That verification was on a fact minutes old: facts
  consolidated into the per-bot [profile] store later refused
  the same removal (see the seed caution under module 00), so a
  correction the platform refuses is reported as refused, never
  as applied. Whether the server retains removed facts is not
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
  is read back from storage after creation and compared word for
  word with the approved text (the battery's routines matched).
  The instruction is self-contained: it names the workspace files
  it reads, the record it appends, and what it posts — because a
  run is a fresh context that holds only its instruction, the
  memory that reaches it, and the files it is told to read.
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
  them.
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
instructions field), its skills verbatim, and its routines
verbatim** — imported **paused**, with import-time parameter
prompts the template declares (measured: "Ask the importing user
for: Timezone"). It does not carry the title, any memory, or any
workspace file. `template/` in this pack holds the contents,
prepared in the repo:

- `template/description.md` — the description text, which is the
  instructions an imported bot starts with.
- `template/skills/` — the skill set, one SKILL.md per skill,
  in the form the account library holds them.
- `template/routines.md` — the routine definitions, each with its
  schedule, its parameter prompts, and its saved instruction
  verbatim.

Publishing the template in the app is a separate ticketed step,
outside this install; the repo remains the source of truth, and
file-based kit state still ships by the workspace route — a
template import delivers skills, routines, and instructions, and
the plan then creates the workspace files (procedures reference,
decision queue, run-record) the routines read.

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
   scaffolding, deleted when the install closes — and it is not
   a sandbox: from the moment it exists it shares the account's
   computer, skill library, and connectors (the two warnings).
2. **Set the source bot's description** to the text in
   `template/description.md`, placeholders filled — the name
   chosen above, the user's name. Role text is set by asking
   the bot in chat (measured: it saved to the bot's own profile;
   no settings-UI fields for it were found).
3. **Skills need no loading onto the bot.** The skill library is
   account-level: a skill staged into a template is one that
   exists in the library, installed verbatim (Test 8). If a pack
   skill is not yet in the library, add it there first, in the
   form `template/skills/` holds it.
4. **Create the three routines on the source bot** from
   `template/routines.md`, saved instructions verbatim,
   placeholders as written, left paused — and state each
   routine's parameter declaration ("Ask the importing user
   for: …", as the definition lists it) with the routine as you
   create it. The pack's definitions carry the declaration as a
   separate line for exactly this purpose.
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
   the description text; Skills — each SKILL.md in full;
   Routines — each routine's full text and cron, **and its
   parameter declaration**. There is no files section and no
   memory section; their absence is correct, not a gap. Check
   every routine shows its declaration before anyone publishes:
   whether the declaration attaches automatically when a routine
   is created, or only when it is stated as in step 4, is
   **unmeasured** — the battery observed the declaration present
   in a staged manifest and the prompt asked at import, and did
   not isolate the mechanism. The manifest check is therefore
   the control: a routine without its declaration showing is not
   ready, whatever the cause.
7. **Publish (the user's click, ticketed as above) and import.**
   Instantiating the template creates the new bot; the declared
   parameters are asked at import, and the routines arrive
   paused (measured). Enabling each routine afterwards is the
   user's act, per the jobs section.

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
read back as the user confirmed them; each routine created
paused-then-enabled per the plan, its saved instruction read back
verbatim against the approved text; the run-record file created
with its header; the procedures reference and decision queue in
the workspace; the egress decision recorded (signed in, with the
token warning shown — or not signed in).

*Deferred:* the first brief run lands inside its window and
appends its line; the first silent-watch line appears with no
post; the first memory audit runs and its findings are decided;
skill auto-discovery confirmed after the platform's list refresh
(invocation by name is the at-install evidence; discovery is
not). Each is ledgered in `SETUP-PLAN.md` with a due date, as the
wizard requires.
