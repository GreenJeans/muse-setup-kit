# Infra Patterns (reference — not an installable module)

Patterns for users with a host they control (home server, VPS),
distilled from the maintainer's working setup. The theme is the
same as the rest of the kit: a backup that isn't verified is a
rumor, and a monitor that can fail silently will.

**Why this is a document and not a module.** Through v0.3 this
shipped as module 07. It was demoted in v0.4 for three reasons: it
was never rehearsed as an install (both wizard dry runs withheld
it, and host work is slow, host-specific, and partly irreversible —
storage choices, retention, offsite credentials — in a way a
sandbox rehearsal cannot exercise cheaply); it is the least
Muse-specific material in the kit; and its genuinely kit-specific
kernel — watches that write run records, flag failed runs, and make
their own silence detectable — already lives in module 02's Watches
pattern. What remains here is sound ops practice, kept where a
reader can use it without the wizard taxing every install for it.

## Layered backups

1. **Image layer.** Nightly snapshots/images of every guest or
   service that would hurt to rebuild, with short retention
   (keep-last 2 is plenty) — and a storage location that is *not*
   the disk whose failure you're protecting against. Check the
   free-space math after every change: retention × image size vs.
   target capacity.
2. **File layer.** An encrypted, versioned backup (e.g. restic) of
   system state and configuration, nightly, with retention tiers
   (daily 7 / weekly 4 / monthly 6) and a weekly prune.
3. **Offsite layer.** The file layer mirrored to object storage
   nightly. Media collections are a deliberate, stated exclusion —
   or not; but state the choice, don't drift into it.
4. **Verification.** A scheduled verify pass that test-reads the
   newest archive per guest (integrity check + completion log),
   checks ages against a staleness threshold, and reports
   PROBLEMS-FOUND or OK. A backup system whose verify hasn't run is
   flagged exactly like a failed backup. Test restores: at least
   once at setup, from *each* layer, byte-compared.

## Health watches

- A lightweight host watch (every 30 minutes): disk thresholds,
  service liveness, backup freshness — writing a run record every
  time, alerting only on exceptions, at most one alert per issue
  per day. (This is module 02's watch pattern pointed at a host.)
- A disk tripwire a few points *below* the level where backups
  start failing, so the first alert arrives while there's still
  room to act.
- Root-cause discipline: when a disk fills during a backup window,
  the backup may not be the only writer. Log sizes in the window
  before concluding.

## Alerts that reach a human

- Route alerts to a phone notification channel the user actually
  sees (a self-hosted push service works well), with priority
  discipline: the highest priority is reserved for true emergencies,
  or the user learns to ignore the channel — and then it isn't one.
- Uptime monitoring watches the services; a dead-man's-switch
  service watches the jobs (a job that stops checking in pages
  exactly like a job that failed).

## If you adopt these

Work them as their own project, under the kit's normal rules:
inventory hosts and guests with the user (every guest, or
rebuildable ones excluded — a stated choice); stand up the layers
in order and run test restores before declaring any layer live;
record the layout — locations, retention, exclusions, restore
steps — where a future session (or a future human) can find it.
Standing up backup infrastructure is exactly the kind of
partly-irreversible work the ticket rule exists for.
