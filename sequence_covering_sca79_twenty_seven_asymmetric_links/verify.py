#!/usr/bin/env python3
"""Exact checker for the twenty-seven-asymmetric-link theorem."""

from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import factorial


G = [factorial(r) * factorial(8 - r) // 72 for r in range(9)]
U = (1, -7, 21, -35, 35, -21, 7, -1, 0)
V = (0, 1, -7, 21, -35, 35, -21, 7, -1)


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


def central_cell_minimum(a: int, coefficients: tuple[int, ...]) -> int:
    assert len(coefficients) == 8
    minimum = 10**9
    for mask in range(1 << 8):
        size = mask.bit_count()
        subset_sum = sum(coefficients[i] for i in range(8) if mask & (1 << i))
        value = G[size] + (-1) ** (size + 1) * (subset_sum - a)
        minimum = min(minimum, value)
    return minimum


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


def analyze_arc_count(
    arc_count: int,
    options_by_extra: dict[int, tuple[tuple[int, int, int, int, int], ...]],
) -> tuple[tuple[int, int, int, int], int, int]:
    """Return aggregate stage counts, signature count, and best minimum cell."""
    s = arc_count - 9
    total_available_extra = 2 * s - 28
    aggregate = [0, 0, 0, 0]
    signatures: set[tuple[int, int, tuple[int, ...], int]] = set()

    for alpha in (0, 1):
        for beta in (0, 1):
            peripheral_extra = total_available_extra - alpha - beta
            if peripheral_extra < 0:
                continue
            target_out = s - 6 - alpha
            target_in = s - 6 - beta

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

    best_minimum = max(signature[3] for signature in signatures)
    return tuple(aggregate), len(signatures), best_minimum


def main() -> None:
    assert G == [560, 70, 20, 10, 8, 10, 20, 70, 560]

    profiles = tuple(
        (a, c, 8 * c - a)
        for c in range(-18, 19)
        for a in range(-560, 89)
        if min(point_cells(a, c)) >= 0
    )
    assert len(profiles) == 249

    # Extra is combined peripheral degree excess beyond its proved minimum 2.
    options_by_extra = {}
    for extra in range(7):
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

    assert [len(options_by_extra[extra]) for extra in range(7)] == [4, 8, 24, 40, 88, 164, 284]

    expected = {
        24: ((513, 105, 27, 0), 1, -21),
        25: ((18522, 2128, 537, 0), 21, -9),
        26: ((281306, 26136, 7163, 0), 48, -9),
    }
    results = {}
    for arc_count in (24, 25, 26):
        result = analyze_arc_count(arc_count, options_by_extra)
        assert result == expected[arc_count]
        results[arc_count] = result

    # At 27 arcs, the all-constant branch has c=0 and degrees exactly (3,3).
    exact_27_profiles = [
        profile
        for profile in profiles
        if profile[1] == 0
        and outgoing_divisibilities(profile[0], 0, 3)
        and incoming_divisibilities(profile[0], 0, 3)
    ]
    assert exact_27_profiles == [(-8, 0, 8), (4, 0, -4)]
    multiplicities = [
        negative_type_count
        for negative_type_count in range(10)
        if -8 * negative_type_count + 4 * (9 - negative_type_count) == 0
    ]
    assert multiplicities == [3]

    print(f"constant coefficient-row profiles: {len(profiles)}")
    print("local options by extra degree 0..6: " + " ".join(str(len(options_by_extra[e])) for e in range(7)))
    for arc_count in (24, 25, 26):
        stages, signature_count, best_minimum = results[arc_count]
        print(
            f"arcs {arc_count}: degree {stages[0]}, balanced {stages[1]}, "
            f"position {stages[2]}, point {stages[3]}, signatures {signature_count}, "
            f"best minimum {best_minimum}"
        )
    print("exact-27 constant profiles: (-8,0,8) and (4,0,-4)")
    print("exact-27 global multiplicities: 3 and 6")
    print("asymmetric ordered-pair-link lower bound: 27")
    print("all checks passed")


if __name__ == "__main__":
    main()
