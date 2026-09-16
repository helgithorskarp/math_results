#!/usr/bin/env python3
"""Negative controls for the exact odd21 geodesic-unitization checker."""

import copy
import json
from pathlib import Path

from verify import verify


HERE = Path(__file__).resolve().parent


def rejected(value):
    try:
        verify(value)
    except (AssertionError, KeyError, TypeError, ValueError):
        return True
    return False


def main():
    original = json.loads((HERE / "certificate.json").read_text())
    cases = []

    bad = copy.deepcopy(original)
    bad["physical_points"] += 1
    cases.append(bad)

    bad = copy.deepcopy(original)
    bad["three_colouring"] = "0" * len(bad["three_colouring"])
    cases.append(bad)

    bad = copy.deepcopy(original)
    bad["equality_witnesses"].pop()
    cases.append(bad)

    bad = copy.deepcopy(original)
    record = bad["equality_witnesses"][0]
    u, v, _ = record["source_edge"]
    j = bad["source_indices"][v]
    replacement = str((int(record["colouring"][bad["source_indices"][u]]) + 1) % 3)
    record["colouring"] = record["colouring"][:j] + replacement + record["colouring"][j+1:]
    cases.append(bad)

    bad = copy.deepcopy(original)
    bad["edges_sha256"] = "0" * 64
    cases.append(bad)

    if not all(rejected(case) for case in cases):
        raise RuntimeError("a deliberate corruption was accepted")
    print(json.dumps({"corruptions_rejected": len(cases), "controls_passed": True},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
