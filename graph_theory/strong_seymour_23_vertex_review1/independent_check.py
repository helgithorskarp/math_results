#!/usr/bin/env python3
"""Definition-level review of the order-23 strong-Seymour counterexample.

This checker imports no module and reads no certificate from the target package.
It treats the published 23-by-23 adjacency matrix as its sole target input.
"""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "strong_seymour_23_vertex_construction" / "tournament23.txt"

PART_SIZES = (1, 1, 1, 1, 2, 1, 1, 1, 4, 4, 1, 1, 4)
PART_TYPES = (0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 2)
BASE_WEIGHTS = (1, 1, 1, 1, 2, 1, 1, 1, 4, 4, 1, 1, 4)
SOURCES = (
    (9, 10), (7, 8), (1, 3, 4, 7, 8), (1, 4, 7, 8),
    (0, 5, 6, 9, 10), (2, 3, 6, 11, 12), (2, 3, 11, 12),
    (8,), (0, 4, 5, 6, 9, 10), (2, 3, 5, 6, 10, 11, 12),
    (2, 3, 5, 6, 11, 12), (12,), (1, 2, 3, 4, 7, 8),
)
TARGET_PARTS = (
    (2, 3, 5, 6), (4, 5, 6), (5, 6, 9, 10, 11),
    (5, 6, 9, 10), (2, 3, 7, 12), (4, 7, 8), (4, 8),
    (0, 6, 10), (1, 2, 3, 7, 11, 12), (0, 1, 4, 7, 8),
    (0, 1, 4, 8), (3, 4), (0, 5, 6, 9, 10, 11),
)
EXPECTED_MAX_FORMS = (
    ((-3, 0, 1), (-2, -1, 1), (0, 0, 0)),
    ((-1, -1, 1), (0, 0, 0)),
    ((-1, 1, 0), (0, 0, 0), (0, 1, -1), (1, 0, -2)),
    ((-1, 1, 0), (0, 0, 0), (0, 1, -1), (1, 0, -2)),
    ((1, 0, 0), (3, 0, -1)),
    ((0, 0, 0), (1, 0, -1), (2, 0, -2), (3, -1, 0), (4, -1, -1)),
    ((0, 0, 0), (1, 0, -1), (2, 0, -2), (3, -1, 0), (4, -1, -1)),
    ((-5, 1, 1), (-3, 0, 1), (0, 0, 0)),
    ((-1, 1, 0), (0, 0, 0)),
    ((0, 0, 0), (1, 0, -1), (3, -1, 0)),
    ((0, 0, 0), (1, 0, -1), (3, -1, 0), (4, -1, -1)),
    ((-1, -1, 1), (0, 0, 0)),
    ((-1, 1, 0), (0, 0, 0)),
)
DUAL = (51, 31, 37, 148, 162, 1, 131, 1, 100, 1, 132, 37, 88)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_literal() -> tuple[list[int], bytes]:
    data = TARGET.read_bytes()
    lines = data.decode("ascii").splitlines()
    need(len(lines) == 23, "literal must have 23 rows")
    need(all(len(line) == 23 and set(line) <= {"0", "1"} for line in lines),
         "literal is not a square zero-one matrix")
    rows = [sum((bit == "1") << j for j, bit in enumerate(line)) for line in lines]
    for i, row in enumerate(rows):
        need(not (row >> i) & 1, "literal has a loop")
        for j in range(i):
            need(((row >> j) & 1) ^ ((rows[j] >> i) & 1),
                 "literal is not a tournament")
    return rows, data


def exact_second(rows: list[int], root: int) -> int:
    first = rows[root]
    reached = 0
    bits = first
    while bits:
        low = bits & -bits
        reached |= rows[low.bit_length() - 1]
        bits ^= low
    return reached & ~first & ~(1 << root) & ((1 << len(rows)) - 1)


