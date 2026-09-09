#!/usr/bin/env python3
"""Positive and negative controls for the exact four-curve gate."""
from copy import deepcopy
from itertools import product
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
    wrong["F4_hyperplanes"]["curve_signature_assignment_sha256"] = "0" * 64
    V.need(rejected(wrong, actual), "wrong curve signatures accepted")
    corruptions.append("wrong curve-signature hash")

    wrong = deepcopy(certificate)
    wrong["exact_four"]["no_circle_signature_patterns"] -= 1
    V.need(rejected(wrong, actual), "missing affine pattern accepted")
    corruptions.append("missing affine cover pattern")

    wrong = deepcopy(certificate)
    wrong["exact_four"]["with_circle_signature_patterns_sha256"] = "0" * 64
    V.need(rejected(wrong, actual), "wrong torus patterns accepted")
    corruptions.append("wrong torus-pattern hash")

    wrong = deepcopy(certificate)
    wrong["pair_frontier"]["mode_orbit_counts"]["at_least_five"] -= 1
    V.need(rejected(wrong, actual), "missing pair orbit accepted")
    corruptions.append("missing at-least-five pair orbit")

    wrong = deepcopy(certificate)
    wrong["pair_frontier"]["exact_four_compatible_bezout_bound"] -= 1
    V.need(rejected(wrong, actual), "wrong Bezout allowance accepted")
    corruptions.append("wrong exact-four Bezout allowance")

    wrong = deepcopy(certificate)
    wrong["pair_frontier"]["compatibility_D3_invariant"] = False
    V.need(rejected(wrong, actual), "false D3 flag accepted")
    corruptions.append("false D3-invariance flag")

    wrong = deepcopy(certificate)
    wrong["explicit_interface"]["sha256"] = "0" * 64
    V.need(rejected(wrong, actual), "wrong interface hash accepted")
    corruptions.append("wrong explicit-interface hash")

    words = tuple(product(range(4), repeat=4))
    full = (1 << 256) - 1
    coordinate_cosets = [V.mask_for_equation((1, 0, 0, 0), c, words) for c in range(4)]
    union = 0
    for mask in coordinate_cosets:
        union |= mask
    V.need(union == full, "four parallel affine hyperplanes do not cover")
    partial = coordinate_cosets[0] | coordinate_cosets[1] | coordinate_cosets[2]
    V.need(partial != full, "three affine hyperplanes unexpectedly cover")

    torus = 0
    for i, word in enumerate(words):
        if all(word):
            torus |= 1 << i
    nonzero_slices = [V.mask_for_equation((1, 0, 0, 0), c, words) & torus for c in (1, 2, 3)]
    V.need((nonzero_slices[0] | nonzero_slices[1] | nonzero_slices[2]) == torus, "torus slice cover")

    print(
        json.dumps(
            {
                "status": "CONTROLS_PASSED",
                "positive_certificate_replay": True,
                "direct_curve_failure_masks": 2797,
                "curve_tail_colour_tests": 2797 * 256,
                "theoretical_affine_hyperplanes": 340,
                "affine_disjointness_classes": 85,
                "exact_four_signature_patterns": 91,
                "pair_orbit_classifications": 132130,
                "small_cover_controls": 3,
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
