# Verify — Module 04: AI Exchange

## At install

- [ ] The folder tree exists: protocol doc, queue sheet, per-agent
      Inbox/Outbox, `Work/`, `Snapshots/`, Published folder with its
      first page.
- [ ] Sharing audit at the source: the tree sits outside any
      household-shared folder; every piece's sharing matches the
      protocol (participants reach their own inbox/outbox and Published,
      nothing else).
- [ ] The queue sheet has the protocol's canonical columns: ID, Group,
      Created, Task, Requester, Owner agent, Status, Input link, Output
      link, Provenance/sources, Ingested, Ingested into,
      Rejected/disputed.
- [ ] Each participant's onboarding note states the output contract.
- [ ] **Canary round-trip**: each participant reads its inbox and writes
      the canary to its own outbox — verified at the source, in the
      right folder, by the right agent. A failed canary stops the
      install like any other failed at-install check.

## Deferred

- [ ] **First real task** (due: first month): completes under the output
      contract (DONE / BLOCKED / PARTIAL stated); at ingest it is
      snapshotted into `Snapshots/` with an ingest memo, and its queue
      row shows provenance and where the output was ingested — or why it
      was rejected.
