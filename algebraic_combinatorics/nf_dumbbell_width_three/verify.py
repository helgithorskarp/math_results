#!/usr/bin/env python3
"""Exact checks for the NF orbit of the dumbbell B_{3,m}."""

from __future__ import annotations

import argparse
import itertools
import sys
from collections.abc import Iterable

Type = tuple[int, int, int, int]
TypeAntichain = frozenset[Type]


# A base type is (x_0, number of ordinary x vertices, y_0).  The last
# coordinate of a wave facet A_s is s + WEIGHT[base].
WEIGHT: dict[tuple[int, int, int], int] = {
    (0, 0, 0): 3,
    (0, 0, 1): 2,
    (0, 1, 0): 1,
    (0, 1, 1): 0,
    (0, 2, 0): 0,
    (0, 2, 1): -1,
    (1, 0, 0): 1,
    (1, 0, 1): -1,
    (1, 1, 0): 0,
    (1, 1, 1): -2,
    (1, 2, 0): -2,
    (1, 2, 1): -3,
}


def leq(left: Type, right: Type) -> bool:
    """Coordinatewise order, equivalent to possible subset containment."""
    return all(x <= y for x, y in zip(left, right, strict=True))


def all_types(m: int) -> Iterable[Type]:
    if m < 2:
        raise ValueError("m must be at least 2")
    return itertools.product((0, 1), range(3), (0, 1), range(m))


def maximal(types: Iterable[Type]) -> TypeAntichain:
    candidates = frozenset(types)
    return frozenset(
        candidate
        for candidate in candidates
        if not any(
            candidate != other and leq(candidate, other) for other in candidates
        )
    )


def delta_types(facets: TypeAntichain, m: int) -> TypeAntichain:
    """Apply delta_NF exactly in the S_2 x S_{m-1} type quotient."""
    fibre_tops: list[Type] = []
    for x0, x_count, y0 in itertools.product((0, 1), range(3), (0, 1)):
        base = (x0, x_count, y0)
        thresholds = [
            facet[3]
            for facet in facets
            if all(facet[i] <= base[i] for i in range(3))
        ]
        height = min(thresholds) - 1 if thresholds else m - 1
        if height >= 0:
            fibre_tops.append((*base, height))
    return maximal(fibre_tops)


def in_range(types: Iterable[Type], m: int) -> TypeAntichain:
    """Discard formula terms whose ordinary-y count lies outside [0,m-1]."""
    return frozenset(t for t in types if 0 <= t[3] < m)


def initial_types(m: int) -> TypeAntichain:
    """Facet types of B_{3,m}, with bridge x_0 y_0."""
    result = {
        (0, 2, 0, 0),  # the edge between the two ordinary x vertices
        (1, 1, 0, 0),  # x_0 to either ordinary x vertex
        (1, 0, 1, 0),  # bridge
        (0, 0, 1, 1),  # y_0 to an ordinary y vertex
    }
    if m >= 3:
        result.add((0, 0, 0, 2))
    return frozenset(result)


def prefix_types(m: int) -> list[TypeAntichain]:
    """The six fixed-form prefix states F_0,...,F_5."""
    q = m - 1
    f0 = initial_types(m)
    f1 = frozenset({(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1)})
    f2 = frozenset({(0, 0, 1, q), (1, 0, 1, 0), (1, 2, 0, 0)})
    f3 = frozenset({(0, 2, 0, q), (0, 2, 1, q - 1), (1, 1, 0, q)})
    f4 = in_range(
        {
            (0, 1, 1, q),
            (1, 0, 1, q),
            (1, 1, 1, q - 1),
            (1, 2, 0, q - 1),
            (1, 2, 1, q - 2),
        },
        m,
    )
    f5 = in_range(
        {
            (0, 0, 1, q),
            (0, 2, 0, q),
            (0, 2, 1, q - 1),
            (1, 0, 1, q - 1),
            (1, 1, 0, q),
            (1, 1, 1, q - 2),
            (1, 2, 0, q - 2),
            (1, 2, 1, q - 3),
        },
        m,
    )
    return [f0, f1, f2, f3, f4, f5]


def wave_types(s: int, m: int) -> TypeAntichain:
    """The translating antichain A_s, defined for 1 <= s <= m-2."""
    if not 1 <= s <= m - 2:
        raise ValueError("wave index must satisfy 1 <= s <= m-2")
    return frozenset(
        (*base, s + weight)
        for base, weight in WEIGHT.items()
        if 0 <= s + weight < m
    )


