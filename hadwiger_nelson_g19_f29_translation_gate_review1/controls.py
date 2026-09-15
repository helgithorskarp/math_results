#!/usr/bin/env python3
"""Independent toy checks and deliberate-corruption controls."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import independent_check as check


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_g19_f29_translation_gate"


def rejected_geometry_mutations(certificate):
    mutations = []
    bad = deepcopy(certificate)
    bad["coordinates"][44][0][0] = "1"
    mutations.append(("coordinate_formula", bad))
    bad = deepcopy(certificate)
    bad["coordinates"][44] = deepcopy(bad["coordinates"][43])
    mutations.append(("coordinate_collision", bad))
    bad = deepcopy(certificate)
    bad["edges"].remove([7, 40])
    mutations.append(("missing_extra_edge", bad))
    bad = deepcopy(certificate)
    bad["edges"].append([0, 44])
    mutations.append(("spurious_edge", bad))
    bad = deepcopy(certificate)
    bad["f29_map"][22] = 41
    mutations.append(("wrong_merge_map", bad))
    bad = deepcopy(certificate)
    bad["inherited_edges"].remove([11, 15])
    mutations.append(("missing_inherited_edge", bad))

    rejected = []
    for name, mutated in mutations:
        try:
            check.reconstruct_geometry(mutated, SOURCE)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted certificate corruption: " + name)
    return rejected


def run_controls():
    certificate = json.loads((SOURCE / "certificate.json").read_text())
    rejected = rejected_geometry_mutations(certificate)
    toy = {
        "empty3_k3": check.enumerate_colourings(3, [], 3)["total"],
        "path3_k2": check.enumerate_colourings(3, [(0, 1), (1, 2)], 2)["total"],
        "path3_k3": check.enumerate_colourings(3, [(0, 1), (1, 2)], 3)["total"],
        "triangle_k2": check.enumerate_colourings(3, [(0, 1), (0, 2), (1, 2)], 2)["total"],
        "triangle_k3": check.enumerate_colourings(3, [(0, 1), (0, 2), (1, 2)], 3)["total"],
        "triangle_k3_pin_v0_0": check.enumerate_colourings(
            3, [(0, 1), (0, 2), (1, 2)], 3, ((0, 0),)
        )["total"],
    }
    check.need(
        toy
        == {
            "empty3_k3": 27,
            "path3_k2": 2,
            "path3_k3": 12,
            "triangle_k2": 0,
            "triangle_k3": 6,
            "triangle_k3_pin_v0_0": 2,
        },
        "toy labeled-colouring census",
    )
    result = check.review(SOURCE)
    check.need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected replay")
    output = {
        "accepted_review_replayed": True,
        "corruptions_rejected": rejected,
        "toy_labeled_colouring_counts": toy,
        "boundary_totals_replayed": {
            "g19": result["normalized_boundary_census"]["g19"]["total"],
            "f29": result["normalized_boundary_census"]["f29"]["total"],
        },
        "minimum_static_extension_library_size": result["universal_extension"][
            "minimum_static_extension_library_size"
        ],
    }
    return output


def main() -> None:
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
