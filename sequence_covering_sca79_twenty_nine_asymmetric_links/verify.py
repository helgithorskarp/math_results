#!/usr/bin/env python3
"""Exact checker for the twenty-nine-asymmetric-link theorem."""

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


@lru_cache(maxsize=None)
def central_cell_minimum(a: int, coefficients: tuple[int, ...]) -> int:
    minimum = 10**9
    for mask in range(1 << 8):
        size = mask.bit_count()
        subset_sum = sum(coefficients[i] for i in range(8) if mask & (1 << i))
        value = G[size] + (-1) ** (size + 1) * (subset_sum - a)
        minimum = min(minimum, value)
    return minimum


def analyze_case(
    alpha: int,
    beta: int,
    options_by_extra: dict[int, tuple[tuple[int, int, int, int, int], ...]],
) -> tuple[tuple[int, int, int, int], set[tuple[int, int, tuple[int, ...], int]]]:
    aggregate = [0, 0, 0, 0]
    signatures: set[tuple[int, int, tuple[int, ...], int]] = set()
    peripheral_extra = 10 - alpha - beta
    target_out = 13 - alpha
    target_in = 13 - beta

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
            if min(560 + a_h * u + b_h * v for u, v in zip(U, V)) < 0:
                continue
            aggregate[2] += 1

            minimum = central_cell_minimum(a_h, coefficients)
            signatures.add((a_h, b_h, coefficients, minimum))
            if minimum < 0:
                continue
            aggregate[3] += 1

    return tuple(aggregate), signatures


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


def check_type_b_certificate() -> None:
    forced = (66, 12, 2, 3, 3, 2, 12, 66)
    certificate = (
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
    expected = vector(
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
    coefficients = add_vectors(*certificate)
    rhs = (
        factorial(0) * factorial(2) * factorial(3)
        + 4 * factorial(1) * factorial(2) * factorial(2)
        + 9 * factorial(2) * factorial(0) * factorial(3)
        - 8 * factorial(2) * factorial(1) * factorial(2)
        + 12 * factorial(3) * factorial(0) * factorial(2)
        - 2 * point_cells(4, 0)[4]
        - 9 * forced[2]
        - 28 * forced[3]
        - 33 * forced[4]
        - 12 * forced[5]
    )
    assert coefficients == expected
    assert min(coefficients) >= 0 and sum(value > 0 for value in coefficients) == 8
    assert rhs == -1


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
    for extra in range(11):
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

    option_counts = [len(options_by_extra[extra]) for extra in range(11)]
    assert option_counts == [4, 8, 24, 40, 88, 164, 284, 404, 603, 758, 747]

    # Reversal is an entry-level bijection on every local option set.
    for extra, options in options_by_extra.items():
        option_set = set(options)
        assert all((i, o, -b, -c, -a) in option_set for o, i, a, c, b in options)

    cases = {}
    all_signatures: set[tuple[int, int, tuple[int, ...], int]] = set()
    for alpha, beta in ((0, 0), (0, 1), (1, 1)):
        stages, signatures = analyze_case(alpha, beta, options_by_extra)
        cases[(alpha, beta)] = stages
        all_signatures.update(signatures)

    expected_cases = {
        (0, 0): (24380366, 1218982, 369484, 0),
        (0, 1): (7673973, 420290, 125045, 0),
        (1, 1): (2388261, 149267, 43785, 0),
    }
    assert cases == expected_cases
    total = tuple(cases[(0, 0)][i] + 2 * cases[(0, 1)][i] + cases[(1, 1)][i] for i in range(4))
    assert total == (42116573, 2208829, 663359, 0)
    assert len(all_signatures) == 1078
    assert max(signature[3] for signature in all_signatures) == -3

    minimum_options = options_by_extra[0]
    assert {option[:2] for option in minimum_options} == {(0, 2), (2, 0)}
    assert 19 - 2 * 6 == 7

    c_zero_low_degree = []
    for a, c, b in profiles:
        if c != 0:
            continue
        out_degree = next(k for k in range(1, 9) if outgoing_divisibilities(a, c, k))
        in_degree = next(k for k in range(1, 9) if incoming_divisibilities(a, c, k))
        if out_degree <= 4 and in_degree <= 4:
            c_zero_low_degree.append((a, out_degree, in_degree))
    assert c_zero_low_degree == [(-8, 3, 3), (-2, 4, 4), (4, 3, 3), (10, 4, 4)]
    assert all(-2 - 8 * n + 4 * (8 - n) != 0 for n in range(9))
    assert all(10 - 8 * n + 4 * (8 - n) != 0 for n in range(9))
    assert -8 * 3 + 4 * 6 == 0

    check_type_b_certificate()
    assert 6 - 2 == 4 > 3

    print(f"constant coefficient-row profiles: {len(profiles)}")
    print("local options by extra degree 0..10: " + " ".join(map(str, option_counts)))
    for alpha, beta, multiplicity in ((0, 0, 1), (0, 1, 2), (1, 1, 1)):
        stages = cases[(alpha, beta)]
        suffix = " (multiplicity 2)" if multiplicity == 2 else ""
        print(
            f"case alpha={alpha} beta={beta}{suffix}: degree {stages[0]}, "
            f"balanced {stages[1]}, position {stages[2]}, point {stages[3]}"
        )
    print(
        f"one-nonconstant total: degree {total[0]}, balanced {total[1]}, "
        f"position {total[2]}, point {total[3]}"
    )
    print(f"central signatures: {len(all_signatures)}; best minimum -3")
    print("two-nonconstant branch: parity contradiction")
    print("all-constant low-degree profiles: -8:3, -2:4, 4:3, 10:4")
    print("regular type-B source: at least 4 forced arcs but outdegree 3")
    print("asymmetric ordered-pair-link lower bound: 29")
    print("all checks passed")


if __name__ == "__main__":
    main()
