# Template contents — workspace starter files

A template carries no files (measured, §6 probe: the staged
manifest has no files section), so the workspace files the
routines read are created at install, in the bot's workspace,
from the starters below. Each block is the file's complete
starting content, with `<PLACEHOLDERS>` filled from the install
record. The formats are the ones the routine instructions, the
skills, and the overlay's Verify step already assume — a starter
that drifts from them breaks the readers, so the shapes here are
fixed and the content is the install's.

## `run-record.txt`

Created with its header; every routine appends one line per run
below it, posted or silent. The header names the file, the bot,
and the creation date, so a record found out of context still
says what it is.

---BEGIN FILE---
# run-record — <AGENT NAME> — created <DATE>
---END FILE---

Appended lines take the form the routine instructions prescribe:
`<routine name> run at <timestamp> — <one-line outcome>`.

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

The install record: what was installed, what the seeds actually
say and where they sit, what is still owed. The weekly audit
routine reads its deferred-checks section; the overlay's
deferred-checks rule lives here because the platform has no
instruction file to carry it.

---BEGIN FILE---
# Setup plan — <AGENT NAME>

Installed <DATE> from the Muse Setup Kit, grok profile, at
pin <PIN>. Billing bucket: <BUCKET, user-stated>.

## Seed log

<!-- One entry per seed, from the bot's quote-back, not from
the proposal: the fact as stored, the store it was confirmed
in, the date. -->

## Auto-review lists

<!-- One dated sub-entry per reading or change — never an
annotation underneath an earlier state. An "(empty)" line with
a rule noted below it reads as a self-contradiction to a later
audit (measured, run 29); dated sub-entries do not. -->

### As found — <DATE>

<!-- Approvals mode, both lists, and any per-tool connector
settings (Always allow / Auto-review / Needs approval /
Blocked), exactly as the user read them in the app and dictated
them — the bot cannot read its own Auto-review settings. Their
scope (per-bot or account-wide) is unmeasured; see the
overlay. -->

### Confirmed — <DATE>

<!-- The lists and per-tool settings as the user confirmed
them after the install's changes. Every later change gets its
own dated sub-entry. -->

## Egress

<!-- Signed in for shell git access, with the token warning
shown — or not signed in. The user's decision, recorded either
way. -->

## Deferred checks

<!-- One line per check: what will be verified, its due date,
and what surfaces it. A check with no routine to surface it is
a failed check. -->
---END FILE---

## `watch-target.txt` — created by an install step, not a starter

The watch routine's import answer names what it watches: a file
or source, and the condition that counts as a trip. When the
answer names a workspace file, that file must exist before the
routine is first enabled — a watch over a missing file cannot
distinguish "nothing to report" from "nothing there". Creating
it is an install step: the user states its starting content
(for a content-condition watch, a line that does not trip the
condition), the bot creates the file with exactly that content
and reads it back. When the answer names an external source
instead, the install records the source and the trip condition
in `SETUP-PLAN.md` and there is no file to create. Either way,
the Verify step checks the target exists as the answer
describes it before the watch routine is enabled.
