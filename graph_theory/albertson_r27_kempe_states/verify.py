#!/usr/bin/env python3
"""Exact verifier for the rooted Kempe-block reduction at Albertson r=27.

The program has three jobs.

* Enumerate the allowed 2x2 and 3x2 color-class adjacency masks directly.
* Count the resulting edge/excess-filtered labelled state overfamilies exactly.
* Check topological K_27 certificates for every E_27 family member occurring
  at one of the three surviving order-53 edge counts.

Only Python integer arithmetic is used.
"""

from __future__ import annotations

import json
from collections import Counter
from functools import cache
from itertools import combinations
from math import comb
from pathlib import Path


K = 27
COLORS = K - 1
TARGET_CASES_53 = ((713, 48), (714, 50), (715, 52))


def masks_2x2() -> tuple[list[dict[str, int]], Counter[tuple[int, int]]]:
    """Enumerate 2x2 masks joining two two-vertex color classes.

    Bit order is yy, yx, xy, xx, where y is the unique neighbor of the
    root in its color class.  The returned polynomial uses exponents
    (edges minus one, distinguished-degree excess).
    """
    records: list[dict[str, int]] = []
    polynomial: Counter[tuple[int, int]] = Counter()
    for mask in range(1 << 4):
        yy, yx, xy, xx = ((mask >> bit) & 1 for bit in range(4))
        connected = bool(yy or (yx and xx and xy))
        if not connected:
            continue
        edges = yy + yx + xy + xx
        distinguished_excess = 2 * yy + yx + xy - 2
        assert distinguished_excess >= 0
        records.append(
            {
                "mask": mask,
                "edges": edges,
                "distinguished_excess": distinguished_excess,
            }
        )
        polynomial[(edges - 1, distinguished_excess)] += 1
    return records, polynomial


def masks_3x2() -> tuple[list[dict[str, int]], Counter[tuple[int, int]]]:
    """Enumerate masks joining the unique triple class to a pair class.

    Bit order is y0-y, y0-x, a-y, a-x, b-y, b-x.  Vertices y0 and y are
    the unique root-neighbors.  The polynomial exponents have the same
    meaning as in masks_2x2().
    """
    records: list[dict[str, int]] = []
    polynomial: Counter[tuple[int, int]] = Counter()
    for mask in range(1 << 6):
        yy, yx, ay, ax, by, bx = ((mask >> bit) & 1 for bit in range(6))
        connected = bool(yy or (yx and ((ay and ax) or (by and bx))))
        if not connected:
            continue
        edges = yy + yx + ay + ax + by + bx
        distinguished_excess = 2 * yy + yx + ay + by - 2
        assert distinguished_excess >= 0
        records.append(
            {
                "mask": mask,
                "edges": edges,
                "distinguished_excess": distinguished_excess,
            }
        )
        polynomial[(edges - 1, distinguished_excess)] += 1
    return records, polynomial


@cache
def pair_coefficient(blocks: int, weight: int, excess: int) -> int:
    """Coefficient [x^weight u^excess] P_2(x,u)^blocks.

    Choose q indirect masks.  Every remaining direct mask independently
    chooses its xx edge and its two root-neighbor incidences.
    """
    total = 0
    for q in range(blocks + 1):
        direct = blocks - q
        plain = weight - 2 * q - excess
        if 0 <= plain <= direct and excess <= 2 * direct:
            total += comb(blocks, q) * comb(direct, plain) * comb(2 * direct, excess)
    return total


def power_distribution(
    polynomial: Counter[tuple[int, int]],
    power: int,
    max_weight: int,
    max_excess: int,
) -> dict[tuple[int, int], int]:
    """Small exact bivariate DP, used only for the 25 triple-pair blocks."""
    distribution: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(power):
        new: dict[tuple[int, int], int] = {}
        for (weight, excess), count in distribution.items():
            for (dw, de), multiplicity in polynomial.items():
                key = (weight + dw, excess + de)
                if key[0] <= max_weight and key[1] <= max_excess:
                    new[key] = new.get(key, 0) + count * multiplicity
        distribution = new
    return distribution


def count_order53(m: int, total_excess: int) -> int:
    blocks = comb(COLORS, 2)
    weight = m - COLORS - blocks
    return sum(pair_coefficient(blocks, weight, d) for d in range(total_excess + 1))


def count_order54(poly3: Counter[tuple[int, int]]) -> int:
    pair_blocks = comb(COLORS - 1, 2)
    triple_blocks = COLORS - 1
    all_blocks = pair_blocks + triple_blocks
    weight = 726 - COLORS - all_blocks
    total_excess = 48
    triples = power_distribution(poly3, triple_blocks, weight, total_excess)
    total = 0
    for (triple_weight, triple_excess), multiplicity in triples.items():
        pair_weight = weight - triple_weight
        if pair_weight < 0:
            continue
        for pair_excess in range(total_excess - triple_excess + 1):
            total += multiplicity * pair_coefficient(
                pair_blocks, pair_weight, pair_excess
            )
    return total


def edge(a: str, b: str) -> frozenset[str]:
    assert a != b
    return frozenset((a, b))


def add_clique(edges: set[frozenset[str]], vertices: list[str]) -> None:
    for a, b in combinations(vertices, 2):
        edges.add(edge(a, b))


