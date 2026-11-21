# Module 08 — Skill Lifecycle

**Reads:** session transcripts, your custom skills, the decision queue,
scheduled-job records. **Writes:** staged proposals (never live skills
directly), a skill-usage ledger, decision-queue items, an archive folder
for retired skills, and a pointer line in the agent's main instruction
file (added at the Lite install). **Network:** none. **Jobs:** none at the
Lite tier; at Full, one nightly session-review sweep and one weekly
curator run.
**Data classes:** personal, third-party. **Action classes:** none.

## Purpose

An agent that can write its own skills will, over time, write too many,
let the good ones rot, and — if its writes land unreviewed — quietly
rewrite its own instructions. This module is the lifecycle that keeps
self-modification useful and safe: a review rubric that captures lessons
while a session is fresh, a staged-diff approval path the user clears
like any other decision, and a deterministic curator that retires what
is no longer used without ever deleting it.

The patterns are adapted from **Hermes Agent** (Nous Research, MIT) —
its background skill reviewer and its curator. One deliberate
divergence: Hermes ships its write-approval gates **off** by default
and biases its reviewer to "be active — a pass that does nothing is a
missed opportunity." This module inverts both. **Gates on, and "nothing
to save" is a neutral outcome.** A reviewer pressured to produce will
produce noise; a gate left off turns that noise into live instructions.

## Tiers

This module installs at one of two tiers. **Lite is the default**;
Full is an upgrade, offered under the conditions below.

- **Lite** — Pattern 1's in-session and explicit triggers only, plus
  Pattern 2's staged-diff approval. No tools, no scheduled jobs, no
  usage ledger, no shadow week: staging happens in sessions the user
  is present for, so the rollout gate the shadow week provides for
  the sweep is unnecessary. Staging expiry (14 days) still applies;
  with no runner, the agent checks staged ages whenever it files or
  applies a proposal and expires what is overdue, logging it.
  Everything Lite needs is discipline plus a staging folder.
- **Full** — everything in this module: the nightly sweep backstop,
  Pattern 3's curator with its ledger and the two reference tools,
  the shadow-week rollout, and the 30-day review. Offer Full when
  the user has **5 or more custom skills**, when Lite proposals are
  being missed between sessions (the user says so, or corrections
  visibly recur), or when the user asks. Below that scale the sweep
  and curator cost more attention than the skills they watch.

Upgrading Lite → Full is Install steps F1–F5 below; nothing Lite
built is redone.

Reading this module at Lite: Patterns 1–2 are yours. Pattern 3, the
Rollout section, and the curator's brief-reporting line under
Pattern 3 are Full-only and are labeled as such where they start —
a Lite installer can skip them on a first read.

## Pattern 1 — The session review (capture)

The highest-value skill signals are single-session: a correction, a
frustration, a fix that was just verified. A cross-session batch loop
sees them only if they recur. This pattern reviews one session at a
time, close to the event, and **stages** what it finds. It never writes
a live skill.

### Triggers (in order of value)

1. **In-session, at the moment of signal (primary).** When the user
   corrects the agent, or a non-trivial fix is verified, the agent runs
   the rubric below before closing the task and stages a proposal in
   the same session if it fires. No machinery — a discipline plus a
   staging folder.
