# Verify — Module 11: Persona & Soul

## At install

- [ ] SOUL.md exists at the path the plan records, rendered
      from this module's template at this pin, and no
      `<PLACEHOLDER>` tokens remain in it. A section the
      interview did not reach was cut, not left as a slot.
- [ ] The draft was shown in full and approved before the
      file was written; the plan records that approval
      separately from the plan's own approval.
- [ ] The examples block holds four filled exchanges plus an
      anti-example, in the template's blockquote form. Each
      exchange is one the adopter supplied, one drafted from
      their real interaction history and marked as drafted
      for their veto or pick, or — where no history exists —
      one drafted from the interview answers applied to a
      situation the adopter named, marked drafted/provisional
      the same way. None was invented from nothing; the plan
      names which kind each is, and ledgers replacing
      drafted-from-answers exchanges with real-history ones
      at the first reread. Fewer than four filled exchanges,
      recorded in the plan as a gap, is not a failed install;
      a recorded examples gap is the one lint finding that
      may stand at install.
- [ ] The priority order in the file is the adopter's ranking
      from the interview, compared against the recorded
      answers, not the order in which the template lists the
      candidates, and not the agent's guess.
- [ ] The governance section names the core's owner, the
      staged-diff rule, the evidence threshold for a change,
      the reread cadence, the size cap, and the adopter's
      drift signs. All six, in the adopter's terms. Where
      the short subset was used, the reread cadence and the
      size cap may stand at the template's defaults; the
      plan records them as defaults adopted, not answers
      given.
- [ ] The failure-mode checklist in MODULE.md was run against
      the draft before it was shown; the plan records the
      result, including any mode left knowingly unaddressed.
- [ ] Word count at or under the cap the governance section
      states (about 1,200 by default). Where a shell is
      available, `tools/soul_lint.py --cap <the cap the
      governance section states>` runs against the file with
      no findings; any boilerplate warnings are
      dispositioned in the plan (kept lines name the behavior
      they change). Where no shell is available, the same
      checks were worked by hand and the plan says so.

## Deferred

- [ ] **First full reread** (due: the first monthly pass
      after install, or install + 1 month, whichever the plan
      records; the ledger row names the event and `due:`
      carries the operative date): the file is reread whole
      against the failure-mode checklist and the linter;
      contradictions and size creep come back as staged
      proposals through the decision queue, never as edits.
- [ ] **Drift check** (due: the first time the adopter
      corrects the agent's tone or register after install, or
      install + 3 months, whichever comes first; the ledger
      row names the event and `due:` carries the fallback
      date): the file's stated drift signs are compared
      against recent sessions, and the result is recorded in
      the plan, including "no drift seen," which is a result,
      not a skip.
- [ ] **Boilerplate creep** (due: the second reread, or
      install + 6 months, whichever comes first): the linter
      runs again; lines added since install are checked
      against the delete-the-line test, and stock lines that
      crept in are cut by staged proposal or kept with the
      behavior they change named in the plan.
