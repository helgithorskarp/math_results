#!/usr/bin/env python3
"""Exact supplementary audits for the global hinge criterion.

No Gaussian-contraction counterexample is asserted or searched for here.
Run --check to compare the deterministic report with EXPECTED.json.
Only Python integers and Fraction are used for mathematical checks.
"""
from argparse import ArgumentParser
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement, permutations
from math import comb
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(x):
    require(type(x) in (int, Q), "exact rational input required")
    return Q(x)


def add(p, q):
    """Sparse bivariate polynomials: exponents are (power of n, power of t)."""
    out = dict(p)
    for exponent, value in q.items():
        out[exponent] = out.get(exponent, Q(0)) + value
    return {e: c for e, c in out.items() if c}


def scale(p, c):
    return {e: c * v for e, v in p.items() if c * v}


def mul(p, q):
    out = {}
    for (a, b), x in p.items():
        for (c, d), y in q.items():
            e = (a + c, b + d)
            out[e] = out.get(e, Q(0)) + x * y
    return {e: c for e, c in out.items() if c}


def beta_polynomial(n, k):
    require(type(n) is int and type(k) is int and 0 <= k <= n,
            "invalid beta indices")
    return {k + j: Q((n + 1) * comb(n, k) * (-1)**j * comb(n - k, j))
            for j in range(n - k + 1)}


def integrate_product(p, q):
    return sum((a * b / Q(i + j + 1)
                for i, a in p.items() for j, b in q.items()), Q(0))


def moment(p, j):
    return sum((v / Q(i + j + 1) for i, v in p.items()), Q(0))


def beta_row(moments, n):
    require(type(n) is int and n >= 0 and len(moments) >= n + 1,
            "insufficient moments or invalid degree")
    a = [rational(x) for x in moments[:n + 1]]
    return [(n + 1) * comb(n, k) * sum(
        ((-1)**j * comb(n - k, j) * a[k + j] for j in range(n - k + 1)),
        Q(0)) for k in range(n + 1)]


def beta_interval_row(moment_bounds, n):
    """Rigorous rational propagation of externally certified a_j intervals.

    This does not certify that the supplied moments come from Gaussian data.
    """
    require(type(n) is int and n >= 0 and len(moment_bounds) >= n + 1,
            "insufficient intervals or invalid degree")
    bounds = []
    for pair in moment_bounds[:n + 1]:
        require(len(pair) == 2, "interval needs two endpoints")
        lo, hi = map(rational, pair)
        require(lo <= hi, "reversed interval")
        bounds.append((lo, hi))
    out = []
    for k in range(n + 1):
        lo = hi = Q(0)
        for j in range(n - k + 1):
            c = (n + 1) * comb(n, k) * (-1)**j * comb(n - k, j)
            left, right = bounds[k + j]
            lo += c * (left if c >= 0 else right)
            hi += c * (right if c >= 0 else left)
        out.append((lo, hi))
    return out


def defect_lower(row):
    require(bool(row), "empty beta row")
    return max(Q(0), -min(row))


