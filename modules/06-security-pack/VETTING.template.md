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

## Entries

<!-- The first entry is the Muse Setup Kit itself. -->
