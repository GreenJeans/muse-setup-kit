# Module 01 — Memory Architecture

**Reads:** your memory files. **Writes:** a schema file, header stamps,
a linter and its reports. **Network:** none. **Jobs:** one weekly linter run.
**Data classes:** personal, third-party. **Action classes:** none.

## Purpose

A personal agent's memory is a compiled wiki: raw material (conversations,
logs, documents) is distilled into pages the agent actually loads. Compilation
drifts. Pages accumulate stale claims stated in the present tense, figures
copied from other summaries, and contradictions nobody noticed. This module
is the discipline that keeps the compiled layer honest, distilled from a
schema in daily use in a working installation.

## The five ideas

1. **Current state at the top; history below, never deleted.** When a fact
   changes, rewrite the live bullet and move the old claim to a History /
   Superseded section in the same edit, with what superseded it, the date,
   and the source. The present tense is a claim; keep it true.
2. **Exact figures come from source, never from a compiled page.** Amounts,
   dates, IDs, and counts are answered and acted on from the daily log or
   the live system. A compiled figure without a verify pointer is treated
   as absent. Sensitive figures (procedures §13) are never copied into
   pages or logs at all: memory records the holding's existence, its
   `(verify: ...)` pointer, and its review-by date, and the figure is
   read from the holding itself.
3. **Provenance is additive and cheap.** Pages carry a header (schema
   version, last verified, sources). Precise claims gain `(verify: ...)`
   pointers opportunistically. Guesses are tagged `[inference]` or
   `[hypothesis]` inline; untagged means fact.
4. **Lint proposes, never resolves.** A deterministic linter (plain code,
   read-only, same output every run) checks mechanical invariants: broken
   references, pages missing stamps, job names in procedures vs. the live
   scheduler, stale claims past their review-by date. Findings are
   candidates. A mind decides each one.
5. **Fidelity is sampled, not assumed.** Weekly, pick a few compiled claims
   at random and check them against their sources. Keep one known
   discrepancy as a standing test case — planted by the *user* (not the
   agent; a self-planted test is not blind) in a dedicated test page whose
   filename contains `fidelity-test`, which excludes it from the memory
   the agent loads and from the linter. The weekly sample reserves one
   slot for that page: the sampler's pool includes it even though the
   agent's loaded memory does not. The true value is recorded only in
   `memory/fidelity-test-log.md`. Never plant a false claim in a live
   page: the test exists to check the sampler, and a sampler that reads
   live pages would be trained on a lie. If the process can't catch the
   planted one, it isn't catching real ones either.

## Forgetting cleanly

Remembering has a counterpart. A topic can leave memory entirely, at the user's direction, and a good platform already knows how: ask the agent to forget something and it should plan before it deletes. Expect that shape, and distrust any agent that starts deleting without one.

This module installs no forget machinery. If your platform has no forget flow, the agent does not improvise one with direct deletions; it tells the user and stops.

**The flow.** If the request could match more than one topic, the agent stops and asks before listing anything. A request to forget triggers a read-only planning pass first: every place the topic lives (active memory, notes, preferences, goals, scheduled work, created items, dated logs, and History or Superseded entries) and anything that could write it back — a standing watch, a recurring job, a goal that would regenerate it. The plan comes back grouped in plain categories, irreversible steps flagged (a step is irreversible when the removal is not recoverable from a backup the user controls), limits stated. Silence, a partial yes, or a yes to a different scope counts as no. On an exact approval the producers stop first, then the copies are removed, then the result is verified fresh: "forgotten" is claimed only when a new search finds nothing active in the store and no producer remains; each named remainder is reported as a remainder, with its own process. Stopping a producer means disabling it; deleting its record is a copy removal, done in the copies step. Email, calendar entries, device records, and shared items are reachable but outside a forget request's scope; each needs a separate approval, and a forget request does not cover them. There is no bulk deletion: mixed files are edited, not truncated. Dated logs and History or Superseded entries are edited the same surgical way: the topic's sentences come out, the rest stays, and each edit is flagged irreversible in the plan. Where a log needs to show that a removal happened, leave a topic-free marker ("entry removed at user's request, YYYY-MM-DD"); that marker is the one sanctioned exception to raw authority and "never deleted". If the user would rather leave the logs untouched, the plan names them as a remainder instead.

A model request is one sentence: "Forget X — show me the plan first."

**Choose the right verb.** Not every removal is forgetting.

- **Supersede** when a fact changed and the trail matters. The default (idea 1): the live bullet is rewritten, the old claim moves to History with its date and source. Nothing is forgotten; the record stays honest.
- **Park** when a topic is dormant but may recur. Close the watches, shelve the ideas, keep the records. Nothing is deleted, and the topic can wake up intact.
- **Forget** when the topic should be gone entirely: the flow above, and only that flow.

This does not contradict "history below, never deleted." That rule governs how memory handles change on its own. Forgetting is the user's explicit instruction, carried out as a plan, never as agent housekeeping. The flow's surgical edit of dated logs and History entries is the one exception to the rule, and it runs on the same terms: in the plan, flagged, on the user's instruction.

**Honest limits.** Active memory, its derived copies, and its producers can be cleaned completely. What sits outside the agent's reach remains, named in the plan and never acted on: copies on other services, other people's copies, anything already published, and backups. A good plan names what remains instead of implying a total erasure, and each remainder has its own process.

**Why users ask.** Sometimes privacy. Just as often, hygiene: a dead interest left in memory keeps resurfacing in feeds, briefs, and proactive suggestions long after the user stopped caring. Forgetting takes a topic out of the agent's attention, not just out of its files.

## Layout (adapt to your platform's conventions)

- A curated long-term memory file (current state + a Superseded section).
- Dated daily logs (raw material; the authority for exact figures —
  except §13-class figures, which live only in their holdings).
- One page per person and per group, with Facts and History sections.
- A `SCHEMA.md` stating the rules (template included).
- The linter under a tools folder, with its run receipts kept.

## Install

1. Copy `SCHEMA.template.md` to your memory workspace as `SCHEMA.md`.
2. **Fresh install (interview Q5a):** create the store —
   `memory/MEMORY.md` from `MEMORY.template.md`, a `memory/logs/` folder
   for dated daily logs, and `memory/people/` + `memory/groups/` folders
   with an `INDEX.md` in each (the linter
   excludes INDEX.md files by name — they are generated listings, not
   compiled pages). **Migrating (Q5b):** stamp existing
   compiled pages with the header (schema version, last_verified,
   sources) instead; pages without a stamp are legacy, and the
   most-loaded ones migrate first.
3. Install the reference linter (`tools/memory_lint.py` in this module —
   adapt its paths): it runs four checks — (a) every compiled page
   carries a provenance header, (b) live bullets containing figures carry
   a source or `(verify: ...)` pointer, (c) job names in the procedures
   exist in `JOBS.md`, the scheduler-of-record the wizard maintains,
   (d) time-bound claims whose `(review-by: ...)` date has passed are
   flagged for re-verification or retirement. It
   is read-only and writes only its report; every report opens with a
   run receipt (timestamp, files scanned, checks run, findings count).
   Schedule it weekly and record the job in `JOBS.md`.
4. Create `memory/fidelity-test-log.md`; ask the user to plant one
   fidelity test case in a dedicated test page whose filename contains
   `fidelity-test` (excluded from loaded memory and from the linter): a
   harmless discrepancy between the test page and its cited source.
   Record the true value in the test log, wire the weekly sample to
   reserve one slot for the test page, and confirm the process finds
   the plant.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
