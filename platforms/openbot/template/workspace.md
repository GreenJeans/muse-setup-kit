# Template contents — workspace starter files

The workspace files the routines read are created at install,
in the agent's workspace, from the starters below. Each block
is the file's complete starting content, with
`<PLACEHOLDERS>` filled from the install record. The formats
are the ones the routine instructions, the skills, and the
overlay's Verify step already assume — a starter that drifts
from them breaks the readers, so the shapes here are fixed
and the content is the install's.

## `run-record.txt`

Created with its header; every routine appends one line per
run below it, posted or silent. The header names the file,
the agent, and the creation date, so a record found out of
context still says what it is.

---BEGIN FILE---
# run-record — <AGENT NAME> — created <DATE>
---END FILE---

Appended lines take the form the routine instructions
prescribe: `<routine name> run at <timestamp> — <one-line
outcome>`.

## `decision-queue.md`

The numbered queue the brief surfaces and the user clears by
number. Items are numbered in the order raised and never
renumbered; a cleared item keeps its number and gains its
disposition, so a brief's "item 3" means the same thing all
week.

---BEGIN FILE---
# Decision queue

Cleared by the user, by number. Silence is never approval for
an irreversible action.

## Open

<!-- 1. <the decision, in one line> — raised <DATE> -->

## Cleared

<!-- 1. <the decision> — <disposition>, <DATE> -->
---END FILE---

## `SETUP-PLAN.md`

The install record: what was installed, what the seed actually
says, what is still owed. The weekly audit routine reads its
deferred-checks section; the overlay's deferred-checks rule
lives here because `AGENTS.md` binds in chat only and cannot
surface them on its own.

---BEGIN FILE---
# Setup plan — <AGENT NAME>

Installed <DATE> from the Muse Setup Kit, openbot profile, at
pin <PIN>. Platform: OpenBot <VERSION> (image tag pinned);
provider CLI: <PROVIDER + VERSION at install>. Billing
bucket: <BUCKET, user-stated>.

## Agents in this container

<!-- Every agent already in this container, named at install
— each one holds the access this install uses (warning 1).
Later additions get their own dated entries. -->

## AGENTS.md seed log

<!-- The seed as put in place: the text, the date, and the
fresh-conversation check that showed it binding. Later edits
get their own dated entries — never an annotation underneath
an earlier state. -->

## Access mode and grants

<!-- One dated sub-entry per reading or change. -->

### As found — <DATE>

<!-- Access mode (Full access / Ask first / Workspace only)
and any credential grants, exactly as found before the
install changed them, read from the app — not from the
agent's account of them. Local-scripts API: off (confirmed
<DATE>). -->

### Confirmed — <DATE>

<!-- The mode and grants as the user confirmed them after
the install's changes. Every grant is "Only this agent".
Every later change gets its own dated sub-entry. -->

## Egress

<!-- Egress measured (overlay, Egress; Test 7, Pass):
branch + tag push under a scoped "Only this agent" grant.
Credential granted: none / "Only this agent" (scope: <SCOPE>)
— the user's decision, recorded either way. Egress rides
the ticket rule. Analytics: off at first run (confirmed
<DATE>) — recorded as known egress either way. -->

## Backup

<!-- Where the backup of the data volume (/data) is, and
its date. The backup exists before any upgrade; migrations
are one-way. -->

## Routines and cadence

<!-- One line per routine: name, schedule as read back from
the routines store. Reconciliation reads the store, never
the agent. -->

## Deferred checks

<!-- One line per check: what will be verified, its due
date, and what surfaces it. A check with no routine to
surface it is a failed check. -->
---END FILE---

## Memory files — module 01's shapes, in the workspace

Module 01's architecture ships as workspace files on this
platform (the platform brings no schema of its own), created
from the module's own templates at install. The starters
below fix only the shapes this pack's routines and skills
assume; the module's `SCHEMA.template.md` governs the rules.

## `MEMORY.md`

The curated long-term file: current state at top, replaced
claims moved to Superseded in the same edit, provenance in
the header.

---BEGIN FILE---
# MEMORY.md

<!-- Curated long-term memory: durable facts, preferences, and
commitments. Keep it tight — raw day-to-day detail belongs in
the daily logs.
schema_version: 1
last_verified: <YYYY-MM-DD>
sources: daily logs in memory/logs/; live sources named
per-claim via (verify: ...) pointers. -->

## Facts

- <One durable fact per bullet, stated as it is true now.
  When a fact changes, rewrite its bullet and move the old
  claim to Superseded below.>

## People

- <Name — relationship, and the one or two facts that matter
  most. Detail lives on their page in memory/people/.>

## Preferences

- <How the user likes things done, in their words where
  possible.>

## Commitments

- <Standing watches, promises, and recurring obligations,
  with cadence.>

## Superseded

<!-- Replaced claims, newest first:
- <YYYY-MM-DD>: <old claim> — superseded by <new claim>.
  Source: <where>. -->
---END FILE---

## Daily logs — `memory/logs/<YYYY-MM-DD>.md`

One file per day: what happened, decisions made, exact
figures with their sources. Raw sources are immutable once
written; exact numbers, dates, and amounts are answered from
the log or the live source, never from a compiled page alone.

---BEGIN FILE---
# <YYYY-MM-DD>

<!-- The day's record: what happened, decisions, exact
figures with sources. Written once; corrections are new
entries, not rewrites. -->
---END FILE---

Person and group pages live in `memory/people/` and
`memory/groups/`, one page each, current state at top with
a `## History` section for replaced claims — the module's
schema governs their shape.

## `watch-target.txt` — created by an install step, not a starter

The watch routine's creation answer names what it watches: a
file or source, and the condition that counts as a trip.
When the answer names a workspace file, that file must exist
before the routine is first enabled — a watch over a missing
file cannot distinguish "nothing to report" from "nothing
there". Creating it is an install step: the user states its
starting content (for a content-condition watch, a line that
does not trip the condition), the agent creates the file
with exactly that content and reads it back. When the answer
names an external source instead, the install records the
source and the trip condition in `SETUP-PLAN.md` and there
is no file to create. Either way, the Verify step checks the
target exists as the answer describes it before the watch
routine is enabled.
