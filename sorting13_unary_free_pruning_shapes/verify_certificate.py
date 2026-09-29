#!/usr/bin/env python3
"""Independent preorder enumeration and definition-level certificate checks.

This checker does not import enumerate_shapes.py and does not use its tree-size
generation recurrence or its recurrence for f.
"""

from collections import Counter
from fractions import Fraction
from itertools import product, combinations
import json
from pathlib import Path


def preorder_words(branches):
    """All full binary plane trees: 1 opens two children, 0 closes a leaf."""
    def walk(internal_left, leaves_left, slots, prefix):
        if slots == 0:
            if internal_left != 0 or leaves_left != 0:
                raise AssertionError("premature completion")
            yield prefix
            return
        if internal_left:
            yield from walk(internal_left - 1, leaves_left, slots + 1, prefix + "1")
        if leaves_left and (slots > 1 or internal_left == 0):
            yield from walk(internal_left, leaves_left - 1, slots - 1, prefix + "0")
    yield from walk(branches, branches + 1, 1, "")


def read_word(word):
    index = 0
    costs = []
    depths = []

    def read(depth):
        nonlocal index
        token = word[index]
        index += 1
        if token == "0":
            depths.append(depth)
            return 1, 0, "x"
        if token != "1":
            raise ValueError("invalid preorder token")
        nl, hl, left = read(depth + 1)
        nr, hr, right = read(depth + 1)
        costs.append(depth + hl + hr + 1)
        if (nl, left) > (nr, right):
            left, right = right, left
        return nl + nr, 1 + max(hl, hr), "(" + left + right + ")"

    leaves, height, tree = read(0)
    assert index == len(word)
    root_cost = costs[-1] if costs else None
    costs.sort()
    value = sum(2 ** c for c in costs)
    return tree, {"height": height, "f": value,
                  "leaf_depths": sorted(depths), "branch_costs": costs,
                  "runner_depth_caps": [9 - c for c in costs],
                  "forced_runner_depths": [9 - c if 2 ** c > 512 - value else None
                                           for c in costs],
                  "root_branch_cost": root_cost,
                  "forced_root_runner_depth": (9 - root_cost if root_cost is not None
                                               and 2 ** root_cost > 512 - value else None)}, leaves


def route_tree(n, comparators):
    """Literal one-hot maximum routes, retaining every touched comparator."""
    nodes = [("leaf",) for _ in range(n)]
    for a, b in comparators:
        left, right = nodes[a], nodes[b]
        if left is not None and right is not None:
            node = ("binary", left, right)
        elif left is not None or right is not None:
            node = ("unary", left if left is not None else right)
        else:
            node = None
        nodes[a], nodes[b] = None, node
    assert nodes[-1] is not None and all(node is None for node in nodes[:-1])
    return nodes[-1]


def invalid_unary_statistic(node):
    """Evaluate the tempting extension, which the fixture disproves."""
    if node[0] == "leaf":
        return 0, 0, 0
    if node[0] == "unary":
        height, value, count = invalid_unary_statistic(node[1])
        return height + 1, 2 * value, count + 1
    hl, fl, ul = invalid_unary_statistic(node[1])
    hr, fr, ur = invalid_unary_statistic(node[2])
    return 1 + max(hl, hr), 2 * (fl + fr + 2 ** (hl + hr)), ul + ur


def check_counterexample(path):
    fixture = json.loads(path.read_text())
    n = fixture["n"]
    net = fixture["comparators"]
    assert n == 4 and len(net) == 6
    assert all(isinstance(a, int) and isinstance(b, int) and 0 <= a < b < n for a, b in net)
    for original in product((0, 1), repeat=n):
        values = list(original)
        for a, b in net:
            values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
        assert values == sorted(original), (original, values)
    deletion_counts = []
    for pair in combinations(range(n), 2):
        # Two fixed largest values: count gates touched by either, once per gate.
        values = [int(i in pair) for i in range(n)]
        count = 0
        for a, b in net:
            count += int(values[a] == 1 or values[b] == 1)
            values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
        assert values == [0, 0, 1, 1]
        deletion_counts.append({"pair": list(pair), "deleted_comparators": count})
    assert deletion_counts == fixture["two_maximum_deletions"]
    height, value, unaries = invalid_unary_statistic(route_tree(n, net))
    assert (height, value, unaries) == (3, 48, 2)
    maximum = max(row["deleted_comparators"] for row in deletion_counts)
    assert maximum == 5 and value > 2 ** maximum
    return {"boolean_inputs": 2 ** n, "false_unary_f": value, "maximum_two_deletion": maximum}


def main():
    directory = Path(__file__).resolve().parent
    certificate = json.loads((directory / "certificate.json").read_text())
    assert certificate["schema"] == "sorting13-full-binary-shapes-v1"
    assert certificate["leaves"] == 13 and certificate["f_cap"] == 512
    expected = {row["tree"]: {key: value for key, value in row.items() if key != "tree"}
                for row in certificate["selected"]}
    assert len(expected) == len(certificate["selected"]) == 6
    selected = {}
    seen = set()
    count = 0
    minimum = None
    for word in preorder_words(12):
        tree, data, leaves = read_word(word)
        assert leaves == 13
        count += 1
        seen.add(tree)
        minimum = data["f"] if minimum is None else min(minimum, data["f"])
        if data["f"] <= 512:
            if tree in selected:
                assert selected[tree] == data
            selected[tree] = data
    assert count == 208012 and len(seen) == 983 and minimum == 392
    assert selected == expected, "entry-level classification mismatch"
    assert all(data["root_branch_cost"] == 7 and data["forced_root_runner_depth"] == 2
               for data in selected.values())
    # Check the entire small-size summary independently as well.
    for row in certificate["table"]:
        n = row["leaves"]
        if n == 13:
            got = (len(seen), minimum)
        else:
            shapes, values = set(), []
            for word in preorder_words(n - 1):
                tree, data, leaves = read_word(word)
                assert leaves == n
                shapes.add(tree)
                values.append(data["f"])
            got = (len(shapes), min(values))
        assert got == (row["nonplane_trees"], row["minimum_f"])
    saturated = [data for data in selected.values() if data["f"] == 512]
    assert len(saturated) == 1
    assert sum(Fraction(1, 2 ** q) for q in saturated[0]["runner_depth_caps"]) == 1
    controls = check_counterexample(directory / "counterexample.json")
    print(json.dumps({"plane_trees": count, "nonplane_trees": len(seen),
                      "selected": len(selected), "minimum_f": minimum,
                      "height_counts": dict(sorted(Counter(data["height"] for data in selected.values()).items())),
                      "counterexample": controls}, sort_keys=True))


if __name__ == "__main__":
    main()
