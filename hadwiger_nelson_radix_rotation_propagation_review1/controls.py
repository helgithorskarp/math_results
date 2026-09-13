#!/usr/bin/env python3
"""Four inexpensive rejection controls for the independent audit."""

import argparse
import copy
import json
import tempfile
from pathlib import Path

import independent_audit as A


def expect_failure(label, phrase, action):
    try:
        action()
    except ValueError as error:
        A.need(phrase in str(error), f"{label} reached its intended check")
        return label
    raise ValueError(f"accepted invalid control: {label}")


def run(frontier, incidence):
    factors, circle, monomials, rowids, signatures, buckets = A.reconstruct_inventory()
    group = A.d3_group(factors, rowids)
    rejected = []
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)

        rotation = json.loads((A.ROTATION / "certificate.json").read_text())
        bad = copy.deepcopy(rotation)
        bad["pair_rows"].pop()
        path = directory / "rotation-missing-row.json"
        path.write_text(json.dumps(bad))
        rejected.append(expect_failure(
            "omitted h4193 pair system", "four h4193 rows",
            lambda: A.audit_h4193(factors, circle, monomials, rowids, group, path),
        ))

        bad = copy.deepcopy(rotation)
        bad["expanded_pair_exclusions"].pop()
        path = directory / "rotation-missing-image.json"
        path.write_text(json.dumps(bad))
        rejected.append(expect_failure(
            "omitted h4193 D3 image", "expanded-pair list",
            lambda: A.audit_h4193(factors, circle, monomials, rowids, group, path),
        ))

        source = json.loads(Path(frontier).read_text())
        source["reflection_and_rotation_pair_exclusions"].pop()
        path = directory / "propagation-missing-input-pair.json"
        path.write_text(json.dumps(source))
        rejected.append(expect_failure(
            "altered h4195 source interface", "fresh h4193 residual interface",
            lambda: A.audit_h4195(
                factors, rowids, signatures, buckets, group, path, incidence,
            ),
        ))

        propagation = json.loads((A.PROPAGATION / "certificate.json").read_text())
        propagation["pencil_catalogue_sha256"] = "0" * 64
        path = directory / "propagation-false-catalogue.json"
        path.write_text(json.dumps(propagation))
        rejected.append(expect_failure(
            "false h4195 pencil catalogue", "entrywise pencil catalogue",
            lambda: A.audit_h4195(
                factors, rowids, signatures, buckets, group, frontier, incidence, path,
            ),
        ))

    return {"verified": True, "assertions_used_for_correctness": False, "rejected": rejected}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--incidence", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.frontier, args.incidence)
    if args.check_expected:
        A.need(
            result == json.loads((A.HERE / "EXPECTED_CONTROLS.json").read_text()),
            "expected control result",
        )
    print(json.dumps(result, indent=2, sort_keys=True))
