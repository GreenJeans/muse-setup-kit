import sys
from pathlib import Path
pairs = []
for line in (Path(sys.argv[1]) / "config.txt").read_text().splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        pairs.append((k.strip(), v.strip()))
keys = [k for k, _ in pairs]
vals = dict(pairs)
# Exact key set, port exactly once: keeping the old port line and
# adding a second one, or adding unrelated keys, is a fail — the
# instruction says change the port and nothing else.
ok = (sorted(keys) == ["host", "mode", "port"]
      and vals.get("port") == "8080"
      and vals.get("host") == "localhost"
      and vals.get("mode") == "dev")
print("pass" if ok else "fail: config keys or values wrong")
sys.exit(0 if ok else 1)
