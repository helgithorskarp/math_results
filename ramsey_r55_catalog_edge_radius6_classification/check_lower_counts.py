#!/usr/bin/env python3
"""Compare radius-six lower models with the radius-one-to-five maps."""

import argparse
from collections import Counter


def count_map(path: str, expected_header: str, expected_fields: int) -> Counter:
    counts = Counter()
    with open(path, encoding="ascii") as source:
        if source.readline().rstrip("\n") != expected_header:
            raise RuntimeError(f"unexpected map header: {path}")
        for line in source:
            if line.startswith("# SUMMARY "):
                break
            fields = line.rstrip("\n").split("\t")
            if len(fields) != expected_fields:
                raise RuntimeError(f"bad map row: {path}")
            counts[int(fields[0])] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("parent_counts")
    parser.add_argument("radius2_map")
    parser.add_argument("radius3_map")
    parser.add_argument("radius4_map")
    parser.add_argument("radius5_map")
    args = parser.parse_args()

    expected = {}
    with open(args.parent_counts, encoding="ascii") as source:
        for line in source:
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

    lower.update(
        count_map(
            args.radius3_map,
            "parent\tedge_1\tedge_2\tedge_3\ttarget_kind\ttarget_index",
            6,
        )
    )
    lower.update(
        count_map(
            args.radius4_map,
            "parent\tedge_1\tedge_2\tedge_3\tedge_4\t"
            "target_kind\ttarget_index",
            7,
        )
    )
    lower.update(
        count_map(
            args.radius5_map,
            "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
            "target_kind\ttarget_index",
            8,
        )
    )

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
