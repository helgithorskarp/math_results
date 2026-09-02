"""Small exact implementation of Q(zeta_84) for the Cayley-core checker.

Elements are low-to-high coefficient tuples modulo Phi_84.  Only the field
operations required to derive Haugland's 84 unit vectors are implemented.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Iterable


DEGREE = 24
MODULUS = (
    1, 0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0,
    1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1, 0, 1,
)
Element = tuple[Fraction, ...]
Point = tuple[Element, Element]


def pad(coefficients: Iterable[Fraction | int]) -> Element:
    result = tuple(Fraction(value) for value in coefficients)
    if len(result) > DEGREE:
        raise ValueError("element degree exceeds field degree")
    return result + (Fraction(0),) * (DEGREE - len(result))


ZERO = pad(())
ONE = pad((1,))
ZETA = pad((0, 1))


def add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value: Element) -> Element:
    return tuple(-coefficient for coefficient in value)


def sub(left: Element, right: Element) -> Element:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def scale(value: Element, scalar: Fraction | int) -> Element:
    scalar = Fraction(scalar)
    return tuple(scalar * coefficient for coefficient in value)


def multiply(left: Element, right: Element) -> Element:
    product = [Fraction(0)] * (2 * DEGREE - 1)
    left_support = [(i, value) for i, value in enumerate(left) if value]
    right_support = [(i, value) for i, value in enumerate(right) if value]
    for i, a in left_support:
        for j, b in right_support:
            product[i + j] += a * b
    for exponent in range(2 * DEGREE - 2, DEGREE - 1, -1):
        leading = product[exponent]
        if not leading:
            continue
        product[exponent] = 0
        shift = exponent - DEGREE
        for i, coefficient in enumerate(MODULUS[:-1]):
            if coefficient:
                product[shift + i] -= leading * coefficient
    return tuple(product[:DEGREE])


def _trim(poly: list[Fraction]) -> list[Fraction]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def _poly_sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = left[:] + [Fraction(0)] * max(0, len(right) - len(left))
    for i, value in enumerate(right):
        result[i] -= value
    return _trim(result)


def _poly_multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    if not left or not right:
        return []
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[i + j] += a * b
    return _trim(result)


def _poly_divmod(
    numerator: list[Fraction], denominator: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    numerator = _trim(numerator[:])
    denominator = _trim(denominator[:])
    if not denominator:
        raise ZeroDivisionError
    quotient = [Fraction(0)] * max(0, len(numerator) - len(denominator) + 1)
    while numerator and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[shift] = coefficient
        for i, value in enumerate(denominator):
            numerator[shift + i] -= coefficient * value
        _trim(numerator)
    return _trim(quotient), numerator


def inverse(value: Element) -> Element:
    if value == ZERO:
        raise ZeroDivisionError
    old_r = [Fraction(value) for value in MODULUS]
    r = _trim(list(value))
    old_t: list[Fraction] = []
    t = [Fraction(1)]
    while r:
        quotient, remainder = _poly_divmod(old_r, r)
        old_r, r = r, remainder
        old_t, t = t, _poly_sub(old_t, _poly_multiply(quotient, t))
    if len(old_r) != 1:
        raise AssertionError("noninvertible field element")
    candidate = pad(coefficient / old_r[0] for coefficient in old_t)
    if multiply(value, candidate) != ONE:
        raise AssertionError("inverse check failed")
    return candidate


def power(value: Element, exponent: int) -> Element:
    if exponent < 0:
        return power(inverse(value), -exponent)
    result = ONE
    base = value
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def point_add(left: Point, right: Point) -> Point:
    return add(left[0], right[0]), add(left[1], right[1])


def point_sub(left: Point, right: Point) -> Point:
    return sub(left[0], right[0]), sub(left[1], right[1])


def squared_norm(point: Point) -> Element:
    return add(multiply(point[0], point[0]), multiply(point[1], point[1]))


def field_constants() -> tuple[Element, list[Point]]:
    imaginary = power(ZETA, 21)
    inverse_i = neg(imaginary)
    if multiply(imaginary, imaginary) != neg(ONE):
        raise AssertionError("zeta^21 is not a square root of -1")
    sqrt3 = multiply(sub(power(ZETA, 14), power(ZETA, -14)), inverse_i)
    if multiply(sqrt3, sqrt3) != scale(ONE, 3):
        raise AssertionError("sqrt(3) identity failed")

    def sine(exponent: int) -> Element:
        return scale(
            multiply(sub(power(ZETA, exponent), power(ZETA, -exponent)), inverse_i),
            Fraction(1, 2),
        )

    alpha = inverse(sine(12))
    beta = inverse(sine(24))
    base_x = scale(multiply(sqrt3, add(alpha, beta)), Fraction(1, 4))
    base_y = scale(sub(alpha, beta), Fraction(1, 4))
    vectors: list[Point] = []
    for j in range(42):
        rotation = power(ZETA, 2 * j)
        inverse_rotation = power(ZETA, -2 * j)
        cosine = scale(add(rotation, inverse_rotation), Fraction(1, 2))
        sine_value = scale(
            multiply(sub(rotation, inverse_rotation), inverse_i), Fraction(1, 2)
        )
        vectors.append((cosine, sine_value))
        vectors.append(
            (
                sub(multiply(base_x, cosine), multiply(base_y, sine_value)),
                add(multiply(base_x, sine_value), multiply(base_y, cosine)),
            )
        )
    if len(set(vectors)) != 84:
        raise AssertionError("the 84 generating vectors are not distinct")
    if any(squared_norm(vector) != ONE for vector in vectors):
        raise AssertionError("a generating vector is not unit")
    if any(vectors[j + 42] != (neg(vectors[j][0]), neg(vectors[j][1])) for j in range(42)):
        raise AssertionError("antipodal vector identity failed")
    return sqrt3, vectors


def coefficient_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def element_text(value: Element) -> str:
    return ",".join(coefficient_text(coefficient) for coefficient in value)


def point_text(point: Point) -> str:
    return element_text(point[0]) + ";" + element_text(point[1])


def coordinate_hash(points: Iterable[Point]) -> str:
    digest = hashlib.sha256()
    for point in sorted(points, key=point_text):
        digest.update((point_text(point) + "\n").encode())
    return digest.hexdigest()


def edge_hash(edges: Iterable[tuple[int, int]]) -> str:
    digest = hashlib.sha256()
    for u, v in sorted(edges):
        digest.update(f"{u} {v}\n".encode())
    return digest.hexdigest()
