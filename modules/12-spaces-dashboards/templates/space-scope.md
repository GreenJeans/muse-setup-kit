# Space scope — one per living page (module 12)

The page's SCOPE.md. A page without this file is not a living
page; it is a document that will rot.

- **Page:**
- **Owns:** (the questions this page answers at a glance)
- **Must never:** (what it must not show or claim — e.g. content
  the user did not opt into, a global graph, a value without a
  freshness timestamp)
- **Sources of truth:** (per section: the tracked state,
  register, or system the section renders — status comes from
  there, never re-typed)
- **Status enum it may use:** done / needs-you / blocked /
  watching / held (trim to the page's set; never prose status)
- **Freshness budget per section:** (section — budget; past
  budget the section renders greyed and badged stale)
- **Refresh machinery:** (schedule, action, source; snapshot
  refresh preferred over edit-based refresh)
- **Content opt-in:** structure only / content extended for
  ___ (the user's explicit choice, per page)
- **Cross-check record:** (value — page — source — date; at
  least one per page, from the build, refreshed at each audit)
