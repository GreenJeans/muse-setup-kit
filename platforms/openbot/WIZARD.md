# OpenBot overlay — read after wizard/SKILL.md

This overlay adapts the wizard to OpenBot. It governs the
`openbot` profile in `wizard/manifest.yaml` (modules 00 and 01,
in the forms below). Where this overlay and the wizard differ,
this overlay governs on OpenBot; where this overlay is silent,
the wizard governs. Every platform claim below carries its
grade: measured by a ten-test battery on a pinned Docker
staging (2026-11-25, OpenBot v0.78.0; 3 Pass, 4 Partial,
2 Fail, 1 Open — the score is named where the claim is
load-bearing), vendor-documented, or unmeasured. Anything with
none of those grades is labeled unmeasured, here and in the
plan.

## The three warnings and the license line (state them in the plan, verbatim in effect)

1. **A second agent is not a sandbox.** Every agent in one
   container runs as one user and can read every other agent's
   files (battery Test 6, Fail: a bystander agent read the
   working agent's canary across workspaces; the only barrier
   was the model choosing not to). Isolation is one container
   per agent. Whether the Workspace only Access mode changes
   this is unmeasured (the 6b probe was not run), so this
   warning stands at full strength until it is.
2. **Silence is a token, not an instruction.** A watcher told
   to post nothing posted a "nothing posted" message anyway
   (Test 10, Fail). The platform documents a `[[no-update]]`
   token for staying silent (vendor-documented, in the UI);
   the battery did not test it. Watchers in this pack answer
   the token *and* write a run-record line — the record line
   itself was written correctly in the same test.
3. **AGENTS.md rules don't reach routine runs.** A rule in
   `AGENTS.md` bound in every fresh interactive conversation
   and did not bind in unattended routine runs (Test 1,
   Partial). Standing rules seed into `AGENTS.md` for chat;
   every routine carries its full instructions, including
   the rules it needs.
4. **License: OpenBot is PolyForm Noncommercial 1.0.0 —
   personal, research, and evaluation use only; commercial
   use breaches its license** (vendor-documented, the
   platform's LICENSE). The plan states this where the user
   will see it before the install closes.

Warning 1 reaches past the files an agent chooses to write. In
the battery, a copy of a test canary file landed in
`Shared/Transfers/` as a generated attachment, readable by
every agent in the container (measured, 2026-11-25). Treat any
generated attachment as leaving a copy behind in a shared
place; write tasks and briefs that involve sensitive material
on that assumption.

## What OpenBot has instead of the kit's usual surfaces

- **`AGENTS.md` is the one auto-loaded instruction surface —
  and it reaches chat only** (Test 1, Partial). Interactive
  sessions honor it reliably (every fresh conversation in the
  battery opened with the seeded reporting line); routine
  runs execute their own verbatim instructions without it.
  The file is free-form text the user owns. A rule that lives
  only in some other workspace file did not bind in chat
  (Test 4, Partial: the user-stated rule bound after the
  agent wrote it into `AGENTS.md` itself; the file-sourced
  rule did not). Standing rules go in `AGENTS.md` or they are
  not standing rules.
- **Memory is workspace files; there is no platform schema to
  fight** (Test 3, Pass). Persistence is files in the agent's
  workspace plus the free-form `AGENTS.md`; retrieval was
  unprompted-correct in the battery. The kit's markdown
  memory architecture — current state at top, Superseded,
  verify pointers — lives in the workspace untouched, and
  the platform brings no schema, no compiled store, and no
  history of its own to reconcile against.
- **Routines are the scheduler** (Test 2, Pass): verbatim
  saved instructions, full tool access in runs, fires
  measured at 0–3 seconds of drift. One staging caveat:
  scheduled fires while the host sleeps do not run
  (battery-observed); server or container staging on an
  always-on host avoids that. Webhook-triggered routines are
  vendor-documented (signed, Standard Webhooks format) and
  were not exercised by the battery — unmeasured.
- **Skills install verbatim** (Test 8, Pass): saved text is
  identical, and skills load fresh and in unattended runs.
  The platform generates its frontmatter from the skill text
  at save, so a frontmatter diff at read-back is not drift —
  content is the comparison.
- **Approvals are Access modes plus credential grants**
  (Test 5, Partial): three modes (Full access / Ask first /
  Workspace only), and commitment points stop at a
  credential-grant prompt. There is no standing class
  pre-approval and no approve-now-run-later queue; the
  approvals section below carries the mapping and its
  limits.

## Step 1 on OpenBot — capability answers

Recorded from the battery; the overlay's Step 1 still checks
each answer live, because installs differ in what is connected
and which provider CLI is in use:

- `scheduling`: yes — routines. Saved instructions read back
  verbatim, runs execute with full tools, fires measured at
  0–3 seconds of drift (Test 2, Pass). Fires while the host
  sleeps do not run; the run-record pattern below is the
  detector either way. A routine's own history is not the
  agent's to report: asked to list its routines, the agent
  included one that did not exist (Test 9, Partial) —
  reconciliation reads the routines store or UI, never asks
  the agent.
- `shell-python`: yes — a real shell and file tools in the
  agent's workspace, in chat and in runs (Tests 2 and 3;
  results verified on disk, not by agent say-so). Kit state
  that must survive lives in workspace files on the data
  volume, and the plan says which. Survival across a version
  upgrade is unmeasured — database migrations are one-way
  (vendor-documented), so the plan records a backup of the
  data volume before any upgrade (see the update posture).
