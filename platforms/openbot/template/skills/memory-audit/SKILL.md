---
name: memory-audit
description: Use this when the user asks for a memory check, or on the weekly audit routine — lint and fidelity over the workspace memory files, corrections proposed as file edits.
---

# Memory audit

The kit's memory module in skill form — both halves, because
on this platform the memory is files and the schema is the
kit's own. Pack-authored for the Muse Setup Kit's OpenBot
profile; the platform surfaces it uses were measured in the
2026-11-25 battery (OpenBot v0.78.0: no platform memory
schema, files plus `AGENTS.md` are the memory, real shell in
runs); rehearsed as part of the pack in run 30 (2026-11-25)
— installed verbatim, with its unattended invocation still
owed (that run's audit executed an inlined procedure; the
pack's routines template now names that a defect).

1. **Inventory.** List the memory files and what each holds:
   the long-term file (`MEMORY.md`), the daily logs in
   `memory/logs/`, and the person and group pages. Every
   compiled page carries its provenance header
   (`schema_version`, `last_verified`, `sources`); a page
   without one is a finding.
2. **Lint.** Check the inventory for: claims that contradict
   each other; a claim superseded by a later dated claim
   still standing as current beside it; precise figures,
   dates, or amounts without a `(verify: ...)` pointer; a
   log entry claiming work no run-record line supports. The
   module's reference linter may be run over the files — the
   shell is there to run it — scoped to the memory files
   only (`MEMORY.md`, `memory/logs/`, `memory/people/`,
   `memory/groups/`): the kit checkout and the skill folders
   are not memory files, and a workspace-wide sweep buries
   the findings. Findings are candidates, listed
   with both sides quoted. Decide nothing yourself.
3. **Fidelity.** Pick a sample of claims at random and check
   each against its source — the daily log, the run-record,
   the user's own earlier words. Report each sampled claim
   as confirmed, contradicted, or unverifiable. A claim with
   no checkable source is unverifiable; say so, do not pass
   over it. Exact numbers are answered from the log or the
   live source, never from a compiled page alone.
4. **Corrections.** For every finding the user approves,
   apply the edit the schema prescribes: rewrite the live
   claim in place, and move the replaced claim to Superseded
   (or History) in the same edit, with superseded-by, date,
   and source. Show the edit verbatim in the report. The
   history is kept, dated, and inspectable — a correction
   that erases the old claim without trace is a defect, not
   a cleanup.
