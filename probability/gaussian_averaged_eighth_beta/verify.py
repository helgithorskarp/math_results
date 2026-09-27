#!/usr/bin/env python3
"""Exact scalar certificate for the averaged eighth-beta argument.

Python 3.11+, standard library only. No floating-point arithmetic, external
inputs, or assertion statements are used. See PROOF.md for the analytic
reduction; this program is not a proof-assistant formalization of that part.
"""

from fractions import Fraction as F
from hashlib import sha256
from math import comb, isqrt
from pathlib import Path
import json
import sys


DEGREE = 8
ROOT_DENOMINATOR = 10000
SUBINTERVALS = 8


def require(condition, message):
    if not condition:
        raise ValueError(message)


def root_enclosures():
    out = []
    for n in range(2, 11):
        k = isqrt(n * ROOT_DENOMINATOR**2)
        lo = F(k, ROOT_DENOMINATOR)
        hi = lo if lo * lo == n else F(k + 1, ROOT_DENOMINATOR)
        require(0 <= lo <= hi and lo * lo <= n <= hi * hi,
                "Invalid square-root enclosure")
        out.append((lo, hi))
    return out


def rational_lower_polynomial(roots):
    # For u >= 0, lower each signed monomial separately.
    out = [comb(DEGREE, j) * (lo if j % 2 == 0 else -hi)
           for j, (lo, hi) in enumerate(roots)]
    out[0] -= F(19, 100)
    out[1] += F(4, 5)
    out[2] -= F(1, 2)
    return out


def power_to_bernstein(power):
    n = len(power) - 1
    return [sum((power[k] * F(comb(i, k), comb(n, k))
                 for k in range(i + 1)), F(0)) for i in range(n + 1)]


def direct_interval(power, left, width):
    # Substitute u = left + width*t in power basis, then change basis.
    n = len(power) - 1
    local = [sum((power[j] * comb(j, k) * left**(j-k) * width**k
                  for j in range(k, n + 1)), F(0)) for k in range(n + 1)]
    return power_to_bernstein(local)


def split_half(control):
    # Independent subdivision using only the Bernstein control polygon.
    rows = [list(control)]
    while len(rows[-1]) > 1:
        r = rows[-1]
        rows.append([(r[i] + r[i+1]) / 2 for i in range(len(r) - 1)])
    return [r[0] for r in rows], [r[-1] for r in reversed(rows)]


def de_casteljau_intervals(power):
    intervals = [power_to_bernstein(power)]
    for _ in range(3):
        intervals = [child for parent in intervals for child in split_half(parent)]
    return intervals


def polynomial_value(power, x):
    value = F(0)
    for c in reversed(power):
        value = value*x + c
    return value


def bernstein_value(control, t):
    n = len(control) - 1
    return sum((c * comb(n, i) * t**i * (1-t)**(n-i)
                for i, c in enumerate(control)), F(0))


def check_certificate(power, intervals):
    require(len(intervals) == SUBINTERVALS, "Incomplete interval coverage")
    for k, control in enumerate(intervals):
        require(len(control) == DEGREE + 1, "Incomplete Bernstein row")
        require(control == direct_interval(power, F(k, 8), F(1, 8)),
                "Incorrect Bernstein coefficients")
        require(min(control) > 0, "Scalar lower polynomial not certified positive")


def outer(v):
    return [[x*y for y in v] for x in v]


def variance_matrix(count, ambient):
    return [[(F(int(i == j)) - F(1, count)) if max(i, j) < count else F(0)
             for j in range(ambient)] for i in range(ambient)]


def check_variance_identities():
    # Quadratic coefficient matrices in one coordinate; summing coordinates
    # proves the same identities in any finite Euclidean dimension.
    u3 = [F(-1, 2), F(-1, 2), F(1)]
    base3, next3, uu3 = variance_matrix(2, 3), variance_matrix(3, 3), outer(u3)
    for i in range(3):
        for j in range(3):
            require(next3[i][j] == base3[i][j] + F(2, 3)*uu3[i][j],
                    "One-addition variance identity failed")
    u = [F(-1, 2), F(-1, 2), F(1), F(0)]
    v = [F(-1, 2), F(-1, 2), F(0), F(1)]
    uu, vv, ww = outer(u), outer(v), outer([x+y for x, y in zip(u, v)])
    base4, next4 = variance_matrix(2, 4), variance_matrix(4, 4)
    for i in range(4):
        for j in range(4):
            require(next4[i][j] == base4[i][j] + uu[i][j] + vv[i][j] - ww[i][j]/4,
                    "Two-addition variance identity failed")
    return 9 + 16


