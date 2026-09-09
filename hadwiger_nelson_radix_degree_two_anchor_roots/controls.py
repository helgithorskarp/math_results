#!/usr/bin/env python3
"""Small positive and negative controls for the portable Sturm checker."""

from copy import deepcopy
import json
from pathlib import Path

import verify as V


HERE = Path(__file__).resolve().parent


def rejects(certificate):
    try:
        V.precheck(certificate)
    except ValueError:
        return True
    return False


def main():
    # Coefficients are in increasing order.
    V.need(V.real_root_count((-2, 1, 1)) == 2, "two simple real roots")
    V.need(V.real_root_count((1, 0, 1)) == 0, "no real roots")
    V.need(V.real_root_count((1, -2, 1)) == 1, "one repeated real root")
    V.need(
        V.canonical_coefficients(V.p_gcd((-1, 0, 1), (2, -3, 1))) == [-1, 1],
        "exact polynomial gcd",
    )
    certificate = json.loads((HERE / "certificate.json").read_text())
    changed = deepcopy(certificate)
    changed["summary"]["remaining_eligible_stabilizer_orbits"] += 1
    V.need(rejects(changed), "corrupt root-orbit count rejected")
    changed = deepcopy(certificate)
    changed["frontier_effect"]["remaining_global_pair_systems"] += 1
    V.need(rejects(changed), "corrupt frontier count rejected")
    print(
        json.dumps(
            {
                "passed": True,
                "controls": [
                    "two_simple_real_roots",
                    "no_real_roots",
                    "repeated_real_root_squarefree",
                    "exact_polynomial_gcd",
                    "corrupt_root_orbit_count_rejected",
                    "corrupt_frontier_count_rejected"
                ]
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
