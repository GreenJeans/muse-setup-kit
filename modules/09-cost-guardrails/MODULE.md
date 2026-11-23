# Module 09 — Cost & Billing Guardrails

**Reads:** your model/provider usage and billing pages (with you
present), the bucket register. **Writes:** a bucket register in the
procedures; decision-queue items when a cap is approached. **Network:**
your providers' billing pages only, with you present. **Jobs:** one
monthly spend check (rides the brief if installed).
**Data classes:** financial. **Action classes:** none.

## Purpose

Agent work can draw on several billing buckets that look identical
from the chat window: a subscription's included usage, an API key
billing per token, a third-party router with its own balance, a
per-seat tool. The surfaces do not tell you which bucket a run hits.
The user finds out from the bill.

The failure this module exists for is specific and common: a premium
model offered inside a subscription product turns out to draw on an
API organization instead. The user runs it hard, believing the work
is covered; the API meter runs until a spend limit stops it — and
because the limit stops it mid-task, the in-progress work is lost
too. Nobody acted in bad faith. The bucket was simply never checked.

## The rules

1. **Keep a bucket register.** A small table, maintained in the
   procedures, listing every model/provider surface the agent can
   use: which bucket it draws on (subscription / which API key or
   org / which router), the hard cap in place, and where usage is
   checked. When a connection or key changes, the register changes in
   the same edit.
2. **Declare the bucket before heavy work.** Before a long or
   expensive run — batch jobs, multi-agent swarms, premium models,
   bulk API work — the agent states, in the plan or the kickoff
   message, which bucket it draws on and the expected order of
   magnitude. If the agent cannot tell which bucket a surface draws
   on, that is a stop condition: it asks, or checks the provider's
   usage page, before the run — never after.
3. **Offers and trials are buckets too.** A model, feature, or
   "included" window offered inside a product may still bill to an
   API org or a separate balance. Verify from the provider's usage or
   billing page — not from the offer surface — before sustained use.
4. **Caps before convenience.** Every API key or org the agent can
   spend from gets a hard spend cap when it is created, set by the
   user, recorded in the register. A cap that stops a run mid-task is
   the system working, not a malfunction to route around; raising a
   cap is the user's call, made deliberately, never mid-incident.
5. **Separate keys per surface where the provider allows.** A shared
   key makes a burn unattributable — nobody can say which agent,
   project, or experiment spent it. One key per surface or agent
   keeps the register honest.
6. **Monthly spend check.** Once a month, read each bucket's usage
   (billing pages are read with the user present), compare against
   the register and the caps, and put surprises — a new bucket, a cap
   approached, spend with no matching work — in the decision queue.
   The check rides the morning brief's monthly pass if one is
   installed; without scheduling it is a manual chore with a named
   owner. Its sibling is the usage audit (module 05) — jobs ranked
   by load, no figures invented; money here, load there.
7. **Metered lanes log one cost line per run.** A dispatch lane
   that bills per use (an API lane, a router lane) appends a
   single line to its run log for every run: the model, tokens in
   and out, and the cost the provider reports for that run. Never
   an estimate, and never a figure reconstructed afterward from
   memory. A subscription lane exposes no per-run metering and
   logs nothing; a missing line is honest, an invented one is a
   false record. The monthly spend check (rule 6) reads the run
   logs, so its comparisons rest on recorded runs rather than
   recall. This is the small form of 2026 production practice:
   cost derived per run and aggregated per agent, because a
   single retry-looping lane can spend heavily before a human
   notices, and per-attempt totals hide it — what a deployment
   can act on is cost per successful outcome, which only
   per-run records can produce.

**Billing data is a financial record (procedures §13).** Usage
figures live in the register and on the providers' pages; a spend
check quotes figures from the source read in that run, and no
billing detail is copied onto shared surfaces or into compiled
memory beyond an existence pointer.

## Install

1. Build the bucket register with the user, from
   `templates/bucket-register.template.md`: every surface the agent
   can currently reach (the subscription itself, each API key/org,
   each router or gateway), its bucket, its cap, its usage page.
   Surfaces nobody can classify are listed as UNKNOWN — an unknown
   bucket is a finding, not a footnote.
2. For each API key or org without a hard cap, set one now (the user
   sets the amount) or record the user's explicit decision to run
   uncapped, in their words, in the register.
3. Add the declare-before-heavy-work rule (rule 2) and the register
   to the operating procedures, as §12, inserted at the procedures
   template's `<!-- ext:billing-buckets -->` anchor (module 00's
   extension-point registry names this module as the anchor's
   owner), replacing the reserved §12 stub the template ships at
   that anchor.
4. Record the monthly spend check in `JOBS.md` as its own bullet,
   marked "(rides morning-brief)" when the brief carries it (the
   brief template's monthly step has the gated spend-check line), or
   as a scheduled job or manual chore per the manifest's degraded
   mode. Detector silence reads cadences from `JOBS.md`, so the
   riding shape must be stated, not implied.

## Verify

See `VERIFY.md` in this module's folder for the checks, split into
at-install and deferred.
