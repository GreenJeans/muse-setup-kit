# Claude Duet

Platform material for running the kit on Claude Duet, a hosted Claude
assistant with fixed rules: no editable instruction file, no persona
file, a built-in brief, routines with a minimum interval, and an
ephemeral shell with one persistent folder.

- `WIZARD.md` — the overlay on `wizard/SKILL.md` for the manifest's
  `duet` profile (modules 00, 06, 09, 10). The installing agent reads
  it after the wizard. It is counted in the profile's audit figure.
- `skill/SKILL.md` — a thin bootstrap packaged as a Claude skill. It
  asks the user for a release, clones and verifies it, and hands over
  to the wizard and the overlay at that pin. It carries no module
  content, so it does not need a new copy for each release. It is
  counted in the profile's audit figure.
- This README is for people; the installing agent does not need it.

**Status: rehearsed in part at v0.13-rc1; changed since.** One test
install ran at v0.13-rc1 (docs/REHEARSALS.md run 22). Files and
at-install checks worked; the routines could not, because a Duet
routine run has no project folder. The routines now read one
generated Claude Doc, the **kit state doc**, which the hosting chat
syncs from `kit/` when the user asks. Module 10's surfacing and the
weekly pass depend on that doc: an item added since the last sync
waits for the next one. That design is unrehearsed. The token
answers behind the profile are in docs/capability-profiles.md
(Platform answers: Claude Duet).

## Adding the skill to a Claude account

Zip the `skill/` folder (the zip holds `SKILL.md` at its top level)
and upload it as a custom skill in Claude's settings. Read it in full
first, as module 06 asks of any skill. Skills added to an account do
load in Duet sessions (checked at v0.13-rc1).

The copy in this folder is the source of truth. When a release
changes it (its description included), re-save it in your account:
the skill tells you if your saved copy differs from the release you
checked out.

Without the skill, a Duet user can paste the README quickstart with
the release tag and ask Duet to read `platforms/duet/WIZARD.md` after
the wizard; the procedure is the same.
