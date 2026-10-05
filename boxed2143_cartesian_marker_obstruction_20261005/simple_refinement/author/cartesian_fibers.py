"""Exact Cartesian-tree fiber audit for decision 410, not a growth theorem.

Nodes/parents use zero-based positions; permutation values are one based.
Trees are encoded by parent arrays, with -1 for the unique root. A fiber fixes
both parent arrays. Its rank assignments are generated from the union of the
minimum-parent<child and maximum-child<parent order constraints.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import time
from pathlib import Path
from typing import Iterator, Sequence

Pair = tuple[tuple[int, ...], tuple[int, ...]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_permutation(values: Sequence[int]) -> tuple[int, ...]:
    p = tuple(values)
    if any(type(x) is not int for x in p) or sorted(p) != list(range(1, len(p) + 1)):
        raise ValueError("Expected a permutation of 1,...,n")
    return p


def stack_parents(p: Sequence[int], maximum: bool = False) -> tuple[int, ...]:
    """Linear monotone-stack construction; p must have distinct entries."""
    parent = [-1] * len(p)
    stack: list[int] = []
    for i, value in enumerate(p):
        last = -1
        while stack and ((value > p[stack[-1]]) if maximum else (value < p[stack[-1]])):
            last = stack.pop()
        if stack:
            parent[i] = stack[-1]
        if last != -1:
            parent[last] = i
        stack.append(i)
    return tuple(parent)


def recursive_parents(p: Sequence[int], maximum: bool = False) -> tuple[int, ...]:
    """Different construction: recursive extrema of contiguous intervals."""
    parent = [-1] * len(p)

    def visit(lo: int, hi: int, ancestor: int) -> None:
        if lo == hi:
            return
        root = (max if maximum else min)(range(lo, hi), key=p.__getitem__)
        parent[root] = ancestor
        visit(lo, root, root)
        visit(root + 1, hi, root)

    visit(0, len(p), -1)
    return tuple(parent)


def pair_key(p: Sequence[int]) -> Pair:
    return stack_parents(p), stack_parents(p, True)


def validate_tree(parent: Sequence[int]) -> None:
    n = len(parent)
    if n == 0:
        return
    if any(type(x) is not int or x < -1 or x >= n for x in parent):
        raise ValueError("Invalid parent index")
    roots = [i for i, x in enumerate(parent) if x == -1]
    if len(roots) != 1:
        raise ValueError("A tree must have one root")
    left = [-1] * n
    right = [-1] * n
    for child, ancestor in enumerate(parent):
        if ancestor == child:
            raise ValueError("Self-parent")
        if ancestor == -1:
            continue
        side = left if child < ancestor else right
        if side[ancestor] != -1:
            raise ValueError("Multiple children on one side")
        side[ancestor] = child
    seen: set[int] = set()
    inorder: list[int] = []

    def walk(node: int) -> None:
        if node == -1:
            return
        if node in seen:
            raise ValueError("Cycle or repeated node")
        seen.add(node)
        walk(left[node])
        inorder.append(node)
        walk(right[node])

    walk(roots[0])
    if inorder != list(range(n)):
        raise ValueError("Disconnected tree or incorrect inorder positions")


def predecessor_masks(pair: Pair) -> tuple[int, ...]:
    low, high = pair
    if len(low) != len(high):
        raise ValueError("Tree sizes differ")
    validate_tree(low)
    validate_tree(high)
    pred = [0] * len(low)
    for child, ancestor in enumerate(low):
        if ancestor != -1:
            pred[child] |= 1 << ancestor
    for child, ancestor in enumerate(high):
        if ancestor != -1:
            pred[ancestor] |= 1 << child
    return tuple(pred)


def fiber_assignments(pair: Pair) -> Iterator[tuple[int, ...]]:
    """Enumerate all distinct rank assignments satisfying both heap orders."""
    pred = predecessor_masks(pair)
    n = len(pred)
    target = (1 << n) - 1
    assignment = [0] * n

    def visit(chosen: int, rank: int) -> Iterator[tuple[int, ...]]:
        if chosen == target:
            yield tuple(assignment)
            return
        available = [i for i in range(n) if not chosen & (1 << i) and not pred[i] & ~chosen]
        if not available:
            raise ValueError("Combined heap constraints contain a cycle")
        for position in available:
            assignment[position] = rank
            yield from visit(chosen | (1 << position), rank + 1)
            assignment[position] = 0

    yield from visit(0, 1)


def load_checker(path: Path):
    spec = importlib.util.spec_from_file_location("sage_literal_boxed_checker", path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load definition checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixtures() -> dict[str, int]:
    p = (2, 1, 3)
    require(pair_key(p) == ((1, -1, 1), (2, 0, -1)), "Hand tree fixture failed")
    ambiguous = pair_key((2, 4, 1, 3))
    require(set(fiber_assignments(ambiguous)) == {(2, 4, 1, 3), (3, 4, 1, 2)},
            "Hand two-assignment fiber fixture failed")
    require(list(fiber_assignments(((), ()))) == [()], "Empty root convention failed")
    invalid = [(0,), (-1, -1), (1, 0), (-1, 0, 0, 0)]
    for parent in invalid:
        try:
            validate_tree(parent)
        except ValueError:
            continue
        raise RuntimeError(f"Malformed tree accepted: {parent}")
    for malformed in ((1, 1), (0,), (True,)):
        try:
            validate_permutation(malformed)
        except ValueError:
            continue
        raise RuntimeError(f"Malformed permutation accepted: {malformed}")
    return {"explicit_valid_fixtures": 3, "rejected_tree_fixtures": len(invalid),
            "rejected_permutation_fixtures": 3}


def census(max_n: int, audit_max_n: int, checker) -> list[dict[str, object]]:
    rows = []
    for n in range(max_n + 1):
        started = time.monotonic()
        groups: dict[Pair, list[tuple[int, ...]]] = {}
        avoidance: dict[tuple[int, ...], bool] = {}
        stream = hashlib.sha256()
        for p in itertools.permutations(range(1, n + 1)):
            pair = pair_key(p)
            if n <= audit_max_n:
                require(pair == (recursive_parents(p), recursive_parents(p, True)),
                        f"Stack/recursive disagreement at {p}")
            groups.setdefault(pair, []).append(p)
            avoidance[p] = checker.avoids(p)
            stream.update(json.dumps([p, pair, avoidance[p]], separators=(",", ":")).encode()+b"\n")
        require(sum(map(len, groups.values())) == math.factorial(n), "Permutation total failed")
        if n <= audit_max_n:
            for pair, expected in groups.items():
                actual = list(fiber_assignments(pair))
                require(len(actual) == len(set(actual)), f"Repeated rank assignment in {pair}")
                require(set(actual) == set(expected), f"Incomplete/incorrect fiber {pair}")
                require(all(pair_key(p) == pair for p in actual), "Assignment reconstruction failed")
        ranked = sorted(groups, key=lambda pair: (-sum(avoidance[p] for p in groups[pair]),
                                                   -len(groups[pair]), pair))
        all_avoiding = [pair for pair in ranked if all(avoidance[p] for p in groups[pair])]

        def report(pair: Pair) -> dict[str, object]:
            family = groups[pair]
            good = [p for p in family if avoidance[p]]
            bad = next((p for p in family if not avoidance[p]), None)
            return {"min_parents": pair[0], "max_parents": pair[1], "fiber_size": len(family),
                    "avoiding_size": len(good), "avoiding_examples": good[:12],
                    "first_nonavoider": bad,
                    "first_nonavoider_occurrence": checker.first_occurrence(bad) if bad else None}

        row = {"n": n, "permutations": math.factorial(n), "tree_pairs": len(groups),
               "avoiders": sum(avoidance.values()), "entry_stream_sha256": stream.hexdigest(),
               "recursive_tree_and_complete_fiber_audited": n <= audit_max_n,
               "top_avoiding_fibers": [report(pair) for pair in ranked[:5]],
               "largest_entirely_avoiding_fiber": report(all_avoiding[0]) if all_avoiding else None,
               "elapsed_seconds": time.monotonic() - started}
        rows.append(row)
        print(json.dumps({"n": n, "tree_pairs": len(groups), "avoiders": row["avoiders"],
                          "max_avoiding_fiber": row["top_avoiding_fibers"][0]["avoiding_size"],
                          "elapsed_seconds": row["elapsed_seconds"]}), flush=True)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--audit-max-n", type=int, default=7)
    parser.add_argument("--checker-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.audit_max_n <= args.max_n <= 9:
        raise ValueError("Require 0<=audit-max-n<=max-n<=9")
    checker = load_checker(args.checker_path)
    require(not checker.avoids((2, 1, 4, 3)), "Literal forbidden fixture failed")
    require(checker.avoids((2, 4, 1, 5, 3)), "Source boundary fixture failed")
    report = {"decision_message_id": 410,
              "claim_status": "known-encoding reproduction and finite structural observations",
              "python": platform.python_version(), "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "checker_path": str(args.checker_path.resolve()),
              "checker_sha256": hashlib.sha256(args.checker_path.read_bytes()).hexdigest(),
              "trust_boundary": "Python 3 standard library and inspected finite checker; no infinite extrapolation",
              "fixtures": fixtures(), "max_n": args.max_n, "audit_max_n": args.audit_max_n,
              "census": census(args.max_n, args.audit_max_n, checker)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix+".tmp")
    temporary.write_text(json.dumps(report, indent=2)+"\n")
    temporary.replace(args.output)


if __name__ == "__main__":
    main()
