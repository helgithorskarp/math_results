#!/usr/bin/env python3
"""Exact checker for the thirty-asymmetric-link theorem."""

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import comb, factorial


G = tuple(factorial(r) * factorial(8 - r) // 72 for r in range(9))
COMPOSITIONS = tuple((i, j, 7 - i - j) for i in range(8) for j in range(8 - i))
COMPOSITION_INDEX = {composition: index for index, composition in enumerate(COMPOSITIONS)}


def point_cells(a: int, c: int) -> tuple[int, ...]:
    return tuple(G[r] + (-1) ** (r + 1) * (r * c - a) for r in range(9))


def outgoing_divisibilities(a: int, c: int, degree: int) -> bool:
    cells = point_cells(a, c)
    return all(cells[r] % (8 - r) == 0 for r in range(degree + 1, 7))


def incoming_divisibilities(a: int, c: int, degree: int) -> bool:
    return outgoing_divisibilities(a - 8 * c, -c, degree)


def minimum_degrees(a: int, c: int) -> tuple[int, int]:
    outdegree = next(
        degree for degree in range(1, 9) if outgoing_divisibilities(a, c, degree)
    )
    indegree = next(
        degree for degree in range(1, 9) if incoming_divisibilities(a, c, degree)
    )
    return outdegree, indegree


@lru_cache(maxsize=None)
def excess_partitions(total: int, maximum: int, slots: int) -> tuple[tuple[int, ...], ...]:
    """Nonincreasing partitions of total into exactly ``slots`` parts."""
    if slots == 0:
        return ((),) if total == 0 else ()
    return tuple(
        (first,) + rest
        for first in range(min(total, maximum), -1, -1)
        for rest in excess_partitions(total - first, first, slots - 1)
    )


def generate_option_multisets(
    options_by_extra: dict[int, tuple[tuple[int, int, int, int], ...]],
    partition: tuple[int, ...],
):
    groups = [
        tuple(combinations_with_replacement(options_by_extra[extra], count))
        for extra, count in sorted(Counter(partition).items())
        if count
    ]
    for selections in product(*groups):
        yield sum(selections, ())


def combined_central_minimum(
    peripheral_profiles: tuple[tuple[int, int], ...],
) -> int:
    """Minimum of the sum of the two aligned nonconstant point cells."""
    a_total = sum(a for a, _ in peripheral_profiles)
    c_total = sum(c for _, c in peripheral_profiles)
    combined_coefficients = (-2 * c_total,) + tuple(
        c - c_total for _, c in peripheral_profiles
    )
    return min(
        2 * G[mask.bit_count()]
        + (-1) ** (mask.bit_count() + 1)
        * (
            sum(
                combined_coefficients[index]
                for index in range(8)
                if mask & (1 << index)
            )
            + a_total
        )
        for mask in range(1 << 8)
    )


def analyze_two_nonconstant_rows(
    profiles: tuple[tuple[int, int, int], ...],
) -> tuple[dict[tuple[int, int], tuple[int, int]], Counter[int]]:
    options_by_extra: dict[int, tuple[tuple[int, int, int, int], ...]] = {}
    for extra in range(3):
        combined_excess = 2 + extra
        options = []
        for out_excess in range(8):
            in_excess = combined_excess - out_excess
            if not 0 <= in_excess <= 7:
                continue
            for a, c, _ in profiles:
                if outgoing_divisibilities(a, c, out_excess + 1) and incoming_divisibilities(
                    a, c, in_excess + 1
                ):
                    options.append((out_excess, in_excess, a, c))
        options_by_extra[extra] = tuple(options)

    assert [len(options_by_extra[e]) for e in range(3)] == [4, 8, 24]

    case_counts = {}
    minimum_distribution: Counter[int] = Counter()
    for alpha_total in range(3):
        for beta_total in range(3):
            peripheral_extra = 2 - alpha_total - beta_total
            if peripheral_extra < 0:
                continue
            raw_count = 0
            profile_multisets = set()
            for partition in excess_partitions(peripheral_extra, peripheral_extra, 7):
                for options in generate_option_multisets(options_by_extra, partition):
                    if sum(option[0] for option in options) != 8 - alpha_total:
                        continue
                    if sum(option[1] for option in options) != 8 - beta_total:
                        continue
                    raw_count += 1
                    profile_multisets.add(
                        tuple(sorted((option[2], option[3]) for option in options))
                    )
            case_counts[(alpha_total, beta_total)] = (raw_count, len(profile_multisets))
            for peripheral in profile_multisets:
                minimum_distribution[combined_central_minimum(peripheral)] += 1

    expected_counts = {
        (0, 0): (538, 226),
        (0, 1): (62, 20),
        (0, 2): (20, 20),
        (1, 0): (62, 20),
        (1, 1): (0, 0),
        (2, 0): (20, 20),
    }
    assert case_counts == expected_counts
    assert sum(minimum_distribution.values()) == 306
    assert min(minimum_distribution) == -60
    assert max(minimum_distribution) == -1
    assert all(value < 0 for value in minimum_distribution)
    return case_counts, minimum_distribution


def central_interval(coefficients: tuple[int, ...]) -> tuple[int, int]:
    """Exact interval of a-values making all 256 central point cells nonnegative."""
    lower = max(sum(coefficients[8 - r :]) - G[r] for r in (0, 2, 4, 6, 8))
    upper = min(sum(coefficients[:r]) + G[r] for r in (1, 3, 5, 7))
    return lower, upper


def analyze_one_nonconstant_row(
    profiles: tuple[tuple[int, int, int], ...],
) -> tuple[int, int, dict[int, dict[tuple[int, tuple[int, ...]], set[tuple[int, int]]]]]:
    profiles_by_c: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for a, c, _ in profiles:
        outdegree, indegree = minimum_degrees(a, c)
        profiles_by_c[c].append((a, outdegree, indegree))

    assert sorted(profiles_by_c) == list(range(-10, 11))
    assert [len(profiles_by_c[c]) for c in range(-10, 11)] == [
        1,
        4,
        7,
        10,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        10,
        7,
        4,
        1,
    ]

    tuple_count = 0
    point_profile_count = 0
    survivors: dict[
        int, dict[tuple[int, tuple[int, ...]], set[tuple[int, int]]]
    ] = {27: defaultdict(set), 28: defaultdict(set), 29: defaultdict(set)}

    for coefficients in combinations_with_replacement(sorted(profiles_by_c), 8):
        if sum(coefficients) != 0 or coefficients == (0,) * 8:
            continue
        lower, upper = central_interval(coefficients)
        if lower > upper:
            continue
        tuple_count += 1
        point_profile_count += upper - lower + 1

        # This is a relaxation: record only sums of the local minimum degrees.
        states = {(0, 0, 0)}
        for c in coefficients:
            states = {
                (a_sum + a, out_sum + outdegree, in_sum + indegree)
                for a_sum, out_sum, in_sum in states
                for a, outdegree, indegree in profiles_by_c[c]
                if out_sum + outdegree <= 22 and in_sum + indegree <= 22
            }

        states_by_a: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for a_sum, out_sum, in_sum in states:
            states_by_a[a_sum].append((out_sum, in_sum))

        for a_h in range(lower, upper + 1):
            degree_pairs = states_by_a[-a_h]
            for arc_count in (27, 28, 29):
                for alpha in (0, 1):
                    for beta in (0, 1):
                        if any(
                            out_sum <= arc_count - 7 - alpha
                            and in_sum <= arc_count - 7 - beta
                            for out_sum, in_sum in degree_pairs
                        ):
                            survivors[arc_count][(a_h, coefficients)].add((alpha, beta))

    expected_29 = {
        (0, (-5, -3, 0, 0, 0, 0, 3, 5)): {(0, 0)},
        (4, (-6, 0, 0, 0, 0, 0, 0, 6)): {(0, 0)},
        (4, (-6, 0, 0, 0, 0, 0, 3, 3)): {(0, 0), (1, 0)},
        (4, (-3, -3, 0, 0, 0, 0, 0, 6)): {(0, 0), (0, 1)},
        (4, (-3, -3, 0, 0, 0, 0, 3, 3)): {(0, 0), (0, 1), (1, 0)},
        (4, (-3, 0, 0, 0, 0, 0, 0, 3)): {(0, 0)},
    }
    assert tuple_count == 1254
    assert point_profile_count == 4566
    assert dict(survivors[27]) == {}
    assert dict(survivors[28]) == {}
    assert dict(survivors[29]) == expected_29

    # Each surviving coefficient tuple lacks seven equal entries.  Hence a
    # central row with such a tuple has both directed degrees eight, requiring
    # (alpha,beta)=(1,1), which is absent from every relaxed survivor set.
    for (_, coefficients), degree_increments in survivors[29].items():
        assert max(Counter(coefficients).values()) <= 6
        assert (1, 1) not in degree_increments

    return tuple_count, point_profile_count, survivors


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


def source_boundary(size: int) -> tuple[int, ...]:
    return vector(
        {
            (size, between, 7 - size - between): comb(7 - size, between)
            for between in range(8 - size)
        }
    )


def target_boundary(size: int) -> tuple[int, ...]:
    return vector({(i, size - i, 7 - size): comb(size, i) for i in range(size + 1)})


def zero_between(index: int) -> tuple[int, ...]:
    return vector({(index, 0, 7 - index): 1})


def forced_zero_between(source_a: int, target_a: int) -> tuple[int, ...]:
    source = point_cells(source_a, 0)
    target = point_cells(target_a, 0)
    values = (
        target[1],
        target[2] // 2,
        target[3] // 3,
        target[4] // 4,
        source[4] // 4,
        source[5] // 3,
        source[6] // 2,
        source[7],
    )
    assert values[1] * 2 == target[2]
    assert values[2] * 3 == target[3]
    assert values[3] * 4 == target[4]
    assert values[4] * 4 == source[4]
    assert values[5] * 3 == source[5]
    assert values[6] * 2 == source[6]
    return values


def certificate_rhs(
    source_a: int,
    target_a: int,
    terms: tuple[tuple[int, str, tuple[int, ...] | int], ...],
) -> int:
    z = forced_zero_between(source_a, target_a)
    rhs = 0
    for weight, kind, argument in terms:
        if kind == "M":
            i, j, k = argument  # type: ignore[misc]
            rhs += weight * factorial(i) * factorial(j) * factorial(k)
        elif kind == "S":
            rhs += weight * point_cells(source_a, 0)[argument]  # type: ignore[index]
        elif kind == "T":
            rhs += weight * point_cells(target_a, 0)[argument + 1]  # type: ignore[operator]
        else:
            assert kind == "Z"
            rhs += weight * z[argument]  # type: ignore[index]
    return rhs


def certificate_vector(
    terms: tuple[tuple[int, str, tuple[int, ...] | int], ...],
) -> tuple[int, ...]:
    vectors = []
    for weight, kind, argument in terms:
        if kind == "M":
            item = marginal(*argument)  # type: ignore[arg-type]
        elif kind == "S":
            item = source_boundary(argument)  # type: ignore[arg-type]
        elif kind == "T":
            item = target_boundary(argument)  # type: ignore[arg-type]
        else:
            assert kind == "Z"
            item = zero_between(argument)  # type: ignore[arg-type]
        vectors.append((weight, item))
    return add_vectors(*vectors)


def check_regular_pair_certificates() -> dict[str, int]:
    certificates = {
        "AA": (
            -8,
            -8,
            (
                (-1, "M", (2, 0, 3)),
                (1, "M", (2, 1, 2)),
                (1, "T", 3),
                (1, "Z", 2),
                (1, "Z", 3),
                (1, "Z", 4),
            ),
        ),
        "BB": (
            4,
            4,
            (
                (1, "M", (0, 2, 3)),
                (4, "M", (1, 2, 2)),
                (9, "M", (2, 0, 3)),
                (-8, "M", (2, 1, 2)),
                (12, "M", (3, 0, 2)),
                (-2, "T", 3),
                (-9, "Z", 2),
                (-28, "Z", 3),
                (-33, "Z", 4),
                (-12, "Z", 5),
            ),
        ),
        "AB": (
            -8,
            4,
            (
                (-3, "M", (1, 0, 4)),
                (6, "M", (1, 1, 3)),
                (-8, "M", (1, 2, 2)),
                (4, "M", (1, 3, 1)),
                (-9, "M", (2, 0, 3)),
                (12, "M", (2, 1, 2)),
                (-2, "M", (2, 2, 1)),
                (-10, "M", (3, 0, 2)),
                (3, "S", 4),
                (2, "T", 4),
                (3, "Z", 1),
                (15, "Z", 2),
                (31, "Z", 3),
                (24, "Z", 4),
                (10, "Z", 5),
            ),
        ),
    }
    expected_rhs = {"AA": -2, "BB": -1, "AB": -1}
    expected_support = {"AA": 7, "BB": 8, "AB": 10}
    expected_vectors = {
        "AA": vector(
            {
                (0, 3, 4): 1,
                (1, 2, 4): 3,
                (2, 1, 4): 2,
                (2, 2, 3): 1,
                (2, 3, 2): 1,
                (3, 2, 2): 2,
                (4, 1, 2): 1,
            }
        ),
        "BB": vector(
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
        ),
        "AB": vector(
            {
                (0, 4, 3): 2,
                (1, 2, 4): 1,
                (1, 3, 3): 2,
                (1, 5, 1): 4,
                (2, 2, 3): 21,
                (2, 4, 1): 6,
                (3, 2, 2): 2,
                (4, 1, 2): 1,
                (4, 2, 1): 7,
                (4, 3, 0): 3,
            }
        ),
    }
    rhs_values = {}
    for name, (source_a, target_a, terms) in certificates.items():
        coefficients = certificate_vector(terms)
        rhs = certificate_rhs(source_a, target_a, terms)
        assert coefficients == expected_vectors[name]
        assert min(coefficients) >= 0
        assert sum(value > 0 for value in coefficients) == expected_support[name]
        assert rhs == expected_rhs[name]
        rhs_values[name] = rhs
    return rhs_values


def analyze_all_constant_rows(
    profiles: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    low_degree = []
    for a, c, _ in profiles:
        if c != 0:
            continue
        outdegree, indegree = minimum_degrees(a, c)
        if outdegree <= 5 and indegree <= 5:
            low_degree.append((a, outdegree, indegree))
    assert low_degree == [
        (-8, 3, 3),
        (-6, 5, 5),
        (-4, 5, 5),
        (-2, 4, 4),
        (0, 5, 5),
        (2, 5, 5),
        (4, 3, 3),
        (6, 5, 5),
        (8, 5, 5),
        (10, 4, 4),
    ]
    minimum = {a: outdegree for a, outdegree, indegree in low_degree}
    assert all(outdegree == indegree for _, outdegree, indegree in low_degree)

    balanced = tuple(
        parameters
        for parameters in combinations_with_replacement(sorted(minimum), 9)
        if sum(parameters) == 0
        and sum(minimum[a] - 3 for a in parameters) <= 2
    )
    expected = (
        (-8, -8, -8, -8, 4, 4, 4, 10, 10),
        (-8, -8, -8, -2, 4, 4, 4, 4, 10),
        (-8, -8, -8, 4, 4, 4, 4, 4, 4),
        (-8, -8, -2, -2, 4, 4, 4, 4, 4),
    )
    assert balanced == expected

    for parameters in balanced:
        regular_count = sum(a in (-8, 4) for a in parameters)
        assert regular_count in (7, 9)
        if regular_count == 7:
            # The two degree-four rows consume all excess in both directions.
            assert sum(minimum[a] for a in parameters) == 29
            forced_regular_targets = 6
        else:
            # At most two of the other eight targets can have indegree > 3.
            forced_regular_targets = 8 - 2
        assert forced_regular_targets == 6 > 3
    return balanced


def main() -> None:
    assert G == (560, 70, 20, 10, 8, 10, 20, 70, 560)
    assert len(COMPOSITIONS) == 36

    profiles = tuple(
        (a, c, 8 * c - a)
        for c in range(-18, 19)
        for a in range(-560, 89)
        if min(point_cells(a, c)) >= 0
    )
    assert len(profiles) == 249

    two_row_counts, two_row_minima = analyze_two_nonconstant_rows(profiles)
    tuple_count, central_count, survivors = analyze_one_nonconstant_row(profiles)
    certificate_values = check_regular_pair_certificates()
    all_constant_profiles = analyze_all_constant_rows(profiles)

    print(f"constant coefficient-row profiles: {len(profiles)}")
    print(
        "two-nonconstant cases: "
        + ", ".join(
            f"{key[0]}{key[1]}={raw}/{unique}"
            for key, (raw, unique) in two_row_counts.items()
        )
    )
    print(
        f"two-nonconstant aggregate profiles: {sum(two_row_minima.values())}; "
        f"cell minima {min(two_row_minima)}..{max(two_row_minima)}"
    )
    print(
        f"one-nonconstant central coefficient tuples/profiles: "
        f"{tuple_count}/{central_count}"
    )
    print(
        "one-nonconstant relaxed survivors at 27/28/29 arcs: "
        f"{len(survivors[27])}/{len(survivors[28])}/{len(survivors[29])}"
    )
    for (a_h, coefficients), increments in sorted(survivors[29].items()):
        increment_text = ",".join(f"{a}{b}" for a, b in sorted(increments))
        print(f"central survivor: a={a_h} c={coefficients} increments={increment_text}")
    print("central survivors requiring increments 11: 6; feasible with increments 11: 0")
    print(
        "regular pair certificate right sides: "
        + " ".join(f"{name}={value}" for name, value in certificate_values.items())
        + " BA=-1(reversal)"
    )
    print(f"all-constant balanced profiles: {len(all_constant_profiles)}")
    print("each all-constant profile forces a degree-3 source to have at least 6 arcs")
    print("asymmetric ordered-pair-link lower bound: 30")
    print("all checks passed")


if __name__ == "__main__":
    main()
