# Design

## Why this kit exists

A personal agent accumulates power quietly: it reads your mail, knows your
family, can send, buy, book, and file. The techniques in this kit are the
control surfaces that make that power safe to use — procedures that separate
reversible work from irreversible action, a memory discipline that keeps the
agent honest about what it knows and how it knows it, and evaluation habits
that catch drift before it costs money or trust.

They were refined over weeks of daily use in one real installation. This repo
distills the *transferable* parts.

## Pattern vs. instance

Every working setup has two layers:

- **Patterns** — procedures, schemas, protocols, templates, checklists.
  These generalize. They are what this repo contains.
- **Instance data** — the user's name, family, accounts, infrastructure,
  finances, history. These never generalize and never leave the installation.

Rule for contributors and adapters: if a file would embarrass or endanger the
original user when published, it is instance data, whatever its format.
Templates ship with `<PLACEHOLDERS>`, never with filled-in examples drawn
from a real life. Where worked examples are included, they are invented
and obviously so.

## The formats are not ours

The kit's three file layers — plain-Markdown project instructions
(AGENTS.md), procedural skills (SKILL.md folders), and manifest-
bundled plugins — are open standards, and since late 2025 they
sit under foundation governance: MCP and AGENTS.md were donated
to the Linux Foundation's Agentic AI Foundation (AAIF) in Dec
2025, and Agent Skills followed in Oct 2026. That matters to a
kit built entirely out of those files: the formats will outlive
any one vendor's product decisions, they are stewarded in the
open, and an install written against them is not stranded when
a platform changes its mind. It is also why the kit pins and
vets third-party material in these formats like dependencies
(module 06): a shared standard is a shared supply chain.

## The defensive-wizard principle

A setup wizard is an instruction surface: someone else's agent will read it
and act. That is exactly the shape of a supply-chain attack, so the kit is
written to the standard it teaches (see module 06):

- Every module declares, in its header, what it **reads**, what it
  **writes**, what **network** access it uses, and what **scheduled jobs**
  it creates.
- The wizard presents a complete plan and waits for explicit approval before
  applying anything. Approval covers exactly what was shown.
- Modules are installed from this repo's files, pinned to the commit the
  user reviewed. Nothing is fetched from a third-party URL at install time.
- The wizard never asks for credentials in chat. Account connections use the
  platform's own secure flows.

If you fork this kit, keep those properties. A fork that drops them is a
different, lesser product.

## Opinions baked in

The kit is not neutral scaffolding; it encodes positions that were earned:

1. **Done means verified.** A task is complete when its deliverable checks
   out against the live system or original record — not when a worker,
   subagent, or scheduled job reports success.
2. **One home per topic.** Every workstream gets one home (a chat, a
   workspace, a doc) with a scope note: what it owns, what it must never do,
   what done looks like, and its source of truth.
3. **Batch the non-urgent.** Decisions that can wait go into a numbered
   queue the user clears in one pass. Interrupts are reserved for the
   time-sensitive, the security-relevant, and the people who matter most.
4. **Lint proposes, never resolves.** Automated checks on memory and
   procedures surface candidate problems; a mind decides.
5. **Audit on a cadence.** The procedures themselves get reviewed — blind,
   by a second model where possible — monthly while they churn, quarterly
   once stable, and out-of-cycle whenever a new failure class appears.

## What this kit is not

- Not a backup of anyone's installation. Nothing here restores a real setup.
- Not autonomous. The wizard proposes; the user disposes.
- Not a promise of parity. Modules assume different subsets of Muse's
  capabilities; the wizard gates on what an install actually has.
