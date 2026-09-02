#!/usr/bin/env python3
"""Exact Lucas--Bergeron--Vessenes verification via Lucas atoms.

A homogeneous symmetric polynomial of degree D is stored losslessly after
setting t=1, as its D+1 coefficients in q.  All arithmetic is over Python's
arbitrary-precision integers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path


Poly = tuple[int, ...]


def add(left: Poly, right: Poly) -> Poly:
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    )


def subtract(left: Poly, right: Poly) -> Poly:
    assert len(left) == len(right)
    return tuple(x - y for x, y in zip(left, right, strict=True))


def multiply(left: Poly, right: Poly) -> Poly:
    product = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            product[i + j] += x * y
    return tuple(product)


def shift(poly: Poly) -> Poly:
    return (0,) + poly


def divide_exact(numerator: Poly, denominator: Poly) -> Poly:
    """Divide monic integer polynomials, stored from low to high degree."""
    remainder = list(numerator)
    while len(remainder) > 1 and remainder[-1] == 0:
        remainder.pop()
    divisor = list(denominator)
    while len(divisor) > 1 and divisor[-1] == 0:
        divisor.pop()
    assert divisor[-1] == 1
    assert len(remainder) >= len(divisor)
    quotient = [0] * (len(remainder) - len(divisor) + 1)
    for position in range(len(quotient) - 1, -1, -1):
        coefficient = remainder[position + len(divisor) - 1]
        quotient[position] = coefficient
        for j, value in enumerate(divisor):
            remainder[position + j] -= coefficient * value
    assert not any(remainder)
    return tuple(quotient)


def lucas_integers(limit: int) -> list[Poly]:
    """Return L_m(q,1), where L_0=0, L_1=1 and L_{m+1}=(q+1)L_m+qL_{m-1}."""
    values: list[Poly] = [(0,)]
    if limit == 0:
        return values
    values.append((1,))
    for m in range(1, limit):
        values.append(add(multiply((1, 1), values[m]), shift(values[m - 1])))
    return values


def lucas_atoms(limit: int) -> list[Poly]:
    """Return anti-cyclotomic atoms A_m(q,1) through m=limit."""
    lucas = lucas_integers(limit)
    atoms: list[Poly] = [(1,)] * (limit + 1)
    for m in range(2, limit + 1):
        proper_divisor_product: Poly = (1,)
        for divisor in range(2, m):
            if m % divisor == 0:
                proper_divisor_product = multiply(
                    proper_divisor_product, atoms[divisor]
                )
        atoms[m] = divide_exact(lucas[m], proper_divisor_product)
        assert atoms[m] == atoms[m][::-1]
    return atoms


def lucas_binomial(n: int, k: int, atoms: list[Poly]) -> Poly:
    """Compute the Lucas binomial {n choose k}(q,1) by atom carries."""
    assert 0 <= k <= n
    k = min(k, n - k)
    result: Poly = (1,)
    degree = 0
    for divisor in range(2, n + 1):
        exponent = n // divisor - k // divisor - (n - k) // divisor
        assert exponent in (0, 1)
        if exponent:
            result = multiply(result, atoms[divisor])
            degree += len(atoms[divisor]) - 1
    assert degree == k * (n - k)
    assert result == result[::-1]
    return result


def schur_coefficients(poly: Poly) -> Poly:
    """Expand a symmetric degree-D polynomial in s_(D-i,i)(q,t)."""
    assert poly == poly[::-1]
    middle = (len(poly) - 1) // 2
    return tuple(poly[i] - (poly[i - 1] if i else 0) for i in range(middle + 1))


def factor_pairs(product: int) -> list[tuple[int, int]]:
    return [
        (factor, product // factor)
        for factor in range(1, isqrt(product) + 1)
        if product % factor == 0
    ]


def update_digest(
    digest: hashlib._Hash,
    product: int,
    quadruple: tuple[int, int, int, int],
    normalized: Poly,
) -> None:
    a, b, c, d = quadruple
    record = (
        f"{product}|{a}|{b}|{c}|{d}|"
        + ",".join(str(value) for value in normalized)
        + "\n"
    )
    digest.update(record.encode("ascii"))


def verify(max_product: int) -> dict[str, object]:
    assert max_product >= 4
    atoms = lucas_atoms(max_product + 1)
    cache: dict[tuple[int, int], Poly] = {}

    def choose(n: int, k: int) -> Poly:
        key = (n, min(k, n - k))
        if key not in cache:
            cache[key] = lucas_binomial(n, k, atoms)
        return cache[key]

    digest = hashlib.sha256()
    comparisons = 0
    positive_orientation = 0
    negative_orientation = 0
    maximum_bits = 0
    for product in range(1, max_product + 1):
        pairs = factor_pairs(product)
        for outer_index, (a, d) in enumerate(pairs):
            for b, c in pairs[outer_index + 1 :]:
                assert 1 <= a < b <= c < d and a * d == b * c == product
                difference = subtract(choose(b + c, b), choose(a + d, a))
                schur = schur_coefficients(difference)
                sign = 1 if a % 2 == 1 else -1
                normalized = tuple(sign * value for value in schur)
                # This also verifies the sign-rigidity lemma instance by instance.
                assert not any(normalized[: a + 1])
                assert normalized[a + 1] == 1
                assert all(value >= 0 for value in normalized)
                update_digest(digest, product, (a, b, c, d), normalized)
                comparisons += 1
                positive_orientation += sign == 1
                negative_orientation += sign == -1
                maximum_bits = max(
                    maximum_bits,
                    max((abs(value).bit_length() for value in schur), default=0),
                )

    # Exact b=2 identity checks; the proof in README.md is symbolic and unbounded.
    for c in range(2, max_product // 2 + 1):
        left = subtract(choose(c + 2, 2), choose(2 * c + 1, 1))
        right = (0, 0) + choose(c, 2) + (0, 0)
        assert left == right

    return {
        "schema": "lucas-bergeron-vessenes-v1",
        "algorithm": "anti-cyclotomic-atom-factorization",
        "max_product": max_product,
        "comparison_count": comparisons,
        "positive_orientation_count": positive_orientation,
        "negative_orientation_count": negative_orientation,
        "maximum_schur_coefficient_bits": maximum_bits,
        "records_sha256": digest.hexdigest(),
        "all_sign_normalized_schur_nonnegative": True,
        "all_first_nonzero_coefficients_verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-product", type=int, default=500)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    arguments = parser.parse_args()
    result = verify(arguments.max_product)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.expect is not None:
        assert json.loads(arguments.expect.read_text(encoding="utf-8")) == result
    if arguments.output is not None:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
