#!/usr/bin/env python3
"""Independent exact audit for the odd cyclic block-polytope theorem.

Python 3.11+, standard library only.  The primary counting path enumerates
row sums directly and reconstructs residue polynomials by a rational
Vandermonde solve; it does not import the submitted verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = ROOT / "EXPECTED.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trim(poly: list[Q]) -> list[Q]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def evaluate(poly: list[Q], x: int | Q) -> Q:
    answer = Q(0)
    for coefficient in reversed(poly):
        answer = answer * x + coefficient
    return answer


def solve_square(matrix: list[list[Q]], rhs: list[Q]) -> list[Q] | None:
    """Exact Gaussian elimination; return None for a singular matrix."""
    n = len(rhs)
    augmented = [list(map(Q, row)) + [Q(value)] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((row for row in range(column, n) if augmented[row][column]), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    x - factor * y
                    for x, y in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def interpolate(points: list[tuple[int, int]]) -> list[Q]:
    """Power-basis interpolation by an exact Vandermonde solve."""
    matrix = [[Q(x) ** degree for degree in range(len(points))] for x, _ in points]
    answer = solve_square(matrix, [Q(y) for _, y in points])
    require(answer is not None, "singular interpolation system")
    return trim(answer)


def direct_row_count(widths: tuple[int, ...], n: int) -> int:
    """Sum stars-and-bars weights over concrete feasible cyclic row sums."""
    m = len(widths)
    weights = tuple(
        tuple(math.comb(r + width - 1, width - 1) for r in range(n + 1))
        for width in widths
    )
    total = 0
    for first in range(n + 1):
        @lru_cache(maxsize=None)
        def suffix(block: int, previous: int) -> int:
            if block == m:
                return int(previous + first <= n)
            return sum(
                weights[block][value] * suffix(block + 1, value)
                for value in range(n - previous + 1)
            )

        total += weights[0][first] * suffix(1, first)
    return total


def coordinate_count(widths: tuple[int, ...], n: int) -> int:
    d = sum(widths)
    answer = 0
    for point in itertools.product(range(n + 1), repeat=d):
        rows = []
        offset = 0
        for width in widths:
            rows.append(sum(point[offset:offset + width]))
            offset += width
        if all(rows[i] + rows[(i + 1) % len(rows)] <= n for i in range(len(rows))):
            answer += 1
    return answer


def poly_divide(numerator: list[Q], denominator: list[Q]) -> tuple[list[Q], list[Q]]:
    numerator = numerator[:]
    denominator = trim(denominator[:])
    if len(numerator) < len(denominator):
        return [Q(0)], trim(numerator)
    quotient = [Q(0)] * (len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and any(numerator):
        degree = len(numerator) - len(denominator)
        factor = numerator[-1] / denominator[-1]
        quotient[degree] = factor
        for i, value in enumerate(denominator):
            numerator[degree + i] -= factor * value
        trim(numerator)
    return trim(quotient), trim(numerator or [Q(0)])


def gamma_by_linear_system(h: list[Q]) -> list[Q]:
    """Solve for gamma coefficients without the target's greedy transform."""
    degree = len(h) - 1
    count = degree // 2 + 1
    matrix = []
    for power in range(count):
        row = []
        for j in range(count):
            exponent = power - j
            top = degree - 2 * j
            row.append(Q(math.comb(top, exponent)) if 0 <= exponent <= top else Q(0))
        matrix.append(row)
    answer = solve_square(matrix, h[:count])
    require(answer is not None, "singular gamma basis")
    reconstructed = [Q(0)] * (degree + 1)
    for j, value in enumerate(answer):
        for exponent in range(degree - 2 * j + 1):
            reconstructed[j + exponent] += value * math.comb(degree - 2 * j, exponent)
    require(reconstructed == h, "gamma reconstruction failed")
    return answer


def enumerate_vertices(blocks: tuple[int, ...]) -> set[tuple[Q, ...]]:
    """Enumerate vertices by all full-rank tight-constraint bases."""
    d = sum(blocks)
    constraints: list[tuple[list[Q], Q]] = []
    for coordinate in range(d):
        row = [Q(0)] * d
        row[coordinate] = Q(1)
        constraints.append((row, Q(0)))
    starts = []
    offset = 0
    for width in blocks:
        starts.append(tuple(range(offset, offset + width)))
        offset += width
    for block in range(len(blocks)):
        row = [Q(0)] * d
        for coordinate in starts[block] + starts[(block + 1) % len(blocks)]:
            row[coordinate] = Q(1)
        constraints.append((row, Q(1)))

    vertices: set[tuple[Q, ...]] = set()
    for chosen in itertools.combinations(range(len(constraints)), d):
        solution = solve_square(
            [constraints[index][0] for index in chosen],
            [constraints[index][1] for index in chosen],
        )
        if solution is None or any(value < 0 for value in solution):
            continue
        if any(
            sum(solution[coordinate] for coordinate in starts[block] + starts[(block + 1) % len(blocks)]) > 1
            for block in range(len(blocks))
        ):
            continue
        vertices.add(tuple(solution))
    return vertices


