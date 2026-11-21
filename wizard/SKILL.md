# Setup Wizard — Muse Setup Kit

You are the installing agent. A user has pointed you at this repository and
asked you to set up their Muse with some or all of the kit's modules. Run
this wizard exactly as written. It is deliberately conservative: **you
propose, the user disposes, and nothing is applied before its plan is shown
and approved.**

## Ground rules (do not skip, do not paraphrase away)

1. **Read before you act.** Read `../docs/DESIGN.md` and `manifest.yaml` in
   this folder, and the `MODULE.md` of every module the user selects,
   before presenting the plan. If security-pack is selected — or a
   field module (a kit-library package from another maintainer) is
   ever in play — also read `../docs/library.md`: it carries the
   field-module rules that module 06's vetting points to.
2. **Pinned source only.** Before anything else, establish what this
   checkout is, one of two ways. If the user gave you a full commit
   hash (from the release page, not from inside this repo), compare it
   with `git rev-parse HEAD`: a mismatch stops the install. An
   abbreviated hash is not a user-supplied hash: anything short of
   the full hash takes the no-hash path below, even when the
   abbreviation uniquely prefixes HEAD — a prefix match proves
   nothing about where the abbreviation came from. If the
   user gave no hash, the checkout must sit exactly on a release tag
   (`git describe --tags --exact-match`): resolve the tag and the full
   hash, and state both in the plan ("installing v0.6, commit <full
   hash>") so the user can compare against the release page. A
   checkout on no tag and with no user-supplied hash stops the
   install — offer to check out the latest release tag, and never
   default to the current commit. Install only from files at that
   commit, and never fetch module content from a URL at install time.
   A tree with no `.git` at all — a copied tree, an extracted
   archive — can take neither path, and the tag remedy does not
   exist for it: there is nothing to check out from. Worse,
   `git rev-parse HEAD` run inside such a tree does not fail; it
   silently returns an *ancestor* repository's HEAD, a wrong pin
   that looks valid. Never take a pin from a tree whose git
   top-level is not the checkout itself (`git rev-parse
   --show-toplevel` must name the checkout). A `.git`-less tree is
   EVALUATION-only: the plan records the state as EVALUATION, the
   user-supplied commit if there is one (labeled user-supplied,
   unverified), and the file list as received.
   One exception, for evaluation installs (a dry run or a
   release-candidate rehearsal): the user may hand you a local tree
   with uncommitted changes. Then the plan records HEAD plus the
   dirty state (`git status --porcelain` and `git diff --stat HEAD`,
   verbatim) and is labeled EVALUATION, per UPGRADING.md. A
   production install never proceeds this way.
3. **Plan before changes.** Present one consolidated plan: every file you
   will create or edit, every scheduled job, every shared surface, with each
   module's reads/writes/network disclosure from the manifest. List
   externally visible items first, separately: every share or invite with
   exact recipients, every job that messages anyone, every account
   connection. Wait for explicit approval: approval must name what it
   covers ("approve 00, 01, 02" or "approve all"); "ok" or "looks good"
   is not approval — ask which parts. Approval covers exactly what was
   shown — if the plan changes, show it again.
4. **Merge, never overwrite.** The user may already have instructions,
   memory files, and habits. Read what exists, propose merges, and keep
   their wording where it doesn't conflict. A conflict is a question for the
   user, not a silent replacement.
5. **No credentials in chat.** If a module needs an account connection, use
   the platform's secure connection flow. Never ask the user to paste a
   password, token, or key into the conversation.
6. **Vet the kit first.** Before the interview, draft a vetting entry
   for this kit: its source, the full commit hash, which files you read
   in full — scoped honestly: if you read only the selected modules,
   the entry says so and names what was not read — and what the
   modules read, write, and contact over the network. It becomes
   the plan's first item and is approved with the
   plan, whether or not security-pack is selected. Where the entry
   lives: in module 06's vetting log when security-pack is installed;
   otherwise in `SETUP-PLAN.md` itself, as the plan's first item — an
   install without module 06 creates no other vetting file, and the
   entry is not homeless. Any third-party
   software a module installs gets its own vetting entry in the plan
   before installation.
7. **Placeholders are not facts.** Templates contain `<PLACEHOLDERS>`. Fill
   them only from what the user tells you in this setup. Never carry over
   any example content as if it were the user's data.
8. **Verify each module after installing it**, using the checks in its
   `VERIFY.md`, and report the result before moving on. Checks split into
   *at-install* and *deferred*: a check that needs live operation (a
   scheduled brief arriving, a fresh session, days of data) is recorded in
   the plan's verification ledger as DEFERRED, with its due date
   written as `due: YYYY-MM-DD` and an owner named (Step 5 item 4
   gives the ledger row format; kit_doctor reads the due date from
   that field). A check whose due is an *event* — "the first renewal
   after install", "the user's next conversation" — is ledgered with
   the event named in the row **and** a fallback `due:` date computed
   at install; the `due:` date is the binding one kit_doctor reads,
   and the event is what the check is actually waiting for. A morning brief surfaces due checks — the kit's module 02
   brief, or a brief-like daily job the user already runs (amend it,
   with approval, to read the plan). Otherwise — and whenever it is
   unclear whether anything brief-like will actually read the plan —
   the install also adds one line to the main instruction file:
   "At session start, check SETUP-PLAN.md for overdue deferred
   checks." The line is harmless when a brief also surfaces them.
   A deferred check with no way to surface is a failed check. Each
   verification report shows its evidence (file listings, scheduler
   output, hashes), not just PASS, and the handover names three checks
   the user can run personally. "Installed" means every
   at-install check passed and every deferred check is ledgered — never
   that a check was skipped silently.

## Step 0 — Audit first (optional, for existing setups)

If the user already has a working setup — their own procedures,
memory, jobs, or skills — offer this mode before Step 1. It is
**read-only**: the wizard writes nothing, creates nothing, and
schedules nothing in this mode. It produces one report:

1. **Inventory.** What exists: instruction and procedure files,
   memory stores, scheduled jobs (names and cadences), custom
   skills, connected accounts and services, and any approval or
   queue mechanism already in use. Read-only inspection only; where
   a fact cannot be checked without a write, say so instead of
   checking.
2. **Map.** Each inventory item against the kit's modules: already
   covered (and by what), partially covered, or absent. Where the
   user's existing piece is stronger than the kit's, say so — the
   map is not a sales document.
3. **Recommend.** Which modules would add something the setup
   lacks, which would duplicate what exists (skip those), and the
   reading cost of the recommended set, from the manifest's audit
   figures.

The report ends the mode. Installing anything starts the normal
wizard at Step 1, with the audit attached to the plan as context —
the plan still needs its own approval, and the audit's existence
does not count as one.

## Step 1 — Capability check

Before the interview, establish what this install can do. Check, and note
the answers for the gating step:

- Can you schedule recurring jobs (cron or equivalent)?
- Is a mailbox connected? A calendar? A task app?
- Is cloud storage with sharing connected (e.g. Google Drive)?
- Does the user have a host they control (a home server, a VPS)?
- Is this setup for one person, or will a second person with their own
  Muse participate?
- Does the user work with other AI agents (other vendors' models, coding
  agents) they might exchange work with?
- Can you run local scripts (shell / Python 3) and read files on this
  machine, including session transcripts where the platform keeps them?
- **Which billing bucket does this session draw on?** An install is
  heavy work: a full one reads on the order of 34,000 words of kit and
  writes dozens of files; a Starter install is about 15,000 of that.
  If neither you nor the user can name the bucket (subscription, API
  org, router), pause and check before planning — this is module 09's
  rule 2 applied to the kit itself, and it is a stop condition, not a
  footnote. You usually cannot verify the bucket from inside the
  session — there is no source to read and no canary to run — so the
  user's word is the source here: name the bucket, and record it in
  the plan as user-stated, not verified. If the bucket still cannot
  be named after checking, the unknown path is this: record it in
  the plan as UNKNOWN, flagged as a standing stop-condition item.
  The interview, planning, and an EVALUATION install may proceed;
  a production install may complete only with the flag carried in
  the plan and named at handover; and no heavy run beyond the
  install itself starts until the bucket is named. The flag, not
  silence, is the path — an unrecorded UNKNOWN is a failed check,
  not a footnote.

Map the answers to the manifest's requirement tokens:

| Capability answer | Token |
|---|---|
| Scheduling available | `scheduling` |
| A second participating person | `second-person` |
| Shared documents (e.g. Drive) | `shared-docs` |
| A shared task app | `shared-tasks` |
| Shared cloud storage | `shared-storage` |
| Other agents in use | `other-agents` |
| A host the user controls | `own-host` |
| Shell / Python 3 execution | `shell-python` |

File-based job definitions count as `scheduling` when the platform
actually runs them — a scheduler, a heartbeat, a session hook,
anything that fires the job files on cadence. The degraded case is a
platform that cannot run jobs at all. A workspace where job files
exist but nothing fires them is the no-scheduling case, and the plan
says so plainly at selection time ("these jobs are recorded, but
nothing will fire them; the brief and the checks happen when you
ask"), with the affected modules offered in their degraded modes per
the matrix.

Do not guess: if you cannot check a capability, ask.

## Step 2 — Interview

Ask these as short multiple-choice questions, one topic at a time. Use the
user's answers verbatim in the plan. Skip a question whose answer
cannot change this install — because the profile is already chosen,
or the module it gates is not offerable — and say in one line why you
are skipping it. Collecting answers nothing consumes teaches the
user their answers don't matter.

1. **Who is this for?** (a) Just me. (b) Me and one other person, who has
   (or will have) their own Muse. (c) A small group. *(If (c):
   household-hq installs in its two-person shape for the user plus one
   named coordinator, with a partner checkpoint per additional person;
   if the shared surfaces cannot support the group, say so at selection
   time rather than improvising a group mode.)*
2. **How much autonomy should the agent have by default?** (a) Ask before
   almost everything. (b) Reversible work on its own; irreversible actions
   (send/buy/book/file/delete) need my approval each time — *the kit's
   recommended default, implemented by the ticket rule.* (c) Broad autonomy
   with after-the-fact reporting. *(If they pick (c), explain what the
   ticket rule protects against and confirm they mean it.)* The answer
   changes the installed procedures: (b) installs §2 as written; (a)
   additionally requires tickets for drafts and internal writes the user
   names; (c) replaces pre-approval with a same-day reporting duty for
   the classes the user names, and the plan records that deviation in
   the user's words. Module 00's Install step applies the variant.
3. **Daily rhythm?** (a) A morning brief. (b) A morning brief plus inbox
   triage during the day. (c) No routine messages; on-demand only.
4. **Other AI agents?** Do you use other AI assistants (other vendors'
   models, coding agents) that you'd like exchanging work with this one?
   (a) Yes. (b) Not now. (c) What would that even do? *(Explain module 04
   briefly, then re-ask.)*
5. **Memory:** (a) Start fresh with the kit's schema. (b) Migrate my
   existing memory files into the schema. (c) Leave my memory alone.
   *(This question only bites when a memory-dependent module is in
   play; on a Starter-only path, skip it per the note above and
   record memory as untouched. If (c): the modules that depend on
   the memory schema — ai-exchange, evaluation-kit, skill-lifecycle
   — are not offerable; say so plainly at selection time.)*
6. **Infrastructure:** (a) I have a host/server I control. (b) Cloud
   only. *(No module gates on this since v0.4 — infra patterns are a
   reference document, docs/patterns/infra-patterns.md, not an
   install. Note the answer in the plan; a host user may want module
   02's watches pointed at it later.)*
7. **Existing work:** Name any ongoing workstreams or projects the agent
   should treat as separate topics (each gets a SCOPE.md), and point to
   the file the agent reads as its main instructions, if one exists. If
   none exists, the install creates one (`INSTRUCTIONS.md`) and module 00
   adds the procedures pointer to it.

## Step 3 — Module selection

From `manifest.yaml`, compute the offerable set:

- Always offer **core-procedures** first; it is the foundation and every
  other module depends on it. If the user declines it, explain that the
  other modules assume it, and offer "procedures lite" (ticket rule +
  decision queue only) rather than nothing.
- Gate by capabilities, per `docs/capability-profiles.md` (the matrix
  of what each capability buys, generated from the manifest): a module
  whose `requires` are unmet is not offerable; a module whose
  `degrades_without` is unmet is offered in its degraded mode, saying
  plainly what won't work, per the matrix's degradation notes.
- Offer the manifest's **profiles first** (Starter, then Standard),
  each with its audit word count from the manifest, then the full
  checklist. First time, the sensible default is Starter; modules can
  be added later, one at a time (UPGRADING.md). The user picks: a
  profile, all, none-but-core, or by number.
- State each offered module's rehearsal status from its manifest
  `rehearsed_at` field, and check docs/REHEARSALS.md for the record.
  The test is mechanical — compare `rehearsed_at` against this
  checkout. If it names this tag or commit, say "rehearsed at this
  pin." If it names an earlier tag or commit — the module was
  rehearsed, then changed — the words are "rehearsed at <what it
  names>; changed since — unrehearsed at this pin." Only when
  `rehearsed_at` is empty, with no rehearsal anywhere in the ledger,
  say "unrehearsed at this pin — you would be the first." Never let
  the plan imply a rehearsal the ledger doesn't show.
- If a module's manifest entry has `tiers`, present the default
  tier (Lite, for skill-lifecycle) as the offer, with its share of
  the reading cost; name the higher tier, what it adds, and the
  condition that triggers offering it (for skill-lifecycle: 5 or
  more custom skills). The plan records the tier chosen.

## Step 4 — The plan

Produce one plan document (show it in chat, and save it as
`SETUP-PLAN.md` in the workspace, marked "presented for approval";
approval updates its status line):

- Selected modules, in dependency order.
- For each: files created/edited (paths), jobs scheduled (cadence,
  delivery), shared surfaces created, and the manifest disclosure lines.
- Every `<PLACEHOLDER>` that needs a user-supplied value, listed as
  questions (names to use — including the agent's own name, the partner's
  name and their agent's name, and other agents' names for the Exchange —
  brief time and timezone, VIP senders for triage, the shield's
  immediacy set (the user's bank, toll operator, package carrier,
  and key services, each with every sending domain and address
  they use), household members,
  storage locations, HQ options: food layer and change detector in/out).
- For two-person installs, **partner checkpoints** are plan items in
  their own right: the partner approves the Principles doc, and reads
  their agent's setup prompt in full before pasting it. Module 03 is not
  installed until those clear or are ledgered as deferred with the
  partner named as the owner.
- Anything in the user's existing setup that conflicts, with your proposed
  resolution.

Expect a short second question round here: several placeholders (the
agent's own name, brief time and timezone, VIP senders, the shield's
immediacy set) are collected
at plan time rather than in the interview, because the answers depend
on which modules were selected. The plan also states every optional
component's decision explicitly — installed or not installed —
including module 02's triage scan, money watch, and promises ledger
and module 03's
food layer and change detector; an unrecorded "not installed" is
how features get silently dropped or silently assumed. Optional
components carry their own rehearsal status, read from
docs/REHEARSALS.md the same way as a module's, and the plan states
it — a component with no rehearsal row is offered as unrehearsed,
by name.

When a plan-time answer is unavailable — the user doesn't know
yet, or a scripted run has no one to ask — the value used is
recorded in the plan as an *assumption*, marked as one, never
presented as the user's answer. Kit defaults cover the mechanical
values (brief at 07:00 in the user's timezone; the triage window
is the user's waking hours); an assumption the user later corrects
is a plan edit, re-approved like any other.

Collect every placeholder answer first, then re-render the plan in its
final form with zero `<PLACEHOLDER>` tokens remaining. Placeholder
answers are not approval. Ask for explicit approval of that exact final
plan. Do not begin Step 5 on partial approval — ask which parts are
approved.

## Step 5 — Install, in dependency order

For each module:

1. Re-read its `MODULE.md` install section.
2. Copy/adapt its templates, filling placeholders from the approved plan.
3. Create its scheduled jobs with the cadences the user chose, and record
   each one in `JOBS.md` at the workspace root (name, cadence, what it
   owes, where it delivers). A "created job" means: the scheduler entry
   where the platform provides one; where the workspace is file-based
   and no scheduler entry exists, a job file at `jobs/<name>.md`
   holding the cadence, instructions, and delivery target, plus its
   `JOBS.md` entry — that pair is the job, and it is the evidence the
   module's VERIFY checks cite. `JOBS.md` is the kit's scheduler-of-record:
   the brief's detector-silence check and the memory linter read it.
4. Run its `VERIFY.md` at-install checks. If a check fails, stop, report,
   and ask — do not improvise a fix that changes the plan. Ledger every
   deferred check in `SETUP-PLAN.md`. Ledger rows take one shape:
   the module, the check, its owner, and the due date written as
   `due: YYYY-MM-DD`. kit_doctor reads the due date from that field,
   so keep other dates out of the row — a completion note's date
   belongs in the install log, not the ledger row. Where a VERIFY
   due is an event rather than a date (a first renewal, a next
   conversation), the row names the event in the check text and
   `due:` carries the fallback date the VERIFY names — computed at
   install, never left for the reader to invent.
5. Log the module, its source commit, and the verification result in
   `SETUP-PLAN.md`. For every file the install created or copied from
   the kit (procedures, filled templates, copied tools — not
   locally-authored content like memory pages), also record its
   baseline line in the plan's `## Installed files (baseline)`
   section, in one of two forms. Static files — content the kit
   supplied, which changes only by an approved edit — take a hash:
   `- installed: <path relative to the workspace> sha256:<sha256 of the file as installed>`.
   Accumulating files — content that grows by design in ordinary
   use (the decision queue, `JOBS.md`, ledgers) — take the word
   instead: `- installed: <path> accumulating`. Hashing an
   accumulating file would make ordinary use read as drift at every
   upgrade, so the doctor never diffs them; the line still puts
   them on the install's inventory for UPGRADING and UNINSTALL.
   This baseline is what makes upgrades mechanical: `kit_doctor.py`
   reports any hash-baselined file that has been edited since
   install, and UPGRADING.md uses that list as its conflict list.
   Re-stamp a static file's line whenever an approved change
   rewrites it (an upgrade, an approved skill-style edit the user
   asked for) — the baseline always describes the last approved
   state. One exception to the hash form: the main instruction file,
   when this install creates or edits it, is recorded `accumulating`,
   never hashed. It is the user's front door — the file they are
   most likely to edit by hand — and hashing it would make their
   first hand edit read as drift. The pointer line it carries is
   verified by module 00's checks, not by the baseline.

## Step 6 — Handover

Close with a short summary:

- What is live now, and what each piece does in one line.
- The three habits that make it work: clear the decision queue by number;
  correct the agent's memory when it's wrong (corrections are the system's
  training signal); never approve a ticket whose details have changed.
- When the first brief will arrive and what it will contain.
- How to uninstall: every artifact is a file or a named job; list them.

Then stop. Do not continue into configuring optional extras the user didn't
select.
