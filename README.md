# 🧰 Muse Setup Kit

> *Turn a fresh Muse install into a disciplined personal agent —*
> *procedures, memory, a morning brief, and (if you want them)*
> *multi-person and multi-agent coordination patterns.*

Everything here was distilled from a working installation, then scrubbed:
**patterns travel, instances don't.** No names, accounts, infrastructure,
or personal data from the original setup appear anywhere in this repo.

---

## What you actually get

A morning, a few weeks in (fictional, but true to format):

> **Brief — Tue 07:19**
> ⚠ Backup watch: no run record in 52h. The watch is the failure.
> ⚠ Decision queue: 3 items waiting (oldest 6 days).
> ✓ All scheduled jobs ran. Inbox: 2 need you, 9 filed silently.
>
> **Decisions:** 1) Renew the domain ($14, auto-renew is off).
> 2) Skill proposal `weather-brief`: 6-char hash `a91f3c` — reply
> "2: approve" and exactly that diff lands, nothing else.

And when something irreversible comes up, your agent stops and
writes a ticket — exact action, exact total, exact fallback — and
waits. That's the kit working. The rest of this page is how to
install it, and what it costs to read first.

## Quickstart

Copy this to your Muse. That's the whole install step:

```
Install the Muse Setup Kit for me: clone
https://github.com/GreenJeans/muse-setup-kit, check out the latest
release tag, then read wizard/SKILL.md and run the setup wizard.
```

Nothing to fill in. The wizard checks out the latest release tag,
resolves the full commit hash itself, and shows it to you in the
plan before anything is installed, so you can compare it against
the release page if you want to. Nothing installs before you
approve that plan.

Want an exact pin instead of the latest tag? The release page
carries the full hash for each release. Give it to your Muse with
the prompt and the wizard will verify the checkout matches it
exactly, and stop if it doesn't.

One more thing before you start: know which billing bucket the
install session draws on (subscription, API key, a router). An
install is heavy work — a full one reads on the order of 64,200
words of kit — and the wizard's first step will ask. If you don't
know, that's worth finding out before, not after.

That's the whole path. The wizard interviews you (multiple choice, a few
minutes), checks which capabilities your install actually has, shows you a
complete plan — every file, job, and shared surface, with each module's
reads/writes/network disclosed — and installs only what you approved,
verifying each module as it goes.

One honest request, from the kit's own security rules: **read
`wizard/SKILL.md`, `wizard/manifest.yaml`, each module's
`module.yaml`, and the `MODULE.md`,
`VERIFY.md`, templates, and any `tools/` scripts of the modules you
plan to install, at your pinned commit, before you approve the plan.** A setup wizard is an instruction
surface, and reading only the entry point leaves the actual payload —
the module instructions your agent will carry out — unaudited. Check
that the pinned-commit, plan-before-changes, and nothing-fetched-at-
install-time rules are intact; if any is missing, you're looking at a
fork that dropped the safety properties.

**First time? Install a profile, not the whole shelf.** The audit
cost below is the wizard, the manifest, and every file an install
reads in that profile's modules (MODULE.md, VERIFY.md, templates,
and tools) — the reading the request above actually asks for:

| Profile | Modules | Audit cost | What you get |
|---|---|---|---|
| **Starter** | 00 + 02 + 09 | ~27,700 words | Tickets and a decision queue, a failures-first brief, a bucket register. No memory migration, no second person, no host. |
| **Standard** | Starter + 01 + 06 | ~35,300 words | Plus the memory schema with its linter, and the security pack. |
| Everything | all twelve modules | ~64,200 words | Module 08 at Full is ~7,000 of that; at its default Lite tier it reads far less (the Full-only sections are labeled and skippable). The remaining modules (03, 04, 05, 08, 10, 11, 12) are each offered on their own merits. |

Modules can be added later, one at a time (see `UPGRADING.md`).
Each module's rehearsal status is in `docs/REHEARSALS.md`; the
wizard states it at selection time, including "unrehearsed at this
pin — you would be the first" where that is true.

## How it works

1. **Interview** — who it's for, how much autonomy, daily rhythm, other
   agents, memory, infrastructure.
2. **Selection** — profiles first, then modules, capability-gated:
   no second person, no Household HQ offer. Degraded modes are named,
   not silent, and so is each module's rehearsal status. The full
   matrix of what each platform capability buys is
   `docs/capability-profiles.md`.
3. **Plan → approve → install → verify** — at-install checks run
   immediately; checks that need live operation are ledgered as deferred
   with due dates, never skipped quietly.

## Modules

