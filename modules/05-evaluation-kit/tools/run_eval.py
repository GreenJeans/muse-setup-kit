#!/usr/bin/env python3
"""Minimal eval runner (Harbor pattern).

  run_eval.py [--evals-dir DIR] --oracle
      Verify each task: the verifier must FAIL on the untouched
      seed and PASS on the reference solution. A task with no
      solution/ is UNVERIFIED and fails the run — an oracle that
      cannot see a pass vouches for nothing. A verifier that
      crashes (traceback) is BAD, not a correct rejection.
  run_eval.py [--evals-dir DIR] --verify TASK WORKDIR [--variant V] [--trial N]
      Run one task's verifier against a finished work dir and
      record the trial in results/. Variant and trial identify
      the arm and repetition; the record carries both, and the
      filename is unique per run (existing records are never
      overwritten).

Full agent trials are driven by the agent in-session (spawn the
agent in a fresh copy of seed/, then --verify). This script owns
the deterministic half: oracle sanity, scoring, per-trial records.

--evals-dir defaults to the evals/ folder beside this file's
module. Set it when the runner is copied into a shared workspace
tools folder, so it still finds its tasks and results.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path


def verify(task: Path, work: Path):
    r = subprocess.run([sys.executable, str(task / "verify.py"), str(work)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def oracle(tasks: Path) -> int:
    ok = True
    for task in sorted(tasks.iterdir()):
        if not (task / "verify.py").exists():
            continue
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "w"
            seed = task / "seed"
            if seed.exists():
                shutil.copytree(seed, work)
            else:
                work.mkdir()
            r_seed, out_seed = verify(task, work)
            if "Traceback" in out_seed:
                print(f"BAD  {task.name}: verifier crashed on the seed")
                ok = False
                continue
            sol = task / "solution"
            if not sol.exists():
                print(f"UNVERIFIED {task.name}: no solution/ — the oracle "
                      "cannot confirm a pass")
                ok = False
                continue
            work2 = Path(td) / "s"
            shutil.copytree(sol, work2)
            r_sol, out_sol = verify(task, work2)
            if "Traceback" in out_sol:
                print(f"BAD  {task.name}: verifier crashed on the solution")
                ok = False
                continue
            good = r_seed != 0 and r_sol == 0
            ok &= good
            print(f"{'OK  ' if good else 'BAD '} {task.name}: "
                  f"seed_rc={r_seed} solution_rc={r_sol}")
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--evals-dir", type=Path,
                    default=Path(__file__).parent.parent / "evals")
    ap.add_argument("--oracle", action="store_true")
    ap.add_argument("--verify", nargs=2, metavar=("TASK", "WORKDIR"))
    ap.add_argument("--variant")
    ap.add_argument("--trial")
    args = ap.parse_args(argv[1:])
    tasks = args.evals_dir / "tasks"
    if args.oracle:
        return oracle(tasks)
    if args.verify:
        name, workdir = args.verify
        rc, _ = verify(tasks / name, Path(workdir))
        rec = {"task": name, "work": workdir,
               "reward": 1 if rc == 0 else 0, "ts": int(time.time())}
        if args.variant:
            rec["variant"] = args.variant
        if args.trial:
            rec["trial"] = args.trial
        out = args.evals_dir / "results"
        out.mkdir(exist_ok=True)
        fname = f"{rec['ts']}-{name}-{uuid.uuid4().hex[:6]}.json"
        with open(out / fname, "x") as fh:
            json.dump(rec, fh, indent=2)
        print(json.dumps(rec))
        return rc
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
