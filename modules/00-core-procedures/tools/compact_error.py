#!/usr/bin/env python3
"""Error compaction (12-Factor Agents, Factor 9).

Turns a raw failure (log / traceback / tool output on stdin or a file)
into a bounded block fit to re-enter context on a retry:
  - the error line (for a Python traceback, the exception line at
    the end, not the "Traceback" header)
  - file:line references (deduped, max 10; both `path.py:12` and
    traceback `File "path.py", line 12` forms)
  - last 5 non-empty lines
  - sha256 of the original's raw bytes, and its line count (so the
    original stays addressable under the procedures ground-truth
    rule (§7) — compaction is a locator, never a replacement)

Usage: compact_error.py [file]   (reads stdin if no file)
Output: the compact block on stdout. Hard cap: 1200 characters,
including the trailing newline; when the block runs over, tail
lines are dropped earliest-first so the final lines, which usually
hold the real error, survive.
"""
import hashlib
import re
import sys
from pathlib import Path

MAX = 1200
raw = Path(sys.argv[1]).read_bytes() if len(sys.argv) > 1 else sys.stdin.buffer.read()
digest = hashlib.sha256(raw).hexdigest()[:12]
text = raw.decode(errors="replace")
lines = [l for l in text.splitlines() if l.strip()]
line_count = len(text.splitlines())

ERROR_RE = re.compile(r"(Error|Exception|FAIL|error:)")
if "Traceback (most recent call last):" in text:
    hits = [l.strip() for l in lines if ERROR_RE.search(l)]
    err = hits[-1] if hits else (lines[-1].strip() if lines else "no output")
else:
    err = next((l.strip() for l in lines if ERROR_RE.search(l)
                or "Traceback" in l),
               lines[0].strip() if lines else "no output")
refs = list(dict.fromkeys(
    re.findall(r"[\w./-]+\.[a-z]+:\d+", text)
    + [f"{p}:{n}" for p, n in
       re.findall(r'File "([\w./-]+)", line (\d+)', text)]))[:10]
tail = lines[-5:]

header = [f"ERROR-COMPACT sha256:{digest} lines:{line_count}",
          f"first-error: {err[:300]}"]
if refs:
    header.append("refs: " + ", ".join(refs))


def render(tail_lines):
    out = header + ["tail:"] + [f"  {l.strip()[:200]}" for l in tail_lines]
    return "\n".join(out)


block = render(tail)
while len(block) > MAX - 1 and len(tail) > 1:
    tail = tail[1:]
    block = render(tail)
print(block[:MAX - 1])
