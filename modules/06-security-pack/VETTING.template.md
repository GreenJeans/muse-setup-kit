# Vetting Log

One entry per third-party skill, connector, or prompt pack considered.
Approval is per item, per pinned version, and never covers an update —
a version change means a new entry.

## Entry shape

### <ITEM NAME> — <YYYY-MM-DD>

- **Source:** <where it came from>
- **Pinned:** <version or commit hash>
- **Read in full at the pin:** yes / no / scoped — full for <scope>,
  <rest> not read (an unscoped "yes" for a partial read is a false
  record. If no: say plainly what was read instead — for a hosted
  connector, "source not readable — hosted" — and what observable
  surface the vetting ran on. Proceeding on that basis is the
  user's decision, recorded in their words under **Why**. For a
  connector or MCP server the presented manifest must still have
  been read in full; if it was not, stop)
- **Reads:** <files, accounts, data it accesses>
- **Writes:** <what it creates or changes>
- **Network:** <endpoints it contacts>
- **Credentials:** <what it wants, and where they are stored>
- **Removal:** <how to uninstall it completely>
- **Decision:** install / install narrowed (a reduced scope set,
  per module 06's scope audit — a different outcome from
  cherry-pick) / install with recorded reservations (name
  them — e.g. an abandoned but credential-free item) / cherry-pick
  (parts taken as patterns, rewritten locally) / reject
- **Why:** <one or two lines>

Connectors and MCP servers add these fields (module 06's vetting pack):

- **Provenance tier:** official / community / unknown
- **Typosquat check:** <name and source compared character-by-character
  against the official source — match, or the difference found;
  "no official comparator" when no official item exists>
- **Scopes / token privilege, as observed:** <each scope on the
  consent screen (or requested-scope list) at connection time, and
  the feature it maps to — vendor statements are not the record;
  for key/PAT servers, the token's breadth and whether a narrower
  or read-only token exists; "none" for a local-only item>
- **Accepted excess scopes:** none / <official tier only: each
  observed scope that maps to no wanted feature and that the user
  accepted anyway — the connector named, each scope named, in the
  user's own words, stating that a narrower configuration was
  unavailable or declined. This record is the user's decision,
  not an audit pass; community and unknown tiers have no such
  record — excess there is a walk-away>
- **Presented-manifest hash:** <sha256 of the presented manifest
  captured at first connection — server instructions, every tool's
  name, description, and input schema including parameter
  descriptions, and prompt/resource descriptions — saved exactly
  as received, in the order presented, as an artifact kept with
  this log; name the capture method if it was anything else. A
  vendor-published manifest file is compared against the capture,
  never used as the pin; a vendor-stated hash with no artifact
  behind it is recorded as "vendor-stated, unverifiable"; MCP
  servers only>
- **Re-vet trigger:** any version change; any scope increase; any
  presented-manifest hash change (re-checked at session start
  where the platform exposes it, and at the monthly inventory)

Field modules (kit-library packages) replace the connector fields
above with these (rules in `docs/library.md`). **A package
without a `module.yaml` is not a kit-library package: it is
vetted as a third-party skill pack under the standard record,
not under this block.**

- **Library / module:** <library-id>/<module-id>
- **module.yaml fields present:** <the fields docs/library.md
  requires, or what is missing>
- **Instructed action classes, declared vs found:** <send / file /
  spend / delete / contact — judged by effect, not file type; any
  undeclared instructed action found is a failed vetting>
- **Risk gate:** <the package's data and action classes, and the
  evidence docs/library.md's gate 4 requires for them>

A field *library* — the add library verb's object — gets its own
entry shape, one per library:

### Library <library-id> — <YYYY-MM-DD>

- **Maintainer:** <a named person or agent — not the library, not
  an org label>
- **Review practice:** <who reviews its modules, and how a review
  is recorded; "none" is a recordable answer, and a bad one>
- **Git repo URL:** <where the library's repository is cloned
  from>
- **Catalog URL:** <where its directory.json is fetched from —
  a separate field from the repo URL; the two are not assumed to
  be the same place>
- **Catalog pin:** <the directory's generated_from at vetting>
- **Advisories channel:** published (advisories.json present) /
  none (no advisories.json — the plan labels the library "no
  advisories channel")
- **Mechanical pass:** <the receipt line from
  tools/kit_selfcheck.py --field <library-id> run on the fetched
  checkout, or "no shell available" where it could not run>
- **Indexed:** unindexed (until the core index carries
  field-library entries, every added library is recorded
  unindexed)

## Entries

<!-- The first entry is the Muse Setup Kit itself. -->
