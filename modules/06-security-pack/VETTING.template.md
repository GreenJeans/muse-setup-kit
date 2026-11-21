# Vetting Log

One entry per third-party skill, connector, or prompt pack considered.
Approval is per item, per pinned version, and never covers an update —
a version change means a new entry.

## Entry shape

### <ITEM NAME> — <YYYY-MM-DD>

- **Source:** <where it came from>
- **Pinned:** <version or commit hash>
- **Read in full at the pin:** yes / no (if no, stop — do not install)
- **Reads:** <files, accounts, data it accesses>
- **Writes:** <what it creates or changes>
- **Network:** <endpoints it contacts>
- **Credentials:** <what it wants, and where they are stored>
- **Removal:** <how to uninstall it completely>
- **Decision:** install / cherry-pick (parts taken as patterns, rewritten
  locally) / reject
- **Why:** <one or two lines>

Connectors and MCP servers add these fields (module 06's vetting pack):

- **Provenance tier:** official / community / unknown
- **Typosquat check:** <name and source compared character-by-character
  against the official source — match, or the difference found>
- **OAuth scopes:** <each scope requested, and the feature it maps to;
  "none" for a local-only item>
- **Tool-manifest hash:** <sha256 of the tool names and descriptions, in
  order, as presented at vetting; MCP servers only>
- **Re-vet trigger:** any version change; any scope increase; any
  tool-manifest hash change

## Entries

<!-- The first entry is the Muse Setup Kit itself. -->
