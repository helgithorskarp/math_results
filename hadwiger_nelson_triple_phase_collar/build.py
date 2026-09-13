#!/usr/bin/env python3
"""Build the compact exact certificate for the triple-phase collar."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def certificate() -> dict:
    z = [0, 0, 0, 0, 1]
    one = [1, 0, 0, 0, 1]
    sqrt3 = [0, 1, 0, 0, 1]
    d0 = [1, 1, 0, 0, 1]
    return {
        "schema": "hn-triple-phase-collar-v1",
        "basis": ["1", "sqrt(3)", "sqrt(5)", "sqrt(15)"],
        "threshold": {
            "distance_expression": "1+sqrt(3)",
            "distance": d0,
            "squared": [4, 2, 0, 0, 1],
            "minimal_polynomial": [1, -2, -2],
            "isolating_interval": [[683, 250], [2733, 1000]],
        },
        "monotonicity": {
            "domain_lower_bound_for_x": 7,
            "threshold_squared_minus_seven": [-3, 2, 0, 0, 1],
            "ab_minus_half_numerator": [-9, -4, 1],
            "ab_minus_half_denominator": "8*x",
            "cosine_gap_numerator": [63, -30, 3],
            "cosine_gap_denominator": "16*x",
            "cosine_gap_factorization": {
                "scalar": 3,
                "factors": [[-3, 1], [-7, 1]],
            },
        },
        "circle_orbit": {
            "rotation_degrees": 60,
            "orbit_size": 6,
            "squared_chords": [0, 1, 3, 4, 3, 1],
        },
        "interior_fixture": {
            "description": "equilateral centres of side 11/4",
            "centres": [
                {"x": z, "y": z},
                {"x": [11, 0, 0, 0, 4], "y": z},
                {"x": [11, 0, 0, 0, 8], "y": [0, 11, 0, 0, 8]},
            ],
            "pair_squared_distances": [[121, 16], [121, 16], [121, 16]],
            "strict_side_interval": [2, 3],
        },
        "cross_triple_fixture": {
            "centre_separation": [11, 4],
            "directions": [
                {"x": [7, 0, 0, 0, 8], "y": [0, 0, 0, 1, 8]},
                {"x": [7, 0, 0, 0, 8], "y": [0, 0, 0, -1, 8]},
                {"x": one, "y": z},
            ],
            "sum": {"x": [11, 0, 0, 0, 4], "y": z},
            "product": {"x": one, "y": z},
        },
        "sharp_triangle": {
            "centre_separation": d0,
            "first_centre": {"x": z, "y": z},
            "second_centre": {"x": d0, "y": z},
            "points": [
                {"x": [0, 1, 0, 0, 2], "y": [-1, 0, 0, 0, 2]},
                {"x": [0, 1, 0, 0, 2], "y": [1, 0, 0, 0, 2]},
                {"x": sqrt3, "y": z},
            ],
            "owners": ["first", "first", "second"],
            "pair_squared_distances": [1, 1, 1],
        },
        "palette": {
            "paired_circle_colours": [0, 1],
            "third_circle_colours": [2, 3],
            "paired_centre_colours": [2, 2],
            "third_centre_colour": 0,
        },
        "claimed_checks": {
            "threshold_identities": 3,
            "threshold_isolation_inequalities": 2,
            "monotonicity_checks": 5,
            "orbit_chord_cases": 6,
            "fixture_pair_norms": 3,
            "fixture_strict_inequalities": 9,
            "cross_triple_checks": 10,
            "sharp_triangle_checks": 7,
            "palette_checks": 6,
            "malformed_certificate_rejections": 8,
            "native_solver_calls": 0,
        },
    }


def encode(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    payload = encode(certificate())
    (args.out / "certificate.json").write_bytes(payload)
    print(json.dumps({
        "certificate_bytes": len(payload),
        "certificate_sha256": hashlib.sha256(payload).hexdigest(),
        "native_solver_calls": 0,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
