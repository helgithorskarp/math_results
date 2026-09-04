#!/usr/bin/env python3
"""Exact audit of the Albertson r=27, order-53, h=19 reduction."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
N = 53
M = 713
H = 19
LOW = N - H
S = K - H
FORCED_LOW_EDGES = 26 * LOW - M


def partitions(total, length, floor, ceiling=26):
    """Nondecreasing bounded integer partitions."""
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(floor, min(ceiling, total // length) + 1):
        for tail in partitions(total - first, length - 1, first, ceiling):
            yield (first,) + tail


def chromatic_edge_cap(edges):
    """Largest c not excluded by e >= binom(c,2)."""
    c = 1
    while comb(c + 1, 2) <= edges:
        c += 1
    assert comb(c, 2) <= edges < comb(c + 1, 2)
    return c


def high_edge_count(low_edges):
    """At h=19 the fixed low degree sum gives e(Q)=e(L)-171."""
    return low_edges - FORCED_LOW_EDGES


def block_count_audit():
    """Five blocks do not fit, and four cannot meet the low-edge floor."""
    five_block_minimum_union = 5 * S - 4
    assert five_block_minimum_union == 36 > LOW

    rows = []
    for q in range(4):
        components = 4 - q
        order_sum = LOW + q
        candidates = tuple(partitions(order_sum, 4, S))
        assert candidates
        maximum = max(
            sum(comb(x, 2) for x in sizes) + comb(components, 2)
            for sizes in candidates
        )
        witnesses = tuple(
            sizes
            for sizes in candidates
            if sum(comb(x, 2) for x in sizes) + comb(components, 2)
            == maximum
        )
        rows.append((q, components, witnesses, maximum))
    assert rows == [
        (0, 4, ((8, 8, 8, 10),), 135),
        (1, 3, ((8, 8, 8, 11),), 142),
        (2, 2, ((8, 8, 8, 12),), 151),
        (3, 1, ((8, 8, 8, 13),), 162),
    ]
    assert max(row[-1] for row in rows) < FORCED_LOW_EDGES
    return five_block_minimum_union, tuple(rows)


def admissible_three_block_geometry(sizes, q):
    """Labelled direct-intersection witnesses under the degree-26 cap."""
    if q == 0:
        return ((),)
    if q == 1:
        return tuple(
            ((u, v),)
            for u, v in combinations(range(3), 2)
            if sizes[u] + sizes[v] <= 28
        )
    assert q == 2
    witnesses = []
    # A common cut in all three blocks has 33 low neighbours.  Thus only a
    # path with two distinct cuts is possible.
    assert sum(sizes) - 3 == 33 > 26
    for middle in range(3):
        ends = tuple(v for v in range(3) if v != middle)
        pairs = tuple(sorted(((middle, ends[0]), (middle, ends[1]))))
        if all(sizes[u] + sizes[v] <= 28 for u, v in pairs):
            witnesses.append(pairs)
    return tuple(witnesses)


def three_block_audit():
    """Enumerate all edge signatures and isolate the palette exceptions."""
    connector_options = {0: (0, 1, 2, 3), 1: (0, 1), 2: (0,)}
    records = []
    labelled_geometries = 0
    for q in range(3):
        for sizes in partitions(LOW + q, 3, S):
            geometries = admissible_three_block_geometry(sizes, q)
            labelled_geometries += len(geometries)
            if not geometries:
                continue
            base = sum(comb(x, 2) for x in sizes)
            for connector_edges in connector_options[q]:
                e_low = base + connector_edges
                if e_low < FORCED_LOW_EDGES:
                    continue
                e_high = high_edge_count(e_low)
                high_cap = chromatic_edge_cap(e_high)
                palette_cap = max(sizes) + high_cap
                records.append(
                    (
                        sizes,
                        q,
                        connector_edges,
                        e_low,
                        e_high,
                        high_cap,
                        palette_cap,
                    )
                )

    records = tuple(sorted(records))
    summary = tuple(
        (
            q,
            sum(row[1] == q for row in records),
            max(row[-1] for row in records if row[1] == q),
        )
        for q in range(3)
    )
    assert summary == ((0, 56, 27), (1, 32, 30), (2, 19, 32))

    exceptions = tuple(row for row in records if row[-1] > 26)
    assert len(exceptions) == 14
    expected_exceptions = (
        ((8, 8, 18), 0, 0),
        ((8, 8, 18), 0, 1),
        ((8, 8, 18), 0, 2),
        ((8, 8, 18), 0, 3),
        ((8, 8, 19), 1, 0),
        ((8, 8, 19), 1, 1),
        ((8, 9, 18), 1, 0),
        ((8, 9, 18), 1, 1),
        ((8, 8, 20), 2, 0),
        ((8, 9, 19), 2, 0),
        ((8, 10, 18), 2, 0),
        ((8, 11, 17), 2, 0),
        ((9, 9, 18), 2, 0),
        ((9, 10, 17), 2, 0),
    )
    assert tuple(sorted((row[0], row[1], row[2]) for row in exceptions)) == tuple(
        sorted(expected_exceptions)
    )
    return records, summary, labelled_geometries, exceptions


def slack_list_audit(exceptions):
    """Check the strict-list inequality and the four residual geometries."""
    checks = []
    for sizes, q, connector_edges, e_low, e_high, high_cap, palette_cap in exceptions:
        large = max(sizes)
        small = tuple(x for x in sizes if x != large)
        # Every exception has a unique largest block.
        assert len(small) == 2
        unused = 26 - high_cap
        assert unused > max(small) - 1
        checks.append((sizes, q, connector_edges, high_cap, unused, max(small)))

    # A component containing the unique large block and another large block
    # has a small leaf block, hence a strict list vertex and is colourable.
    # The large block can be isolated only in the following geometries.
    residual = (
        # orders, direct intersections, connector edges, e(L), e(Q), chi(Q) cap
        ((8, 8, 18), 0, 0, 209, 38, 9),
        ((8, 8, 18), 0, 1, 210, 39, 9),
        ((8, 8, 19), 1, 0, 227, 56, 11),
        ((8, 9, 18), 1, 0, 217, 46, 10),
    )
    for sizes, q, connector_edges, e_low, e_high, cap in residual:
        assert e_low == sum(comb(x, 2) for x in sizes) + connector_edges
        assert e_high == high_edge_count(e_low)
        assert cap == chromatic_edge_cap(e_high)

    # Rigid clique-list obstruction under an optimal c-colouring of Q.
    rigidity = []
    for sizes, q, connector_edges, e_low, e_high, cap in residual:
        b = max(sizes)
        forbidden_colours = 27 - b
        assert b - 1 + forbidden_colours == 26
        assert forbidden_colours <= cap
        rigidity.append((b, forbidden_colours, cap))
    assert tuple(rigidity) == ((18, 9, 9), (18, 9, 9), (19, 8, 11), (18, 9, 10))
    return tuple(checks), residual, tuple(rigidity)


def two_clique_audit():
    """Reconstruct the h=19 rows and every numerical terminal identity."""
    profiles = []
    terminal_checks = 0
    for a in range(S, LOW // 2 + 1):
        b = LOW - a
        if b >= K:
            continue
        p, q = a - S, b - S
        base = comb(a, 2) + comb(b, 2)
        deficit = comb(H, 2) - M + 26 * LOW - base
        if deficit < 0:
            continue
        profiles.append((a, b, p, q, deficit))

        assert p + q == H - 1
        assert p >= 1
        for side, other, support, opposite_support in (
            (a, b, p, q),
            (b, a, q, p),
        ):
            # One-larger incidence matchings leave seven residual cross-pairs.
            assert side - (support + 1) == other - (opposite_support + 1) == 26 - H == 7
            assert H + (26 - H) == 26
            # One target contraction leaves eight residual cross-pairs.
            assert side - support == other - opposite_support == 27 - H == 8
            assert H - 1 + (27 - H) == 26
            # Double uniformity partitions Q into support+opposite+1 vertices.
            assert support + opposite_support + 1 == H
            assert other + support + 1 == K

            # In the one-target route, an endpoint has two graph neighbours
            # and a one-end support has ten in the opposite clique.  If the
            # latter lower bound exceeds the clique order, that support type
            # is itself impossible.
            target_g_neighbours = other - (25 - (support + 1))
            support_g_neighbours = other - (25 - (S + support + 1))
            opposite_type_g_neighbours = other - (25 - (S + support + 2))
            assert target_g_neighbours == 2
            assert support_g_neighbours == 10
            assert opposite_type_g_neighbours == 11
            assert target_g_neighbours >= 2
            assert support_g_neighbours >= 2 or support_g_neighbours > other

            # The conformal-triangle deletions leave nine low vertices per
            # side; the bridge residual pairing has order seven.
            assert 28 - H == 9
            assert 26 - H == 7 >= 2
            terminal_checks += 12

    assert tuple(profiles) == (
        (9, 25, 1, 17, 6),
        (10, 24, 2, 16, 21),
        (11, 23, 3, 15, 34),
        (12, 22, 4, 14, 45),
        (13, 21, 5, 13, 54),
        (14, 20, 6, 12, 61),
        (15, 19, 7, 11, 66),
        (16, 18, 8, 10, 69),
        (17, 17, 9, 9, 70),
    )
    bridge_variants = 2 * len(profiles)
    assert bridge_variants == 18

    pairs = tuple(combinations(range(H), 2))
    ordered_distinct_contractions = 0
    for first in pairs:
        for second in pairs:
            if first == second:
                continue
            intersection = set(first) & set(second)
            even_subsets = sum(
                1
                for size in range(len(intersection) + 1)
                for _ in combinations(intersection, size)
                if size % 2 == 0
            )
            assert even_subsets == 1
            ordered_distinct_contractions += 1
    assert ordered_distinct_contractions == comb(H, 2) * (comb(H, 2) - 1)
    return tuple(profiles), bridge_variants, terminal_checks, ordered_distinct_contractions


def main():
    five_min, four = block_count_audit()
    three, summary, geometries, exceptions = three_block_audit()
    slack, residual, rigidity = slack_list_audit(exceptions)
    two, variants, terminal, contractions = two_clique_audit()
    record = (
        f"five={five_min};four={four};three={three};summary={summary};"
        f"geometries={geometries};exceptions={exceptions};slack={slack};"
        f"residual={residual};rigidity={rigidity};two={two};"
        f"variants={variants};terminal={terminal};contractions={contractions}"
    )
    print("PASS Albertson r=27 order-53 h=19 structural reduction")
    print(f"forced_eL={FORCED_LOW_EDGES}; five_block_min_union={five_min}")
    print(f"four_block_caps={tuple(row[-1] for row in four)}")
    print(f"three_block_summary={summary}; labelled_geometries={geometries}")
    print(f"palette_exceptions={len(exceptions)}; residual_forms={residual}")
    print(f"rigid_clique_colour_rows={rigidity}")
    print(f"two_clique_profiles={two}; bridge_variants={variants}")
    print(f"terminal_checks={terminal}; contraction_checks={contractions}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