- `second-person`, `shared-docs`, `shared-tasks`,
  `shared-storage`: not used by this profile. The pack is
  single-agent and single-user. Native connectors are thin
  (vendor-documented: no Gmail/Drive/Calendar natively; a
  documented third-party route exists) and were not exercised
  by the battery — unmeasured. No kit surface in this pack
  shares through them, and the plan must not imply a
  connected account the install has not verified.
- `other-agents`: present on the platform in the worst way —
  every agent in the container can read every other agent's
  files (Test 6, Fail) — and module 04 is excluded anyway
  (below).
- `persona-file`: an auto-loaded instruction file exists
  (`AGENTS.md`, binding interactively — Test 1), but in this
  profile it is the procedures surface, not a persona file.
  Module 11 is not offered; its fit on this surface is
  unmeasured.
- `spaces`: no — unmeasured. The battery did not test
  persistent page or space surfaces; module 12 is not
  offered.
- `own-host`: yes by construction — the platform is
  self-hosted, and the install runs on a host the user
  controls. That host is also the security boundary (see the
  update posture): at Full access an agent can read anything
  its OS user can read (vendor-documented).
- Billing bucket (wizard Step 1's stop condition) applies
  unchanged, with an OpenBot wrinkle: the bucket is the
  provider CLI's (API key or subscription, per that
  provider's terms — the vendor's own terms document
  recommends API-key auth for SDK-driven use; vendor-
  documented). Billing is invisible from inside the agent
  (Test 9, Partial: honestly unreadable); usage lives in the
  app's Settings, not the agent. Name the bucket in the
  plan, user-stated.

## Module 00 on OpenBot — an AGENTS.md seed

Module 00's procedures install as a seed written into the
agent's `AGENTS.md` — the one surface that binds in
interactive chat (Test 1). The seed text is in
`template/agents-md.md`: the ticket rule, the reporting
format, the correction rule, and the scope rule, stated as
text the user puts in place. The user writes it in (or has
the agent write it and reads it back); a rule sitting in
some other workspace file is not a standing rule (Test 4:
the file-sourced rule did not bind in chat).

Two measured limits shape everything downstream:

- **The seed binds interactively only.** Routine runs do not
  load `AGENTS.md` (Test 1). Every routine template in this
  pack therefore embeds its own copies of the rules it
  needs — the run-record append, the no-deciding rule, the
  silence token — in its saved instruction. A routine that
  needs a rule carries it; no plan may claim a routine
  inherits the seed.
