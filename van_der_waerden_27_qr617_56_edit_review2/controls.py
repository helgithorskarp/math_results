#!/usr/bin/env python3
"""Reject corrupt mathematical deductions and incomplete case covers."""
import argparse
import copy
import json
from pathlib import Path

import check


def run(bundle):
    rejected = []

    def reject(label, action):
        try:
            action()
        except ValueError:
            rejected.append(label)
            return
        raise RuntimeError("Corrupt certificate accepted: " + label)

    check.check_suite(bundle)
    for label, pair in (("constant AP", [1, 0]), ("free pole in AP", [0, 1])):
        bad = copy.deepcopy(bundle["prefix-26-1848.json"])
        bad["records"][0][1][0] = pair
        reject(label, lambda bad=bad: check.check_prefix(bad))

    bad = copy.deepcopy(bundle["prefix-27-28.json"])
    row = next(row for row in bad["records"] if len(row[1]) > 1)
    row[1][-1] = row[1][0].copy()
    reject("overlapping prefix packing", lambda: check.check_prefix(bad))

    bad = copy.deepcopy(bundle["prefix-27-28.json"])
    bad["records"].pop()
    reject("truncated prefix cover", lambda: check.check_prefix(bad))

    bad = copy.deepcopy(bundle["branch-0-1.json"])
    bad["records"].insert(0, ["f", 2, [[1, 1]]])
    reject("unproved conditional antecedent", lambda: check.check_branch(bad))

    bad = copy.deepcopy(bundle["branch-0-1.json"])
    bad["records"].insert(0, ["t", 618, 1, 617])
    reject("nonunit or already satisfied forcing clause", lambda: check.check_branch(bad))

    bad = copy.deepcopy(bundle["branch-0-1.json"])
    bad["records"].insert(0, ["budget", 0])
    reject("unexhausted budget", lambda: check.check_branch(bad))

    bad = copy.deepcopy(bundle["branch-0-1235.json"])
    pairs = bad["contradiction"]["aps"]
    pairs[-1] = pairs[0].copy()
    reject("overlapping terminal packing", lambda: check.check_branch(bad))

    bad = bundle.copy()
    del bad["branch-1-3656.json"]
    reject("missing endpoint root", lambda: check.check_suite(bad))

    bad = {k: v for k, v in bundle.items() if not k.startswith("branch-1-")}
    reject("missing endpoint color", lambda: check.check_suite(bad))

    bad = bundle.copy()
    bad["branch-0-1235.json"] = copy.deepcopy(bad["branch-0-1852.json"])
    reject("valid transcript substituted for another case", lambda: check.check_suite(bad))

    bad = copy.deepcopy(bundle["branch-0-1235.json"])
    bad["contradiction"] = {"reason": "too_many_forced"}
    reject("unsupported terminal contradiction", lambda: check.check_branch(bad))

    # Independent color calculations exercise reciprocity signs and pole zeros.
    squares = {a * a % check.PRIME for a in range(1, check.PRIME)}
    for a in range(check.PRIME):
        expected = 0 if not a else (1 if a in squares else -1)
        check.require(check.jacobi(a, check.PRIME) == expected, "Jacobi cross-check")
    return {"positive_control": True, "rejected_controls": rejected,
            "quadratic_reciprocity_cross_checks": check.PRIME}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    bundle, _ = check.read_bundle(args.directory)
    print(json.dumps(run(bundle), indent=2))
