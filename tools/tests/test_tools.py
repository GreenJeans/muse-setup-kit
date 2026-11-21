#!/usr/bin/env python3
"""Regression fixtures for the kit's shipped tools (stdlib unittest).

Every fixture here encodes a bug the kit's review rounds actually
found, so the fix cannot silently regress:

  - the memory linter flagging a textbook install (INDEX.md files,
    its own report) and bolded JOBS.md entries;
  - the linter's review-by check (check D) flagging a claim whose
    review-by date has passed — the check the schema template always
    claimed and the code did not have until v0.8;
  - the curator's substring exemptions, dateless-record immortality,
    dead grace floor, and job-name matching (tax-docs vs
    tax-docs-prep);
  - stage_check expiry and the shadow-folder exemption;
  - kit_doctor going blind on mixed pins and missing overdue
    deferred checks.

Run: python3 -m unittest discover -s tools/tests
"""
import datetime
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LINT = os.path.join(REPO, "modules/01-memory-architecture/tools/memory_lint.py")
CURATOR = os.path.join(REPO, "modules/08-skill-lifecycle/tools/curator.py")
STAGE = os.path.join(REPO, "modules/08-skill-lifecycle/tools/stage_check.py")
DOCTOR = os.path.join(REPO, "modules/05-evaluation-kit/tools/kit_doctor.py")
TODAY = datetime.date.today()


def run(script, *argv, cwd=None):
    return subprocess.run([sys.executable, script, *argv],
                          capture_output=True, text=True, cwd=cwd)


def days_ago(n):
    return str(TODAY - datetime.timedelta(days=n))


class LinterTest(unittest.TestCase):
    def test_textbook_install_lints_quiet(self):
        with tempfile.TemporaryDirectory() as td:
            mem = os.path.join(td, "memory")
            os.makedirs(mem)
            with open(os.path.join(mem, "SCHEMA.md"), "w") as fh:
                fh.write("<!-- schema_version: 1.1 | last_verified: 2026-11-20 -->\n# Schema\n\n## Current state\n- One fact.\n")
            with open(os.path.join(mem, "INDEX.md"), "w") as fh:
                fh.write("# Index\n- [One](one.md) — plain current-state fact, no history.\n")
            with open(os.path.join(mem, "one.md"), "w") as fh:
                fh.write("<!-- schema_version: 1.1 | last_verified: 2026-11-20 -->\n# One\n\n## Facts\n- A current fact.\n")
            jobs = os.path.join(td, "JOBS.md")
            with open(jobs, "w") as fh:
                fh.write("- **memory-lint** — weekly\n- morning-brief — daily\n")
            proc = os.path.join(td, "OPERATING_PROCEDURES.md")
            with open(proc, "w") as fh:
                fh.write("Jobs: the `memory-lint` job and the `morning-brief` job.\n")
            r = run(LINT, "--memory-dir", mem, "--procedures", proc,
                    "--jobs", jobs, "--report", os.path.join(td, "r.md"))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("No findings", r.stdout)

    def test_review_by_check_flags_only_passed_dates(self):
        with tempfile.TemporaryDirectory() as td:
            mem = os.path.join(td, "memory")
            os.makedirs(mem)
            past = days_ago(30)
            future = str(TODAY + datetime.timedelta(days=30))
            with open(os.path.join(mem, "one.md"), "w") as fh:
                fh.write("<!-- schema_version: 1.1 | last_verified: 2026-11-20 -->\n"
                         "# One\n\n## Facts\n"
                         f"- A settled claim (review-by: {past}).\n"
                         f"- A live claim (review-by: {future}).\n"
                         "- A claim with a broken date (review-by: soon).\n")
            jobs = os.path.join(td, "JOBS.md")
            with open(jobs, "w") as fh:
                fh.write("- morning-brief — daily\n")
            proc = os.path.join(td, "OPERATING_PROCEDURES.md")
            with open(proc, "w") as fh:
                fh.write("# Procedures\n")
            r = run(LINT, "--memory-dir", mem, "--procedures", proc,
                    "--jobs", jobs, "--report", os.path.join(td, "r.md"))
            # D findings are medium severity: reported, exit stays 0.
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("checks=A,B,C,D", r.stdout)
            self.assertIn(f"D: ", r.stdout)
            self.assertIn(f"review-by {past} has passed", r.stdout)
            self.assertIn("unparseable review-by date 'soon'", r.stdout)
            self.assertNotIn(f"review-by {future} has passed", r.stdout)


