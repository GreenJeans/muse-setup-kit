# Worked example — a spaces audit and redesign (module 12)

The run module 12 distills: the maintainer's own setup,
audited and redesigned end to end in one day. Generalized for
publication — the shape of the numbers is real (counts of
pages, the sidebar arithmetic, one wrong figure), the
identifying details are not.

## Starting state

Fourteen spaces, twelve of them pinned in the sidebar. At the
top of the sidebar sat three one-shot research pages, months
past the questions they answered. A board whose data backend
had been disconnected five days earlier sat frozen, still
pinned, still presenting its last state as current. Two static
pages had never been edited since the day they were created.
Nothing in the list said any of this; it had to be checked.

## The run

**Research first.** The platform's own literature on spaces
was fifteen days old and launch-only — feature announcements,
no retention evidence. The durable patterns came from adjacent
systems that have run dashboards for years: self-hosted
dashboard projects, a home-automation platform, a notes tool's
favorites guidance, a monitoring service's dead-man's-switch
model. They converged, and module 12's concepts are that
convergence.

**Audit against live state.** Every space was checked at the
source: its actions, its snapshot time, its version history,
whether its refresh machinery had actually run. The seed
inventory the audit started from was mostly right — and wrong
in the ways that mattered, including one page whose refresh
had silently stopped and one whose headline number was wrong
(below).

**Design, batched.** One proposal, seven numbered questions:
the merges, the sidebar budget, which pages would render
content versus structure, and every proposed delete named. The
user answered once. No page was built, moved, or deleted
before that answer.

**Builds.** Three related live pages merged into one, their
statuses becoming sections fed by the snapshot refresh that
already existed. Three new living pages: an initiative
tracker; a self-monitoring page (job health as a dead man's
switch — absence past the cadence window renders as failure);
and a memory page (counts header, recent changes with diffs, a
health list — no global graph; content extended because the
user chose it for that page, asked explicitly).

**Placement and deletes last.** The three research pages'
substance was folded into the initiative page's lineage
section; once the surviving page was verified carrying it,
each research page was deleted, individually confirmed.

## End state

Sidebar 12 → 7. Total spaces unchanged at 14 — but only seven
earn sidebar rent; the library holds the reference pages, the
briefing letters, and three frozen pages kept at the user's
call.

Two results worth naming. The self-monitoring page caught a
real failure on its first day: a nightly job that had been
failing for two nights on a connection error, invisible
because a stopped job produces nothing to notice. And the
memory page's counts were cross-checked against independent
probes and matched exactly — the cross-check is what makes a
page's numbers believable.

## The failure

The merged page's top Exception reported a backup disk at 92%
used. Live state said about 70%: the probe behind the figure
had overstated use by roughly a third. The number was repeated
to the user twice before a check against the live source
caught it; the correction went out the same day, in the same
channel. Module 12's failure case is this, kept because it is
the module in one story: a dashboard is only as honest as its
probe, and a page that has never been cross-checked is
unverified, however polished.
