# Fictional incident seeds — Module 05 starter library

**These incidents are invented.** They exist so a fresh install — one
with no real failures yet — can run a real first audit instead of
waiting to accumulate damage. Label any packet that uses them
"fictional seeds"; replace them with real seeds as real incidents
happen, and retire each fictional seed once a real one covers the same
failure class.

Seed format: what happened, when it was noticed, what it cost, which
rule or gap it points at. Facts only, no blame.

- **F-1 — The confident "done."** A nightly job failed on its first
  night (a path typo) and wrote its error to a log nobody read. The
  agent reported the job as running for nine days because its own
  setup note said it existed. Noticed when the user asked for the
  output and there wasn't any. Points at: completion claims made from
  records of intent instead of live state.
- **F-2 — The summary that ate a date.** Asked when a subscription
  renewed, the agent answered from a compiled summary page ("renews in
  March") instead of the provider record (March 27 of the *previous*
  year; it had already lapsed). The summary was a locator treated as a
  source. Points at: ground-truth discipline for exact figures.
- **F-3 — Silence, taken as a yes.** A low-stakes default ("if I don't
  hear otherwise, I'll tidy the archive folder") was applied by
  analogy to moving a folder that turned out to hold the only copy of
  a document. The default was printed for one action and borrowed for
  another. Points at: defaults bind to the exact action they were
  printed for, never to a class.
- **F-4 — The watch that died quietly.** A disk-space watch stopped
  running when its host rebooted; nothing restarted it and nothing
  missed it. The disk filled eleven days later. Points at: detector
  silence is itself a failure; every watch owes a run record.
- **F-5 — The approved summary.** A skill change was approved from the
  agent's one-line summary of its own diff. The diff also removed a
  safety check the summary didn't mention. Nothing bad happened — this
  time. Points at: approvals bind to bytes (the diff and its hash),
  not to summaries of bytes.
- **F-6 — The address that wouldn't die.** The user corrected an
  address in chat; the agent updated the daily log but not the
  compiled page, which kept serving the old address as current for a
  month. Points at: corrections propagate to every live copy in the
  same edit, or they haven't happened.
