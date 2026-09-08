#!/usr/bin/env python3
"""Verify the transitive(44) certificate and its Cayley(44) dependency."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / "ramsey_r55_cayley44_puncture_obstruction"


def run(cwd, *arguments):
    process = subprocess.run([sys.executable, "-B", *map(str, arguments)],
                             cwd=cwd, text=True, capture_output=True)
    if process.returncode:
        raise RuntimeError((arguments, process.returncode,
                            process.stdout, process.stderr))
    return process.stdout


def check_manifest():
    for row in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, relative = row.split("  ", 1)
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError((relative, expected, actual))


def main():
    cayley = run(PARENT, PARENT / "reproduce.py")
    if cayley.strip() != "REPRODUCED_COMPLETE_CAYLEY44_PUNCTURE_EXCLUSION":
        raise AssertionError("Cayley(44) dependency")
    with tempfile.TemporaryDirectory() as temporary:
        report_path = Path(temporary) / "verification.json"
        report = json.loads(run(
            ROOT, ROOT / "verify.py", "--catalog", ROOT / "catalog.txt",
            "--certificates", ROOT / "certificates.json",
            "--report", report_path))
        if report != json.loads(report_path.read_text()):
            raise AssertionError("verification report mismatch")
    report.pop("elapsed_seconds")
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    if report != expected["verification"]:
        raise AssertionError(("semantic verification", report,
                              expected["verification"]))
    controls = json.loads(run(ROOT, ROOT / "controls.py"))
    if controls != expected["controls"]:
        raise AssertionError(("controls", controls, expected["controls"]))
    check_manifest()
    print("REPRODUCED_COMPLETE_VERTEX_TRANSITIVE44_PUNCTURE_EXCLUSION")


if __name__ == "__main__":
    main()
