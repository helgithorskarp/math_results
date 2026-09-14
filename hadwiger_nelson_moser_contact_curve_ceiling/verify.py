#!/usr/bin/env python3
"""Exact two-route verification of the contact multiplicity ceiling."""

import argparse
import copy
import itertools
import json
from pathlib import Path

from model import (
    ONE,
    direct_inventory,
    factorized_inventory,
    norm,
    require,
    spindle,
    sub,
    summarize,
)

HERE = Path(__file__).resolve().parent


def rejected(test):
    try:
        test()
    except ValueError:
        return
    raise ValueError("negative control accepted")


def run(expected_path):
    direct = direct_inventory()
    factorized = factorized_inventory()
    require(direct == factorized, "direct and difference-factorized inventories disagree")
    baseline, constant_noncontacts, groups = direct
    summary = summarize(baseline, constant_noncontacts, groups)
    expected = json.loads(Path(expected_path).read_text())
    require(summary == expected, "expected summary mismatch")

    M = spindle()
    source_edges = [
        (i, j)
        for i, j in itertools.combinations(range(7), 2)
        if norm(sub(M[i], M[j])) == ONE
    ]
    require(len(source_edges) == 11, "Moser source edge count")

    changed_count = copy.deepcopy(groups)
    first_key = next(iter(changed_count))
    changed_count[first_key][0] += 1
    rejected(lambda: require(changed_count == factorized[2], "corrupt multiplicity"))
    changed_type = copy.deepcopy(groups)
    changed_type[first_key][2] = not changed_type[first_key][2]
    rejected(lambda: require(changed_type == factorized[2], "corrupt class type"))
    rejected(lambda: summarize(baseline + 1, constant_noncontacts, groups))

    return dict(summary, source_vertices=7, source_edges=len(source_edges), exact_enumeration_routes=2,
                negative_controls=3, record_improvement=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", default=str(HERE / "expected-summary.json"))
    args = parser.parse_args()
    print(json.dumps(run(args.expected), indent=2, sort_keys=True))