def matching_by_state_dp(rows: list[int], left_mask: int, right_mask: int) -> int:
    """Maximum matching cardinality via reachable used-right masks."""
    states = {0}
    bits = left_mask
    while bits:
        low = bits & -bits
        u = low.bit_length() - 1
        options = rows[u] & right_mask
        added: set[int] = set()
        for used in states:
            free = options & ~used
            while free:
                edge = free & -free
                added.add(used | edge)
                free ^= edge
        states |= added
        bits ^= low
    return max(mask.bit_count() for mask in states)


def exhaustive_hall(rows: list[int], left_mask: int, right_mask: int) -> tuple[int, int]:
    """Maximum |S|-|Gamma(S)|, with adjacency unions built by subset DP."""
    vertices = [i for i in range(len(rows)) if (left_mask >> i) & 1]
    unions = [0] * (1 << len(vertices))
    maximum = 0
    for mask in range(1, 1 << len(vertices)):
        low = mask & -mask
        k = low.bit_length() - 1
        unions[mask] = unions[mask ^ low] | (rows[vertices[k]] & right_mask)
        maximum = max(maximum, mask.bit_count() - unions[mask].bit_count())
    return maximum, len(unions)


def derive_quotient(rows: list[int]) -> tuple[list[int], list[range]]:
    parts: list[range] = []
    start = 0
    for size in PART_SIZES:
        parts.append(range(start, start + size))
        start += size
    need(start == 23, "part sizes do not sum to 23")
    quotient = [0] * 13
    for i, part in enumerate(parts):
        for u in part:
            for v in part:
                if u < v:
                    need((rows[u] >> v) & 1, "internal part is not increasing-transitive")
        for j in range(i + 1, 13):
            other = parts[j]
            orientations = {bool((rows[u] >> v) & 1) for u in part for v in other}
            need(len(orientations) == 1, "external pair is not homogeneous")
            if orientations.pop():
                quotient[i] |= 1 << j
            else:
                quotient[j] |= 1 << i
    for i in range(13):
        for j in range(i):
            need(bool((quotient[i] >> j) & 1) ^ bool((quotient[j] >> i) & 1),
                 "derived quotient is not a tournament")
    return quotient, parts


def quotient_target(quotient: list[int], root: int, source_mask: int) -> int:
    reached = 0
    bits = source_mask
    while bits:
        low = bits & -bits
        reached |= quotient[low.bit_length() - 1]
        bits ^= low
    in_mask = ((1 << 13) - 1) & ~quotient[root] & ~(1 << root)
    return reached & in_mask


def coefficient(source_mask: int, target_mask: int) -> tuple[int, int, int]:
    return tuple(
        sum(((source_mask >> j) & 1) - ((target_mask >> j) & 1)
            for j, part_type in enumerate(PART_TYPES) if part_type == kind)
        for kind in range(3)
    )


def nondominated(forms: set[tuple[int, int, int]]) -> tuple[tuple[int, int, int], ...]:
    keep = [form for form in forms if not any(
        form != other and all(x <= y for x, y in zip(form, other))
        for other in forms)]
    return tuple(sorted(keep))


def selected_matrix_and_symbolics(quotient: list[int]) -> tuple[list[list[int]], int, str]:
    matrix: list[list[int]] = []
    all_maxima = []
    nonempty_count = 0
    for root in range(13):
        selected = sum(1 << j for j in SOURCES[root])
        need(selected & ~quotient[root] == 0, "selected source is not an out-set")
        target = quotient_target(quotient, root, selected)
        expected_target = sum(1 << j for j in TARGET_PARTS[root])
        need(target == expected_target, "selected quotient target mismatch")
        row = [((selected >> j) & 1) - ((target >> j) & 1) for j in range(13)]
        need(sum(x * y for x, y in zip(row, BASE_WEIGHTS)) == 1,
             "selected Hall deficiency is not one")
        matrix.append(row)

        outs = [j for j in range(13) if (quotient[root] >> j) & 1]
        forms: set[tuple[int, int, int]] = set()
        for local_mask in range(1 << len(outs)):
            source = sum(1 << outs[k] for k in range(len(outs)) if (local_mask >> k) & 1)
            forms.add(coefficient(source, quotient_target(quotient, root, source)))
        nonempty_count += (1 << len(outs)) - 1
        maximum_forms = nondominated(forms)
        need(maximum_forms == EXPECTED_MAX_FORMS[root], "symbolic maximum table mismatch")
        all_maxima.append(maximum_forms)
    encoded = json.dumps(all_maxima, separators=(",", ":")).encode("ascii")
    return matrix, nonempty_count, sha256(encoded).hexdigest()


