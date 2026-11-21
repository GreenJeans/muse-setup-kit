import sys
from pathlib import Path
t = (Path(sys.argv[1])/"config.txt").read_text()
ok = "port=8080" in t and "host=localhost" in t and "mode=dev" in t
print("pass" if ok else "fail"); sys.exit(0 if ok else 1)
