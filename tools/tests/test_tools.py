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
  - kit_doctor going blind on mixed pins, missing overdue
    deferred checks, and deleted accumulating files (run 15: a
    deleted service log passed the doctor without a word);
  - the EX-024/025 verification round's residuals: advisory
    module ids that resolve to nothing, the doctor offering
    repairs the wizard refuses, symlink escapes from declared
    paths, catalog staleness the regenerate-and-diff check
    cannot see, and the parser's last uncaught spellings
    (YAML 1.1 booleans, a block-list item that is a list,
    negated class prose);
  - module 11's soul linter and registration: a filled soul
    file lints quiet, the shipped template (all slots) never
    lints clean, inherited boilerplate is a warning and never
    a finding, and the module is registered in the catalog,
    the matrix, and the README while staying out of the
    profiles until the maintainer's merge call.

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

    def test_baseline_class_tokens_are_accepted(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            tool = os.path.join(td, "tool.py")
            with open(tool, "w") as fh:
                fh.write("tool\n")
            h = hashlib.sha256(b"tool\n").hexdigest()
            with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
                fh.write("# Plan\n- install — commit aaaaaaa1111\n"
                         "## Installed files (baseline)\n"
                         f"- installed: tool.py sha256:{h} static-verbatim\n")
            with open(os.path.join(td, "JOBS.md"), "w") as fh:
                fh.write("# Jobs\n")
            with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
                fh.write("# Procedures\n")
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertTrue(any("1 hashed, 0 accumulating" in n
                                for n in rep["notes"]))
            self.assertFalse(any("edited since install" in n
                                 for n in rep["notes"]))
            with open(tool, "w") as fh:
                fh.write("tampered\n")
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertTrue(any("edited since install: tool.py" in n
                                for n in rep["notes"]))

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

    def test_missing_accumulating_file_is_noted_not_a_problem(self):
        # Run 15 friction: deleting an accumulating file (a service
        # log) produced no doctor output at all, while a missing
        # hashed file was a PROBLEM. Absence is noted, never diffed,
        # and not a problem.
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "SETUP-PLAN.md"), "w") as fh:
                fh.write("# Plan\n- install — commit aaaaaaa1111\n"
                         "## Installed files (baseline)\n"
                         "- installed: queue.md accumulating\n")
            with open(os.path.join(td, "JOBS.md"), "w") as fh:
                fh.write("# Jobs\n")
            with open(os.path.join(td, "OPERATING_PROCEDURES.md"), "w") as fh:
                fh.write("# Procedures\n")
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertTrue(any("accumulating file missing" in n and
                                "queue.md" in n for n in rep["notes"]))
            self.assertFalse(any("queue.md" in p for p in rep["problems"]))
            # And a present accumulating file draws no such note.
            with open(os.path.join(td, "queue.md"), "w") as fh:
                fh.write("item 1\n")
            rep = json.loads(run(DOCTOR, "--workspace", td, "--json").stdout)
            self.assertFalse(any("accumulating file missing" in n
                                 for n in rep["notes"]))

    def test_recorded_removal_is_a_note_not_a_problem(self):
        # EX-022/023: a file the user deleted on purpose, recorded
        # with a "- removed:" line, must not be reported as damage
        # forever — and repair must never resurrect it.
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            h = hashlib.sha256(b"gone\n").hexdigest()
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "## Installed files (baseline)\n"
                    f"- installed: gone.md sha256:{h} static-rendered"
                    " core/example\n"
                    "- removed: gone.md 2026-11-01 user deleted it"
                    " on purpose\n")
            self.assertFalse(any("gone.md" in p
                                 for p in rep["problems"]))
            self.assertTrue(any("recorded removal" in n and
                                "gone.md" in n for n in rep["notes"]))

    def test_missing_static_verbatim_offers_repair_or_removal(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            h = hashlib.sha256(b"tool\n").hexdigest()
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "## Installed files (baseline)\n"
                    f"- installed: tool.py sha256:{h} static-verbatim"
                    " core/example from:core/example:tools/tool.py\n")
            self.assertTrue(any("repair, or record the removal" in p
                                for p in rep["problems"]))

    def test_missing_static_verbatim_without_source_offers_no_repair(self):
        # EX-024/025 (R11): a legacy static-verbatim line with no
        # from: token is not repairable — the wizard's repair
        # reads the source from that token and refuses without
        # it. The doctor must not offer a repair that will abort.
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            h = hashlib.sha256(b"tool\n").hexdigest()
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "## Installed files (baseline)\n"
                    f"- installed: tool.py sha256:{h} static-verbatim"
                    " core/example\n")
            self.assertTrue(any("not repairable" in p
                                for p in rep["problems"]))
            self.assertFalse(any("repair, or record the removal" in p
                                 for p in rep["problems"]))

    def test_two_modules_claiming_one_path_is_a_problem(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "shared.md"), "w") as fh:
                fh.write("shared\n")
            h = hashlib.sha256(b"shared\n").hexdigest()
            rep = self._doctor_workspace(
                td, "# Plan\n- install — commit aaaaaaa1111\n"
                    "## Installed files (baseline)\n"
                    f"- installed: shared.md sha256:{h}"
                    " static-rendered core/one\n"
                    f"- installed: shared.md sha256:{h}"
                    " static-rendered core/two\n")
            self.assertTrue(any("claimed by two modules" in p
                                for p in rep["problems"]))


