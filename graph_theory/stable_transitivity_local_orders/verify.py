#!/usr/bin/env python3
"""Exact audit for the stable-transitivity theorem on local orders.

The universal proof is in THEOREM.md.  This checker exhausts all labelled
tournaments through order six and verifies the constructive identity for
every root.  It also checks independent cut-switch and carousel families.
"""

from __future__ import annotations

import itertools
from functools import lru_cache
from typing import Iterable, Sequence

Profile = tuple[int, ...]


@lru_cache(maxsize=None)
def pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((u, v) for u in range(n) for v in range(u + 1, n))


@lru_cache(maxsize=None)
def pair_index(n: int) -> dict[tuple[int, int], int]:
    return {pair: i for i, pair in enumerate(pairs(n))}


def arc(profile: Profile, n: int, u: int, v: int) -> bool:
    """Return whether the tournament profile contains u->v."""
    assert u != v and len(profile) == len(pairs(n))
    if u < v:
        return bool(profile[pair_index(n)[(u, v)]])
    return not bool(profile[pair_index(n)[(v, u)]])


def order_profile(order: Sequence[int]) -> Profile:
    n = len(order)
    assert sorted(order) == list(range(n))
    position = [0] * n
    for i, vertex in enumerate(order):
        position[vertex] = i
    return tuple(int(position[u] < position[v]) for u, v in pairs(n))


def transitive_order(profile: Profile, n: int, vertices: Iterable[int]) -> tuple[int, ...] | None:
    """Return the unique forward order of an induced tournament, if any."""
    subset = tuple(vertices)
    assert len(set(subset)) == len(subset)
    assert all(0 <= vertex < n for vertex in subset)
    outdegree = {
        u: sum(arc(profile, n, u, w) for w in subset if w != u)
        for u in subset
    }
    order = tuple(sorted(subset, key=lambda u: (-outdegree[u], u)))
    if any(not arc(profile, n, u, v) for i, u in enumerate(order) for v in order[i + 1 :]):
        return None
    return order


def is_transitive(profile: Profile, n: int) -> bool:
    return transitive_order(profile, n, range(n)) is not None


def is_locally_transitive(profile: Profile, n: int) -> bool:
    for root in range(n):
        out = [u for u in range(n) if u != root and arc(profile, n, root, u)]
        inn = [u for u in range(n) if u != root and arc(profile, n, u, root)]
        if transitive_order(profile, n, out) is None:
            return False
        if transitive_order(profile, n, inn) is None:
            return False
    return True


def switch_cut(profile: Profile, n: int, left: Iterable[int]) -> Profile:
    left_set = frozenset(left)
    assert left_set <= frozenset(range(n))
    return tuple(
        value if ((u in left_set) == (v in left_set)) else 1 - value
        for value, (u, v) in zip(profile, pairs(n))
    )


def rooted_witness(profile: Profile, n: int, root: int) -> tuple[tuple[int, ...], ...]:
    """Construct (P-order,A-order,B-order) from the proof."""
    assert is_locally_transitive(profile, n)
    left = frozenset(
        [root] + [u for u in range(n) if u != root and arc(profile, n, root, u)]
    )
    right = frozenset(range(n)) - left
    switched = switch_cut(profile, n, left)
    p_order = transitive_order(switched, n, range(n))
    assert p_order is not None
    left_order = tuple(u for u in p_order if u in left)
    right_order = tuple(u for u in p_order if u in right)
    a_order = left_order + right_order
    b_order = right_order + left_order
    lhs = tuple(x + y for x, y in zip(profile, order_profile(p_order)))
    rhs = tuple(x + y for x, y in zip(order_profile(a_order), order_profile(b_order)))
    assert lhs == rhs
    return p_order, a_order, b_order


def carousel(q: int) -> Profile:
    assert q >= 1
    n = 2 * q + 1
    return tuple(int(1 <= ((v - u) % n) <= q) for u, v in pairs(n))


def carousel_orders(q: int) -> tuple[tuple[int, ...], ...]:
    assert q >= 1
    n = 2 * q + 1
    p: list[int] = []
    for i in range(q):
        p.extend((i, q + 1 + i))
    p.append(q)
    a = tuple(range(n))
    b = tuple(range(q + 1, n)) + tuple(range(q + 1))
    return tuple(p), a, b


def audit_all_tournaments(max_n: int = 6) -> tuple[int, int, int, int]:
    total = local = transitive = rooted = 0
    for n in range(1, max_n + 1):
        for profile in itertools.product((0, 1), repeat=len(pairs(n))):
            total += 1
            if not is_locally_transitive(profile, n):
                continue
            local += 1
            if is_transitive(profile, n):
                transitive += 1
            for root in range(n):
                rooted_witness(profile, n, root)
                rooted += 1
    return total, local, transitive, rooted


def audit_cut_switches(max_n: int = 12) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        base = order_profile(tuple(range(n)))
        # Complements give the same switched tournament; require vertex 0 on
        # the chosen side to make this an exact nonredundant enumeration.
        for mask in range(1 << max(0, n - 1)):
            left = {0}
            left.update(i + 1 for i in range(n - 1) if (mask >> i) & 1)
            switched = switch_cut(base, n, left)
            assert is_locally_transitive(switched, n)
            checked += 1
    return checked


def audit_carousels(max_q: int = 256) -> int:
    for q in range(1, max_q + 1):
        profile = carousel(q)
        p, a, b = carousel_orders(q)
        lhs = tuple(x + y for x, y in zip(profile, order_profile(p)))
        rhs = tuple(x + y for x, y in zip(order_profile(a), order_profile(b)))
        assert lhs == rhs
        assert not is_transitive(profile, 2 * q + 1)
    return max_q


def main() -> None:
    total, local, transitive, rooted = audit_all_tournaments()
    cut_switches = audit_cut_switches()
    carousels = audit_carousels()
    print(f"labelled_tournaments_checked={total}")
    print(f"locally_transitive_tournaments={local}")
    print(f"transitive_tournaments={transitive}")
    print(f"rooted_witnesses_checked={rooted}")
    print(f"canonical_cut_switches_checked={cut_switches}")
    print(f"carousel_formulas_checked={carousels}")
    print("status=ok")


if __name__ == "__main__":
    main()
