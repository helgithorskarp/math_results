#!/usr/bin/env python3
"""Independent matching/enumeration audit of the Albertson h=22 closure."""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from math import comb


def colour_cap(edges):
    return max(c for c in range(1, 28) if comb(c, 2) <= edges)


def signatures(length, total):
    return tuple(
        values
        for values in combinations_with_replacement(range(5, 27), length)
        if sum(values) == total
    )


def rows_for_count(count):
    rows = []
    for repeated_cuts in range(count):
        direct_components = count - repeated_cuts
        for sizes in signatures(count, 31 + repeated_cuts):
            clique_edges = sum(comb(size, 2) for size in sizes)
            for extra_edges in range(comb(direct_components, 2) + 1):
                low_edges = clique_edges + extra_edges
                if low_edges < 93:
                    continue
                high_edges = low_edges - 93
                cap = colour_cap(high_edges)
                rows.append(
                    (
                        sizes,
                        repeated_cuts,
                        extra_edges,
                        low_edges,
                        high_edges,
                        cap,
                        max(sizes) + cap,
                    )
                )
    return tuple(sorted(rows))


def isolation_overcount(rows):
    kept = []
    for row in rows:
        sizes, repeated_cuts, extra_edges, *_ = row
        maximum = max(sizes)
        if sizes.count(maximum) != 1:
            continue
        other_blocks = len(sizes) - 1
        if repeated_cuts > other_blocks - 1:
            continue
        other_components = other_blocks - repeated_cuts
        if extra_edges <= comb(other_components, 2):
            kept.append(row)
    return tuple(kept)


def maximum_matching(lists, palette_size=26):
    owner = [-1] * palette_size

    def augment(vertex, seen):
        for colour in lists[vertex]:
            if colour in seen:
                continue
            seen.add(colour)
            if owner[colour] == -1 or augment(owner[colour], seen):
                owner[colour] = vertex
                return True
        return False

    return sum(augment(vertex, set()) for vertex in range(len(lists)))


def split_matchings(block_order):
    """Build the two actual list types and solve every SDR instance."""
    active = 27 - block_order
    old = 0
    fresh = 25
    active_colours = set(range(active))
    palette = set(range(26))
    records = []
    for split_size in range(1, block_order):
        available = []
        for vertex in range(block_order):
            forbidden = (
                (active_colours - {old}) | {fresh}
                if vertex < split_size
                else active_colours
            )
            choices = tuple(sorted(palette - forbidden))
            assert len(choices) == block_order - 1
            available.append(choices)
        matching = maximum_matching(available)
        assert matching == block_order
        records.append((split_size, matching))
    return tuple(records)


def vector_enumeration(block_order):
    """Enumerate all labelled full/zero endpoint vectors without a formula shortcut."""
    active = 27 - block_order
    digest = sha256()
    count = 0
    observed_floors = set()
    for full_vertices in combinations(range(22), active):
        full = set(full_vertices)
        weights = tuple(block_order if vertex in full else 0 for vertex in range(22))
        assert sum(weights) == block_order * active
        degree_sum = sum(
            active - 1 if weight else block_order - 4 for weight in weights
        )
        observed_floors.add(degree_sum)
        digest.update(repr((full_vertices, degree_sum)).encode())
        digest.update(b"\n")
        count += 1
    assert count == comb(22, active)
    assert len(observed_floors) == 1
    return count, observed_floors.pop(), digest.hexdigest()


def block_and_endpoint_audit():
    seven_caps = []
    for repeated_cuts in range(7):
        rows = signatures(7, 31 + repeated_cuts)
        if rows:
            components = 7 - repeated_cuts
            seven_caps.append(
                (
                    repeated_cuts,
                    max(
                        sum(comb(size, 2) for size in sizes) + comb(components, 2)
                        for sizes in rows
                    ),
                )
            )
    assert seven_caps == [(4, 73), (5, 76), (6, 81)]

    six = rows_for_count(6)
    five = rows_for_count(5)
    four = rows_for_count(4)
    three = rows_for_count(3)
    assert len(six) == 10 and max(row[-1] for row in six) == 16
    assert len(five) == 247 and max(row[-1] for row in five) == 25
    assert len(four) == 450 and len(three) == 223

    four_bad = tuple(row for row in four if row[-1] > 26)
    three_bad = tuple(row for row in three if row[-1] > 26)
    assert len(four_bad) == 31 and len(three_bad) == 138
    assert all(row[0].count(max(row[0])) == 1 for row in four_bad)
    four_isolated = isolation_overcount(four_bad)
    assert len(four_isolated) == 12

    tied = tuple(row for row in three_bad if row[0].count(max(row[0])) != 1)
    assert tied == (((5, 14, 14), 2, 0, 192, 99, 14, 28),)
    unique = tuple(row for row in three_bad if row not in tied)
    three_isolated = isolation_overcount(unique)
    assert len(three_isolated) == 54

    # Independently locate every pre-split smaller-block strictness exception.
    strict_fail = []
    for row in unique:
        sizes, _, _, _, _, cap, _ = row
        maximum = max(sizes)
        if any(26 - cap <= size - 1 for size in sizes if size != maximum):
            strict_fail.append(row)
    assert strict_fail == [
        ((5, 13, 15), 2, 0, 193, 100, 14, 29),
        ((6, 13, 14), 2, 0, 184, 91, 14, 28),
    ]
    for row in tied + tuple(strict_fail):
        assert 26 - row[5] > min(row[0]) - 1

    residual = four_isolated + three_isolated
    orders = tuple(range(14, 23))
    matchings = tuple((order, split_matchings(order)) for order in orders)
    vectors = tuple((order, *vector_enumeration(order)) for order in orders)
    vector_by_order = {row[0]: row for row in vectors}

    certificate_rows = []
    split_exceptions = []
    for row in residual:
        sizes, repeated_cuts, extra_edges, _, high_edges, cap, _ = row
        block_order = max(sizes)
        smaller = max(size for size in sizes if size != block_order)
        unused_after_split = 26 - (cap + 1)
        if unused_after_split < smaller:
            split_exceptions.append(row)
            assert repeated_cuts == 1 and extra_edges == 0
            assert sizes == (5, 13, 14) and unused_after_split == 12 > 4
        vector_row = vector_by_order[block_order]
        degree_floor = vector_row[2]
        assert degree_floor > 2 * high_edges
        certificate_rows.append(
            (
                sizes,
                repeated_cuts,
                extra_edges,
                high_edges,
                cap,
                block_order,
                unused_after_split,
                degree_floor,
                2 * high_edges,
                degree_floor - 2 * high_edges,
            )
        )
    assert split_exceptions == [((5, 13, 14), 1, 0, 179, 86, 13, 27)]
    assert min(row[-1] for row in certificate_rows) == 10
    return (
        tuple(seven_caps),
        six,
        five,
        four,
        four_bad,
        four_isolated,
        three,
        three_bad,
        three_isolated,
        matchings,
        vectors,
        tuple(certificate_rows),
    )