MODULE_YAML = os.path.join(REPO, "tools", "module_yaml.py")
BUILD_DIR = os.path.join(REPO, "tools", "build_directory.py")
SELFCHECK = os.path.join(REPO, "tools", "kit_selfcheck.py")

MODULE_FIXTURE = (
    'id: {mid}\n'
    'dir: modules/{folder}\n'
    'title: Example\n'
    'pitch: "A pitch."\n'
    'version: "0.1"\n'
    'maintainer: A Person\n'
    'license: MIT\n'
    'kit_compat: [kit-1]\n'
    'depends_on: []\n'
    'requires: []\n'
    'degrades_without: []\n'
    'reads: "the files."\n'
    'writes: "a register."\n'
    'network: "none."\n'
    'jobs: "none."\n'
    'rehearsed_at: null\n'
    'data_classes: [personal]\n'
    'action_classes: [none]\n'
    'files: []\n')


def git(repo, *argv):
    return subprocess.run(["git", "-C", repo] + list(argv),
                          capture_output=True, text=True)


def make_repo(td, modules):
    """A git repo holding the given (folder, module-id) modules."""
    os.makedirs(os.path.join(td, "modules"))
    for folder, mid in modules:
        mdir = os.path.join(td, "modules", folder)
        os.makedirs(mdir)
        with open(os.path.join(mdir, "module.yaml"), "w") as fh:
            fh.write(MODULE_FIXTURE.format(mid=mid, folder=folder))
    git(td, "init", "-q")
    git(td, "config", "user.email", "t@example.com")
    git(td, "config", "user.name", "Test")
    git(td, "add", "-A")
    git(td, "commit", "-qm", "fixture")
    return td


