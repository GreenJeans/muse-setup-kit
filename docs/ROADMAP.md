# Roadmap

## Phase 1 — scaffold (this commit)

- Repo skeleton, README, design notes.
- Wizard skill + module manifest.
- Modules 00–04 distilled with templates; 05–07 as full method outlines.
- Scrub pass: no instance data anywhere (grep-verified against a denylist
  kept *outside* this repo).

## Phase 2 — hardening

- Dry run: execute the wizard in a fresh session with no memory loaded and
  confirm it produces a coherent setup from zero. Fix what it trips on.
- Fill remaining template gaps found by the dry run.
- Add a `VERIFY.md` per module: the checks an installer runs to prove the
  module works (the kit's own "done means verified" rule, applied to itself).

## Phase 3 — publication (separate decision)

- Final scrub + license review.
- Publish as a public git repository; tag v0.1.0.
- Optional: submit the wizard to community skill directories, following the
  kit's own verify-before-install discipline in reverse — publish the pinned
  commit hash alongside any listing.

## Ideas parking lot

- A "diff my setup" tool: compare an existing installation against the kit
  and report which patterns are present, missing, or drifted.
- Worked example (fully fictional) of a filled-in memory store and brief, so
  adopters can see the target state without any real data.
- Localization of the templates.
