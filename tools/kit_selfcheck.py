#!/usr/bin/env python3
"""kit_selfcheck.py — the kit lints itself. Structural checks only.

Deterministic, stdlib only, report-only: it writes nothing but its
report (stdout, or a file with --report). It checks the class of
defect the kit's review rounds kept finding by hand:

  1. Every module folder on disk carries a module.yaml that parses
     under the strict flat subset (tools/module_yaml.py — anything
     outside the subset is a loud parse error, named by file and
     line), carries every required field, and points back at its
     own folder. wizard/manifest.yaml holds library-level data and
     profiles only: a per-module field there is a duplication
     defect, and every profile entry must reference existing
     qualified module ids.
  2. MODULE.md header parity: each module's module.yaml
     reads/writes/network/jobs agree with its MODULE.md header
     block — the header is the human-readable form of the same
     claims, and the two may not drift apart.
  3. Every module has MODULE.md (with the Reads/Writes/Network/Jobs
     header and an Install section) and VERIFY.md (with At install
     and Deferred sections); files a MODULE.md references
     (templates/, tools/, *.template.md, *.py in backticks) exist;
     every file module.yaml declares exists, with a valid class.
  4. The README module table matches the module folders on disk.
  5. Profile audit word counts in the manifest are within 10% of
     the counts recomputed from the tree. Audit cost counts every
     installed file: the wizard, the manifest, and each module's
     MODULE.md, VERIFY.md, module.yaml, templates, and tools.
  6. The README's printed audit figures match the manifest's
     (Starter, Standard) and the recomputed all-modules figure
     (Everything) exactly — the numbers a stranger reads are the
     numbers the manifest carries.

It also prints per-module word counts (the kit's word-budget
discipline: every release should know what it weighs) and an
informational rehearsal-staleness report: for each module, whether
files in its directory changed after the pin its rehearsed_at
names. Staleness is printed, never counted in findings — the
release gate is the findings count — and the check skips silently
when the checkout is not a git work tree.

Usage:
    python3 tools/kit_selfcheck.py [--repo .] [--report PATH]

Exit code: 0 = no findings, 1 = findings, 2 = bad arguments.
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import module_yaml  # noqa: E402

BACKTICK = re.compile(r"`([^`]+)`")
REQUIRED_FIELDS = ("id", "dir", "title", "pitch", "version",
                   "maintainer", "license", "kit_compat", "depends_on",
                   "requires", "degrades_without", "reads", "writes",
                   "network", "jobs", "rehearsed_at", "data_classes",
                   "action_classes", "files")
FILE_CLASSES = ("static-verbatim", "static-rendered", "accumulating")
DATA_CLASSES = ("none", "personal", "financial", "health", "third-party")
ACTION_CLASSES = ("none", "send", "file", "spend", "delete", "contact")


def words(path):
    try:
        return len(open(path, encoding="utf-8", errors="replace").read().split())
    except OSError:
        return 0


def tree_words(root):
    """Words in every text file under root (skips caches/binaries)."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for f in filenames:
            if f.endswith((".pyc", ".png", ".jpg", ".gif")):
                continue
            total += words(os.path.join(dirpath, f))
    return total


def count_module_words(mdir):
    """Audit words for one module: every file an install reads —
    MODULE.md, VERIFY.md, module.yaml, templates (templates/ and
    *.template.md), and tools/."""
    w = words(os.path.join(mdir, "MODULE.md"))
    w += words(os.path.join(mdir, "VERIFY.md"))
    w += words(os.path.join(mdir, "module.yaml"))
    tdir = os.path.join(mdir, "templates")
    if os.path.isdir(tdir):
        w += tree_words(tdir)
    for f in os.listdir(mdir):
        if f.endswith(".template.md"):
            w += words(os.path.join(mdir, f))
    tools_dir = os.path.join(mdir, "tools")
    if os.path.isdir(tools_dir):
        w += tree_words(tools_dir)
    return w


def round100(n):
    return int(round(n / 100.0)) * 100


