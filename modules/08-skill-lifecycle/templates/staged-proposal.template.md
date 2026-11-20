# Staged Proposal Template

One folder per proposal: `staged/<queue-number>-<skill-name>/`,
containing the three files below. Copy this template for
`proposal.md`; `diff.patch` and `base.json` follow the shapes given.

A proposal without a matching base hash is invalid and is not staged.
Before staging, check the staging folder and the decision queue for an
open item on the same skill and the same lesson — a hit means append
evidence to the existing proposal, never a second queue item.

## proposal.md

```markdown
# Proposal — <patch | support file | create> `<skill-name>`

## Signal
<Which rubric signal fired, in one line: user correction (style /
workflow), verified fix, or a loaded skill that was wrong or stale.>

## Evidence
<Verbatim: the user's correction quoted exactly, with chat and date —
or the verified fix, what was tried, and how it was verified working.
No paraphrase where a quote exists. Dead ends and unverified attempts
do not belong here.>

## Preference-order justification
<Why this target: (1) the skill in play, (2) an existing umbrella,
(3) a support file under an umbrella, (4) a new class-level skill.
Name the earlier options and why each did not fit. For a create, the
name is class-level: no dates, error strings, codenames, or numbers.>

## Change summary
<What the diff does, in plain lines: +N/−M in <file>, the rule or step
added/changed, and the effect on the skill's behavior.>

## Risk if wrong
<The worst plausible outcome of applying, and how it is reversed
(reject a later patch, restore from version control, un-archive).>

## Routing note
<Anything from the same signal that belongs in memory instead of the
skill, and where it went — or "none".>
```

## diff.patch

A unified diff against the live skill for a patch or support-file
proposal. For a create: the complete proposed `SKILL.md` plus a list
of every file the create would add.

## base.json

```json
{
  "targets": ["<path to each live file the diff touches>"],
  "sha256": {"<path>": "<sha256 of the live file at review time>"},
  "reviewer": "<in-session | nightly-sweep | platform-loop>",
  "session": "<chat or session reference + date>"
}
```

The hashes are the read-before-write attestation: the reviewer read
exactly these bytes. At apply time the live files are re-hashed; any
mismatch aborts the apply (see MODULE.md, Pattern 2).
