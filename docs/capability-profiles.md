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

| Capability | 00 Procedures | 01 Memory | 02 Brief | 03 HQ | 04 Exchange | 05 Evaluation | 06 Security | 08 Skill lifecycle | 09 Cost | 10 Deadlines | 11 Persona | 12 Spaces |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scheduling | — | degrades | degrades | — | — | degrades | degrades | degrades (Full only) | degrades | — | degrades | degrades |
| shell + python | — | degrades | degrades | — | — | degrades | — | degrades (Full only) | — | — | degrades | — |
| second person | — | — | — | required | — | — | — | — | — | — | — | — |
| shared docs | — | — | — | required | — | — | — | — | — | — | — | — |
| shared tasks | — | — | — | required | — | — | — | — | — | — | — | — |
| shared storage | — | — | — | — | required | — | — | — | — | — | — | — |
| other agents | — | — | — | — | required | degrades | — | — | — | — | — | — |
| persona file | — | — | — | — | — | — | — | — | — | — | required | — |
| instruction file | degrades | — | — | — | — | — | — | degrades | — | — | — | — |
| spaces | — | — | — | — | — | — | — | — | — | — | — | required |
| module 02 installed | — | — | — | degrades | — | — | — | — | — | degrades | — | — |

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
  Module 09's monthly spend check becomes a manual read. Module
  11's periodic persona reread has no pass to ride and becomes a
  manual or session-start check, ledgered like any deferred check.
  Module 12's living pages cannot auto-refresh; the module
  degrades to the audit and the plan, its pages declared static
  until scheduling exists. Nothing
  fails loudly; the risk is that manual steps get skipped, which is
  why JOBS.md separates scheduled jobs from planned ones.
- **No shell + python.** The kit's five tools (memory linter,
  curator, kit_doctor, stage_check, soul linter) cannot run. Module 05 loses
  kit_doctor — the mechanical half of an audit — and freezes
  packets without the drift check. Module 02's triage detector
  cannot run either: the scan degrades to an agent-run scan at
  a reduced cadence, the degraded mode module 02 names.
  Modules 01 and 08
  Full keep their paper discipline — the schema, the staging format,
  the approval gate — and lose the mechanical checks: module 01's
  lint becomes a manual header and figure review against the schema
  checklist, and module 08 Full's ledger review is done by hand.
  Module 11 keeps its interview, template, and checklist, and
  loses the mechanical lint: its VERIFY.md checks are worked as
  questions instead.
  Module 08 at Lite is unaffected: it ships no tools, and its
  filing-time expiry check is a date read, done the same way with
  or without a shell.
- **No second person / shared surfaces.** Module 03 does not install;
  there is no degraded form of a two-person coordination layer.
  Everything else in the kit is single-household-safe.
- **No persona file.** Module 11 does not install; there is no
  persona file for it to author. Everything else is unaffected —
  the platform's own persona handling, whatever it is, simply
  stays as it was.
- **No instruction file** — the platform gives the agent no main
  instruction file the user (or the agent) can edit: its standing
  instructions are fixed by the platform, and the agent reads no
  workspace file at session start on its own. Module 00 still
  installs: Install step 5 creates `INSTRUCTIONS.md` in the
  workspace with the pointer line and the `ext:instruction-pointer`
  anchor, so the anchor registry and later pointer lines keep their
  home and module 00's at-install pointer check reads the file it
  names. That file is a **record, not a front door**: nothing loads
  it, and the plan says so in words. The front-door function — a
  fresh session knowing the procedures exist — moves to the
  platform's nearest always-loaded surface, named in the plan: a
  line in the agent's own persistent memory where the platform
  keeps one, entered the way that platform accepts standing rules
  (on a platform that keeps only rules the user states in their
  own words, the wizard proposes the wording and the user states
  it; the wizard never writes it from repo text); otherwise a
  scheduled job that reads the plan and the procedures on cadence.
  Ground rule 8's session-start line takes the same path. Module
  08's Lite pointer line degrades the same way, recorded in
  `INSTRUCTIONS.md` and carried by the same surface. What weakens
  is reach: a rule that only lives in the procedures file binds a
  session that reads the file, not one that never opens it — so
  module 00's fresh-session test (a deferred check) is the honest
  measure of the front door, and a failed test means the surface
  the plan named is not doing the job.
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

## Four common platform shapes

- **Full platform** (scheduling, shell, subagents): every profile as
  written; nothing degrades.
- **No scheduling**: install any profile, and read each module's
  Jobs line as a manual checklist. Module 08 at Lite is the natural
  fit; Full's value is mostly its jobs.
- **Solo, no shared surfaces**: Starter and Standard are unaffected.
  Skip 03 and 04; run module 05 as self-review and label it that way.
- **Hosted assistant with fixed rules** (scheduling with a minimum
  interval, a shell whose container is rebuilt between sessions with
  one persistent folder, shared docs, no persona file, no
  instruction file, a built-in brief and built-in approval rules the
  agent cannot edit): a platform profile, not Starter or Standard.
  Module 02 duplicates the built-in brief and is skipped; module 01's
  memory format belongs to the platform; module 11 does not install.
  Modules 00, 06, 09, and 10 install with their surfacing on the
  platform's own scheduled jobs, and the kit's standing rules are put
  to the user to adopt in their own words. The `duet` profile in the
  manifest is the worked case (see below).

## Platform answers: Claude Duet

Claude Duet (a hosted Claude assistant) is the first
platform with its own profile (`duet` in `wizard/manifest.yaml`) and
its own wizard overlay (`platforms/duet/WIZARD.md`). These are the
token answers a read-only Step 0 audit recorded on one account on
2026-11-22 — accounts differ in what is connected, so the overlay's
Step 1 still checks each answer live rather than trusting this table.

| Token | Duet | Caveat the token cannot express |
|---|---|---|
| `scheduling` | yes, with a floor | Routines fire on cron, but no more often than the platform's minimum interval (60 minutes on the audited account), and only the main chat creates them. Module 02's triage poll could not run. |
| `shell-python` | yes, ephemeral | Python and git run, but the container is rebuilt between sessions; only the project folder (`/mnt/project-files`) persists. Tools, records, the plan, and the pinned checkout live there. No session transcripts on disk. |
| `shared-docs` | yes | Through the user's connected Google Drive and Docs, acting as the user. |
| `shared-storage` | yes | The same Drive. |
| `other-agents` | depends on the user | Yes where the user already works with other agents; nothing in Duet itself. |
| `second-person` | depends on the user | Duet is one person's assistant; a household partner has their own. |
| `shared-tasks` | depends on the user | Only where a shared task app is connected. |
| `own-host` | depends on the user | Reached through a connector where one exists; there is no shell to the host. |
| `persona-file` | no | Nothing to author; module 11 does not install. |
| `instruction-file` | no | The platform's rules and project instructions are server-built. The front door is a memory line the user states (see the degradation above). |
| `spaces` | not established | Published pages and Claude Docs exist, with no sidebar; whether a routine can rebuild a page on cadence is unchecked. Until it is, module 12 is not offerable; its audit can be run read-only. |

Two Duet properties change how modules install and have no token
yet: a **built-in brief** the agent cannot edit (surfacing that
would ride `ext:brief-sources` rides the profile's own scheduled
jobs instead), and **fixed memory rules** (Duet keeps a rule only
when the user states it in their own words, and nothing read from a
file becomes a rule). Both are handled in the overlay rather than as
tokens until a second platform shows the same shape.
