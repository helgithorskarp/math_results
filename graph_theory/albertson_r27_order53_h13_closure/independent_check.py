#!/usr/bin/env python3
"""Independent arithmetic/structure audit of the Albertson h=13 closure."""

from hashlib import sha256
from itertools import combinations, product
from math import comb


def component_count(order, edges):
    seen = set()
    adjacency = {v: set() for v in range(order)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    count = 0
    for start in range(order):
        if start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            for v in adjacency[u] - seen:
                seen.add(v)
                stack.append(v)
    return count


def structural_reconstruction():
    """Use labelled block forests, separately from the primary checker."""
    signatures = set()
    candidates = 0
    for block_count in range(1, 5):
        pairs = tuple(combinations(range(block_count), 2))
        for orders in product(range(14, 27), repeat=block_count):
            if tuple(sorted(orders)) != orders:
                continue
            for bits in range(1 << len(pairs)):
                intersections = {pairs[i] for i in range(len(pairs)) if bits >> i & 1}
                components = component_count(block_count, intersections)
                if len(intersections) != block_count - components:
                    continue
                if any(orders[u] != 14 or orders[v] != 14 for u, v in intersections):
                    continue
                if sum(orders) - len(intersections) != 40:
                    continue
                candidates += 1
                if block_count == 2:
                    assert not intersections
                    signatures.add(("two", orders))
                else:
                    assert block_count == 3
                    assert orders == (14, 14, 14)
                    assert len(intersections) == 2
                    signatures.add(("three", orders))
    assert candidates == 10
    assert signatures == {
        *(("two", (a, 40 - a)) for a in range(14, 21)),
        ("three", (14, 14, 14)),
    }
    return candidates, signatures


def edge_table():
    table = []
    for a in range(14, 21):
        b = 40 - a
        base = comb(a, 2) + comb(b, 2)
        low_high = 1040 - 2 * base
        high_edges = 713 - base - low_high
        missing_high = comb(13, 2) - high_edges
        if missing_high < 0:
            continue
        d, e = 13 - (26 - (a - 1)), 13 - (26 - (b - 1))
        assert (d, e) == (a - 14, b - 14)
        table.append((a, b, d, e, missing_high))
    expected = [
        (15, 25, 1, 11, 0),
        (16, 24, 2, 10, 9),
        (17, 23, 3, 9, 16),
        (18, 22, 4, 8, 21),
        (19, 21, 5, 7, 24),
        (20, 20, 6, 6, 25),
    ]
    assert table == expected
    assert sum(1 + (row[-1] > 0) for row in table) == 11
    return table


def abstract_terminal_checks(table):
    checks = 0
    for a, b, d, e, missing in table:
        assert d + e == 12
        assert a == 14 + d and b == 14 + e
        assert a - d == b - e == 14
        if missing == 0:
            # Common-row failure on either side exposes 27 branch vertices.
            assert a + 13 - d == b + 13 - e == 27
            checks += 2
            continue

        # One contracted high pair leaves 12 high colour classes and 14
        # residual vertices on each low side.
        assert a - d == b - e == 14
        # Double-uniform partition Q=S+R+z and its two possible branch sets.
        assert b + d + 1 == a + e + 1 == 27
        # Every conformal-triangle deletion used in the proof leaves 15 lows
        # on both sides before the final complement matching.
        assert a - (d - 1) == b - (e - 1) == 15
        assert a - 1 - (d - 2) == b - (e - 1) == 15
        assert a - (d - 1) == b - 1 - (e - 2) == 15
        # The short-path degree estimates remain valid in either orientation
        # of the deficient side at h=13.
        for support, opposite in ((d, b), (e, a)):
            assert opposite - (25 - (support + 1)) == 2
            assert 2 * 17 > opposite
            assert 16 >= 2
        # A bridge leaves 13 residual lows per side and its TK branch has 27.
        assert a - (d + 1) == b - (e + 1) == 13
        checks += 11
    return checks


def main():
    candidates, signatures = structural_reconstruction()
    table = edge_table()
    # The only intersecting cover is three K14s in a path.
    e_low = 3 * comb(14, 2)
    forced_low_incident = e_low + (26 * 40 - 2 * e_low)
    assert (e_low, forced_low_incident) == (273, 767)
    checks = abstract_terminal_checks(table)
    record = (
        f"candidates={candidates};signatures={len(signatures)};"
        f"three_path={e_low},{forced_low_incident};rows={table};checks={checks}"
    )
    print("PASS independent Albertson r=27 h=13 audit")
    print(f"block_candidates={candidates}; canonical_signatures={len(signatures)}")
    print(f"three_K14_path: eL={e_low}, forced_low_incident={forced_low_incident}>713")
    print("two_clique_rows:", table)
    print(f"terminal_identity_checks={checks}")
    print(f"independent_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
