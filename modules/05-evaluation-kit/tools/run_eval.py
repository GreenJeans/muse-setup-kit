#!/usr/bin/env python3
"""Minimal eval runner (Harbor pattern).

  run_eval.py --oracle           # verify each task fails on seed, passes on solution/ if present
  run_eval.py --verify TASK WORKDIR   # run one task's verifier against a finished work dir

Full agent trials are driven by the agent in-session (spawn the agent in a
fresh copy of seed/, then --verify). This script owns the deterministic
half: oracle sanity + scoring + the per-trial record in evals/results/.
"""
import json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

TASKS = Path(__file__).parent.parent / "evals" / "tasks"

def verify(task: Path, work: Path) -> int:
    return subprocess.run([sys.executable, str(task / "verify.py"), str(work)],
                          capture_output=True, text=True).returncode

def oracle():
    ok = True
    for task in sorted(TASKS.iterdir()):
        if not (task / "verify.py").exists(): continue
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "w"; seed = task / "seed"
            shutil.copytree(seed, work) if seed.exists() else work.mkdir()
            r_seed = verify(task, work)
            sol = task / "solution"
            r_sol = None
            if sol.exists():
                work2 = Path(td) / "s"; shutil.copytree(sol, work2); r_sol = verify(task, work2)
            good = r_seed != 0 and (r_sol in (0, None))
            ok &= good
            print(f"{'OK  ' if good else 'BAD '} {task.name}: seed_rc={r_seed} solution_rc={r_sol}")
    return 0 if ok else 1

if __name__ == "__main__":
    if sys.argv[1:] == ["--oracle"]:
        sys.exit(oracle())
    if len(sys.argv) == 4 and sys.argv[1] == "--verify":
        task, work = TASKS / sys.argv[2], Path(sys.argv[3])
        rc = verify(task, work)
        rec = {"task": sys.argv[2], "work": str(work), "reward": 1 if rc == 0 else 0, "ts": int(time.time())}
        out = Path(__file__).parent.parent / "evals" / "results"; out.mkdir(exist_ok=True)
        (out / f"{rec['ts']}-{rec['task']}.json").write_text(json.dumps(rec, indent=2))
        print(json.dumps(rec)); sys.exit(rc)
    print(__doc__); sys.exit(2)
