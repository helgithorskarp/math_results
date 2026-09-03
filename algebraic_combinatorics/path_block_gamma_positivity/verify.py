#!/usr/bin/env python3
"""Exact finite checks for gamma-positivity of bipartite clique blow-ups.

The universal result is proved in README.md.  This script checks, from the
definitions, that the relevant h*-polynomials agree with descent enumerators
of the graded posets used in the proof.  It also converts the resulting
polynomials to the gamma basis using exact Python integers.
"""

from __future__ import annotations

from functools import cache
from itertools import product
from math import comb
from typing import Callable, Iterable


Polynomial = tuple[int, ...]
Edge = tuple[int, int]


def block_weight(a: int, height: int) -> int:
    """Number of weak a-compositions of ``height``."""
    return comb(height + a - 1, a - 1)


def path_lattice_count(m: int, a: int, q: int) -> int:
    """Count lattice points in q times the (m,a) path block polytope."""
    weights = [block_weight(a, r) for r in range(q + 1)]
    state = weights[:]
    for _ in range(1, m):
        prefix: list[int] = []
        running = 0
        for value in state:
            running += value
            prefix.append(running)
        state = [weights[s] * prefix[q - s] for s in range(q + 1)]
    return sum(state)


def cycle_lattice_count(m: int, a: int, q: int) -> int:
    """Count lattice points for the cyclic adjacent-block constraints."""
    weights = [block_weight(a, r) for r in range(q + 1)]
    total = 0
    for first in range(q + 1):
        state = [0] * (q + 1)
        state[first] = weights[first]
        for _ in range(1, m):
            prefix: list[int] = []
            running = 0
            for value in state:
                running += value
                prefix.append(running)
            state = [weights[s] * prefix[q - s] for s in range(q + 1)]
        total += sum(state[last] for last in range(q + 1 - first))
    return total


def graph_lattice_count(
    vertex_count: int, a: int, edges: Iterable[Edge], q: int
) -> int:
    """Definition-level count for a small clique blow-up of a graph."""
    edge_list = tuple(edges)
    weights = [block_weight(a, r) for r in range(q + 1)]
    total = 0
    for heights in product(range(q + 1), repeat=vertex_count):
        if all(heights[u] + heights[v] <= q for u, v in edge_list):
            contribution = 1
            for height in heights:
                contribution *= weights[height]
            total += contribution
    return total


def hstar(dimension: int, counter: Callable[[int], int]) -> Polynomial:
    """Recover h* from L(0),...,L(d) using finite differences."""
    lattice_counts = [counter(q) for q in range(dimension + 1)]
    coefficients = []
    for j in range(dimension + 1):
        coefficients.append(
            sum(
                (-1) ** i * comb(dimension + 1, i) * lattice_counts[j - i]
                for i in range(j + 1)
            )
        )
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    assert all(value >= 0 for value in coefficients)
    return tuple(coefficients)


