#!/usr/bin/env python3
"""Compare radius-four lower models with the radius-two/three maps."""

import argparse
from collections import Counter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("parent_counts")
    parser.add_argument("radius2_map")
    parser.add_argument("radius3_map")
    args = parser.parse_args()

    expected = {}
    for line in open(args.parent_counts, encoding="ascii"):
        values = dict(field.split("=", 1) for field in line.split())
        parent = int(values["parent"])
        expected[parent] = int(values["lower_models"])
    if sorted(expected) != list(range(328)):
        raise RuntimeError("parent-count file does not cover 0,...,327 exactly")

    lower = Counter()
    with open(args.radius2_map, encoding="ascii") as source:
        if not source.readline().startswith("radius\tparent\t"):
            raise RuntimeError("unexpected radius-two map header")
        for line in source:
            if line.startswith("# SUMMARY "):
                break
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 6 or fields[0] not in {"1", "2"}:
                raise RuntimeError("bad radius-two map row")
            lower[int(fields[1])] += 1

    with open(args.radius3_map, encoding="ascii") as source:
        if not source.readline().startswith("parent\tedge_1\t"):
            raise RuntimeError("unexpected radius-three map header")
        for line in source:
            if line.startswith("# SUMMARY "):
                break
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 6:
                raise RuntimeError("bad radius-three map row")
            lower[int(fields[0])] += 1

    bad = [
        parent
        for parent in range(328)
        if expected[parent] != 1 + lower[parent]
    ]
    if bad:
        raise RuntimeError(f"lower-model count mismatch at parents {bad}")
    print("lower_count_crosscheck=328/328")


if __name__ == "__main__":
    main()
