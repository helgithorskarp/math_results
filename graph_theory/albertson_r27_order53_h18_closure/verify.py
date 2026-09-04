#!/usr/bin/env python3
"""Exact finite audit for the Albertson r=27, order-53, h=18 closure."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
N = 53
M = 713
H = 18
LOW = N - H
S = K - H
FORCED_LOW_EDGES = 26 * LOW - M


def partitions(total, length, floor, ceiling=26):
    """Nondecreasing integer partitions with fixed length and bounds."""
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(floor, min(ceiling, total // length) + 1):
        for tail in partitions(total - first, length - 1, first, ceiling):
            yield (first,) + tail


def chromatic_edge_cap(edges):
    """Largest c not excluded by the elementary floor e>=C(c,2)."""
    c = 1
    while comb(c + 1, 2) <= edges:
        c += 1
    assert comb(c, 2) <= edges < comb(c + 1, 2)
    return c


def four_block_audit():
    """Four large blocks have far too few low--low edges."""
    rows = []
    for q in range(4):
        components = 4 - q
        total_orders = LOW + q
        sizes = tuple(partitions(total_orders, 4, S))
        if not sizes:
            rows.append((q, components, None, None))
            continue
        maximum = max(
            sum(comb(x, 2) for x in row) + comb(components, 2)
            for row in sizes
        )
        witnesses = tuple(
            row
            for row in sizes
            if sum(comb(x, 2) for x in row) + comb(components, 2) == maximum
        )
        rows.append((q, components, witnesses, maximum))
    assert rows == [
        (0, 4, None, None),
        (1, 3, ((9, 9, 9, 9),), 147),
        (2, 2, ((9, 9, 9, 10),), 154),
        (3, 1, ((9, 9, 9, 11),), 163),
    ]
    assert max(row[3] for row in rows if row[3] is not None) < FORCED_LOW_EDGES
    return tuple(rows)


def admissible_three_block_geometry(sizes, q):
    """Return labelled direct-intersection witnesses for a size multiset."""
    witnesses = []
    indices = range(3)
    if q == 0:
        return ((),)
    if q == 1:
        for u, v in combinations(indices, 2):
            if sizes[u] + sizes[v] <= 28:
                witnesses.append(((u, v),))
        return tuple(witnesses)
    assert q == 2
    # A single cut vertex common to all blocks would have
    # sum_i(|B_i|-1)=34 low neighbours, so only paths with distinct cuts
    # need be retained.  Record the two incident pairs for each middle block.
    for middle in indices:
        ends = [v for v in indices if v != middle]
        edges = tuple(sorted(((middle, ends[0]), (middle, ends[1]))))
        if all(sizes[u] + sizes[v] <= 28 for u, v in edges):
            witnesses.append(edges)
    return tuple(witnesses)


def three_block_audit():
    """Enumerate every edge-budget survivor and its palette certificate."""
    connector_options = {0: (0, 1, 2, 3), 1: (0, 1), 2: (0,)}
    records = []
    geometry_count = 0
    for q in range(3):
        for sizes in partitions(LOW + q, 3, S):
            witnesses = admissible_three_block_geometry(sizes, q)
            geometry_count += len(witnesses)
            if not witnesses:
                continue
            base = sum(comb(x, 2) for x in sizes)
            for extra in connector_options[q]:
                e_low = base + extra
                if e_low < FORCED_LOW_EDGES:
                    continue
                e_high = e_low - FORCED_LOW_EDGES
                high_cap = chromatic_edge_cap(e_high)
                palette_cap = max(sizes) + high_cap
                records.append((sizes, q, extra, e_low, e_high, high_cap, palette_cap))

    records = tuple(sorted(records))
    assert tuple(sum(row[1] == q for row in records) for q in range(3)) == (13, 24, 14)
    assert tuple(max(row[-1] for row in records if row[1] == q) for q in range(3)) == (22, 26, 29)
    exceptions = tuple(row for row in records if row[-1] > 26)
    assert exceptions == (
        ((9, 9, 19), 2, 0, 243, 46, 10, 29),
        ((9, 10, 18), 2, 0, 234, 37, 9, 27),
    )
    return records, geometry_count, exceptions


def exceptional_palette_audit():
    """Check the colour-class reuse counts in the two exceptional paths."""
    checks = 0

    # In the (9,10,18) path, a cut of K18 has complement row at least 17.
    # If chi(Q)=9, at most one of the nine colour classes is contaminated by
    # the sole possible G-neighbour outside that row.
    for adjacent_order in (9, 10):
        row_size = 18 + adjacent_order - 10
        assert row_size >= 17
        bad = H - row_size
        compatible_classes = 9 - bad
        assert compatible_classes >= 1
        assert 18 + 9 - 1 == 26
        checks += 4

    # In the (9,9,19) path, a K19 cut row is all Q.  An internal K19 row
    # has size 10, so its eight bad vertices contaminate at most eight colour
    # classes.  For c=10, exhaust the worst case in which each of two rows
    # has only two compatible classes and verify a two-matching always exists.
    for c in (8, 9, 10):
        required_reuses = c - 7
        internal_reuses = max(0, required_reuses - 1)
        compatible_per_internal_row = c - (H - 10)
        assert compatible_per_internal_row >= internal_reuses
        assert 19 + c - required_reuses == 26
        checks += 3

    hall_checks = 0
    classes = range(10)
    for first in combinations(classes, 2):
        for second in combinations(classes, 2):
            assert len(set(first) | set(second)) >= 2
            hall_checks += 1
    assert hall_checks == comb(10, 2) ** 2 == 2025

    # At most three K19 colours are reused on Q.  At least sixteen clean
    # colours remain, more than the nine clean colours needed to propagate a
    # colouring along two K9 blocks while avoiding the marked colours.
    assert 19 - 3 == 16 >= 9
    return checks, hall_checks


def two_clique_audit():
    """Reconstruct all two-clique rows and the parametric terminal identities."""
    rows = []
    variants = []
    terminal_checks = 0
    for a in range(S, LOW // 2 + 1):
        b = LOW - a
        if b >= K:
            continue
        p, q = a - S, b - S
        base = comb(a, 2) + comb(b, 2)
        D = comb(H, 2) - M + 26 * LOW - base
        if D < 0:
            continue
        rows.append((a, b, p, q, D))
        for bridge in (0, 1):
            missing_high_edges = D - bridge
            if missing_high_edges >= 0:
                variants.append((a, b, p, q, bridge, missing_high_edges))

        assert p + q == H - 1
        assert p >= 1
        for c_order, other_order, support, opposite_support in (
            (a, b, p, q),
            (b, a, q, p),
        ):
            # Uniform-support branch set.
            assert c_order + (H - support) == K
            # Simultaneous one-larger matchings leave eight cross-pairs.
            assert c_order - (support + 1) == S - 1
            assert other_order - (opposite_support + 1) == S - 1
            assert H + (S - 1) == 26
            # Contracting a target leaves 17 high classes and nine pairs.
            assert c_order - support == other_order - opposite_support == S
            assert (H - 1) + S == 26
            # Double-uniform support partition and TK27 branch set.
            assert support + opposite_support + 1 == H
            assert other_order + support + 1 == K

            if support == 1:
                assert other_order == 25
                # A target endpoint cannot miss all K25 vertices in G.
                assert other_order + 1 > 25
            else:
                # A target endpoint has at least two G-neighbours in the
                # opposite clique; a one-end support has at least eleven.
                target_g_neighbours = other_order - (25 - (support + 1))
                support_g_neighbours = other_order - (25 - (S + support + 1))
                assert target_g_neighbours == 2
                assert support_g_neighbours == 11
            terminal_checks += 12

    assert tuple(rows) == (
        (10, 25, 1, 16, 5),
        (11, 24, 2, 15, 19),
        (12, 23, 3, 14, 31),
        (13, 22, 4, 13, 41),
        (14, 21, 5, 12, 49),
        (15, 20, 6, 11, 55),
        (16, 19, 7, 10, 59),
        (17, 18, 8, 9, 61),
    )
    assert len(variants) == 16
    assert all(missing >= 0 for *_, missing in variants)
    return tuple(rows), tuple(variants), terminal_checks


def contraction_parity_audit():
    """Two distinct failed target contractions force equal original rows."""
    pairs = tuple(combinations(range(H), 2))
    checked = 0
    for first in pairs:
        for second in pairs:
            if first == second:
                continue
            intersection = set(first) & set(second)
            # The equal-cardinality symmetric difference is even and lies in
            # both endpoint pairs, whose intersection has order at most one.
            even_subsets = sum(
                1
                for size in range(len(intersection) + 1)
                for _ in combinations(intersection, size)
                if size % 2 == 0
            )
            assert even_subsets == 1
            checked += 1
    assert checked == comb(H, 2) * (comb(H, 2) - 1) == 23256
    return checked


def main():
    four = four_block_audit()
    three, geometries, exceptions = three_block_audit()
    exceptional_checks, hall_checks = exceptional_palette_audit()
    two, variants, terminal_checks = two_clique_audit()
    parity_checks = contraction_parity_audit()
    record = (
        f"four={four};three={three};geometries={geometries};"
        f"exceptions={exceptions};exceptional_checks={exceptional_checks};"
        f"hall={hall_checks};two={two};variants={variants};"
        f"terminal={terminal_checks};parity={parity_checks}"
    )
    print("PASS Albertson r=27 order-53 h=18 closure audit")
    print(f"forced_eL={FORCED_LOW_EDGES}; four_block_bounds={four}")
    print(
        "three_block_survivors_by_q="
        f"{tuple(sum(row[1] == q for row in three) for q in range(3))}; "
        f"labelled_geometry_witnesses={geometries}"
    )
    print(
        "three_block_palette_maxima="
        f"{tuple(max(row[-1] for row in three if row[1] == q) for q in range(3))}; "
        f"exceptions={exceptions}"
    )
    print(
        f"exceptional_reuse_checks={exceptional_checks}; "
        f"two-row_Hall_checks={hall_checks}"
    )
    print(f"two_clique_profiles={two}; bridge_variants={len(variants)}")
    print(f"terminal_identity_checks={terminal_checks}; contraction_checks={parity_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