- **The seed is text, not machinery.** There is no standing
  pre-approval on this platform (Test 5), so the ticket rule
  in `AGENTS.md` is a rule the agent follows in conversation,
  backed at commitment points by the credential-grant prompt
  — not a platform-enforced gate. The plan states it that
  way.

The seed is verified the way the battery verified it: after
the seed is in place, a fresh interactive conversation
shows it binding (the reporting format appears unprompted).
That check is at-install, not deferred — the battery
measured the mechanism the same way.

## Module 01 on OpenBot — both halves

**What ships: the architecture and the audits.** The platform
brings no memory schema (Test 3, Pass: files plus free-form
`AGENTS.md` are the memory), so module 01's markdown
architecture — current state at top, superseded claims moved
to Superseded in the same edit, verify pointers on precise
claims, provenance headers — installs as workspace files,
untouched, from the module's own templates. The starters in
`template/workspace.md` carry the file shapes the pack's
routines and skills assume.

The audit half runs over those files with a real shell:

- *Inventory.* List the memory files and what each holds:
  the long-term file, the daily logs, the person and group
  pages. Every compiled page carries its provenance header
  (`schema_version`, `last_verified`, `sources`); a page
  without one is a finding.
- *Lint.* Deterministic checks over the files: claims that
  contradict each other, a superseded claim still standing
  as current beside its replacement, precise figures without
  verify pointers, a log entry claiming work no run-record
  line supports. The module's reference linter runs as-is —
  there is a shell to run it with. Findings are candidates;
  a mind decides each one — module 01's rule, unchanged.
- *Fidelity.* Sample claims at random and check each against
  its source: the daily log, the run-record, the user's own
  correction. A claim with no checkable source is reported
  as unverifiable, never passed over in silence.
- *Correction.* A correction is a file edit: rewrite the
  live bullet, move the replaced claim to Superseded (or
  History) in the same edit, with superseded-by, date, and
  source. Every correction is proposed to the user first
  and applied on approval, shown as the edit it is. Unlike
  a platform store, the history here is the kit's own —
  kept, dated, and inspectable.

## Module 04 — excluded, and the plan says why

Module 04 (AI Exchange) is not in the profile and is not
offered per-module on OpenBot. The battery's isolation test
failed (Test 6): every agent in one container can read every
other agent's files, so a coordination layer designed on
assumed isolation would be designed on a fiction. Anyone who
wants more than one credentialed agent runs **one container
per agent** — the vendor's own documented remedy
(vendor-documented) — and coordinates between containers,
never inside one. If a future battery re-measures isolation
(for example the Workspace only mode, unmeasured here) and
it passes, the exclusion is revisited then — on evidence,
not on a platform announcement.

## The jobs layer — routines

Jobs install as routines from `template/routines.md`. The
disciplines, all measured unless labeled:

- **Verbatim saved instructions.** A routine's saved
  instruction is read back from storage after creation and
  compared with the approved text (Test 2, Pass: instructions
  matched, and a canary was quoted from storage). The
  instruction is self-contained: it names the workspace
  files it reads, the record it appends, and what it posts —
  because a run is a fresh context that holds only its
  instruction and the files it is told to read, and
  `AGENTS.md` does not reach it (Test 1).
- **The run-record pattern.** Every routine appends one line
  per run to a workspace record file — name, timestamp,
  one-line outcome — whether or not it posts anything. A
  missing line is the detector's signal: the brief reads the
  record the way module 02 reads a jobs file, and a job with
  no line inside its window is a failure to surface, not a
  quiet success. The record line itself was written
  correctly even in the run where silence failed (Test 10).
- **Silence is a token.** A watcher that has nothing to
  report answers `[[no-update]]` and appends its run-record
  line. The token is vendor-documented (in the UI) and
  **untested**: instruction-only silence posted anyway
  (Test 10, Fail). The first silent-watch run after install
  is therefore a deferred check with teeth — if it posts,
  that is a finding to surface, not a pass to assume.
