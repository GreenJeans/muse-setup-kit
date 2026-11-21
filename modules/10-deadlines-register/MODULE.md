# Module 10 — Deadlines & Expiry Register

**Reads:** the register file; a source document when its date needs
re-reading at the original. **Writes:** the register — one local file,
updated in place. **Network:** none. **Jobs:** none of its own;
surfacing rides module 02's brief when installed.

**Data classes:** personal — document types and expiry dates. The
register never holds a document's number (procedures §13).

## Purpose

Passports, licences, warranties, insurance policies, certifications:
every household has documents that expire, and the expiry tends to be
discovered at the moment it hurts — at the border, at the claim, at
the renewal that already lapsed. This module keeps one register of
what expires and when, with a lead time per item, so a renewal
surfaces while there is still time to act on it.

The register is deliberately small. It records *that* a document
exists, what it is, when it expires, and where the original lives.
It never records the document's number — no passport numbers, policy
numbers, or ID numbers (§13). The number is in the document; the
register points at the document.

## The register

One local file — `household/deadlines-register.md` by default; the
plan may choose another path and records it — built from
`register.template.md`. It is an **accumulating** file (the library
spec's file classes, `docs/library.md`): it grows by design in
ordinary use, so the install baseline inventories it and never diffs
it. One row per item:

- **Item** — what it is: a passport, a driving licence, a warranty,
  an insurance policy, a certification.
- **Expires** — the expiry date, read from the document itself. An
  item whose date nobody has read yet is recorded as `unknown` —
  never omitted. An omitted item cannot surface; an unknown one can
  be chased.
- **Lead time** — how far ahead the item should surface, set with
  the user per item: a passport wants months, a warranty wants
  weeks. Every row carries one — on an `unknown` row it is the
  provisional window, the lead time that applies the day the date
  is read; it cannot fire while the date is unknown, and the
  chase rule below is what surfaces the row meanwhile.
- **Source** — where the original document lives: a folder, a
  filing cabinet, a portal the user reads. A pointer, never the
  document, never its number.
- **State** — current, renewed, or expired.

Current state sits at the top. When an item is renewed, its row
updates in place — new expiry, state current — and the old expiry
moves to the register's History section with the renewal date.
Current state never carries two expiries for one item, and History
is never silently overwritten (the memory schema's
current-state-at-top rule, module 01).

An item past its expiry reads **expired**, and keeps reading that
way until the user renews it or drops it. It is never described as
clear, handled, or fine.

## Surfacing

A register nobody reads on cadence is a diary. Two shapes, and the
plan states in words which one an install has:

- **With module 02 installed**, the brief reads the register. The
  rule: an item surfaces in the brief's **Today** section on the
  first day `today >= expiry − lead time`, and stays there until
  it is renewed or dropped. An item already expired surfaces in
  **Failures** — an expired document is a failure, not a deadline.
  An item whose date is still `unknown` surfaces in **Today** as
  a one-line chase item in every brief until it is dated or
  dropped: both date-driven rules pass it by, and an unknown item
  nobody chases is an omitted item with extra steps — they are
  few by nature, and the register exists so they are not
  forgotten. The brief quotes the date from the register; when a
  date will be acted on, the agent re-reads the document itself
  (ground truth, §7).
- **Without module 02** there is no brief to ride, and nothing
  surfaces on its own. The module degrades to a deferred check: a
  dated entry in the plan's verification ledger (or the decision
  queue) under which the user or the agent reads the register by
  hand, on a cadence the user picks at install.

Adding an item is a conversation, not a form: the user names the
document, the agent asks for the expiry date and where the original
lives, and the row is written. Reading the date off the document
with parsing software is out of scope for this module — if the user
runs such an engine themselves, its output is a suggestion the user
confirms, and the confirmed date is what the register records.

## Install

1. Create the register from `register.template.md` at the path the
   plan records, and inventory it in the baseline as an
   accumulating file.
2. Seed it with the user: walk the obvious categories — identity
   documents, vehicle, insurance, warranties, certifications — and
   write one row per item the user actually has. Items the user
   knows exist but cannot date today go in as `unknown`. The seed
   is the user's list, not the agent's guesses. Expect the user
   to offer a document number while seeding — "put it in so we
   never lose it" is the sensible-sounding reason, and it will
   come up. Decline it, in §13's terms, and answer the actual
   worry: the number lives in the document, and the register's
   source pointer exists so the document can always be found.
   The refusal is the rule working, not a refusal of the user's
   goal.
3. Set each item's lead time with the user. Defaults exist to
   be argued with — six months for a passport, one month for an
   insurance renewal, two weeks for a warranty — and the plan
   records what was chosen. When a default supplies a value the
   user didn't state, the plan names it as a default: a value
   the user never said should never read in the plan as their
   answer.
4. Wire the surfacing, per the plan's shape: [IF morning-brief
   installed] keep the brief template's
   `[IF deadlines register installed]` block in the brief job's
   instructions — the block carries the surfacing rule (expired
   → Failures, in-window → Today, unknown-date → chase line).
   [IF morning-brief not installed]
   record the manual deferred check in the plan's verification
   ledger, with the cadence the user chose, and say in the plan
   that nothing surfaces on its own.

## Uninstall

The register is the user's content, not kit machinery. The export
offer in `UNINSTALL.md` applies: the agent offers the register as
an export before removing anything, and uninstalling this module
never deletes the register without the user's say-so.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
