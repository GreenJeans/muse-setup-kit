import re
import sys
from pathlib import Path
t = (Path(sys.argv[1]) / "MEMORY.md").read_text()
facts, _, sup = t.partition("## Superseded")
# The superseded entry must carry the full provenance the instruction
# requires — superseded-by, a date, and a source — not just the old
# value and a date somewhere in the section.
entry = any("$10" in line and "superseded-by" in line
            and re.search(r"\d{4}-\d{2}-\d{2}", line) and "source" in line
            for line in sup.splitlines())
ok = "$12" in facts and "$10" not in facts and entry
print("pass" if ok else "fail: current/superseded split or provenance wrong")
sys.exit(0 if ok else 1)