def algebra_audit():
    one, n, t = {(0, 0): Q(1)}, {(1, 0): Q(1)}, {(0, 1): Q(1)}
    # The numerator of E(V-t)^2 after multiplying by (n+2)(n+3).
    ej2plus = add(add(mul(mul(n, add(n, scale(one, -1))), mul(t, t)),
                     scale(mul(n, t), 4)), scale(one, 2))
    term2 = scale(mul(mul(t, add(mul(n, t), one)),
                      add(n, scale(one, 3))), -2)
    term3 = mul(mul(t, t), mul(add(n, scale(one, 2)), add(n, scale(one, 3))))
    variance = add(add(ej2plus, term2), term3)
    expected = scale(add(one, mul(mul(add(n, scale(one, -3)), t),
                                 add(one, scale(t, -1)))), 2)
    require(variance == expected, "generic second-moment identity")

    # Positive, negative, mixed and boundary-zero polynomial controls.
    polynomials = [
        {0: Q(1)}, {1: Q(1), 2: Q(-1)},
        {1: Q(-1), 2: Q(1)},
        {1: Q(-1, 3), 2: Q(4, 3), 3: Q(-1)},
        {0: Q(-2), 1: Q(3), 4: Q(-5, 7)},
    ]
    integration_checks = elevation_checks = normalization_checks = 0
    for degree in range(17):
        weights = [beta_polynomial(degree, k) for k in range(degree + 1)]
        for w in weights:
            require(integrate_product(w, {0: Q(1)}) == 1, "beta normalization")
            normalization_checks += 1
        for p in polynomials:
            moments = [moment(p, j) for j in range(degree + 2)]
            row, nxt = beta_row(moments, degree), beta_row(moments, degree + 1)
            for k, value in enumerate(row):
                require(value == integrate_product(weights[k], p),
                        "finite difference versus direct integration")
                integration_checks += 1
                elevated = (Q(degree + 1 - k, degree + 2) * nxt[k]
                            + Q(k + 1, degree + 2) * nxt[k + 1])
                require(value == elevated, "degree elevation")
                elevation_checks += 1
            require(defect_lower(row) <= defect_lower(nxt), "monotone defect")

    # H=u(1-u)(u-1/3) has every monomial moment positive but a negative beta test.
    mixed = polynomials[3]
    moments = [moment(mixed, j) for j in range(19)]
    for j, a in enumerate(moments):
        require(a == Q(2 * (j + 1), 3 * (j + 2) * (j + 3) * (j + 4)) and a > 0,
                "positive monomial-moment control")
    require(beta_row(moments, 3)[0] == Q(-2, 315), "negative finite witness")
    require(all(x >= 0 for n in range(3) for x in beta_row(moments, n)),
            "first negative degree")
    # These H controls are abstract signed polynomials, not Gaussian pairs.
    negative = polynomials[2]
    m = [moment(negative, j) for j in range(65)]
    for degree in range(65):
        d = defect_lower(beta_row(m, degree))
        require(0 <= d <= Q(1, 4), "exact control maximum")
        require((Q(1, 4) - d)**4 * (degree + 2) <= 3**4,
                "global error normalization on a negative control")

    # Sign-aware interval propagation, checked at every corner of a small box.
    eps = Q(1, 100000)
    bounds = [(x - eps, x + eps) for x in moments[:4]]
    enclosing = beta_interval_row(bounds, 3)
    for mask in range(16):
        corner = [pair[(mask >> j) & 1] for j, pair in enumerate(bounds)]
        row = beta_row(corner, 3)
        require(all(lo <= b <= hi for b, (lo, hi) in zip(row, enclosing)),
                "interval enclosure")
    require(enclosing[0][1] < 0, "interval negative witness")
    return {
        "generic_bivariate_variance_identity": True,
        "beta_normalizations": normalization_checks,
        "integration_comparisons": integration_checks,
        "degree_elevations": elevation_checks,
        "negative_control_degrees": 65,
        "positive_monomial_mixed_control": {
            "formula": "a_j=2(j+1)/(3(j+2)(j+3)(j+4))",
            "first_negative_beta": [3, 0, "-2/315"],
            "not_a_gaussian_counterexample": True,
        },
        "interval_corner_checks": 16,
        "negative_interval": list(map(str, enclosing[0])),
    }


def finite_coupling_audit():
    # Four ordered scalar levels; equal atoms permit denominator-five laws.
    size = 5
    laws = list(combinations_with_replacement(range(4), size))
    assignments = {b: set(permutations(b)) for b in laws}
    histogram = [0] * (size + 1)
    pairs = 0
    for a in laws:
        for b in laws:
            defect = max(sum(x <= t for x in b) - sum(x <= t for x in a)
                         for t in range(4))
            shifted = [b[(j + defect) % size] for j in range(size)]
            cyclic_cost = sum(x > y for x, y in zip(a, shifted))
            optimum = min(sum(x > y for x, y in zip(a, perm))
                          for perm in assignments[b])
            require(cyclic_cost == defect == optimum, "optimal scalar coupling")
            histogram[defect] += 1
            pairs += 1
    require(pairs == 3136 and histogram[0] > 0 and histogram[5] > 0,
            "finite coupling coverage")
    return {"support_levels": 4, "common_denominator": size,
            "marginals": len(laws), "ordered_pairs": pairs,
            "failure_count_histogram": histogram,
            "cyclic_matches_exhaustive_assignment_optimum": True}


def invalid_controls():
    bad_calls = [
        lambda: beta_row([Q(1)], 2),
        lambda: beta_polynomial(2, 3),
        lambda: beta_row([0.1], 0),
        lambda: beta_interval_row([(Q(2), Q(1))], 0),
        lambda: require(Q(-2, 315) >= 0, "false positive-sign claim"),
    ]
    rejected = 0
    for call in bad_calls:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("invalid control accepted")
    return rejected


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = {"schema": 1, "arithmetic": "integers and fractions.Fraction",
              "algebra": algebra_audit(), "coupling": finite_coupling_audit(),
              "invalid_controls_rejected": invalid_controls()}
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_bytes()
        require(encoded == expected, "EXPECTED.json mismatch")
        print("GLOBAL_CRITERION_EXACT_AUDITS_PASS " + sha256(encoded).hexdigest())
    else:
        print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