class BuildDirectoryTest(unittest.TestCase):
    def test_clean_tree_generates_and_stamps_head(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 0, r.stderr)
            doc = json.load(open(os.path.join(td, "directory.json")))
            head = git(td, "rev-parse", "HEAD").stdout.strip()
            self.assertEqual(doc["generated_from"], head)
            self.assertNotIn("reviewed_at", doc["modules"][0])

    def test_dirty_tree_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            with open(os.path.join(td, "modules", "example",
                                   "module.yaml"), "a") as fh:
                fh.write("# a note\n")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("dirty", r.stderr)

    def test_no_git_fails_instead_of_a_null_pin(self):
        with tempfile.TemporaryDirectory() as td:
            mdir = os.path.join(td, "modules", "example")
            os.makedirs(mdir)
            with open(os.path.join(mdir, "module.yaml"), "w") as fh:
                fh.write(MODULE_FIXTURE.format(mid="core/example",
                                               folder="example"))
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertFalse(os.path.exists(
                os.path.join(td, "directory.json")))

    def test_review_fields_and_unknown_keys_stop_generation(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            p = os.path.join(td, "modules", "example", "module.yaml")
            with open(p, "a") as fh:
                fh.write("reviewed_by: A Person\n")
            git(td, "add", "-A")
            git(td, "commit", "-qm", "add review field")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("allowlist", r.stderr)

    def test_namespace_and_duplicate_ids_are_enforced(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "other/example")])
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("namespace", r.stderr)
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("one", "core/example"),
                           ("two", "core/example")])
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("duplicate", r.stderr)

    def test_absent_advisories_source_means_no_file(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            stale = os.path.join(td, "advisories.json")
            with open(stale, "w") as fh:
                fh.write("{}\n")
            git(td, "add", "-A")
            git(td, "commit", "-qm", "stale fabricated advisories")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertFalse(os.path.exists(stale))

    def test_advisories_validate(self):
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            with open(os.path.join(td, "advisories.yaml"), "w") as fh:
                fh.write("advisories:\n"
                         "  - id: ADV-2026-001\n"
                         "    module: core/example\n"
                         "    pin: all\n"
                         "    date: 2026-11-21\n"
                         "    reason: a bad pin shipped\n"
                         "    remedy: suspend core/example\n")
            git(td, "add", "-A")
            git(td, "commit", "-qm", "advisories")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 0, r.stderr)
            doc = json.load(open(os.path.join(td, "advisories.json")))
            self.assertEqual(len(doc["advisories"]), 1)
            with open(os.path.join(td, "advisories.yaml"), "w") as fh:
                fh.write("advisories:\n"
                         "  - id: ADV-2026-001\n"
                         "    module: core/example\n"
                         "    pin: shortpin\n"
                         "    date: 2026-11-21\n"
                         "    reason: a bad pin shipped\n"
                         "    remedy: suspend core/example\n")
            git(td, "add", "-A")
            git(td, "commit", "-qm", "bad advisory")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)

    def _advisory_repo(self, td, module_field):
        make_repo(td, [("example", "core/example")])
        with open(os.path.join(td, "advisories.yaml"), "w") as fh:
            fh.write("advisories:\n"
                     "  - id: ADV-2026-001\n"
                     f"    module: {module_field}\n"
                     "    pin: all\n"
                     "    date: 2026-11-21\n"
                     "    reason: a bad pin shipped\n"
                     "    remedy: suspend it\n")
        git(td, "add", "-A")
        git(td, "commit", "-qm", "advisories")

    def test_advisory_module_must_resolve(self):
        # EX-024/025 (R3): resolvability used to be void for any
        # id containing "/" — a typoed own-library advisory
        # (core/exampl) passed validation and would never match
        # an installed module at audit. Only the library itself
        # or a module this catalog carries resolves.
        with tempfile.TemporaryDirectory() as td:
            self._advisory_repo(td, "core/exampl")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("does not resolve", r.stderr)
        with tempfile.TemporaryDirectory() as td:
            self._advisory_repo(td, "bogus/example")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("does not resolve", r.stderr)
        with tempfile.TemporaryDirectory() as td:
            self._advisory_repo(td, "core")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 0, r.stderr)
            doc = json.load(open(os.path.join(td, "advisories.json")))
            self.assertEqual(len(doc["advisories"]), 1)

    def test_pitch_cap_is_enforced(self):
        # Fix item 26's missing fixture: catalog text is
        # length-capped, and the generator is where it bites.
        with tempfile.TemporaryDirectory() as td:
            make_repo(td, [("example", "core/example")])
            p = os.path.join(td, "modules", "example", "module.yaml")
            text = open(p).read().replace(
                'pitch: "A pitch."', 'pitch: "' + "x" * 401 + '"')
            with open(p, "w") as fh:
                fh.write(text)
            git(td, "add", "-A")
            git(td, "commit", "-qm", "long pitch")
            r = run(BUILD_DIR, "--repo", td, "--library", "core")
            self.assertEqual(r.returncode, 1)
            self.assertIn("capped", r.stderr)


