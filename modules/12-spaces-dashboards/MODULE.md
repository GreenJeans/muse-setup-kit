# Module 12 — Spaces & Living Dashboards

**Reads:** the user's space catalog (each space's actions,
snapshot and state, version history), the sidebar order, refresh
schedules, and the tracked items or goals a page claims to
reflect. Metadata and freshness first; page content only as
needed. **Writes:** a spaces audit and redesign plan in the
workspace; new or edited spaces only after the user approves the
plan; sidebar order only on approval; deletes only per space,
individually confirmed. **Network:** public web, for pattern
research when the platform's own literature is thin. **Jobs:**
none of its own; each dynamic page names its refresh machinery
(a scheduled space action preferred) at build time, and those
schedules belong to the pages.

**Data classes:** personal — a page can hold anything the user's
setup holds; the audit reads metadata and freshness first and
content only as needed. **Action classes:** delete — the module's
procedure can end in deleting the user's own spaces, each one
individually confirmed by the user first; creates and edits are
the module's own surface and happen only under an approved plan.

## Purpose

Every long-running setup accumulates pages: dashboards, trackers,
one-shot research, briefing letters, boards. Left alone they rot
in a specific way. Research pages pile into the sidebar's prime
real estate and stay there months after the question was
answered. Static pages go stale by construction and keep
presenting themselves as current. Prose status write-ups decay
the day they are written, because nothing re-writes them. A page
whose backend was disconnected sits frozen, still pinned, still
trusted.

This module is the counter-discipline: audit what exists against
live state, classify it, merge what belongs together, set a
sidebar budget, and build the few pages that earn a permanent
slot as *living* pages — exception-first, status as an enum,
freshness stamped, refreshed by machinery rather than memory.
The worked run behind it is generalized in
`docs/examples/spaces-redesign.md`: an audit of a 14-space
sidebar that ended with 7 pages earning sidebar rent, three
pages merged into one, three research pages folded into a
lineage section and deleted, and three new living pages built.

## Concepts

