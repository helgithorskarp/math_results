#!/usr/bin/env python3
"""Exact checks for direct-sum locality of the Ray--West correction."""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement, permutations


Permutation = tuple[int, ...]
Triple = tuple[Permutation, tuple[int, int], tuple[int, int]]


def active_site(w: Permutation, row: int, column: int) -> bool:
    n = len(w)
    return not (
        (column <= n and w[column - 1] == row)
        or (column > 1 and w[column - 2] == row)
    )


def active_triples(w: Permutation):
    sites = range(1, len(w) + 2)
    for rows in combinations_with_replacement(sites, 2):
        for columns in combinations_with_replacement(sites, 2):
            for rho in ((1, 2), (2, 1)):
                triple = (rho, rows, columns)
                if all(
                    active_site(w, rows[rho[j] - 1], columns[j])
                    for j in range(2)
                ):
                    yield triple


def insert(w: Permutation, triple: Triple) -> Permutation:
    rho, rows, columns = triple
    out: list[int | None] = [None] * (len(w) + 2)
    for column_rank, row_rank in enumerate(rho, start=1):
        full_column = columns[column_rank - 1] + column_rank - 1
        full_row = rows[row_rank - 1] + row_rank - 1
        out[full_column - 1] = full_row
    for old_column, old_row in enumerate(w, start=1):
        full_column = old_column + sum(c <= old_column for c in columns)
        full_row = old_row + sum(r <= old_row for r in rows)
        if out[full_column - 1] is not None:
            raise AssertionError("insertion collision")
        out[full_column - 1] = full_row
    answer = tuple(x for x in out if x is not None)
    if sorted(answer) != list(range(1, len(w) + 3)):
        raise AssertionError("not a permutation")
    return answer


@lru_cache(maxsize=None)
def j_value(w: Permutation) -> int:
    n = len(w)
    g2 = len({insert(w, triple) for triple in active_triples(w)})
    base = (n**4 + 2 * n**3 + n**2 + 4 * n + 4) // 2
    return base - g2


def direct_sum(left: Permutation, right: Permutation) -> Permutation:
    return left + tuple(len(left) + x for x in right)


def complement(w: Permutation) -> Permutation:
    n = len(w)
    return tuple(n + 1 - x for x in w)


def skew_sum(left: Permutation, right: Permutation) -> Permutation:
    return tuple(len(right) + x for x in left) + right


def left_down(w: Permutation) -> bool:
    b = w[0]
    return w[:b] == tuple(range(b, 0, -1))


def right_down(w: Permutation) -> bool:
    n = len(w)
    a = n + 1 - w[-1]
    return w[n - a :] == tuple(range(n, n - a, -1))


def left_up(w: Permutation) -> bool:
    n = len(w)
    b = n + 1 - w[0]
    return w[:b] == tuple(range(w[0], n + 1))


def right_up(w: Permutation) -> bool:
    a = w[-1]
    return w[len(w) - a :] == tuple(range(1, a + 1))


def separated(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return max(a) < min(b) or max(b) < min(a)


@lru_cache(maxsize=None)
def c_boundaries(w: Permutation) -> frozenset[int]:
    """Recover the Ray--West pattern-(C) boundary labels from collisions."""
    groups: dict[Permutation, list[Triple]] = defaultdict(list)
    for triple in active_triples(w):
        groups[insert(w, triple)].append(triple)
    answer: set[int] = set()
    for triples in groups.values():
        for triple in triples:
            _, rows, columns = triple
            is_left_c = any(
                rows < other[1]
                and separated(rows, other[1])
                and separated(columns, other[2])
                for other in triples
            )
            if not is_left_c:
                continue
            matches = []
            for p in range(1, len(w)):
                if w[p - 1] > w[p]:
                    if min(rows) == w[p] and max(columns) == p:
                        matches.append(p)
                elif min(rows) == w[p - 1] and min(columns) == p + 2:
                    matches.append(p)
            if len(matches) != 1:
                raise AssertionError((w, triple, matches))
            answer.add(matches[0])
    return frozenset(answer)


def junction_triples(left: Permutation, right: Permutation) -> tuple[Triple, Triple]:
    r = len(left)
    x = left[-1]
    y = r + right[0]
    first = ((1, 2), (x, r), (r + 2, y + 1))
    second = ((1, 2), (r + 2, y + 1), (x, r))
    return first, second


def verify_pair(left: Permutation, right: Permutation) -> tuple[int, int]:
    pi = direct_sum(left, right)
    j_left, j_right, j_pi = j_value(left), j_value(right), j_value(pi)
    bridge = int(right_down(left) and left_down(right))
    if j_pi != j_left + j_right + bridge:
        raise AssertionError((left, right, j_left, j_right, j_pi, bridge))

    boundaries = c_boundaries(pi)
    if (boundaries & set(range(1, len(left)))) != c_boundaries(left):
        raise AssertionError((left, right, "left locality"))
    shifted_right = {p - len(left) for p in boundaries if p > len(left)}
    if shifted_right != c_boundaries(right):
        raise AssertionError((left, right, "right locality"))
    if (len(left) in boundaries) != bool(bridge):
        raise AssertionError((left, right, "junction boundary"))

    first, second = junction_triples(left, right)
    explicit = all(
        active_site(pi, first[1][first[0][j] - 1], first[2][j])
        for j in range(2)
    ) and insert(pi, first) == insert(pi, second)
    if explicit != bool(bridge):
        raise AssertionError((left, right, "explicit junction", first, second))

    skew = skew_sum(left, right)
    skew_bridge = int(right_up(left) and left_up(right))
    if j_value(skew) != j_left + j_right + skew_bridge:
        raise AssertionError((left, right, "skew", skew_bridge))
    if skew != complement(direct_sum(complement(left), complement(right))):
        raise AssertionError((left, right, "complement dual"))
    return bridge, skew_bridge


def main() -> None:
    cache: dict[int, list[Permutation]] = {
        n: list(permutations(range(1, n + 1))) for n in range(1, 7)
    }
    pairs = direct_bridges = skew_bridges = 0
    for r in range(1, 5):
        for s in range(1, 5):
            for left in cache[r]:
                for right in cache[s]:
                    db, sb = verify_pair(left, right)
                    pairs += 1
                    direct_bridges += db
                    skew_bridges += sb
    print(
        f"exhaustive factor lengths <=4: {pairs} ordered pairs; "
        f"direct bridges={direct_bridges}; skew bridges={skew_bridges}"
    )

    one_sided = one_sided_bridges = 0
    singleton = (1,)
    for n in range(1, 7):
        for w in cache[n]:
            for left, right in ((w, singleton), (singleton, w)):
                db, _ = verify_pair(left, right)
                one_sided += 1
                one_sided_bridges += db
    print(
        f"one-sided factors through length 6: {one_sided} ordered pairs; "
        f"direct bridges={one_sided_bridges}"
    )

    block = (2, 4, 1, 3)
    current = block
    for t in range(1, 7):
        expected = 2 * t
        if j_value(current) != expected:
            raise AssertionError((t, current, j_value(current), expected))
        if any(abs(current[i] - current[i + 1]) == 1 for i in range(len(current) - 1)):
            raise AssertionError((t, "unexpected bond"))
        if t < 6:
            current = direct_sum(current, block)
    print("bondless family: verified j((2413) direct_sum^t)=2t for 1<=t<=6")
    print("all direct-sum, skew-sum, locality, and junction checks passed")


if __name__ == "__main__":
    main()
