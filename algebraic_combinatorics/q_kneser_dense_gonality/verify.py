#!/usr/bin/env python3
"""Exact arithmetic audit for the q-Kneser half-density theorem.

Only prime-power q correspond to graphs over finite fields, but the Gaussian
identities and inequalities are checked for every integer q in the requested
range. The universal theorem is proved in THEOREM.md, not by this finite run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction


def gaussian_recurrence(n: int, k: int, q: int) -> int:
    """Return [n choose k]_q by the recurrence used in the proof."""
    if q < 2 or n < 0 or k < 0 or k > n:
        raise ValueError("require q>=2 and 0<=k<=n")
    row = [1]
    for m in range(1, n + 1):
        new = [1]
        for j in range(1, m):
            left = row[j - 1]
            right = row[j] if j < len(row) else 0
            new.append(left + q**j * right)
        new.append(1)
        row = new
    return row[k]


def gaussian_product(n: int, k: int, q: int) -> int:
    """Return [n choose k]_q from its defining exact product."""
    if q < 2 or n < 0 or k < 0 or k > n:
        raise ValueError("require q>=2 and 0<=k<=n")
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for i in range(k):
        numerator *= q ** (n - i) - 1
        denominator *= q ** (k - i) - 1
    quotient, remainder = divmod(numerator, denominator)
    if remainder:
        raise ArithmeticError("Gaussian product did not divide exactly")
    return quotient


def q_kneser_counts(q: int, n: int, r: int) -> tuple[int, int, int, int]:
    """Return (vertices, degree, independence number, predicted value)."""
    if n < 2 * r or r < 1:
        raise ValueError("require n>=2r>=2")
    vertices = gaussian_recurrence(n, r, q)
    degree = q ** (r * r) * gaussian_recurrence(n - r, r, q)
    independence = gaussian_recurrence(n - 1, r - 1, q)
    value = q**r * gaussian_recurrence(n - 1, r, q)
    if vertices - independence != value:
        raise AssertionError("Gaussian recurrence identity failed")
    return vertices, degree, independence, value


def is_exception(q: int, n: int, r: int) -> bool:
    return q == 2 and n == 2 * r and r >= 2


def audit(max_q: int, max_r: int, max_excess: int) -> dict[str, object]:
    if max_q < 2 or max_r < 1 or max_excess < 0:
        raise ValueError("invalid audit bounds")

    records: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    positive_margins: list[int] = []
    exceptions = 0

    for q in range(2, max_q + 1):
        for r in range(1, max_r + 1):
            for excess in range(max_excess + 1):
                n = 2 * r + excess
                vertices, degree, independence, value = q_kneser_counts(q, n, r)
                product_vertices = gaussian_product(n, r, q)
                product_degree = q ** (r * r) * gaussian_product(n - r, r, q)
                if (vertices, degree) != (product_vertices, product_degree):
                    raise AssertionError("recurrence/product disagreement")

                dense = 2 * degree > vertices
                expected_dense = not is_exception(q, n, r)
                margin = 2 * degree - vertices
                ratio = Fraction(degree, vertices)
                record = {
                    "q": q,
                    "n": n,
                    "r": r,
                    "N": vertices,
                    "d": degree,
                    "alpha": independence,
                    "N_minus_alpha": value,
                    "ratio": f"{ratio.numerator}/{ratio.denominator}",
                    "margin_2d_minus_N": margin,
                    "dense": dense,
                    "expected_dense": expected_dense,
                }
                records.append(record)
                if dense != expected_dense:
                    failures.append(record)
                if dense:
                    positive_margins.append(margin)
                else:
                    exceptions += 1

    canonical = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    instances = {}
    for q, n, r in ((2, 5, 2), (2, 4, 2), (3, 4, 2)):
        N, d, alpha, value = q_kneser_counts(q, n, r)
        instances[f"q={q},n={n},r={r}"] = {
            "N": N,
            "d": d,
            "alpha": alpha,
            "N_minus_alpha": value,
            "dense": 2 * d > N,
        }

    return {
        "bounds": {
            "q": [2, max_q],
            "r": [1, max_r],
            "excess_n_minus_2r": [0, max_excess],
        },
        "cases_checked": len(records),
        "classification_failures": len(failures),
        "excluded_binary_middle_cases": exceptions,
        "minimum_positive_margin_2d_minus_N": min(positive_margins),
        "known_instances": instances,
        "records_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q", type=int, default=13)
    parser.add_argument("--max-r", type=int, default=8)
    parser.add_argument("--max-excess", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(audit(args.max_q, args.max_r, args.max_excess), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
