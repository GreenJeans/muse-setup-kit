# OpenBot

Platform material for running the kit on OpenBot, a self-hosted,
local-first agent workspace that runs other vendors' agent CLIs
as persistent teammates. Agents here have real files in a real
workspace, an `AGENTS.md` instruction file, routines that fire
on schedule with full tools, and a real shell — on a machine
you control, in a container you can pin.

**Read these three warnings and the license line before
anything else in this pack. The warnings are measured, not
conjectured:**

> **A second agent is not a sandbox.** Every agent in one
> container runs as one user and can read every other agent's
> files — a bystander agent read the working agent's canary
> across workspaces in the battery (Test 6, Fail). The only
> barrier was the model choosing not to. Isolation means one
> container per agent; there is no softer setting the battery
> measured, and this pack does not pretend otherwise.

> **Silence is a token, not an instruction.** A watcher told to
> post nothing posted a "nothing posted" message anyway
> (Test 10, Fail). The platform documents a `[[no-update]]`
> token for staying silent; it is untested. This pack's
> watchers answer the token *and* write a run-record line, so
> silence is both intended and detectable.

> **AGENTS.md rules don't reach routine runs.** A rule in
> `AGENTS.md` bound in every fresh interactive conversation and
> did not bind in unattended routine runs (Test 1, Partial).
> Standing rules seed into `AGENTS.md` for chat; every routine
> carries its full instructions, including the rules it needs.

> **License: OpenBot is PolyForm Noncommercial 1.0.0 —
> personal, research, and evaluation use only. Running it
> commercially breaches its license.** This pack is
> documentation and templates; the constraint is on the
> platform underneath it, and it is yours to respect.

## What this pack is

A profile (`openbot` in `wizard/manifest.yaml`) plus this
folder:

- `WIZARD.md` — the overlay on `wizard/SKILL.md` for the
  `openbot` profile (modules 00 and 01, in the forms below).
  The installing agent reads it after the wizard. It is
  counted in the profile's audit figure.
- `template/` — the contents an install puts in place: the
  `AGENTS.md` seed text, the skill set, the routine
  definitions, and the starter contents for the workspace
  files. The template files are counted in the profile's
  audit figure.
- This README is for people; the installing agent does not
  need it.

## How the kit maps onto OpenBot, as measured

The platform was measured with a ten-test battery on a pinned
Docker staging (2026-11-25, OpenBot v0.78.0): 3 Pass,
4 Partial, 2 Fail, 1 Open. The pack is built from those
results, each claim carrying its grade in the overlay
(battery-measured, vendor-documented, or unmeasured); the
overlay states the score behind each surface it uses.

- **Module 00** ships as an *`AGENTS.md` seed*. `AGENTS.md` is
  the one auto-loaded instruction surface, and it binds in
  interactive chat (Test 1, Partial — the Partial is the
  routine-run gap in warning 3). The seed carries the ticket
  rule, the reporting format, the correction rule, and the
  scope rule as text the user puts in place. A rule that only
  exists in a workspace file did not bind in chat (Test 4,
  Partial); the seed goes in `AGENTS.md` or it is not a
  standing rule. Routine templates embed their own copies of
  the rules they need, because `AGENTS.md` does not reach
  runs.
- **Module 01** ships *both halves*. The platform has no
  memory schema of its own — persistence is workspace files
  (Test 3, Pass), so the kit's markdown memory (current
  state, Superseded, verify pointers) lives in the agent
  workspace untouched, and the audit half (lint and fidelity
  over files, with a real shell) runs against it. This is
  the strongest memory substrate the battery has measured.
- **Module 04 is excluded.** The battery's isolation test
  failed: a coordination layer designed on assumed isolation
  would be designed on a fiction. This is a single-agent
  pack, and it says so wherever the question could arise.
  Anyone who wants more than one credentialed agent runs one
  container per agent.
- **Jobs are routines.** Saved instructions read back
  verbatim, runs execute with full tools, and fires measured
  0–3 seconds of drift (Test 2, Pass). The pack's routine
  templates carry the run-record pattern (each run appends a
  line; the record is the run history and the silence
  detector). Two cautions ride along: fires while the host
  sleeps do not run, and the agent's own account of its
  routines is not reliable — reconciliation reads the
  routines store, never asks the agent (Test 9, Partial).
- **Approvals are Access modes plus credential grants.** Three
  modes exist (Full access / Ask first / Workspace only);
  Full access does local reversible work unasked and reports
  afterwards, which is the kit's default posture. Commitment
  points stop at a credential-grant prompt, and the grant
  discipline is "Only this agent", never "All agents
  (Vault)" — warning 1 is why (Test 5, Partial). There is no
  standing pre-approval on this platform, and the pack does
  not pretend otherwise; the ticket rule rides in
  `AGENTS.md` and in the grant prompts.
- **Egress is human-landed for now.** A branch-and-tag push
  from the agent was not exercised (Test 7, Open); what is
  measured is that no push happens without a credential grant
  (Test 5). Until egress is exercised, releases are landed
  by a human, and the plan says so.
- **The pin is soft.** Support covers the latest release
  only, provider CLIs auto-update hourly outside the pin, and
  database migrations are one-way. The overlay carries the
  update posture in full: pin the image tag, back up the data
  volume before upgrades, and treat battery results as
  "this OpenBot version plus the provider CLI versions at run
  time."

**Status: battery-measured 2026-11-25 at v0.78.0; not
rehearsed.** The platform was measured by the battery; no
end-to-end install of this pack has run. The capability
answers behind the profile are in
docs/capability-profiles.md (Platform answers: OpenBot).
