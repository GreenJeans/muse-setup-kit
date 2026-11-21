# 🧰 Muse Setup Kit

> *Turn a fresh Muse install into a disciplined personal agent —*
> *procedures, memory, a morning brief, and (if you want them)*
> *multi-person and multi-agent coordination patterns.*

Everything here was distilled from a working installation, then scrubbed:
**patterns travel, instances don't.** No names, accounts, infrastructure,
or personal data from the original setup appear anywhere in this repo.

---

## Quickstart

Tell your Muse:

```
Clone https://github.com/GreenJeans/muse-setup-kit and check out commit
<PASTE THE FULL HASH FROM THE RELEASE PAGE>. Confirm git rev-parse HEAD
matches it exactly; if it does not match, or I gave you no hash, stop and
ask me. Then read wizard/SKILL.md and run the setup wizard.
```

The hash is the trust anchor: get it from the release page (outside the
repo), never from a file inside the checkout you are about to trust.

That's the whole path. The wizard interviews you (multiple choice, a few
minutes), checks which capabilities your install actually has, shows you a
complete plan — every file, job, and shared surface, with each module's
reads/writes/network disclosed — and installs only what you approved,
verifying each module as it goes.

One honest request, from the kit's own security rules: **read
`wizard/SKILL.md`, `wizard/manifest.yaml`, and the `MODULE.md` (plus any
`tools/` scripts) of the modules you plan to install, at your pinned
commit, before you approve the plan.** A setup wizard is an instruction
surface, and reading only the entry point leaves the actual payload —
the module instructions your agent will carry out — unaudited. Check
that the pinned-commit, plan-before-changes, and nothing-fetched-at-
install-time rules are intact; if any is missing, you're looking at a
fork that dropped the safety properties.

## How it works

1. **Interview** — who it's for, how much autonomy, daily rhythm, other
   agents, memory, infrastructure.
2. **Selection** — modules are capability-gated: no second person, no
   Household HQ offer; no host, no Infra. Degraded modes are named, not
   silent.
3. **Plan → approve → install → verify** — at-install checks run
   immediately; checks that need live operation are ledgered as deferred
   with due dates, never skipped quietly.

## Modules

| # | Module | What it gives you | Needs |
|---|--------|-------------------|-------|
| 00 | **Core procedures** | Ticket rule for irreversible actions, a numbered decision queue, ground-truth and abort-on-mismatch rules, room close-out, standing security rules | Nothing — the foundation |
| 01 | **Memory architecture** | A compiled-memory schema (current state + superseded history, provenance, verify pointers), a deterministic linter, weekly fidelity sampling | 00 |
| 02 | **Morning brief** | A failures-first daily brief, inbox triage with interrupt rules, silent-by-design watches whose silence is itself checked | 00; a mailbox/calendar helps |
| 03 | **Household HQ** | Two people, two agents, one shared coordination system: task layer, memory layer, a notebook protocol, a principles doc | 00; a second person with their own Muse; shared docs/tasks |
| 04 | **AI Exchange** | Several AI agents exchanging work through shared storage — protocol, queue, blind reviews, ingest discipline | 00, 01; shared cloud storage; at least one other agent |
| 05 | **Evaluation kit** | Blind dual-review audits of your own procedures, seeded-error tests, memory fidelity checks | 00, 01 |
| 06 | **Security pack** | Verify-before-install, one-time permission grants, content-exclusion lists, session canary, retitle-before-share | 00 |
| 07 | **Infra patterns** | Layered backups with a verification pass, health watches, an alert channel that reaches your phone | 00; a host you control |
| 08 | **Skill lifecycle** | A session-review rubric that stages skill lessons instead of writing them live, staged-diff approval through the decision queue, a curator that archives unused skills but never deletes — gates on, unlike the system it adapts | 00, 01 |
| 09 | **Cost & billing guardrails** | Bucket discipline for agent spending: know whether a run draws on a subscription, an API key, or a router before it starts; hard caps set in advance; a monthly spend check | 00 |

## Design principles

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

Where a technique came from somewhere else, the module says so. The
procedures, templates, and the wizard itself are original to this kit.

## Repository layout

```
README.md            ← you are here
UPGRADING.md         ← moving an existing install to a newer pin
docs/                ← DESIGN.md (reasoning) · ROADMAP.md (status)
wizard/              ← SKILL.md (the wizard) · manifest.yaml (modules)
modules/
  00-core-procedures/      MODULE.md · VERIFY.md · templates/
  01-memory-architecture/  MODULE.md · VERIFY.md · SCHEMA + MEMORY templates · tools/ (reference linter)
  02-morning-brief/        MODULE.md · VERIFY.md · brief template
  03-household-hq/         MODULE.md · VERIFY.md · principles + partner-prompt templates
  04-ai-exchange/          MODULE.md · VERIFY.md · protocol template
  05-evaluation-kit/       MODULE.md · VERIFY.md · templates/ (fictional seeds) · tools/ (kit doctor)
  06-security-pack/        MODULE.md · VERIFY.md · vetting-log template
  07-infra-patterns/       MODULE.md · VERIFY.md
  08-skill-lifecycle/      MODULE.md · VERIFY.md · templates/ (staged proposal, queue items) · tools/ (reference curator, stage check)
  09-cost-guardrails/      MODULE.md · VERIFY.md
```

## Status

Rehearsed, and then audited: the wizard was run end to end twice by
fresh agents with no memory of the original setup (a solo user, and a
two-person household), in sandboxes, and every friction finding from
both runs was fixed. The kit was then given to two outside models for
a blind adversarial review (module 05's method, applied to the kit
itself); their convergent findings — including a fictional quickstart
pin, an install that failed the kit's own linter, and a module with no
install section — drove v0.3, and module 08 was dry-run a third time,
by another fresh agent, before v0.3 was tagged. What has not been
rehearsed is said plainly in `docs/ROADMAP.md`.

License: MIT (see `LICENSE`).
