#!/usr/bin/env python3
"""Verifier-gated done for a feature_list.json.

The agent works the list but never edits a feature's `status` or
`verifier` fields. This script is the only thing that sets them:

  init <list> [--force]
      Stamp each feature with a hash of its verifier. Refuses if
      any feature already carries a hash: re-stamping would bless
      a changed verifier, so it is the user's call, via --force,
      never a routine step.
  check <list> [--timeout N]
      First a pre-pass: a feature with no hash is reported NOT
      INITIALIZED and one whose verifier no longer matches its
      hash is reported TAMPER; if either occurs, nothing runs,
      nothing is saved, exit 2. Otherwise every feature's verifier
      runs, including features already marked done — a record
      cannot sit on a flip the gate never made, and a done whose
      verifier now fails flips back to failed. Exit 0 when every
      verifier passes, 1 when any fails or times out.

Verifier commands run through the system shell from the feature
list's own directory, so a list behaves the same from any working
directory. The hash detects a changed verifier; it does not make
the file proof against an agent willing to forge its own record —
the agent holds write access. What the gate guarantees is that a
status the gate set was set by a verifier run, and that check
re-runs those verifiers rather than trusting the file.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def vhash(feature):
    payload = json.dumps(
        {"id": feature["id"], "verifier": feature["verifier"]},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def load(path):
    return json.loads(Path(path).read_text())


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def cmd_init(path, force):
    data = load(path)
    stamped = [f["id"] for f in data["features"] if f.get("verifier_hash")]
    if stamped and not force:
        print(f"REFUSED: already initialized ({', '.join(stamped)}). "
              "Re-stamping blesses any verifier change since the first "
              "init; if that is intended, re-run with --force.")
        return 2
    for f in data["features"]:
        f.setdefault("status", "pending")
        f["verifier_hash"] = vhash(f)
    save(path, data)
    print(f"init: stamped {len(data['features'])} feature(s)")
    return 0


def cmd_check(path, timeout):
    data = load(path)
    problems = []
    for f in data["features"]:
        if not f.get("verifier_hash"):
            problems.append(f"NOT INITIALIZED {f['id']}: run init first")
        elif f["verifier_hash"] != vhash(f):
            problems.append(f"TAMPER {f['id']}: verifier changed since init"
                            " — refusing to run")
    if problems:
        print("\n".join(problems))
        return 2
    rc = 0
    workdir = Path(path).resolve().parent
    for f in data["features"]:
        try:
            r = subprocess.run(f["verifier"], shell=True, cwd=workdir,
                               capture_output=True, text=True,
                               timeout=timeout)
            out = (r.stdout + r.stderr).strip()
            passed = r.returncode == 0
        except subprocess.TimeoutExpired:
            out = f"timeout after {timeout}s"
            passed = False
        f["status"] = "done" if passed else "failed"
        f["last_verifier_output"] = out[-500:]
        print(f"{'PASS' if passed else 'FAIL'} {f['id']}: {out[-200:]}")
        if not passed:
            rc = 1
    save(path, data)
    return rc


def main(argv):
    if len(argv) < 3 or argv[1] not in ("init", "check"):
        print(__doc__)
        return 2
    cmd, path = argv[1], argv[2]
    rest = argv[3:]
    if cmd == "init":
        return cmd_init(path, "--force" in rest)
    timeout = 300
    if "--timeout" in rest:
        timeout = int(rest[rest.index("--timeout") + 1])
    return cmd_check(path, timeout)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
