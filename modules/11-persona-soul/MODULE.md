# Module 11 — Persona & Soul

**Reads:** the existing persona file if one exists, the
adopter's interview answers, and, for examples the adopter
cannot supply, their interaction history. **Writes:** the
persona file (SOUL.md), drafted from the interview and written
only on the adopter's approval; the soul linter, copied as a
tool. **Network:** none. **Jobs:** none of its own; the
periodic reread rides the brief's monthly pass or the memory
linter's weekly run when either is installed.

**Data classes:** personal, third-party: the adopter's own
preferences and voice, and the postures the file records toward
the people in their life. **Action classes:** none.

## Purpose

Every install has a persona file whether anyone authors one or
not: the platform ships a stock SOUL.md, and an unauthored one
is inherited boilerplate: template lines kept because they
sound right, describing behavior the agent would show anyway,
and silent on everything that makes this adopter's agent
theirs. This module authors the file deliberately instead:
an interview, a front-loaded template filled from the answers,
examples drawn from real history, and governance for every
later change.

The discipline the module teaches, in one paragraph: examples
beat adjectives (a trait written as behavior is followed, a
trait written as an adjective is performed); every line must
change a response in a situation the adopter can name, or it
is dead weight; values are stated as a priority order, because
unranked values get picked per session by the model's default
pulls; disagreement gets a ladder with a hold rule, because
style bans ("no empty praise") do not stop an agent agreeing
on substance; and the file's own edit rules are a gate,
because self-edits are the main channel by which a persona
drifts.

## What installs

- **SOUL.md** at the path the plan records (the platform's
  persona file), rendered from `templates/SOUL.template.md`
  and baselined static-rendered. Where a persona file already
  exists, this module merges rather than overwrites (wizard
  ground rule 4): the adopter's own wording survives where it
  does not conflict, and a conflict is a question, not a
  replacement. Stock lines the platform shipped are not the
  adopter's wording: each survives only through the
  delete-the-line test, with the adopter keeping it and the
  behavior it changes named.
- **The interview** (`templates/interview.md`), copied
  static-verbatim into the workspace's module record beside
  the plan: the deferred reread works from it, alongside the
  failure-mode checklist below, which stays with the module
  record the same way. Of the module's declared files, these
  and the linter are what land; the template itself lands
  only as SOUL.md, rendered.
- **`tools/soul_lint.py`**, copied from this module and
  baselined static-verbatim: the mechanical half of the
  module's checks (word cap, examples block filled, priority
  order present, governance footer present, inherited
  boilerplate flagged as warnings). Without shell + python it
  cannot run, and VERIFY.md carries the same checks as
  questions; the module degrades, it does not block.

## The procedure

The ask-draft-approve shape follows the Soul Finder pattern in
Nous Research's Hermes Agent, the same source module 08
adapts: ask plainly, draft from the answers, show the draft
for approval before writing anything.

1. **Ask.** Run `templates/interview.md` in conversation, one
   group at a time. Must-answer questions first; the short
   subset when the adopter's time is short. Record answers in
   the adopter's words where wording matters.
2. **Draft.** Fill `templates/SOUL.template.md` from the
   answers. Every must-answer answer lands in a named slot;
   an answer with no line in the draft is a drafting error,
   not an optional cut. The routing: Who I am from Q1, Q2,
   and Q4 (the AI-nature stance is its own line); the
   priority order from Q14; Voice and Modes from Q7–Q13,
   Modes merging the interview's two axes (tasks from Q10,
   audiences from Q9) into one table; Examples from Q8, Q24,
   and Q28, with the fallback below; Disagreement from Q17
   (the sequence), Q18 (loyalty's limits, which bound the
   ladder), Q20 (the threshold), Q21 (the form and the
   hold rule), Q22 (the re-raise), and Q23 (where to push
   harder, where to just execute); Temperament from Q15's
   task ranking (the care-versus-speed trait) and Q16's named
   habits; People as a synthesis of Q3, Q30 (hard lines),
   Q31 (the sharing posture), Q32 (who else), Q33 (quiet
   topics), and Q34 (other agents); Repair from Q36 (the
   disclosure threshold), Q37 (the repair shape), and Q38
   (repeated mistakes); governance from Q40–Q43. Sections
   the answers do not reach are cut, not padded: a short
   honest file beats a complete generic one. On a
   short-subset run, sections no subset answer reaches
   (Voice beyond what the examples show, Modes beyond the
   warm row) are cut the same way, and governance stands at
   the template's defaults where the subset does not ask —
   VERIFY.md sanctions the defaults. Run the failure-mode
   checklist below against the draft before showing it.
3. **Show.** Present the full draft. Approval of the setup
   plan was approval to run the interview, not to write the
   file; the draft needs its own approval, and edits the
   adopter makes while approving are the draft improving, not
   scope creep.