def gamma_coefficients(polynomial: Polynomial, degree: int) -> Polynomial:
    """Expand a palindromic polynomial in z^j(1+z)^(degree-2j)."""
    padded = polynomial + (0,) * (degree + 1 - len(polynomial))
    assert len(padded) == degree + 1
    assert padded == padded[::-1]

    gamma: list[int] = []
    for j in range(degree // 2 + 1):
        already_accounted_for = sum(
            gamma[i] * comb(degree - 2 * i, j - i) for i in range(j)
        )
        gamma.append(padded[j] - already_accounted_for)

    reconstruction = [0] * (degree + 1)
    for j, value in enumerate(gamma):
        for k in range(degree - 2 * j + 1):
            reconstruction[j + k] += value * comb(degree - 2 * j, k)
    assert tuple(reconstruction) == padded
    return tuple(gamma)


def bipartite_poset_predecessors(
    vertex_count: int, a: int, edges: Iterable[Edge], left: Iterable[int]
) -> tuple[int, ...]:
    """Build predecessor masks under a canonical natural labeling.

    Vertices in ``left`` are the low blocks.  Every low block precedes all
    adjacent high blocks.  Each block is itself a chain.  Labels list all low
    blocks first and are therefore order-preserving.
    """
    left_set = frozenset(left)
    right_set = frozenset(range(vertex_count)) - left_set
    assert left_set and right_set

    edge_list: list[Edge] = []
    for u, v in edges:
        if u in right_set and v in left_set:
            u, v = v, u
        assert u in left_set and v in right_set
        edge_list.append((u, v))

    block_order = sorted(left_set) + sorted(right_set)
    nodes: dict[tuple[int, int], int] = {}
    for block in block_order:
        for level in range(a):
            nodes[block, level] = len(nodes)

    predecessors = [0] * (a * vertex_count)
    for block in range(vertex_count):
        for level in range(1, a):
            predecessors[nodes[block, level]] |= 1 << nodes[block, level - 1]
    for low, high in edge_list:
        predecessors[nodes[high, 0]] |= 1 << nodes[low, a - 1]
    return tuple(predecessors)


def descent_polynomial(predecessors: tuple[int, ...]) -> Polynomial:
    """Enumerate linear extensions by descents with ideal-state dynamic programming."""
    size = len(predecessors)
    full_mask = (1 << size) - 1

    @cache
    def extend(mask: int, last: int) -> Polynomial:
        if mask == full_mask:
            return (1,)

        total = [0] * size
        for label, required in enumerate(predecessors):
            bit = 1 << label
            if mask & bit or required & ~mask:
                continue
            tail = extend(mask | bit, label)
            shift = int(last > label) if last >= 0 else 0
            for descents, count in enumerate(tail):
                total[descents + shift] += count

        while len(total) > 1 and total[-1] == 0:
            total.pop()
        return tuple(total)

    return extend(0, -1)


def path_edges(m: int) -> tuple[Edge, ...]:
    return tuple((i, i + 1) for i in range(m - 1))


def cycle_edges(m: int) -> tuple[Edge, ...]:
    return path_edges(m) + ((m - 1, 0),)


def check_path_examples() -> None:
    published: dict[tuple[int, int], Polynomial] = {
        (3, 1): (1, 1),
        (4, 1): (1, 3, 1),
        (5, 1): (1, 7, 7, 1),
        (3, 2): (1, 4, 1),
        (4, 2): (1, 12, 27, 12, 1),
        (5, 2): (1, 32, 203, 368, 203, 32, 1),
        (3, 3): (1, 9, 9, 1),
        (4, 3): (1, 27, 162, 282, 162, 27, 1),
    }
    for (m, a), expected in published.items():
        actual = hstar(a * m, lambda q, m=m, a=a: path_lattice_count(m, a, q))
        assert actual == expected
    print(f"published path h* examples: {len(published)} passed")


def check_descent_bridge() -> None:
    path_cases = [(m, a) for a, upper in ((1, 8), (2, 6), (3, 4)) for m in range(2, upper + 1)]
    for m, a in path_cases:
        polynomial = hstar(a * m, lambda q, m=m, a=a: path_lattice_count(m, a, q))
        poset = bipartite_poset_predecessors(m, a, path_edges(m), range(0, m, 2))
        assert polynomial == descent_polynomial(poset)
    print(f"path Ehrhart/descent comparisons: {len(path_cases)} passed")

    cycle_cases = [(m, a) for a in range(1, 3) for m in (4, 6)]
    for m, a in cycle_cases:
        polynomial = hstar(a * m, lambda q, m=m, a=a: cycle_lattice_count(m, a, q))
        poset = bipartite_poset_predecessors(m, a, cycle_edges(m), range(0, m, 2))
        assert polynomial == descent_polynomial(poset)
    print(f"even-cycle Ehrhart/descent comparisons: {len(cycle_cases)} passed")

    generic_cases = (
        (4, 1, ((0, 1), (0, 2), (0, 3)), (0,), "K_1,3"),
        (4, 2, ((0, 1), (0, 2), (0, 3)), (0,), "K_1,3[K_2]"),
        (5, 1, ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)), (0, 1), "K_2,3"),
    )
    for vertices, a, edges, left, _name in generic_cases:
        polynomial = hstar(
            a * vertices,
            lambda q, vertices=vertices, a=a, edges=edges: graph_lattice_count(
                vertices, a, edges, q
            ),
        )
        poset = bipartite_poset_predecessors(vertices, a, edges, left)
        assert polynomial == descent_polynomial(poset)
        assert all(value >= 0 for value in gamma_coefficients(polynomial, a * (vertices - 2)))
    print(f"non-path bipartite blow-up comparisons: {len(generic_cases)} passed")


def check_gamma_sweep() -> None:
    path_cases = [(m, a) for a in range(1, 6) for m in range(2, 9)]
    for m, a in path_cases:
        polynomial = hstar(a * m, lambda q, m=m, a=a: path_lattice_count(m, a, q))
        gamma = gamma_coefficients(polynomial, a * (m - 2))
        assert all(value >= 0 for value in gamma)
    print(f"path gamma-basis checks: {len(path_cases)} passed")

    cycle_cases = [(m, a) for a in range(1, 4) for m in (4, 6, 8)]
    for m, a in cycle_cases:
        polynomial = hstar(a * m, lambda q, m=m, a=a: cycle_lattice_count(m, a, q))
        gamma = gamma_coefficients(polynomial, a * (m - 2))
        assert all(value >= 0 for value in gamma)
    print(f"even-cycle gamma-basis checks: {len(cycle_cases)} passed")

    samples = ((3, 2), (4, 2), (5, 2), (4, 3))
    for m, a in samples:
        polynomial = hstar(a * m, lambda q, m=m, a=a: path_lattice_count(m, a, q))
        gamma = gamma_coefficients(polynomial, a * (m - 2))
        print(f"path (m={m}, a={a}): h*={list(polynomial)} gamma={list(gamma)}")


def main() -> None:
    check_path_examples()
    check_descent_bridge()
    check_gamma_sweep()
    print("all exact checks passed")


if __name__ == "__main__":
    main()
