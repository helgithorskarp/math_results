#!/usr/bin/env python3
"""Replay selected complete radius-five SAT parents and compare flip sets."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


SAMPLES = (0, 39, 152, 327)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("enumerator", type=Path)
    args = parser.parse_args()
    enumerator = args.enumerator.resolve()
    assert enumerator.is_file()
    here = Path(__file__).resolve().parent
    artifact = here.parent / "ramsey_r55_catalog_edge_radius5_classification"
    catalog = artifact / "r55_42some.g6"
    expected_lines = {
        int(line.split()[0].split("=")[1]): line
        for line in (artifact / "EXPECTED_PARENT_COUNTS.txt").read_text(encoding="ascii").splitlines()
    }
    expected_flips: dict[int, set[tuple[str, ...]]] = {parent: set() for parent in SAMPLES}
    for line in (artifact / "EDGE_RADIUS5_MAP.tsv").read_text(encoding="ascii").splitlines()[1:]:
        if line.startswith("# SUMMARY "):
            break
        fields = line.split("\t")
        parent = int(fields[0])
        if parent in expected_flips:
            expected_flips[parent].add(tuple(fields[1:6]))

    results = {}
    for parent in SAMPLES:
        completed = subprocess.run(
            [str(enumerator), str(catalog), str(parent), "1"],
            check=True, capture_output=True, text=True,
        )
        diagnostics = completed.stderr.splitlines()
        values = dict(field.split("=", 1) for field in expected_lines[parent].split())
        assert diagnostics == [
            expected_lines[parent],
            f"SUMMARY start={parent} count=1 exact5={len(expected_flips[parent])} lower_models={values['lower_models']}",
        ]
        actual_flips = set()
        for line in completed.stdout.splitlines():
            fields = line.split("\t")
            assert len(fields) == 7 and int(fields[0]) == parent
            actual_flips.add(tuple(fields[1:6]))
        assert actual_flips == expected_flips[parent]
        results[str(parent)] = {
            "clauses": int(values["clauses"]),
            "exact5": int(values["exact5"]),
            "lower_models": int(values["lower_models"]),
            "ramsey_clauses": int(values["ramsey_clauses"]),
        }
    print(json.dumps({
        "all_sample_flip_sets_match": True,
        "enumerator_sha256": sha256(enumerator),
        "samples": results,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