def e_family_graph(a_size: int, b_size: int):
    """Construct the Kostochka--Stiebitz E_27 member with |A2|=a, |B2|=b."""
    assert 1 <= a_size < COLORS
    assert 1 <= b_size < COLORS
    assert a_size + b_size <= COLORS
    a1 = [f"a1_{i}" for i in range(COLORS - a_size)]
    a2 = [f"a2_{i}" for i in range(a_size)]
    b1 = [f"b1_{i}" for i in range(COLORS - b_size)]
    b2 = [f"b2_{i}" for i in range(b_size)]
    c = "c"
    vertices = a1 + a2 + b1 + b2 + [c]
    edges: set[frozenset[str]] = set()
    add_clique(edges, a1 + a2)
    add_clique(edges, b1 + b2)
    for x in a2:
        for y in b2:
            edges.add(edge(x, y))
    for x in a1 + b1:
        edges.add(edge(c, x))
    return vertices, edges, a1, a2, b1, b2, c


def check_subdivision(
    vertices: list[str],
    edges: set[frozenset[str]],
    branches: list[str],
    routed_paths: list[list[str]],
) -> None:
    """Check that direct edges plus routed paths form a subdivision."""
    assert len(branches) == K and len(set(branches)) == K
    assert set(branches) <= set(vertices)
    branch_set = set(branches)
    missing = {
        frozenset((a, b))
        for a, b in combinations(branches, 2)
        if edge(a, b) not in edges
    }
    path_pairs: set[frozenset[str]] = set()
    used_internal: set[str] = set()
    for path in routed_paths:
        assert len(path) >= 3
        assert path[0] in branch_set and path[-1] in branch_set
        pair = frozenset((path[0], path[-1]))
        assert pair not in path_pairs
        path_pairs.add(pair)
        assert all(edge(x, y) in edges for x, y in zip(path, path[1:]))
        internal = set(path[1:-1])
        assert len(internal) == len(path) - 2
        assert not (internal & branch_set)
        assert not (internal & used_internal)
        used_internal.update(internal)
    assert path_pairs == missing


def verify_e_family_certificates() -> list[tuple[int, int, int, int]]:
    certificate_path = Path(__file__).with_name("certificate.json")
    certificate = json.loads(certificate_path.read_text())
    representatives = []
    checked_ordered = []
    for item in certificate["representatives"]:
        representative = (item["a_size"], item["b_size"])
        assert representative[0] <= representative[1]
        representative_paths = None
        for a_size, b_size in (representative, representative[::-1]):
            vertices, edges, a1, a2, b1, b2, c = e_family_graph(a_size, b_size)
            if a_size <= b_size:
                assert a_size <= len(b1)  # follows from a+b <= 26
                branches = a1 + a2 + [c]
                paths = [[c, b1[i], b2[i], a2[i]] for i in range(a_size)]
            else:
                assert b_size <= len(a1)
                branches = b1 + b2 + [c]
                paths = [[c, a1[i], a2[i], b2[i]] for i in range(b_size)]
            check_subdivision(vertices, edges, branches, paths)

            m = len(edges)
            assert len(vertices) == 53
            assert m == 701 + (a_size - 1) * (b_size - 1)
            assert m == item["edges"]
            checked_ordered.append((a_size, b_size, m, len(paths)))
            if (a_size, b_size) == representative:
                representative_paths = len(paths)
        assert representative_paths is not None
        representatives.append((*representative, item["edges"], representative_paths))

    assert representatives == [
        (2, 13, 713, 2),
        (3, 7, 713, 3),
        (4, 5, 713, 4),
        (2, 14, 714, 2),
        (2, 15, 715, 2),
        (3, 8, 715, 3),
    ]
    assert len(checked_ordered) == 12 and len(set(checked_ordered)) == 12
    return representatives


def main() -> None:
    masks2, poly2 = masks_2x2()
    masks3, poly3 = masks_3x2()
    assert len(masks2) == 9
    assert len(masks3) == 39
    assert poly2 == Counter(
        {
            (0, 0): 1,
            (1, 0): 1,
            (1, 1): 2,
            (2, 0): 1,
            (2, 1): 2,
            (2, 2): 1,
            (3, 2): 1,
        }
    )
    assert poly3 == Counter(
        {
            (0, 0): 1,
            (1, 0): 2,
            (1, 1): 3,
            (2, 0): 3,
            (2, 1): 6,
            (2, 2): 3,
            (3, 0): 2,
            (3, 1): 5,
            (3, 2): 6,
            (3, 3): 1,
            (4, 1): 1,
            (4, 2): 3,
            (4, 3): 2,
            (5, 3): 1,
        }
    )

    counts = {}
    for m, excess in TARGET_CASES_53:
        counts[(53, m)] = count_order53(m, excess)
    counts[(54, 726)] = count_order54(poly3)
    expected = json.loads(Path(__file__).with_name("certificate.json").read_text())[
        "state_counts"
    ]
    for (n, m), count in counts.items():
        assert str(count) == expected[f"{n},{m}"]

    checked = verify_e_family_certificates()
    print("PASS: direct mask enumeration gives 9 pair-pair and 39 triple-pair states")
    for (n, m), count in counts.items():
        print(
            f"n={n}, m={m}: edge/excess-filtered labelled states={count} "
            f"(decimal digits={len(str(count))}, bit_length={count.bit_length()})"
        )
    print(
        "PASS: six E_27 unordered parameter types (12 ordered parameter pairs) at "
        "m=713,714,715 have explicit topological K_27 certificates"
    )
    for a_size, b_size, m, paths in checked:
        print(f"  (|A2|,|B2|)=({a_size},{b_size}), m={m}, routed_paths={paths}")


if __name__ == "__main__":
    main()
