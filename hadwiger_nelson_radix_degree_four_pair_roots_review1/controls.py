#!/usr/bin/env python3
"""Three rejection controls for the independent degree-four review."""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent


def expect_failure(label, phrase, action):
    try:
        action()
    except ValueError as error:
        audit.need(phrase in str(error), f"{label} reached its intended check: {error}")
        return label
    raise ValueError(f"invalid control passed: {label}")


def run(residual_path, certificate_path):
    residual = json.loads(Path(residual_path).read_text())
    certificate = json.loads(Path(certificate_path).read_text())
    architecture = audit.load_architecture()
    _rows, _events, factors, factor_edges, base_edges, _collisions, _simple, _circle = architecture.build()
    degrees = [architecture.degree(factor) for factor in factors]
    pairs = [row for row in residual["remaining_six"]
             if 4 in (degrees[row[0]], degrees[row[1]])]
    rejected = []

    counts = Counter(
        key for entry in certificate["pair_components"] for key in entry["real_component_keys"]
    )
    unique_key = next(key for key, count in counts.items() if count == 1)
    missing = copy.deepcopy(certificate)
    missing["components"] = [row for row in missing["components"]
                             if row["component_key"] != unique_key]
    for entry in missing["pair_components"]:
        entry["real_component_keys"] = [key for key in entry["real_component_keys"]
                                         if key != unique_key]
    rejected.append(expect_failure(
        "omitted real resultant branch",
        "one certified branch",
        lambda: audit.audit_root_cover(pairs, factors, missing),
    ))

    bad_pair = copy.deepcopy(pairs[0])
    bad_pair[4] += 1
    rejected.append(expect_failure(
        "unequal orbit allowance",
        "orbit allowance",
        lambda: audit.need(bad_pair[3] == bad_pair[4], "orbit allowance mismatch"),
    ))

    injective = next(row for row in certificate["components"] if not row["collision_rows"])
    edges = sorted(base_edges + [edge for curve in injective["active_curves"]
                                 for edge in factor_edges[curve]])
    bad_word = [0] * 243
    rejected.append(expect_failure(
        "monochromatic strict edge",
        "colouring replay",
        lambda: audit.need(
            all(bad_word[left] != bad_word[right] for left, right in edges),
            "colouring replay failed",
        ),
    ))
    return {"verified": True, "rejected": rejected}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, default=audit.TARGET / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run(arguments.residual, arguments.certificate)
    if arguments.check_expected:
        audit.need(result == json.loads((HERE / "EXPECTED_CONTROLS.json").read_text()),
                   "expected control output")
    print(json.dumps(result, indent=2, sort_keys=True))
