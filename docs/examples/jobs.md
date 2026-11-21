# Jobs

The scheduler-of-record: every standing job the agent runs, in one
place, in one canonical form. The procedures file names jobs in
backticks; this file is where they are defined.

## Entry format (canonical — two kit tools parse this file)

One bullet per job, exactly this shape:

- `job-name` — cadence; what it owes; where it delivers; run record: <path or "the brief">

Rules both parsers (module 01's linter, module 08's curator) rely
on, and a fresh agent's future jobs must keep:

- The bullet starts with the job name in backticks, lowercase
  letters, digits, and hyphens (`morning-brief`, `skill-curator`).
  Bold (`**name**`) is also accepted by both parsers; backticks are
  the house style.
- One job per bullet. A job named in the procedures but missing
  here is a linter finding; a job here that nothing runs is drift
  for the morning brief's reconciliation.
- When a job is created, changed, or retired, this file changes in
  the same edit. The brief's detector-silence check reads run
  records against the cadences stated here: a job whose run record
  is 48 hours past its cadence is flagged as silent, and detector
  silence is a failure, not an all-clear.

## Jobs

<!-- Entries land here as modules install them, e.g.:
- `morning-brief` — daily at 07:19; the failures-first brief; delivers to the main chat; run record: the brief itself
- `spend-check` — monthly on the 1st (rides morning-brief); bucket usage vs caps; delivers via the brief; run record: the brief's monthly section
A check that rides another job still gets its own bullet, marked as
riding — detector silence reads the cadences stated here. -->

- `morning-brief` — daily at 07:30; the failures-first brief; delivers to the main chat; run record: the brief itself
- `spend-check` — monthly on the 1st (rides morning-brief); bucket usage vs caps; delivers via the brief; run record: the brief's monthly section

## Planned (not yet scheduled)

Jobs approved in a plan but not yet scheduled (module 08's rollout
waits for the user's scheduling approval, for instance) are recorded
here, in the same bullet shape, with the approval they wait on named.
Detector silence does not read this section. When a job is scheduled,
its bullet moves up to Jobs in the same edit.
