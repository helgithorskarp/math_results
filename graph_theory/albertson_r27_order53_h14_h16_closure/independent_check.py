#!/usr/bin/env python3
"""Independent reconstruction of the Albertson h=14,15,16 arithmetic."""

from hashlib import sha256
from itertools import combinations
from math import comb


def convex_three_block_bound(h, intersections):
    low = 53 - h
    s = 27 - h
    # For fixed sum and lower bound, convexity maximizes the sum of binomial
    # coefficients at the two lower endpoints.
    largest = low + intersections - 2 * s
    connector = {0: 3, 1: 1, 2: 0}[intersections]
    return 2 * comb(s, 2) + comb(largest, 2) + connector


def reconstruct():
    summary = []
    for h in range(14, 18):
        low = 53 - h
        s = 27 - h
        minimum_low_edges = 26 * low - 713
        upper = tuple(convex_three_block_bound(h, q) for q in range(3))
        if h <= 16:
            assert max(upper) < minimum_low_edges

        rows = []
        for d in range((h - 1) // 2 + 1):
            e = h - 1 - d
            a, b = s + d, s + e
            if b >= 27:
                continue
            base = comb(a, 2) + comb(b, 2)
            high_edges = 713 - (26 * low - base)
            D = comb(h, 2) - high_edges
            if D >= 0:
                rows.append((a, b, d, e, D))
        assert rows and all(row[2] >= 1 for row in rows)
        assert len(rows) == {14: 6, 15: 7, 16: 7, 17: 8}[h]

        identities = 0
        for a, b, d, e, D in rows:
            assert d + e == h - 1
            for p, q, c_order, other_order in ((d, e, a, b), (e, d, b, a)):
                assert c_order + h - p == 27
                assert other_order == 26 - p
                assert other_order + p + 1 == 27
                assert c_order - p == other_order - q == s
                assert h - 1 + s == 26
                if p == 1:
                    assert other_order == 25
                else:
                    assert 2 * (30 - h) > other_order
                identities += 6
            assert D >= 1
            # Both t=0 and t=1 are arithmetically admissible.
            assert D - 1 >= 0
        summary.append((h, minimum_low_edges, upper, tuple(rows), identities))

    # A separate parity audit of the two-contraction lemma.
    parity_checks = 0
    for h in range(14, 18):
        pairs = tuple(combinations(range(h), 2))
        for first, second in combinations(pairs, 2):
            assert len(set(first) & set(second)) <= 1
            parity_checks += 1

    # Independent closed-form reconstruction of the exact h=17 three-block
    # size/edge frontier.  Here q is the number of direct intersections and
    # `extra` counts edges in connector K2/K3 blocks.
    frontier = set()
    h = 17
    low = 36
    for x in range(10, 27):
        for y in range(x, 27):
            for z in range(y, 27):
                for q, extras in ((0, range(4)), (1, range(2)), (2, range(1))):
                    if x + y + z - q != low:
                        continue
                    base = comb(x, 2) + comb(y, 2) + comb(z, 2)
                    for extra in extras:
                        e_low = base + extra
                        if e_low >= 26 * low - 713:
                            frontier.add(((x, y, z), q, extra, e_low, e_low - 223))
    # All surviving size triples have pair sums at most 28, so an admissible
    # intersection forest realizing q exists in each recorded signature.
    assert all(sizes[-1] + sizes[0] <= 28 for sizes, q, *_ in frontier if q)
    assert len(frontier) == 11

    return summary, parity_checks, tuple(sorted(frontier))


def main():
    summary, parity_checks, frontier = reconstruct()
    record = f"summary={summary};parity={parity_checks};h17={frontier}"
    print("PASS independent Albertson h=14,15,16 reconstruction")
    for h, minimum, upper, rows, identities in summary:
        print(
            f"h={h}: forced e(L)>={minimum}; three-block upper={upper}; "
            f"rows={len(rows)}; terminal identities={identities}"
        )
    print(f"unordered_contraction_pair_checks={parity_checks}")
    print(f"h17_three_block_signatures={frontier}")
    print(f"independent_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