def determinant_bareiss(matrix: list[list[int]]) -> int:
    a = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(len(a) - 1):
        pivot_row = next((i for i in range(k, len(a)) if a[i][k]), None)
        need(pivot_row is not None, "selected matrix is singular")
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                need(remainder == 0, "Bareiss division was not exact")
                a[i][j] = quotient
        previous = pivot
    return sign * a[-1][-1]


def verify_dual(matrix: list[list[int]]) -> None:
    need(sum(DUAL) == 920, "dual numerator sum mismatch")
    need(all(sum(DUAL[i] * matrix[i][j] for i in range(13)) == 40
             for j in range(13)), "dual identity mismatch")
    need(determinant_bareiss(matrix) == 40, "selected determinant mismatch")
    need(all(sum(row[j] * BASE_WEIGHTS[j] for j in range(13)) == 1
             for row in matrix), "base weights do not solve M w = 1")
    need(sum(BASE_WEIGHTS) == 23, "base weight total mismatch")


def enumerate_small_weights(matrix: list[list[int]]) -> tuple[int, list[list[int]]]:
    """Check every positive 13-composition of total at most 23."""
    checked = 0
    feasible: list[list[int]] = []
    sparse_rows = [[(j, value) for j, value in enumerate(row) if value] for row in matrix]
    for total in range(13, 24):
        for cuts in combinations(range(1, total), 12):
            marks = (0,) + cuts + (total,)
            weights = [marks[i + 1] - marks[i] for i in range(13)]
            checked += 1
            if all(sum(value * weights[j] for j, value in row) >= 1
                   for row in sparse_rows):
                feasible.append(weights)
    need(feasible == [list(BASE_WEIGHTS)], "selected cone has another small solution")
    return checked, feasible


def main() -> None:
    rows, literal = parse_literal()
    profile = []
    hall_subsets = 0
    for root in range(23):
        left = rows[root]
        right = exact_second(rows, root)
        matching = matching_by_state_dp(rows, left, right)
        deficiency, count = exhaustive_hall(rows, left, right)
        need(deficiency == left.bit_count() - matching and deficiency > 0,
             "matching/Hall equality or no-strong claim failed")
        profile.append([left.bit_count(), right.bit_count(), matching, deficiency])
        hall_subsets += count
    quotient, _ = derive_quotient(rows)
    matrix, symbolic_subsets, formula_hash = selected_matrix_and_symbolics(quotient)
    verify_dual(matrix)
    compositions, feasible = enumerate_small_weights(matrix)
    result = {
        "status": "REVIEW CHECK PASSED",
        "literal_order": 23,
        "literal_sha256": sha256(literal).hexdigest(),
        "literal_hall_subsets": hall_subsets,
        "literal_profile": profile,
        "strong_vertices": [],
        "quotient_parts": 13,
        "selected_hall_witnesses": 13,
        "symbolic_nonempty_subsets": symbolic_subsets,
        "symbolic_maxima_sha256": formula_hash,
        "selected_matrix_determinant": determinant_bareiss(matrix),
        "dual_numerator_sum": sum(DUAL),
        "selected_cone_minimum": sum(BASE_WEIGHTS),
        "positive_compositions_checked": compositions,
        "feasible_at_or_below_23": feasible,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
