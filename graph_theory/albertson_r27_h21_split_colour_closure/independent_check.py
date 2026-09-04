#!/usr/bin/env python3
"""Independent arithmetic/matching audit of the Albertson h=21 closure."""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from math import comb


def colour_cap(edges):
    return max(c for c in range(1, 28) if comb(c, 2) <= edges)


def tuples_with_sum(length, total):
    return tuple(
        row
        for row in combinations_with_replacement(range(6, 27), length)
        if sum(row) == total
    )


def rows_for_count(count):
    rows = []
    for overlap in range(count):
        components = count - overlap
        for sizes in tuples_with_sum(count, 32 + overlap):
            base = sum(comb(size, 2) for size in sizes)
            for extra in range(comb(components, 2) + 1):
                low_edges = base + extra
                if low_edges < 119:
                    continue
                high_edges = low_edges - 119
                cap = colour_cap(high_edges)
                rows.append((sizes, overlap, extra, low_edges, high_edges, cap, max(sizes) + cap))
    return tuple(sorted(rows))


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


def split_matchings(order):
    """Construct both list types and find an SDR at every split size."""
    active = 27 - order
    active_colours = set(range(active))
    palette = set(range(26))
    old = 0
    fresh = 25
    records = []
    for weight in range(1, order):
        lists = []
        for vertex in range(order):
            forbidden = (
                (active_colours - {old}) | {fresh}
                if vertex < weight
                else active_colours
            )
            available = tuple(sorted(palette - forbidden))
            assert len(available) == order - 1
            lists.append(available)
        matching = maximum_matching(lists)
        assert matching == order
        records.append((weight, matching))
    return tuple(records)


def endpoint_enumeration(order):
    """Enumerate every labelled zero/full vector for one block order."""
    active = 27 - order
    expected_floor = active * (active - 1) + (21 - active) * (order - 5)
    count = 0
    digest_terms = []
    for full_vertices in combinations(range(21), active):
        full = set(full_vertices)
        weights = tuple(order if vertex in full else 0 for vertex in range(21))
        assert sum(weights) == order * active
        degree_sum = sum(active - 1 if weight else order - 5 for weight in weights)
        assert degree_sum == expected_floor
        digest_terms.append((full_vertices, degree_sum))
        count += 1
    assert count == comb(21, active)
    return count, expected_floor, sha256(repr(digest_terms).encode()).hexdigest()


def main():
    # Convex connector caps are reconstructed with combinations rather than
    # the recursive partition generator used by the primary checker.
    caps = []
    for count in (6, 5):
        for overlap in range(count):
            components = count - overlap
            tuples = tuples_with_sum(count, 32 + overlap)
            if not tuples:
                continue
            edge_cap = max(
                sum(comb(size, 2) for size in sizes) + comb(components, 2)
                for sizes in tuples
            )
            caps.append((count, overlap, edge_cap))
    assert caps == [
        (6, 4, 91),
        (6, 5, 96),
        (5, 0, 98),
        (5, 1, 102),
        (5, 2, 108),
        (5, 3, 116),
        (5, 4, 126),
    ]

    five = rows_for_count(5)
    four = rows_for_count(4)
    three = rows_for_count(3)
    assert len(five) == 2 and max(row[-1] for row in five) == 16
    assert tuple(sum(row[1] == q for row in four) for q in range(4)) == (73, 72, 46, 27)
    four_bad = tuple(row for row in four if row[-1] > 26)
    assert four_bad == (((6, 6, 6, 17), 3, 0, 181, 62, 11, 28),)

    three_bad = tuple(row for row in three if row[-1] > 26)
    assert tuple(sum(row[1] == q for row in three_bad) for q in range(3)) == (36, 26, 21)
    tied = tuple(row for row in three_bad if row[0].count(max(row[0])) > 1)
    assert tied == (((6, 14, 14), 2, 0, 197, 78, 13, 27),)
    for sizes, _, _, _, _, cap, _ in three_bad:
        if sizes.count(max(sizes)) == 1:
            assert all(26 - cap > size - 1 for size in sizes if size != max(sizes))

    isolated = tuple(
        row
        for row in three_bad
        if row not in tied
        and ((row[1] == 0 and row[2] <= 1) or (row[1] == 1 and row[2] == 0))
    )
    assert len(isolated) == 31

    orders = tuple(sorted({max(row[0]) for row in isolated}))
    assert orders == (15, 16, 17, 18, 19, 20, 21)
    split_records = tuple((order, split_matchings(order)) for order in orders)
    endpoint_records = tuple((order, *endpoint_enumeration(order)) for order in orders)

    endpoint_rows = []
    for sizes, overlap, extra, _, high_edges, cap, _ in isolated:
        order = max(sizes)
        smaller = max(size for size in sizes if size != order)
        assert 26 - (cap + 1) >= smaller
        floor = next(row[2] for row in endpoint_records if row[0] == order)
        assert floor > 2 * high_edges
        endpoint_rows.append((sizes, overlap, extra, high_edges, cap, order, floor, 2 * high_edges))
    endpoint_rows = tuple(endpoint_rows)
    assert min(row[-2] - row[-1] for row in endpoint_rows) == 28

    # Independently reconstruct the two-clique profile table and every new
    # parameter value used by the inherited matching/topological dichotomy.
    two = []
    numerical_checks = 0
    for small in range(6, 17):
        large = 32 - small
        if large >= 27:
            continue
        p, q = small - 6, large - 6
        deficit = comb(21, 2) - 713 + 26 * 32 - comb(small, 2) - comb(large, 2)
        if deficit < 0:
            continue
        two.append((small, large, p, q, deficit))
        assert p >= 1 and p + q + 1 == 21
        assert small - p - 1 == large - q - 1 == 5
        assert small - p == large - q == 6
        assert large - (25 - (p + 1)) == 2
        assert large - (25 - (6 + p + 1)) == 8
        assert large - (25 - (6 + p + 2)) == 9
        numerical_checks += 6
    assert two == [
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
    ]

    record = (
        f"caps={caps};five={five};four={four};four_bad={four_bad};"
        f"three={three};three_bad={three_bad};tied={tied};isolated={isolated};"
        f"splits={split_records};endpoint_records={endpoint_records};"
        f"endpoint_rows={endpoint_rows};two={two};checks={numerical_checks}"
    )
    print("PASS independent Albertson r=27 h=21 closure check")
    print(f"caps={caps}; five_rows={len(five)}")
    print(f"four_rows={len(four)}; strict_list_exceptions={len(four_bad)}")
    print(
        f"three_rows={len(three)}; list_exceptions={len(three_bad)}; "
        f"isolated_rows={len(isolated)}"
    )
    print(
        f"split_matching_instances={sum(len(row[1]) for row in split_records)}; "
        f"endpoint_vectors={sum(row[1] for row in endpoint_records)}"
    )
    print(f"minimum_endpoint_margin={min(row[-2] - row[-1] for row in endpoint_rows)}")
    print(f"two_clique_profiles={two}; numerical_checks={numerical_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