2. **Nightly sweep (backstop; Full tier only).** A scheduled job scans the day's
   sessions one by one (never pooled — pooling is the platform-level
   loop's job, below), runs the same rubric, and stages anything the
   in-session pass missed. Silent unless it stages something or fails;
   a failed run is flagged like any other job's.
3. **Explicit.** The user asks for a session to be reviewed; the agent
   runs the pass on the spot.

Not adopted from the source system: a nudge to self-write after any
long task. Task size is not a signal; corrections and verified fixes
are.

### The reviewer

- A forked subagent where the platform supports one, or the agent
  itself acting under this rubric for the in-session trigger.
- **Write-only to staging.** Its only writable path is the staging
  folder. It cannot edit live skills, memory, jobs, or this rubric,
  and it cannot message the user — its output returns to the main
  agent, who files the queue item.
- Input: the session transcript (corrections are never summarized
  away), the list of skills loaded or read in that session, and the
  custom-skill index (names and descriptions only).

### The rubric

Signals — any one warrants a proposal:

- The user corrected style, tone, format, or verbosity. Frustration
  phrasing ("stop doing X", "you always do Y", "too polished") is a
  **first-class skill signal**, not only a memory signal. Route it to
  the governing skill's body: memory holds who the user is and current
  state; skills hold how to do this class of task for this user.
- The user corrected workflow, approach, or sequence.
- A non-trivial technique, fix, workaround, or tool-usage pattern
  emerged **and was verified working** in the session.
- A skill loaded this session was wrong, missing a step, or outdated.

Preference order — earliest that fits:

1. Patch the skill that was in play this session.
2. Patch an existing class-level umbrella skill.
3. Add a support file under an umbrella (`references/`, `templates/`,
   or `scripts/`) plus a one-line pointer in its `SKILL.md`.
4. Create a new skill — only if no class covers it, and the name is
   class-level. Never a session artifact: no dates, error strings,
   codenames, issue or PR numbers, no "fix-X / debug-Y" names.

Hard rules:

- **Read-before-write, mechanical.** A proposal against an existing
  skill must include a fresh read of that skill taken during the
  review, with its sha256 recorded in `base.json`. A proposal without
  a matching base hash is invalid and is not staged.
- **Verified fixes only.** Capture the fix, never the failure. Dead
  ends, environment-dependent breakage, transient errors that later
  resolved, and unresolved attempts are not captured. If a session
  ended without a working method, the only valid proposal is one for
  an independently verified alternative; otherwise, nothing to save.
- **"Nothing to save" is a neutral outcome.** The deliberate inversion
  of the source system's be-active bias. A reviewer that stages
  nothing has done its job.
- **Caps.** At most 2 proposals per session and at most 5
  staged-and-undecided proposals total, across all sources. At cap,
  the reviewer logs the signals and stages nothing — queue fatigue is
  a failure mode, not a backlog.
- **Self-exclusion.** The reviewer may not propose changes to this
  rubric, the operating procedures, the agent's main instructions,
  SCOPE files, or the curator. Procedure changes stay user-approved
  document edits in their own workstreams.
- **Sensitive records are never quoted as evidence.** A proposal
  never quotes a §13-class record (financial, health, third-party
  personal — procedures §13) into `proposal.md` or a queue item.
  A correction *about* a sensitive matter is recorded by topic,
  with a pointer to the session — the verbatim-quoting rule is for
  corrections, not for records.
- **Memory routing unchanged.** Facts about the user and current
  state still go to memory under its schema (module 01). This pass is
  skills-only; it does not become a second memory writer.

### Dedupe with a platform-level learning loop

If the platform runs its own background skill-review loop, it stays
unchanged — this module complements it rather than replacing it.
Staging is the single funnel. There is at most **one open proposal
per skill**: before staging, check the staging folder and the decision
queue for an open item on the same skill. A hit on an *unfiled*
proposal means append evidence (date, session, quote) to it. A hit on
a *filed* item — or a new lesson for a skill that already has one —
means restage: build a fresh proposal that supersedes the old diff
(with the added evidence or lesson folded in), void the old item, and
note the supersession on it. A filed proposal is never edited in
place; that is what makes approval bind to bytes (Pattern 2). If the
platform loop writes a skill directly for a lesson that also has a
staged proposal, mark the proposal superseded by that write and close
it — noted where the user will see it, never silently dropped.

## Pattern 2 — Staged-diff approval (the gate)

No new UI. A staged skill write **is** a decision-queue item (module
00) with a fixed extra structure, plus a staging folder holding the
full diff. The queue stays the single surface the user clears by
number.

### Staging area

One folder per proposal under this module's workstream folder. The
reviewer stages under `staged/draft-<skill-name>-<date>/` — it cannot
know the queue number yet, and pretending otherwise corrupts the
naming. The main agent renames the folder to
`staged/<queue-number>-<skill-name>/` when it files the queue item.
Contents:

- `proposal.md` — the signal; verbatim evidence (the user's correction
  quoted, with chat and date, or the verified fix and how it was
  verified); the preference-order justification; a routing note for
  anything sent to memory instead. Template:
  `templates/staged-proposal.template.md`.
- `diff.patch` — a unified diff against the live skill (patch or
  support file), or the complete proposed `SKILL.md` plus a file list
  (create).
- `base.json` — target path(s); the sha256 of each live file at review
  time (the read-before-write attestation); `diff_sha256`, the sha256
  of `diff.patch` itself; reviewer identity (in-session / nightly
  sweep / platform loop); session reference.

Staging expires undecided after **14 days**: expiry auto-rejects the
proposal (logged), it never applies it. Expiry has a runner at the
Full tier: the nightly sweep checks `staged/` on every run, and the
weekly curator run backstops it (`tools/stage_check.py` is the
mechanical helper). At Lite there is no runner; the agent checks
staged ages whenever it files or applies a proposal, as the Tiers
section states.
An expired item moves to `staged/expired/` and its queue item is
marked expired, freeing its cap slot.

### Queue items

Two item types, defined in the queue's header when this module
installs: `[type: skill-write]` for proposals from Pattern 1 (both
tiers), and `[type: skill-curator]` for Pattern 3 (Full tier only —
a Lite install defines only the first). Formats:
`templates/skill-queue-items.template.md`. The rules that make them
work:

- **Silence is never consent** — restated on every skill item. Its
  only default is *stay staged*, then expire.
- **Approval is the ticket.** "N: approve" authorizes exactly one
  application: exact action = the diff whose sha256 is printed on the
  item (and stored as `diff_sha256` in `base.json`), exact target =
  the base-hashed file, fallback = abort if *either* hash changed.
  The item shows the diff itself: 20 lines or fewer inline in full;
  longer diffs show their first 20 lines and the total, and approval
  of a longer diff must quote the diff hash's first six characters
  ("N: approve 3fa9c1"). It is not a standing approval — a changed
  diff, a changed target, or an expired item needs a new item.
  "N: edit: <change>" voids the item; the agent restages as a new
  numbered item (queue numbers are never reused).
- **Executable content escalates out of the queue — judged by effect,
  not file type.** A proposal escalates if it creates a skill, touches
  anything under `scripts/` or any code block, or adds text that tells
  the agent to run a command, call a service, use a credential, send,
  share, delete, or spend. (A skill body is instructions the agent
  follows: a prose line can be executable in effect while looking like
  a text patch.) The verbs bind on actions the text *instructs*, not
  topics it touches: an ordering or wording preference (cheapest-first
  results, terser output) is presentation, not spending, even though
  it is adjacent to money. Escalated proposals need the
  verify-before-install record (module 06) plus an explicit ticket.
  When unsure, escalate. One boundary case, worked: a patch that
  changes *when or how often* an existing, already-gated action
  happens — a reminder's cadence, the wording of an existing
  draft-first flow — adds no new action, recipient, or send, and
  stays a queue item. A patch that adds a send, a recipient, a
  channel, or any new instructed action escalates, however small
  the diff.

### Apply procedure (on approval, in session)

1. Re-read the target live file and the staged diff; compare both
   sha256 values to `base.json`. **Either mismatch → abort, report,
   restage fresh.** No silent rebase — this is module 00's
   abort-on-mismatch rule applied to skills.
2. Apply the diff (or the move, for curator items). One item, one
   application.
3. Verify: re-read the result; for a patch, confirm the changed lines
   are present and the rest of the file is unchanged outside the diff;
   for a create, confirm the skill appears where the index should show
   it; for an archive, confirm the folder listing on both sides.
4. At Full, update the usage ledger (patch counts, `last_patched`,
   curator states). Move the queue item to Resolved with outcome and date,
   move the staging folder to `staged/applied/` (kept 30 days, then
   cleanup is proposed — not automatic), and log the change.
5. If the skill carries a managed review record, the apply also sets
   its success criterion and a `review_after` date (+30 days), so an
   approved change is itself audited. A change that fails its review
   is staged for revert as a new queue item — never auto-reverted.

## Pattern 3 — The curator (retire) — Full tier only

Deterministic only: a small script plus a ledger. No LLM pass, no
automatic consolidation or merging of skills.

### Usage ledger

One record per custom skill: name, `created` date (or null),
`seeded_on` (the day the ledger first carried the record — the
curator stamps it onto any record that lacks it), pinned flag,
`last_viewed` / `last_used` / `last_patched`, view / use / patch
counts, exemptions, and lifecycle state. Counts are best-effort and
will under-report — a skill applied from the prompt index may leave no
transcript-visible trace. Sources, in order: the nightly sweep's scan
of the day's transcripts (a read of a skill's file = a view; a read
followed by its procedure being applied = a use; when in doubt, count
a view), patch events from the apply procedure (mechanical), and a
one-time seed from verifiable records (anything unverifiable seeds as
null, protected by the grace floor below). Under-reporting biases
toward false "stale" — which is exactly why stale and archive are
proposals, not automatic moves. The reference implementation is
`tools/curator.py` (stdlib only, no network, never moves a folder).