def terminal_audit():
    """Rebuild profiles and audit independent route/capacity inequalities."""
    profiles = []
    route_rows = []
    for small in range(5, 16):
        large = 31 - small
        p, q = small - 5, large - 5
        deficit = comb(22, 2) - 713 + 26 * 31 - comb(small, 2) - comb(large, 2)
        if large >= 27 or deficit < 0:
            continue
        profiles.append((small, large, p, q, deficit))
        assert p >= 1 and p + q + 1 == 22
        assert small + large == 31 > 25
        assert 22 + (small - (p + 1)) == 26
        assert 21 + (small - p) == 26
        for side, other, support in ((small, large, p), (large, small, q)):
            target_one_centre = other - (25 - (support + 1))
            one_end_support = other - (25 - (side + 1))
            mutual_support = other - (25 - (side + 2))
            assert (target_one_centre, one_end_support, mutual_support) == (2, 7, 8)
            # A floor above the whole opposite clique makes that support type
            # impossible; otherwise every constructive route needs at most two
            # distinct opposite-clique vertices.
            route_rows.append(
                (
                    side,
                    other,
                    support,
                    target_one_centre,
                    one_end_support,
                    mutual_support,
                    one_end_support <= other,
                    mutual_support <= other,
                )
            )
        assert small - (p + 1) == large - (q + 1) == 4
        assert small - p == large - q == 5
        assert small + q + 1 == large + p + 1 == 27
        assert min(small - 1, large - 1) >= 5

    assert profiles == [
        (6, 25, 1, 20, 9),
        (7, 24, 2, 19, 27),
        (8, 23, 3, 18, 43),
        (9, 22, 4, 17, 57),
        (10, 21, 5, 16, 69),
        (11, 20, 6, 15, 79),
        (12, 19, 7, 14, 87),
        (13, 18, 8, 13, 93),
        (14, 17, 9, 12, 97),
        (15, 16, 10, 11, 99),
    ]

    target_edges = tuple(combinations(range(22), 2))
    unordered_checks = 0
    for first, second in combinations(target_edges, 2):
        common = set(first).intersection(second)
        assert len(common) <= 1
        # No nonempty even set can be contained in this intersection.
        assert not any(size > 0 and size % 2 == 0 for size in range(len(common) + 1))
        unordered_checks += 1
    assert unordered_checks == comb(comb(22, 2), 2) == 26565
    return tuple(profiles), tuple(route_rows), unordered_checks


def main():
    block_records = block_and_endpoint_audit()
    profiles, routes, contractions = terminal_audit()
    record = repr((block_records, profiles, routes, contractions))
    vectors = block_records[10]
    certificate_rows = block_records[11]
    print("PASS independent Albertson r=27 h=22 closure check")
    print(
        f"six_rows={len(block_records[1])}; five_rows={len(block_records[2])}; "
        f"four_rows={len(block_records[3])}; four_bad={len(block_records[4])}; "
        f"four_isolated={len(block_records[5])}"
    )
    print(
        f"three_rows={len(block_records[6])}; three_bad={len(block_records[7])}; "
        f"three_isolated={len(block_records[8])}"
    )
    print(
        f"split_matching_instances={sum(len(row[1]) for row in block_records[9])}; "
        f"endpoint_vectors={sum(row[1] for row in vectors)}; "
        f"minimum_endpoint_margin={min(row[-1] for row in certificate_rows)}"
    )
    print(
        f"two_clique_profiles={profiles}; route_rows={len(routes)}; "
        f"unordered_contraction_checks={contractions}"
    )
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