| # | Module | What it gives you | Needs |
|---|--------|-------------------|-------|
| 00 | **Core procedures** | Ticket rule for irreversible actions, a numbered decision queue, ground-truth and abort-on-mismatch rules, room close-out, standing security rules, the sensitive-records rule, a continuity handover | Nothing — the foundation |
| 01 | **Memory architecture** | A compiled-memory schema (current state + superseded history, provenance, verify pointers), a deterministic linter, weekly fidelity sampling | 00 |
| 02 | **Morning brief** | A failures-first daily brief, inbox triage with interrupt rules and a scam & impersonation shield, silent-by-design watches whose silence is itself checked, an optional money watch, an optional promises & waiting-on ledger | 00; a mailbox/calendar helps |
| 03 | **Household HQ** | Two people, two agents, one shared coordination system: task layer, memory layer, a notebook protocol, a principles doc | 00; a second person with their own Muse; shared docs/tasks |
| 04 | **AI Exchange** | Several AI agents exchanging work through shared storage — protocol, queue, blind reviews, ingest discipline | 00, 01; shared cloud storage; at least one other agent |
| 05 | **Evaluation kit** | Blind dual-review audits of your own procedures, seeded-error tests, memory fidelity checks | 00, 01 |
| 06 | **Security pack** | Verify-before-install (with the connector/MCP vetting pack: provenance tiers, scope audits, tool-manifest pinning), one-time permission grants, content-exclusion lists, session canary, retitle-before-share | 00 |
| 08 | **Skill lifecycle** | A session-review rubric that stages skill lessons instead of writing them live, staged-diff approval through the decision queue, a curator that archives unused skills but never deletes — gates on, unlike the system it adapts | 00, 01 |
| 09 | **Cost & billing guardrails** | Bucket discipline for agent spending: know whether a run draws on a subscription, an API key, or a router before it starts; hard caps set in advance; a monthly spend check | 00 |
| 10 | **Deadlines & expiry register** | One local register of what expires — passports, licences, warranties, policies, certifications — each with a lead time and a pointer to the original; no document numbers stored | 00; 02 surfaces it in the brief (manual check without) |
| 11 | **Persona & soul** | Author the persona file instead of inheriting the stock template: an authoring interview, a front-loaded SOUL template filled with real examples, a mechanical linter, and staged-diff governance for every later change | 00; a persistent persona file |
| 12 | **Spaces & living dashboards** | Audit the pages your setup accumulates against live state, merge peers, fold research into lineage, set a sidebar budget, and build the survivors as living pages: exception-first, status as an enum, freshness-stamped, refreshed by machinery | 00; a spaces surface |

Not a module: **infra patterns** (layered backups, health watches,
alert discipline for people with a host) live in
`docs/patterns/infra-patterns.md` as a reference document — sound
practice, but never rehearsed as an install, so the wizard doesn't
install it. And `docs/governance-test.md` is a standalone discipline
check you can run against your *current* setup, kit or no kit.
## Design principles

One-line summaries of the kit's constitutional rules; the operative
text is module 00's procedures template, whose canonical-location
table says where each rule lives.

- **Reversible work is pre-authorized; irreversible work needs a ticket.**
  Sending, buying, booking, filing, deleting — each needs an exact,
  human-approved ticket (action, total, fallback), void if any detail
  changes.
- **Facts come from the original record.** Summaries are locators, not
  truth. Anything the agent will act on is re-read at the source.
- **Silence is a failure mode.** A scheduled job that owes a deliverable
  and produces nothing is an exception, not a quiet day. A watch that
  stops running is itself an alert.
- **Done means verified.** Completion is checked against the live system,
  never accepted from a worker's report alone.
- **Lint proposes, never resolves.** Automated checks surface candidate
  problems; a mind decides.

## Standing on shoulders

This kit is a distillation, and some of its best ideas started elsewhere:

- **Andrej Karpathy's "LLM Wiki" gist** — the compiled-memory pattern
  behind module 01: raw sources below, an agent-maintained wiki above,
  a schema file as the constitution. Google's **Open Knowledge Format**
  and Letta's **MemFS** converged on the same substrate and were useful
  prior art to check our schema against.
- **[awesome-muse](https://github.com/cszach/awesome-muse)** — a
  community survey of Muse resources. Several standing rules trace to
  incident reports collected there: share-link title leaks (hence
  retitle-before-share) and a Marketplace address leak (hence
  content-exclusion lists on every message ticket).
- **A "96 things" field report** by a Muse user on Reddit — the source
  of the ground-truth rule, abort-on-mismatch, the session canary, and
  the periodic hands-on review session.
- **"Having Muse use Gemini to upgrade itself"** (r/MuseAgent) — the
  spark for the AI Exchange and the blind dual-review audit method in
  modules 04–05: freeze a packet, let two models review it independently,
  adopt changes one by one.
- **Skill Harbor's catalog** — mined for patterns, never installed from:
  **Contract Reader** (quote ambiguous passages verbatim; mark unread
  sections "not verified"), **Home Maintenance** (the declare-equipment /
  mark-hire-out / state-your-skips checklist shape), and **Lifeboat**
  (the backup coverage guard that became a linter check).
- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)**
  (Nous Research, MIT) — the source of module 08's skill-learning loop:
  a background reviewer with an explicit rubric (corrections as
  first-class signals, patch the in-play skill before creating, class-
  level names, read-before-write) and a curator that archives unused
  skills without deleting them. Studied at source and adapted, not
  adopted as-is: Hermes ships its write-approval gates off and biases
  its reviewer to "be active"; the kit's version is gates-on, with
  staged diffs the user approves, and "nothing to save" as a neutral
  outcome.

