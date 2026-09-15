#!/usr/bin/env python3
"""Small independent controls and deliberate-corruption tests."""

from copy import deepcopy
import argparse
import json
from pathlib import Path

import independent_check as check


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_palette_private_bridge"


def colouring_count(vertices, edges, colours):
    return check.enumerate_canonical_colourings(vertices, edges, colours, lambda _word: None)


def run_controls():
    certificate = json.loads((SOURCE / "certificate.json").read_text())
    _points, _edges, inherited = check.exact_geometry(certificate)
    rejected = []
    mutations = []

    bad = deepcopy(certificate)
    bad["coordinates"][18][0][0] = "0"
    mutations.append(("coordinate_formula", bad))
    bad = deepcopy(certificate)
    bad["coordinates"][18] = deepcopy(bad["coordinates"][17])
    mutations.append(("collision", bad))
    bad = deepcopy(certificate)
    bad["edges"].remove([1, 16])
    mutations.append(("missing_cross_edge", bad))
    bad = deepcopy(certificate)
    bad["edges"].append([0, 18])
    mutations.append(("extra_nonunit_edge", bad))
    bad = deepcopy(certificate)
    bad["inherited_edges"].remove([0, 1])
    mutations.append(("missing_inherited_edge", bad))
    for name, bad in mutations:
        try:
            check.exact_geometry(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)

    toy = {
        "empty3_k3": colouring_count(3, [], 3),
        "path3_k2": colouring_count(3, [(0, 1), (1, 2)], 2),
        "path3_k3": colouring_count(3, [(0, 1), (1, 2)], 3),
        "triangle_k2": colouring_count(3, [(0, 1), (0, 2), (1, 2)], 2),
        "triangle_k3": colouring_count(3, [(0, 1), (0, 2), (1, 2)], 3),
    }
    check.need(toy == {"empty3_k3": 5, "path3_k2": 1, "path3_k3": 2,
                       "triangle_k2": 0, "triangle_k3": 1}, "toy enumerations")

    _count, relations, _rows = check.contact_profile(inherited)
    monotonicity_checks = 0
    for weaker in range(16):
        for stronger in range(16):
            if weaker & stronger == weaker:
                check.need(relations[stronger] <= relations[weaker], "contact monotonicity")
                monotonicity_checks += 1
    check.need(monotonicity_checks == 81, "monotonicity-pair count")

    result = check.review(SOURCE)
    check.need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected replay")
    output = {
        "accepted_review_replayed": True,
        "corruptions_rejected": rejected,
        "contact_monotonicity_checks": monotonicity_checks,
        "all_four_contacts_conditionally_essential": all(
            row["canonical_restored"] > 0
            for row in result["leave_one_contact_out"].values()
        ),
        "disjoint_pair_gain_decomposition": result["contact_pair_decomposition"][
            "gain_sets_disjoint_and_exhaust_full_gain"
        ],
        "toy_canonical_colouring_counts": toy,
    }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = run_controls()
    if args.check_expected:
        check.need(output == json.loads((HERE / "CONTROLS_EXPECTED.json").read_text()),
                   "controls expected output mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
