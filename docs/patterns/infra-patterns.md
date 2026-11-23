# Infra Patterns (reference — not an installable module)

Patterns for users with a host they control (home server, VPS),
distilled from the maintainer's working setup. The theme is the
same as the rest of the kit: a backup that isn't verified is a
rumor, and a monitor that can fail silently will.

**Why this is a document and not a module.** Through v0.3 this
shipped as module 07. It was demoted in v0.4 for three reasons: it
was never rehearsed as an install (both wizard dry runs withheld
it, and host work is slow, host-specific, and partly irreversible —
storage choices, retention, offsite credentials — in a way a
sandbox rehearsal cannot exercise cheaply); it is the least
Muse-specific material in the kit; and its genuinely kit-specific
kernel — watches that write run records, flag failed runs, and make
their own silence detectable — already lives in module 02's Watches
pattern. What remains here is sound ops practice, kept where a
reader can use it without the wizard taxing every install for it.

## Layered backups

1. **Image layer.** Nightly snapshots/images of every guest or
   service that would hurt to rebuild, with short retention
   (keep-last 2 is plenty) — and a storage location that is *not*
   the disk whose failure you're protecting against. Check the
   free-space math after every change: retention × image size vs.
   target capacity.
2. **File layer.** An encrypted, versioned backup (e.g. restic) of
   system state and configuration, nightly, with retention tiers
   (daily 7 / weekly 4 / monthly 6) and a weekly prune.
3. **Offsite layer.** The file layer mirrored to object storage
   nightly. Media collections are a deliberate, stated exclusion —
   or not; but state the choice, don't drift into it.
4. **Verification.** A scheduled verify pass that test-reads the
   newest archive per guest (integrity check + completion log),
   checks ages against a staleness threshold, and reports
   PROBLEMS-FOUND or OK. A backup system whose verify hasn't run is
   flagged exactly like a failed backup. Test restores: at least
   once at setup, from *each* layer, byte-compared.

## Health watches

