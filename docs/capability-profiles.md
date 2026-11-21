# Capability profiles — what each platform capability buys

The wizard's Step 1 establishes which capability tokens your platform
has. This matrix is the reference behind those questions: for each
capability, which modules need it, which degrade without it, and what
the degradation actually is. It is generated from the modules'
`module.yaml` files (their `requires` and `degrades_without`
fields); if the two ever disagree, the `module.yaml` wins and this
page has a bug.

Legend: **required** = the module will not install without it.
**degrades** = installs and works; the named function weakens.
**—** = unaffected.

| Capability | 00 Procedures | 01 Memory | 02 Brief | 03 HQ | 04 Exchange | 05 Evaluation | 06 Security | 08 Skill lifecycle | 09 Cost | 10 Deadlines |
|---|---|---|---|---|---|---|---|---|---|---|
| scheduling | — | degrades | degrades | — | — | degrades | degrades | degrades (Full only) | degrades | — |
| shell + python | — | degrades | — | — | — | degrades | — | degrades (Full only) | — | — |
| second person | — | — | — | required | — | — | — | — | — | — |
| shared docs | — | — | — | required | — | — | — | — | — | — |
| shared tasks | — | — | — | required | — | — | — | — | — | — |
| shared storage | — | — | — | — | required | — | — | — | — | — |
| other agents | — | — | — | — | required | degrades | — | — | — | — |
| module 02 installed | — | — | — | degrades | — | — | — | — | — | degrades |

## What each degradation means

- **No scheduling** — the platform cannot run jobs at all.
  File-based job definitions count as scheduling only when
  something actually fires them on cadence (a scheduler, a
  heartbeat, a session hook); job files that nothing runs are this
  row, not a degraded form of scheduling. Module 01's weekly lint becomes a manual run.
  Module 02's brief is generated when asked instead of arriving,
  and its money watch runs only on demand.
  Module 05's scheduled audit reminders become manual; the audits
  themselves run on demand. Module 06's periodic re-checks (grants
  inventory, watch liveness) become manual. Module 08 Full's sweep
  and curator run on demand (Lite is unaffected — it has no jobs).
  Module 09's monthly spend check becomes a manual read. Nothing
  fails loudly; the risk is that manual steps get skipped, which is
  why JOBS.md separates scheduled jobs from planned ones.
- **No shell + python.** The kit's four tools (memory linter,
  curator, kit_doctor, stage_check) cannot run. Module 05 loses
  kit_doctor — the mechanical half of an audit — and freezes
  packets without the drift check. Modules 01 and 08
  Full keep their paper discipline — the schema, the staging format,
  the approval gate — and lose the mechanical checks: module 01's
  lint becomes a manual header and figure review against the schema
  checklist, and module 08 Full's ledger review is done by hand.
  Module 08 at Lite is unaffected: it ships no tools, and its
  filing-time expiry check is a date read, done the same way with
  or without a shell.
- **No second person / shared surfaces.** Module 03 does not install;
  there is no degraded form of a two-person coordination layer.
  Everything else in the kit is single-household-safe.
- **No shared storage or other agents.** Module 04 does not install.
  Module 05 loses its strongest method — blind cross-model review —
  and keeps self-review, cold installs, and the kit's own doctor
  (where a shell is available), labeled as the weaker evidence
  they are.
- **No module 02.** Module 03 installs, but its decision and waiting
  items surface only when someone opens the task layer; the brief is
  what makes them arrive. Module 10 installs, but its register
  surfaces only through a manual deferred check on a cadence the
  user picks — nothing arrives on its own, and the plan says so.
  Nothing else degrades — module 04's output polling riding the
  brief, where both are installed, is a synergy, not a dependency.

## Three common platform shapes

- **Full platform** (scheduling, shell, subagents): every profile as
  written; nothing degrades.
- **No scheduling**: install any profile, and read each module's
  Jobs line as a manual checklist. Module 08 at Lite is the natural
  fit; Full's value is mostly its jobs.
- **Solo, no shared surfaces**: Starter and Standard are unaffected.
  Skip 03 and 04; run module 05 as self-review and label it that way.
