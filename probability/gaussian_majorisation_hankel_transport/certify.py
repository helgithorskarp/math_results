#!/usr/bin/env python3
"""Exact finite polynomial witnesses for three-dimensional majorisation.

A positive or inconclusive result concerns ONLY the supplied polynomial.
Only CERTIFIED_COUNTEREXAMPLE establishes a failure of the conjecture.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial
import json
from pathlib import Path

from bounds import I, exp_negative, sqrt_integer


def rational(value):
    if type(value) is not int and not isinstance(value, (str, F)):
        raise ValueError("rationals must be integers or fraction strings")
    return F(value)


def distance_matrix(points):
    return [[sum((a - b)**2 for a, b in zip(x, y))
             for y in points] for x in points]


def parse_case(case):
    if not isinstance(case, dict):
        raise ValueError("input must be a JSON object")
    if case.get("dimension") != 3:
        raise ValueError("this checker requires dimension three")
    x = [[rational(c) for c in row] for row in case["x"]]
    y = [[rational(c) for c in row] for row in case["y"]]
    w = [rational(c) for c in case["weights"]]
    p = [rational(c) for c in case["polynomial_square_root"]]
    s = rational(case["variance"])
    if not x or len(x) != len(y) or len(x) != len(w):
        raise ValueError("inconsistent nonempty point/weight arrays")
    if any(len(row) != 3 for row in x + y):
        raise ValueError("each point must have three coordinates")
    if s <= 0 or any(a <= 0 for a in w) or sum(w) != 1:
        raise ValueError("positive variance and positive probability weights required")
    if not p or not any(p):
        raise ValueError("nonzero polynomial required")
    dx, dy = distance_matrix(x), distance_matrix(y)
    margins = [dx[i][j] - dy[i][j]
               for i in range(len(x)) for j in range(i)]
    if any(m < 0 for m in margins):
        raise ValueError("labelled map is not a contraction")
    return x, y, w, p, s, dx, dy, min(margins, default=F(0))


def compositions(total, size):
    if size == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, size - 1):
            yield (first,) + rest


def replica_histogram(distances, weights, k, variance):
    """Exact multinomial expansion before the common k^(-3/2) factor."""
    out = defaultdict(F)
    n = len(weights)
    for counts in compositions(k, n):
        coefficient = F(factorial(k))
        for weight, count in zip(weights, counts):
            coefficient *= weight**count / factorial(count)
        quadratic = sum(counts[i] * counts[j] * distances[i][j]
                        for i in range(n) for j in range(i))
        out[-quadratic / (2 * k * variance)] += coefficient
    return {exponent: value for exponent, value in out.items() if value}


def difference_histogram(dx, dy, w, k, s):
    result = defaultdict(F, replica_histogram(dy, w, k, s))
    for exponent, value in replica_histogram(dx, w, k, s).items():
        result[exponent] -= value
    return {exponent: value for exponent, value in result.items() if value}


def moment_gap(histogram, k, digits):
    if not histogram:
        return I.of(0)
    total = I.of(0)
    for exponent, coefficient in sorted(histogram.items()):
        total += coefficient * exp_negative(exponent, digits)
    return (total / (k * sqrt_integer(k, digits))).rounded(digits)


def square_coefficients(p):
    out = [F(0)] * (2 * len(p) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(p):
            out[i + j] += a * b
    return out


def evaluate_case(case, digits=70, max_states=250000):
    if type(digits) is not int or not 10 <= digits <= 1000:
        raise ValueError("precision must be an integer in 10..1000")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("workload limit must be a positive integer")
    x, y, w, p, s, dx, dy, margin = parse_case(case)
    maximum_k = 2 * len(p)
    states = 2 * sum(comb(k + len(w) - 1, len(w) - 1)
                     for k in range(2, maximum_k + 1))
    if states > max_states:
        raise ValueError("multinomial workload exceeds --max-states")
    moments, histograms = {}, {}
    for k in range(2, maximum_k + 1):
        histograms[k] = difference_histogram(dx, dy, w, k, s)
        moments[k] = moment_gap(histograms[k], k, digits)
    coefficients = square_coefficients(p)
    value = I.of(0)
    for j, coefficient in enumerate(coefficients):
        value += coefficient * moments[j + 2] / ((j + 1) * (j + 2))
    value = value.rounded(digits)
    if value.hi < 0:
        verdict = "CERTIFIED_COUNTEREXAMPLE"
    elif value.lo >= 0:
        verdict = "NO_NEGATIVE_WITNESS"
    else:
        verdict = "INCONCLUSIVE_PRECISION"
    return {
        "verdict": verdict,
        "meaning": "Only the supplied polynomial is tested; a positive result is not majorisation.",
        "dimension": 3,
        "atoms": len(w),
        "energy_degree": maximum_k,
        "precision_digits": digits,
        "multinomial_states": states,
        "minimum_squared_distance_margin": str(margin),
        "energy_gap_interval": value.strings(digits),
        "moment_gap_intervals": {str(k): v.strings(24) for k, v in moments.items()},
        "energy_coefficients_from_degree_two": [
            str(c / ((j + 1) * (j + 2))) for j, c in enumerate(coefficients)
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--digits", type=int, default=70)
    parser.add_argument("--max-states", type=int, default=250000)
    args = parser.parse_args()
    if not 10 <= args.digits <= 1000 or args.max_states < 1:
        parser.error("precision must be 10..1000 and workload limit positive")
    try:
        case = json.loads(args.input.read_text())
        result = evaluate_case(case, args.digits, args.max_states)
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
