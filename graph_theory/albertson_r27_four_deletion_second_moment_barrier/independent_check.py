#!/usr/bin/env python3
"""Independent exact reconstruction of the four-deletion moment barrier."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb


LINES = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
    (Fraction(6), Fraction(266, 9)),
)


def ceiling(x):
    return -((-x.numerator) // x.denominator)


def pava(values):
    blocks = []
    for rise in (values[i + 1] - values[i] for i in range(len(values) - 1)):
        blocks.append([1, rise])
        while len(blocks) > 1:
            a, b = blocks[-2], blocks[-1]
            if Fraction(a[1], a[0]) < Fraction(b[1], b[0]):
                break
            blocks[-2:] = [[a[0] + b[0], a[1] + b[1]]]
    answer = [(0, values[0])]
    for run, rise in blocks:
        answer.append((answer[-1][0] + run, answer[-1][1] + rise))
    return answer


def evaluate(hull, x):
    i = bisect_right([point[0] for point in hull], x) - 1
    if i == len(hull) - 1 or x == hull[i][0]:
        return Fraction(hull[i][1])
    x0, y0 = hull[i]
    x1, y1 = hull[i + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def table():
    rows = {}
    hulls = {}
    digest = sha256()
    for n in range(4, 54):
        row = []
        for m in range(comb(n, 2) + 1):
            value = max([0] + [ceiling(a * m - b * (n - 2)) for a, b in LINES])
            for s in range(4, n):
                mean = Fraction(m * s * (s - 1), n * (n - 1))
                candidate = ceiling(
                    comb(n, s) * evaluate(hulls[s], mean) / comb(n - 4, s - 4)
                )
                value = max(value, candidate)
            row.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode())
        rows[n] = row
        hulls[n] = pava(row)
    return rows, digest.hexdigest()


def partitions(total, least=1, prefix=()):
    if total == 0:
        yield prefix
        return
    for value in range(least, min(24, total) + 1):
        yield from partitions(total - value, value, prefix + (value,))


def feasible_B_values():
    return tuple(
        sorted(
            {
                sum(comb(x, 2) for x in part)
                for part in partitions(48)
                if len(part) >= 18
            }
        )
    )


S0 = comb(53, 4)
S1 = 713 * comb(51, 4)
MULTIPLICITY = comb(49, 4)


def second_moment(B):
    adjacent = 18473 + B
    return adjacent * comb(50, 4) + (comb(713, 2) - adjacent) * comb(49, 4)


def feasible_quadratics(local):
    answer = []
    for x, y, z in combinations(range(575, 616), 3):
        slope0 = Fraction(local[y] - local[x], y - x)
        slope1 = Fraction(local[z] - local[y], z - y)
        c = Fraction(slope1 - slope0, z - x)
        b = slope0 - c * (x + y)
        a = Fraction(local[x]) - b * x - c * x * x
        if all(a + b * q + c * q * q <= local[q] for q in range(575, 616)):
            answer.append((a, b, c, (x, y, z)))
    return tuple(answer)


def main():
    rows, table_digest = table()
    assert table_digest == "55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43"
    local = rows[49]

    feasible_B = feasible_B_values()
    assert (len(feasible_B), min(feasible_B), max(feasible_B)) == (298, 0, 304)

    quadratics = feasible_quadratics(local)
    assert len(quadratics) == 276
    optima = {}
    contacts = {}
    for B in feasible_B:
        sq_sum = 2 * second_moment(B) + S1
        value, contact = max(
            (a * S0 + b * S1 + c * sq_sum, contact)
            for a, b, c, contact in quadratics
        )
        optima[B] = value / MULTIPLICITY
        contacts[B] = contact

    assert {contacts[B] for B in feasible_B if B <= 11} == {(608, 610, 615)}
    assert {contacts[B] for B in feasible_B if B >= 12} == {(575, 608, 615)}
    assert max(optima, key=optima.get) == 304
    assert optima[304] == Fraction(742965030571, 122358390)

    counts = {575: 8153, 607: 1024, 608: 224909, 615: 58739}
    assert sum(counts.values()) == S0
    assert sum(q * number for q, number in counts.items()) == S1
    assert sum(comb(q, 2) * number for q, number in counts.items()) == second_moment(304)
    local_sum = sum(local[q] * number for q, number in counts.items())
    assert local_sum == 1286520178
    assert ceiling(Fraction(local_sum, MULTIPLICITY)) == 6073

    record = (
        f"B={feasible_B};quadratics={len(quadratics)};"
        f"contacts={[(B, contacts[B]) for B in feasible_B]};"
        f"max={optima[304]};integral={sorted(counts.items())},{local_sum};"
        f"table={table_digest}"
    )
    print("PASS independent four-deletion moment reconstruction")
    print(f"unordered_excess_partitions_B_values={len(feasible_B)}")
    print(f"pointwise_feasible_quadratics={len(quadratics)}")
    print(f"sharp_max={optima[304]}; ceiling={ceiling(optima[304])}")
    print(f"integral_obstruction_sum={local_sum}; ceiling=6073")
    print(f"result_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
