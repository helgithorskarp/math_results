#!/usr/bin/env python3
"""Exact audit of the Albertson r=27, order-53, h=20 reduction."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
N = 53
M = 713
H = 20
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
    return low_edges - FORCED_LOW_EDGES


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
    # A common cut in all three has sum_i(|B_i|-1)=32>26.  Only paths
    # with two distinct cut vertices remain.
    assert sum(sizes) - 3 == 32 > 26
    witnesses = []
    for middle in range(3):
        ends = tuple(v for v in range(3) if v != middle)
        pairs = tuple(sorted(((middle, ends[0]), (middle, ends[1]))))
        if all(sizes[u] + sizes[v] <= 28 for u, v in pairs):
            witnesses.append(pairs)
    return tuple(witnesses)


def many_block_audit():
    """Exclude five blocks and close four blocks by disjoint palettes."""
    six_block_minimum_union = 6 * S - 5
    assert six_block_minimum_union == 37 > LOW

    five_caps = []
    for q in range(5):
        components = 5 - q
        candidates = tuple(partitions(LOW + q, 5, S))
        if not candidates:
            continue
        cap = max(
            sum(comb(x, 2) for x in sizes) + comb(components, 2)
            for sizes in candidates
        )
        five_caps.append((q, cap))
    assert five_caps == [(2, 108), (3, 113), (4, 120)]
    assert max(cap for _, cap in five_caps) < FORCED_LOW_EDGES

    four_caps = []
    four_rows = []
    for q in range(4):
        components = 4 - q
        candidates = tuple(partitions(LOW + q, 4, S))
        if not candidates:
            continue
        cap = max(
            sum(comb(x, 2) for x in sizes) + comb(components, 2)
            for sizes in candidates
        )
        four_caps.append((q, cap))
        for sizes in candidates:
            base = sum(comb(x, 2) for x in sizes)
            for connector_edges in range(comb(components, 2) + 1):
                e_low = base + connector_edges
                if e_low < FORCED_LOW_EDGES:
                    continue
                e_high = high_edge_count(e_low)
                c_cap = chromatic_edge_cap(e_high)
                four_rows.append(
                    (sizes, q, connector_edges, e_low, e_high, c_cap, max(sizes) + c_cap)
                )
    assert four_caps == [(0, 135), (1, 144), (2, 155), (3, 168)]
    assert tuple(sum(row[1] == q for row in four_rows) for q in range(4)) == (0, 0, 5, 14)
    assert tuple(max((row[-1] for row in four_rows if row[1] == q), default=0) for q in range(4)) == (0, 0, 19, 22)
    assert all(row[-1] <= 26 for row in four_rows)
    return six_block_minimum_union, tuple(five_caps), tuple(four_caps), tuple(sorted(four_rows))


def three_block_audit():
    """Enumerate edge signatures and reduce list obstructions to 14 forms."""
    connector_options = {0: range(4), 1: range(2), 2: range(1)}
    rows = []
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
                c_cap = chromatic_edge_cap(e_high)
                rows.append(
                    (sizes, q, connector_edges, e_low, e_high, c_cap, max(sizes) + c_cap)
                )

    rows = tuple(sorted(rows))
    assert tuple(sum(row[1] == q for row in rows) for q in range(3)) == (76, 42, 24)
    assert tuple(max(row[-1] for row in rows if row[1] == q) for q in range(3)) == (31, 33, 36)
    exceptions = tuple(row for row in rows if row[-1] > 26)
    assert tuple(sum(row[1] == q for row in exceptions) for q in range(3)) == (16, 12, 12)

    for sizes, _, _, _, _, c_cap, _ in exceptions:
        largest = max(sizes)
        small = tuple(x for x in sizes if x != largest)
        assert len(small) == 2
        assert 26 - c_cap > max(small) - 1

    # The unique largest block can be isolated only with no connector, with
    # one bridge joining the two smaller disjoint blocks, or when the two
    # smaller blocks meet directly and there is no connector.
    residual = tuple(
        row
        for row in exceptions
        if (row[1] == 0 and row[2] <= 1) or (row[1] == 1 and row[2] == 0)
    )
    expected = (
        ((7, 7, 19), 0, 0, 213, 68, 12, 31),
        ((7, 7, 19), 0, 1, 214, 69, 12, 31),
        ((7, 7, 20), 1, 0, 232, 87, 13, 33),
        ((7, 8, 18), 0, 0, 202, 57, 11, 29),
        ((7, 8, 18), 0, 1, 203, 58, 11, 29),
        ((7, 8, 19), 1, 0, 220, 75, 12, 31),
        ((7, 9, 17), 0, 0, 193, 48, 10, 27),
        ((7, 9, 17), 0, 1, 194, 49, 10, 27),
        ((7, 9, 18), 1, 0, 210, 65, 11, 29),
        ((7, 10, 17), 1, 0, 202, 57, 11, 28),
        ((8, 8, 17), 0, 0, 192, 47, 10, 27),
        ((8, 8, 17), 0, 1, 193, 48, 10, 27),
        ((8, 8, 18), 1, 0, 209, 64, 11, 29),
        ((8, 9, 17), 1, 0, 200, 55, 11, 28),
    )
    assert residual == expected
    return rows, labelled_geometries, exceptions, residual


def weighted_degree_floor(b, f, c):
    """DP over twenty weights in [0,b] with total b*f."""
    infinity = 10**9
    dp = {(0, 0): 0}
    for _ in range(H):
        next_dp = {}
        for (count, total), value in dp.items():
            for weight in range(b + 1):
                if weight == 0:
                    degree = b - 6
                elif weight == b:
                    degree = f - 1
                else:
                    degree = c - 1
                key = count + 1, total + weight
                next_dp[key] = min(next_dp.get(key, infinity), value + degree)
        dp = next_dp
    return dp[H, b * f]


def weighted_incidence_audit(residual):
    """Apply the multi-zero recolouring floor to every residual form."""
    survivors = []
    all_rows = []
    for sizes, q, connector_edges, _, e_high, c_cap, _ in residual:
        b = max(sizes)
        f = K - b
        for c in range(f, c_cap + 1):
            floor = weighted_degree_floor(b, f, c)
            row = (sizes, q, connector_edges, e_high, b, f, c, floor, 2 * e_high)
            all_rows.append(row)
            if floor <= 2 * e_high:
                survivors.append(row)
    expected = (
        ((7, 7, 20), 1, 0, 87, 20, 7, 7, 120, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 8, 134, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 9, 148, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 10, 162, 174),
        ((7, 8, 19), 1, 0, 75, 19, 8, 8, 140, 150),
    )
    assert tuple(survivors) == expected
    return tuple(all_rows), tuple(survivors)


def two_clique_audit():
    """Check that the preceding two-clique terminal proof retains slack."""
    profiles = []
    checks = 0
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
        assert p >= 1 and p + q == H - 1
        for side, other, support, opposite in ((a, b, p, q), (b, a, q, p)):
            assert side - (support + 1) == other - (opposite + 1) == 26 - H == 6
            assert H + (26 - H) == 26
            assert side - support == other - opposite == 27 - H == 7
            assert H - 1 + (27 - H) == 26
            assert support + opposite + 1 == H
            assert other + support + 1 == K
            target_g_neighbours = other - (25 - (support + 1))
            one_end_g_neighbours = other - (25 - (S + support + 1))
            opposite_type_g_neighbours = other - (25 - (S + support + 2))
            assert target_g_neighbours == 2
            assert one_end_g_neighbours == 9
            assert opposite_type_g_neighbours == 10
            assert 28 - H == 8
            assert 26 - H == 6 >= 2
            checks += 14
    expected = (
        (8, 25, 1, 18, 7),
        (9, 24, 2, 17, 23),
        (10, 23, 3, 16, 37),
        (11, 22, 4, 15, 49),
        (12, 21, 5, 14, 59),
        (13, 20, 6, 13, 67),
        (14, 19, 7, 12, 73),
        (15, 18, 8, 11, 77),
        (16, 17, 9, 10, 79),
    )
    assert tuple(profiles) == expected

    pairs = tuple(combinations(range(H), 2))
    contraction_checks = 0
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
            contraction_checks += 1
    assert contraction_checks == comb(H, 2) * (comb(H, 2) - 1)
    return tuple(profiles), checks, contraction_checks


def main():
    six_min, five, four_caps, four_rows = many_block_audit()
    three, geometries, exceptions, residual = three_block_audit()
    weighted, survivors = weighted_incidence_audit(residual)
    two, terminal_checks, contraction_checks = two_clique_audit()
    record = (
        f"six={six_min};five={five};four_caps={four_caps};four={four_rows};"
        f"three={three};geometries={geometries};exceptions={exceptions};"
        f"residual={residual};weighted={weighted};survivors={survivors};"
        f"two={two};terminal={terminal_checks};contractions={contraction_checks}"
    )
    print("PASS Albertson r=27 h=20 weighted-incidence pruning")
    print(f"forced_eL={FORCED_LOW_EDGES}; six_block_min_union={six_min}")
    print(f"five_block_caps={five}; four_block_caps={four_caps}")
    print(f"four_block_rows={len(four_rows)}; max_palette={max(row[-1] for row in four_rows)}")
    print(
        "three_block_rows_by_q="
        f"{tuple(sum(row[1] == q for row in three) for q in range(3))}; "
        f"exceptions={len(exceptions)}; rigid_residual={len(residual)}"
    )
    print(f"weighted_rows={len(weighted)}; surviving_colour_cases={survivors}")
    print(f"two_clique_profiles={two}; terminal_checks={terminal_checks}")
    print(f"contraction_checks={contraction_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
