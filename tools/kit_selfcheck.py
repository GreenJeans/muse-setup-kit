#!/usr/bin/env python3
"""kit_selfcheck.py — the kit lints itself. Structural checks only.

Deterministic, stdlib only, report-only: it writes nothing but its
report (stdout, or a file with --report). It checks the class of
defect the kit's review rounds kept finding by hand:

  1. Every module in wizard/manifest.yaml has MODULE.md (with the
     Reads/Writes/Network/Jobs header and an Install section) and
     VERIFY.md (with At install and Deferred sections).
  2. Files a MODULE.md references (templates/, tools/, *.template.md,
     *.py in backticks) exist in the module's folder.
  3. Every module folder on disk is in the manifest (no orphans),
     and the README module table matches the manifest.
  4. Profile audit word counts in the manifest are within 10% of
     the counts recomputed from the tree.

It also prints per-module word counts (the kit's word-budget
discipline: every release should know what it weighs).

Usage:
    python3 tools/kit_selfcheck.py [--repo .] [--report PATH]

Exit code: 0 = no findings, 1 = findings, 2 = bad arguments.
"""
import argparse
import os
import re
import sys

BACKTICK = re.compile(r"`([^`]+)`")


def words(path):
    try:
        return len(open(path, encoding="utf-8", errors="replace").read().split())
    except OSError:
        return 0


def parse_manifest(path):
    """Tiny reader for the manifest's regular shape (no yaml dep)."""
    text = open(path, encoding="utf-8").read()
    modules, profiles = [], []
    section = None
    cur = None
    for line in text.splitlines():
        if line.startswith("modules:"):
            section = "modules"
        elif line.startswith("profiles:"):
            section = "profiles"
        m = re.match(r"\s*- id:\s*(\S+)", line)
        if m and section:
            cur = {"id": m.group(1)}
            (modules if section == "modules" else profiles).append(cur)
            continue
        if cur is not None:
            for key in ("dir", "audit_words"):
                m = re.match(rf"\s*{key}:\s*(\S+)", line)
                if m:
                    cur[key] = m.group(1).strip('"')
            m = re.match(r"\s*modules:\s*\[([^\]]*)\]", line)
            if m and section == "profiles":
                cur["modules"] = [x.strip() for x in m.group(1).split(",")]
    return modules, profiles


def main():
    ap = argparse.ArgumentParser(description="Structural self-check for the kit repo.")
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    ap.add_argument("--report", help="also write the report to this path")
    args = ap.parse_args()
    repo = os.path.abspath(os.path.expanduser(args.repo))
    findings, notes = [], []

    manifest_path = os.path.join(repo, "wizard", "manifest.yaml")
    if not os.path.isfile(manifest_path):
        print(f"error: no manifest at {manifest_path}", file=sys.stderr)
        return 2
    modules, profiles = parse_manifest(manifest_path)
    by_id = {}
    modules_root = os.path.join(repo, "modules")
    on_disk_all = sorted(d for d in os.listdir(modules_root)
                         if os.path.isdir(os.path.join(modules_root, d))) \
        if os.path.isdir(modules_root) else []

    base_words = words(os.path.join(repo, "wizard", "SKILL.md")) + words(manifest_path)
    module_words = {}
    for mod in modules:
        mid, mdir = mod["id"], os.path.join(repo, mod.get("dir", ""))
        by_id[mid] = mod
        if not os.path.isdir(mdir):
            findings.append(f"{mid}: manifest dir missing: {mod.get('dir')}")
            continue
        module_md = os.path.join(mdir, "MODULE.md")
        verify_md = os.path.join(mdir, "VERIFY.md")
        text = ""
        if not os.path.isfile(module_md):
            findings.append(f"{mid}: MODULE.md missing")
        else:
            text = open(module_md, encoding="utf-8", errors="replace").read()
            head = "\n".join(text.splitlines()[:12])
            for token in ("Reads:", "Writes:", "Network:", "Jobs:"):
                if token not in head:
                    findings.append(f"{mid}: MODULE.md header missing {token}")
            if "## Install" not in text:
                findings.append(f"{mid}: MODULE.md has no Install section")
            for ref in sorted(set(BACKTICK.findall(text))):
                if ("/" in ref and (ref.startswith(("templates/", "tools/")))
                        or ref.endswith((".template.md", ".py"))):
                    if os.path.exists(os.path.join(mdir, ref)):
                        continue
                    # A bare filename may be a cross-module reference
                    # (e.g. module 03 amending module 02's brief
                    # template): it counts as present if it exists
                    # anywhere in the modules tree.
                    if "/" not in ref and any(
                            os.path.exists(os.path.join(repo, "modules", d, ref))
                            for d in on_disk_all):
                        continue
                    findings.append(f"{mid}: referenced file missing: {ref}")
        if not os.path.isfile(verify_md):
            findings.append(f"{mid}: VERIFY.md missing")
        else:
            vtext = open(verify_md, encoding="utf-8", errors="replace").read()
            if "## At install" not in vtext:
                findings.append(f"{mid}: VERIFY.md has no At install section")
            if "## Deferred" not in vtext:
                findings.append(f"{mid}: VERIFY.md has no Deferred section")
        w = words(module_md)
        tools_dir = os.path.join(mdir, "tools")
        if os.path.isdir(tools_dir):
            w += sum(words(os.path.join(tools_dir, f))
                     for f in os.listdir(tools_dir))
        module_words[mid] = w

    on_disk = sorted(d for d in os.listdir(os.path.join(repo, "modules"))
                     if os.path.isdir(os.path.join(repo, "modules", d)))
    manifest_dirs = sorted(os.path.basename(m.get("dir", "")) for m in modules)
    for d in on_disk:
        if d not in manifest_dirs:
            findings.append(f"orphan module folder not in manifest: modules/{d}")

    readme = open(os.path.join(repo, "README.md"), encoding="utf-8").read()
    table_nums = sorted(set(re.findall(r"^\| (\d{2}) \|", readme, re.M)))
    manifest_nums = sorted(d.split("-")[0] for d in manifest_dirs)
    if table_nums != manifest_nums:
        findings.append(f"README module table {table_nums} != manifest {manifest_nums}")

    for prof in profiles:
        stated = int(prof.get("audit_words", 0))
        actual = base_words + sum(module_words.get(m, 0)
                                   for m in prof.get("modules", []))
        if stated and abs(actual - stated) > 0.10 * stated:
            findings.append(f"profile {prof['id']}: audit_words {stated} "
                            f"vs recomputed {actual} (>10% drift)")
        notes.append(f"profile {prof['id']}: audit cost {actual} words "
                     f"(manifest says {stated})")
    for mid in sorted(module_words, key=module_words.get, reverse=True):
        notes.append(f"module words: {mid} {module_words[mid]}")

    lines = [f"run_receipt: modules={len(modules)} profiles={len(profiles)} "
             f"findings={len(findings)}"]
    lines += [f"- [finding] {f}" for f in findings]
    lines += [f"- [note] {n}" for n in notes]
    if not findings:
        lines.append("No findings.")
    out = "\n".join(lines)
    print(out)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