### Lifecycle rules

- **Stale:** no view, use, or patch for **14 days** → state `stale`.
  Effect: a line in the next curator queue item. Nothing moves.
- **Archive candidate:** no activity for **30 days** → staged as an
  archive proposal (`[type: skill-curator]`). On approval, the agent
  moves the folder to `.archive/<name>/` inside the skills folder and
  sets the ledger state to `archived`. **Never delete.** Restore is a
  move back plus a ledger update; no queue item is needed if the user
  asks directly.
- **Grace floor:** a never-used skill is not an archive candidate
  until it is at least 14 days old. Zero uses is absence of evidence,
  not evidence of uselessness.
- **Exemptions** (never stale, never archive candidates; still listed
  in the ledger with their reason):
  - Pinned by the user in the ledger (the agent never pins on its own).
  - Referenced by any scheduled job — matched against `JOBS.md`, the
    scheduler-of-record, at each curator run: a job entry whose name
    is the skill's name, or the skill's name plus a suffix
    (`tax-docs-prep` runs `tax-docs`). When two skill names could
    match one job, the longest wins. (A prose mention of the name
    inside a job's description does not count; references in the
    procedures and other skills are matched as whole tokens.)
  - Referenced by the operating procedures or the agent's main
    instructions.
  - Linked as an amendment to a system skill whose own managed review
    cycle is live; the curator defers to that cycle and takes over
    only if it lapses.
  - Referenced by another active skill or connector doc (scanned at
    run time).

