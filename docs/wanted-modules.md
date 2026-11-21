# Wanted modules

Field modules the project would like to see built. None of
these belongs in the core library: each serves a domain the core
maintainer does not run, which is exactly what field libraries
are for. The package format and gates are in `docs/library.md`;
how contributions work is in `CONTRIBUTING.md`.

Each entry gives the sketch and the constraint that shapes it.
The constraint is not fine print. In every case it is the reason
the module needs care, and a design that ignores it does not
meet the risk gate. One boundary, stated once: compliance with
the law and the rules of these domains is the field
maintainer's and the installer's responsibility. The core
maintainer does not perform legal, medical, or regulatory
review, and a listing is not one either.

## Housing and rental operations

Unit turns, maintenance requests, a rent ledger, notices with
deadlines: the recurring work of running rental housing with an
agent's help. This is the richest worked domain outside the core
maintainer's own setup that the kit's design reviews (blind
rounds by two outside AI models, recorded in docs/ROADMAP.md)
saw, and both reviewers agreed on its shape: contributed by the people
who do the work, not written for them from outside. Notices and
ledgers mean third-party data and send/file actions, so the risk
gate applies in full: two rehearsals, one with a leak check, and
§13 handling for tenant records throughout.

## Caregiver coordination

An agent helping someone coordinate care for a family member:
appointments, medications, documents, and several adults sharing
the work. The constraint is structural. Module 03's sharing rules
ban health detail on shared surfaces, and caregiving's core
content is health detail, so this cannot be a profile or a
variant of module 03; a profile cannot override a module rule.
It must be its own module, with its own answer to what may be
shared, with whom, and where the rest lives. The
sensitive-records rule (procedures §13) is a prerequisite, not
an option: health records live in named local files, and shared
surfaces carry pointers and logistics, never the detail.

## Small-business back office

The one-person business: customer inbox triage, invoice chasing,
appointment and seasonal checklists, review replies drafted in
the owner's voice. The kit has no work-life module by design;
this is a field-shaped gap, not a core one. The constraint is
authorization. Business sends are externally visible acts, so
the ticket rule applies to them, and the module has to say
plainly which sends, if any, the owner pre-approves as standing
patterns and which always need a fresh ticket. A standing
pattern is not an exemption from the ticket rule: it must
itself be exact and ticket-shaped (the named send, the exact
class of content it may carry, a cap, a fallback), approved
once by the owner, and anything outside it needs a fresh
ticket. The module may not create an approval the core rules
do not grant. Drafts in the owner's voice are the easy part;
the send discipline is the module.

## Medical-records organizer

Claims, deadlines, per-account balances against limits, question
lists before appointments: the paperwork layer of dealing with
insurers. Field only, and the constraint is the strictest on
this page. These are §13 records in two classes at once (health
and financial). Files live locally, in a named folder the user
chose. Nothing goes on a shared surface, nothing goes to a
multi-agent exchange, and the agent never asks for a portal
password or a claim number in chat: data arrives as exports the
user downloads or files the user places, or it does not arrive.
A design that starts from "connect to the insurer" starts
wrong.

## Not modules, still wanted

- **Adopter rehearsal reports** for any core module, in the
  shape `docs/REHEARSALS.md` keeps. Several core modules are
  unrehearsed at their current pins, and the Standard profile
  has never been installed as a unit. A stranger's run is worth
  more than the maintainer's tenth.
- **Translations of the worked example** in `docs/examples/`,
  if anyone is moved to make one. The example is the fastest way
  for a new reader to see what an install leaves behind; a
  faithful translation (structure and scrub intact, idiom local)
  widens that door. A translation needs a second reader of the
  language, names the source pin it was made from, and is marked
  stale when the example changes.

## Claiming one

Open an issue first, naming the module and the library it will
live in, and title it "Claim: <module>" so open claims are
findable at a glance. That takes a minute and saves real waste:
two people building the same module in parallel helps neither.
The issue is a claim, not a commitment; if you stop, say so in
the issue and the claim lapses. A claim with no update for 60
days is stale: anyone may ask in the issue, and with no reply
within 14 days the claim lapses on its own. When the package
exists, the recommended road in is the one `CONTRIBUTING.md`
describes: rehearsal at a pin, then listing, then, if you want
it, review by someone who is not you. Recommended, not
required; a listed library can hold any of those, or none of
those. And a field module's review record lives in the
reviewer's own vetting log. It does not travel with the
library, and there is no shared field review list yet.