def row_projection(point: tuple[Q, ...], blocks: tuple[int, ...]) -> tuple[Q, ...]:
    result = []
    offset = 0
    for width in blocks:
        result.append(sum(point[offset:offset + width], Q(0)))
        offset += width
    return tuple(result)


def inverse_cycle(m: int) -> list[list[Q]]:
    matrix = [
        [Q(int(j == i or j == (i + 1) % m)) for j in range(m)]
        for i in range(m)
    ]
    inverse = []
    for column in range(m):
        rhs = [Q(int(i == column)) for i in range(m)]
        solution = solve_square(matrix, rhs)
        require(solution is not None, "odd cycle matrix is singular")
        inverse.append(solution)
    return [list(row) for row in zip(*inverse)]


def matrix_product(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def audit_matrix_and_cone() -> dict[str, int]:
    parity_vectors = 0
    for m in (3, 5, 7):
        inverse = inverse_cycle(m)
        expected = [
            [Q((-1) ** ((j - i) % m), 2) for j in range(m)]
            for i in range(m)
        ]
        require(inverse == expected, "cycle inverse formula failed")
        transpose = [list(row) for row in zip(*inverse)]
        gram = matrix_product(inverse, transpose)
        require(all(gram[i][i] == Q(m, 4) for i in range(m)), "Gram diagonal failed")
        require(sum(map(sum, gram), Q(0)) == Q(m, 4), "Gram total failed")
        for u in itertools.product(range(-1, 3), repeat=m):
            image = [sum(inverse[i][j] * u[j] for j in range(m)) for i in range(m)]
            integral = all(value.denominator == 1 for value in image)
            require(integral == (sum(u) % 2 == 0), "lattice parity characterization failed")
            parity_vectors += 1
    return {"parity_vectors": parity_vectors, "matrix_orders": 3}


def audit_vertices() -> dict[str, int]:
    row_vertex_count = 0
    block_vertex_count = 0
    for m in (3, 5, 7):
        vertices = enumerate_vertices((1,) * m)
        half = (Q(1, 2),) * m
        require(half in vertices, "fractional cycle vertex missing")
        require(
            all(all(value in (0, Q(1, 2), 1) for value in vertex) for vertex in vertices),
            "row vertex is not half-integral",
        )
        require(
            {vertex for vertex in vertices if any(value.denominator == 2 for value in vertex)} == {half},
            "row polytope has another fractional vertex",
        )
        row_vertex_count += len(vertices)

    for blocks in ((2, 1, 2), (2, 2, 2), (3, 1, 2)):
        vertices = enumerate_vertices(blocks)
        row_vertices = enumerate_vertices((1,) * len(blocks))
        for vertex in vertices:
            projection = row_projection(vertex, blocks)
            require(projection in row_vertices, "block vertex projects to a nonvertex")
            require(all(value.denominator <= 2 for value in vertex), "block vertex denominator exceeds two")
            offset = 0
            for width in blocks:
                require(sum(vertex[offset + j] > 0 for j in range(width)) <= 1,
                        "two positive coordinates in one block")
                offset += width
        require(any(any(value.denominator == 2 for value in vertex) for vertex in vertices),
                "block polytope has no fractional vertex")
        block_vertex_count += len(vertices)
    return {"row_vertices": row_vertex_count, "block_vertices": block_vertex_count}


def audit_case(widths: tuple[int, ...]) -> tuple[dict[str, object], int]:
    m = len(widths)
    d = sum(widths)
    b = tuple(width - 1 for width in widths)
    k = sum(b)
    maximum = 2 * d + 5
    values = [direct_row_count(widths, n) for n in range(maximum + 1)]
    even = interpolate([(n, values[n]) for n in range(0, 2 * d + 1, 2)])
    odd = interpolate([(n, values[n]) for n in range(1, 2 * d + 2, 2)])
    for n in range(2 * d + 2, maximum + 1):
        require(evaluate(even if n % 2 == 0 else odd, n) == values[n],
                "residue polynomial misses an extra dilation")
    length = max(len(even), len(odd))
    even += [Q(0)] * (length - len(even))
    odd += [Q(0)] * (length - len(odd))
    alternating = trim([(x - y) / 2 for x, y in zip(even, odd)])
    denominator = math.prod(math.factorial(value) for value in b)
    require(len(alternating) == k + 1, "wrong alternating degree")
    require(alternating[-1] == Q(1, 2 ** (d + 1) * denominator),
            "wrong alternating leading coefficient")
    require(evaluate(even, 0) == 1, "n=0 polynomial extension failed")

    h = []
    for n in range(maximum + 1):
        h.append(sum(
            (-1) ** j * math.comb(d + 1, j) * values[n - 2 * j]
            for j in range(min(d + 1, n // 2) + 1)
        ))
    h = trim(list(map(Q, h)))
    quotient = h
    multiplicity = 0
    while len(quotient) > 1:
        candidate, remainder = poly_divide(quotient, [Q(1), Q(1)])
        if any(remainder):
            break
        quotient = candidate
        multiplicity += 1
    residual = math.factorial(k) // denominator
    require(multiplicity == m, "wrong root multiplicity")
    require(evaluate(quotient, -1) == residual, "wrong residual at minus one")

    record: dict[str, object] = {
        "widths": list(widths),
        "alternating_degree": k,
        "alternating_leading": str(alternating[-1]),
        "root_multiplicity": multiplicity,
        "residual": residual,
    }
    if len(set(widths)) == 1:
        a = widths[0]
        bb = a - 1
        c = 2 * a + 1
        degree = 2 * a * (m - 1) + 1
        require(len(h) == degree + 1 and h == h[::-1], "palindromicity failed")
        gamma = gamma_by_linear_system(h)
        index = (degree - m) // 2
        mass = math.factorial(m * bb) // math.factorial(bb) ** m
        require(gamma[index] == (-1) ** index * mass, "terminal gamma failed")
        require(not any(gamma[index + 1:]), "gamma tail did not vanish")
        if bb:
            ratio = Q(bb * (4 * bb + 3) * (m * m - 1), 24 * (m * bb - 1))
            require(gamma[index - 1] == (-1) ** (index - 1) * mass * ratio,
                    "penultimate gamma failed")
            require(gamma[index] * gamma[index - 1] < 0, "terminal signs agree")
            beta = alternating[-1]
            center = Q(c, 2)
            variance = Q(m * bb * (3 * m - 3 * bb - 4 * bb * bb + 4), 24)
            require(alternating[k - 1] == beta * k * center,
                    "centered linear coefficient failed")
            require(alternating[k - 2] == beta * (math.comb(k, 2) * center ** 2 + variance),
                    "centered quadratic coefficient failed")

            offsets = [Q(j) - Q(a, 2) for j in range(1, bb + 1)]
            require(sum(offsets, Q(0)) == 0, "offset sum failed")
            offset_e2 = sum((offsets[i] * offsets[j]
                             for i in range(bb) for j in range(i + 1, bb)), Q(0))
            require(offset_e2 == -Q(bb * (bb * bb - 1), 24), "offset e2 failed")
            e0 = (
                m * offset_e2
                - Q(m * m * bb * (bb - 1), 32)
                + Q(m * bb * bb * (m - 1), 32)
            )
            require(4 * e0 == variance, "Hessian coefficient aggregation failed")
            expansion = Q(d + 1, 8) + Q(k + 1, 24) + variance / (k * (k - 1))
            require(expansion == ratio, "asymptotic-to-gamma simplification failed")

        for n in range(c):
            interior = 0
            for rows in itertools.product(range(n + 1), repeat=m):
                if all(value >= a for value in rows) and all(
                    rows[i] + rows[(i + 1) % m] <= n - 1 for i in range(m)
                ):
                    interior += math.prod(math.comb(value - 1, a - 1) for value in rows)
            require(interior == 0, "interior point occurs below codegree")
        for n in range(c, c + 3):
            interior = 0
            for rows in itertools.product(range(n + 1), repeat=m):
                if all(value >= a for value in rows) and all(
                    rows[i] + rows[(i + 1) % m] <= n - 1 for i in range(m)
                ):
                    interior += math.prod(math.comb(value - 1, a - 1) for value in rows)
            require(interior == values[n - c], "interior translation failed")
        record.update({
            "numerator_degree": degree,
            "terminal_gamma": int(gamma[index]),
            "penultimate_gamma": int(gamma[index - 1]) if index else None,
        })
    return record, len(values)


def build_report() -> dict[str, object]:
    cases = (
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
        (1, 1, 2),
        (1, 2, 2),
        (1, 2, 3),
        (1, 3, 5),
        (2, 3, 4),
        (1, 1, 6),
        (2, 5, 2),
        (4, 1, 3),
        (1, 1, 1, 1, 1),
        (2, 2, 2, 2, 2),
        (1, 2, 1, 2, 1),
        (1, 1, 1, 1, 1, 1, 1),
    )
    records = []
    dilation_values = 0
    for widths in cases:
        record, checked = audit_case(widths)
        records.append(record)
        dilation_values += checked

    coordinate_checks = 0
    for widths, maximum in (((1, 1, 1), 4), ((2, 1, 1), 3), ((2, 2, 2), 2)):
        for n in range(maximum + 1):
            require(coordinate_count(widths, n) == direct_row_count(widths, n),
                    "stars-and-bars reduction failed")
            coordinate_checks += 1

    vertices = audit_vertices()
    matrices = audit_matrix_and_cone()
    digest = hashlib.sha256(
        json.dumps(records, separators=(",", ":"), sort_keys=True).encode("ascii")
    ).hexdigest()
    return {
        "arithmetic": "exact Python integers and Fraction",
        "case_count": len(cases),
        "dilation_values": dilation_values,
        "coordinate_checks": coordinate_checks,
        **vertices,
        **matrices,
        "record_sha256": digest,
        "status": "VERIFIED",
    }


def main() -> None:
    report = build_report()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    require(report == expected, "report differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
