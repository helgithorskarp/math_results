#!/usr/bin/env python3
"""Verify the v1.0.1 manifest and rerun its recorded 47 commands on POSIX."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(root: Path) -> int:
    manifest = root / "MANIFEST_SHA256.txt"
    count = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(" *", 1)
        target = root / relative.replace("\\", "/")
        assert target.is_file(), target
        assert digest(target).lower() == expected.lower(), target
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_root", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    root = args.archive_root.resolve()
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=True)

    manifest_entries = verify_manifest(root)
    reference = json.loads(
        (root / "verification/reference-pre-alternating/run_summary.json").read_text(
            encoding="utf-8"
        )
    )
    results = []
    for number, row in enumerate(reference["runs"], 1):
        source = root / row["source"]
        executable = "node" if source.suffix == ".js" else sys.executable
        arguments = list(row.get("arguments", []))
        if "--json" in arguments:
            arguments[arguments.index("--json") + 1] = str(
                output / f"generated-{number:02d}.json"
            )
        started = time.monotonic()
        completed = subprocess.run(
            [executable, str(source), *arguments], text=True, capture_output=True
        )
        elapsed_ms = round((time.monotonic() - started) * 1000)
        log = output / f"{number:02d}-{source.name}.txt"
        log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
        result = {
            "number": number,
            "source": row["source"],
            "sha256": digest(source),
            "arguments": arguments,
            "exitCode": completed.returncode,
            "runtimeMilliseconds": elapsed_ms,
            "stdout": str(log),
        }
        results.append(result)
        print(
            f"{number:02d}/{reference['runCount']} exit={completed.returncode} "
            f"ms={elapsed_ms} {row['source']}",
            flush=True,
        )
        if completed.returncode:
            break

    all_passed = len(results) == reference["runCount"] and all(
        row["exitCode"] == 0 for row in results
    )
    summary = {
        "manifestEntries": manifest_entries,
        "referenceRunCount": reference["runCount"],
        "actualRunCount": len(results),
        "allPassed": all_passed,
        "pythonVersion": sys.version,
        "nodeVersion": subprocess.check_output(
            ["node", "--version"], text=True
        ).strip(),
        "runs": results,
    }
    (output / "run_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Manifest entries verified: {manifest_entries}")
    print(f"All recorded runs passed: {all_passed}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
