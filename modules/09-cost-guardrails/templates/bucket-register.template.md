# Bucket register (template — module 09)

Copy this table into the procedures file (or wherever the install
keeps it) and fill it in with the user. The angle-bracket tokens are
fill-ins: a row that still contains one is unfilled, and module 00's
placeholder check will correctly flag the procedures file for it. One row per surface the
agent can spend from. A surface nobody can classify is a row with
Bucket: UNKNOWN — an unknown bucket is a finding, not a footnote,
and it blocks heavy work on that surface until it is classified.

| Surface | Billing bucket | Hard cap | Usage / billing page | Key scope | Last verified |
|---|---|---|---|---|---|
| <the agent itself> | <subscription / API org / router / own hardware> | <amount or "none — deliberate"> | <where the user checks spend> | <what the key can reach> | <YYYY-MM-DD> |
| <local models, if any> | own hardware | none (no marginal cost) | n/a | n/a | <YYYY-MM-DD> |
| <anything unclassifiable> | UNKNOWN | — | — | — | <YYYY-MM-DD> |

## Heavy-run declaration (the snippet rule 2 asks for)

Before a long or expensive run, the plan or kickoff message carries
three lines:

Bucket: <which bucket this run draws on>
Expected magnitude: <order of magnitude, in the bucket's own terms>
Cap check: <the cap in the register, and what happens when it hits>
