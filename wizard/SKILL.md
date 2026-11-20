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
   `MODULE.md`, and report the result before moving on. "Installed" means
   verified, not written.

## Step 1 — Capability check

Before the interview, establish what this install can do. Check, and note
the answers for the gating step:

- Can you schedule recurring jobs (cron or equivalent)?
- Is a mailbox connected? A calendar? A task app?
- Is cloud storage with sharing connected (e.g. Google Drive)?
- Does the user have a host they control (a home server, a VPS)?
- Is this setup for one person, or will a second person with their own
  Muse participate?

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
   ticket rule protects against and confirm they mean it.)*
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

## Step 3 — Module selection

From `manifest.yaml`, compute the offerable set:

- Always offer **core-procedures** first; it is the foundation and every
  other module depends on it. If the user declines it, explain that the
  other modules assume it, and offer "procedures lite" (ticket rule +
  decision queue only) rather than nothing.
- Gate by capabilities: no scheduling → morning-brief installs as an
  on-demand brief instead of a scheduled one; no second person →
  household-hq is not offerable; no shared storage or no other agents →
  ai-exchange is not offerable; no host → infra-patterns is not offerable.
- Present the offerable modules as a checklist with their one-line pitches
  and disclosures. The user picks: all, none-but-core, or by number.

## Step 4 — The plan

Produce one plan document (show it in chat; also save it as
`SETUP-PLAN.md` in the workspace once approved):

- Selected modules, in dependency order.
- For each: files created/edited (paths), jobs scheduled (cadence,
  delivery), shared surfaces created, and the manifest disclosure lines.
- Every `<PLACEHOLDER>` that needs a user-supplied value, listed as
  questions (names to use, brief time and timezone, VIP senders for triage,
  household members, storage locations).
- Anything in the user's existing setup that conflicts, with your proposed
  resolution.

Wait for approval. Do not begin Step 5 on partial approval — ask which
parts are approved.

## Step 5 — Install, in dependency order

For each module:

1. Re-read its `MODULE.md` install section.
2. Copy/adapt its templates, filling placeholders from the approved plan.
3. Create its scheduled jobs with the cadences the user chose.
4. Run its verification checks. If a check fails, stop, report, and ask —
   do not improvise a fix that changes the plan.
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
