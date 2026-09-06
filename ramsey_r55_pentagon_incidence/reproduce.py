#!/usr/bin/env python3
"""Regenerate, check both packages and compare exact compact results."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def run(script, args=(), optimized=False):
    command = [sys.executable, "-B"] + (["-O"] if optimized else [])
    result = subprocess.run(command + [str(script), *map(str, args)],
                            check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def reproduce():
    # These exact file bytes pin the sole mathematical input from the
    # preceding contribution. Its ordinary proof remains a trust boundary.
    dep = json.loads((HERE / "dependency.json").read_text())
    source = HERE.parent / dep["directory"]
    for name, digest in dep["files"].items():
        require(hashlib.sha256((source / name).read_bytes()).hexdigest() == digest,
                "dependency mismatch: " + name)
    previous = run(source / "reproduce.py")
    require(previous["status"] == "REPRODUCED_INDUCED_PENTAGON_FORCING",
            "zero-pentagon dependency replay")
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "certificate.json"
        run(HERE / "build.py", [output])
        require(output.read_bytes() == (HERE / "certificate.json").read_bytes(),
                "certificate regeneration mismatch")
    for optimized in (False, True):
        require(run(HERE / "check.py", [HERE / "certificate.json"], optimized) ==
                json.loads((HERE / "expected.json").read_text()), "coverage mismatch")
        require(run(HERE / "controls.py", optimized=optimized) ==
                json.loads((HERE / "controls_expected.json").read_text()), "control mismatch")
    return {"status": "REPRODUCED_GLOBAL_PENTAGON_INCIDENCE",
            "certificate_sha256": hashlib.sha256((HERE / "certificate.json").read_bytes()).hexdigest(),
            "normalized_unique_pentagon_cases": 258048,
            "second_pentagon_certificates": 1794,
            "global43_seven_set_lower_bound": 906,
            "global43_pentagon_lower_bound": 18,
            "new_R55_bound": False}


if __name__ == "__main__":
    print(json.dumps(reproduce(), sort_keys=True))
