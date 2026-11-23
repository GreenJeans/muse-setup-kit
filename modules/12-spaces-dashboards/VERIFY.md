# Verify — Module 12: Spaces & Living Dashboards

## At install

- [ ] The audit exists: one filled `space-audit` worksheet per
      space in the user's catalog, each with a verdict (keep /
      merge / move to library / freeze / delete) and an evidence
      line that names what was checked at the source — not a
      summary of a summary. For every live or dynamic space the
      worksheet's cross-check fields are filled: the refresh
      machinery checked, and one rendered value checked against
      its live source.
- [ ] Every space in the final sidebar has a named source of
      truth and either live refresh machinery (or, without
      scheduling, a named on-demand snapshot action and a
      freshness budget) or an explicit "static / archival"
      declaration — in its audit worksheet for an existing
      space, in its scope file for a new one.
- [ ] The sidebar plan was presented with its questions batched
      and approved before any build, move, or delete, and the
      plan records that approval; every deleted space was
      individually confirmed, and each one's substance (if any)
      is verified carried by a named surviving page.
- [ ] The sidebar count is at or under the budget the user set
      (default 7).
- [ ] Every living sidebar page (new, merged, or kept dynamic)
      has a scope file: owns, must never, sources of truth, a
      freshness budget per section, refresh machinery, the
      status enum it may use, its content opt-in (structure
      only, or the user's explicit per-page choice), and any
      composition anchors with a single recorded owner each.
- [ ] Every dynamic section on a new or merged page shows a
      freshness timestamp; status renders as the scope file's
      enum from tracked state, never as prose; and at least one
      rendered value per new or merged page was cross-checked
      against its live source during the build and agreed — or,
      after a recorded miss, the probe was fixed and a re-check
      agreed. Until agreement, the value renders as no data.
      Where a source cannot be reached, the section shows the
      honest blank.
- [ ] No page renders a global graph (local, single-node-seeded
      graphs only).

## Deferred

- [ ] **First stale render** (due: the first section that passes
      its freshness budget): the section renders greyed and
      badged stale, not as if live. If a section whose timestamp
      is past budget still renders fresh-looking, the staleness
      check or rendering is broken — fix the stale-state
      display first, verify it renders greyed and badged stale
      while overdue, and then repair the underlying refresh
      machinery.
- [ ] **Self-monitoring catch** (only if a self-monitoring page
      was built, and scheduling is available; otherwise N/A):
      the first monitored job that misses its cadence window —
      the page shows the absence as a failure with last success,
      last failure reason, next expected, and whether an alert
      is attached; and the monitored set still excludes system
      and heartbeat jobs by design.
