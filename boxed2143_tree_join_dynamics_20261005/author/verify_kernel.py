#!/usr/bin/env python3
"""Finite definition-level check of the maximum-insertion kernel; no universal growth claim."""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations, permutations
import json
import platform
import time

from kernel import (boxed_occurrences, insert_maximum, legal_maximum_gaps,
                    new_maximum_occurrences, validate_permutation)


def direct_occurrences(p: tuple[int, ...]) -> tuple[tuple[int, int, int, int], ...]:
    result = []
    for i1, i2, i3, i4 in combinations(range(len(p)), 4):
        if not p[i2] < p[i1] < p[i4] < p[i3]:
            continue
        selected = {i1, i2, i3, i4}
        if all(j in selected or not p[i2] < p[j] < p[i3]
               for j in range(i1 + 1, i4)):
            result.append((i1, i2, i3, i4))
    return tuple(result)


def require_equal(actual, expected, context) -> None:
    if actual != expected:
        raise RuntimeError(json.dumps({"failure": context, "actual": actual, "expected": expected}))


def check(max_parent: int) -> dict:
    start = time.monotonic()
    stream = hashlib.sha256()
    parent_total = child_total = occurrence_total = 0
    avoider_counts: dict[int, int] = {}
    for malformed in [(1, 1), (0,), (2,), (True,), (1.0,)]:
        try:
            validate_permutation(malformed)
        except ValueError:
            pass
        else:
            raise RuntimeError("malformed permutation was accepted: " + repr(malformed))
    for gap in [-1, 1, True]:
        try:
            insert_maximum((), gap)
        except ValueError:
            pass
        else:
            raise RuntimeError("malformed gap was accepted: " + repr(gap))
    require_equal(legal_maximum_gaps((2, 1, 3)), (0, 1, 3), "hand-checkable 213 insertion")
    require_equal(boxed_occurrences((2, 1, 4, 3)), ((0, 1, 2, 3),), "pattern itself")
    require_equal(boxed_occurrences((2, 4, 1, 3)), (), "different exceptional orbit")
    for n in range(max_parent + 1):
        avoiding_parents = avoiding_children = 0
        for p in permutations(range(1, n + 1)):
            parent_total += 1
            old = direct_occurrences(p)
            require_equal(boxed_occurrences(p), old, {"parent": p, "kind": "complete checker"})
            if not old:
                avoiding_parents += 1
            legal = set(legal_maximum_gaps(p))
            for gap in range(n + 1):
                child_total += 1
                child = insert_maximum(p, gap)
                actual = direct_occurrences(child)
                occurrence_total += len(actual)
                new = new_maximum_occurrences(p, gap)
                shifted_old = tuple(tuple(i + (i >= gap) for i in occurrence) for occurrence in old)
                predicted = tuple(sorted(shifted_old + new))
                require_equal(predicted, actual, {"parent": p, "gap": gap, "kind": "all child occurrences"})
                require_equal(gap in legal, not new, {"parent": p, "gap": gap, "kind": "new-occurrence gaps"})
                if not actual:
                    avoiding_children += 1
                require_equal(not actual, not old and gap in legal,
                              {"parent": p, "gap": gap, "kind": "full child avoidance"})
                stream.update(json.dumps([child, actual], separators=(",", ":")).encode("ascii") + b"\n")
        if n in avoider_counts:
            require_equal(avoiding_parents, avoider_counts[n], {"size": n, "kind": "unique maximum parent"})
        avoider_counts[n] = avoiding_parents
        avoider_counts[n + 1] = avoiding_children
    for n, known in enumerate([1, 1, 2, 6, 23, 106]):
        if n in avoider_counts:
            require_equal(avoider_counts[n], known, {"size": n, "kind": "source baseline"})
    return {
        "status": "PASS",
        "scope": "Every parent in S_n for 0<=n<=max_parent; every maximum insertion gap; exact child occurrence sets.",
        "max_parent": max_parent,
        "parents_checked": parent_total,
        "children_checked": child_total,
        "child_occurrences_checked": occurrence_total,
        "avoider_counts": avoider_counts,
        "stream_sha256": stream.hexdigest(),
        "python": platform.python_version(),
        "dependencies": "Python standard library only",
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "universal_claim_basis": "written derivation, awaiting different researcher review",
        "full_growth_target_solved": False,
        "independent_team_review": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-parent", type=int, default=7)
    args = parser.parse_args()
    if not 0 <= args.max_parent <= 8:
        parser.error("max-parent must be between 0 and 8")
    print(json.dumps(check(args.max_parent), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
