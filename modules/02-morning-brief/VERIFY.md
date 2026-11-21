# Verify — Module 02: Morning Brief & Inbox Triage

Checks scope to what was installed: a brief-only install has no triage or
watch checks.

## At install

- [ ] The brief job exists — scheduler entry, or a job file at `jobs/morning-brief.md` plus its `JOBS.md` entry where the workspace is file-based — with the chosen time, timezone, and delivery,
      and is recorded in `JOBS.md`.
- [ ] The brief instructions name every source, mark conditional blocks
      `[IF ...]`, and contain the rule that an unread source is reported
      as unread — never as clear.
- [ ] If triage was installed: the VIP list and interrupt rules are
      filled in, and the delivery window matches the user's waking hours.

## Deferred

- [ ] **First brief** (due: first scheduled morning): arrives on time,
      failures section first, decision-queue items numbered.
- [ ] **Interrupt test** (due: first week; triage installs only): a test
      message from a VIP address with a direct question interrupts; a
      newsletter does not.
- [ ] **Detector-silence drill** (due: first month; only if watches
      exist): with the user's knowledge, pause one watch past 48 hours;
      the brief flags the silence.
