#!/usr/bin/env python3
"""Small exact controls and deliberate certificate corruptions."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import independent_check as check


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent


def rejected_mutations(certificate, cases):
    mutations = []
    bad = deepcopy(certificate)
    bad["schema"] = 2
    mutations.append(("schema", bad))
    bad = deepcopy(certificate)
    bad["cases"][0]["points"] += 1
    mutations.append(("point_count", bad))
    bad = deepcopy(certificate)
    bad["cases"][1]["edges"] -= 1
    mutations.append(("edge_count", bad))
    bad = deepcopy(certificate)
    bad["cases"][2]["point_sha256"] = "0" * 64
    mutations.append(("point_hash", bad))
    bad = deepcopy(certificate)
    del bad["cases"][3]["terminal_witnesses"]["012"]
    mutations.append(("missing_terminal_pattern", bad))
    bad = deepcopy(certificate)
    word = bad["cases"][4]["terminal_witnesses"]["001"]
    bad["cases"][4]["terminal_witnesses"]["001"] = "1" + word[1:]
    mutations.append(("wrong_terminal_pattern", bad))

    rejected = []
    for name, bad in mutations:
        try:
            check.validate_target(bad, cases)
        except check.ReviewFailure:
            rejected.append(name)
        else:
            raise check.ReviewFailure("accepted target corruption: " + name)
    return rejected


def run_controls():
    directions, rows = check.enumerate_unit_directions()
    source = check.reconstruct_source(REPOSITORY / check.SOURCE_NAME, directions)
    cases = check.reconstruct_cases(source, directions)
    certificate = check.read_json(REPOSITORY / check.TARGET_NAME / "certificate.json")
    check.validate_target(certificate, cases)
    rejected = rejected_mutations(certificate, cases)

    triangle = ((0, 1), (0, 2), (1, 2))
    path = ((0, 1), (1, 2))
    toy = {}
    for name, order, edges, colours, pins in (
        ("path3_k2", 3, path, 2, ()),
        ("triangle_k2", 3, triangle, 2, ()),
        ("triangle_k3", 3, triangle, 3, ()),
        ("triangle_k3_equal_pin_conflict", 3, triangle, 3, ((0, 0), (1, 0))),
        ("moser_k3", 7, check.MOSER_PATTERN_EDGES, 3, ()),
    ):
        answer, stats = check.solve_colouring(order, edges, colours, pins)
        toy[name] = {"satisfiable": answer is not None, "stats": stats}
    expected_toy = {
        "path3_k2": {"satisfiable": True, "stats": {"nodes": 4, "dead_ends": 0}},
        "triangle_k2": {"satisfiable": False, "stats": {"nodes": 3, "dead_ends": 1}},
        "triangle_k3": {"satisfiable": True, "stats": {"nodes": 4, "dead_ends": 0}},
        "triangle_k3_equal_pin_conflict": {
            "satisfiable": False, "stats": {"nodes": 0, "dead_ends": 1}
        },
        "moser_k3": {"satisfiable": False, "stats": {"nodes": 9, "dead_ends": 2}},
    }
    check.need(toy == expected_toy, "toy solver outcomes")
    return {
        "status": "CONTROLS_PASS",
        "unit_direction_box_rows_replayed": rows,
        "unit_directions_replayed": len(directions),
        "five_d3_cases_reconstructed": len(cases),
        "corruptions_rejected": rejected,
        "toy_solver_checks": toy,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run_controls()
    if args.check_expected:
        check.need(result == check.read_json(HERE / "CONTROLS_EXPECTED.json"),
                   "controls expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
