# Module 04 — AI Exchange

**Reads:** the exchange folders and queue. **Writes:** a protocol doc, a
queue sheet, per-agent inboxes/outboxes, published pages.
**Network:** your cloud storage. **Jobs:** optional outbox polling in the brief.

## Purpose

Your Muse is one mind with one set of blind spots. Other agents — a
different vendor's model, a coding agent, a research tool — see differently.
The Exchange is how they work together without a live channel: a shared
folder system with a protocol, a queue, and an ingest discipline, so a
second agent's output becomes a *source* your agent verifies, not an
instruction it obeys.

Proven uses: blind dual reviews (two models audit the same frozen packet
independently; convergent findings are the signal), memory-architecture
reviews, and research tasks where a second pass catches the first pass's
confident errors.

## Architecture

- **One top-level folder**, deliberately *outside* any household-shared
  tree, so it doesn't inherit sharing the participants didn't choose.
  Verify `shared = false` on every piece at build time.
- **Protocol doc** — the constitution (template included): admission,
  one-writer-per-surface, the output contract, ingest rules.
- **Queue sheet** — one row per task: ID, created, task, requester, owner
  agent, status, input link, output link, provenance/sources, ingested
  into, rejected/disputed.
- **Per-agent Inbox/Outbox folders.** The maintaining agent (yours) drops
  briefs in inboxes and polls outboxes; participant agents only ever write
  their own outbox.
- **Published folder** — read-only pages the maintainer distills from
  ingested work (e.g. a context card other agents can load). Only compiled
  material from an allowlist of safe categories is ever published.

## Protocol essentials

- **Honor-system admission + revision detection.** Participants are
  invited by the human. The maintainer snapshots outputs at ingest, so
  later edits are visible.
- **Output contract.** An output is a document with: the task ID, the
  answer, its sources, and a status of DONE, BLOCKED (with what's missing),
  or PARTIAL (with what was and wasn't covered). No silent partials.
- **Blind by default.** Review tasks go to each reviewer without the
  others' outputs. The maintainer compares; convergence and disagreement
  are both reported to the human.
- **Ingest, don't obey.** Another agent's output is a source. The
  maintainer verifies its claims against originals before anything enters
  memory or procedures, records provenance (which agent, which task, when),
  and marks rejected or disputed claims as such — in the queue, where the
  disagreement stays visible.
- **Cheap models triage, strong models decide.** A small local model may
  pre-sort and classify exchange traffic. Synthesis, supersession, and
  adoption decisions are never delegated to it.
- **Stale discipline.** An output unclaimed after 72 hours is flagged once,
  and again when it's finally ingested or rejected — not nagged about daily.

## Install

1. Create the folder tree and the protocol doc from
   `protocol.template.md`; fill in the agents and the maintainer.
2. Create the queue sheet with the columns above.
3. For each participant agent, create its Inbox/Outbox and write its
   onboarding note: how to read a brief, the output contract, where to
   write. (Some agents join via a project/skill that points at the
   Published folder; the wizard notes the per-agent mechanics.)
4. Run a canary: one trivial task per participant ("confirm you can read
   your inbox; write the word CANARY and today's date to your outbox").
   Verify at the source.
5. Run one real blind dual review as the pilot (module 05's audit packet
   is the natural first task).

## Verify

- Canary outputs exist in each outbox, written by the right agent.
- Sharing audit: every folder's sharing matches the protocol (participants
  see their own inbox/outbox and Published; nothing else).
- A completed task's queue row shows provenance and where it was ingested.