def tail_types(m: int) -> TypeAntichain:
    """The terminal state T before the return to F_0."""
    return in_range(
        {
            (0, 0, 0, 3),
            (0, 0, 1, 2),
            (0, 1, 0, 1),
            (0, 1, 1, 0),
            (1, 0, 0, 1),
            (1, 2, 0, 0),
        },
        m,
    )


def predicted_orbit(m: int) -> list[TypeAntichain]:
    if m < 2:
        raise ValueError("m must be at least 2")
    return (
        prefix_types(m)
        + [wave_types(s, m) for s in range(m - 2, 0, -1)]
        + [tail_types(m)]
    )


def expand_types(types: TypeAntichain, m: int) -> frozenset[int]:
    """Expand type orbits to bit-mask facets on x_0,x_1,x_2,y_0,y_1,... ."""
    ordinary_x_bits = (1, 2)
    ordinary_y_bits = range(4, m + 3)
    result: set[int] = set()
    for x0, x_count, y0, y_count in types:
        fixed = x0 | (y0 << 3)
        for chosen_x in itertools.combinations(ordinary_x_bits, x_count):
            for chosen_y in itertools.combinations(ordinary_y_bits, y_count):
                mask = fixed
                for bit in itertools.chain(chosen_x, chosen_y):
                    mask |= 1 << bit
                result.add(mask)
    return frozenset(result)


def delta_masks(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    """Definition-level NF operator on the full Boolean lattice."""
    admissible = {
        candidate
        for candidate in range(1 << vertex_count)
        if not any(candidate & facet == facet for facet in facets)
    }
    return frozenset(
        candidate
        for candidate in admissible
        if all(
            candidate | (1 << bit) not in admissible
            for bit in range(vertex_count)
            if not candidate & (1 << bit)
        )
    )


def verify_type_formula(max_m: int) -> tuple[int, int]:
    states = 0
    transitions = 0
    for m in range(2, max_m + 1):
        orbit = predicted_orbit(m)
        if len(orbit) != m + 5:
            raise AssertionError(f"m={m}: wrong orbit length {len(orbit)}")
        if len(set(orbit)) != len(orbit):
            raise AssertionError(f"m={m}: premature labelled repetition")
        for left, right in itertools.pairwise(orbit):
            if delta_types(left, m) != right:
                raise AssertionError(f"m={m}: incorrect internal transition")
            transitions += 1
        if delta_types(orbit[-1], m) != orbit[0]:
            raise AssertionError(f"m={m}: orbit does not close")
        transitions += 1
        states += len(orbit)
    return states, transitions


def verify_nongraph_states(max_m: int) -> None:
    for m in range(2, max_m + 1):
        orbit = predicted_orbit(m)
        if any(sum(t) != 2 for t in orbit[0] | orbit[1]):
            raise AssertionError(f"m={m}: first two states should be graphs")
        for step, state in enumerate(orbit[2:], start=2):
            if max(map(sum, state)) < 3:
                raise AssertionError(f"m={m}, step={step}: expected a large facet")


def verify_definition_level(direct_max_m: int) -> tuple[int, int]:
    states = 0
    facets_checked = 0
    for m in range(2, direct_max_m + 1):
        orbit = predicted_orbit(m)
        actual = expand_types(orbit[0], m)
        for expected_types in orbit:
            expected = expand_types(expected_types, m)
            if actual != expected:
                raise AssertionError(f"definition-level mismatch for m={m}")
            states += 1
            facets_checked += len(actual)
            actual = delta_masks(actual, m + 3)
        if actual != expand_types(orbit[0], m):
            raise AssertionError(f"definition-level orbit does not close for m={m}")
    return states, facets_checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=300)
    parser.add_argument("--direct-max-m", type=int, default=8)
    args = parser.parse_args()
    if args.max_m < 2:
        parser.error("--max-m must be at least 2")
    if not 2 <= args.direct_max_m <= args.max_m:
        parser.error("require 2 <= --direct-max-m <= --max-m")

    states, transitions = verify_type_formula(args.max_m)
    verify_nongraph_states(args.max_m)
    direct_states, facets = verify_definition_level(args.direct_max_m)
    print(
        "VERIFIED "
        f"B_(3,m), m=2..{args.max_m}; type_states={states}; "
        f"type_transitions={transitions}; definition_states={direct_states}; "
        f"expanded_facets={facets}; NF(B_(3,m))=m+5"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