- **Timing.** Fires measured 0–3 seconds of drift (Test 2) —
  detector windows can be tight, and the run-record detector
  is kept anyway. Fires while the host sleeps do not run;
  a missed window after a sleep gap is surfaced as missed,
  never silently caught up.
- **Reconciliation reads the store, never the agent.** Asked
  to list its routines, the agent included one that did not
  exist (Test 9, Partial). Jobs reconciliation — what
  routines exist, their schedules, their saved instructions
  — reads the routines store or UI. The agent's self-report
  of its own jobs is not evidence.
- **Billing is invisible from inside.** Usage and spend live
  in the app's Settings (Test 9); no routine reports its own
  cost from inside, and the plan does not ask it to.

## Approvals — Access modes, credential grants, and the limits

The ticket rule (module 00, procedures §2) maps onto
OpenBot's approval surfaces like this (Test 5, Partial):

- **Full access** does local reversible work unasked and
  reports afterwards — the kit's default posture for the
  reversible tier. **Ask first** and **Workspace only** exist
  as stricter modes (vendor-documented names; the battery
  exercised the grant stops, not every mode's full
  semantics — unmeasured beyond Test 5). The install sets
  the mode with the user present and records it in
  `SETUP-PLAN.md` as found, before changing it.
- **Credential grants are the commitment-point stop.** A push
  attempt stopped at a grant prompt (Test 5): the choice is
  "Only this agent" or "All agents (Vault)". **The grant
  discipline is "Only this agent", always** — warning 1 is
  why: a Vault-wide grant is readable by every agent in the
  container. The plan records each grant, its scope, and
  the user's decision.
- **No standing pre-approval exists.** There is no
  approve-this-class-forever setting and no
  approve-now-run-later queue (Test 5). The ticket rule
  therefore rides in `AGENTS.md` (binding interactively) and
  in each routine's saved instruction (binding in runs),
  backed at commitment points by the grant prompt. The plan
  must never state that the platform will pre-approve a
  class of action, and no routine may claim an approval it
  will not actually hold.
- **The local-scripts API stays off.** It is off by default
  per agent (vendor-documented) and can submit approvals —
  an approval bypass by design. The install does not enable
  it, and the plan records that it is off.
- **Spill.** Generated attachments can land in
  `Shared/Transfers/`, readable by every agent in the
  container (measured, 2026-11-25). Treat any read that
  produces an attachment as leaving a copy behind in a
  shared place, per warning 1.

## Egress — human-landed until measured

A branch-and-tag push from the agent was not exercised
(Test 7, **Open** — unexercised by decision, not by failure).
What is measured: no push happens without a credential grant
(Test 5), and the grant discipline above applies to any
future egress credential. Until a scoped-token push is
exercised and verified from outside the container, **releases
are landed by a human**, and the plan says so instead of
discovering it mid-release. The plan records the egress
decision (no credential granted / credential granted to this
agent only), and an install that does not need egress grants
nothing.

## Update posture and staging — the pin is soft

Vendor-documented, from the platform's own docs and license
at the measured pin; the battery did not exercise an upgrade:

- **Support covers the latest release only** — no backports.
  Staying on an old pin means running unsupported.
- **Provider CLIs auto-update hourly**, outside the OpenBot
  pin. Battery results are therefore "OpenBot v0.78.0 plus
  the provider CLI versions at run time"; the plan records
  the provider and CLI versions at install. How a CLI
  auto-update behaves across an OpenBot version bump is
  unobserved — labeled unmeasured wherever the plan leans
  on it.
- **Database migrations are one-way**, with no pre-upgrade
  backup taken by the platform. **Pin the image tag, and
  back up the data volume before any upgrade**; the plan
  records the backup's location and date.
