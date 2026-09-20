#!/usr/bin/env python3
"""Definition-level finite audit for the stable-transitivity substitution law.

The universal proof is in THEOREM.md.  This program independently enumerates
small k-tournaments, computes their stable-transitivity numbers from the
definition, and checks both the substitution and strong-component formulas.
It uses exact integer tuples only; there is no solver or randomness.
"""

from __future__ import annotations

import itertools
from functools import lru_cache
from typing import Iterator, Sequence

Profile = tuple[int, ...]


@lru_cache(maxsize=None)
def pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((u, v) for u in range(n) for v in range(u + 1, n))


@lru_cache(maxsize=None)
def pair_index(n: int) -> dict[tuple[int, int], int]:
    return {pair: i for i, pair in enumerate(pairs(n))}


def add_profiles(left: Profile, right: Profile) -> Profile:
    assert len(left) == len(right)
    return tuple(a + b for a, b in zip(left, right))


def order_profile(order: Sequence[int]) -> Profile:
    """Counts u->v for u<v in the transitive tournament of ``order``."""
    n = len(order)
    assert sorted(order) == list(range(n))
    position = [0] * n
    for i, vertex in enumerate(order):
        position[vertex] = i
    return tuple(int(position[u] < position[v]) for u, v in pairs(n))


@lru_cache(maxsize=None)
def order_profiles(n: int) -> tuple[Profile, ...]:
    return tuple(order_profile(order) for order in itertools.permutations(range(n)))


@lru_cache(maxsize=None)
def ttd_profiles(n: int, degree: int) -> frozenset[Profile]:
    """All degree-``degree`` profiles that are sums of total orders."""
    assert n >= 1 and degree >= 0
    zero = (0,) * len(pairs(n))
    if degree == 0:
        return frozenset({zero})
    previous = ttd_profiles(n, degree - 1)
    return frozenset(
        add_profiles(profile, order)
        for profile in previous
        for order in order_profiles(n)
    )


@lru_cache(maxsize=None)
def stable_number(n: int, degree: int, profile: Profile) -> int:
    """Compute m(profile) exactly for the small audit ranges.

    The search bound ``degree`` suffices in the audited ranges and is attained
    by the doubled directed triangle when degree=2.  Failure to find a value is
    fatal rather than silently treated as a larger answer.
    """
    assert len(profile) == len(pairs(n))
    assert all(0 <= entry <= degree for entry in profile)
    for added_degree in range(degree + 1):
        targets = ttd_profiles(n, degree + added_degree)
        for added in ttd_profiles(n, added_degree):
            if add_profiles(profile, added) in targets:
                return added_degree
    raise AssertionError(
        f"audit bound failed for n={n}, degree={degree}, profile={profile}"
    )


def all_profiles(n: int, degree: int) -> Iterator[Profile]:
    yield from itertools.product(range(degree + 1), repeat=len(pairs(n)))


def positive_compositions(total: int) -> Iterator[tuple[int, ...]]:
    """All ordered compositions of ``total``."""
    if total == 0:
        yield ()
        return
    for first in range(1, total + 1):
        for tail in positive_compositions(total - first):
            yield (first,) + tail


def substitute(
    quotient: Profile,
    blocks: Sequence[Profile],
    sizes: Sequence[int],
    degree: int,
) -> Profile:
    """Return the profile of quotient[block_0,...,block_(r-1)]."""
    r = len(sizes)
    assert r == len(blocks)
    assert len(quotient) == len(pairs(r))
    assert all(len(block) == len(pairs(size)) for block, size in zip(blocks, sizes))
    assert all(0 <= entry <= degree for entry in quotient)

    offsets = [0]
    for size in sizes:
        offsets.append(offsets[-1] + size)
    n = offsets[-1]
    out = [0] * len(pairs(n))
    out_index = pair_index(n)

    for block_index, (block, size) in enumerate(zip(blocks, sizes)):
        offset = offsets[block_index]
        for value, (u, v) in zip(block, pairs(size)):
            out[out_index[(offset + u, offset + v)]] = value

    quotient_index = pair_index(r)
    for i in range(r):
        for j in range(i + 1, r):
            value = quotient[quotient_index[(i, j)]]
            for u in range(offsets[i], offsets[i + 1]):
                for v in range(offsets[j], offsets[j + 1]):
                    out[out_index[(u, v)]] = value
    return tuple(out)


