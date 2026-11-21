#!/usr/bin/env python3
"""kit_selfcheck.py — the kit lints itself. Structural checks only.

Deterministic, stdlib only, report-only: it writes nothing but its
report (stdout, or a file with --report). It checks the class of
defect the kit's review rounds kept finding by hand:

  1. Every module folder on disk carries a module.yaml that parses
     under the strict flat subset (tools/module_yaml.py — anything
     outside the subset is a loud parse error, named by file and
     line), carries every required field, and points back at its
     own folder. Module ids are unique. Review fields
     (reviewed_at / reviewed_by) are forbidden in a package: a
     module's review record lives in the core index or the
     installer's vetting log, never in the module's own files
     (decision, 2026-11-21). wizard/manifest.yaml — read with the
     same strict parser — holds library-level data and profiles
     only: a per-module field there is a duplication defect, and
     every profile entry must reference existing qualified
     module ids. Each module's kit_compat must name the core
     interface version the manifest declares.
  2. MODULE.md header parity: each module's module.yaml
     reads/writes/network/jobs agree with its MODULE.md header
     block, and the header's Data classes / Action classes lines
     name the same class sets the module.yaml declares — the
     header is the human-readable form of the same claims, and
     the two may not drift apart.
  3. Every module has MODULE.md (with the Reads/Writes/Network/Jobs
     header and an Install section) and VERIFY.md (with At install
     and Deferred sections); files a MODULE.md references
     (templates/, tools/, *.template.md, *.py in backticks) exist;
     every file module.yaml declares exists, with a valid class,
     at a path confined to the module directory — lexically and
     by resolution: a declared path that is a symlink pointing
     outside the module directory is an escape, not a file; and
     the check
     runs both ways — a file shipped under templates/ or tools/
     (or as a top-level *.template.md) that module.yaml never
     declares is a finding, because the audit counter counts it
     while the catalog would not disclose it.
  4. The README module table matches the module folders on disk.
  5. Profile audit word counts in the manifest are within 10% of
     the counts recomputed from the tree. Audit cost counts every
     installed file: the wizard, the manifest, and each module's
     MODULE.md, VERIFY.md, module.yaml, templates, and tools.
  6. The README's printed audit figures match the manifest's
     (Starter, Standard) and the recomputed all-modules figure
     (Everything) exactly — the numbers a stranger reads are the
     numbers the manifest carries.
  7. The generated catalog is fresh: directory.json equals what
     tools/build_directory.py regenerates from the tree's current
     records (generated_from aside — the pin names the commit the
     records were read at, and the catalog commit follows it), and
     advisories.json exists exactly when advisories.yaml does,
     with entries that validate. A stale catalog is a finding:
     the listing verbs speak from it. Two depth checks ride with
     it: in core mode a missing directory.json is itself a
     finding (the catalog is generated, not optional), and when
     the checkout is a git work tree, module records changed
     after the catalog's generated_from pin are a finding even
     when the edit is invisible to the catalog's payload — the
     pin must name the records the catalog was built from.

A field library (no manifest, no README table, no profiles) is
checked with `--field <library-id>`: the same package checks —
schema, qualified ids, classes, file existence both ways, parity
— without the core repo's own furniture. The wizard's inspect
and add library verbs run this mode on a fetched field checkout
and paste the receipt into the vetting entry.

It also prints per-module word counts (the kit's word-budget
discipline: every release should know what it weighs) and an
informational rehearsal-staleness report: for each module, whether
files in its directory changed after the pin its rehearsed_at
names. Staleness is printed, never counted in findings — the
release gate is the findings count — and the check skips silently
when the checkout is not a git work tree.

Usage:
    python3 tools/kit_selfcheck.py [--repo .] [--report PATH]
                                   [--field LIBRARY-ID]

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
FORBIDDEN_FIELDS = ("reviewed_at", "reviewed_by")
FILE_CLASSES = ("static-verbatim", "static-rendered", "accumulating")
DATA_CLASSES = module_yaml.DATA_CLASSES
ACTION_CLASSES = module_yaml.ACTION_CLASSES


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
    """Read the manifest with the strict subset parser — the same
    fail-loud discipline as module.yaml, so malformed manifest
    syntax is a finding, not a silent misread.
    Returns (library_id, profiles, has_module_section,
    interface_version). Raises module_yaml.ModuleYamlError."""
    doc = module_yaml.parse_file(path)
    library = doc.get("library")
    profiles = doc.get("profiles") or []
    has_module_section = "modules" in doc
    interface = doc.get("interface_version")
    return library, profiles, has_module_section, interface


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
    ap.add_argument("--field", metavar="LIBRARY-ID",
                    help="check a field library: package checks only "
                         "(no manifest, README, or profile checks)")
    args = ap.parse_args()
    repo = os.path.abspath(os.path.expanduser(args.repo))
    findings, notes = [], []

    manifest_path = os.path.join(repo, "wizard", "manifest.yaml")
    interface = None
    if args.field:
        library, profiles = args.field, []
    else:
        if not os.path.isfile(manifest_path):
            print(f"error: no manifest at {manifest_path}",
                  file=sys.stderr)
            return 2
        try:
            library, profiles, has_module_section, interface = \
                parse_manifest(manifest_path)
        except module_yaml.ModuleYamlError as exc:
            print(f"run_receipt: manifest unparseable")
            print(f"- [finding] manifest.yaml: {exc}")
            return 1
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
            if mid in by_id:
                findings.append(f"{mid}: duplicate module id — "
                                f"modules/{by_id[mid]['_folder']} and "
                                f"modules/{d} both claim it; the "
                                f"catalog would carry both and the "
                                f"index neither unambiguously")
            by_id[mid] = meta

    module_words = {}
    for meta in metas:
        mid = meta.get("id", f"modules/{meta['_folder']}")
        mdir = os.path.join(repo, meta.get("dir", ""))
        for field in REQUIRED_FIELDS:
            if field not in meta:
                findings.append(f"{mid}: module.yaml missing field: {field}")
        for field in FORBIDDEN_FIELDS:
            if field in meta:
                findings.append(f"{mid}: module.yaml carries {field} — "
                                f"review records are not package fields "
                                f"(they live in the core index or the "
                                f"installer's vetting log; decision, "
                                f"2026-11-21)")
        if meta.get("dir") != f"modules/{meta['_folder']}":
            findings.append(f"{mid}: module.yaml dir {meta.get('dir')!r} "
                            f"does not match its folder "
                            f"modules/{meta['_folder']}")
        if not (isinstance(mid, str) and mid.startswith(f"{library}/")
                and mid.count("/") == 1 and len(mid) > len(library) + 1):
            findings.append(f"{mid}: id is not a qualified "
                            f"{library}/<module> id")
        if interface is not None:
            compat = meta.get("kit_compat") or []
            if f"kit-{interface}" not in compat:
                findings.append(f"{mid}: kit_compat {compat} does not "
                                f"name kit-{interface}, the interface "
                                f"version the manifest declares — the "
                                f"wizard may not offer it")
        for dep in meta.get("depends_on") or []:
            if dep not in by_id and (not args.field
                                     or dep.startswith(f"{library}/")):
                findings.append(f"{mid}: depends_on names unknown "
                                f"module: {dep}")
        for deg in meta.get("degrades_without") or []:
            if "/" in deg and deg not in by_id and (not args.field
                    or deg.startswith(f"{library}/")):
                findings.append(f"{mid}: degrades_without names unknown "
                                f"module: {deg}")
        for dc in meta.get("data_classes") or []:
            if dc not in DATA_CLASSES:
                findings.append(f"{mid}: unknown data class: {dc}")
        for ac in meta.get("action_classes") or []:
            if ac not in ACTION_CLASSES:
                findings.append(f"{mid}: unknown action class: {ac}")
        declared = set()
        for entry in meta.get("files") or []:
            if not isinstance(entry, dict) or "path" not in entry \
                    or "class" not in entry:
                findings.append(f"{mid}: files entry is not a "
                                f"path/class pair: {entry!r}")
                continue
            declared.add(entry["path"])
            if entry["class"] not in FILE_CLASSES:
                findings.append(f"{mid}: file {entry['path']} has "
                                f"unknown class: {entry['class']}")
            rel = entry["path"]
            if os.path.isabs(rel) or ".." in rel.split("/"):
                findings.append(f"{mid}: declared file path escapes "
                                f"the module directory: {rel}")
                continue
            root = os.path.realpath(mdir)
            target = os.path.realpath(os.path.join(mdir, rel))
            if target != root and not target.startswith(root + os.sep):
                findings.append(f"{mid}: declared file path escapes "
                                f"the module directory: {rel} "
                                f"(resolves outside it)")
                continue
            if not os.path.isfile(os.path.join(mdir, rel)):
                findings.append(f"{mid}: declared file missing: {rel}")
        # The inverse direction: a file the package ships under
        # templates/ or tools/ (or as a top-level *.template.md)
        # that module.yaml never declares is counted by the audit
        # counter but invisible to the catalog.
        shipped = set()
        for sub in ("templates", "tools"):
            sdir = os.path.join(mdir, sub)
            if os.path.isdir(sdir):
                for dirpath, dirnames, filenames in os.walk(sdir):
                    dirnames[:] = [x for x in dirnames
                                   if x != "__pycache__"]
                    for f in filenames:
                        if f.endswith(".pyc"):
                            continue
                        shipped.add(os.path.relpath(
                            os.path.join(dirpath, f), mdir))
        if os.path.isdir(mdir):
            for f in os.listdir(mdir):
                if f.endswith(".template.md"):
                    shipped.add(f)
        for rel in sorted(shipped - declared):
            findings.append(f"{mid}: shipped file not declared in "
                            f"module.yaml files: {rel}")
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

    if not args.field:
        readme = open(os.path.join(repo, "README.md"),
                      encoding="utf-8").read()
        table_nums = sorted(set(re.findall(r"^\| (\d{2}) \|", readme,
                                           re.M)))
        disk_nums = sorted(d.split("-")[0] for d in on_disk)
        if table_nums != disk_nums:
            findings.append(f"README module table {table_nums} != "
                            f"module folders {disk_nums}")

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

    if not args.field:
        # Check 6: README figures == manifest / recomputed figures.
        readme_figs = {}
        for label, pat in (("starter", r"\*\*Starter\*\*"),
                           ("standard", r"\*\*Standard\*\*"),
                           ("everything", r"Everything")):
            m = re.search(pat + r"[^|\n]*\|[^|\n]*\|[^|\n]*~\s*([\d,]+)\s*words",
                          readme)
            if m:
                readme_figs[label] = int(m.group(1).replace(",", ""))
        stated_by_id = {p["id"]: int(p.get("audit_words", 0))
                        for p in profiles}
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

    # Check 7: the generated catalog is fresh, and the advisories
    # pair is honest (advisories.json exists exactly when its
    # source does, and its entries validate).
    import json as _json
    directory_path = os.path.join(repo, "directory.json")
    advisories_src = os.path.join(repo, "advisories.yaml")
    advisories_path = os.path.join(repo, "advisories.json")
    if os.path.isfile(advisories_src):
        try:
            adv_doc = module_yaml.parse_file(advisories_src)
            import build_directory as _bd
            for problem in _bd.validate_advisories(
                    adv_doc.get("advisories") or [],
                    set(by_id), library):
                findings.append(f"advisories.yaml: {problem}")
        except module_yaml.ModuleYamlError as exc:
            findings.append(f"advisories.yaml: {exc}")
    if not args.field and not os.path.isfile(directory_path):
        findings.append("directory.json is missing — the catalog is "
                        "generated from the module records, not "
                        "optional; regenerate it with "
                        "tools/build_directory.py and commit it")
    if os.path.isfile(directory_path):
        try:
            on_disk_dir = _json.load(open(directory_path,
                                          encoding="utf-8"))
            import build_directory as _bd
            fresh_dir, fresh_adv = _bd.build_payloads(
                repo, library, on_disk_dir.get("generated_from"))
            if _json.dumps(fresh_dir, sort_keys=True) != \
                    _json.dumps(on_disk_dir, sort_keys=True):
                findings.append("directory.json is stale — it differs "
                                "from what tools/build_directory.py "
                                "regenerates from the current records; "
                                "regenerate and commit it")
            gen = on_disk_dir.get("generated_from")
            if isinstance(gen, str) \
                    and re.fullmatch(r"[0-9a-f]{40}", gen) \
                    and os.path.exists(os.path.join(repo, ".git")):
                def _git(*argv):
                    try:
                        r = subprocess.run(["git", "-C", repo, *argv],
                                           capture_output=True,
                                           text=True, timeout=30)
                    except (OSError, subprocess.SubprocessError):
                        return None
                    return r.stdout if r.returncode == 0 else None

                if _git("rev-parse", "--verify", "--quiet",
                        gen + "^{commit}") is not None:
                    changed = _git("diff", "--name-only", gen, "HEAD",
                                   "--", "modules",
                                   "advisories.yaml") or ""
                    dirty = _git("status", "--porcelain", "--",
                                 "modules", "advisories.yaml") or ""
                    # One count per file: a file both changed
                    # since the pin and dirty in the worktree is
                    # still one record file.
                    paths = {l.strip() for l in changed.splitlines()
                             if l.strip()}
                    for l in dirty.splitlines():
                        if not l.strip():
                            continue
                        p = l[3:].strip()
                        if " -> " in p:
                            p = p.split(" -> ", 1)[1]
                        paths.add(p.strip('"'))
                    n = len(paths)
                    if n:
                        findings.append(
                            "module records changed after "
                            "directory.json's generated_from pin "
                            f"({gen[:7]}): {n} record file(s) "
                            "differ from the pinned commit — "
                            "regenerate the catalog so its pin "
                            "names the records it was built from")
            if os.path.isfile(advisories_src):
                if not os.path.isfile(advisories_path):
                    findings.append("advisories.yaml exists but "
                                    "advisories.json is missing — "
                                    "regenerate it")
                elif _json.dumps(fresh_adv, sort_keys=True) != \
                        _json.dumps(_json.load(open(
                            advisories_path, encoding="utf-8")),
                            sort_keys=True):
                    findings.append("advisories.json is stale — "
                                    "regenerate it with "
                                    "tools/build_directory.py")
            elif os.path.isfile(advisories_path):
                findings.append("advisories.json exists but "
                                "advisories.yaml does not — the "
                                "generator never fabricates a channel; "
                                "remove the generated file or add "
                                "the source")
        except Exception as exc:  # BuildError or bad JSON on disk
            findings.append(f"catalog freshness check failed: {exc}")
    elif os.path.isfile(advisories_path) and \
            not os.path.isfile(advisories_src):
        findings.append("advisories.json exists but advisories.yaml "
                        "does not — the generator never fabricates "
                        "a channel")

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