- **Docker is the documented staging shape**: the pinned
  image (`ghcr.io/nightly-labs/openbot:<tag>`), build
  provenance verified before first run (`gh attestation
  verify`), the compose and seccomp files taken from the
  pinned tag (not from main), bridge networking, **no
  published ports**, a single data volume, no host folder
  mounts, no Docker socket. The desktop app is the fallback
  shape — with the standing caution that at Full access an
  agent can read anything its OS user can read, so the
  container or VM is the only boundary; never stage with
  host folders mounted into a full-access agent.
- **Analytics**: production builds send metadata events, the
  opt-in starts ticked for US users, and turning it off
  still sends anonymous install events (vendor-documented).
  The install turns it off at first run and the plan records
  it as known egress either way.

## Install steps — how the template contents become an install

`template/` in this pack holds the contents, prepared in the
repo. They become an install in this order:

1. **Stage the platform** per the update posture above
   (pinned image, attestation verified, no published ports)
   and create the agent. The plan names every agent already
   in the container, because each one holds the access this
   install is about to use (warning 1).
2. **Write the `AGENTS.md` seed** from
   `template/agents-md.md`, placeholders filled, put in
   place by the user (or written by the agent and read back
   by the user). Then verify it binds: a fresh interactive
   conversation shows the seed's reporting format unprompted
   — the battery's own check (Test 1).
3. **Create the workspace files** from
   `template/workspace.md` starters: the run-record with its
   header, the decision queue, `SETUP-PLAN.md`, and the
   memory files (module 01's templates, in the workspace).
4. **Add the skills** from `template/skills/` verbatim. Read
   each back from the library and compare content — the
   platform generates its frontmatter from the skill text,
   so a frontmatter diff is not drift (Test 8).
5. **Create the routines** from `template/routines.md`,
   saved instructions verbatim, left paused. Read each
   saved instruction back against the approved text before
   enabling anything; enabling each routine afterwards is
   the user's act, after they have read its instruction.
   Real schedule values are chosen with the user at
   creation; the plan records each routine's cadence.
6. **Set the Access mode and record the grants** — as found
   first, then as confirmed — in `SETUP-PLAN.md`, with the
   user present (see Approvals). Confirm the local-scripts
   API is off. Record the egress decision (human-landed;
   no credential, or "Only this agent").

## Deferred checks on OpenBot

Deferred checks live in `SETUP-PLAN.md` in the workspace, and
the weekly memory-audit routine's instruction includes
reading it and surfacing any check whose due date has passed
— a routine is a fresh context that reads the files it is
told to read, which is the measured route. `AGENTS.md` may
also carry the wizard's session-start surfacing line for
interactive sessions, but it binds in chat only (Test 1), so
the audit routine is the surfacing route the install relies
on. A deferred check with no routine to surface it is a
failed check, as the wizard says; if the user declines the
audit routine, the plan names what surfaces the checks
instead, or the install does not close.

## Verify (this pack)

*At install:* the `AGENTS.md` seed in place, read back, and
shown binding in a fresh interactive conversation; the
Access mode and any credential grants recorded as found
before the install changed them, and read back as the user
confirmed them; the local-scripts API confirmed off; each
routine created paused-then-enabled per the plan, its saved
instruction read back verbatim against the approved text and
its cadence in the plan's routines section; the run-record
file created with its header; the decision queue,
`SETUP-PLAN.md`, and the memory files in the workspace,
created from the `template/workspace.md` starters and module
01's templates; the skills read back verbatim (content
compared, frontmatter excepted); the watch routine's target
in place as its definition describes it, before the watch is
enabled; jobs reconciliation read from the routines store or
UI — not from the agent; the egress decision recorded
(human-landed, per Test 7 Open); the data-volume backup
recorded before any upgrade is contemplated.

*Deferred:* the first brief run lands inside its window and
appends its line; the first silent-watch run appends its
line with no post — the `[[no-update]]` probe, where a post
is a finding, not a pass; the first memory audit runs and
its findings are decided; a skill invoked in a fresh session
and in an unattended run; the first fire after a host sleep
gap surfaced as missed rather than silently caught up. Each
is ledgered in `SETUP-PLAN.md` with a due date, as the
wizard requires.
