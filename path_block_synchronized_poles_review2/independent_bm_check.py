#!/usr/bin/env python3
"""Independent exact check of synchronized endpoint root-of-unity poles.

The target verifier multiplies a coefficient prefix by a known common
quasipolynomial denominator.  This checker instead forms the h-star series
coefficients and recovers their minimal rational recurrence with exact
Berlekamp--Massey over Q.  Cyclotomic valuations of the reconstructed
numerator and denominator then give the pole orders.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from functools import cache
from math import comb, gcd, lcm


Partition = tuple[int, ...]
IntPolynomial = list[int]  # constant coefficient first


@cache
def partitions(total: int, maximum: int | None = None) -> tuple[Partition, ...]:
    if total == 0:
        return ((),)
    maximum = min(total, total if maximum is None else maximum)
    result: list[Partition] = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def divisors(number: int) -> tuple[int, ...]:
    return tuple(value for value in range(1, number + 1) if number % value == 0)


def trim(poly: list[int] | list[Fraction]) -> list[int] | list[Fraction]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mul(left: IntPolynomial, right: IntPolynomial) -> IntPolynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)  # type: ignore[return-value]


def exact_division(
    numerator: IntPolynomial, denominator: IntPolynomial
) -> IntPolynomial | None:
    numerator = trim(numerator[:])  # type: ignore[assignment]
    denominator = trim(denominator[:])  # type: ignore[assignment]
    if denominator == [0]:
        raise ZeroDivisionError
    if len(numerator) < len(denominator):
        return [0] if numerator == [0] else None
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    leading = denominator[-1]
    for degree in range(len(numerator) - 1, len(denominator) - 2, -1):
        value = numerator[degree]
        if value == 0:
            continue
        if value % leading:
            return None
        coefficient = value // leading
        offset = degree - len(denominator) + 1
        quotient[offset] = coefficient
        for j, entry in enumerate(denominator):
            numerator[offset + j] -= coefficient * entry
    return trim(quotient) if not any(numerator) else None  # type: ignore[return-value]


@cache
def cyclotomic(order: int) -> tuple[int, ...]:
    if order < 1:
        raise ValueError(order)
    polynomial: IntPolynomial = [-1] + [0] * (order - 1) + [1]
    for proper_divisor in divisors(order)[:-1]:
        quotient = exact_division(polynomial, list(cyclotomic(proper_divisor)))
        if quotient is None:
            raise AssertionError((order, proper_divisor))
        polynomial = quotient
    return tuple(polynomial)


def valuation(poly: IntPolynomial, factor: IntPolynomial) -> int:
    value = 0
    remainder = poly[:]
    while True:
        quotient = exact_division(remainder, factor)
        if quotient is None:
            return value
        value += 1
        remainder = quotient


def accumulated_counts(partition: Partition, maximum: int) -> list[int]:
    exact = [0] * (maximum + 1)
    exact[0] = 1
    for weight in partition:
        for degree in range(weight, maximum + 1):
            exact[degree] += exact[degree - weight]
    running = 0
    for degree, value in enumerate(exact):
        running += value
        exact[degree] = running
    return exact


def endpoint_determinant(partition: Partition) -> IntPolynomial:
    determinant: IntPolynomial = [1, -1]
    for weight in partition + partition:
        factor = [0] * (weight + 1)
        factor[0] = 1
        factor[weight] = -1
        determinant = poly_mul(determinant, factor)
    return determinant


def hstar_series(partition: Partition, maximum: int) -> list[int]:
    counts = accumulated_counts(partition, maximum)
    square = [value * value for value in counts]
    determinant = endpoint_determinant(partition)
    return [
        sum(
            determinant[j] * square[degree - j]
            for j in range(min(degree, len(determinant) - 1) + 1)
        )
        for degree in range(maximum + 1)
    ]


def berlekamp_massey(sequence: list[int]) -> list[Fraction]:
    """Return C with sum_i C[i] s[n-i] = 0 over the rationals."""
    connection = [Fraction(1)]
    previous = [Fraction(1)]
    order = 0
    shift = 1
    previous_discrepancy = Fraction(1)

    for index, value in enumerate(sequence):
        discrepancy = Fraction(value)
        for j in range(1, order + 1):
            if j < len(connection):
                discrepancy += connection[j] * sequence[index - j]
        if discrepancy == 0:
            shift += 1
            continue

        old_connection = connection[:]
        multiplier = -discrepancy / previous_discrepancy
        required = len(previous) + shift
        if len(connection) < required:
            connection.extend(Fraction(0) for _ in range(required - len(connection)))
        for j, coefficient in enumerate(previous):
            connection[j + shift] += multiplier * coefficient

        if 2 * order <= index:
            order = index + 1 - order
            previous = old_connection
            previous_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1

    connection = connection[: order + 1]
    return trim(connection)  # type: ignore[return-value]


def primitive_integer_polynomial(poly: list[Fraction]) -> IntPolynomial:
    denominator = 1
    for coefficient in poly:
        denominator = lcm(denominator, coefficient.denominator)
    result = [int(coefficient * denominator) for coefficient in poly]
    content = 0
    for coefficient in result:
        content = gcd(content, abs(coefficient))
    if content:
        result = [coefficient // content for coefficient in result]
    if result[0] < 0:
        result = [-coefficient for coefficient in result]
    return trim(result)  # type: ignore[return-value]


def reconstruct_fraction(partition: Partition) -> tuple[IntPolynomial, IntPolynomial]:
    period = 1
    for part in partition:
        period = lcm(period, part)
    cycles = len(partition)
    determinant_degree = 1 + 2 * sum(partition)
    recurrence_bound = period * (2 * cycles + 1) + determinant_degree
    training_length = 2 * recurrence_bound + 8
    held_out = recurrence_bound + 8
    sequence = hstar_series(partition, training_length + held_out - 1)

    connection_q = berlekamp_massey(sequence[:training_length])
    for degree in range(training_length, len(sequence)):
        discrepancy = sum(
            connection_q[j] * sequence[degree - j]
            for j in range(len(connection_q))
        )
        if discrepancy:
            raise AssertionError((partition, "held-out recurrence", degree, discrepancy))

    denominator = primitive_integer_polynomial(connection_q)
    numerator = [
        sum(
            denominator[j] * sequence[degree - j]
            for j in range(min(degree, len(denominator) - 1) + 1)
        )
        for degree in range(len(sequence))
    ]
    numerator = trim(numerator)  # type: ignore[assignment]
    if len(numerator) >= training_length:
        raise AssertionError((partition, "unresolved numerator tail", len(numerator)))
    return numerator, denominator


def preimage_root_orders(scale: int, reduced_order: int) -> tuple[int, ...]:
    """Orders ell satisfying ell/gcd(ell,scale)=reduced_order."""
    return tuple(
        reduced_order * factor
        for factor in divisors(scale)
        if gcd(reduced_order, scale // factor) == 1
    )


def expected_rectangular(partition: Partition) -> IntPolynomial:
    scale = partition[0]
    cycles = len(partition)
    result = [0] * (scale * cycles + 1)
    for j in range(cycles + 1):
        result[scale * j] = comb(cycles, j) ** 2
    return trim(result)  # type: ignore[return-value]


def check_partition(partition: Partition) -> tuple[int, tuple[int, ...]] | None:
    numerator, denominator = reconstruct_fraction(partition)
    scale = gcd(*partition)
    reduced = tuple(part // scale for part in partition)

    if all(part == 1 for part in reduced):
        expected = expected_rectangular(partition)
        if denominator != [1] or numerator != expected:
            raise AssertionError((partition, numerator, denominator, expected))
        return None

    cycles = len(reduced)
    divisibility = {
        order: sum(part % order == 0 for part in reduced)
        for order in range(2, max(reduced) + 1)
    }
    maximal = max(divisibility.values())
    maximizing_orders = tuple(
        order for order, count in divisibility.items() if count == maximal
    )
    expected_order = cycles - maximal
    checked_root_orders: list[int] = []
    for reduced_order in maximizing_orders:
        for root_order in preimage_root_orders(scale, reduced_order):
            factor = list(cyclotomic(root_order))
            actual = valuation(denominator, factor) - valuation(numerator, factor)
            if actual != expected_order:
                raise AssertionError(
                    (partition, reduced_order, root_order, actual, expected_order)
                )
            checked_root_orders.append(root_order)
    return expected_order, tuple(checked_root_orders)


def verify(maximum_width: int) -> dict[str, object]:
    checked = 0
    nonrectangular = 0
    root_orders = 0
    histogram: dict[int, int] = {}
    for width in range(1, maximum_width + 1):
        for partition in partitions(width):
            witness = check_partition(partition)
            checked += 1
            if witness is not None:
                nonrectangular += 1
                pole_order, orders = witness
                root_orders += len(orders)
                histogram[pole_order] = histogram.get(pole_order, 0) + 1

    least_num, least_den = reconstruct_fraction((2, 1))
    if least_num != [1, 2, 6, 2, 1] or least_den != [1, 1]:
        raise AssertionError(((2, 1), least_num, least_den))
    scaled_num, scaled_den = reconstruct_fraction((4, 2))
    if scaled_num != [1, 0, 2, 0, 6, 0, 2, 0, 1] or scaled_den != [1, 0, 1]:
        raise AssertionError(((4, 2), scaled_num, scaled_den))

    report: dict[str, object] = {
        "maximum_width": maximum_width,
        "partitions_checked": checked,
        "nonrectangular_checked": nonrectangular,
        "maximizing_preimage_orders_checked": root_orders,
        "pole_order_histogram": tuple(sorted(histogram.items())),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=10)
    args = parser.parse_args()
    if args.maximum_width < 1:
        raise SystemExit("maximum width must be positive")
    report = verify(args.maximum_width)
    histogram = ",".join(
        f"{order}:{count}" for order, count in report["pole_order_histogram"]
    )
    print(
        "INDEPENDENT SYNCHRONIZED-POLE AUDIT PASSED; "
        f"maximum_width={report['maximum_width']}; "
        f"partitions_checked={report['partitions_checked']}; "
        f"nonrectangular_checked={report['nonrectangular_checked']}; "
        f"maximizing_preimage_orders_checked="
        f"{report['maximizing_preimage_orders_checked']}; "
        f"pole_order_histogram={histogram}; sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
