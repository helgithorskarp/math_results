#!/usr/bin/env python3
"""Exact verifier for the Albertson r=27 four-deletion moment barrier."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


N = 53
M = 713
K = 27
T = 4
MIN_SUPPORT = 18
MAX_EXCESS = 24
TOTAL_EXCESS = 48
Q_MIN = 575
Q_MAX = 615
TARGET = 6084

LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
    (Fraction(6), Fraction(266, 9)),
)


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def base_bound(n: int, m: int) -> int:
    return max(
        [0]
        + [ceil_fraction(a * m - b * (n - 2)) for a, b in LINEAR_BOUNDS]
    )


def monotone_hull(values: list[int]) -> list[tuple[int, int]]:
    hull: list[tuple[int, int]] = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            if Fraction(y1 - y0, x1 - x0) >= Fraction(y2 - y1, x2 - x1):
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def pooled_hull(values: list[int]) -> list[tuple[int, int]]:
    blocks: list[list[int]] = []
    for i in range(len(values) - 1):
        blocks.append([1, values[i + 1] - values[i]])
        while len(blocks) >= 2:
            r0, z0 = blocks[-2]
            r1, z1 = blocks[-1]
            if Fraction(z0, r0) < Fraction(z1, r1):
                break
            blocks[-2:] = [[r0 + r1, z0 + z1]]
    hull = [(0, values[0])]
    x, y = hull[0]
    for run, rise in blocks:
        x += run
        y += rise
        hull.append((x, y))
    return hull


def hull_value(hull: list[tuple[int, int]], x: Fraction) -> Fraction:
    positions = [point[0] for point in hull]
    i = bisect_right(positions, x) - 1
    if i == len(hull) - 1 or x == hull[i][0]:
        return Fraction(hull[i][1])
    x0, y0 = hull[i]
    x1, y1 = hull[i + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def recursive_closure(max_n: int):
    bounds: dict[int, list[int]] = {}
    hulls: dict[int, list[tuple[int, int]]] = {}
    digest = sha256()
    for n in range(4, max_n + 1):
        values = []
        for m in range(comb(n, 2) + 1):
            value = base_bound(n, m)
            for s in range(4, n):
                mean = Fraction(m * s * (s - 1), n * (n - 1))
                local_sum = comb(n, s) * hull_value(hulls[s], mean)
                sampled = ceil_fraction(
                    Fraction(local_sum, comb(n - 4, s - 4))
                )
                value = max(value, sampled)
            values.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull_a = monotone_hull(values)
        hull_b = pooled_hull(values)
        assert hull_a == hull_b
        bounds[n] = values
        hulls[n] = hull_a
    return bounds, digest.hexdigest()


def feasible_degree_square_excesses() -> tuple[int, ...]:
    """Enumerate B=sum C(x,2) over positive excess multisets."""
    states: dict[tuple[int, int], set[int]] = {(0, 0): {0}}
    for used in range(TOTAL_EXCESS):
        for total in range(TOTAL_EXCESS + 1):
            values = states.get((used, total))
            if not values:
                continue
            for x in range(1, min(MAX_EXCESS, TOTAL_EXCESS - total) + 1):
                destination = states.setdefault((used + 1, total + x), set())
                destination.update(value + comb(x, 2) for value in values)
    feasible = set()
    for support in range(MIN_SUPPORT, TOTAL_EXCESS + 1):
        feasible.update(states.get((support, TOTAL_EXCESS), set()))
    return tuple(sorted(feasible))


S0 = comb(N, T)
S1 = M * comb(N - 2, T)
CROSSING_MULTIPLICITY = comb(N - 4, T)


def moment_sums(B: int) -> tuple[int, int, int]:
    adjacent_pairs = 53 * comb(26, 2) + 26 * TOTAL_EXCESS + B
    assert adjacent_pairs == 18473 + B
    S2 = (
        adjacent_pairs * comb(N - 3, T)
        + (comb(M, 2) - adjacent_pairs) * comb(N - 4, T)
    )
    return S0, S1, S2


def solve_three_supports(qs: tuple[int, int, int], B: int) -> tuple[Fraction, ...]:
    s0, s1, s2 = moment_sums(B)
    matrix = [
        [Fraction(1), Fraction(1), Fraction(1), Fraction(s0)],
        [Fraction(q) for q in qs] + [Fraction(s1)],
        [Fraction(comb(q, 2)) for q in qs] + [Fraction(s2)],
    ]
    for column in range(3):
        pivot = next(row for row in range(column, 3) if matrix[row][column])
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [entry / scale for entry in matrix[column]]
        for row in range(3):
            if row == column:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                matrix[row][j] - scale * matrix[column][j] for j in range(4)
            ]
    return tuple(matrix[i][3] for i in range(3))


def interpolate_quadratic(qs: tuple[int, int, int], local: list[int]):
    x, y, z = qs
    first = Fraction(local[y] - local[x], y - x)
    second = Fraction(local[z] - local[y], z - y)
    c = Fraction(second - first, z - x)
    b = first - c * (x + y)
    a = Fraction(local[x]) - b * x - c * x * x
    return a, b, c


def sharp_moment_relaxations(local: list[int], feasible_B: tuple[int, ...]):
    totals = {}
    contact_switches = []
    last_contacts = None
    for B in feasible_B:
        contacts = (608, 610, 615) if B <= 11 else (575, 608, 615)
        if contacts != last_contacts:
            contact_switches.append((B, contacts))
            last_contacts = contacts
        weights = solve_three_supports(contacts, B)
        assert all(weight >= 0 for weight in weights)
        primal = sum(weight * local[q] for weight, q in zip(weights, contacts))

        a, b, c = interpolate_quadratic(contacts, local)
        for q in range(Q_MIN, Q_MAX + 1):
            assert a + b * q + c * q * q <= local[q]
        s0, s1, s2 = moment_sums(B)
        sum_q_squared = 2 * s2 + s1
        dual = a * s0 + b * s1 + c * sum_q_squared
        assert primal == dual
        totals[B] = primal
    return totals, tuple(contact_switches)


def integral_obstruction(local: list[int]):
    B = 304
    counts = {575: 8153, 607: 1024, 608: 224909, 615: 58739}
    assert sum(counts.values()) == S0
    assert sum(q * count for q, count in counts.items()) == S1
    assert sum(comb(q, 2) * count for q, count in counts.items()) == moment_sums(B)[2]
    local_sum = sum(local[q] * count for q, count in counts.items())
    certificate = ceil_fraction(Fraction(local_sum, CROSSING_MULTIPLICITY))
    threshold_sum = (TARGET - 1) * CROSSING_MULTIPLICITY + 1
    return B, counts, local_sum, certificate, threshold_sum - local_sum


def main() -> None:
    assert TOTAL_EXCESS == 2 * M - (K - 1) * N
    assert Q_MIN == M - (K - 1) * T - (TOTAL_EXCESS - (MIN_SUPPORT - T))
    assert Q_MAX == M - (K - 1) * T + comb(T, 2)

    bounds, table_digest = recursive_closure(N)
    assert table_digest == "55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43"
    local = bounds[N - T]
    assert [local[q] for q in (575, 607, 608, 610, 615)] == [3634, 4355, 4379, 4429, 4555]

    feasible_B = feasible_degree_square_excesses()
    assert (len(feasible_B), feasible_B[0], feasible_B[-1]) == (298, 0, 304)
    assert sum(comb(x, 2) for x in ([24, 8] + [1] * 16)) == 304

    totals, switches = sharp_moment_relaxations(local, feasible_B)
    assert switches == ((0, (608, 610, 615)), (12, (575, 608, 615)))
    best_B = max(feasible_B, key=totals.get)
    assert best_B == 304
    best_ratio = totals[best_B] / CROSSING_MULTIPLICITY
    assert best_ratio == Fraction(742965030571, 122358390)
    assert ceil_fraction(best_ratio) == 6073

    B, counts, local_sum, certificate, gap = integral_obstruction(local)
    assert B == 304
    assert local_sum == 1286520178
    assert certificate == 6073
    assert gap == 2321531

    record = (
        f"B={feasible_B};switches={switches};best={best_B},{best_ratio};"
        f"integral={sorted(counts.items())},{local_sum},{certificate},{gap};"
        f"table={table_digest}"
    )
    result_digest = sha256(record.encode("ascii")).hexdigest()

    print("PASS Albertson r=27 four-deletion second-moment barrier")
    print(f"degree_square_values={len(feasible_B)}, range={feasible_B[0]}..{feasible_B[-1]}")
    print(f"dual_contact_switches={switches}")
    print(f"sharp_relaxation_max_at_B={best_B}: {best_ratio}; ceiling=6073")
    print(
        f"integral_obstruction={counts}; local_sum={local_sum}; "
        f"ceiling={certificate}; target_sum_gap={gap}"
    )
    print(f"recursive_table_sha256={table_digest}")
    print(f"result_sha256={result_digest}")


if __name__ == "__main__":
    main()
