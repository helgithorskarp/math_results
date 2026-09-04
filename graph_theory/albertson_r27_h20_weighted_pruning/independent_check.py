#!/usr/bin/env python3
"""Independent finite check of the Albertson r=27 h=20 reduction."""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from math import comb


def colour_cap(edges):
    return max(c for c in range(1, 28) if comb(c, 2) <= edges)


def tuples_with_sum(length, total):
    return tuple(
        row
        for row in combinations_with_replacement(range(7, 27), length)
        if sum(row) == total
    )


def three_geometry_exists(sizes, overlap):
    if overlap == 0:
        return True
    if overlap == 1:
        return any(sizes[i] + sizes[j] <= 28 for i, j in combinations(range(3), 2))
    assert overlap == 2
    # A common cut has 32 low neighbours.  Test the three possible middle
    # blocks of a path with distinct cut vertices.
    return any(
        all(sizes[middle] + sizes[end] <= 28 for end in range(3) if end != middle)
        for middle in range(3)
    )


def category_weight_floor(b, active, colours):
    """Minimise by zero/intermediate/full multiplicities, not vertex DP."""
    target = b * active
    best = None
    witnesses = []
    for zero in range(21):
        for full in range(21 - zero):
            intermediate = 20 - zero - full
            remainder = target - b * full
            feasible = (
                remainder == 0
                if intermediate == 0
                else intermediate <= remainder <= intermediate * (b - 1)
            )
            if not feasible:
                continue
            value = zero * (b - 6) + full * (active - 1) + intermediate * (colours - 1)
            if best is None or value < best:
                best = value
                witnesses = [(zero, intermediate, full)]
            elif value == best:
                witnesses.append((zero, intermediate, full))
    assert best is not None
    return best, tuple(witnesses)


def main():
    low = 33
    threshold = 145

    # Connector blocks form a hyperforest on the direct large-block
    # components, so their edge total is at most C(components,2).
    block_summary = []
    for count in (5, 4):
        for overlap in range(count):
            components = count - overlap
            rows = tuples_with_sum(count, low + overlap)
            if not rows:
                continue
            edge_cap = max(
                sum(comb(x, 2) for x in sizes) + comb(components, 2)
                for sizes in rows
            )
            block_summary.append((count, overlap, edge_cap))
    assert block_summary == [
        (5, 2, 108),
        (5, 3, 113),
        (5, 4, 120),
        (4, 0, 135),
        (4, 1, 144),
        (4, 2, 155),
        (4, 3, 168),
    ]

    four_survivors = []
    for overlap in (2, 3):
        components = 4 - overlap
        for sizes in tuples_with_sum(4, low + overlap):
            base = sum(comb(x, 2) for x in sizes)
            for extra in range(comb(components, 2) + 1):
                e_low = base + extra
                if e_low < threshold:
                    continue
                e_high = e_low - threshold
                four_survivors.append((sizes, overlap, extra, max(sizes) + colour_cap(e_high)))
    assert len(four_survivors) == 19
    assert max(row[-1] for row in four_survivors) == 22

    three_rows = []
    for overlap in range(3):
        components = 3 - overlap
        for sizes in tuples_with_sum(3, low + overlap):
            if not three_geometry_exists(sizes, overlap):
                continue
            base = sum(comb(x, 2) for x in sizes)
            for extra in range(comb(components, 2) + 1):
                e_low = base + extra
                if e_low < threshold:
                    continue
                e_high = e_low - threshold
                c_cap = colour_cap(e_high)
                three_rows.append((sizes, overlap, extra, e_high, c_cap, max(sizes) + c_cap))
    assert tuple(sum(row[1] == q for row in three_rows) for q in range(3)) == (76, 42, 24)

    obstructed = [row for row in three_rows if row[-1] > 26]
    assert tuple(sum(row[1] == q for row in obstructed) for q in range(3)) == (16, 12, 12)
    for sizes, _, _, _, c_cap, _ in obstructed:
        largest_index = sizes.index(max(sizes))
        assert sizes.count(sizes[largest_index]) == 1
        smaller = sizes[:largest_index] + sizes[largest_index + 1 :]
        assert 26 - c_cap > max(smaller) - 1

    rigid = [
        row
        for row in obstructed
        if (row[1] == 0 and row[2] in (0, 1)) or (row[1] == 1 and row[2] == 0)
    ]
    assert len(rigid) == 14

    weighted = []
    survivor_witnesses = []
    for sizes, overlap, extra, e_high, c_cap, _ in rigid:
        b = max(sizes)
        active = 27 - b
        for colours in range(active, c_cap + 1):
            floor, witnesses = category_weight_floor(b, active, colours)
            if floor <= 2 * e_high:
                weighted.append((sizes, overlap, extra, e_high, colours, floor))
                survivor_witnesses.append((b, active, colours, witnesses))
    assert weighted == [
        ((7, 7, 20), 1, 0, 87, 7, 120),
        ((7, 7, 20), 1, 0, 87, 8, 134),
        ((7, 7, 20), 1, 0, 87, 9, 148),
        ((7, 7, 20), 1, 0, 87, 10, 162),
        ((7, 8, 19), 1, 0, 75, 8, 140),
    ]

    # Independently reconstruct the two-block table and all numerical slack
    # used by the already established matching/conformal-triangle mechanism.
    two_rows = []
    numerical_checks = 0
    for small in range(7, 17):
        large = low - small
        if large >= 27:
            continue
        p, q = small - 7, large - 7
        deficit = comb(20, 2) - 713 + 26 * low - comb(small, 2) - comb(large, 2)
        if deficit < 0:
            continue
        two_rows.append((small, large, p, q, deficit))
        assert p + q + 1 == 20
        assert small - p == large - q == 7
        assert small - p - 1 == large - q - 1 == 6
        assert large - (25 - (p + 1)) == 2
        assert large - (25 - (7 + p + 1)) == 9
        assert large - (25 - (7 + p + 2)) == 10
        numerical_checks += 6
    assert two_rows == [
        (8, 25, 1, 18, 7),
        (9, 24, 2, 17, 23),
        (10, 23, 3, 16, 37),
        (11, 22, 4, 15, 49),
        (12, 21, 5, 14, 59),
        (13, 20, 6, 13, 67),
        (14, 19, 7, 12, 73),
        (15, 18, 8, 11, 77),
        (16, 17, 9, 10, 79),
    ]

    record = (
        f"blocks={block_summary};four={four_survivors};three={three_rows};"
        f"rigid={rigid};weighted={weighted};witnesses={survivor_witnesses};"
        f"two={two_rows};checks={numerical_checks}"
    )
    print("PASS independent Albertson r=27 h=20 pruning check")
    print(f"block_summary={block_summary}")
    print(f"four_rows={len(four_survivors)}; four_max_palette={max(row[-1] for row in four_survivors)}")
    print(f"three_rows={len(three_rows)}; list_obstructions={len(obstructed)}; rigid_forms={len(rigid)}")
    print(f"weighted_survivors={weighted}")
    print(f"two_block_rows={two_rows}; numerical_checks={numerical_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
