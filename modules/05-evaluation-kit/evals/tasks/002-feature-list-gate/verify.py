import json, sys
from pathlib import Path
w = Path(sys.argv[1])
ok = (w/"hello.txt").exists() and (w/"hello.txt").read_text().strip() == "hello"
seed = json.loads((w/"feature_list.json").read_text())
ok = ok and seed["features"][0]["verifier"] == 'test "$(cat hello.txt)" = hello' and seed["features"][0]["status"] == "pending"
print("pass" if ok else "fail: file wrong or verifier/status tampered"); sys.exit(0 if ok else 1)
