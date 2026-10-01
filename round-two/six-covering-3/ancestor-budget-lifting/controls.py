"""Damaged mathematical application and pre-import source-pin controls."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lifting_checker", HERE / "check.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
data = json.loads((HERE / "application.json").read_text())
cases = []
d = deepcopy(data); d["beta"] = [108, 100]
cases.append(("wrong descendant domination factor", d))
d = deepcopy(data); d["absorbed_resources"] = [16, 15, 64]
cases.append(("wrong coupled resource identity", d))
d = deepcopy(data); d["root_anchors"][3][1] = 0
cases.append(("wrong ancestor known phase", d))
d = deepcopy(data); d["exact_eight_ancestor_count"] = 126
cases.append(("incomplete ancestor family", d))
d = deepcopy(data); d["orbit_factors"][0][0] = 0
cases.append(("plausible but false simultaneous orbit", d))
out = []
for name, damaged in cases:
    try:
        m.check(damaged)
    except ValueError as error:
        out.append({"case": name, "rejected": str(error)})
    else:
        raise ValueError("damaged input accepted: " + name)
with tempfile.TemporaryDirectory() as temporary:
    prior = Path(temporary)
    # Pins are validated before import, so this executable must not run.
    (prior / "check.py").write_text("raise RuntimeError('untrusted code executed')\n")
    try:
        m.check(data, prior_dir=prior)
    except ValueError as error:
        out.append({"case": "damaged prior executable before import", "rejected": str(error)})
    else:
        raise ValueError("damaged executable accepted")
print(json.dumps({"agent": "six-covering-3", "role": "researcher", "controls": out}))
