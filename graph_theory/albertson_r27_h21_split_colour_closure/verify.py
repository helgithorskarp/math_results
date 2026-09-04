#!/usr/bin/env python3
"""Exact audit of the Albertson r=27, order-53, h=21 closure."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
N = 53
M = 713
H = 21
LOW = N - H
S = K - H
FORCED_LOW_EDGES = 26 * LOW - M
PALETTE = 26


def partitions(total, length, floor, ceiling=26):
    """Yield nondecreasing bounded integer partitions."""
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


def block_rows(count):
    """Enumerate the connector-edge over-approximation for a block count."""
    rows = []
    for overlap in range(count):
        components = count - overlap
        for sizes in partitions(LOW + overlap, count, S):
            base = sum(comb(size, 2) for size in sizes)
            for connector_edges in range(comb(components, 2) + 1):
                low_edges = base + connector_edges
                if low_edges < FORCED_LOW_EDGES:
                    continue
                high_edges = low_edges - FORCED_LOW_EDGES
                colour_cap = chromatic_edge_cap(high_edges)
                rows.append(
                    (
                        sizes,
                        overlap,
                        connector_edges,
                        low_edges,
                        high_edges,
                        colour_cap,
                        max(sizes) + colour_cap,
                    )
                )
    return tuple(sorted(rows))


def block_count_audit():
    """Close six/five blocks and reduce four blocks to a strict-list row."""
    seven_minimum_union = 7 * S - 6
    assert seven_minimum_union == 36 > LOW

    caps = {}
    for count in (6, 5):
        values = []
        for overlap in range(count):
            components = count - overlap
            candidates = tuple(partitions(LOW + overlap, count, S))
            if not candidates:
                continue
            edge_cap = max(
                sum(comb(size, 2) for size in sizes) + comb(components, 2)
                for sizes in candidates
            )
            values.append((overlap, edge_cap))
        caps[count] = tuple(values)

    assert caps[6] == ((4, 91), (5, 96))
    assert max(value for _, value in caps[6]) < FORCED_LOW_EDGES
    assert caps[5] == ((0, 98), (1, 102), (2, 108), (3, 116), (4, 126))

    five_rows = block_rows(5)
    assert five_rows == (
        ((6, 6, 6, 6, 12), 4, 0, 126, 7, 4, 16),
        ((6, 6, 6, 7, 11), 4, 0, 121, 2, 2, 13),
    )
    assert all(row[-1] <= PALETTE for row in five_rows)

    four_rows = block_rows(4)
    assert tuple(sum(row[1] == q for row in four_rows) for q in range(4)) == (
        73,
        72,
        46,
        27,
    )
    assert tuple(max(row[-1] for row in four_rows if row[1] == q) for q in range(4)) == (
        21,
        23,
        26,
        28,
    )
    exceptions = tuple(row for row in four_rows if row[-1] > PALETTE)
    assert exceptions == (((6, 6, 6, 17), 3, 0, 181, 62, 11, 28),)
    # The direct large-block family is connected.  A noncut vertex in a
    # smaller K6 has low degree 5, while all 15 colours unused on Q occur in
    # its list.  This is the strict vertex used by the prose greedy argument.
    assert PALETTE - exceptions[0][5] == 15 > 5
    return seven_minimum_union, caps, five_rows, four_rows, exceptions


def three_block_audit():
    """Reduce all three-block list obstructions to isolated largest cliques."""
    rows = block_rows(3)
    assert tuple(sum(row[1] == q for row in rows) for q in range(3)) == (96, 54, 30)
    exceptions = tuple(row for row in rows if row[-1] > PALETTE)
    assert tuple(sum(row[1] == q for row in exceptions) for q in range(3)) == (36, 26, 21)

    tied = tuple(row for row in exceptions if row[0].count(max(row[0])) > 1)
    assert tied == (((6, 14, 14), 2, 0, 197, 78, 13, 27),)
    # The K6 has a noncut vertex even when it is the middle block of the only
    # possible direct-intersection path, and 13 unused colours exceed degree 5.
    assert PALETTE - tied[0][5] == 13 > 5

    unique = tuple(row for row in exceptions if row not in tied)
    for sizes, _, _, _, _, colour_cap, _ in unique:
        largest = max(sizes)
        smaller = tuple(size for size in sizes if size != largest)
        assert len(smaller) == 2
        assert all(PALETTE - colour_cap > size - 1 for size in smaller)

    # An isolated largest block is possible only when all three large blocks
    # are disjoint and there is at most one connector edge, or when the two
    # smaller blocks meet directly and there is no connector.
    residual = tuple(
        row
        for row in unique
        if (row[1] == 0 and row[2] <= 1) or (row[1] == 1 and row[2] == 0)
    )
    assert len(residual) == 31
    assert tuple(sum(row[1] == q for row in residual) for q in range(3)) == (18, 13, 0)
    return rows, exceptions, tied, residual


def hall_audit(block_order):
    """Check Hall for the two list types created by every strict split."""
    records = []
    for split_weight in range(1, block_order):
        minimum_slack = block_order
        checks = 0
        for chosen_adjacent in range(split_weight + 1):
            for chosen_nonadjacent in range(block_order - split_weight + 1):
                chosen = chosen_adjacent + chosen_nonadjacent
                if chosen == 0:
                    continue
                union = (
                    block_order
                    if chosen_adjacent and chosen_nonadjacent
                    else block_order - 1
                )
                assert union >= chosen
                minimum_slack = min(minimum_slack, union - chosen)
                checks += 1
        assert minimum_slack == 0
        records.append((split_weight, checks, minimum_slack))
    return tuple(records)


def split_colour_audit(residual):
    """Audit split-palette slack and every terminal endpoint degree sum."""
    distinct_orders = tuple(sorted({max(row[0]) for row in residual}))
    assert distinct_orders == (15, 16, 17, 18, 19, 20, 21)
    hall = tuple((order, hall_audit(order)) for order in distinct_orders)

    endpoint_rows = []
    for sizes, overlap, connector_edges, _, high_edges, colour_cap, _ in residual:
        block_order = max(sizes)
        active = K - block_order
        smaller = max(size for size in sizes if size != block_order)
        unused_after_split = PALETTE - (colour_cap + 1)
        assert unused_after_split >= smaller

        full = active
        zero = H - active
        full_floor = active - 1
        zero_floor = block_order - 5
        degree_floor = full * full_floor + zero * zero_floor
        handshake = 2 * high_edges
        assert degree_floor > handshake
        endpoint_rows.append(
            (
                sizes,
                overlap,
                connector_edges,
                high_edges,
                colour_cap,
                block_order,
                active,
                smaller,
                unused_after_split,
                degree_floor,
                handshake,
                degree_floor - handshake,
            )
        )

    endpoint_rows = tuple(endpoint_rows)
    assert min(row[-1] for row in endpoint_rows) == 28
    grouped = []
    for order in distinct_orders:
        rows = tuple(row for row in endpoint_rows if row[5] == order)
        grouped.append((order, rows[0][9], max(row[10] for row in rows), min(row[-1] for row in rows)))
    assert tuple(grouped) == (
        (15, 222, 134, 88),
        (16, 220, 142, 78),
        (17, 222, 154, 68),
        (18, 228, 170, 58),
        (19, 238, 190, 48),
        (20, 252, 214, 38),
        (21, 270, 242, 28),
    )
    return hall, endpoint_rows, tuple(grouped)


def two_clique_audit():
    """Check the exact profiles and slack in the parametric terminal proof."""
    profiles = []
    checks = 0
    for a in range(S, LOW // 2 + 1):
        b = LOW - a
        if b >= K:
            continue
        p, q = a - S, b - S
        deficit = comb(H, 2) - M + 26 * LOW - comb(a, 2) - comb(b, 2)
        if deficit < 0:
            continue
        profiles.append((a, b, p, q, deficit))
        assert p >= 1 and p + q == H - 1
        for side, other, support, opposite in ((a, b, p, q), (b, a, q, p)):
            assert side - (support + 1) == other - (opposite + 1) == PALETTE - H
            assert H + (PALETTE - H) == PALETTE
            assert side - support == other - opposite == K - H
            assert H - 1 + (K - H) == PALETTE
            assert support + opposite + 1 == H
            assert other + support + 1 == K
            target_neighbours = other - (25 - (support + 1))
            one_end_neighbours = other - (25 - (S + support + 1))
            opposite_type_neighbours = other - (25 - (S + support + 2))
            assert (target_neighbours, one_end_neighbours, opposite_type_neighbours) == (
                2,
                8,
                9,
            )
            assert 28 - H == 7
            assert PALETTE - H == 5 >= 2
            checks += 14

    assert tuple(profiles) == (
        (7, 25, 1, 19, 8),
        (8, 24, 2, 18, 25),
        (9, 23, 3, 17, 40),
        (10, 22, 4, 16, 53),
        (11, 21, 5, 15, 64),
        (12, 20, 6, 14, 73),
        (13, 19, 7, 13, 80),
        (14, 18, 8, 12, 85),
        (15, 17, 9, 11, 88),
        (16, 16, 10, 10, 89),
    )

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
    seven_min, caps, five, four, four_exceptions = block_count_audit()
    three, exceptions, tied, residual = three_block_audit()
    hall, endpoints, grouped = split_colour_audit(residual)
    two, terminal_checks, contraction_checks = two_clique_audit()
    record = (
        f"seven={seven_min};caps={caps};five={five};four={four};"
        f"four_exceptions={four_exceptions};three={three};exceptions={exceptions};"
        f"tied={tied};residual={residual};hall={hall};endpoints={endpoints};"
        f"grouped={grouped};two={two};terminal={terminal_checks};"
        f"contractions={contraction_checks}"
    )
    print("PASS Albertson r=27 h=21 split-colour closure")
    print(f"forced_eL={FORCED_LOW_EDGES}; seven_block_min_union={seven_min}")
    print(f"six_block_caps={caps[6]}; five_block_rows={len(five)}")
    print(
        "four_block_rows_by_q="
        f"{tuple(sum(row[1] == q for row in four) for q in range(4))}; "
        f"strict_list_exceptions={len(four_exceptions)}"
    )
    print(
        "three_block_rows_by_q="
        f"{tuple(sum(row[1] == q for row in three) for q in range(3))}; "
        f"list_exceptions={len(exceptions)}; isolated_rows={len(residual)}"
    )
    print(f"endpoint_groups={grouped}; minimum_margin={min(row[-1] for row in endpoints)}")
    print(f"two_clique_profiles={two}; terminal_checks={terminal_checks}")
    print(f"contraction_checks={contraction_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
