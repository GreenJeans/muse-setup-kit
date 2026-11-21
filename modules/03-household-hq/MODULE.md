# Module 03 — Household HQ

**Reads:** the shared surfaces both people agreed to share.
**Writes:** shared lists, a shared notebook, a shared ops sheet.
**Network:** your shared accounts. **Jobs:** an optional change detector.

## Purpose

Two people, each with their own agent, need to coordinate a household
without either agent seeing the other's private world. There is (today) no
direct agent-to-agent channel — and it turns out you don't need one. Shared
*state* does the job: a task layer both agents work, a memory layer both
agents read, and a notebook where agents leave each other dated notes.

## Architecture

- **Task layer** — a shared task app. Lists per domain (household, trips,
  projects). Three tags do most of the work: `waiting` (blocked on the
  other person), `decision` (needs a human call), `urgent`. Field
  discipline: every task has done-criteria; comments carry the per-task
  context so the list stays scannable.
- **Memory layer** — shared cloud docs: an **Agents' Notebook** (sections
  named for their writer — "From <AGENT A>" is A's outbox, read by B;
  dated entries; the other agent reads it in their morning routine), an
  **Ops sheet** (standing reference: trips, expiry dates, projects), and
  a **Principles & Autonomy** doc (template included) stating what each
  agent may do on shared surfaces without asking.
- **Food layer (optional)** — a shared recipe/meal-plan app if the
  household cooks from one library.

## Rules that make it work

- **One writer per surface section.** Your agent writes its notebook
  section; the other agent writes theirs. Nobody edits the other's words —
  corrections are new dated entries.
- **Shared surfaces hold shared facts only.** Never gifts (surprises die),
  finances, health detail, or anything one person hasn't agreed to share.
  The notebook is a coordination surface, not a diary. Where those
  records live instead is procedures §13 (sensitive records): local
  files only, each person's own.
- **Standing authorizations are written down.** If one person wants the
  other's agent to just handle a class of request (e.g. "a book request in
  the notebook means deliver it"), that rule lives in the Principles doc,
  dated, in the grantor's words.
- **The brief enforces hygiene.** Each agent's morning brief scans the
  `decision` and `waiting` tags and flags past-due shared tasks; a monthly
  sweep clears undated tasks.
- **A change detector, not a poll.** A small script diffs the shared
  surfaces and wakes an agent only when something changed. Silence means
  no change, and the detector's own liveness is checked like any watch
  (module 02).

## Install

1. Create the shared folder, notebook, ops sheet, and Principles doc from
   `principles.template.md` — unshared for now. Sharing happens only
   after the partner checkpoint (step 4) clears; see step 4a. The
   notebook's own header states the section convention (sections named
   for their writer).
2. Decide the options explicitly, with both people: the **food layer**
   (a shared recipe/meal app) in or out, and the **change detector** job
   in or out. Record both decisions in the plan; neither is a default.
3. Create the shared lists and the three tags in the task app. The
   `urgent` tag is consumed by the brief/triage machinery (module 02):
   an urgent-tagged task interrupts like a triage item.
4. Generate the partner's setup prompt from
   `partner-setup-prompt.template.md`. **Partner checkpoint:** the
   partner reads the prompt and the Principles doc and approves both
   before pasting anything into their agent — the prompt is an
   instruction set written by someone else's setup process, and module
   06's verify-before-install discipline applies to it. The installing
   person's own agent gets the same content as a local instruction.
   If the checkpoint cannot clear during this install, ledger it in
   `SETUP-PLAN.md` as DEFERRED with the partner named as owner — and
   sharing still waits. A deferred checkpoint never means "share now,
   approve later."
4a. **Share the surfaces** with exactly the two people — only now that
   the checkpoint has cleared — and verify the sharing at the source.
5. **Amend the brief:** if module 02 is installed, add the notebook to
   the installed brief job now — the `[IF household-hq installed]`
   source block in `brief.template.md` (the other agent's notebook
   section, surfaced attributed and dated). Without this step the
   notebook is written and never read. If module 02 is not installed
   (this module's degraded mode), record a notebook check as an
   on-demand chore in `JOBS.md` and tell the user plainly: the notebook
   surfaces only when someone asks, until a brief exists.
6. Pilot on one real project (a trip works well) before making it the
   default for everything.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
