# Uninstalling the kit

Everything the kit installs is a file or a named job, so everything
it installs can be removed. Uninstalling is a ticket-shaped action:
the agent shows the full removal list first, the user approves it,
and the agent verifies the result. Nothing here is a background
operation.

## Principles

- **Your content is yours.** Memory pages, briefs, queue history,
  and anything you or the agent authored are content, not kit
  machinery. Before removing anything, the agent offers to export
  or archive them somewhere you name. The kit's files go; your
  words stay as long as you want them.
- **Shares are revoked at the source, and verified there.** A
  shared folder or doc is not uninstalled until its sharing state
  is changed at the provider and re-read to confirm.
- **Jobs stop before files move.** A scheduled job pointing at
  removed files will fail noisily; remove the jobs first.

## The removal list comes from the install's own records

1. `SETUP-PLAN.md` — what was installed, from which pins, and the
   **installed-file baseline**: every file the wizard created or
   copied from the kit. That list is the removal manifest. A
   hash-baselined file whose hash no longer matches was edited
   since install — it is listed separately, and removing it needs
   an explicit yes per file, because it now holds local work.
   Files baselined as `accumulating` (the queue, `JOBS.md`,
   ledgers) are content by design: the export offer applies to
   them, and removing them needs the same explicit yes.
2. `JOBS.md` — every scheduled job to remove, by name.
3. The plan's module list — per-module leftovers (below).

An install old enough to have no baseline falls back to the plan's
module list plus each module's template names, and the agent says
plainly that the manifest is reconstructed, not recorded.

## Steps

1. **Inventory.** Build the removal list from the records above:
   jobs, baselined files (unchanged vs edited), module leftovers,
   shares to revoke. Show it to the user in full. Approval covers
   exactly this list.
2. **Export offer.** Name where content files (memory, briefs,
   queue, staged proposals) go if the user wants them kept — an
   archive folder outside the workspace is the default suggestion.
3. **Stop the jobs.** Remove every job in `JOBS.md` from the
   scheduler, then remove `JOBS.md` itself. (`JOBS.md` is removed
   here, with the jobs — it does not also appear as a step-5 file,
   though the baseline lists it for inventory.)
4. **Revoke shares at the source.** Per module: household HQ
   surfaces (module 03) return to single-owner or are transferred
   to the partner, per the user's choice; AI Exchange folders
   (module 04) are unshared with the other agents' accounts.
   Re-read each surface's sharing state to confirm.
5. **Remove the files.** Baselined files whose hashes still match
   are deleted. Edited files are deleted only where the approval
   named them; the rest are listed in the close-out as kept.
   Module leftovers: module 08's `staged/` (undecided proposals
   expire with the module — list them in the close-out), its
   `.archive/` of retired skills (content — export offer applies),
   and module 05's vetting log (content — export offer applies).
6. **Close out.** Remove `SETUP-PLAN.md` last, after printing a
   summary: jobs removed, files removed, files kept and why,
   shares revoked and verified. The summary is the record; keep it
   wherever the user keeps such things.

## Verify

- [ ] The scheduler holds no job the kit created (checked at the
      scheduler, not from `JOBS.md`, which is gone). In a
      file-based workspace the job files plus `JOBS.md` ARE the
      scheduler-of-record; there, their absence is the evidence.
- [ ] Every surface the kit shared reads back as unshared or
      transferred.
- [ ] The workspace contains no baselined file the approval said
      to remove.
- [ ] The close-out summary exists and lists anything kept, with
      the reason.
