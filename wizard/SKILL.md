# Setup Wizard — Muse Setup Kit

You are the installing agent. A user has pointed you at this repository and
asked you to set up their Muse with some or all of the kit's modules. Run
this wizard exactly as written. It is deliberately conservative: **you
propose, the user disposes, and nothing is applied before its plan is shown
and approved.**

## Ground rules (do not skip, do not paraphrase away)

1. **Read before you act.** Read `../docs/DESIGN.md` and `manifest.yaml` in
   this folder, and the `MODULE.md` of every module the user selects,
   before presenting the plan.
2. **Pinned source only.** Before anything else, compare this checkout's
   full commit hash with the hash the user gave you (from the release
   page, not from inside this repo). If the user gave none, or the two
   differ, stop and ask — never default to the current commit. Install
   only from files at that commit, and never fetch module content from a
   URL at install time. One exception, for evaluation installs (a dry
   run or a release-candidate rehearsal): the user may hand you a local
   tree with uncommitted changes. Then the plan records HEAD plus the
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
   in full, and what the modules read, write, and contact over the
   network. It becomes the plan's first item and is approved with the
   plan, whether or not security-pack is selected. Any third-party
   software a module installs gets its own vetting entry in the plan
   before installation.
7. **Placeholders are not facts.** Templates contain `<PLACEHOLDERS>`. Fill
   them only from what the user tells you in this setup. Never carry over
   any example content as if it were the user's data.
8. **Verify each module after installing it**, using the checks in its
   `VERIFY.md`, and report the result before moving on. Checks split into
   *at-install* and *deferred*: a check that needs live operation (a
   scheduled brief arriving, a fresh session, days of data) is recorded in
   the plan's verification ledger as DEFERRED with a due date and an
   owner. A morning brief surfaces due checks — the kit's module 02
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
  heavy work: a full one reads on the order of 20,000 words of kit and
  writes dozens of files; a Starter install is about a fifth of that.
  If neither you nor the user can name the bucket (subscription, API
  org, router), pause and check before planning — this is module 09's
  rule 2 applied to the kit itself, and it is a stop condition, not a
  footnote.

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

Do not guess: if you cannot check a capability, ask.

## Step 2 — Interview

Ask these as short multiple-choice questions, one topic at a time. Use the
user's answers verbatim in the plan.

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
   *(If (c): the modules that depend on the memory schema —
   ai-exchange, evaluation-kit, skill-lifecycle — are not offerable;
   say so plainly at selection time.)*
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
- Gate by capabilities: no scheduling → morning-brief installs as an
  on-demand brief instead of a scheduled one, skill-lifecycle's
  sweep and curator run on demand, memory-architecture's linter runs
  by hand, and security-pack's grants inventory is a manual monthly
  chore; no shell/python → the linter and the curator degrade to
  manual reviews against the same checklists; no second person →
  household-hq is not offerable; no shared storage or no other agents →
  ai-exchange is not offerable.
- If a module's manifest entry lists `degrades_without` and the user lacks
  that capability, offer the module in its degraded mode and say plainly
  what won't work (for example: evaluation-kit without other agents runs
  single-reviewer; the morning brief without scheduling runs on demand).
- Offer the manifest's **profiles first** (Starter, then Standard),
  each with its audit word count from the manifest, then the full
  checklist. First time, the sensible default is Starter; modules can
  be added later, one at a time (UPGRADING.md). The user picks: a
  profile, all, none-but-core, or by number.
- State each offered module's rehearsal status from its manifest
  `rehearsed_at` field, and check docs/REHEARSALS.md for the record.
  A module with no rehearsal at or near the pinned commit is offered
  with the words "unrehearsed at this pin — you would be the first."
  Never let the plan imply a rehearsal the ledger doesn't show.

## Step 4 — The plan

Produce one plan document (show it in chat; also save it as
`SETUP-PLAN.md` in the workspace once approved):

- Selected modules, in dependency order.
- For each: files created/edited (paths), jobs scheduled (cadence,
  delivery), shared surfaces created, and the manifest disclosure lines.
- Every `<PLACEHOLDER>` that needs a user-supplied value, listed as
  questions (names to use — including the agent's own name, the partner's
  name and their agent's name, and other agents' names for the Exchange —
  brief time and timezone, VIP senders for triage, household members,
  storage locations, HQ options: food layer and change detector in/out).
- For two-person installs, **partner checkpoints** are plan items in
  their own right: the partner approves the Principles doc, and reads
  their agent's setup prompt in full before pasting it. Module 03 is not
  installed until those clear or are ledgered as deferred with the
  partner named as the owner.
- Anything in the user's existing setup that conflicts, with your proposed
  resolution.

Expect a short second question round here: several placeholders (the
agent's own name, brief time and timezone, VIP senders) are collected
at plan time rather than in the interview, because the answers depend
on which modules were selected. The plan also states every optional
component's decision explicitly — installed or not installed —
including module 02's triage scan and module 03's food layer and
change detector; an unrecorded "not installed" is how features get
silently dropped or silently assumed.

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
   deferred check in `SETUP-PLAN.md` with its due date.
5. Log the module, its source commit, and the verification result in
   `SETUP-PLAN.md`.

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
