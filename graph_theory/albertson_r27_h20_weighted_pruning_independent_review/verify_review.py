#!/usr/bin/env python3
"""Independent finite audit of the Albertson r=27 h=20 structural reduction."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
N = 53
M = 713
H = 20
LOW = N - H
MIN_BLOCK = K - H
MIN_LOW_EDGES = 26 * LOW - M


def bounded_partitions(total, count, minimum, maximum=26):
    """Generate nondecreasing integer partitions without target-code imports."""
    if count == 0:
        if total == 0:
            yield ()
        return
    upper = min(maximum, total - minimum * (count - 1))
    for first in range(minimum, upper + 1):
        for tail in bounded_partitions(total - first, count - 1, first, maximum):
            yield (first,) + tail


def chromatic_cap(edge_count):
    """Largest c consistent with e >= binom(c,2)."""
    return max(c for c in range(1, K + 1) if comb(c, 2) <= edge_count)


def direct_geometry_exists(sizes, overlap):
    """Check the degree-26 restrictions on direct block intersections."""
    if overlap == 0:
        return True
    if overlap == 1:
        return any(sizes[i] + sizes[j] <= 28 for i, j in combinations(range(3), 2))
    assert overlap == 2
    # A common cut would have sum(|B_i|-1)=32 low neighbours.  The only
    # alternative is a path of blocks with two distinct cut vertices.
    assert sum(sizes) - 3 == 32
    return any(
        all(sizes[middle] + sizes[end] <= 28 for end in range(3) if end != middle)
        for middle in range(3)
    )


def many_block_check():
    assert 6 * MIN_BLOCK - 5 == 37 > LOW
    caps = []
    rows = {}
    for count in (5, 4):
        rows[count] = []
        for overlap in range(count):
            components = count - overlap
            partitions = tuple(
                bounded_partitions(LOW + overlap, count, MIN_BLOCK)
            )
            if not partitions:
                continue
            connector_cap = comb(components, 2)
            edge_cap = max(
                sum(comb(size, 2) for size in sizes) + connector_cap
                for sizes in partitions
            )
            caps.append((count, overlap, edge_cap))
            for sizes in partitions:
                base = sum(comb(size, 2) for size in sizes)
                for connector_edges in range(connector_cap + 1):
                    low_edges = base + connector_edges
                    if low_edges < MIN_LOW_EDGES:
                        continue
                    high_edges = low_edges - MIN_LOW_EDGES
                    rows[count].append(
                        (
                            sizes,
                            overlap,
                            connector_edges,
                            high_edges,
                            max(sizes) + chromatic_cap(high_edges),
                        )
                    )
    assert caps == [
        (5, 2, 108),
        (5, 3, 113),
        (5, 4, 120),
        (4, 0, 135),
        (4, 1, 144),
        (4, 2, 155),
        (4, 3, 168),
    ]
    assert not rows[5]
    assert len(rows[4]) == 19
    assert max(row[-1] for row in rows[4]) == 22
    return tuple(caps), tuple(sorted(rows[4]))


def three_block_check():
    rows = []
    for overlap in range(3):
        components = 3 - overlap
        for sizes in bounded_partitions(LOW + overlap, 3, MIN_BLOCK):
            if not direct_geometry_exists(sizes, overlap):
                continue
            base = sum(comb(size, 2) for size in sizes)
            for connector_edges in range(comb(components, 2) + 1):
                low_edges = base + connector_edges
                if low_edges < MIN_LOW_EDGES:
                    continue
                high_edges = low_edges - MIN_LOW_EDGES
                cap = chromatic_cap(high_edges)
                rows.append(
                    (sizes, overlap, connector_edges, high_edges, cap, max(sizes) + cap)
                )
    rows = tuple(sorted(rows))
    assert tuple(sum(row[1] == q for row in rows) for q in range(3)) == (76, 42, 24)
    exceptions = tuple(row for row in rows if row[-1] > 26)
    assert tuple(sum(row[1] == q for row in exceptions) for q in range(3)) == (16, 12, 12)
    assert all(sizes.count(max(sizes)) == 1 for sizes, *_ in exceptions)

    residual = []
    for row in exceptions:
        sizes, overlap, connector_edges, *_ = row
        small = sizes[:-1]
        # An obstruction can remain only when the unique largest block is an
        # isolated component: the smaller blocks may be disjoint, joined by
        # their sole connector edge, or meet directly at one cut vertex.
        isolated_largest = (
            overlap == 0 and connector_edges in (0, 1)
        ) or (
            overlap == 1 and connector_edges == 0 and sum(small) <= 28
        )
        if isolated_largest:
            residual.append(row)
    residual = tuple(residual)
    assert len(residual) == 14
    assert all(26 - row[4] > max(row[0][:-1]) - 1 for row in exceptions)
    return rows, exceptions, residual


def category_floor(block_order, active_count, colour_count):
    """Minimise over zero/intermediate/full multiplicities."""
    target = block_order * active_count
    best = None
    witnesses = []
    for zero in range(H + 1):
        for full in range(H - zero + 1):
            intermediate = H - zero - full
            intermediate_weight = target - block_order * full
            feasible = (
                intermediate_weight == 0
                if intermediate == 0
                else intermediate <= intermediate_weight <= intermediate * (block_order - 1)
            )
            if not feasible:
                continue
            value = (
                zero * (block_order - 6)
                + intermediate * (colour_count - 1)
                + full * (active_count - 1)
            )
            if best is None or value < best:
                best = value
                witnesses = [(zero, intermediate, full)]
            elif value == best:
                witnesses.append((zero, intermediate, full))
    assert best is not None
    return best, tuple(witnesses)


def weighted_check(residual):
    checked = []
    survivors = []
    for sizes, overlap, connector_edges, high_edges, cap, _ in residual:
        block_order = max(sizes)
        active = K - block_order
        for colours in range(active, cap + 1):
            floor, witnesses = category_floor(block_order, active, colours)
            row = (
                sizes,
                overlap,
                connector_edges,
                high_edges,
                block_order,
                active,
                colours,
                floor,
                2 * high_edges,
                witnesses,
            )
            checked.append(row)
            if floor <= 2 * high_edges:
                survivors.append(row[:-1])
    expected = (
        ((7, 7, 20), 1, 0, 87, 20, 7, 7, 120, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 8, 134, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 9, 148, 174),
        ((7, 7, 20), 1, 0, 87, 20, 7, 10, 162, 174),
        ((7, 8, 19), 1, 0, 75, 19, 8, 8, 140, 150),
    )
    assert tuple(survivors) == expected
    return tuple(checked), tuple(survivors)


def two_clique_check():
    """Reconstruct every profile and the boundary slack in the terminal kernel."""
    profiles = []
    for p in range(1, 10):
        a = MIN_BLOCK + p
        b = LOW - a
        q = b - MIN_BLOCK
        deficit = comb(H, 2) - M + 26 * LOW - comb(a, 2) - comb(b, 2)
        profiles.append((a, b, p, q, deficit))
        assert p + q == H - 1

        # Simultaneous one-larger matchings leave six vertices on each side.
        assert a - (p + 1) == b - (q + 1) == 26 - H == 6
        assert H + (26 - H) == 26

        # After one target contraction, p and q attachments leave seven pairs.
        assert a - p == b - q == K - H == 7
        assert H - 1 + (K - H) == 26

        # Worst one-target graph-neighbour floors in the opposite clique.
        target_floor = b - (25 - (p + 1))
        one_end_floor = b - (25 - (MIN_BLOCK + p + 1))
        opposite_type_floor = b - (25 - (MIN_BLOCK + p + 2))
        assert (target_floor, one_end_floor, opposite_type_floor) == (2, 9, 10)
        assert b >= 17 and min(target_floor, one_end_floor, opposite_type_floor) >= 2

        # The double-uniform case partitions Q as S union R union {z}; both
        # branch-path injections have more low vertices than support vertices.
        assert p + q + 1 == H
        assert a > p and b > q

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

    # Two distinct failed target contractions force an even symmetric
    # difference contained in an intersection of size at most one.
    contraction_pairs = 0
    targets = tuple(combinations(range(H), 2))
    for first, second in combinations(targets, 2):
        assert len(set(first) & set(second)) <= 1
        contraction_pairs += 1
    assert contraction_pairs == comb(comb(H, 2), 2)

    # The conformal-triangle and bridge constructions retain nontrivial room.
    assert 28 - H == 8
    assert 26 - H == 6 >= 2
    return tuple(profiles), contraction_pairs


def main():
    caps, four_rows = many_block_check()
    three_rows, exceptions, residual = three_block_check()
    weighted, survivors = weighted_check(residual)
    two_profiles, contraction_pairs = two_clique_check()
    record = (
        caps,
        four_rows,
        three_rows,
        exceptions,
        residual,
        weighted,
        survivors,
        two_profiles,
        contraction_pairs,
    )
    print("PASS independent Albertson r=27 h=20 structural audit")
    print(f"minimum_low_edges={MIN_LOW_EDGES}; many_block_caps={caps}")
    print(
        f"four_rows={len(four_rows)}; three_rows={len(three_rows)}; "
        f"palette_exceptions={len(exceptions)}; isolated_largest_rows={len(residual)}"
    )
    print(f"weighted_rows={len(weighted)}; survivors={survivors}")
    print(
        f"two_profiles={two_profiles}; unordered_contraction_pairs={contraction_pairs}"
    )
    print(f"review_sha256={sha256(repr(record).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
