#!/usr/bin/env python3
"""Exact checks for the NF orbit of the dumbbell B_{2,m}.

The production check uses the S_{m-1}-orbit quotient of subsets.  A tuple
(a, c, d, j) records membership of x_0, x_1, y_0 and the number j of
ordinary y-vertices.  The optional definition-level check expands these
types to bit masks and applies the NF operator without using the quotient.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections.abc import Iterable

Type = tuple[int, int, int, int]
TypeAntichain = frozenset[Type]


WEIGHT: dict[tuple[int, int, int], int] = {
    (0, 0, 0): 3,
    (0, 0, 1): 2,
    (0, 1, 0): 1,
    (0, 1, 1): 0,
    (1, 0, 0): 1,
    (1, 0, 1): -1,
    (1, 1, 0): -1,
    (1, 1, 1): -2,
}


def leq(left: Type, right: Type) -> bool:
    """Coordinatewise order, equivalent to possible subset containment."""
    return all(x <= y for x, y in zip(left, right, strict=True))


def all_types(m: int) -> Iterable[Type]:
    if m < 2:
        raise ValueError("m must be at least 2")
    return itertools.product((0, 1), (0, 1), (0, 1), range(m))


def delta_types(facets: TypeAntichain, m: int) -> TypeAntichain:
    """Apply delta_NF exactly in the orbit-type quotient."""
    # In each fixed binary fibre u, admissible last coordinates form an
    # initial interval.  Its top is one below the least forbidden facet
    # height lying under u, or m-1 when there is no such facet.
    fibre_tops: list[Type] = []
    for bits in itertools.product((0, 1), repeat=3):
        thresholds = [
            facet[3]
            for facet in facets
            if all(facet[i] <= bits[i] for i in range(3))
        ]
        height = min(thresholds) - 1 if thresholds else m - 1
        if height >= 0:
            fibre_tops.append((*bits, height))

    return frozenset(
        candidate
        for candidate in fibre_tops
        if not any(
            candidate != other and leq(candidate, other) for other in fibre_tops
        )
    )


def initial_types(m: int) -> TypeAntichain:
    """Facet types of B_{2,m}, with bridge x_0 y_0."""
    result = {
        (1, 1, 0, 0),  # the K_2 edge
        (1, 0, 1, 0),  # the bridge
        (0, 0, 1, 1),  # y_0 y_i
    }
    if m >= 3:
        result.add((0, 0, 0, 2))  # y_i y_j
    return frozenset(result)


def wave_types(s: int, m: int) -> TypeAntichain:
    """The antichain A_s in the closed-form orbit."""
    if not 0 <= s <= m - 2:
        raise ValueError("wave index must satisfy 0 <= s <= m-2")
    return frozenset(
        (*bits, s + weight)
        for bits, weight in WEIGHT.items()
        if 0 <= s + weight <= m - 1
    )


def predicted_orbit(m: int) -> list[TypeAntichain]:
    """States before the first labelled return asserted by the proof."""
    if m < 2:
        raise ValueError("m must be at least 2")
    if m == 2:
        first = initial_types(m)
        return [first, delta_types(first, m)]

    b = m - 1
    f0 = initial_types(m)
    f1 = frozenset({(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1)})
    f2 = frozenset({(0, 0, 1, b), (1, 0, 1, 0), (1, 1, 0, 0)})
    f3 = frozenset({(0, 1, 0, b), (0, 1, 1, b - 1), (1, 0, 0, b)})
    f4 = frozenset(
        {
            (0, 0, 1, b),
            (1, 0, 1, b - 1),
            (1, 1, 0, b - 1),
            (1, 1, 1, b - 2),
        }
    )
    return [f0, f1, f2, f3, f4] + [
        wave_types(s, m) for s in range(b - 1, -1, -1)
    ]


def expand_types(types: TypeAntichain, m: int) -> frozenset[int]:
    """Expand type orbits to bit-mask facets on x_0,x_1,y_0,y_1,... ."""
    ordinary_y_bits = range(3, m + 2)
    result: set[int] = set()
    for x0, x1, y0, count in types:
        fixed = x0 | (x1 << 1) | (y0 << 2)
        for chosen in itertools.combinations(ordinary_y_bits, count):
            mask = fixed
            for bit in chosen:
                mask |= 1 << bit
            result.add(mask)
    return frozenset(result)


def delta_masks(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    """Definition-level NF operator, independent of type compression."""
    admissible = {
        candidate
        for candidate in range(1 << vertex_count)
        if not any(candidate & facet == facet for facet in facets)
    }
    maximal = {
        candidate
        for candidate in admissible
        if all(
            candidate | (1 << bit) not in admissible
            for bit in range(vertex_count)
            if not candidate & (1 << bit)
        )
    }
    return frozenset(maximal)


def relabel_masks(facets: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    result: set[int] = set()
    for facet in facets:
        image = 0
        for old, new in enumerate(permutation):
            if facet & (1 << old):
                image |= 1 << new
        result.add(image)
    return frozenset(result)


def verify_type_formula(max_m: int) -> tuple[int, int]:
    transitions = 0
    states = 0
    for m in range(2, max_m + 1):
        orbit = predicted_orbit(m)
        states += len(orbit)
        if len(set(orbit)) != len(orbit):
            raise AssertionError(f"premature labelled repetition for m={m}")
        for left, right in itertools.pairwise(orbit):
            if delta_types(left, m) != right:
                raise AssertionError(f"incorrect transition for m={m}")
            transitions += 1
        if delta_types(orbit[-1], m) != orbit[0]:
            raise AssertionError(f"orbit does not close for m={m}")
        transitions += 1
        expected_length = 2 if m == 2 else m + 4
        if len(orbit) != expected_length:
            raise AssertionError(f"wrong labelled period for m={m}")
    return states, transitions


def verify_exceptional_isomorphism() -> None:
    """For B_{2,2}=P_4, delta(B_{2,2}) is an isomorphic relabelling."""
    m = 2
    initial = expand_types(initial_types(m), m)
    image = delta_masks(initial, m + 2)
    # Old path x_1--x_0--y_0--y_1 maps to y_0--x_1--y_1--x_0.
    permutation = (1, 2, 3, 0)  # x_0->x_1, x_1->y_0, y_0->y_1, y_1->x_0
    if relabel_masks(initial, permutation) != image:
        raise AssertionError("the explicit P_4 isomorphism failed")


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
            actual = delta_masks(actual, m + 2)
        if actual != expand_types(orbit[0], m):
            raise AssertionError(f"definition-level orbit does not close for m={m}")
    return states, facets_checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=200)
    parser.add_argument("--direct-max-m", type=int, default=8)
    args = parser.parse_args()
    if args.max_m < 3:
        parser.error("--max-m must be at least 3")
    if not 2 <= args.direct_max_m <= args.max_m:
        parser.error("require 2 <= --direct-max-m <= --max-m")

    states, transitions = verify_type_formula(args.max_m)
    verify_exceptional_isomorphism()
    direct_states, facets = verify_definition_level(args.direct_max_m)
    print(
        "VERIFIED "
        f"m=2..{args.max_m}; type_states={states}; "
        f"type_transitions={transitions}; "
        f"definition_states={direct_states}; expanded_facets={facets}; "
        "NF(B_2,2)=1 up_to_isomorphism"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
