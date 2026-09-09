#!/usr/bin/env python3
"""Positive and negative controls for the exact D3 certificate."""
from copy import deepcopy
from pathlib import Path
import json
import verify as V

HERE = Path(__file__).resolve().parent


def rejected(certificate, actual):
    try:
        V.check_certificate(certificate, actual)
    except ValueError:
        return True
    return False


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    actual = V.actual_certificate()
    V.check_certificate(certificate, actual)
    corruptions = []

    wrong = deepcopy(certificate)
    wrong["curves"]["rotation_permutation_sha256"] = "0" * 64
    V.need(rejected(wrong, actual), "wrong curve action accepted")
    corruptions.append("wrong curve rotation permutation hash")

    wrong = deepcopy(certificate)
    wrong["pairs"]["representatives_sha256"] = "0" * 64
    V.need(rejected(wrong, actual), "wrong pair representatives accepted")
    corruptions.append("wrong pair representative hash")

    wrong = deepcopy(certificate)
    wrong["pairs"]["orbits"] -= 1
    V.need(rejected(wrong, actual), "missing pair orbit accepted")
    corruptions.append("missing pair orbit")

    wrong = deepcopy(certificate)
    wrong["collisions"]["parameter_orbit_degree_bound"] -= 1
    V.need(rejected(wrong, actual), "wrong collision bound accepted")
    corruptions.append("wrong collision orbit degree bound")

    wrong = deepcopy(certificate)
    wrong["parameter_action"]["fundamental_chamber"] = "x>=0 and y>=0"
    V.need(rejected(wrong, actual), "wrong chamber accepted")
    corruptions.append("incomplete fundamental chamber")

    print(
        json.dumps(
            {
                "status": "CONTROLS_PASSED",
                "positive_certificate_replay": True,
                "curve_polynomial_substitution_checks": actual["curves"]["objects"] * 2,
                "collision_coefficient_action_checks": actual["collisions"]["objects"] * 2,
                "D3_relation_checks": 6,
                "digit_triangle_isometry_checks": 6,
                "rejected_corruptions": corruptions,
                "CAS_calls": 0,
                "solver_calls": 0,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
