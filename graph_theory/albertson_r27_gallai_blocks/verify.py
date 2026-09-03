#!/usr/bin/env python3
"""Exact checks for the Albertson r=27 Gallai-block reduction."""

from dataclasses import dataclass
from math import comb


K = 27


@dataclass(frozen=True)
class Row:
    n: int
    m: int
    excess: int
    first_allowed_h: int


ROWS = (
    Row(53, 713, 48, 8),
    Row(53, 714, 50, 8),
    Row(53, 715, 52, 9),
    Row(54, 726, 48, 10),
)


def minimum_large_block_order(n: int, h: int) -> int:
    if n == 2 * K - 1:
        # At least K-1-h fully-low pair classes, plus the root.
        return K - h
    if n == 2 * K:
        # At least K-h-2 fully-low pair classes, plus the root.
        return K - h - 1
    raise ValueError(n)


def block_pairs(n: int, h: int):
    low = n - h
    lower = minimum_large_block_order(n, h)
    for a in range(lower, K):
        b = low - a
        if lower <= b <= K - 1 and a <= b:
            yield a, b


def excess_cap(n: int, h: int, a: int, b: int) -> int:
    low = n - h
    low_edges = comb(a, 2) + comb(b, 2)
    return (
        (K - 1) * low
        - 2 * low_edges
        + 2 * comb(h, 2)
        - (K - 1) * h
    )


def balanced_cap(n: int, h: int) -> tuple[int, int, int]:
    low = n - h
    a = low // 2
    b = low - a
    return excess_cap(n, h, a, b), a, b


def check_block_forcing_preconditions(n: int, h: int) -> None:
    low = n - h
    s = minimum_large_block_order(n, h)
    pair_count = K - 1 if n == 2 * K - 1 else K - 2
    fully_low = s - 1
    assert fully_low >= 3
    assert fully_low <= pair_count
    # Large clique blocks are vertex-disjoint, at least two are needed,
    # and three cannot fit.
    assert 2 * (s - 1) > K - 1
    assert low > K - 1
    assert 3 * s > low


def check_structural_range(n: int, h: int) -> None:
    check_block_forcing_preconditions(n, h)
    assert list(block_pairs(n, h))


def exact_maximum(n: int, h: int) -> tuple[int, tuple[int, int]]:
    candidates = [(excess_cap(n, h, a, b), (a, b)) for a, b in block_pairs(n, h)]
    assert candidates
    result = max(candidates)
    # Independent convexity check: the balanced integer pair is feasible
    # and has the same value as the full enumeration.
    closed, a, b = balanced_cap(n, h)
    assert (a, b) in [pair for _, pair in candidates]
    assert result == (closed, (a, b))
    return result


def first_feasible_h(row: Row) -> int:
    for h in range(1, K):
        pairs = list(block_pairs(row.n, h))
        if not pairs:
            check_block_forcing_preconditions(row.n, h)
            continue
        # The structural argument is used only while its three fully-low
        # pairs and block-disjointness/count inequalities hold.
        try:
            check_structural_range(row.n, h)
        except AssertionError:
            continue
        cap, _ = exact_maximum(row.n, h)
        if cap >= row.excess:
            return h
    raise AssertionError("no feasible h found in proved range")


def defect_profiles(row: Row, h: int):
    """Return (a,b,t,r), where t and r are extra-low/missing-high edges."""
    profiles = []
    for a, b in block_pairs(row.n, h):
        cap = excess_cap(row.n, h, a, b)
        defect = cap - row.excess
        if defect < 0 or defect % 2:
            continue
        # In a Gallai forest whose two large blocks cover L, at most one
        # extra low edge can occur: it is the bridge between the blocks.
        for t in range(2):
            r = defect // 2 - t
            if r >= 0:
                profiles.append((a, b, t, r))
    return profiles


def verify_frontier():
    for row in ROWS:
        assert row.excess == 2 * row.m - (K - 1) * row.n
        found = first_feasible_h(row)
        assert found == row.first_allowed_h
        for h in range(1, found):
            pairs = list(block_pairs(row.n, h))
            if not pairs:
                check_block_forcing_preconditions(row.n, h)
                continue
            check_structural_range(row.n, h)
            cap, _ = exact_maximum(row.n, h)
            assert cap < row.excess


def verify_boundary_profiles():
    expected = {
        (53, 713): [(22, 23, 0, 1), (22, 23, 1, 0)],
        (53, 714): [(22, 23, 0, 0)],
        (53, 715): [
            (21, 23, 0, 2),
            (21, 23, 1, 1),
            (22, 22, 0, 3),
            (22, 22, 1, 2),
        ],
        (54, 726): [
            (21, 23, 0, 0),
            (22, 22, 0, 1),
            (22, 22, 1, 0),
        ],
    }
    actual = {}
    for row in ROWS:
        profiles = defect_profiles(row, row.first_allowed_h)
        actual[(row.n, row.m)] = profiles
        assert profiles == expected[(row.n, row.m)]
    return actual


def display_caps(n: int, last_h: int):
    values = []
    for h in range(1, last_h + 1):
        pairs = list(block_pairs(n, h))
        if not pairs:
            continue
        check_structural_range(n, h)
        cap, pair = exact_maximum(n, h)
        values.append((h, cap, pair))
    return values


def main():
    verify_frontier()
    profiles = verify_boundary_profiles()
    caps53 = display_caps(53, 9)
    caps54 = display_caps(54, 9)
    print("PASS: Gallai-block count and degree-support bounds")
    print("order 53 caps:", ", ".join(f"h={h}:{cap}@{a}+{b}" for h, cap, (a, b) in caps53))
    print("order 54 caps:", ", ".join(f"h={h}:{cap}@{a}+{b}" for h, cap, (a, b) in caps54))
    print("frontier high-vertex lower bounds:")
    for row in ROWS:
        print(f"  (n,m)=({row.n},{row.m}): h>={row.first_allowed_h}")
    print("PASS: exact minimum-h boundary profiles")
    for key, rows in profiles.items():
        encoded = ", ".join(f"({a},{b};t={t},r={r})" for a, b, t, r in rows)
        print(f"  {key}: {encoded}")


if __name__ == "__main__":
    main()
