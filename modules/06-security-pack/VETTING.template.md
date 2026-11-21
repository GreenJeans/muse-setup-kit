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
  against the official source — match, or the difference found>
- **OAuth scopes:** <each scope requested, and the feature it maps to;
  "none" for a local-only item>
- **Tool-manifest hash:** <sha256 of the named manifest artifact: the
  vendor-published manifest file (name it), or the tool list exactly
  as presented at first connection, saved verbatim as the artifact;
  a vendor-stated hash with no artifact behind it is recorded as
  "vendor-stated, unverifiable"; MCP servers only>
- **Re-vet trigger:** any version change; any scope increase; any
  tool-manifest hash change

Field modules (kit-library packages) replace the connector fields
above with these (rules in `docs/library.md`):

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
