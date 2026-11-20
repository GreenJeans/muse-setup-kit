# Module 01 — Memory Architecture

**Reads:** your memory files. **Writes:** a schema file, header stamps,
a linter and its reports. **Network:** none. **Jobs:** one weekly linter run.

## Purpose

A personal agent's memory is a compiled wiki: raw material (conversations,
logs, documents) is distilled into pages the agent actually loads. Compilation
drifts. Pages accumulate stale claims stated in the present tense, figures
copied from other summaries, and contradictions nobody noticed. This module
is the discipline that keeps the compiled layer honest — distilled from a
schema that survived a blind dual review by two frontier models.

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
   discrepancy as a standing test case: if your process can't catch the
   planted one, it isn't catching real ones either.

## Layout (adapt to your platform's conventions)

- A curated long-term memory file (current state + a Superseded section).
- Dated daily logs (raw material; the authority for exact figures).
- One page per person and per group, with Facts and History sections.
- A `SCHEMA.md` stating the rules (template included).
- The linter under a tools folder, with its run receipts kept.

## Install

1. Copy `SCHEMA.template.md` to your memory workspace as `SCHEMA.md`.
2. Stamp existing compiled pages with the header (schema version,
   last_verified, sources). Pages without a stamp are legacy; migrate the
   most-loaded ones first.
3. Create the linter: start with three checks — (a) every compiled page
   carries a header, (b) no live bullet contains a figure without a source
   or verify pointer, (c) names of scheduled jobs mentioned in procedures
   exist in the live scheduler. Keep it read-only; it writes only its
   report. Schedule it weekly.
4. Plant one fidelity test case (a known, harmless discrepancy between a
   compiled page and its source, labeled in the test log only) and confirm
   the weekly sample process is capable of finding that class of error.

## Verify

- Change one fact in a daily log's domain (e.g. correct a date with the
  user) and watch the compiled page: live bullet rewritten, old claim in
  Superseded with date and source.
- Run the linter; it produces a report with a run receipt, and modifies
  nothing.
- Ask the agent for an exact figure that lives only in a compiled page
  without a verify pointer. It should go to the source or say it can't
  verify — not recite the compiled number.
