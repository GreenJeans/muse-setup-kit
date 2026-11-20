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
2. **Pinned source only.** Install from the files in this checkout, at its
   current commit. Never fetch module content from a URL at install time.
   Tell the user the commit hash you are installing from.
3. **Plan before changes.** Present one consolidated plan: every file you
   will create or edit, every scheduled job, every shared surface, with each
   module's reads/writes/network disclosure from the manifest. Wait for
   explicit approval. Approval covers exactly what was shown — if the plan
   changes, show it again.
4. **Merge, never overwrite.** The user may already have instructions,
   memory files, and habits. Read what exists, propose merges, and keep
   their wording where it doesn't conflict. A conflict is a question for the
   user, not a silent replacement.
5. **No credentials in chat.** If a module needs an account connection, use
   the platform's secure connection flow. Never ask the user to paste a
   password, token, or key into the conversation.
6. **Placeholders are not facts.** Templates contain `<PLACEHOLDERS>`. Fill
   them only from what the user tells you in this setup. Never carry over
   any example content as if it were the user's data.
7. **Verify each module after installing it**, using the checks in its
   `VERIFY.md`, and report the result before moving on. Checks split into
   *at-install* and *deferred*: a check that needs live operation (a
   scheduled brief arriving, a fresh session, days of data) is recorded in
   the plan's verification ledger as DEFERRED with a due date, and the
   brief (or a follow-up) surfaces it when due. "Installed" means every
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

Do not guess: if you cannot check a capability, ask.

## Step 2 — Interview

Ask these as short multiple-choice questions, one topic at a time. Use the
user's answers verbatim in the plan.

1. **Who is this for?** (a) Just me. (b) Me and one other person, who has
   (or will have) their own Muse. (c) A small group.
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
6. **Infrastructure:** (a) I have a host/server I control and want backup
   and health patterns. (b) Cloud only, skip infra. (c) Later.
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
  on-demand brief instead of a scheduled one, and skill-lifecycle's
  sweep and curator run on demand; no second person →
  household-hq is not offerable; no shared storage or no other agents →
  ai-exchange is not offerable; no host → infra-patterns is not offerable.
- If a module's manifest entry lists `degrades_without` and the user lacks
  that capability, offer the module in its degraded mode and say plainly
  what won't work (for example: evaluation-kit without other agents runs
  single-reviewer; the morning brief without scheduling runs on demand).
- Present the offerable modules as a checklist with their one-line pitches
  and disclosures. The user picks: all, none-but-core, or by number.

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

Wait for approval. Do not begin Step 5 on partial approval — ask which
parts are approved.

## Step 5 — Install, in dependency order

For each module:

1. Re-read its `MODULE.md` install section.
2. Copy/adapt its templates, filling placeholders from the approved plan.
3. Create its scheduled jobs with the cadences the user chose, and record
   each one in `JOBS.md` at the workspace root (name, cadence, what it
   owes, where it delivers). `JOBS.md` is the kit's scheduler-of-record:
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
