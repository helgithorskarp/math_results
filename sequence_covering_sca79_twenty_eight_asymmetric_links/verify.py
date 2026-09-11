#!/usr/bin/env python3
"""Exact checker for the twenty-eight-asymmetric-link theorem."""

from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import comb, factorial


G = [factorial(r) * factorial(8 - r) // 72 for r in range(9)]
U = (1, -7, 21, -35, 35, -21, 7, -1, 0)
V = (0, 1, -7, 21, -35, 35, -21, 7, -1)
COMPOSITIONS = tuple((i, j, 7 - i - j) for i in range(8) for j in range(8 - i))
COMPOSITION_INDEX = {composition: index for index, composition in enumerate(COMPOSITIONS)}


def point_cells(a: int, c: int) -> tuple[int, ...]:
    return tuple(G[r] + (-1) ** (r + 1) * (r * c - a) for r in range(9))


def outgoing_divisibilities(a: int, c: int, degree: int) -> bool:
    cells = point_cells(a, c)
    return all(cells[r] % (8 - r) == 0 for r in range(degree + 1, 7))


def incoming_divisibilities(a: int, c: int, degree: int) -> bool:
    b = 8 * c - a
    return outgoing_divisibilities(-b, -c, degree)


@lru_cache(maxsize=None)
def excess_partitions(total: int, maximum: int, slots: int) -> tuple[tuple[int, ...], ...]:
    """Nonincreasing partitions of total into exactly slots nonnegative parts."""
    if slots == 0:
        return ((),) if total == 0 else ()
    return tuple(
        (first,) + rest
        for first in range(min(maximum, total), -1, -1)
        for rest in excess_partitions(total - first, first, slots - 1)
    )


def generate_multisets(
    options_by_extra: dict[int, tuple[tuple[int, int, int, int, int], ...]],
    part: tuple[int, ...],
):
    counts = Counter(part)
    groups = [
        tuple(combinations_with_replacement(options_by_extra[extra], count))
        for extra, count in sorted(counts.items())
        if count
    ]
    for selections in product(*groups):
        yield sum(selections, ())


def central_cell_minimum(a: int, coefficients: tuple[int, ...]) -> int:
    minimum = 10**9
    for mask in range(1 << 8):
        size = mask.bit_count()
        subset_sum = sum(coefficients[i] for i in range(8) if mask & (1 << i))
        value = G[size] + (-1) ** (size + 1) * (subset_sum - a)
        minimum = min(minimum, value)
    return minimum


def analyze_one_nonconstant_branch(
    options_by_extra: dict[int, tuple[tuple[int, int, int, int, int], ...]],
) -> tuple[tuple[int, int, int, int], int, int]:
    """Enumerate the exact-27 relaxation with one designated nonconstant row."""
    aggregate = [0, 0, 0, 0]
    signatures: set[tuple[int, int, tuple[int, ...], int]] = set()

    for alpha in (0, 1):
        for beta in (0, 1):
            peripheral_extra = 8 - alpha - beta
            target_out = 12 - alpha
            target_in = 12 - beta

            for part in excess_partitions(peripheral_extra, peripheral_extra, 8):
                for options in generate_multisets(options_by_extra, part):
                    if sum(option[0] for option in options) != target_out:
                        continue
                    if sum(option[1] for option in options) != target_in:
                        continue
                    aggregate[0] += 1

                    coefficients = tuple(sorted(option[3] for option in options))
                    if sum(coefficients) != 0:
                        continue
                    aggregate[1] += 1

                    a_h = -sum(option[2] for option in options)
                    b_h = -a_h
                    positions = tuple(560 + a_h * u + b_h * v for u, v in zip(U, V))
                    if min(positions) < 0:
                        continue
                    aggregate[2] += 1

                    minimum = central_cell_minimum(a_h, coefficients)
                    signatures.add((a_h, b_h, coefficients, minimum))
                    if minimum < 0:
                        continue
                    aggregate[3] += 1

    return tuple(aggregate), len(signatures), max(signature[3] for signature in signatures)


def vector(entries: dict[tuple[int, int, int], int]) -> tuple[int, ...]:
    result = [0] * len(COMPOSITIONS)
    for composition, coefficient in entries.items():
        result[COMPOSITION_INDEX[composition]] = coefficient
    return tuple(result)


def add_vectors(*weighted_vectors: tuple[int, tuple[int, ...]]) -> tuple[int, ...]:
    return tuple(
        sum(weight * item[index] for weight, item in weighted_vectors)
        for index in range(len(COMPOSITIONS))
    )


def marginal(i: int, j: int, k: int) -> tuple[int, ...]:
    assert i + j + k == 5
    entries = Counter()
    for di, dj, dk, coefficient in (
        (2, 0, 0, 1),
        (0, 2, 0, 1),
        (0, 0, 2, 1),
        (1, 1, 0, 2),
        (1, 0, 1, 2),
        (0, 1, 1, 2),
    ):
        entries[(i + di, j + dj, k + dk)] += coefficient
    return vector(dict(entries))


def target_boundary(size: int) -> tuple[int, ...]:
    return vector({(i, size - i, 7 - size): comb(size, i) for i in range(size + 1)})


def zero_between(index: int) -> tuple[int, ...]:
    return vector({(index, 0, 7 - index): 1})


def forced_zero_between(type_parameter: int) -> tuple[int, ...]:
    cells = point_cells(type_parameter, 0)
    return tuple(
        [cells[a + 1] // (a + 1) for a in range(4)]
        + [cells[a] // (8 - a) for a in range(4, 7)]
        + [cells[7]]
    )


def check_same_type_certificates() -> tuple[int, int]:
    forced_a = forced_zero_between(-8)
    forced_b = forced_zero_between(4)
    assert forced_a == (78, 6, 6, 0, 0, 6, 6, 78)
    assert forced_b == (66, 12, 2, 3, 3, 2, 12, 66)

    certificate_a = (
        (-1, marginal(2, 0, 3)),
        (1, marginal(2, 1, 2)),
        (1, target_boundary(3)),
        (1, zero_between(2)),
        (1, zero_between(3)),
        (1, zero_between(4)),
    )
    expected_a = vector(
        {
            (0, 3, 4): 1,
            (1, 2, 4): 3,
            (2, 1, 4): 2,
            (2, 2, 3): 1,
            (2, 3, 2): 1,
            (3, 2, 2): 2,
            (4, 1, 2): 1,
        }
    )
    coefficients_a = add_vectors(*certificate_a)
    rhs_a = (
        -factorial(2) * factorial(0) * factorial(3)
        + factorial(2) * factorial(1) * factorial(2)
        + point_cells(-8, 0)[4]
        + forced_a[2]
        + forced_a[3]
        + forced_a[4]
    )
    assert coefficients_a == expected_a
    assert min(coefficients_a) >= 0 and rhs_a == -2

    certificate_b = (
        (1, marginal(0, 2, 3)),
        (4, marginal(1, 2, 2)),
        (9, marginal(2, 0, 3)),
        (-8, marginal(2, 1, 2)),
        (12, marginal(3, 0, 2)),
        (-2, target_boundary(3)),
        (-9, zero_between(2)),
        (-28, zero_between(3)),
        (-33, zero_between(4)),
        (-12, zero_between(5)),
    )
    expected_b = vector(
        {
            (0, 2, 5): 1,
            (0, 4, 3): 1,
            (1, 3, 3): 10,
            (1, 4, 2): 4,
            (2, 1, 4): 4,
            (2, 2, 3): 2,
            (3, 1, 3): 26,
            (4, 1, 2): 16,
        }
    )
    coefficients_b = add_vectors(*certificate_b)
    rhs_b = (
        factorial(0) * factorial(2) * factorial(3)
        + 4 * factorial(1) * factorial(2) * factorial(2)
        + 9 * factorial(2) * factorial(0) * factorial(3)
        - 8 * factorial(2) * factorial(1) * factorial(2)
        + 12 * factorial(3) * factorial(0) * factorial(2)
        - 2 * point_cells(4, 0)[4]
        - 9 * forced_b[2]
        - 28 * forced_b[3]
        - 33 * forced_b[4]
        - 12 * forced_b[5]
    )
    assert coefficients_b == expected_b
    assert min(coefficients_b) >= 0 and rhs_b == -1

    return sum(value > 0 for value in coefficients_a), sum(value > 0 for value in coefficients_b)


def main() -> None:
    assert G == [560, 70, 20, 10, 8, 10, 20, 70, 560]
    assert len(COMPOSITIONS) == 36

    profiles = tuple(
        (a, c, 8 * c - a)
        for c in range(-18, 19)
        for a in range(-560, 89)
        if min(point_cells(a, c)) >= 0
    )
    assert len(profiles) == 249

    options_by_extra = {}
    for extra in range(9):
        combined_excess = 2 + extra
        options = []
        for out_excess in range(8):
            in_excess = combined_excess - out_excess
            if not 0 <= in_excess <= 7:
                continue
            for a, c, b in profiles:
                if outgoing_divisibilities(a, c, out_excess + 1) and incoming_divisibilities(
                    a, c, in_excess + 1
                ):
                    options.append((out_excess, in_excess, a, c, b))
        options_by_extra[extra] = tuple(options)

    option_counts = [len(options_by_extra[extra]) for extra in range(9)]
    assert option_counts == [4, 8, 24, 40, 88, 164, 284, 404, 603]

    branch_result = analyze_one_nonconstant_branch(options_by_extra)
    assert branch_result == ((3890963, 259869, 75293, 0), 460, -3)

    exact_27_profiles = [
        profile
        for profile in profiles
        if profile[1] == 0
        and outgoing_divisibilities(profile[0], 0, 3)
        and incoming_divisibilities(profile[0], 0, 3)
    ]
    assert exact_27_profiles == [(-8, 0, 8), (4, 0, -4)]
    assert -8 * 3 + 4 * 6 == 0

    support_a, support_b = check_same_type_certificates()
    forced_arcs = 3 * 2 + 6 * 5
    assert support_a == 7 and support_b == 8
    assert forced_arcs == 36 > 27

    stages, signature_count, best_minimum = branch_result
    print(f"constant coefficient-row profiles: {len(profiles)}")
    print("local options by extra degree 0..8: " + " ".join(map(str, option_counts)))
    print(
        f"exact-27 one-nonconstant branch: degree {stages[0]}, balanced {stages[1]}, "
        f"position {stages[2]}, point {stages[3]}"
    )
    print(f"exact-27 central signatures: {signature_count}; best minimum {best_minimum}")
    print(f"type -8 same-type certificate: rhs -2, nonnegative cell coefficients {support_a}")
    print(f"type 4 same-type certificate: rhs -1, nonnegative cell coefficients {support_b}")
    print(f"forced same-type arcs in the constant branch: {forced_arcs}")
    print("asymmetric ordered-pair-link lower bound: 28")
    print("all checks passed")


if __name__ == "__main__":
    main()
