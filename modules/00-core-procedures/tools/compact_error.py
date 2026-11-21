#!/usr/bin/env python3
"""Error compaction (12-Factor Agents, Factor 9).

Turns a raw failure (log / traceback / tool output on stdin or a file)
into a bounded block fit to re-enter context on a retry:
  - error class + first meaningful line
  - file:line references (deduped, max 10)
  - last 5 non-empty lines
  - sha256 of the full original, and its line count (so the original
    stays addressable under the procedures ground-truth rule (§7) —
    compaction is a locator, never a replacement for the source)

Usage: compact_error.py [file]   (reads stdin if no file)
Output: the compact block on stdout. Hard cap: 1200 characters.
"""
import hashlib, re, sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(errors="replace") if len(sys.argv) > 1 else sys.stdin.read()
lines = [l for l in raw.splitlines() if l.strip()]
digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
err = next((l.strip() for l in lines if re.search(r"(Error|Exception|FAIL|Traceback|error:)", l)), lines[0].strip() if lines else "no output")
refs = list(dict.fromkeys(re.findall(r"[\w./-]+\.[a-z]+:\d+", raw)))[:10]
tail = lines[-5:]
out = [f"ERROR-COMPACT sha256:{digest} lines:{len(raw.splitlines())}",
       f"first-error: {err[:300]}"]
if refs: out.append("refs: " + ", ".join(refs))
out.append("tail:"); out += [f"  {l.strip()[:200]}" for l in tail]
print("\n".join(out)[:1200])
