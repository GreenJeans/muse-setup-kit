# Skill Queue Items — Template

Add the header definitions to your decision queue when module 08
installs, then use the two item shapes below. Both extend the queue's
normal item shape (module 00); numbering is the queue's own and is
never reused.

## Header definitions (add to the queue file, near the top)

> Skill items carry a type tag. `[type: skill-write]` is a staged
> skill change from the module 08 review pass; `[type: skill-curator]`
> is a stale/archive proposal from the module 08 curator. For both
> types, silence is NEVER consent: an undecided item's only default is
> to stay staged, and staging expires (auto-reject, logged) after 14
> days. "N: approve" authorizes exactly the staged diff or move, one
> application, and is void if the target has changed since staging.
> "N: edit: <change>" voids the item; the agent restages as a new
> numbered item.

## Item shape — skill-write

```text
N. **Skill write (staged) — <patch | support file | create> `<skill-name>`** [type: skill-write]
   Signal: <user correction | verified fix | stale skill>, <YYYY-MM-DD>,
   <chat/session> — "<short verbatim quote>" (full evidence in
   staged/N-<skill-name>/proposal.md).
   Change: +<n>/−<m> lines in <file> — <what the diff does, one line>.
   Full diff: staged/N-<skill-name>/diff.patch.
   Base hash: matches the live file as of staging (sha256 <short hash>).
   Void if the target changes before approval.
   Risk if wrong: <one line>. Reversible by <how>.
   Default if no reply: stays staged, nothing applied. Resurface
   <YYYY-MM-DD>; staging expires after 14 days undecided.
   Smallest ask: "N: approve" / "N: reject" / "N: edit: <change>".
```

Escalation note: a proposal that adds a script, any network call, any
credential use, or a new skill rather than a patch does **not** use
this shape — it leaves the queue path and needs a verify-before-install
record (module 06) plus an explicit ticket.

## Item shape — skill-curator (batched)

```text
N. **Skill curator — <k> candidate(s)** [type: skill-curator]
   - `<skill-name>`: <stale | archive candidate> — last activity
     <YYYY-MM-DD> (<source: view | use | patch, from the ledger>);
     exemptions checked: none apply. Approval authorizes the move
     <skills-dir>/<skill-name>/ → <skills-dir>/.archive/<skill-name>/
     (archive candidates only; stale candidates change nothing but
     their ledger state). Restore: move back + ledger update.
   - <repeat per candidate>
   Each candidate is individually approvable: "N: approve <skill-name>
   only" applies to that skill alone.
   Default if no reply: nothing moves. Stale lines resurface in the
   next curator item; archive candidates expire with this item after
   14 days and may be re-proposed by a later run.
   Smallest ask: "N: approve <skill-name>" / "N: approve all" /
   "N: reject".
```