**Exception-first, glanceable.** A page the user opens daily
answers the morning question in five to ten seconds, no clicking
or scrolling. Exceptions sit at the top, each with a reason and
an owner. Healthy state collapses to one quiet line ("N of M ran
on schedule"). A page that leads with everything it knows is a
report, not a dashboard.

**Status is an enum, never prose.** A small, stable set of pills
— done / needs-you / blocked / watching / held — fed from the
system's tracked state, never re-typed into the page by hand.
Prose status paragraphs rot; an enum rendered from tracked items
cannot drift from the record it claims to reflect, because it
*is* the record, rendered.

**Freshness is part of the value.** Every section carries its
own last-updated timestamp and a freshness budget. Past budget,
the section renders greyed and badged stale — never as if live.
A value is a number plus the time it was observed; a number
without a time is a claim without a date.

**Auto-refreshed, not maintained.** If a human has to remember
to update a page, the page is already dead; the remembering is
what fails. Every dynamic page names its refresh machinery —
schedule, action, source — at build time, in its scope file. A
page with no machinery is declared static or archival, on
purpose, in the audit.

**Refresh by snapshot, not by edit.** Prefer a page whose
refresh is a snapshot action: cheap, idempotent, timestamped,
fed by a scheduled run. Refresh that rewrites the page's content
daily works, but it is the expensive and fragile fallback. When
the audit finds a page being maintained the hard way, flag it;
do not normalize it.

**The sidebar is a budget.** Five to seven pinned pages is the
working maximum; platform guidance and the cognitive research
agree on "a handful". Everything else is classified: reference
material to the library, inactive pages frozen in the library,
dead pages deleted with confirmation. A flat list of twelve
pinned pages is not a sidebar, it is a pile.

**Merge peers; fold research into lineage.** Related live pages
merge into one page with sections — their statuses become
sections of a whole, not competing pins. One-shot research pages
are inputs to an initiative: their substance folds into the
initiative page's lineage section, and once it is carried there,
the research pages are deleted. A research page is a means, and
it should not outlive the question as a peer of the answer.

**The interactivity that survives** is a persisted checklist
that clears when checked, and a control on the same tile as the
status it changes. Per-item metadata forms — fields to fill in
per row, per page, forever — are where dashboards go to die.

**Counts and structure over content — unless the user opts in.**
Dashboards show aggregates, dates, and exceptions; raw content
stays in its source system, one click away. A page may render
content itself (excerpts, diffs) when the user explicitly
chooses that for that page, asked per page. The default is
structure; content is the opt-in.

**Self-monitoring is a dead man's switch.** A job that stops
running produces nothing, so silence reads as health unless the
page treats absence past the cadence window (26 hours daily, 8
days weekly) as failure in itself. Monitor only the jobs whose
silent absence costs something; system and heartbeat noise is
excluded by design. Show last success, last failure *with
reason*, next expected, and whether an alert is attached. Built
this way, the page catches real failures on its first day,
because real failures are usually already happening.

**Never draw the global graph.** For memory or knowledge
visualization, the global node graph hairballs past a few
hundred nodes — every platform that ships one ships a beautiful
toy. What works instead: a counts header, recent changes with
diffs, a quiet / stale / orphans health list, and at most a
local graph seeded from one node.

## The failure case

The worked run's merged page opened with an Exception: a backup
disk at 92% used. It was wrong. Live state said about 70% — the
probe behind the number had overstated use by roughly a third.
The figure was repeated to the user twice before a check against
the live source caught it, and the correction went out the same
day, in the same channel.

- **A dashboard is only as honest as its probe.** One wrong
  number, displayed confidently, erodes trust in every other
  number on the page. Trust is the whole product.
- **Verify one rendered value against ground truth before
  trusting a page.** During a build or an audit, cross-check at
  least one value per page against its live source and record
  the check. A page that has never been cross-checked is
  unverified, however polished.
- **"No data" is a valid render.** Where a source cannot be
  reached, show the honest blank. A convincing fake number is
  worse than an empty pill.
- **Corrections go out plainly and fast**, in the same channel
  the wrong number arrived in. (Procedures §7 is the general
  rule; a dashboard is where it bites hardest, because the page
  repeats the number every time it is opened.)

## Procedure

1. **Research first, if the patterns are new to you.** Platform
   literature on pages and dashboards may be days old and
   launch-only, with no retention evidence behind it. Say so,
   and borrow from adjacent, battle-tested systems (self-hosted
   dashboard projects, monitoring tools, note systems) whose
   patterns have survived contact with real users.
2. **Audit against live state, not summaries.** One worksheet
   per space (`templates/space-audit.md`), filled from the
   source: the space's own actions and snapshot, its version
   history, whether its refresh machinery actually runs. An
   inventory compiled from summaries will be mostly right and
   wrong in the ways that matter; the audit exists to find
   those.
3. **Design before building, questions batched.** Present the
   redesign as one proposal with numbered questions — merges,
   the sidebar budget, per-page content opt-ins, every proposed
   delete named. The user answers once. Deletes are approved
   per space before any deletion happens; a bulk "clean it up"
   is not a delete approval (module 00's ticket rule governs).
4. **Build.** Merges first, then new living pages, each with a
   scope file (`templates/space-scope.md`): what it owns, what
   it must never show, its sources of truth, a freshness budget
   per section, its refresh machinery, the status enum it may
   use. Cross-check one rendered value per new page against its
   live source before calling it done, and record the check.
5. **Placement and deletes last.** Reorder the sidebar to the
   agreed budget (`templates/sidebar-plan.md`). Delete only
   after the surviving page is verified carrying the deleted
   page's substance, and only the spaces individually confirmed.

## Install

1. Copy the module's templates to the workspace templates
   folder. There are no tools in this version.
2. Run the audit (Procedure step 2) before proposing anything;
   the module's first deliverable is the filled worksheets plus
   a sidebar plan, not a page.

## Extension points (anchors)

A page built under this module may declare composition anchors
in its scope file for sections other modules feed — the morning
brief's exceptions (module 02), the deadlines register's
expiries (module 10) — one recorded owner per anchor, per module
00's composition rule. The anchors are extension points, not
content: this module owns the page's shape, the feeding module
owns what its section says.
