# Muse Setup Kit

A field kit for turning a fresh Muse install into a disciplined personal-agent
setup: operating procedures, a memory architecture, a morning brief, and —
optionally — multi-person and multi-agent coordination patterns. Everything
here was distilled from a working installation, then scrubbed: **patterns
travel, instances don't.** No names, accounts, infrastructure, or personal
data from the original setup are included anywhere in this repo.

## Use it

Tell your Muse:

> Clone this repository, read `wizard/SKILL.md`, and run the setup wizard.

The wizard interviews you (multiple choice, a few minutes), checks which
capabilities your install actually has, and installs only the modules you
pick. Before it changes anything, it shows you a plan — files it will create,
jobs it will schedule, surfaces it will touch — and waits for your approval.

## Modules

| # | Module | What it gives you | Needs |
|---|----------|------------------------------------------------|-------|
| 00 | Core procedures | Ticket rule for irreversible actions, a numbered decision queue, ground-truth and abort-on-mismatch rules, room close-out, standing security rules | Nothing — this is the foundation |
| 01 | Memory architecture | A compiled-memory schema (current state + superseded history, provenance, verify pointers) plus a deterministic linter | Module 00 |
| 02 | Morning brief | A failures-first daily brief, inbox triage with interrupt rules, silent-by-design watches | 00; a mailbox/calendar helps |
| 03 | Household HQ | Two people, two agents, one shared coordination system (task layer + memory layer + notebook protocol) | A second person with their own Muse; shared docs/tasks |
| 04 | AI Exchange | Several AI agents (different vendors) exchanging work through shared storage, with blind reviews and an ingest discipline | Shared cloud storage; at least one other agent |
| 05 | Evaluation kit | Blind dual-review audits of your own procedures, seeded-error tests, fidelity checks for memory | 00, 01 |
| 06 | Security pack | Verify-before-install, one-time permission grants, content-exclusion lists, session canary, retitle-before-share | 00 |
| 07 | Infra patterns | Layered backups with verification, health watches, an alert channel that reaches your phone | A host you control (optional) |

## Design principles

- **Reversible work is pre-authorized; irreversible work needs a ticket.**
  Sending, buying, booking, filing, deleting — each needs an exact,
  human-approved ticket (action, total, fallback), void if any detail changes.
- **Facts come from the original record.** Summaries are locators, not truth.
- **Silence is a failure mode.** A scheduled job that owes a deliverable and
  produces nothing is an exception, not a quiet day. A watch that stops
  running is itself an alert.
- **The wizard is defensive.** This repo is an instruction surface other
  people's agents will execute. Every module declares its reads, writes, and
  network use up front, and the wizard applies nothing without showing the
  user first. Treat any third-party addition to this kit the same way: read
  it fully before you let your agent run it.

See `docs/DESIGN.md` for the reasoning and `docs/ROADMAP.md` for what's
planned. License: MIT (see `LICENSE`).
