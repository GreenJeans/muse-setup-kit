# Capability profiles — what each platform capability buys

The wizard's Step 1 establishes which capability tokens your platform
has. This matrix is the reference behind those questions: for each
capability, which modules need it, which degrade without it, and what
the degradation actually is. It is generated from the modules'
`module.yaml` files (their `requires` and `degrades_without`
fields); if the two ever disagree, the `module.yaml` wins and this
page has a bug.

The platform answers behind this matrix are measured, not
assumed: each platform runs the Ten-Test Battery
(`docs/method.md`) on a pinned staging before it gets a
profile, and every claim here carries its evidence grade.

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

## Platform answers: Grok Bot

Grok Bot (xAI's consumer agent app, on Cursor's platform) has its
own profile (`grok` in `wizard/manifest.yaml`) and its own wizard
overlay (`platforms/grok/WIZARD.md`). These are the token answers
a ten-test battery measured on one live account on 2026-11-23 —
accounts differ in what is connected, so the overlay's Step 1
still checks each answer live rather than trusting this table.

| Token | Grok Bot | Caveat the token cannot express |
|---|---|---|
| `scheduling` | yes | Routines are real cron with verbatim saved instructions, but timing is approximate: dailies drift minutes inside their windows and an "exact" one-off fired about ten minutes late. A run's own history is not inspectable from inside the bot; the run-record file pattern is the history and the detector. |
| `shell-python` | yes | A real shell and file tools on a hosted computer, in chat and in runs. The platform volunteers that the computer is occasionally swapped and some folders cleared; a day of testing falsified none of it, and multi-day file survival is unmeasured. |
| `second-person` | no | One user per account for this pack's purposes. Bots on the account are the same person's conversations, not other people's agents. |
| `shared-docs` / `shared-tasks` / `shared-storage` | not used | Connectors exist on the platform, but no surface in this profile shares through them; the modules that require these tokens are not in the profile. |
| `other-agents` | present, adversely | Every bot on the account can read every other bot's files, fire its skills, and reach its connectors — measured, Test 6 Fail. Module 04 is excluded from the profile on exactly this evidence: no coordination layer is designed on assumed isolation. |
| `persona-file` | no | The bot's description is editable text and doubles as the template instructions field; it is not a persona file read as standing instructions. Module 11 is not offered. |
| `spaces` | no | No persistent user pages the agent maintains. |

Two Grok properties change how modules install and have no token
yet: **standing instructions live in platform memory**, stated by
the user in their own words (there is no instruction file at
all — module 00 installs as reference text plus the memory-seed
list in the overlay), and **the approval surface does not cover
the shell** — Auto-review gates connector calls, while shell
actions, pushes included, run uncarded, so the pack's ticket
discipline for egress is procedural. Both are handled in the
overlay rather than as tokens until a second platform shows the
same shape.

## Platform answers: OpenBot

OpenBot (a self-hosted, local-first workspace that runs other
vendors' agent CLIs) has its own profile (`openbot` in
`wizard/manifest.yaml`) and its own wizard overlay
(`platforms/openbot/WIZARD.md`). These are the token answers a
ten-test battery measured on a pinned Docker staging on
2026-11-25 (OpenBot v0.78.0) — installs differ in what is
connected and which provider CLI is in use, so the overlay's
Step 1 still checks each answer live rather than trusting this
table.

| Token | OpenBot | Caveat the token cannot express |
|---|---|---|
| `scheduling` | yes | Routines are real schedules with verbatim saved instructions, full tool access in runs, and fires measured at 0–3 seconds of drift. Fires while the host sleeps do not run. The agent's own list of its routines included a fabricated entry — reconciliation reads the routines store, never asks the agent. |
| `shell-python` | yes | A real shell and file tools in the agent's workspace, in chat and in runs; results verified on disk. Kit state lives in workspace files on the data volume; survival across a version upgrade is unmeasured (migrations are one-way), so the plan backs the volume up before upgrades. |
| `second-person` | not used | The profile is single-agent and single-user. Team surfaces exist on the platform (vendor-documented), but no surface in this profile shares through them, and the battery did not exercise them. |
| `shared-docs` / `shared-tasks` / `shared-storage` | not used | Native connectors are thin (vendor-documented: no Gmail/Drive/Calendar natively) and unmeasured by the battery; the modules that require these tokens are not in the profile. |
| `other-agents` | present, adversely | Every agent in one container runs as one user and can read every other agent's files — measured, Test 6 Fail. Module 04 is excluded from the profile on exactly this evidence; isolation means one container per agent. |
| `persona-file` | instruction file only | `AGENTS.md` is auto-loaded and binds in interactive chat (Test 1), but it is the procedures surface in this profile, not a persona file; it does not reach routine runs. Module 11 is not offered, and its fit is unmeasured. |
| `spaces` | no | Unmeasured — the battery did not test persistent page or space surfaces. Module 12 is not offered. |

Three OpenBot properties change how modules install and have no
token yet: **standing instructions bind in chat only** —
`AGENTS.md` is honored interactively and does not reach routine
runs, so every routine template embeds its own rule copies;
**silence is a token, not an instruction** — a watcher told to
post nothing posted anyway, and the documented `[[no-update]]`
token is measured working (2026-11-25 probe), so watchers
pair the token with a run-record line; and **there is no standing pre-approval** — commitment
points stop at a credential-grant prompt ("Only this agent",
never "All agents (Vault)"), and the ticket rule rides in
`AGENTS.md` and in routine instructions rather than in platform
machinery. All three are handled in the overlay rather than as
tokens until a second platform shows the same shape. Checked
against that test at this profile's build: two of the three
now appear on a second platform in the same shape —
procedural ticket discipline where the platform's review
surface has a hole (Grok's shell path; OpenBot's grant stops
with no standing pre-approval), and standing rules that bind
in chat but not in runs (Grok's memory seeds; OpenBot's
`AGENTS.md`). They stay overlay-handled here; promoting
either to a token is a maintainer call, not made here.
