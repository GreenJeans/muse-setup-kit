# Verify — Module 12: Spaces & Living Dashboards

## At install

- [ ] The audit exists: one filled `space-audit` worksheet per
      space in the user's catalog, each with a verdict (keep /
      merge / freeze / delete) and an evidence line that names
      what was checked at the source — not a summary of a
      summary.
- [ ] Every sidebar space has a named source of truth and either
      live refresh machinery or an explicit "static / archival"
      declaration in its worksheet.
- [ ] The sidebar plan was presented with its questions batched
      and approved before any build, move, or delete; every
      deleted space was individually confirmed, and each one's
      substance (if any) is carried by a named surviving page.
- [ ] The sidebar count is at or under the budget the user set
      (default 7).
- [ ] Every new or merged page has a scope file: owns, must
      never, sources of truth, a freshness budget per section,
      refresh machinery, and the status enum it may use.
- [ ] Every dynamic section on a new page shows a freshness
      timestamp, and at least one rendered value per new page
      was cross-checked against its live source during the
      build, with the check recorded in the page's scope file
      or the audit.
- [ ] No page renders a global graph as its landing view.

## Deferred

- [ ] **First stale render** (due: the first section that passes
      its freshness budget): the section renders greyed and
      badged stale, not as if live. If it renders fresh-looking
      past budget, the page's refresh or its budget is wrong —
      fix the machinery, not the badge.
- [ ] **Self-monitoring catch** (due: the first monitored job
      that misses its cadence window): the page shows the
      absence as a failure with last success, last failure
      reason, and next expected — and the monitored set still
      excludes system and heartbeat jobs by design.
