#!/usr/bin/env python3
"""build_directory.py — generate a library's directory.json and
advisories.json from its own records (docs/library.md).

Generated files are never hand-edited. directory.json is generated
from the module.yaml files under <repo>/modules/; advisories.json
from <repo>/advisories.yaml (a small human-maintained file in the
same strict flat subset). Both outputs carry the library id and
`generated_from`, the full commit hash of the repository HEAD the
records were read at, and are written deterministically — sorted
keys, stable module ordering — so a diff of the generated files
is reviewable like any other change. Per-module audit words are
computed on the kit's all-files basis by the same counter the
selfcheck uses.

The pin discipline is enforced, not assumed: generation refuses
a dirty working tree (a catalog generated from uncommitted
records would stamp a HEAD its entries do not describe) and
fails outright when the repo has no git HEAD to stamp. Entries
are built from an allowlist of package fields — an unknown key
in a module.yaml is an error, not a pass-through — and review
fields are not package fields at all (decision, 2026-11-21):
a module's review record lives in the core index or the
installer's vetting log, never in the module's own catalog
entry. An absent advisories.yaml means the library has no
advisories channel: no advisories.json is written, and a stale
one is removed — an empty list is a claim, and the generator
does not make claims the records do not support.

Usage:
    python3 tools/build_directory.py [--repo .] [--library core]
                                     [--no-advisories]

--library defaults to the `library:` id in the repo's
wizard/manifest.yaml when one exists (the core repo); a field
library with no manifest passes its id explicitly. Every module
id must start with `<library>/` — the namespace is enforced
here as well as in the selfcheck.

Exit code: 0 = written, 1 = a record failed validation or the
tree is not generatable, 2 = bad args.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import module_yaml  # noqa: E402
import kit_selfcheck  # noqa: E402  (for the audit-word counter)

# The package fields a catalog entry may carry: module_yaml's
# required fields, the optional tiers block, and the computed
# audit_words. Anything else in a module.yaml — a review field,
# a stray note, a hostile library's extra key — stops generation.
ENTRY_FIELDS = ("id", "dir", "title", "pitch", "version",
                "maintainer", "license", "kit_compat", "depends_on",
                "requires", "degrades_without", "reads", "writes",
                "network", "jobs", "rehearsed_at", "data_classes",
                "action_classes", "files", "tiers")
PITCH_MAX = 400  # the wizard tells installers catalog text is
                 # length-capped; this is the cap
ADVISORY_ID = re.compile(r"^ADV-\d{4}-\d{3}$")
FULL_HASH = re.compile(r"^[0-9a-f]{40}$")
DATE_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class BuildError(Exception):
    pass


def git(repo, *argv):
    try:
        r = subprocess.run(["git", "-C", repo, *argv],
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def git_head(repo):
    out = git(repo, "rev-parse", "HEAD")
    return out.strip() if out else None


def tree_dirty(repo):
    out = git(repo, "status", "--porcelain")
    if out is None:
        return True  # cannot prove the tree is clean: treat as dirty
    return bool(out.strip())


def manifest_library(repo):
    path = os.path.join(repo, "wizard", "manifest.yaml")
    if not os.path.isfile(path):
        return None
    try:
        doc = module_yaml.parse_file(path)
    except module_yaml.ModuleYamlError as exc:
        raise BuildError(str(exc))
    lib = doc.get("library")
    return lib if isinstance(lib, str) else None


def collect_entries(repo, library):
    """Parse every module.yaml under <repo>/modules and build its
    catalog entry from the allowlist. Raises BuildError."""
    entries = []
    seen = {}
    modules_root = os.path.join(repo, "modules")
    for d in sorted(os.listdir(modules_root)):
        mdir = os.path.join(modules_root, d)
        yaml_path = os.path.join(mdir, "module.yaml")
        if not os.path.isfile(yaml_path):
            continue
        try:
            meta = module_yaml.parse_file(yaml_path)
        except module_yaml.ModuleYamlError as exc:
            raise BuildError(str(exc))
        mid = meta.get("id")
        if not isinstance(mid, str) or \
                not mid.startswith(f"{library}/"):
            raise BuildError(
                f"{yaml_path}: id {mid!r} does not start with "
                f"{library}/ — the library namespace is enforced")
        if mid in seen:
            raise BuildError(
                f"{yaml_path}: duplicate module id {mid} (first "
                f"seen in {seen[mid]})")
        seen[mid] = yaml_path
        unknown = sorted(set(meta) - set(ENTRY_FIELDS))
        if unknown:
            raise BuildError(
                f"{yaml_path}: keys outside the catalog allowlist: "
                f"{unknown} (review records are not package fields; "
                f"see docs/library.md)")
        pitch = meta.get("pitch")
        if isinstance(pitch, str) and len(pitch) > PITCH_MAX:
            raise BuildError(
                f"{yaml_path}: pitch is {len(pitch)} characters; "
                f"catalog text is capped at {PITCH_MAX}")
        entry = {k: meta[k] for k in ENTRY_FIELDS if k in meta}
        entry["audit_words"] = kit_selfcheck.count_module_words(mdir)
        entries.append(entry)
    entries.sort(key=lambda e: e["id"])
    return entries


def validate_advisories(entries, known_ids, library):
    """Return a list of problems with advisory entries. `pin` is
    the module's checkout pin (docs/library.md), or the literal
    `all`; `known_ids` is the set of module ids resolvable in
    this repo — an entry may also name the library itself, or a
    qualified id from another library the core index carries."""
    problems = []
    if not isinstance(entries, list):
        return ["advisories: not a list"]
    for adv in entries:
        if not isinstance(adv, dict):
            problems.append(f"advisory is not a record: {adv!r}")
            continue
        aid = adv.get("id")
        if not isinstance(aid, str) or not ADVISORY_ID.match(aid):
            problems.append(f"advisory id {aid!r} is not ADV-YYYY-NNN")
        mod = adv.get("module")
        if not isinstance(mod, str) or not mod:
            problems.append(f"{aid}: module missing")
        elif mod != library and mod not in known_ids \
                and "/" not in mod:
            problems.append(f"{aid}: module {mod!r} does not resolve")
        pin = adv.get("pin")
        if pin != "all" and not (isinstance(pin, str)
                                 and FULL_HASH.match(pin)):
            problems.append(f"{aid}: pin {pin!r} is neither a full "
                            f"commit hash (the checkout pin) nor 'all'")
        date = adv.get("date")
        if not isinstance(date, str) or not DATE_SHAPE.match(date):
            problems.append(f"{aid}: date {date!r} is not YYYY-MM-DD")
        else:
            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                problems.append(f"{aid}: date {date!r} is not a date")
        for field in ("reason", "remedy"):
            if not isinstance(adv.get(field), str) \
                    or not adv[field].strip():
                problems.append(f"{aid}: {field} missing or empty")
        if "fixed_in" in adv:
            fixed = adv["fixed_in"]
            if not isinstance(fixed, str) or not FULL_HASH.match(fixed):
                problems.append(f"{aid}: fixed_in {fixed!r} is not a "
                                f"full commit hash")
    return problems


def advisory_entries(repo, known_ids, library):
    """The validated advisory list from <repo>/advisories.yaml, or
    None when the file is absent (no advisories channel). Raises
    BuildError on a parse or validation failure."""
    src = os.path.join(repo, "advisories.yaml")
    if not os.path.isfile(src):
        return None
    try:
        doc = module_yaml.parse_file(src)
    except module_yaml.ModuleYamlError as exc:
        raise BuildError(str(exc))
    entries = doc.get("advisories") or []
    problems = validate_advisories(entries, known_ids, library)
    if problems:
        raise BuildError("advisories.yaml: " + "; ".join(problems))
    return sorted(entries, key=lambda a: a.get("id", ""))


def build_payloads(repo, library, generated_from):
    """(directory_payload, advisories_payload_or_None) for the
    repo's current records, stamped with the given generated_from.
    The selfcheck calls this to test catalog freshness without
    git. Raises BuildError."""
    entries = collect_entries(repo, library)
    directory = {"library": library, "generated_from": generated_from,
                 "modules": entries}
    advisories = advisory_entries(
        repo, {e["id"] for e in entries}, library)
    payload = None
    if advisories is not None:
        payload = {"library": library,
                   "generated_from": generated_from,
                   "advisories": advisories}
    return directory, payload


def dump(path, payload):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def main():
    ap = argparse.ArgumentParser(
        description="Generate directory.json and advisories.json.")
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    ap.add_argument("--library", help="library id (default: the "
                                      "manifest's, if any)")
    ap.add_argument("--no-advisories", action="store_true",
                    help="write directory.json only")
    args = ap.parse_args()
    repo = os.path.abspath(os.path.expanduser(args.repo))
    try:
        library = args.library or manifest_library(repo)
        if not library:
            print("error: no library id (no manifest, no --library)",
                  file=sys.stderr)
            return 2
        generated_from = git_head(repo)
        if not generated_from:
            print("error: no git HEAD to stamp — a catalog without "
                  "a pin is not generated", file=sys.stderr)
            return 1
        if tree_dirty(repo):
            print("error: working tree is dirty — a catalog stamps "
                  "the HEAD its records were read at, so commit "
                  "the records first", file=sys.stderr)
            return 1
        directory, advisories = build_payloads(repo, library,
                                               generated_from)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    dump(os.path.join(repo, "directory.json"), directory)
    print(f"directory.json: library={library} "
          f"modules={len(directory['modules'])} "
          f"generated_from={generated_from}")

    if not args.no_advisories:
        out = os.path.join(repo, "advisories.json")
        if advisories is None:
            if os.path.isfile(out):
                os.remove(out)
                print("advisories.json: removed — no advisories.yaml, "
                      "so no advisories channel is claimed")
            else:
                print("advisories.json: not written — no "
                      "advisories.yaml (no advisories channel)")
        else:
            dump(out, advisories)
            print(f"advisories.json: {len(advisories['advisories'])} "
                  f"advisories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