class SelfcheckFieldTest(unittest.TestCase):
    def _field_repo(self, td, extra_yaml="", files_line="files: []\n"):
        mdir = os.path.join(td, "modules", "home-operations")
        os.makedirs(mdir)
        with open(os.path.join(mdir, "module.yaml"), "w") as fh:
            fh.write(MODULE_FIXTURE.format(
                mid="field/home-operations",
                folder="home-operations").replace(
                    "files: []\n", files_line) + extra_yaml)
        with open(os.path.join(mdir, "MODULE.md"), "w") as fh:
            fh.write("# Module — Home Operations\n\n"
                     "**Reads:** the files. **Writes:** a register.\n"
                     "**Network:** none. **Jobs:** none.\n"
                     "**Data classes:** personal. "
                     "**Action classes:** none.\n\n"
                     "## Install\n\n1. Do it.\n")
        with open(os.path.join(mdir, "VERIFY.md"), "w") as fh:
            fh.write("# Verify\n\n## At install\n\n- x\n\n"
                     "## Deferred\n\n- y\n")
        return td

    def test_field_library_passes_without_a_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(td)
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("findings=0", r.stdout)

    def test_field_mode_flags_review_fields_and_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(td, extra_yaml="reviewed_by: A Person\n")
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("not package fields", r.stdout)
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(
                td, files_line="files:\n"
                               "  - path: ../outside.md\n"
                               "    class: static-verbatim\n")
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("escapes the module directory", r.stdout)

    def test_field_mode_flags_a_duplicate_id(self):
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(td)
            other = os.path.join(td, "modules", "home-operations-2")
            os.makedirs(other)
            src = open(os.path.join(
                td, "modules", "home-operations", "module.yaml")).read()
            with open(os.path.join(other, "module.yaml"), "w") as fh:
                fh.write(src.replace("modules/home-operations",
                                     "modules/home-operations-2"))
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("duplicate module id", r.stdout)

    def test_field_mode_flags_an_undeclared_shipped_file(self):
        # Fix item 26's missing fixture (library #13's inverse
        # check): a file shipped under templates/ that
        # module.yaml never declares is counted by the audit
        # counter but invisible to the catalog.
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(td)
            tdir = os.path.join(td, "modules", "home-operations",
                                "templates")
            os.makedirs(tdir)
            with open(os.path.join(tdir, "extra.md"), "w") as fh:
                fh.write("# Extra\n")
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("shipped file not declared", r.stdout)

    def test_field_mode_flags_a_symlink_escape(self):
        # EX-024/025 (R13): confinement used to be lexical only,
        # so a symlink inside the module pointing outside passed.
        # Resolution is confinement too.
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(
                td, files_line="files:\n"
                               "  - path: link.md\n"
                               "    class: static-verbatim\n")
            outside = os.path.join(td, "outside.md")
            with open(outside, "w") as fh:
                fh.write("# Outside\n")
            os.symlink(outside, os.path.join(
                td, "modules", "home-operations", "link.md"))
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("escapes the module directory", r.stdout)

    def test_records_changed_after_the_catalog_pin_is_a_finding(self):
        # EX-024/025 (R14): the regenerate-and-diff check is
        # blind to payload-invisible edits (a same-word-count
        # prose change alters nothing the catalog stores). The
        # git half of the check reads the pin: records changed
        # after generated_from are a finding even then.
        with tempfile.TemporaryDirectory() as td:
            self._field_repo(td)
            git(td, "init", "-q")
            git(td, "config", "user.email", "t@example.com")
            git(td, "config", "user.name", "Test")
            git(td, "add", "-A")
            git(td, "commit", "-qm", "fixture")
            r = run(BUILD_DIR, "--repo", td, "--library", "field")
            self.assertEqual(r.returncode, 0, r.stderr)
            git(td, "add", "-A")
            git(td, "commit", "-qm", "catalog")
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            mp = os.path.join(td, "modules", "home-operations",
                              "MODULE.md")
            with open(mp) as fh:
                prose = fh.read()
            with open(mp, "w") as fh:
                fh.write(prose.replace("1. Do it.", "1. Do it!"))
            git(td, "add", "-A")
            git(td, "commit", "-qm", "payload-invisible prose edit")
            r = run(SELFCHECK, "--repo", td, "--field", "field")
            self.assertEqual(r.returncode, 1)
            self.assertIn("changed after directory.json's "
                          "generated_from pin", r.stdout)
            self.assertNotIn("directory.json is stale", r.stdout)