- **The harness-engineering shelf** — Harbor's task-run shape (a task,
  a verifier, an oracle check) behind module 05's Track B; HumanLayer's
  **12-Factor Agents** checklist, borrowed from twice in module 00
  (error compaction, factor 9; pause/resume cards, factor 6); and
  walkinglabs' **Learn Harness Engineering** course, the fuller
  treatment of the verifier-gated feature list in module 00. Patterns
  studied and adapted; none of the three is a kit dependency.

Where a technique came from somewhere else, the module says so. The
procedures, templates, and the wizard itself are original to this kit.

## Repository layout

```
README.md            ← you are here
UPGRADING.md         ← moving an existing install to a newer pin
UNINSTALL.md         ← removing an install, verified clean
docs/                ← DESIGN.md (reasoning) · ROADMAP.md (status) · REHEARSALS.md (what's been rehearsed, honestly) · library.md (the module-library design) · capability-profiles.md (the capability matrix) · governance-test.md (standalone check) · examples/ (a worked example from a real rehearsal) · patterns/ (reference, not installed)
wizard/              ← SKILL.md (the wizard) · manifest.yaml (profiles + library data)
directory.json       ← generated catalog of the core library (tools/build_directory.py) · advisories.json (generated; advisories.yaml is its human-maintained source)
modules/
  00-core-procedures/      module.yaml · MODULE.md · VERIFY.md · templates/
  01-memory-architecture/  module.yaml · MODULE.md · VERIFY.md · SCHEMA + MEMORY templates · tools/ (reference linter)
  02-morning-brief/        module.yaml · MODULE.md · VERIFY.md · brief, money-watch (baseline, run records, job), and ledger templates
  03-household-hq/         module.yaml · MODULE.md · VERIFY.md · principles + partner-prompt templates
  04-ai-exchange/          module.yaml · MODULE.md · VERIFY.md · protocol template
  05-evaluation-kit/       module.yaml · MODULE.md · VERIFY.md · templates/ (fictional seeds) · tools/ (kit doctor)
  06-security-pack/        module.yaml · MODULE.md · VERIFY.md · vetting-log template · grants-inventory job template
  08-skill-lifecycle/      module.yaml · MODULE.md · VERIFY.md · templates/ (staged proposal, queue items) · tools/ (reference curator, stage check)
  09-cost-guardrails/      module.yaml · MODULE.md · VERIFY.md · templates/ (bucket register)
  10-deadlines-register/   module.yaml · MODULE.md · VERIFY.md · register template
  11-persona-soul/         module.yaml · MODULE.md · VERIFY.md · templates/ (SOUL template, authoring interview) · tools/ (soul linter)
  12-spaces-dashboards/    module.yaml · MODULE.md · VERIFY.md · templates/ (space audit, space scope, sidebar plan)
tools/               ← kit_selfcheck.py (the kit lints itself) · module_yaml.py (the strict package parser) · build_directory.py (generates directory.json + advisories.json) · tests/ (tool fixtures)```

## Status

Rehearsed, and then audited — repeatedly, by fresh agents in
sandboxes and by two outside models in blind review rounds. The
record, including what has *not* been rehearsed, is
`docs/REHEARSALS.md`; the history is `docs/ROADMAP.md`. v0.9 adds:
module 10, the deadlines & expiry register — the first module
designed under the library spec in `docs/library.md`, its data
class declared and its register an accumulating file; it was
rehearsed once at the v0.9 candidate (run 13, at abb9f86) and has
changed since — unrehearsed at this pin, and labeled that way.
Module 02 gains the promises & waiting-on ledger (the
return-and-refund tracker is its worked example) and the scam &
impersonation shield in triage — module 06's
content-is-not-instructions rule turned outward, with a pointer
from module 06.

On the unreleased **library branch**, the design in
`docs/library.md` is implemented: a `module.yaml` per module
(strict flat subset, fail-loud parser, MODULE.md header parity
checked by the selfcheck) replaces the manifest fragments;
qualified ids (`core/<module>`) throughout; `directory.json` and
`advisories.json` are generated at the repo root by
`tools/build_directory.py`; and the wizard gains the lifecycle
verbs — list installed / available / upgradable, suspend, the
narrowed repair, inspect, rollback, reconfigure, add/remove
library. A one-module field library (home operations) pilots the
package format from a separate local repository. The branch is
not a release: the verbs have not yet had a fresh-agent
rehearsal, and the merge is the maintainer's call. The branch
also adds module 11, persona & soul: the authoring interview,
template, and linter for the persona file every install already
has, rehearsed in runs 16–17 (see `docs/REHEARSALS.md`). It is
offered per module, not in a profile; which profile it joins,
if any, is a maintainer call for the merge.

License: MIT (see `LICENSE`).
