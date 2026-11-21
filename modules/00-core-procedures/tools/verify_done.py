#!/usr/bin/env python3
"""Verifier-gated done (Learn Harness Engineering + Harbor pattern).

Reads a feature_list.json, runs each pending feature's verifier command,
and ONLY this script flips status to "done" (on exit 0) or "failed".
The agent may read the file and work the features; it must not edit
status/verifier fields to claim completion. Hash of verifier fields is
recorded at creation; a changed verifier is flagged, not silently run.

Usage:
  verify_done.py init   <feature_list.json>   # stamp verifier_hash per feature
  verify_done.py check  <feature_list.json>   # run verifiers, flip status, print report
Exit code: 0 if every feature is done, 1 otherwise, 2 on tamper/usage error.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

def vhash(f):
    return hashlib.sha256(json.dumps(
        {"id": f["id"], "verifier": f["verifier"]}, sort_keys=True).encode()).hexdigest()[:16]

def load(p):
    return json.loads(Path(p).read_text())

def save(p, data):
    Path(p).write_text(json.dumps(data, indent=2) + "\n")

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("init", "check"):
        print(__doc__); return 2
    cmd, path = sys.argv[1], sys.argv[2]
    data = load(path)
    feats = data["features"]
    if cmd == "init":
        for f in feats:
            f.setdefault("status", "pending")
            f["verifier_hash"] = vhash(f)
        save(path, data); print(f"init: stamped {len(feats)} feature(s)"); return 0
    rc = 0
    for f in feats:
        if f.get("verifier_hash") != vhash(f):
            print(f"TAMPER {f['id']}: verifier changed since init — refusing to run"); rc = 2; continue
        if f.get("status") == "done":
            print(f"SKIP   {f['id']}: already done"); continue
        r = subprocess.run(f["verifier"], shell=True, capture_output=True, text=True, timeout=300,
                           cwd=str(Path(path).resolve().parent))
        f["status"] = "done" if r.returncode == 0 else "failed"
        f["last_verifier_output"] = (r.stdout + r.stderr).strip()[-500:]
        print(f"{'PASS' if r.returncode==0 else 'FAIL'}   {f['id']}: {f['title']}")
        if r.returncode != 0: rc = 1
    save(path, data)
    return rc if rc else (0 if all(f.get("status")=="done" for f in feats) else 1)

if __name__ == "__main__":
    sys.exit(main())
