#!/usr/bin/env python3
"""Enumerate nonplane full binary trees and the Van Voorhis statistic exactly."""

import argparse
from collections import Counter
from functools import cache
import json
from pathlib import Path


@cache
def trees(leaves):
    """Canonicalize siblings by (number of leaves, serialization)."""
    if leaves == 1:
        return ("x",)
    answer = []
    for left_size in range(1, leaves // 2 + 1):
        right_size = leaves - left_size
        for left in trees(left_size):
            for right in trees(right_size):
                if left_size == right_size and left > right:
                    continue
                answer.append("(" + left + right + ")")
    assert len(answer) == len(set(answer))
    return tuple(answer)


def children(tree):
    assert tree.startswith("(") and tree.endswith(")")
    balance = 0
    for index in range(1, len(tree) - 1):
        balance += (tree[index] == "(") - (tree[index] == ")")
        if balance == 0:
            return tree[1 : index + 1], tree[index + 1 : -1]
    raise ValueError("malformed tree")


@cache
def statistics(tree):
    if tree == "x":
        return 1, 0, 0, (0,), ()
    left, right = children(tree)
    nl, hl, fl, dl, cl = statistics(left)
    nr, hr, fr, dr, cr = statistics(right)
    height = 1 + max(hl, hr)
    value = 2 * (fl + fr + (1 << (hl + hr)))
    leaf_depths = tuple(sorted(depth + 1 for depth in dl + dr))
    branch_costs = tuple(sorted((hl + hr + 1,) + tuple(c + 1 for c in cl + cr)))
    assert value == sum(1 << c for c in branch_costs)
    return nl + nr, height, value, leaf_depths, branch_costs


def certificate():
    table = []
    for n in range(1, 14):
        values = [statistics(tree)[2] for tree in trees(n)]
        table.append({"leaves": n, "nonplane_trees": len(values), "minimum_f": min(values)})
    selected = []
    for tree in sorted(trees(13)):
        n, height, value, leaf_depths, branch_costs = statistics(tree)
        if value <= 512:
            selected.append(
                {
                    "tree": tree,
                    "height": height,
                    "f": value,
                    "leaf_depths": list(leaf_depths),
                    "branch_costs": list(branch_costs),
                    "runner_depth_caps": [9 - c for c in branch_costs],
                    "forced_runner_depths": [9 - c if (1 << c) > 512 - value else None
                                             for c in branch_costs],
                    "root_branch_cost": statistics(children(tree)[0])[1]
                                        + statistics(children(tree)[1])[1] + 1,
                    "forced_root_runner_depth": 2,
                }
            )
    return {
        "schema": "sorting13-full-binary-shapes-v1",
        "agent": "six-sorting-2",
        "role": "researcher",
        "scope": "Full binary tree classification; network corollary assumes no unary maximum-route gates.",
        "leaves": 13,
        "f_cap": 512,
        "table": table,
        "selected": selected,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = certificate()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check:
        expected = json.loads(args.check.read_text())
        if expected != result:
            raise SystemExit("certificate mismatch")
    heights = Counter(row["height"] for row in result["selected"])
    print(json.dumps({"nonplane_trees": len(trees(13)), "selected": len(result["selected"]),
                      "minimum_f": result["table"][-1]["minimum_f"],
                      "height_counts": dict(sorted(heights.items()))}, sort_keys=True))


if __name__ == "__main__":
    main()
