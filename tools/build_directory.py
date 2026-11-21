#!/usr/bin/env python3
"""build_directory.py — generate a library's directory.json and
advisories.json from its own records (docs/library.md).

Generated files are never hand-edited. directory.json is generated
from the module.yaml files under <repo>/modules/; advisories.json
from <repo>/advisories.yaml (a small human-maintained file in the
same strict flat subset; an absent file means no advisories). Both
outputs carry the library id and `generated_from`, the full commit
hash of the repository HEAD the records were read at, and are
written deterministically — sorted keys, stable module ordering —
so a diff of the generated files is reviewable like any other
change. Per-module audit words are computed on the kit's all-files
basis by the same counter the selfcheck uses.

Usage:
    python3 tools/build_directory.py [--repo .] [--library core]
                                     [--no-advisories]

--library defaults to the `library:` id in the repo's
wizard/manifest.yaml when one exists (the core repo); a field
library with no manifest passes its id explicitly.

Exit code: 0 = written, 1 = a record failed to parse, 2 = bad args.
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import module_yaml  # noqa: E402
import kit_selfcheck  # noqa: E402  (for the audit-word counter)


def git_head(repo):
    try:
        r = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def manifest_library(repo):
    path = os.path.join(repo, "wizard", "manifest.yaml")
    if not os.path.isfile(path):
        return None
    for line in open(path, encoding="utf-8"):
        if line.startswith("library:"):
            return line.split(":", 1)[1].strip()
    return None


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
    library = args.library or manifest_library(repo)
    if not library:
        print("error: no library id (no manifest, no --library)",
              file=sys.stderr)
        return 2
    generated_from = git_head(repo)

    modules = []
    modules_root = os.path.join(repo, "modules")
    for d in sorted(os.listdir(modules_root)):
        mdir = os.path.join(modules_root, d)
        yaml_path = os.path.join(mdir, "module.yaml")
        if not os.path.isfile(yaml_path):
            continue
        try:
            meta = module_yaml.parse_file(yaml_path)
        except module_yaml.ModuleYamlError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        entry = dict(meta)
        entry["audit_words"] = kit_selfcheck.count_module_words(mdir)
        modules.append(entry)
    modules.sort(key=lambda e: e.get("id", ""))
    dump(os.path.join(repo, "directory.json"),
         {"library": library, "generated_from": generated_from,
          "modules": modules})
    print(f"directory.json: library={library} modules={len(modules)} "
          f"generated_from={generated_from}")

    if not args.no_advisories:
        advisories = []
        src = os.path.join(repo, "advisories.yaml")
        if os.path.isfile(src):
            try:
                doc = module_yaml.parse_file(src)
            except module_yaml.ModuleYamlError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
            advisories = doc.get("advisories") or []
        advisories = sorted(advisories,
                            key=lambda a: a.get("id", "") if
                            isinstance(a, dict) else "")
        dump(os.path.join(repo, "advisories.json"),
             {"library": library, "generated_from": generated_from,
              "advisories": advisories})
        print(f"advisories.json: {len(advisories)} advisories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
