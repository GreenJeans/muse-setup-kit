# Module 01 — Memory Architecture

**Reads:** your memory files. **Writes:** a schema file, header stamps,
a linter and its reports. **Network:** none. **Jobs:** one weekly linter run.

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
   as absent.
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

## Layout (adapt to your platform's conventions)

- A curated long-term memory file (current state + a Superseded section).
- Dated daily logs (raw material; the authority for exact figures).
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
   adapt its paths): it runs three checks — (a) every compiled page
   carries a provenance header, (b) live bullets containing figures carry
   a source or `(verify: ...)` pointer, (c) job names in the procedures
   exist in `JOBS.md`, the scheduler-of-record the wizard maintains. It
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
