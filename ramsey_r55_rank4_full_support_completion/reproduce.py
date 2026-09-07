#!/usr/bin/env python3
"""Fast compact-evidence reproduction; full DRAT replay is documented separately."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    expected_files = {}
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected_files[name] = digest
    for name, digest in expected_files.items():
        path = ROOT / name
        if not path.is_file() or file_hash(path) != digest:
            raise RuntimeError(f"source/evidence hash mismatch: {name}")
    expected = json.loads((ROOT / "EXPECTED.json").read_text(encoding="utf-8"))
    outputs = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command += ["-B", str(ROOT / "audit.py"), str(ROOT)]
        run = subprocess.run(command, capture_output=True, text=True, check=True)
        result = json.loads(run.stdout)
        if result != expected:
            raise RuntimeError(f"audit mismatch optimized={optimized}")
        outputs.append(result)
    if outputs[0] != outputs[1]:
        raise RuntimeError("normal and optimized audits differ")
    result = json.loads((ROOT / "RESULT.json").read_text(encoding="utf-8"))
    if result["status"] != "VERIFIED_NONAFFINE_FULL_SUPPORT_RANK4_REMAINDER_EXCLUDED":
        raise RuntimeError("unexpected result status")
    print(json.dumps({
        "status": "VERIFIED_COMPACT_FULL_SUPPORT_RANK4_EXCLUSION",
        "files": len(expected_files),
        "audit": expected,
        "result_sha256": file_hash(ROOT / "RESULT.json"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