class SelfcheckCoreTest(unittest.TestCase):
    def _core_repo(self, td, compat="[kit-1]"):
        sys.path.insert(0, os.path.join(REPO, "tools"))
        import kit_selfcheck as ks
        mdir = os.path.join(td, "modules", "02-example")
        os.makedirs(mdir)
        with open(os.path.join(mdir, "module.yaml"), "w") as fh:
            fh.write(MODULE_FIXTURE.format(
                mid="core/example", folder="02-example").replace(
                    "[kit-1]", compat))
        with open(os.path.join(mdir, "MODULE.md"), "w") as fh:
            fh.write("# Module — Example\n\n"
                     "**Reads:** the files. **Writes:** a register.\n"
                     "**Network:** none. **Jobs:** none.\n"
                     "**Data classes:** personal. "
                     "**Action classes:** none.\n\n"
                     "## Install\n\n1. Do it.\n")
        with open(os.path.join(mdir, "VERIFY.md"), "w") as fh:
            fh.write("# Verify\n\n## At install\n\n- x\n\n"
                     "## Deferred\n\n- y\n")
        wdir = os.path.join(td, "wizard")
        os.makedirs(wdir)
        manifest = os.path.join(wdir, "manifest.yaml")
        with open(manifest, "w") as fh:
            fh.write("library: core\n"
                     "interface_version: 1\n"
                     "profiles:\n"
                     "  - id: starter\n"
                     "    modules: [core/example]\n"
                     "    audit_words: 0\n"
                     "  - id: standard\n"
                     "    modules: [core/example]\n"
                     "    audit_words: 0\n")
        everything = ks.round100(ks.words(manifest)
                                 + ks.count_module_words(mdir))
        with open(os.path.join(td, "README.md"), "w") as fh:
            fh.write("# Fixture\n\n"
                     "| 02 | Example | x |\n\n"
                     "| **Starter** | 02 | ~0 words |\n"
                     "| **Standard** | 02 | ~0 words |\n"
                     f"| Everything | all | ~{everything} words |\n")
        git(td, "init", "-q")
        git(td, "config", "user.email", "t@example.com")
        git(td, "config", "user.name", "Test")
        git(td, "add", "-A")
        git(td, "commit", "-qm", "fixture")
        return td

    def test_missing_directory_json_is_a_finding_in_core_mode(self):
        # EX-024/025 (R14): the freshness block used to run only
        # when directory.json existed, so a core repo with no
        # catalog at all passed clean.
        with tempfile.TemporaryDirectory() as td:
            self._core_repo(td)
            r = run(SELFCHECK, "--repo", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("directory.json is missing", r.stdout)
            r = run(BUILD_DIR, "--repo", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            git(td, "add", "-A")
            git(td, "commit", "-qm", "catalog")
            r = run(SELFCHECK, "--repo", td)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_kit_compat_gate_is_checked(self):
        # Fix item 26's missing fixture: a module whose
        # kit_compat does not name the manifest's interface
        # version may not be offered by the wizard.
        with tempfile.TemporaryDirectory() as td:
            self._core_repo(td, compat="[kit-9]")
            r = run(SELFCHECK, "--repo", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("kit_compat", r.stdout)
            self.assertIn("does not name kit-1", r.stdout)

    def test_stale_catalog_is_a_finding(self):
        # Fix item 26's missing fixture: records edited after
        # generation, catalog not regenerated.
        with tempfile.TemporaryDirectory() as td:
            self._core_repo(td)
            r = run(BUILD_DIR, "--repo", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            git(td, "add", "-A")
            git(td, "commit", "-qm", "catalog")
            p = os.path.join(td, "modules", "02-example",
                             "module.yaml")
            with open(p) as fh:
                text = fh.read()
            with open(p, "w") as fh:
                fh.write(text.replace('title: Example',
                                      'title: Example Revised'))
            r = run(SELFCHECK, "--repo", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("directory.json is stale", r.stdout)


class ModuleYamlTest(unittest.TestCase):
    def _write(self, td, name, text):
        p = os.path.join(td, name)
        with open(p, "w") as fh:
            fh.write(text)
        return p

    def test_valid_document_parses(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "module.yaml",
                            'id: core/example\n'
                            'title: Example\n'
                            'pitch: "A pitch: with a colon, quoted."\n'
                            'version: "0.9"\n'
                            'depends_on: [core/core-procedures]\n'
                            'requires: []\n'
                            'rehearsed_at: null\n'
                            'kit_compat: [kit-1]\n'
                            'files:\n'
                            '  - path: tools/x.py\n'
                            '    class: static-verbatim\n'
                            '  - path: register.template.md\n'
                            '    class: accumulating\n')
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 0, r.stderr)
            doc = json.loads(r.stdout)
            self.assertEqual(doc["id"], "core/example")
            self.assertEqual(doc["pitch"], "A pitch: with a colon, quoted.")
            self.assertEqual(doc["version"], "0.9")
            self.assertEqual(doc["depends_on"], ["core/core-procedures"])
            self.assertEqual(doc["requires"], [])
            self.assertIsNone(doc["rehearsed_at"])
            self.assertEqual(doc["files"][1],
                             {"path": "register.template.md",
                              "class": "accumulating"})

    def test_nested_map_fails_loud(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.yaml",
                            "id: core/example\n"
                            "tiers:\n"
                            "  lite: the nested form\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad.yaml:3", r.stderr)

    def test_anchor_fails_loud(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.yaml",
                            "id: core/example\n"
                            "title: &anchor Example\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad.yaml:2", r.stderr)
            self.assertIn("anchor", r.stderr)

    def test_block_scalar_and_tab_fail_loud(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.yaml",
                            "id: core/example\n"
                            "pitch: |\n"
                            "  a multi-line pitch\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad.yaml:2", r.stderr)
            p = self._write(td, "bad2.yaml",
                            "id: core/example\n"
                            "\ttitle: Example\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad2.yaml:2", r.stderr)
            self.assertIn("tab", r.stderr)

    def test_out_of_subset_scalars_fail_loud(self):
        # The EX-022/023 reviewers' probes: every spelling full
        # YAML would silently reinterpret must be an error here,
        # named by file and line — including the probe that would
        # have manufactured a review record out of a comment.
        cases = [
            'version: 0.9 # bumped',
            "title: 'Morning Brief'",
            'version: !!str 0.9',
            'kit_compat: [[kit-1]]',
            'reviewed_by: ~',
            'reviewed_by: null # pending review',
            'reviewed_by: Null',
            'reviewed_by: false',
            'reviewed_by: yes',
            'title: on',
            'title: Off',
            'title: No',
            'title: say "hi" there',
            'title: "unterminated',
        ]
        with tempfile.TemporaryDirectory() as td:
            for line in cases:
                p = self._write(td, "bad.yaml",
                                "id: core/example\n" + line + "\n")
                r = run(MODULE_YAML, p)
                self.assertEqual(r.returncode, 1,
                                 f"accepted out-of-subset: {line}")
                self.assertIn("bad.yaml:2", r.stderr)

    def test_nested_block_sequence_fails_loud(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.yaml",
                            "id: core/example\n"
                            "files:\n"
                            "  - - path\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad.yaml:3", r.stderr)
            self.assertIn("nested", r.stderr)

    def test_block_list_item_that_is_a_list_fails_loud(self):
        # EX-024/025 (R19): `- [a, b]` used to parse into a
        # nested list no check caught — the one list form the
        # original probes missed.
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.yaml",
                            "id: core/example\n"
                            "files:\n"
                            "  - [a, b]\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 1)
            self.assertIn("bad.yaml:3", r.stderr)
            self.assertIn("nested", r.stderr)

    def test_block_list_map_may_hold_an_inline_list(self):
        # The manifest's own shape: a block-list map item whose
        # value is an inline list of scalars is one level, and
        # parses (the profiles in wizard/manifest.yaml rely on it).
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "ok.yaml",
                            "profiles:\n"
                            "  - id: starter\n"
                            "    modules: [core/example]\n")
            r = run(MODULE_YAML, p)
            self.assertEqual(r.returncode, 0, r.stderr)
            doc = json.loads(r.stdout)
            self.assertEqual(doc["profiles"][0]["modules"],
                             ["core/example"])

    def test_parity_negated_class_mention_is_not_a_declaration(self):
        # EX-024/025 (R19): _class_tokens matched negated prose —
        # "no financial data is held" declared financial. A
        # negation is not a declaration.
        with tempfile.TemporaryDirectory() as td:
            self._write(td, "module.yaml",
                        'id: core/example\n'
                        'reads: "the files."\n'
                        'writes: "a register."\n'
                        'network: "none."\n'
                        'jobs: "none."\n'
                        'data_classes: [none]\n'
                        'action_classes: [none]\n')
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Writes:** a register.\n"
                        "**Network:** none. **Jobs:** none.\n"
                        "**Data classes:** none — no financial data "
                        "is held. **Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_parity_binds_class_sets(self):
        with tempfile.TemporaryDirectory() as td:
            self._write(td, "module.yaml",
                        'id: core/example\n'
                        'reads: "the files."\n'
                        'writes: "a register."\n'
                        'network: "none."\n'
                        'jobs: "none."\n'
                        'data_classes: [personal]\n'
                        'action_classes: [none]\n')
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Writes:** a register.\n"
                        "**Network:** none. **Jobs:** none.\n"
                        "**Data classes:** personal, financial. "
                        "**Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("data classes disagree", r.stderr)
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Writes:** a register.\n"
                        "**Network:** none. **Jobs:** none.\n"
                        "**Data classes:** personal. "
                        "**Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_parity_rejects_a_repeated_header_label(self):
        with tempfile.TemporaryDirectory() as td:
            self._write(td, "module.yaml",
                        'id: core/example\n'
                        'reads: "the files."\n'
                        'writes: "a register."\n'
                        'network: "none."\n'
                        'jobs: "none."\n'
                        'data_classes: [personal]\n'
                        'action_classes: [none]\n')
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Reads:** the files.\n"
                        "**Writes:** a register.\n"
                        "**Network:** none. **Jobs:** none.\n"
                        "**Data classes:** personal. "
                        "**Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("repeats the reads label", r.stderr)

    def test_parity_mismatch_is_named(self):
        with tempfile.TemporaryDirectory() as td:
            self._write(td, "module.yaml",
                        'id: core/example\n'
                        'reads: "the files."\n'
                        'writes: "a register."\n'
                        'network: "none."\n'
                        'jobs: "none."\n'
                        'data_classes: [personal]\n'
                        'action_classes: [none]\n')
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Writes:** something "
                        "else entirely.\n**Network:** none. "
                        "**Jobs:** none.\n"
                        "**Data classes:** personal. "
                        "**Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 1)
            self.assertIn("writes disagrees", r.stderr)
            self._write(td, "MODULE.md",
                        "# Module — Example\n\n"
                        "**Reads:** the files. **Writes:** a register.\n"
                        "**Network:** none. **Jobs:** none.\n"
                        "**Data classes:** personal. "
                        "**Action classes:** none.\n")
            r = run(MODULE_YAML, "--parity", td)
            self.assertEqual(r.returncode, 0, r.stderr)


SOUL_LINT = os.path.join(
    REPO, "modules/11-persona-soul/tools/soul_lint.py")
SOUL_TEMPLATE = os.path.join(
    REPO, "modules/11-persona-soul/templates/SOUL.template.md")

VALID_SOUL = """# Test Agent

## What wins when things collide

1. Truth
2. The household
3. The user's instruction

## Examples

### Ops acknowledgment

> User: do the thing
> Agent: Done.

### Disagreement

> User: ship it anyway
> Agent: It breaks the export; I would fix that first. Your call.

### Warm mode

> User: bad news today
> Agent: That is a rough one. Here is what I can take off your plate.

### Repair

> User: that was wrong
> Agent: It was; the record is fixed.

### Anti-example

> User: do the thing
> Agent: Great question! I'd be happy to help with that!!

## How this file changes (governance)

- The core is the user's. Changes are staged diffs, approved
  before they land.
"""


class SoulLintTest(unittest.TestCase):
    def _lint(self, td, text, *extra):
        p = os.path.join(td, "SOUL.md")
        with open(p, "w") as fh:
            fh.write(text)
        return run(SOUL_LINT, p, *extra)

    def test_clean_file_is_quiet(self):
        with tempfile.TemporaryDirectory() as td:
            r = self._lint(td, VALID_SOUL)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(r.stdout, "")

    def test_word_cap_is_a_finding(self):
        with tempfile.TemporaryDirectory() as td:
            r = self._lint(td, VALID_SOUL, "--cap", "10")
            self.assertEqual(r.returncode, 1)
            self.assertIn("over the cap of 10", r.stdout)

    def test_missing_sections_are_findings(self):
        with tempfile.TemporaryDirectory() as td:
            r = self._lint(td, "# Agent\n\nBe helpful and kind.\n")
            self.assertEqual(r.returncode, 1)
            self.assertIn("no examples block", r.stdout)
            self.assertIn("no priority order", r.stdout)
            self.assertIn("no governance footer", r.stdout)

    def test_unfilled_template_never_lints_clean(self):
        # The shipped template is all slots: its placeholders
        # must not count as filled examples or as a ranking.
        r = run(SOUL_LINT, SOUL_TEMPLATE)
        self.assertEqual(r.returncode, 1)
        self.assertIn("0 filled exchange lines", r.stdout)
        self.assertIn("priority order holds 0 filled items",
                      r.stdout)

    def test_boilerplate_is_a_warning_not_a_finding(self):
        with tempfile.TemporaryDirectory() as td:
            text = VALID_SOUL + \
                "\nYou're not a chatbot. You're becoming someone.\n"
            r = self._lint(td, text)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("[warning]", r.stdout)
            self.assertIn("inherited boilerplate", r.stdout)


class PersonaSoulRegistrationTest(unittest.TestCase):
    def test_directory_carries_the_module(self):
        doc = json.load(open(os.path.join(REPO, "directory.json")))
        entries = {m["id"]: m for m in doc["modules"]}
        self.assertIn("core/persona-soul", entries)
        entry = entries["core/persona-soul"]
        files = {f["path"]: f["class"] for f in entry["files"]}
        self.assertEqual(files["templates/SOUL.template.md"],
                         "static-rendered")
        self.assertEqual(files["templates/interview.md"],
                         "static-verbatim")
        self.assertEqual(files["tools/soul_lint.py"],
                         "static-verbatim")
        self.assertIn("personal", entry["data_classes"])
        self.assertEqual(entry["depends_on"],
                         ["core/core-procedures"])
        self.assertEqual(entry["requires"], ["persona-file"])

    def test_profiles_do_not_include_persona_soul(self):
        # Profile membership is the maintainer's merge call;
        # until then the module is offered per module only.
        sys.path.insert(0, os.path.join(REPO, "tools"))
        import module_yaml
        doc = module_yaml.parse_file(
            os.path.join(REPO, "wizard", "manifest.yaml"))
        for prof in doc["profiles"]:
            self.assertNotIn("core/persona-soul", prof["modules"])

    def test_matrix_and_readme_carry_the_module(self):
        matrix = open(os.path.join(
            REPO, "docs", "capability-profiles.md")).read()
        self.assertIn("11 Persona", matrix)
        self.assertIn("persona file", matrix)
        readme = open(os.path.join(REPO, "README.md")).read()
        self.assertRegex(readme, r"(?m)^\| 11 \|")


if __name__ == "__main__":
    unittest.main()
