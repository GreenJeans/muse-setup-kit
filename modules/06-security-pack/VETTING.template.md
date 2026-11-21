# Vetting Log

One entry per third-party skill, connector, or prompt pack considered.
Approval is per item, per pinned version, and never covers an update —
a version change means a new entry.

## Entry shape

### <ITEM NAME> — <YYYY-MM-DD>

- **Source:** <where it came from>
- **Pinned:** <version or commit hash>
- **Read in full at the pin:** yes / no / scoped — full for <scope>,
  <rest> not read (if no, stop — do not install; an unscoped "yes"
  for a partial read is a false record)
- **Reads:** <files, accounts, data it accesses>
- **Writes:** <what it creates or changes>
- **Network:** <endpoints it contacts>
- **Credentials:** <what it wants, and where they are stored>
- **Removal:** <how to uninstall it completely>
- **Decision:** install / install with recorded reservations (name
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
above with these (rules in `docs/library.md`). **Not applicable
until the library phase ships the package format: a package
without a `module.yaml` is vetted as a third-party skill pack
under the standard record, not under this block.**

- **Library / module:** <library-id>/<module-id>
- **module.yaml fields present:** <the fields docs/library.md
  requires, or what is missing>
- **Instructed action classes, declared vs found:** <send / file /
  spend / delete / contact — judged by effect, not file type; any
  undeclared instructed action found is a failed vetting>
- **Risk gate:** <the package's data and action classes, and the
  evidence docs/library.md's gate 4 requires for them>

## Entries

<!-- The first entry is the Muse Setup Kit itself. -->
