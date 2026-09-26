#!/usr/bin/env python3
"""Damage controls for the face certificate; works under python -O."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent


def main():
    cert = json.loads((HERE / "CERTIFICATE.json").read_text())
    controls = []
    c = deepcopy(cert)
    c["maximal_face_masks"].pop()
    controls.append(("missing_face", c, "check_matroid.py"))
    c = deepcopy(cert)
    c["maximal_face_masks"][0] ^= 1
    controls.append(("changed_face", c, "check_matroid.py"))
    c = deepcopy(cert)
    c["A_sections"][0]["normal_p"][0] = "99"
    controls.append(("false_symbolic_normal", c, "certify.py"))
    c = deepcopy(cert)
    c["constant_checks"]["claimed_full_gap_lower"] = "1"
    controls.append(("false_margin", c, "certify.py"))
    with TemporaryDirectory(prefix="rank_face_controls_") as tmp:
        for name, damaged, script in controls:
            path = Path(tmp) / (name + ".json")
            path.write_text(json.dumps(damaged))
            command = [sys.executable]
            if sys.flags.optimize:
                command.append("-O")
            command.append(str(HERE / script))
            if script == "certify.py":
                command.append("--certificate")
            command.append(str(path))
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 or "ValueError" not in result.stderr:
                raise ValueError("damage control did not fail as expected: " + name)
    print(json.dumps({"damage_controls_rejected": [r[0] for r in controls], "status": "PASS"}))


if __name__ == "__main__":
    main()
