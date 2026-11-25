---
name: kit-bootstrap
description: Use this at the start of a session or routine run when the agent needs its kit bearings — workspace files, open decisions, and what its routines have done lately.
---

# Kit bootstrap

Pack-authored for the Muse Setup Kit's OpenBot profile. The
platform surfaces it uses were measured in the 2026-11-25
battery (OpenBot v0.78.0: routines verbatim with full tools,
fires at 0–3 seconds of drift, files as the memory); the
skill itself is unrehearsed.

1. Read the workspace run-record's most recent lines. State,
   in one or two lines, which routines ran, which are
   overdue against their schedules (allow a few minutes of
   drift before calling a run late; a window missed across a
   host sleep gap is named as missed), and any run whose
   recorded outcome was a failure.
2. Read the decision queue. State how many items are open
   and which is oldest. Do not decide any of them; the user
   clears the queue by number.
3. If `SETUP-PLAN.md` is in the workspace, check its
   deferred checks: name any whose due date has passed, with
   the check and its owner.
4. Report what you could not inspect — a file that is
   absent, a store you cannot list — as unverified, never as
   empty or fine. Absence of evidence is a finding, not a
   pass. Your own account of your routines is not evidence;
   the run-record is.
