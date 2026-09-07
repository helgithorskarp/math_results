#!/usr/bin/env python3
"""Fresh deterministic replay of the all-row support-eight boundary."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
COVER = ROOT.parent / "ramsey_r55_rank4_complete_task_cover" / "row_cover.tsv"


def run(script: str, arguments: list[str]) -> subprocess.CompletedProcess:
    flags = ["-B"] if __debug__ else ["-B", "-O"]
    return subprocess.run([sys.executable] + flags + [str(ROOT / script)] + arguments,
                          text=True, capture_output=True, check=True)


def verify_manifest() -> None:
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        observed = sha256((ROOT / name).read_bytes()).hexdigest()
        if observed != expected:
            raise AssertionError((name, observed, expected))


def normalized_metadata(path: Path) -> dict:
    value = json.loads(path.read_text())
    value["formula"].pop("generation_seconds", None)
    return value


def main() -> None:
    verify_manifest()
    with tempfile.TemporaryDirectory(prefix="rank4-all-row-support8-") as temporary:
        work = Path(temporary)
        controls = work / "controls.json"
        run("controls.py", ["--cover", str(COVER), "--output", str(controls)])
        if controls.read_bytes() != (ROOT / "controls.json").read_bytes():
            raise AssertionError("control replay")

        cnf = work / "aggregate.cnf"
        metadata = work / "metadata.json"
        run("aggregate.py", ["--cover", str(COVER), "--cnf", str(cnf),
                             "--metadata", str(metadata)])
        if normalized_metadata(metadata) != normalized_metadata(ROOT / "metadata.json"):
            raise AssertionError("formula regeneration")

        audit = work / "audit.json"
        run("audit.py", ["--cover", str(COVER), "--cnf", str(cnf),
                         "--metadata", str(metadata), "--output", str(audit)])
        if audit.read_bytes() != (ROOT / "audit.json").read_bytes():
            raise AssertionError("independent audit replay")

        compact = run("compact_check.py", [str(ROOT), "--cover", str(COVER)])
        payload = json.loads(compact.stdout)
    payload["status"] = "VERIFIED_ALL_ROW_SUPPORT8_UNKNOWN_BOUNDARY"
    payload["files"] = len((ROOT / "SHA256SUMS").read_text().splitlines())
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
