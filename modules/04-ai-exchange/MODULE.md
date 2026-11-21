# Module 04 — AI Exchange

**Reads:** the exchange folders and queue. **Writes:** a protocol doc, a
queue sheet, per-agent inboxes/outboxes, published pages, a `Work/`
folder for the maintainer's own outputs, and `Snapshots/` with ingest
memos.
**Network:** your cloud storage. **Jobs:** optional outbox polling in the brief.
**Data classes:** personal, third-party. **Action classes:** none.

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
  Verify at build time that each piece is shared with exactly the
  accounts in the protocol's Participants table, and no one else.
- **Protocol doc** — the constitution (template included): admission,
  one-writer-per-surface, the output contract, ingest rules.
- **Queue sheet** — one row per agent-task, with the canonical column
  list in the protocol (rule 2). A logical task with two reviewers is
  two rows sharing one **Group** ID, so the pairing is structural, not
  prose.
- **Per-agent Inbox/Outbox folders.** Participant agents only ever write
  their own outbox. The maintaining agent has no inbox/outbox: it drops
  briefs in inboxes, polls outboxes, and keeps its *own* outputs (e.g.
  its half of a blind review) in a `Work/` folder inside the tree.
- **Snapshots folder + ingest memos.** At ingest, the maintainer copies
  the output into `Snapshots/` (immutable, named by task ID) and writes
  an ingest memo beside it: claims verified, claims rejected with the
  verbatim text, convergence and disputes. This is the artifact that
  makes disagreement visible later.
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
  The mirror case matters as much: a queue row whose output *never
  arrives* is flagged once at 72 hours after assignment, and again when
  the output lands. Silence from a participant is a finding, not a gap
  in the record.

## Install

1. Create the folder tree — per-agent Inbox/Outbox, `Work/`,
   `Snapshots/`, and the Published folder — and the protocol doc from
   `protocol.template.md`; fill in the agents and the maintainer.
2. Create the queue sheet with the protocol's canonical columns.
3. For each participant agent, create its Inbox/Outbox and write its
   onboarding note: how to read a brief, the output contract, where to
   write. (Some agents join via a project/skill that points at the
   Published folder; the wizard notes the per-agent mechanics.)
4. Publish the first Published page — "Agent lanes & how to task us",
   from the protocol's allowlist — so participants have something to
   read on day one.
5. Run a canary: one trivial task per participant ("confirm you can read
   your inbox; write the word CANARY and today's date to your outbox").
   Verify at the source. The canary is an at-install check: a failed
   canary stops the install like any other.
6. Run one small blind review as the pilot (two reviewers, one short
   document, one Group ID). Once evaluation-kit is installed, its audit
   packet becomes the grown-up version of this pilot.
7. **Wire the read path.** Outputs nobody polls are work nobody did.
   If a morning brief is installed, add the `[IF ai-exchange installed]`
   source block from module 02's `brief.template.md` to the installed
   brief job: open queue rows checked against their owners' outboxes,
   with the 72-hour stale flags above. Without a brief, record outbox
   polling as a named chore in `JOBS.md` with an owner.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