def check_normalization():
    # In the replica formula, separate the factor m^(-3/2) from its
    # rational multiplier. Dividing d_m by m(m-1) leaves 1/(4s*m).
    for m in range(2, 11):
        differentiated_pair_factor = F(comb(m, 2), 2*m)
        require(differentiated_pair_factor == F(m-1, 4), "Pair factor failed")
        require(differentiated_pair_factor / (m*(m-1)) == F(1, 4*m),
                "Moment normalization failed")
        require(F(m) * F(1, m**3)**2 == F(1, m**5), "Lift exponent failed")
    eta_coefficients = [F(19, 100), -F(4, 5), F(1, 2)]
    B_coefficients = [c/F((i+2)**3) for i, c in enumerate(eta_coefficients)]
    require(B_coefficients == [F(19, 800), -F(4, 135), F(1, 128)],
            "Quadratic-minorant conversion failed")
    h1 = sum(B_coefficients, F(0))
    derivative_upper = -F(4, 135) + F(3, 128)
    require(h1 == F(167, 86400) and derivative_upper == -F(107, 17280),
            "Final cubic sign failed")
    b_over_B2_div_s = F(9, 4)*h1
    require(b_over_B2_div_s == F(167, 38400), "Beta normalization failed")
    # d2 = B2/(8*sqrt(2)*s). Record the rational coefficient of sqrt(2)*d2.
    require(8*b_over_B2_div_s == F(167, 4800), "Second-moment conversion failed")
    return h1, derivative_upper, b_over_B2_div_s


def corruption_controls(power, intervals):
    bad = [list(row) for row in intervals]
    bad[3][4] += F(1, 1000000)
    failures = 0
    for candidate in [bad, intervals[:-1]]:
        try:
            check_certificate(power, candidate)
        except ValueError:
            failures += 1
    require(failures == 2, "Corrupt certificate accepted")
    return failures


def certificate():
    roots = root_enclosures()
    power = rational_lower_polynomial(roots)
    direct = [direct_interval(power, F(i, 8), F(1, 8)) for i in range(8)]
    alternate = de_casteljau_intervals(power)
    require(direct == alternate, "Subdivision algorithms disagree")
    check_certificate(power, direct)
    # Nine distinct rational evaluations per subinterval independently check
    # degree-eight polynomial equality, not merely a few sample signs.
    identity_evaluations = 0
    for k, control in enumerate(direct):
        for j in range(9):
            t = F(j, 8)
            require(polynomial_value(power, F(k, 8)+t/8) == bernstein_value(control, t),
                    "Polynomial identity audit failed")
            identity_evaluations += 1
    h1, derivative_upper, beta_constant = check_normalization()
    canonical = json.dumps([[str(x) for x in row] for row in direct],
                           separators=(",", ":")).encode()
    return {
        "claim": "P8(u) >= 19/100 - 4*u/5 + u^2/2 for 0 <= u <= 1",
        "arithmetic": "Python arbitrary-precision integers and Fraction; no floating point",
        "root_denominator": ROOT_DENOMINATOR,
        "root_enclosures": [{"n": n, "lower": str(lo), "upper": str(hi)}
                            for n, (lo, hi) in enumerate(roots, start=2)],
        "rational_lower_power_coefficients": [str(x) for x in power],
        "closed_subintervals": [[str(F(i, 8)), str(F(i+1, 8))] for i in range(8)],
        "bernstein_degree": DEGREE,
        "positive_coefficients": 72,
        "interval_minima": [str(min(row)) for row in direct],
        "global_coefficient_minimum": str(min(map(min, direct))),
        "all_coefficients_sha256": sha256(canonical).hexdigest(),
        "de_casteljau_entrywise_agreement": True,
        "exact_polynomial_identity_evaluations": identity_evaluations,
        "variance_matrix_entries_checked": check_variance_identities(),
        "corruptions_rejected": corruption_controls(power, direct),
        "h_at_one": str(h1),
        "h_derivative_upper": str(derivative_upper),
        "b80_lower_coefficient_of_B2_over_s": str(beta_constant),
        "b80_lower_coefficient_of_sqrt2_d2": "167/4800",
        "scope": "Exact scalar premise and algebra audit; analytic Jensen/lift proof in PROOF.md",
        "full_majorisation_proved": False,
    }


def main():
    require(sys.argv[1:] in ([], ["--emit"]), "Usage: python3 verify.py [--emit]")
    result = certificate()
    if sys.argv[1:] == ["--emit"]:
        print(json.dumps(result, indent=2))
        return
    expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
    require(result == expected, "Expected certificate mismatch")
    print(json.dumps({
        "status": "PASS",
        "positive_bernstein_coefficients": result["positive_coefficients"],
        "minimum": result["global_coefficient_minimum"],
        "two_subdivision_algorithms_agree": True,
        "b80_lower_bound": "167*sqrt(2)*d2/4800",
        "independent_review": "pending",
        "full_majorisation_proved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
