#!/usr/bin/env python3
"""Exact Q(zeta_5) model for the golden reciprocal-overlay closure."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations

ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
ZETA = (F(0), F(1), F(0), F(0))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    """Multiply modulo 1+x+x^2+x^3+x^4."""
    coefficients = [F(0)] * 7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            coefficients[i + j] += x * y
    for degree in range(6, 3, -1):
        value = coefficients[degree]
        for offset in range(1, 5):
            coefficients[degree - offset] -= value
    return tuple(coefficients[:4])


def power(a, exponent):
    result = ONE
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent //= 2
    return result


def conjugate(a):
    """Complex conjugation: zeta maps to zeta^-1."""
    c0, c1, c2, c3 = a
    return (c0 - c1, -c1, -c1 + c3, -c1 + c2)


def norm(a):
    return mul(a, conjugate(a))


def inverse(a):
    """Invert by exact Gaussian elimination on the power basis."""
    columns = [mul(a, power(ZETA, exponent)) for exponent in range(4)]
    matrix = [
        [columns[column][row] for column in range(4)] + [ONE[row]]
        for row in range(4)
    ]
    for column in range(4):
        pivot = next(row for row in range(column, 4) if matrix[row][column])
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        value = matrix[column][column]
        matrix[column] = [entry / value for entry in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            value = matrix[row][column]
            if value:
                matrix[row] = [
                    entry - value * pivot_entry
                    for entry, pivot_entry in zip(matrix[row], matrix[column])
                ]
    result = tuple(matrix[row][4] for row in range(4))
    if mul(a, result) != ONE:
        raise ArithmeticError("field inversion failed")
    return result


PHI = (F(0), F(0), F(-1), F(-1))
PHI_SQUARED = add(PHI, ONE)
INVERSE_PHI_SQUARED = mul(inverse(PHI), inverse(PHI))
UNIT_NORM = (F(3), F(0), F(1), F(1))
GOLDEN_NORM = mul(PHI_SQUARED, UNIT_NORM)

# Coefficients of five pentagon vertices in Parts's source, in label order.
# A physical point is q times the displayed cyclotomic sum, where
# q=1/|1-zeta|.  The common factor is omitted in all stored coordinates.
SOURCE_ROWS = (
    (0, 0, 0, 0, 5), (1, 0, 0, 0, 4),
    (0, 0, 0, 1, 4), (1, 0, 0, 1, 3),
    (0, 1, 0, 0, 4), (0, 0, 1, 0, 4),
    (1, 0, 1, 0, 3), (0, 1, 0, 1, 3),
    (1, 1, 0, 0, 3), (0, 0, 1, 1, 3),
    (1, 1, 0, 1, 2), (1, 0, 1, 1, 2),
    (0, 1, 1, 0, 3), (1, 1, 1, 0, 2),
    (0, 1, 1, 1, 2), (1, 1, 1, 1, 1),
)

POWERS = tuple(power(ZETA, exponent) for exponent in range(5))
SOURCE = tuple(
    tuple(
        sum(F(coefficient) * POWERS[exponent][coordinate]
            for exponent, coefficient in enumerate(row))
        for coordinate in range(4)
    )
    for row in SOURCE_ROWS
)


def canonical_key(a):
    """Encode z=((A+B sqrt5)+i sqrt(10+2sqrt5)(C+D sqrt5))/88."""
    c0, c1, c2, c3 = a
    real_a = c0 - (c1 + c2 + c3) / 4
    real_b = (c1 - c2 - c3) / 4
    imag_c = c1 / 4 - c2 / 8 + c3 / 8
    imag_d = c2 / 8 - c3 / 8
    values = (real_a, real_b, imag_c, imag_d)
    integers = tuple(int(88 * value) for value in values)
    if any(F(integer, 88) != value
           for integer, value in zip(integers, values)):
        raise ArithmeticError("coordinate is not on the certified denominator-88 grid")
    return integers


def point_set_key(points):
    return tuple(sorted(canonical_key(point) for point in points))


def source_edges(target_norm):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(SOURCE)), 2)
        if norm(sub(SOURCE[right], SOURCE[left])) == target_norm
    )


def enumerate_copies(scale_squared):
    pairs = tuple(combinations(range(len(SOURCE)), 2))
    differences = {
        pair: sub(SOURCE[pair[1]], SOURCE[pair[0]]) for pair in pairs
    }
    inverses = {pair: inverse(value) for pair, value in differences.items()}
    conjugate_inverses = {
        pair: inverse(conjugate(value)) for pair, value in differences.items()
    }
    copies = {}
    raw_specifications = 0
    for source_left, source_right in pairs:
        source_difference = differences[source_left, source_right]
        source_norm = norm(source_difference)
        for target_left, target_right in pairs:
            target_difference = differences[target_left, target_right]
            if norm(target_difference) != mul(scale_squared, source_norm):
                continue
            for swap in (False, True):
                image_left, image_right = (
                    (target_right, target_left) if swap
                    else (target_left, target_right)
                )
                image_difference = sub(SOURCE[image_right], SOURCE[image_left])
                for reflected in (False, True):
                    raw_specifications += 1
                    multiplier = mul(
                        image_difference,
                        conjugate_inverses[source_left, source_right]
                        if reflected else inverses[source_left, source_right],
                    )
                    moved = []
                    for point in SOURCE:
                        difference = sub(point, SOURCE[source_left])
                        if reflected:
                            difference = conjugate(difference)
                        moved.append(add(
                            SOURCE[image_left], mul(multiplier, difference)
                        ))
                    key = point_set_key(moved)
                    copies.setdefault(
                        key,
                        (source_left, source_right, target_left, target_right,
                         swap, reflected, tuple(moved)),
                    )
    return raw_specifications, tuple(copies[key] for key in sorted(copies))


def integer_power_basis(a):
    integers = tuple(int(11 * value) for value in a)
    if any(F(integer, 11) != value
           for integer, value in zip(integers, a)):
        raise ArithmeticError("point is not on the certified denominator-11 grid")
    return integers


def integer_mul(a, b):
    coefficients = [0] * 7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            coefficients[i + j] += x * y
    for degree in range(6, 3, -1):
        value = coefficients[degree]
        for offset in range(1, 5):
            coefficients[degree - offset] -= value
    return tuple(coefficients[:4])


def integer_conjugate(a):
    c0, c1, c2, c3 = a
    return (c0 - c1, -c1, -c1 + c3, -c1 + c2)


INTEGER_UNIT_NORM = (363, 0, 121, 121)


def unit_edges(points):
    integer_points = tuple(integer_power_basis(point) for point in points)
    edges = []
    for left, right in combinations(range(len(points)), 2):
        difference = tuple(
            y - x for x, y in zip(integer_points[left], integer_points[right])
        )
        if integer_mul(difference, integer_conjugate(difference)) \
                == INTEGER_UNIT_NORM:
            edges.append((left, right))
    return tuple(edges)


def digest_rows(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(str(value) for value in row) + "\n").encode())
    return digest.hexdigest()


def build_closures():
    groups = {}
    for name, scale_squared in (
            ("down", INVERSE_PHI_SQUARED), ("up", PHI_SQUARED)):
        raw, copies = enumerate_copies(scale_squared)
        groups[name] = (raw, copies)

    closure_rows = {}
    for name, (_raw, copies) in groups.items():
        point_map = {canonical_key(point): point for point in SOURCE}
        for copy in copies:
            for point in copy[-1]:
                point_map.setdefault(canonical_key(point), point)
        keys = tuple(sorted(point_map))
        points = tuple(point_map[key] for key in keys)
        closure_rows[name] = (keys, points, unit_edges(points))

    point_map = {canonical_key(point): point for point in SOURCE}
    for _raw, copies in groups.values():
        for copy in copies:
            for point in copy[-1]:
                point_map.setdefault(canonical_key(point), point)
    keys = tuple(sorted(point_map))
    points = tuple(point_map[key] for key in keys)
    edges = unit_edges(points)
    return groups, closure_rows, keys, points, edges