def parse_manifest(path):
    """Tiny reader for the manifest's regular shape (no yaml dep).
    Returns (library_id, profiles, has_module_section)."""
    text = open(path, encoding="utf-8").read()
    library = None
    profiles = []
    section = None
    cur = None
    has_module_section = False
    for line in text.splitlines():
        if line.startswith("modules:"):
            has_module_section = True
        elif line.startswith("profiles:"):
            section = "profiles"
        m = re.match(r"library:\s*(\S+)", line)
        if m and library is None:
            library = m.group(1)
        m = re.match(r"\s*- id:\s*(\S+)", line)
        if m and section == "profiles":
            cur = {"id": m.group(1)}
            profiles.append(cur)
            continue
        if cur is not None and section == "profiles":
            m = re.match(r"\s*audit_words:\s*(\S+)", line)
            if m:
                cur["audit_words"] = m.group(1).strip('"')
            m = re.match(r"\s*modules:\s*\[([^\]]*)\]", line)
            if m:
                cur["modules"] = [x.strip() for x in m.group(1).split(",")]
    return library, profiles, has_module_section


def staleness_lines(repo, metas):
    """Informational rehearsal-staleness report. Uses git when the
    checkout is a git work tree; returns [] (silence) otherwise."""
    if not os.path.isdir(os.path.join(repo, ".git")):
        return []

    def git(*argv):
        try:
            r = subprocess.run(["git", "-C", repo, *argv],
                               capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        return r.stdout if r.returncode == 0 else None

    if git("rev-parse", "--verify", "--quiet", "HEAD") is None:
        return []
    out = []
    for meta in metas:
        mid, mdir_rel = meta["id"], meta["dir"]
        ra = meta.get("rehearsed_at")
        if not ra:
            out.append(f"{mid}: unrehearsed (no rehearsed_at)")
            continue
        pin = None
        for tok in reversed(re.findall(r"\b[0-9a-f]{7,40}\b", str(ra))):
            if git("rev-parse", "--verify", "--quiet",
                   tok + "^{commit}") is not None:
                pin = tok
                break
        if pin is None:
            out.append(f"{mid}: no pin recorded in rehearsed_at")
            continue
        changed = git("diff", "--name-only", pin, "HEAD", "--", mdir_rel)
        if changed is None:
            continue
        n = len([l for l in changed.splitlines() if l.strip()])
        dirty = git("status", "--porcelain", "--", mdir_rel)
        if dirty:
            n += len([l for l in dirty.splitlines() if l.strip()])
        if n:
            out.append(f"{mid}: changed since rehearsal pin {pin[:7]} "
                       f"({n} file(s)) — 'rehearsed at pin; changed "
                       f"since'")
        else:
            out.append(f"{mid}: current at rehearsal pin {pin[:7]}")
    return out


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
    library, profiles, has_module_section = parse_manifest(manifest_path)
    if has_module_section:
        findings.append("manifest.yaml carries a modules: section — "
                        "per-module data lives in module.yaml only "
                        "(duplication is a defect)")
    if not library:
        findings.append("manifest.yaml names no library id")

    modules_root = os.path.join(repo, "modules")
    on_disk = sorted(d for d in os.listdir(modules_root)
                     if os.path.isdir(os.path.join(modules_root, d))) \
        if os.path.isdir(modules_root) else []

    metas = []
    by_id = {}
    for d in on_disk:
        mdir = os.path.join(modules_root, d)
        yaml_path = os.path.join(mdir, "module.yaml")
        if not os.path.isfile(yaml_path):
            findings.append(f"modules/{d}: module.yaml missing")
            continue
        try:
            meta = module_yaml.parse_file(yaml_path)
        except module_yaml.ModuleYamlError as exc:
            findings.append(f"module.yaml parse error: {exc}")
            continue
        meta["_folder"] = d
        metas.append(meta)
        mid = meta.get("id")
        if isinstance(mid, str):
            by_id[mid] = meta

    module_words = {}
    for meta in metas:
        mid = meta.get("id", f"modules/{meta['_folder']}")
        mdir = os.path.join(repo, meta.get("dir", ""))
        for field in REQUIRED_FIELDS:
            if field not in meta:
                findings.append(f"{mid}: module.yaml missing field: {field}")
        if meta.get("dir") != f"modules/{meta['_folder']}":
            findings.append(f"{mid}: module.yaml dir {meta.get('dir')!r} "
                            f"does not match its folder "
                            f"modules/{meta['_folder']}")
        if not (isinstance(mid, str) and mid.startswith(f"{library}/")
                and mid.count("/") == 1 and len(mid) > len(library) + 1):
            findings.append(f"{mid}: id is not a qualified "
                            f"{library}/<module> id")
        for dep in meta.get("depends_on") or []:
            if dep not in by_id:
                findings.append(f"{mid}: depends_on names unknown "
                                f"module: {dep}")
        for deg in meta.get("degrades_without") or []:
            if "/" in deg and deg not in by_id:
                findings.append(f"{mid}: degrades_without names unknown "
                                f"module: {deg}")
        for dc in meta.get("data_classes") or []:
            if dc not in DATA_CLASSES:
                findings.append(f"{mid}: unknown data class: {dc}")
        for ac in meta.get("action_classes") or []:
            if ac not in ACTION_CLASSES:
                findings.append(f"{mid}: unknown action class: {ac}")
        for entry in meta.get("files") or []:
            if not isinstance(entry, dict) or "path" not in entry \
                    or "class" not in entry:
                findings.append(f"{mid}: files entry is not a "
                                f"path/class pair: {entry!r}")
                continue
            if entry["class"] not in FILE_CLASSES:
                findings.append(f"{mid}: file {entry['path']} has "
                                f"unknown class: {entry['class']}")
            if not os.path.isfile(os.path.join(mdir, entry["path"])):
                findings.append(f"{mid}: declared file missing: "
                                f"{entry['path']}")
        for problem in module_yaml.check_parity(mdir):
            findings.append(f"{mid}: {problem}")

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
                            os.path.exists(os.path.join(repo, "modules", dd, ref))
                            for dd in on_disk):
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
        if isinstance(mid, str):
            module_words[mid] = count_module_words(mdir)

    for prof in profiles:
        for ref in prof.get("modules", []):
            if ref not in by_id:
                findings.append(f"profile {prof['id']}: references "
                                f"unknown module: {ref}")

    readme = open(os.path.join(repo, "README.md"), encoding="utf-8").read()
    table_nums = sorted(set(re.findall(r"^\| (\d{2}) \|", readme, re.M)))
    disk_nums = sorted(d.split("-")[0] for d in on_disk)
    if table_nums != disk_nums:
        findings.append(f"README module table {table_nums} != module "
                        f"folders {disk_nums}")

    base_words = words(os.path.join(repo, "wizard", "SKILL.md")) \
        + words(manifest_path)
    for prof in profiles:
        stated = int(prof.get("audit_words", 0))
        actual = base_words + sum(module_words.get(m, 0)
                                  for m in prof.get("modules", []))
        if stated and abs(actual - stated) > 0.10 * stated:
            findings.append(f"profile {prof['id']}: audit_words {stated} "
                            f"vs recomputed {actual} (>10% drift)")
        notes.append(f"profile {prof['id']}: audit cost {actual} words "
                     f"(manifest says {stated})")

    # Check 6: README figures == manifest / recomputed figures.
    readme_figs = {}
    for label, pat in (("starter", r"\*\*Starter\*\*"),
                       ("standard", r"\*\*Standard\*\*"),
                       ("everything", r"Everything")):
        m = re.search(pat + r"[^|\n]*\|[^|\n]*\|[^|\n]*~\s*([\d,]+)\s*words",
                      readme)
        if m:
            readme_figs[label] = int(m.group(1).replace(",", ""))
    stated_by_id = {p["id"]: int(p.get("audit_words", 0)) for p in profiles}
    for label in ("starter", "standard"):
        if label not in readme_figs:
            findings.append(f"README: no audit figure found for {label}")
        elif readme_figs[label] != stated_by_id.get(label):
            findings.append(f"README {label} figure {readme_figs[label]} "
                            f"!= manifest audit_words {stated_by_id.get(label)}")
    everything = round100(base_words + sum(module_words.values()))
    if "everything" not in readme_figs:
        findings.append("README: no audit figure found for everything")
    elif readme_figs["everything"] != everything:
        findings.append(f"README everything figure {readme_figs['everything']} "
                        f"!= recomputed {everything}")
    notes.append(f"everything: audit cost {everything} words (rounded)")
    for mid in sorted(module_words, key=module_words.get, reverse=True):
        notes.append(f"module words: {mid} {module_words[mid]}")

    stale = staleness_lines(repo, metas)

    lines = [f"run_receipt: modules={len(metas)} profiles={len(profiles)} "
             f"findings={len(findings)}"]
    lines += [f"- [finding] {f}" for f in findings]
    lines += [f"- [note] {n}" for n in notes]
    if stale:
        lines.append("rehearsal staleness (informational, not findings):")
        lines += [f"- [staleness] {s}" for s in stale]
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