- A lightweight host watch (every 30 minutes): disk thresholds,
  service liveness, backup freshness — writing a run record every
  time, alerting only on exceptions, at most one alert per issue
  per day. (This is module 02's watch pattern pointed at a host.)
- A disk tripwire a few points *below* the level where backups
  start failing, so the first alert arrives while there's still
  room to act.
- Root-cause discipline: when a disk fills during a backup window,
  the backup may not be the only writer. Log sizes in the window
  before concluding.

## Script-first detectors

Module 02's watch pattern states the architecture — a cheap
script polls and diffs against a small state file, silent on
no-change, waking an agent only on a verified change — and the
guardrails (unreadable is a report once, a full sweep stays as
the safety net, over-sensitive on purpose, VIP/security checks
before any mute rule). What follows is the shape of three real
conversions, generalized: each began as an agent run on a clock
and ended as a detector that spends agent time only on judgment.

- **Inbox triage.** An agent scan every 30 minutes across the
  waking day is 48 agent runs a day, nearly all of them learning
  that nothing needed it. Converted: a script polls the mailbox
  every 5 minutes, diffs against its state file (seen message
  IDs, a noise list), and wakes the agent only for mail that is
  neither seen nor muted. The agent grades and judges what
  survives — the shield, the interrupt rules — and feeds its
  mutes back into the noise list, so the detector gets quieter
  weekly. Verify the conversion both ways before trusting it:
  unjudged mail must wake, all-muted mail must stay silent, and
  both runs write their records.
- **Host health watch.** An agent checking host health every
  2 hours is 12 runs a day reading mostly-green dashboards.
  Converted: a script detector every 30 minutes (thresholds,
  liveness, freshness — the checks above, mechanized), waking
  the agent only on an exception, plus a daily full agent sweep.
  The honest coverage note matters more than the savings: the
  checks that need judgment over the whole estate — which
  automations are off, a full device census — live in the
  sweep, not the detector. The detector does not cover them,
  and the layout record says so, so nobody reads the detector's
  silence as the sweep's all-clear.
- **A booked flight, months out.** No detector needed — the
  lesson is cadence banding. Daily agent checks on a flight
  half a year away buy nothing; the schedule rarely moves that
  far out. The watch bands: daily at booking, every 3 days
  through the quiet middle, daily again inside 30 days of
  departure, stepping up automatically as the event nears.
  Match the cadence to how fast the source can change, and let
  the calendar, not habit, set the rate.

The common thread: the agent's context is the expensive,
judgment-bearing resource. Spend it on the change, the
exception, and the periodic full read — never on the polling.

## Alerts that reach a human

- Route alerts to a phone notification channel the user actually
  sees (a self-hosted push service works well), with priority
  discipline: the highest priority is reserved for true emergencies,
  or the user learns to ignore the channel — and then it isn't one.
- Uptime monitoring watches the services; a dead-man's-switch
  service watches the jobs (a job that stops checking in pages
  exactly like a job that failed).

## Tracing agent work

Module 02's watches make a job's silence detectable; they do
not say what happened inside a run that did execute. For agent
work running on a host you control, trace it:

- **One trace per operation, a span per step.** Model calls,
  tool executions, retrievals, and sub-agent spawns are child
  spans carrying token counts (split input / output /
  cache-read — the splits are priced differently), latency,
  and a typed error. Multi-turn sessions correlate as threads
  of traces, so a failure mid-chain has an address instead of
  a shrug.
- **Emit OpenTelemetry GenAI conventions** (the `gen_ai.*`
  attributes — operation name, provider, model, token usage)
  rather than a proprietary schema, so the backend stays
  interchangeable. **Pin with your eyes open:** as of late
  2026 every GenAI convention is still marked Development, not
  Stable; the conventions moved to their own repository in
  Jun 2026, which has no tagged release. Pin to a commit or a
  dated snapshot, and expect attribute churn — dashboards
  built on the conventions may need migration as they settle.
- **Attribute cost from the spans.** Aggregate tokens to run,
  agent, and feature from the same records (module 09's run
  logs are the small-install form of this). Cost per
  *successful* outcome is the figure worth charting; per-attempt
  totals reward setups that fail cheaply and often.
- **Classify every failed run.** A failure taxonomy, not
  anecdotes: framework, model routing, memory, ingestion,
  tools, execution, observability — plus the agent-specific
  classes, coordination failures and judge failures. A class
  that recurs is a finding with a basis; a pile of unclassified
  failures is weather.
- **Content capture is opt-in, with redaction, never
  default-on.** Traces that record full prompts and tool
  payloads by default are a privacy leak and an
  injection-evidence leak in one. Record the metadata; sample
  content deliberately, when a diagnosis needs it.

## Audit the lanes after they run

Some lanes act on instructions alone — an inbox triage that
must never send mail or create drafts, a household watch that
must never write to the shared surfaces it reads. Their
prohibitions are prose, and a prose prohibition deserves a
check that does not trust the lane's own report:

- **A deterministic, read-only audit, run after the fact.**
  Nothing blocks the lane; the audit reads records and flags
  for human review. Build wake spans from the detector logs —
  a wake plus the window a worker could plausibly act in —
  then read the live systems for effects inside those spans:
  messages sent or drafted, shared records created or
  modified. An effect timestamped inside a span is flagged,
  with the attribution stated as what it is: circumstantial.
  A flag means *review this*, not *proven*.
- **State the coverage limits in the record.** Some legs have
  no ground-truth source — a click leaves no trace in any
  system the audit can read; a shared document may carry no
  per-edit authorship. The audit reports those legs as partial
  rather than claiming a check it did not make. An audit that
  hides its blind legs is worse than none: it converts "not
  checked" into "checked".
- **Cadence beats depth.** A monthly audit of a lane that runs
  daily permits a full cycle of undetected violation, so
  audit per run: a script-first detector polls on a short
  cycle, audits each wake once its span has fully closed, and
  records every wake's result — silent when clean, waking a
  reporter only on a flag. A leg that cannot be read is
  retried a bounded number of times across polls, then
  recorded **UNVERIFIED** as its final state and surfaced in
  rollups — never silently dropped, and never reported as
  clean.
- **Roll the per-run records up.** A monthly pass reads the
  per-run log plus one full-window cross-check run, so slow
  drift and attribution edge cases (one event inside
  overlapping spans is one event, however many spans recorded
  it) get a second look at human cadence.

Whether the audit itself catches what it should is a recall
question, and recall is proven by seeding, not by quiet
months: module 05's audit method ("Measure detective controls
by seeding them") carries that discipline, and it applies to
this audit exactly as it does to the lanes it watches.

## If you adopt these

Work them as their own project, under the kit's normal rules:
inventory hosts and guests with the user (every guest, or
rebuildable ones excluded — a stated choice); stand up the layers
in order and run test restores before declaring any layer live;
record the layout — locations, retention, exclusions, restore
steps — where a future session (or a future human) can find it.
Standing up backup infrastructure is exactly the kind of
partly-irreversible work the ticket rule exists for.