### The curator run

A weekly scheduled job runs the script: rescan the skills folder (new
skills get ledger records), recompute exemptions from live sources,
update states, and file at most **one** batched queue item per run
(the install hand run excepted — it files nothing; the user reviews
its report directly)
covering all stale and archive candidates. Each candidate in a
batched item is individually approvable ("N: approve <skill> only") —
approval applies per skill, never all-or-nothing by default. No
changes → no item, no message. The script never moves a folder; moves
happen only in the apply procedure, after approval, verified by
re-listing.

Deliberate deviation from the source system, which auto-archives at
30 days: here archive is gated because the counts are lossy and the
posture is approval-before-self-modification throughout. There is no
pre-written path to automatic archiving. A user who wants it must
first meet an evidence bar — at least 90 days of curator history, at
least 10 archive decisions, and no archive restored within 30 days of
its move — and the flip itself is a ticket, not a one-line edit.

### Reporting

One line in the morning brief (module 02) only when the curator staged
something. Monthly (the brief's 1st-of-month pass, or the curator
job's own monthly note if no brief is installed): total custom skills,
active / stale / archived counts, exemptions in force. No standalone
curator report.

## Rollout — shadow week (Full tier only)

Lite needs no rollout: its triggers fire in sessions the user is
present for, and its first staged proposal is itself the test. Full
adds machinery that runs while the user is away, so: do not switch
the sweep on live. Roll out in phases:

1. **Format first.** Queue header gains the two item types; staging
   conventions live; ledger built and seeded; curator script written
   and run once by hand, its first output reviewed by the user before
   any job exists. Nothing archives; stale flags only.
2. **Shadow week.** For 7 days, *both* staging triggers — the nightly
   sweep and in-session staging — stage only to `staged/shadow-*`,
   file no queue items, and report only to this module's home. The
   user judges each shadow proposal keep-or-noise. **Pass bar:** at
   least 2 shadow proposals, at least half judged keep. Below the bar,
   tighten the rubric and run another shadow week; fewer than 2
   proposals extends the week by 7 days; two failed weeks means
   recommend in-session-only staging and drop the sweep. Shadow lifts
   only on the user's explicit say-so, recorded as a job change.
   During the shadow week the `shadow-` naming replaces Pattern 2's
   `draft-` naming — everything stages to
   `staged/shadow-<skill-name>-<date>/`. Shadow folders do not expire
   during the week (the expiry runner skips them); at the lift
   decision each is judged — keepers are re-staged as real proposals
   with fresh base hashes and filed, noise moves to
   `staged/expired/`. Nothing shadow-staged is left in limbo.
3. **Curator gating live.** Archive proposals start flowing as queue
   items (still approval-gated).
4. **Review at 30 days** (counted from the day shadow lifts — the
   day the sweep goes live). Acceptance rate (the success bar: at least
   half of staged items approved or edited — below that, the rubric
   is too loose and gets tightened before any expansion), false-stale
   count (an archive restored within 7 days counts as one), restage
   rate (if more than about 1 in 5 applies aborts on hash drift, the
   staging window is too long — shorten the expiry), and queue load.
   Two warnings are read as warnings, not health: **zero rejections
   and zero edits** across the window suggests rubber-stamping, and
   the reviewer reports corrections it saw in transcripts that never
   became proposals (the recall gap) alongside its precision.

## Install — Lite

1. Choose the module's home: a workstream folder with a `SCOPE.md`
   (module 00). Create `staged/` inside it, with `staged/applied/`
   and `staged/expired/` holding folders. Defaults, unless the plan
   renames them: home folder `skill-lifecycle/`.
2. Add the `[type: skill-write]` item type to the decision queue's
   header, at its `ext:queue-header` anchor (module 00's
   extension-point registry), using the definition in
   `templates/skill-queue-items.template.md`, and confirm the
   never-consent rule is stated in that header definition.
3. Copy `templates/staged-proposal.template.md` where reviewers
   will find it (the module home).
4. Add a pointer line to the agent's main instruction file, inside
   its `ext:instruction-pointer` anchor: skill
   self-modification stages through this module; nothing writes a
   live skill without the user's approval of the staged diff.

That is the whole Lite install: no tools copied, no jobs scheduled,
no ledger created.

## Install — upgrading to Full (F1–F5)

Assumes Lite is installed; nothing below redoes a Lite step.

F1. Add the `[type: skill-curator]` item type to the queue header
    (same template file).
F2. Seed the usage ledger (`skill-lifecycle/skill-usage.json` by
    default): one record per existing custom skill, created dates
    from verifiable records only — the skills folder's own records,
    a git history, dated session logs (a date asserted only inside
    the skill's own file is taken as given, and recorded as
    taken-as-given, not dressed up as verified) — null when no
    record exists; the curator anchors those to the `seeded_on`
    stamp it writes on every record, and reports dateless records
    as unseeded. Counts are zero where unverifiable — counts are
    never null (a null count reads as "used" to the curator and
    defeats the grace floor; null is for dates only). The ledger's
    record format is the one `tools/curator.py` writes — fields
    listed under Pattern 3 — and seeding matches it exactly, one
    way only: the curator's first hand run (F3) creates records for
    skills not yet ledgered. Do not hand-write records ahead of it.
    A "verifiable" created date is one from a record (a dated log,
    a commit, the user's statement); never backfill a date from a
    file's mtime and call it created.
F3. Copy `tools/curator.py` and `tools/stage_check.py` into the
    module home, point the curator at your skills folder, ledger,
    procedures/instructions files, and job records; run it once by
    hand and show the user its first report. Do not schedule it
    yet. "Pointing" the curator is command-line flags — there is
    no config file — so record the full invocation, flags
    included, in the `JOBS.md` entries when the jobs are created
    (F5); the flags live there.
F4. Run the shadow week (Rollout, above).
F5. After the user approves the rollout, schedule the two jobs
    (sweep nightly, after the day's work; curator weekly, early
    enough that its item makes the next brief), record both in
    `JOBS.md`, and start the sweep live.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.

## Attribution

The review rubric, the forked-reviewer shape, and the curator
lifecycle are adapted from **Hermes Agent** by Nous Research
(https://github.com/NousResearch/hermes-agent, MIT), studied at source.
The gates-on posture, the staged-diff queue mechanics, the "nothing to
save is neutral" inversion, and the shadow-mode rollout are this kit's
adaptation, not Hermes features.
