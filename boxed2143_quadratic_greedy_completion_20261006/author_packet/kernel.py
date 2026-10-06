#!/usr/bin/env python3
"""Exact boxed-2143 maximum-insertion kernel. All entry indices are zero based."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from typing import Iterable


Permutation = tuple[int, ...]
Occurrence = tuple[int, int, int, int]


def validate_permutation(values: Iterable[int]) -> Permutation:
    p = tuple(values)
    if any(type(v) is not int for v in p):
        raise ValueError("entries must be integers")
    seen = [False] * (len(p) + 1)
    for value in p:
        if not 1 <= value <= len(p) or seen[value]:
            raise ValueError("entries must be precisely 1,...,n with no repetitions")
        seen[value] = True
    return p


def validate_gap(p: Permutation, gap: int) -> None:
    if type(gap) is not int or not 0 <= gap <= len(p):
        raise ValueError("gap must be an integer between 0 and n")


def insert_maximum(values: Iterable[int], gap: int) -> Permutation:
    p = validate_permutation(values)
    validate_gap(p, gap)
    return p[:gap] + (len(p) + 1,) + p[gap:]


def nearest_greater(values: Iterable[int]) -> tuple[list[int | None], list[int | None]]:
    p = validate_permutation(values)
    left: list[int | None] = [None] * len(p)
    right: list[int | None] = [None] * len(p)
    stack: list[int] = []
    for j, value in enumerate(p):
        while stack and p[stack[-1]] < value:
            stack.pop()
        left[j] = stack[-1] if stack else None
        stack.append(j)
    stack.clear()
    for j in range(len(p) - 1, -1, -1):
        while stack and p[stack[-1]] < p[j]:
            stack.pop()
        right[j] = stack[-1] if stack else None
        stack.append(j)
    return left, right


@dataclass(frozen=True)
class Blocker:
    left: int
    minimum: int
    right: int

    @property
    def first_gap(self) -> int:
        return self.minimum + 1

    @property
    def last_gap(self) -> int:
        return self.right

    def blocks(self, gap: int) -> bool:
        return self.first_gap <= gap <= self.last_gap

    def child_occurrence(self, gap: int) -> Occurrence:
        if not self.blocks(gap):
            raise ValueError("blocker does not apply to this gap")
        return self.left, self.minimum, gap, self.right + 1


def blockers(values: Iterable[int]) -> tuple[Blocker, ...]:
    p = validate_permutation(values)
    left, right = nearest_greater(p)
    result: list[Blocker] = []
    for j, (l, r) in enumerate(zip(left, right)):
        if l is not None and r is not None and p[l] < p[r]:
            result.append(Blocker(l, j, r))
    return tuple(result)


def legal_maximum_gaps(values: Iterable[int]) -> tuple[int, ...]:
    """Gaps creating no new occurrence. Parent avoidance is a separate condition."""
    p = validate_permutation(values)
    difference = [0] * (len(p) + 2)
    for blocker in blockers(p):
        difference[blocker.first_gap] += 1
        difference[blocker.last_gap + 1] -= 1
    active = 0
    legal: list[int] = []
    for gap in range(len(p) + 1):
        active += difference[gap]
        if active == 0:
            legal.append(gap)
    return tuple(legal)


def new_maximum_occurrences(values: Iterable[int], gap: int) -> tuple[Occurrence, ...]:
    p = validate_permutation(values)
    validate_gap(p, gap)
    return tuple(blocker.child_occurrence(gap) for blocker in blockers(p) if blocker.blocks(gap))


def boxed_occurrences(values: Iterable[int]) -> tuple[Occurrence, ...]:
    """Complete occurrence set, using maximum restrictions and nearest-greater triples."""
    p = validate_permutation(values)
    result: list[Occurrence] = []
    for maximum in range(4, len(p) + 1):
        positions = [i for i, value in enumerate(p) if value <= maximum]
        restricted = tuple(p[i] for i in positions)
        gap = restricted.index(maximum)
        parent = restricted[:gap] + restricted[gap + 1:]
        for occurrence in new_maximum_occurrences(parent, gap):
            result.append(tuple(positions[i] for i in occurrence))
    return tuple(sorted(result))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pi", required=True, help="comma-separated entries; empty string for n=0")
    args = parser.parse_args()
    try:
        p = validate_permutation(()) if args.pi == "" else validate_permutation(int(s) for s in args.pi.split(","))
    except ValueError as e:
        parser.error(str(e))
    payload = {
        "permutation": p,
        "index_convention": "zero-based entries; gap g after g entries",
        "boxed_occurrences": boxed_occurrences(p),
        "gaps_creating_no_new_occurrences": legal_maximum_gaps(p),
        "parent_avoidance_required_for_legal_child": True,
        "blockers": [vars(blocker) for blocker in blockers(p)],
        "forbidden_gap_witnesses": {
            str(gap): new_maximum_occurrences(p, gap)
            for gap in range(len(p) + 1) if new_maximum_occurrences(p, gap)
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
