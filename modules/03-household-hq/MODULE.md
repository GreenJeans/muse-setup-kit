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
- **Memory layer** — shared cloud docs: an **Agents' Notebook** (each
  agent has a section; dated entries; the other agent reads it in their
  morning routine), an **Ops sheet** (standing reference: trips, expiry
  dates, projects), and a **Principles & Autonomy** doc (template included)
  stating what each agent may do on shared surfaces without asking.
- **Food layer (optional)** — a shared recipe/meal-plan app if the
  household cooks from one library.

## Rules that make it work

- **One writer per surface section.** Your agent writes its notebook
  section; the other agent writes theirs. Nobody edits the other's words —
  corrections are new dated entries.
- **Shared surfaces hold shared facts only.** Never gifts (surprises die),
  finances, health detail, or anything one person hasn't agreed to share.
  The notebook is a coordination surface, not a diary.
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
   `principles.template.md`; share them with exactly the two people.
2. Create the shared lists and the three tags in the task app.
3. Each person pastes a short setup prompt into *their own* agent (the
   wizard generates it): it names the surfaces, the notebook section, and
   the principles doc, and instructs the agent to check the notebook in
   its morning routine.
4. Pilot on one real project (a trip works well) before making it the
   default for everything.

## Verify

- Person A's agent leaves a notebook note; person B's agent surfaces it in
  B's next brief, attributed and dated.
- A task tagged `decision` appears in both briefs until resolved.
- Check the sharing settings: the surfaces are shared with the two people
  and no one else — verify at the source, not from a report.
