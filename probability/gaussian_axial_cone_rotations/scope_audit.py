#!/usr/bin/env python3
"""Exact supplemental audits of PROOF Section 5.1; no new subclass search.

Default: deterministic JSON. --check: compare against EXPECTED_SCOPE.json.
Uses the original fixture pinned by its unchanged EXPECTED.json digest.
Author audit, not an independent reproduction or a universal numerical proof.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

from verify import determinant, dot, neg, norm2, rank, require


BASE = Path(__file__).resolve().parent
ORIGINAL = "50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4"


def run():
    fixture_bytes = (BASE / "EXPECTED.json").read_bytes()
    require(sha256(fixture_bytes).hexdigest() == ORIGINAL, "original fixture digest changed")
    fixture = json.loads(fixture_bytes)["fixture"]
    directions = [tuple(map(F, d)) for d in fixture["directions"]]
    p, q = F(fixture["p"]), F(fixture["q"])
    A = [(p * u, p * v, F(1)) for u, v in directions]
    B = [(q * u, q * v, F(1)) for u, v in directions]
    zero = (F(0),) * 3
    source = [zero] + A + [neg(b) for b in B]
    target = [zero] + A + B
    require(len(set(source)) == len(set(target)) == 25, "injective fixture changed")
    origin_slacks = [norm2(x) - norm2(y) for x, y in zip(source[1:], target[1:])]
    require(origin_slacks == [0] * 24, "a scalar constraint is not forced by zero slack")

    # Each row forces e.x - f.y = 0. A nonzero determinant makes even
    # nonzero unrestricted (e,f) impossible, hence excludes unit vectors.
    rows = [x + neg(y) for x, y in zip(source[1:], target[1:])]
    selected = [rows[i] for i in (0, 3, 6, 12, 15, 18)]
    minor = determinant(selected)
    require(rank(rows) == 6 and minor == -F(288, 25), "scalar-obstruction certificate failed")

    # A genuine positive control: identity endpoints preserve the scalar
    # e=f=(0,0,1), so the same zero-slack argument must not reject them.
    identity_rows = [x + neg(x) for x in source[1:]]
    control = (F(0), F(0), F(1)) * 2
    require(rank(identity_rows) == 3 and all(dot(row, control) == 0 for row in identity_rows),
            "identity control falsely rejected")

    denominator = 2 ** len(source) - 1
    weights = [F(2 ** i, denominator) for i in range(len(source))]
    require(sum(weights) == 1 and min(weights) > 0 and len(set(weights)) == 25,
            "distinct normalized weight certificate failed")
    return {
        "status": "AXIAL_CONE_SCOPE_AUDITS_PASS",
        "arithmetic": "integers and fractions.Fraction",
        "original_expected_sha256": ORIGINAL,
        "scalar_obstruction": {
            "zero_slack_origin_pairs": len(origin_slacks),
            "rank": rank(rows),
            "selected_labels_zero_based_with_origin": [1, 4, 7, 13, 16, 19],
            "minor_rows": [[str(x) for x in row] for row in selected],
            "minor_determinant": str(minor),
        },
        "identity_control": {"rank": rank(identity_rows), "unit_e_equals_f": [0, 0, 1]},
        "injective_weight_certificate": {
            "source_and_target_sites": 25,
            "common_denominator": denominator,
            "numerators": [2 ** i for i in range(25)],
            "sum": str(sum(weights)),
            "distinct_positive_weights": len(set(weights)),
        },
        "trust_boundary": "Matrix and weight audit only; analytic comparisons remain written proofs.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = (json.dumps(run(), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        require(output == (BASE / "EXPECTED_SCOPE.json").read_bytes(), "scope output mismatch")
        print("AXIAL_CONE_SCOPE_AUDITS_PASS " + sha256(output).hexdigest())
    else:
        print(output.decode(), end="")


if __name__ == "__main__":
    main()