def support_sccs(profile: Profile, n: int, degree: int) -> tuple[tuple[int, ...], ...]:
    """Strong components of the positive-multiplicity support digraph."""
    index = pair_index(n)
    adjacency = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for u, v in pairs(n):
        uv = profile[index[(u, v)]]
        if uv > 0:
            adjacency[u].append(v)
            reverse[v].append(u)
        if uv < degree:
            adjacency[v].append(u)
            reverse[u].append(v)

    seen = [False] * n
    finish: list[int] = []

    def visit(u: int) -> None:
        seen[u] = True
        for v in adjacency[u]:
            if not seen[v]:
                visit(v)
        finish.append(u)

    for vertex in range(n):
        if not seen[vertex]:
            visit(vertex)

    seen = [False] * n
    components: list[tuple[int, ...]] = []

    def collect(u: int, component: list[int]) -> None:
        seen[u] = True
        component.append(u)
        for v in reverse[u]:
            if not seen[v]:
                collect(v, component)

    for vertex in reversed(finish):
        if not seen[vertex]:
            component: list[int] = []
            collect(vertex, component)
            components.append(tuple(sorted(component)))
    return tuple(components)


def restrict_increasing(profile: Profile, component: Sequence[int], n: int) -> Profile:
    assert tuple(component) == tuple(sorted(component))
    index = pair_index(n)
    return tuple(profile[index[(component[i], component[j])]] for i, j in pairs(len(component)))


def audit_substitutions(max_n: int, degree: int) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        for sizes in positive_compositions(n):
            r = len(sizes)
            quotient_profiles = all_profiles(r, degree)
            block_spaces = [tuple(all_profiles(size, degree)) for size in sizes]
            for quotient in quotient_profiles:
                quotient_m = stable_number(r, degree, quotient)
                for blocks in itertools.product(*block_spaces):
                    expanded = substitute(quotient, blocks, sizes, degree)
                    expected = max(
                        [quotient_m]
                        + [
                            stable_number(size, degree, block)
                            for size, block in zip(sizes, blocks)
                        ]
                    )
                    actual = stable_number(n, degree, expanded)
                    assert actual == expected, (
                        n,
                        degree,
                        sizes,
                        quotient,
                        blocks,
                        actual,
                        expected,
                    )
                    checked += 1
    return checked


def audit_scc_localization(max_n: int, degree: int) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        for profile in all_profiles(n, degree):
            component_numbers = []
            for component in support_sccs(profile, n, degree):
                restricted = restrict_increasing(profile, component, n)
                component_numbers.append(stable_number(len(component), degree, restricted))
            expected = max(component_numbers, default=0)
            actual = stable_number(n, degree, profile)
            assert actual == expected, (n, degree, profile, actual, expected)
            checked += 1
    return checked


def main() -> None:
    ordinary_substitutions = audit_substitutions(max_n=5, degree=1)
    degree_two_substitutions = audit_substitutions(max_n=4, degree=2)
    ordinary_scc = audit_scc_localization(max_n=5, degree=1)
    degree_two_scc = audit_scc_localization(max_n=4, degree=2)

    print(f"ordinary_substitutions_checked={ordinary_substitutions}")
    print(f"degree_two_substitutions_checked={degree_two_substitutions}")
    print(f"ordinary_scc_profiles_checked={ordinary_scc}")
    print(f"degree_two_scc_profiles_checked={degree_two_scc}")
    print("theorem=substitution_max_and_scc_localization")
    print("status=PASS")


if __name__ == "__main__":
    main()
