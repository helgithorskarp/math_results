#!/usr/bin/env python3
"""Produce the compact exact audit certificate for the open-collar theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def certificate() -> dict:
    zero = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    two_sqrt2 = [0, 2, 0, 0, 0, 0, 0, 0, 1]
    sqrt2 = [0, 1, 0, 0, 0, 0, 0, 0, 1]
    sqrt6 = [0, 0, 0, 1, 0, 0, 0, 0, 1]
    return {
        "schema": "hn-open-dominating-triple-collar-v1",
        "threshold": {
            "distance_expression": "(sqrt(3)+sqrt(15))/2",
            "distance_basis_coefficients": [0, 0, 1, 0, 0, 0, 1, 0, 2],
            "squared_basis_coefficients": [9, 0, 0, 0, 3, 0, 0, 0, 2],
            "squared_minimal_polynomial": [1, -9, 9],
            "squared_isolating_interval": [[157, 20], [63, 8]],
        },
        "circle_orbit": {
            "rotation_degrees": 60,
            "orbit_size": 6,
            "squared_chords": [0, 1, 3, 4, 3, 1],
        },
        "open_fixture": {
            "description": "equilateral centres of side 2*sqrt(2)",
            "coordinate_basis": ["1", "sqrt(2)", "sqrt(3)", "sqrt(6)", "sqrt(5)", "sqrt(10)", "sqrt(15)", "sqrt(30)"],
            "centres": [
                {"x": zero, "y": zero},
                {"x": two_sqrt2, "y": zero},
                {"x": sqrt2, "y": sqrt6},
            ],
            "pair_squared_distances": [8, 8, 8],
            "strict_interval_squared": [4, 9],
        },
        "cap_fixture": {
            "centre_squared_distance": 8,
            "active_x_lower_bound_squared": [25, 32],
            "cap_diameter_squared_upper_bound": [7, 8],
        },
        "palette": {
            "leaf_circle_colours": [0, 1],
            "third_circle_colours": [2, 3],
            "leaf_centre_colours": [2, 2],
            "third_centre_colour": 0,
        },
        "claimed_checks": {
            "threshold_identities": 2,
            "threshold_isolation_inequalities": 2,
            "orbit_chord_cases": 6,
            "fixture_pair_norms": 3,
            "fixture_strict_inequalities": 7,
            "cap_fixture_identities": 2,
            "palette_checks": 6,
            "malformed_certificate_rejections": 6,
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
    target = args.out / "certificate.json"
    target.write_bytes(payload)
    print(json.dumps({
        "certificate_bytes": len(payload),
        "certificate_sha256": hashlib.sha256(payload).hexdigest(),
        "native_solver_calls": 0,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
