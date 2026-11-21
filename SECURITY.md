# Security

Some reports should not be public. This file names the
private route and what belongs on it.

## Report privately

- A credential, token, or personal data leaked in any file,
  issue, pull request, or listing connected to this
  repository, including in a listed field library.
- A scrub failure: real instance data (names, addresses,
  figures, transcripts) published where only patterns should
  be.
- A module, pattern, or listed library that sends data
  somewhere its declared reads and writes do not admit, or
  that instructs an agent to do so.
- Injection text planted in a module's or a catalog's fields:
  text written to be followed as an instruction by an agent,
  carried in a description, a pitch, or any field an installer
  would read as data.
- A defect in the kit's own tools (the linters, the
  selfcheck, the catalog generator) that makes a check pass
  when it should fail, or that leaks what a check read.

## The route

Use GitHub's private vulnerability reporting: the
repository's **Security** tab, "Report a vulnerability." The
report stays private between you and the maintainer.

If that route is unavailable to you, open a public issue that
says only that you need a private channel for a security
report. No details, no links to the problem, nothing that
points at it. The maintainer will open the channel.

## Never in a public issue

Credentials or tokens, anyone's personal data, anything that
identifies where leaked material sits — naming the repository
and the file is already a pointer — or working detail on how
a module exfiltrates data. Public
issues are public on arrival and are mirrored by feeds and
notification mail; a detail posted there cannot be taken
back.

If the leaked thing is a credential of yours, rotate it
first, before reporting. Do not wait for the maintainer.

## What the maintainer commits to

This project has one maintainer. Reports are read in arrival
order, and the aim is to acknowledge a private report within
three days. That is a target, not a service level; there is
no on-call and no bounty. A confirmed leak or exfiltration
report is handled before ordinary work: the entry or file is
pulled or the listing removed, and where people who already
installed something are affected, an advisory is published,
because a quiet fix does not reach an existing install.

For a field library, report to that library's maintainer as
well if you can. The core maintainer's part is the listing:
removal, recorded in the Removed section of
`docs/known-libraries.md` with the reason. Where the core
catalog or this page pointed at the problem, the core
maintainer asks the library's maintainer to publish the
advisory in the library's own advisories channel; core
advisories cover core modules only.