4. **Write.** Only on approval. Baseline the file, stamp the
   plan, and run VERIFY.md's at-install checks.

**The examples fallback.** The interview's highest-leverage
answers are the examples, and they are the ones adopters most
often cannot supply on demand ("name a reply that sounded
right" draws a blank). The fallback is never to invent a
persona from nothing. Where interaction history exists, the
agent drafts candidate exchanges from it, marks them as
drafted, and the adopter vetoes or picks. Where no history
exists — a first-run install, the cold start — candidates
are drafted from the adopter's interview answers applied to
situations the adopter names (named on the spot, or the
recurring tasks from Q10 where it was asked), each marked
drafted/provisional and individually approved the same way;
the plan ledgers replacing them with real-history exchanges
at the first reread. Fewer than four surviving exchanges is
a recorded gap in the plan, not a failed install. A drafted
example the adopter has not seen does not enter the file
either way.

## The failure-mode checklist

Run against any drafted SOUL.md, at install and at every
reread. One line each: the mode, and the fix.

1. **Vagueness / adjective soup.** Traits stacked with no
   behavior attached. Fix: rewrite each as trait + observable
   behavior + reason, or cut it.
2. **Performative traits.** A personality described but not
   acted on, or acted on as tics: catchphrases, forced jokes,
   a signature move in every reply. Fix: anchor the trait in
   the examples; if no example can show it, the trait is not
   real yet.
3. **Unresolved contradictions.** Two directives that collide
   with no rule for which wins. Fix: the priority order
   decides, or an explicit tie-breaker is written next to the
   pair.
4. **Sycophancy trap.** Style banned (no empty praise) while
   substance is not: premises accepted, positions reversed
   under pushback. Fix: the disagreement ladder, above all
   the hold rule: reverse on new evidence, not on pressure.
5. **Accretion / patch-log growth.** The file becomes a log
   of patches for past mistakes. Fix: the size cap, and
   history moves to the memory store; the live file holds
   current state only.
6. **Inherited boilerplate.** Template lines kept because
   they sound right. Fix: the delete-the-line test, applied
   line by line; the linter flags the known stock lines as
   warnings.
7. **Stale history steering.** Past names, retired frames,
   and old dates reread as present-tense instruction. Fix:
   history out of the live file, into memory, where it is
   labeled as history.
8. **Scope bleed.** Procedures living in the soul file (or
   persona living in the procedures), two copies drifting
   apart. Fix: procedures in module 00's file, persona here,
   each pointing at the other, never duplicating.
9. **Single-principal blindness.** The persona defined toward
   one person and improvised toward family, other agents, and
   everyone else. Fix: the People section, filled for every
   party the agent actually deals with.
10. **Premature self-edits.** A single bad session fossilized
    into permanent identity. Fix: the governance gate below;
    no edit off one incident.

## Governance

After install, SOUL.md changes follow module 08's staged-diff
pattern, whether or not module 08 is installed: the agent
proposes a diff with its reasons and its evidence, the
adopter approves the exact diff through the decision queue,
and nothing self-applies. Approval is void if the diff
changes. A change needs the threshold the file's governance
section states (a recurring pattern, or the adopter's
direction), never a single bad day.

Once in force, the file is reread whole on a cadence, to
catch contradictions and size creep as they build: the module
recommends folding the reread into the morning brief's
monthly (1st-of-month) pass where module 02 is installed, or
the memory linter's weekly run where module 01 is, and
ledgering it as a deferred check in VERIFY.md either way.
The reread runs the failure-mode checklist and the linter;
its output is staged proposals, not edits.

## Install

1. Confirm the capability gate: the platform keeps a
   persistent persona file (`persona-file`). Without one
   there is nothing for this module to author, and it is not
   offered.
2. Read the existing persona file if one exists, and note
   what the interview must preserve or deliberately replace.
3. Run the procedure above: interview, draft, checklist,
   show, approval, write. The wizard's persona step carries
   the same flow; a skip at any point is recorded in the plan
   with its cost stated (generic behavior, no examples, no
   priority order of yours, no governance), and no file is
   written.
4. Copy `tools/soul_lint.py` into the workspace's tools and
   baseline it static-verbatim; baseline SOUL.md
   static-rendered at the path the plan records.
5. Run VERIFY.md's at-install checks; ledger the deferred
   reread with its cadence and fallback date.

## Uninstall

SOUL.md is the adopter's content, not kit machinery. The
export offer in `UNINSTALL.md` applies: the agent offers the
file as an export before removing anything, and uninstalling
this module never deletes the persona file without the
adopter's say-so; the usual outcome is that the file stays and
only the linter copy and the module's plan records go. A
persona file left behind is the adopter's voice, kept on
purpose, not residue.

## Verify

See `VERIFY.md` in this module's folder for the checks, split
into at-install and deferred.