class CuratorTest(unittest.TestCase):
    def _setup(self, td, records):
        skills = os.path.join(td, "skills")
        for name in records:
            os.makedirs(os.path.join(skills, name))
            with open(os.path.join(skills, name, "SKILL.md"), "w") as fh:
                fh.write(f"# {name}\n")
        ledger = os.path.join(td, "ledger.json")
        with open(ledger, "w") as fh:
            json.dump({"version": 1, "skills": records}, fh)
        jobs = os.path.join(td, "JOBS.md")
        with open(jobs, "w") as fh:
            fh.write("- `tax-docs-prep` — weekly; owes a summary\n")
        return skills, ledger, jobs

    def _rec(self, created):
        return {"created": created, "pinned": False, "last_viewed": None,
                "last_used": None, "last_patched": None, "views": 0,
                "uses": 0, "patches": 0, "exemptions": [], "state": "active"}

    def test_job_name_matching_is_not_substring(self):
        with tempfile.TemporaryDirectory() as td:
            records = {"tax": self._rec(days_ago(50)),
                       "tax-docs": self._rec(days_ago(50))}
            skills, ledger, jobs = self._setup(td, records)
            r = run(CURATOR, "--skills-dir", skills, "--ledger", ledger,
                    "--jobs-file", jobs)
            self.assertEqual(r.returncode, 0, r.stderr)
            rep = json.loads(r.stdout)
            self.assertIn("job-ref", rep["skills"]["tax-docs"]["exemptions"])
            self.assertEqual(rep["skills"]["tax"]["state"], "archive-candidate")

    def test_first_run_empty_ledger_longest_match(self):
        # Regression: the matcher once received the ledger-so-far as
        # its name list, so on a first run `tax` (alphabetically
        # before `tax-docs`) wrongly claimed the tax-docs-prep job.
        with tempfile.TemporaryDirectory() as td:
            skills, ledger, jobs = self._setup(td, {})
            for name in ("tax", "tax-docs"):
                os.makedirs(os.path.join(skills, name), exist_ok=True)
                with open(os.path.join(skills, name, "SKILL.md"), "w") as fh:
                    fh.write(f"# {name}\n")
            r = run(CURATOR, "--skills-dir", skills, "--ledger", ledger,
                    "--jobs-file", jobs)
            self.assertEqual(r.returncode, 0, r.stderr)
            rep = json.loads(r.stdout)
            self.assertIn("job-ref", rep["skills"]["tax-docs"]["exemptions"])
            self.assertNotIn("job-ref", rep["skills"]["tax"]["exemptions"])

    def test_dateless_record_anchors_to_seed_not_zero(self):
        with tempfile.TemporaryDirectory() as td:
            records = {"old-skill": self._rec(None)}
            skills, ledger, jobs = self._setup(td, records)
            r = run(CURATOR, "--skills-dir", skills, "--ledger", ledger,
                    "--jobs-file", jobs)
            rep = json.loads(r.stdout)
            self.assertIn("old-skill", rep["unseeded"])
            self.assertNotEqual(rep["skills"]["old-skill"]["state"],
                                "archive-candidate")

    def test_grace_floor_keeps_young_unused_skill(self):
        with tempfile.TemporaryDirectory() as td:
            records = {"young-skill": self._rec(days_ago(20))}
            skills, ledger, jobs = self._setup(td, records)
            r = run(CURATOR, "--skills-dir", skills, "--ledger", ledger,
                    "--jobs-file", jobs)
            rep = json.loads(r.stdout)
            self.assertEqual(rep["skills"]["young-skill"]["state"], "stale")


class StageCheckTest(unittest.TestCase):
    def test_expiry_and_shadow_exemption(self):
        with tempfile.TemporaryDirectory() as td:
            staged = os.path.join(td, "staged")
            for name, staged_line in [("3-old-skill", days_ago(20)),
                                      ("shadow-1-x", days_ago(20))]:
                d = os.path.join(staged, name)
                os.makedirs(d)
                with open(os.path.join(d, "proposal.md"), "w") as fh:
                    fh.write(f"# Proposal\n\nStaged: {staged_line}\n")
            r = run(STAGE, "--staged-dir", staged, "--json")
            rep = json.loads(r.stdout)
            self.assertEqual(len(rep["expired"]), 1)
            r = run(STAGE, "--staged-dir", staged, "--apply")
            self.assertTrue(os.path.isdir(
                os.path.join(staged, "expired", "3-old-skill")))
            self.assertTrue(os.path.isdir(os.path.join(staged, "shadow-1-x")))


