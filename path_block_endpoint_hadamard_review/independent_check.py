#!/usr/bin/env python3
"""Independent exact audit of the three-block endpoint Hadamard theorem.

The target checker uses one global quasipolynomial recurrence.  This audit
instead splits each coefficient sequence into residue classes, reconstructs
the numerator of every residue-class generating function by finite
differences, and only then interlaces the classes.  All arithmetic is over
Python integers.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from functools import cache
from math import comb, lcm

Partition = tuple[int, ...]
Polynomial = list[int]  # Constant coefficient first.


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def poly_substitute_power(poly: Polynomial, power: int) -> Polynomial:
    result = [0] * ((len(poly) - 1) * power + 1)
    for degree, coefficient in enumerate(poly):
        result[degree * power] = coefficient
    return trim(result)


def exact_quotient(numerator: Polynomial, denominator: Polynomial) -> Polynomial | None:
    """Return the integer-polynomial quotient, or None when not divisible."""
    numerator = trim(numerator[:])
    denominator = trim(denominator[:])
    if denominator == [0]:
        raise ZeroDivisionError
    if len(numerator) < len(denominator):
        return [0] if numerator == [0] else None
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    lead = denominator[-1]
    for degree in range(len(numerator) - 1, len(denominator) - 2, -1):
        coefficient = numerator[degree]
        if coefficient == 0:
            continue
        if coefficient % lead:
            return None
        q = coefficient // lead
        offset = degree - len(denominator) + 1
        quotient[offset] = q
        for j, value in enumerate(denominator):
            numerator[offset + j] -= q * value
    return trim(quotient) if not any(numerator) else None


def binomial_power_factor(period: int, exponent: int) -> Polynomial:
    result = [0] * (period * exponent + 1)
    for j in range(exponent + 1):
        result[j * period] = (-1) ** j * comb(exponent, j)
    return result


def divisors(number: int) -> tuple[int, ...]:
    return tuple(candidate for candidate in range(1, number + 1) if number % candidate == 0)


@cache
def cyclotomic(order: int) -> tuple[int, ...]:
    """Return the monic cyclotomic polynomial Phi_order."""
    polynomial = [-1] + [0] * (order - 1) + [1]
    for proper_divisor in divisors(order)[:-1]:
        quotient = exact_quotient(polynomial, list(cyclotomic(proper_divisor)))
        if quotient is None:
            raise AssertionError((order, proper_divisor, polynomial))
        polynomial = quotient
    return tuple(polynomial)


def polynomial_valuation(poly: Polynomial, factor: Polynomial) -> int:
    valuation = 0
    residue = poly[:]
    while True:
        quotient = exact_quotient(residue, factor)
        if quotient is None:
            return valuation
        valuation += 1
        residue = quotient


@cache
def partitions(total: int, maximum: int | None = None) -> tuple[Partition, ...]:
    if total == 0:
        return ((),)
    maximum = min(total, maximum if maximum is not None else total)
    result: list[Partition] = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def exact_weight_counts(partition: Partition, maximum: int) -> list[int]:
    counts = [0] * (maximum + 1)
    counts[0] = 1
    for weight in partition:
        for n in range(weight, maximum + 1):
            counts[n] += counts[n - weight]
    return counts


def accumulated_weight_counts(partition: Partition, maximum: int) -> list[int]:
    counts = exact_weight_counts(partition, maximum)
    running = 0
    for n, count in enumerate(counts):
        running += count
        counts[n] = running
    return counts


def cycle_determinant(partition: Partition) -> Polynomial:
    determinant = [1]
    for cycle_length in partition:
        factor = [0] * (cycle_length + 1)
        factor[0] = 1
        factor[cycle_length] = -1
        determinant = poly_mul(determinant, factor)
    return determinant


def endpoint_hadamard_fraction(
    left: Partition, right: Partition
) -> tuple[Polynomial, Polynomial]:
    """Return N,D for sum_n A_left(n) A_right(n) t^n = N/D.

    On each residue modulo L, the coefficients form a polynomial in the
    residue-class index of degree at most m-1, where
    m=#cycles(left)+#cycles(right)+1.  Multiplication by (1-u)^m and finite
    differences recover that residue's numerator from its first m values.
    """
    period = 1
    for cycle_length in left + right:
        period = lcm(period, cycle_length)
    exponent = len(left) + len(right) + 1
    maximum = period * exponent - 1
    left_counts = accumulated_weight_counts(left, maximum)
    right_counts = accumulated_weight_counts(right, maximum)
    numerator = [0] * (period * exponent)
    for residue in range(period):
        values = [
            left_counts[residue + period * q] * right_counts[residue + period * q]
            for q in range(exponent)
        ]
        for k in range(exponent):
            coefficient = sum(
                (-1) ** j * comb(exponent, j) * values[k - j]
                for j in range(k + 1)
            )
            numerator[residue + period * k] = coefficient
    return trim(numerator), binomial_power_factor(period, exponent)


def endpoint_hstar_fraction(
    left: Partition, right: Partition
) -> tuple[Polynomial, Polynomial]:
    numerator, denominator = endpoint_hadamard_fraction(left, right)
    determinant = poly_mul([1, -1], cycle_determinant(left + right))
    return poly_mul(numerator, determinant), denominator


def endpoint_hstar_polynomial(
    left: Partition, right: Partition
) -> Polynomial | None:
    numerator, denominator = endpoint_hstar_fraction(left, right)
    return exact_quotient(numerator, denominator)


def fixed_block_vectors(width: int, cycle_type: Partition, dilation: int) -> list[tuple[int, ...]]:
    """Enumerate coordinate vectors fixed by a canonical permutation."""
    if sum(cycle_type) != width:
        raise ValueError((width, cycle_type))
    boundaries: list[tuple[int, int]] = []
    start = 0
    for cycle_length in cycle_type:
        boundaries.append((start, start + cycle_length))
        start += cycle_length
    result: list[tuple[int, ...]] = []
    for vector in itertools.product(range(dilation + 1), repeat=width):
        if sum(vector) > dilation:
            continue
        if all(len(set(vector[start:end])) == 1 for start, end in boundaries):
            result.append(vector)
    return result


def direct_fixed_count(
    widths: tuple[int, int, int],
    cycle_types: tuple[Partition, Partition, Partition],
    dilation: int,
) -> int:
    blocks = [
        fixed_block_vectors(width, cycle_type, dilation)
        for width, cycle_type in zip(widths, cycle_types, strict=True)
    ]
    sums = [[sum(vector) for vector in block] for block in blocks]
    return sum(
        left + middle <= dilation and middle + right <= dilation
        for left in sums[0]
        for middle in sums[1]
        for right in sums[2]
    )


def factored_fixed_count(
    cycle_types: tuple[Partition, Partition, Partition], dilation: int
) -> int:
    left, middle, right = cycle_types
    left_counts = accumulated_weight_counts(left, dilation)
    middle_counts = exact_weight_counts(middle, dilation)
    right_counts = accumulated_weight_counts(right, dilation)
    return sum(
        middle_counts[block_sum]
        * left_counts[dilation - block_sum]
        * right_counts[dilation - block_sum]
        for block_sum in range(dilation + 1)
    )


def verify_definition_level_counts() -> int:
    checks = 0
    for width in range(1, 4):
        widths = (width, width, width)
        for cycle_types in itertools.product(partitions(width), repeat=3):
            for dilation in range(4):
                direct = direct_fixed_count(widths, cycle_types, dilation)
                factored = factored_fixed_count(cycle_types, dilation)
                if direct != factored:
                    raise AssertionError((widths, cycle_types, dilation, direct, factored))
                checks += 1

    # Unequal widths ensure that no equal-block assumption entered the count.
    widths = (2, 1, 3)
    for cycle_types in itertools.product(*(partitions(width) for width in widths)):
        for dilation in range(4):
            direct = direct_fixed_count(widths, cycle_types, dilation)
            factored = factored_fixed_count(cycle_types, dilation)
            if direct != factored:
                raise AssertionError((widths, cycle_types, dilation, direct, factored))
            checks += 1
    return checks


def rectangular_type(width: int, cycle_length: int) -> Partition:
    if width % cycle_length:
        raise ValueError((width, cycle_length))
    return (cycle_length,) * (width // cycle_length)


def rectangular_formula(left_cycles: int, right_cycles: int, d: int) -> Polynomial:
    degree = d * min(left_cycles, right_cycles)
    result = [0] * (degree + 1)
    for j in range(min(left_cycles, right_cycles) + 1):
        result[d * j] = comb(left_cycles, j) * comb(right_cycles, j)
    return trim(result)


def is_rectangular(partition: Partition) -> bool:
    return len(set(partition)) == 1


def verify_heterogeneous_classification(maximum_width: int = 8) -> tuple[int, int, int]:
    """Audit all endpoint pairs, including unequal endpoint widths."""
    all_types = [
        (width, partition)
        for width in range(1, maximum_width + 1)
        for partition in partitions(width)
    ]
    tested = 0
    polynomial_pairs = 0
    expected_pairs = 0
    for left_width, left in all_types:
        for right_width, right in all_types:
            tested += 1
            quotient = endpoint_hstar_polynomial(left, right)
            expected = (
                is_rectangular(left)
                and is_rectangular(right)
                and left[0] == right[0]
            )
            if expected:
                expected_pairs += 1
            if (quotient is not None) != expected:
                raise AssertionError((left_width, left, right_width, right, quotient))
            if quotient is not None:
                polynomial_pairs += 1
                predicted = rectangular_formula(len(left), len(right), left[0])
                if quotient != predicted:
                    raise AssertionError((left, right, quotient, predicted))
    return tested, polynomial_pairs, expected_pairs


def verify_equal_width_extension(maximum_width: int = 11) -> tuple[int, int]:
    tested = 0
    polynomial_pairs = 0
    for width in range(1, maximum_width + 1):
        for left in partitions(width):
            for right in partitions(width):
                tested += 1
                quotient = endpoint_hstar_polynomial(left, right)
                expected = left == right and is_rectangular(left)
                if (quotient is not None) != expected:
                    raise AssertionError((width, left, right, quotient))
                polynomial_pairs += quotient is not None
    return tested, polynomial_pairs


def verify_one_sided_pole_orders(maximum_width: int = 11) -> tuple[int, int]:
    """Check exact cyclotomic pole orders for every one-sided type in range."""
    types_checked = 0
    root_orders_checked = 0
    for width in range(2, maximum_width + 1):
        identity = (1,) * width
        for nonidentity in partitions(width):
            if nonidentity == identity:
                continue
            numerator, denominator = endpoint_hstar_fraction(nonidentity, identity)
            period = 1
            for part in nonidentity:
                period = lcm(period, part)
            for root_order in divisors(period):
                factor = list(cyclotomic(root_order))
                residual_order = polynomial_valuation(
                    denominator, factor
                ) - polynomial_valuation(numerator, factor)
                expected = (
                    width
                    if root_order > 1
                    and any(part % root_order == 0 for part in nonidentity)
                    else 0
                )
                if residual_order != expected:
                    raise AssertionError(
                        (width, nonidentity, root_order, residual_order, expected)
                    )
                root_orders_checked += 1
            types_checked += 1
    return types_checked, root_orders_checked


def verify_scaling_identity(maximum_reduced_width: int = 5, maximum_scale: int = 4) -> int:
    checks = 0
    for left_width in range(1, maximum_reduced_width + 1):
        for right_width in range(1, maximum_reduced_width + 1):
            for left in partitions(left_width):
                for right in partitions(right_width):
                    base_num, base_den = endpoint_hstar_fraction(left, right)
                    for scale in range(2, maximum_scale + 1):
                        scaled_left = tuple(scale * part for part in left)
                        scaled_right = tuple(scale * part for part in right)
                        scaled_num, scaled_den = endpoint_hstar_fraction(
                            scaled_left, scaled_right
                        )
                        expected_num = poly_substitute_power(base_num, scale)
                        expected_den = poly_substitute_power(base_den, scale)
                        if poly_mul(scaled_num, expected_den) != poly_mul(
                            expected_num, scaled_den
                        ):
                            raise AssertionError((left, right, scale))
                        checks += 1
    return checks


def verify() -> dict[str, int | str]:
    direct_checks = verify_definition_level_counts()
    heterogeneous_pairs, heterogeneous_polynomial, expected_pairs = (
        verify_heterogeneous_classification()
    )
    equal_width_pairs, equal_width_polynomial = verify_equal_width_extension()
    one_sided_types, one_sided_root_orders = verify_one_sided_pole_orders()
    scaling_checks = verify_scaling_identity()
    if heterogeneous_polynomial != expected_pairs:
        raise AssertionError((heterogeneous_polynomial, expected_pairs))
    report: dict[str, int | str] = {
        "direct_fixed_count_checks": direct_checks,
        "equal_width_maximum": 11,
        "equal_width_pairs": equal_width_pairs,
        "equal_width_polynomial_pairs": equal_width_polynomial,
        "heterogeneous_maximum_width": 8,
        "heterogeneous_pairs": heterogeneous_pairs,
        "heterogeneous_polynomial_pairs": heterogeneous_polynomial,
        "one_sided_root_orders": one_sided_root_orders,
        "one_sided_types": one_sided_types,
        "scaling_identity_checks": scaling_checks,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "INDEPENDENT ENDPOINT-HADAMARD AUDIT PASSED; "
        f"direct_fixed_count_checks={report['direct_fixed_count_checks']}; "
        f"equal_width_pairs={report['equal_width_pairs']}; "
        f"equal_width_polynomial_pairs={report['equal_width_polynomial_pairs']}; "
        f"heterogeneous_pairs={report['heterogeneous_pairs']}; "
        f"heterogeneous_polynomial_pairs={report['heterogeneous_polynomial_pairs']}; "
        f"one_sided_types={report['one_sided_types']}; "
        f"one_sided_root_orders={report['one_sided_root_orders']}; "
        f"scaling_identity_checks={report['scaling_identity_checks']}; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
