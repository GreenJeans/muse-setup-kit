import sys
from pathlib import Path
t = (Path(sys.argv[1])/"MEMORY.md").read_text()
facts, _, sup = t.partition("## Superseded")
ok = "$12" in facts and "$10" not in facts and "$10" in sup and "2026-11-21" in sup
print("pass" if ok else "fail: current/superseded split wrong"); sys.exit(0 if ok else 1)