class KitDoctorTest(unittest.TestCase):
    def test_mixed_pins_are_listed_not_blind(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
                fh.write("# Plan\n- module core-procedures — commit aaaaaaa1111\n"
                         "- module skill-lifecycle — commit bbbbbbb2222\n"
                         "- [ ] Something DEFERRED due 2020-01-01\n")
            with open(os.path.join(td, "JOBS.md"), "w") as fh:
                fh.write("# Jobs\n")
            with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
                fh.write("# Procedures\n")
            r = run(DOCTOR, "--workspace", td, "--json")
            rep = json.loads(r.stdout)
            notes = " ".join(rep["notes"])
            self.assertIn("aaaaaaa1111", notes)
            self.assertIn("bbbbbbb2222", notes)
            self.assertTrue(any("overdue" in p for p in rep["problems"]))

    def _doctor_workspace(self, td, plan):
        with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
            fh.write(plan)
        with open(os.path.join(td, "JOBS.md"), "w") as fh:
            fh.write("# Jobs\n")
        with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
            fh.write("# Procedures\n")
        return json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)

    def test_due_field_governs_the_deferred_row(self):
        with tempfile.TemporaryDirectory() as td:
            # A status-cell date in the past must not make the row
            # overdue when the explicit due: field is in the future.
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "- [ ] Money-watch first run DEFERRED due: 2099-01-01"
                    " — PART DONE 2020-01-01\n")
            self.assertFalse(any("overdue" in p for p in rep["problems"]))
            # And a past due: field governs even beside a future date.
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "- [ ] Money-watch first run DEFERRED due: 2020-01-01"
                    " — rescheduled from 2099-01-01\n")
            self.assertTrue(any("overdue" in p for p in rep["problems"]))

    def test_labeled_pin_beats_a_disclaimed_hash(self):
        with tempfile.TemporaryDirectory() as td:
            real, fake = "a" * 40, "b" * 40
            rep = self._doctor_workspace(
                td, f"# Plan\n- install pin: {real}\n"
                    f"- note: the hash {fake} was NOT used as the pin;"
                    " it is an ancestor repo's HEAD\n")
            notes = " ".join(rep["notes"])
            self.assertIn(real, notes)
            self.assertNotIn(fake, notes)
            self.assertNotIn("mixed pins", notes)

    def test_baseline_reports_edits_and_missing(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            keep = os.path.join(td, "keep.md")
            with open(keep, "w") as fh:
                fh.write("original\n")
            keep_hash = hashlib.sha256(b"original\n").hexdigest()
            gone_hash = hashlib.sha256(b"gone\n").hexdigest()
            with open(os.path.join(td, "gone.md"), "w") as fh:
                fh.write("gone\n")
            with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
                fh.write("# Plan\n- install — commit aaaaaaa1111\n"
                         "## Installed files (baseline)\n"
                         f"- installed: keep.md sha256:{keep_hash}\n"
                         f"- installed: gone.md sha256:{gone_hash}\n")
            with open(os.path.join(td, "JOBS.md"), "w") as fh:
                fh.write("# Jobs\n")
            with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
                fh.write("# Procedures\n")
            # clean state: no edit note, no missing problem
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertFalse(any("edited since install" in n
                                 for n in rep["notes"]))
            self.assertFalse(any("baselined file missing" in p
                                 for p in rep["problems"]))
            # edit keep.md -> note; delete gone.md -> problem
            with open(keep, "w") as fh:
                fh.write("edited\n")
            os.remove(os.path.join(td, "gone.md"))
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertTrue(any("edited since install: keep.md" in n
                                for n in rep["notes"]))
            self.assertTrue(any("baselined file missing: gone.md" in p
                                for p in rep["problems"]))

    def test_accumulating_files_are_inventoried_not_diffed(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            q = os.path.join(td, "queue.md")
            with open(q, "w") as fh:
                fh.write("item 1\n")
            with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
                fh.write("# Plan\n- install — commit aaaaaaa1111\n"
                         "## Installed files (baseline)\n"
                         "- installed: queue.md accumulating\n")
            with open(os.path.join(td, "JOBS.md"), "w") as fh:
                fh.write("# Jobs\n")
            with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
                fh.write("# Procedures\n")
            with open(q, "w") as fh:
                fh.write("item 1\nitem 2\nitem 3\n")
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertFalse(any("edited since install" in n
                                 for n in rep["notes"]))
            self.assertTrue(any("1 hashed, 0 accumulating" not in n and
                                "accumulating" in n for n in rep["notes"]))

if __name__ == "__main__":
    unittest.main()
