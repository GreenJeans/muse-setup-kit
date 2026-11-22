# Upgrading an existing install

An approval covers exactly one pin. It never covers an update — so an
upgrade is a small, deliberate procedure, not a `git pull`.

1. **Get the new pins from outside the repo.** An install records
   two pins per module (wizard Step 5 item 5), and an upgrade moves
   both. The release you want, named by its tag (or by the full
   commit hash from its release page). Check the checkout out at
   that tag or hash, resolve `git rev-parse HEAD`, and record the
   full hash as the new **checkout pin**; if the user supplied a
   hash, it must match exactly. The new **catalog pin** is the
   `generated_from` of the `directory.json` at that checkout.
   *(Evaluation installs — a dry run or rehearsal against unreleased
   changes — are the one exception: they may proceed from an
   uncommitted tree when the vetting entry records HEAD plus the
   dirty state — the output of `git status --porcelain` and
   `git diff --stat HEAD`, verbatim — and the plan is labeled
   EVALUATION. A production install never does.)*
2. **Diff the pins.** List what changed between your installed
   checkout pin and the new one (`git diff --stat <old>..<new>`),
   and read the changed files in full — at minimum every changed
   `MODULE.md`, `wizard/` file, and anything under a `tools/`
   folder. A module you did not install can be skimmed; a module
   you run gets read. (If the old install was itself an EVALUATION
   install from an uncommitted tree, the recorded HEAD is the diff
   base and the diff is approximate — the plan says so; the tree
   has moved since.)
3. **Write a fresh vetting entry** for the new pins: source, new hashes,
   files read, anything new the changed modules read, write, or
   contact. It lives in module 06's vetting log if that module is
   installed; otherwise it goes in `SETUP-PLAN.md` as the upgrade
   plan's first item. The old pin's entry does not carry over.
4. **Show the user an upgrade plan**: which installed files change,
   which stay untouched, which jobs change cadence or content, and any
   new disclosures. Local edits the user (or their agent) made to
   installed files are listed as conflicts and merged, never
   overwritten silently. The conflict list is mechanical where a
   baseline exists: run `kit_doctor.py` (it ships with module 05) —
   every "edited since install" line is a conflict to list. Without
   module 05, compare by hand: for each baseline line not marked
   `accumulating`, the file's `sha256sum` against its recorded hash;
   every mismatch is a conflict. (An install with no baseline falls
   back to comparing against the old pin's files by hand.)
   Approval names the new pins.
5. **Apply module by module**, in dependency order, re-running each
   changed module's `VERIFY.md` at-install checks as you go. A failed
   check stops the upgrade at that module; earlier modules stay
   upgraded, later ones stay on the old pin, and the plan records
   exactly that state. Where applying a module re-renders a file
   that hosts a registration anchor (the brief job file above all),
   every registered block in it is extracted first and re-inserted
   verbatim at the anchor, shown in the diff the user approved,
   before the file's baseline line is re-stamped — a re-render is
   never how another module's surfacing disappears (module 00's
   Registered blocks rule).
6. **Record the new pins** in `SETUP-PLAN.md` — the new checkout pin
   and the new catalog pin for each upgraded module (the old pins
   stay in the plan's history), re-stamp the baseline line of every
   file the upgrade rewrote or merged (new sha256, as it now stands
   — the baseline always describes the last approved state), and note
   the upgrade in the decision queue's resolved items or the vetting
   log.

Taking a single new module without a full upgrade works the same way,
scoped to that module: read it at the new checkout pin, vet it, plan it, and
record which pin each installed module came from — mixed pins are
normal, hidden mixed pins are not.
