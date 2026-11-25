# Grok profile mismatches

Pinned commit: v0.16, `ceda863`, published Latest 2026-11-23
7:16 PM PT. Last checked against an install run: not yet
(install run pending).

This list records places where `platforms/grok/WIZARD.md` at the
pinned commit and a live install diverge. One entry per
mismatch. IDs (M0, M1, …) are never renumbered. Status is the
only field edited in place; allowed values are `open`,
`confirmed`, `fixed-on-main`, `released`, and `withdrawn`.

## Ranking and evidence

**Ranking.** When choosing the top fix for a PR, rank by impact
tier first (`blocks install`, then `wrong result silently`,
then `wrong expectation only`, then `cosmetic`), then by
wizard order (earliest first) within a tier.

**Evidence.** An "Install does" claim marked observed must
point at evidence. Otherwise it is unverified, and the entry
cannot be confirmed.

## Entries

### M0

1. **ID:** M0
2. **Status:** fixed-on-main
3. **Where:** WIZARD.md@ceda863 — absent. The text was inserted
   after warning 2 (L21–25) in section "The two warnings
   (state them in the plan, verbatim in effect)", immediately
   before `## What Grok has instead of the kit's usual
   surfaces` (L27). On origin/main (`5846ad3`, after PR #13)
   the diff adds eleven lines: the paragraph at L27–36 plus
   the following blank line.
4. **Wizard says:** Nothing at `ceda863`. Warning 2 ends at
   L25 and the next section opens at L27; the overlay is
   silent on tool-result persistence.
5. **Install does:** Tool results generally, not only
   connector reads, can persist as files in the bot's agent
   asset store on the account's shared computer,
   automatically, whether or not the bot copies or saves
   anything. Observed (Bart (Grok Bot), measured 2026-11-23;
   a connector read, a tool-catalog listing, and a
   spreadsheet read all persisted). Evidence: the paragraph
   added on origin/main by PR #13, also visible in
   `git diff ceda863 origin/main -- platforms/grok/WIZARD.md`:

   > Warning 2 reaches past the files a bot chooses to write. Tool
   > results generally, not only connector reads, can persist as
   > files in the bot's agent asset store on the account's shared
   > computer, automatically, whether or not the bot copies or saves
   > anything. Measured, not conjectured (2026-11-23): a connector
   > read, a tool-catalog listing, and a spreadsheet read all
   > persisted. By warning 2, every bot on the account can read
   > those files. Treat any read as leaving a file behind; write
   > tasks and briefs that involve sensitive material on that
   > assumption.

6. **User impact:** wrong result silently — without the
   warning, sensitive tool results can persist as files
   every bot on the account can read, and the installer is
   not told.
7. **Fix kind:** doc change
8. **Proposed fix:** Ship the paragraph already on
   origin/main in the next release.

### M1

1. **ID:** M1
2. **Status:** open
3. **Where:** WIZARD.md@ceda863 L48, section "What Grok has
   instead of the kit's usual surfaces"
4. **Wizard says:** "**Routines are the scheduler** (Test 2,
   Pass): real cron, …"
5. **Install does:** Routines also accept event triggers
   (webhook, email, GitHub). Observed by Bart (Grok Bot) on
   2026-11-24: webhook routine `kit-doorbell` was created at
   6:15 PM PT and woke Bart about two minutes after a
   6:19 PM PT #workshop post. The routine was hand-created,
   not imported from the template.
6. **User impact:** wrong expectation only
7. **Fix kind:** doc change
8. **Proposed fix:** Add one sentence that routines can also
   be triggered by webhook, email, or GitHub events.

### M2

1. **ID:** M2
2. **Status:** open
3. **Where:** WIZARD.md@ceda863 L48–53, same section ("What
   Grok has instead of the kit's usual surfaces")
4. **Wizard says:** "Timing is approximate — dailies drifted
   minutes inside their windows and an "exact" one-off fired
   about ten minutes late. Every job this pack installs
   tolerates at least ten minutes of drift."
5. **Install does:** Schedules have a 5-minute minimum
   interval. Observed by Bart (Grok Bot) on 2026-11-24,
   creating `kit-session-clock` at `@every 5m`; platform
   routine rules state runs must be at least 5 minutes
   apart.
6. **User impact:** wrong expectation only
7. **Fix kind:** platform limit
8. **Proposed fix:** Document the 5-minute floor next to the
   drift note.

## Install-run stress checks

The pending install run must show all four of these:

1. **Template import.** Semantic read-back of the imported
   template. A formatting diff is not a failure.
2. **Memory seeds.** Seeds are present in the user's own
   words, found by path, and dated.
3. **Routines enabled only at the plan step.** Routines are
   created paused, and enabled only at the plan step.
4. **Saved-instruction read-back.** Compare each routine's
   saved instructions against `template/routines.md`. Exactly
   two platform-added lines are allowed; any extras are
   recorded verbatim.

## Changelog

- 2026-11-24 — M0 created as `fixed-on-main`; M1 and M2
  created as `open` (Bart (Grok Bot), workshop session 6).
