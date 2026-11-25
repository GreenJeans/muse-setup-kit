# Grok Bot

Platform material for running the kit on Grok Bot (xAI's consumer
agent app, on Cursor's platform), a hosted assistant whose bots have
real routines, a real shell on a hosted computer, account-shared
skills, and platform-owned memory — and no instruction file.

**Read these two warnings before anything else in this pack. Both
are measured, not conjectured:**

> **A second bot is not a sandbox.** On one account there is one
> computer, one filesystem, one skill library, and one connector
> set. A bystander bot created mid-test could immediately read the
> working bot's workspace files, fire its skills, and reach every
> connected account. Only the conversation and each bot's private
> memory are per-bot. Creating another bot creates another
> *conversation*, not another agent.

> **Every bot on the account can read everything every other bot
> can read.** Anything one bot can reach — files, skills,
> connected accounts, the account-level user profile — every bot
> can reach. Treat every bot on the account as the same agent for
> security purposes, because the platform does.

## What this pack is

A profile (`grok` in `wizard/manifest.yaml`) plus this folder:

- `WIZARD.md` — the overlay on `wizard/SKILL.md` for the `grok`
  profile (modules 00 and 01, in the forms below). The installing
  agent reads it after the wizard. It is counted in the profile's
  audit figure.
- `MISMATCHES.md` — the rehearsal-divergence ledger: places where
  the overlay at the pinned commit and a live install diverge, one
  entry per mismatch, statuses edited in place. It is counted in
  the profile's audit figure.
- `template/` — the contents of a bot template, prepared in the
  repo: the bot description (which is the template's instructions
  field), the skill set, the routine definitions, and the starter
  contents for the workspace files a template cannot carry.
  Publishing the template in the Grok app is a separate, ticketed
  step and is not part of this pack's install. The template files
  are counted in the profile's audit figure.
- This README is for people; the installing agent does not need it.

## How the kit maps onto Grok, as measured

The platform was measured with a ten-test battery on a live account
(2026-11-23): 7 Pass, 2 Partial, 1 Fail. The pack is built only
from those results; the overlay states the score behind each
surface it uses.

- **Module 00** ships as *reference text + a memory-seed list*.
  Grok has no instruction file and no settings field for standing
  instructions; rules live in platform memory, stated by the user
  in their own words in chat. Memory-saved rules were measured to
  bind in chat *and* in unattended routine runs — the strongest
  instruction-surface result the battery has recorded on any
  platform it has run on. Seed carefully, though: a cleanup pass
  removed a fact from the account-level user profile cleanly,
  while two facts saved under a memory store the platform's tool
  had since retired refused exact-text removal — that store now
  read-only, and no user-facing removal surface found. A seed
  can become effectively permanent through no act of yours; the
  overlay carries the caution in full where the seed list
  lives.
- **Module 01** ships its *audit half only*: lint and fidelity
  checks over Grok's memory stores, which are legible, dated, and
  searchable, so audits are runnable. The architecture half does
  not ship, with the reason stated in the overlay: the schema and
  the history are platform-owned, and there are no verify
  pointers. Kit-grade history, if wanted, lives in workspace files
  the bot maintains, with platform memory as the index.
- **Module 04 is excluded.** The battery's isolation test failed:
  a coordination layer designed on assumed isolation would be
  designed on a fiction. This is a single-bot pack, and it says so
  wherever the question could arise.
- **Jobs are routines.** The pack's routine templates carry
  verbatim saved instructions and the run-record pattern (each run
  appends a line to a record file; the record is the run history
  and the silence detector — measured working). Routine timing is
  approximate: allow at least ten minutes of drift, "exact"
  settings included.
- **Approvals are Auto-review recipes** — Always Ask for sends,
  deletes, and purchases, with rule changes confirmed by the user
  on a card — plus one warning the overlay teaches at full
  strength: **the shell path is unreviewed. A push is a send.**
  Measured: branch and tag pushes over the shell ran with no
  confirmation card at all, in a class the bot itself listed as
  stop-first.

**Status: rehearsed — run 29 (2026-11-23) at b1efc3b.** The
platform was measured by the battery; the pack was then installed
end to end on a live account through the template front door, and
the imported bot is the live install. docs/REHEARSALS.md row 29
is the record; the front door's parameter declarations are the
weakest surface the run found. The capability answers behind
the profile are in docs/capability-profiles.md (Platform answers:
Grok Bot).
