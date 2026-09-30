#!/usr/bin/env python3
"""Positive control and deliberately malformed mathematical certificates."""

import argparse
import copy
import json
from pathlib import Path

import verify


def rejected(name, action):
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return name
    raise AssertionError(f"Corrupted certificate accepted: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("build"))
    args = parser.parse_args()
    bundle = {name: json.loads((args.directory / name).read_text()) for name in verify.required_names()}
    positive = verify.verify_suite(bundle)
    assert positive["required_nonzero_changes"] == 56
    passed = []

    prefix = copy.deepcopy(bundle["prefix-26-1848.json"])
    prefix["budget"][0] = 27
    passed.append(rejected("wrong opposite-color budget", lambda: verify.verify_prefix(prefix)))

    prefix = copy.deepcopy(bundle["prefix-27-28.json"])
    packing = next(row for row in prefix["records"] if len(row[1]) > 1)
    packing[1][-1] = packing[1][0].copy()
    passed.append(rejected("intersecting prefix packing", lambda: verify.verify_prefix(prefix)))

    prefix = copy.deepcopy(bundle["prefix-27-28.json"])
    prefix["records"].pop()
    passed.append(rejected("truncated prefix coverage", lambda: verify.verify_prefix(prefix)))

    branch = copy.deepcopy(bundle["branch-0-1235.json"])
    pairs = branch["contradiction"]["aps"]
    pairs[-1] = pairs[0].copy()
    passed.append(rejected("intersecting required packing", lambda: verify.verify_branch(branch)))

    branch = copy.deepcopy(bundle["branch-0-1.json"])
    branch["records"].insert(0, ["t", 2, 1, 617])
    passed.append(rejected("unproved singleton forcing", lambda: verify.verify_branch(branch)))

    branch = copy.deepcopy(bundle["branch-0-1.json"])
    branch["records"].insert(0, ["budget", 0])
    passed.append(rejected("unexhausted class budget", lambda: verify.verify_branch(branch)))

    incomplete = bundle.copy()
    del incomplete["branch-1-3656.json"]
    passed.append(rejected("missing endpoint root", lambda: verify.verify_suite(incomplete)))

    incomplete = {name: data for name, data in bundle.items() if not name.startswith("branch-1-")}
    passed.append(rejected("missing endpoint color", lambda: verify.verify_suite(incomplete)))

    wrong_case = copy.deepcopy(bundle)
    wrong_case["branch-0-1235.json"]["root"] = 1852
    passed.append(rejected("valid case substituted for a different root", lambda: verify.verify_suite(wrong_case)))

    print(json.dumps({"positive_control": True, "rejected_controls": passed}, sort_keys=True))


if __name__ == "__main__":
    main()
