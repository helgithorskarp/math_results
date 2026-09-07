#!/usr/bin/env python3
"""Verify compact evidence; full DRAT replay is documented separately."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def checked_output(command):
    run = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def main():
    entries = {}
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        entries[name] = digest
    for name, digest in entries.items():
        path = ROOT / name
        if not path.is_file() or file_hash(path) != digest:
            raise RuntimeError(f"source/evidence hash mismatch: {name}")

    expected_audit = json.loads((ROOT / "EXPECTED.json").read_text())
    expected_controls = json.loads((ROOT / "EXPECTED_CONTROLS.json").read_text())
    audits = []
    controls = []
    for optimized in (False, True):
        prefix = [sys.executable]
        if optimized:
            prefix.append("-O")
        controls.append(checked_output(prefix + ["-B", str(ROOT / "encoding_controls.py")]))
        audits.append(checked_output(prefix + ["-B", str(ROOT / "audit.py"), str(ROOT)]))
    if controls != [expected_controls, expected_controls]:
        raise RuntimeError("encoding-control mismatch")
    if audits != [expected_audit, expected_audit]:
        raise RuntimeError("independent-audit mismatch")
    result = json.loads((ROOT / "RESULT.json").read_text())
    if result["status"] != "VERIFIED_RANK4_ROW_TRIPLE_SUPPORT_5_8_EXCLUDED":
        raise RuntimeError("unexpected result status")
    print(json.dumps({
        "status": "VERIFIED_COMPACT_ROW_TRIPLE_SUPPORT_5_8_EXCLUSION",
        "files": len(entries),
        "audit": expected_audit,
        "controls": expected_controls,
        "result_sha256": file_hash(ROOT / "RESULT.json"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
