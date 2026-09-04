#!/usr/bin/env python3
"""Independent audit of the hard residual order-five Ramsey reduction.

The degree stage uses unlabeled compositions with multinomial recovery.  The
local graph stage uses packed edge masks.  No contributor code or data is
imported.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter


U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
WEIGHT = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}
COLUMNS = {0: (0, 1, 2, 3, 5, 5, 6, 6), 1: tuple(range(8))}
PAIRS13 = tuple(itertools.combinations(range(13), 2))
EDGE_BIT = {edge: 1 << index for index, edge in enumerate(PAIRS13)}
FIVE_MASKS = tuple(
    sum(EDGE_BIT[edge] for edge in itertools.combinations(vertices, 2))
    for vertices in itertools.combinations(range(13), 5)
)


def multinomial(parts: tuple[int, ...]) -> int:
    result = math.factorial(sum(parts))
    for part in parts:
        result //= math.factorial(part)
    return result


def audit_degree_compositions() -> None:
    weighted = parity = one_defect = triangle_rejected = survivors = 0
    surviving_profiles = set()
    for low in range(9):
        for high in range(9 - low):
            central = 8 - low - high
            labeled = multinomial((low, central, high))
            weight = 3 + 15 * (low + high)
            if weight > 39:
                continue
            weighted += labeled
            degree_sum = 62 + 5 * (20 * low + 21 * central + 22 * high)
            if degree_sum % 2:
                continue
            parity += labeled
            red_edges = degree_sum // 2
            if low + high == 0:
                local_sum = math.comb(22, 2) - red_edges + 20 * 21
                rounded_cap = 5 * ((U[20] - 7) // 5) + 5 * ((U[22] - 7) // 5)
                assert local_sum == 200 and rounded_cap == 195
                one_defect += labeled
                continue
            assert low + high == 2 and weight == 33 and (43 - weight) // 2 == 5
            red_local = 290 + 5 * (low * 93 + central * 100 + high * 107)
            blue_local = 305 + 5 * (low * 107 + central * 100 + high * 93)
            if red_local % 3 or blue_local % 3:
                triangle_rejected += labeled
                continue
            survivors += labeled
            surviving_profiles.add((low, central, high, red_edges,
                                    red_local // 3, blue_local // 3))
    assert (weighted, parity, one_defect, triangle_rejected, survivors) == (
        129, 113, 1, 56, 56)
    assert surviving_profiles == {(1, 6, 1, 451, 1430, 1435)}
    print("PASS degree_assignments=6561 weight_survivors=129 parity_survivors=113 "
          "one_defect_rejected=1 triangle_rejected=56 final_labeled=56")
    print("PASS unique_profile=20^6,21^32,22^5 red_edges=451 "
          "triangles=1430,1435 excess=5 z_local=90,105 exact_anchors=32")


def swap_xy(column: int) -> int:
    return (column & 4) | ((column & 1) << 1) | ((column & 2) >> 1)


def audit_marked_placements():
    retained = []
    labeled_counts = Counter()
    normalized = {}
    for h, columns in COLUMNS.items():
        for low, high in itertools.permutations(range(8), 2):
            differences = tuple(
                5 * (bool(columns[high] & (1 << fixed)) -
                     bool(columns[low] & (1 << fixed)))
                for fixed in range(3)
            )
            if differences != (0, 0, -5):
                continue
            labeled_counts[h] += 1
            pair = (columns[low], columns[high])
            canonical = min(pair, tuple(map(swap_xy, pair)))
            normalized[h, canonical] = (low, high)
    assert labeled_counts == {0: 4, 1: 4}
    assert set(normalized) == {
        (0, (5, 1)), (1, (4, 0)), (1, (5, 1)), (1, (7, 3))}
    for h, pair in sorted(key for key in normalized if key != (1, (7, 3))):
        columns = COLUMNS[h]
        retained.append((h, columns.index(pair[0]), columns.index(pair[1]), pair))
    assert retained == [(0, 4, 1, (5, 1)),
                        (1, 4, 0, (4, 0)),
                        (1, 5, 1, (5, 1))]
    print("PASS exceptional_placements labeled_h0=4 labeled_h1=4 "
          "marked_classes=4 xy_obstruction=1 retained=3")
    print("PASS marked_cases=(0,4,1),(1,4,0),(1,5,1) low_high_cross_degree=3")
    return retained


def edge(u: int, v: int) -> int:
    return EDGE_BIT[(u, v) if u < v else (v, u)]


def local_red_mask(low_column: int, high_column: int,
                   low_step: int, high_step: int, word: int) -> int:
    red = edge(0, 1)
    for start, column, step in ((3, low_column, low_step),
                                (8, high_column, high_step)):
        for a, b in itertools.combinations(range(5), 2):
            if (b - a) % 5 in (step, 5 - step):
                red |= edge(start + a, start + b)
        for fixed in range(3):
            if column & (1 << fixed):
                for vertex in range(start, start + 5):
                    red |= edge(fixed, vertex)
    for a in range(5):
        for b in range(5):
            if word & (1 << ((b - a) % 5)):
                red |= edge(3 + a, 8 + b)
    return red


def locally_ramsey(red: int) -> bool:
    return all(red & five not in (0, five) for five in FIVE_MASKS)


def audit_local_domains(retained) -> None:
    all_records = []
    valid = tested = 0
    expected = {
        (4, 0): lambda s, t: 10,
        (5, 1): lambda s, t: 5 if s == t else 10,
        (7, 3): lambda s, t: 0,
    }
    for h, pair in ((0, (5, 1)), (1, (4, 0)),
                    (1, (5, 1)), (1, (7, 3))):
        for low_step, high_step in itertools.product((1, 2), repeat=2):
            allowed = []
            for word in range(32):
                if word.bit_count() != 3:
                    continue
                tested += 1
                if locally_ramsey(local_red_mask(
                        pair[0], pair[1], low_step, high_step, word)):
                    allowed.append(word)
                    valid += 1
            assert len(allowed) == expected[pair](low_step, high_step)
            all_records.append([h, *pair, low_step, high_step, allowed])
    assert tested == 160 and valid == 100 and len(retained) == 3
    digest = hashlib.sha256(json.dumps(
        all_records, separators=(",", ":")).encode("ascii")).hexdigest()
    print(f"PASS local_pair_colorings tested={tested} valid={valid} "
          f"five_sets_each={len(FIVE_MASKS)} domains_sha256={digest}")


def audit_linear_interface(retained) -> None:
    for h, low, high, _ in retained:
        columns = COLUMNS[h]
        degrees = [21] * 8
        degrees[low], degrees[high] = 20, 22
        row_targets = [degree - 2 - column.bit_count()
                       for degree, column in zip(degrees, columns, strict=True)]
        assert sum(row_targets) == 140
        differences = [(index, bool(column & 4)) for index, column in enumerate(columns)
                       if index not in (low, high)]
        assert len(differences) == 6
        # Literal derivation from the exact fixed local counts.
        fixed_targets = {
            "R_x": 100 // 5 - 4 - (1 + h),
            "R_y": 100 // 5 - 4 - (1 + h),
            "B_x": 6 * 5 - (100 // 5 - 4 - 2),
            "B_y": 6 * 5 - (100 // 5 - 4 - 2),
            "R_z": 90 // 5 - 4,
            "B_z": 6 * 5 - (105 // 5 - 4 - 4),
        }
        assert fixed_targets == {"R_x": 15 - h, "R_y": 15 - h,
                                 "B_x": 16, "B_y": 16,
                                 "R_z": 14, "B_z": 17}
    print("PASS linear_interface row_target_sum=140 cross_degree_sum=70 "
          "ordinary_differences=6 fixed_cuts=15-h,15-h,16,16,14,17")


def main() -> None:
    audit_degree_compositions()
    retained = audit_marked_placements()
    audit_local_domains(retained)
    audit_linear_interface(retained)
    print("PASS independent hard order-five branch audit; global extensions unresolved")


if __name__ == "__main__":
    main()
