#!/usr/bin/env python3
"""Exact sufficient hypotheses for PROOF.md, not a numerical hinge test.

CPython 3.11+, standard library only. Two independent finite rational laws
are accepted. A failed sufficient condition means UNRESOLVED.
"""

import argparse
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def rational(value):
    """No binary floats; a dyadic object avoids enormous decimal inputs."""
    if isinstance(value, Fraction):
        return value
    if type(value) is int or type(value) is str:
        return Fraction(value)
    if type(value) is dict and set(value) == {"numerator", "negative_exponent"}:
        n = value["numerator"]
        if type(n) is not int:
            raise ValueError("dyadic numerator must be an integer")
        e = integer(value["negative_exponent"], "negative_exponent")
        return Fraction(n, 1 << e)
    raise ValueError("expected an exact integer, rational string, or dyadic object")


def schedule(R, j):
    integer(R, "R", 1)
    integer(j, "j")
    Z = j + 3 + R * R
    S = 4 * R * (1 << j) * (5 * R * R + 2 * j + 4)
    m = (S + R) ** 2
    B = m + j + 5 * Z + R * R + 14
    return {
        "R": R, "j": j, "Z": Z, "S": S, "m": m, "B": B,
        "target_radius_negative_exponent": B + 1,
        "hinge_margin_negative_exponent": B + 1,
        "contraction_damping": {"negative_exponent": B + 2, "divisor": R},
    }


def ceil_log2_positive(q):
    """Least integer k with q <= 2**k; never use logarithms or floats."""
    if q <= 0:
        raise ValueError("q must be positive")
    n, d = q.numerator, q.denominator
    k = n.bit_length() - d.bit_length()
    fits = n <= (d << k) if k >= 0 else (n << -k) <= d
    return k if fits else k + 1


def le_negative_power(q, exponent):
    """q <= 2**(-exponent), without constructing that possibly huge power."""
    integer(exponent, "exponent")
    if q < 0:
        raise ValueError("q must be nonnegative")
    return q == 0 or ceil_log2_positive(q) <= -exponent


def centered_law(data):
    if type(data) is not dict or set(data) != {"points", "weights"}:
        raise ValueError("a law must contain exactly points and weights")
    if not isinstance(data["points"], (list, tuple)) or not isinstance(data["weights"], (list, tuple)):
        raise ValueError("points and weights must be lists")
    points, weights = data["points"], data["weights"]
    if not points or len(points) != len(weights):
        raise ValueError("equal nonzero point and weight counts required")
    parsed = []
    for p, w in zip(points, weights):
        if not isinstance(p, (list, tuple)) or len(p) != 3:
            raise ValueError("each point must have three coordinates")
        q, mass = tuple(rational(x) for x in p), rational(w)
        if mass < 0:
            raise ValueError("negative probability weight")
        parsed.append((q, mass))
    if sum(w for _, w in parsed) != 1:
        raise ValueError("weights must sum exactly to one")
    parsed = [(p, w) for p, w in parsed if w > 0]
    mean = tuple(sum(w * p[k] for p, w in parsed) for k in range(3))
    return [(tuple(p[k] - mean[k] for k in range(3)), w) for p, w in parsed]


def determinant(matrix):
    n = len(matrix)
    total = Fraction(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        product = Fraction(-1 if inversions % 2 else 1)
        for i in range(n):
            product *= matrix[i][perm[i]]
        total += product
    return total


def psd_three(matrix):
    # A real symmetric matrix is PSD iff EVERY principal minor is nonnegative.
    if any(matrix[i][j] != matrix[j][i] for i in range(3) for j in range(3)):
        raise ValueError("PSD test requires a symmetric matrix")
    for size in range(1, 4):
        for inds in combinations(range(3), size):
            if determinant([[matrix[i][j] for j in inds] for i in inds]) < 0:
                return False
    return True


def finite_guard(source, target, *, variance=1, R=1, j=2):
    parameters = schedule(R, j)
    s = rational(variance)
    if s <= 0:
        raise ValueError("variance must be positive")
    xlaw, ylaw = centered_law(source), centered_law(target)
    source_radius_ok = all(sum(v * v for v in x) <= s * R * R for x, _ in xlaw)
    covariance = [[sum(w * x[i] * x[k] for x, w in xlaw) / s
                   for k in range(3)] for i in range(3)]
    kappa = Fraction(1, 1 << j)
    residual = [[covariance[i][k] - (kappa if i == k else 0)
                 for k in range(3)] for i in range(3)]
    covariance_ok = psd_three(residual)
    target_radius_squared = max(sum(v * v for v in y) / s for y, _ in ylaw)
    target_radius_ok = le_negative_power(target_radius_squared, 2 * (parameters["B"] + 1))
    guards = {"source_radius": source_radius_ok, "source_covariance": covariance_ok,
              "target_radius": target_radius_ok}
    return {
        "status": "CERTIFIED" if all(guards.values()) else "UNRESOLVED",
        "claim": "all_threshold_gaussian_majorisation",
        "guards": guards, "schedule": parameters,
        "positive_source_atoms": len(xlaw), "positive_target_atoms": len(ylaw),
        "trust": "conditional on the written analytic proof; no Gaussian quadrature",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("schedule")
    p.add_argument("R", type=int)
    p.add_argument("j", type=int)
    p = subs.add_parser("check")
    p.add_argument("input", type=Path)
    args = parser.parse_args()
    if args.command == "schedule":
        result = schedule(args.R, args.j)
    else:
        request = json.loads(args.input.read_text())
        if type(request) is not dict or not {"source", "target"} <= set(request) or set(request) - {"source", "target", "variance", "R", "j"}:
            raise ValueError("invalid request fields")
        result = finite_guard(**request)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
