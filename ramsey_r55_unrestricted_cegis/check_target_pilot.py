#!/usr/bin/env python3
"""Compare a fresh target-size portfolio receipt with the archived receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("expected", type=Path)
    args = parser.parse_args()
    actual = json.loads(args.summary.read_text(encoding="utf-8"))
    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    parameters = expected["parameters"]

    require(actual["status"] == expected["status"], "portfolio status differs")
    require(actual["targets"] == 0, "archived pilot unexpectedly reproduced a target")
    require(actual["root_degrees"] == [18, 19, 20, 21], "wrong branch coverage")
    require(len(actual["branches"]) == 4, "wrong branch count")
    for branch, receipt in zip(actual["branches"], expected["branches"], strict=True):
        for actual_key, expected_key in (
                ("root_degree", "root_degree"), ("seed", "seed"),
                ("rounds", "rounds"), ("clauses_added", "clauses_added"),
                ("best_red", "best_red_K5"), ("best_blue", "best_blue_K5"),
                ("best_edges", "best_red_edges"),
                ("graph_sha256", "graph_sha256"),
                ("checkpoint_sha256", "checkpoint_sha256")):
            require(branch[actual_key] == receipt[expected_key],
                    f"degree {receipt['root_degree']} field {actual_key} differs")
        require(branch["status"] == "INCOMPLETE", "branch is not incomplete")
        require(branch["physical_status"] == "NOT_GOOD_GRAPH",
                "physical branch status differs")
        require(branch["best"] == branch["best_red"] + branch["best_blue"],
                "producer violation subtotal mismatch")
        require(branch["physical_red_K5"] == branch["best_red"] and
                branch["physical_blue_K5"] == branch["best_blue"],
                "independent physical violation count mismatch")
        require(branch["physical_five_subsets_checked"] ==
                expected["physical_five_subsets_checked_per_final_candidate"],
                "physical scan coverage differs")
        command = branch["command"]
        require(command[1:] == [
            str(parameters["n"]), str(receipt["seed"]),
            str(parameters["rounds_per_branch"]), str(parameters["initial_fives"]),
            str(parameters["max_new"]), str(receipt["root_degree"]),
            str(parameters["degree_bounds"][0]), str(parameters["degree_bounds"][1]),
            "<checkpoint>"], "producer command differs")
    print("TARGET_PILOT_REPLAY status=PASS branches=4 "
          "physical_five_subsets_per_branch=962598")


if __name__ == "__main__":
    main()
