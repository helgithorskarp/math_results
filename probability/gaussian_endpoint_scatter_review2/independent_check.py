"""Independent exact check of the two-point endpoint-scatter obstruction.

This program deliberately does not read the author's certificate or checker.
It reconstructs the finite Laplace spectrum from the binomial expansion of
the two translated Gaussians, uses fixed rational square-root brackets, and
checks both the published derivative witness and a smaller-order refinement.
"""

from fractions import Fraction as Q
from math import comb, isqrt
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# Independently chosen six-decimal rational brackets.  Their validity is
# checked below by squaring, so no floating-point value is trusted.
ROOT_BRACKETS = {
    1: (Q(1), Q(1)),
    2: (Q(1414213, 10**6), Q(1414214, 10**6)),
    3: (Q(1732050, 10**6), Q(1732051, 10**6)),
    5: (Q(2236067, 10**6), Q(2236068, 10**6)),
    6: (Q(2449489, 10**6), Q(2449490, 10**6)),
    7: (Q(2645751, 10**6), Q(2645752, 10**6)),
}


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def squarefree_part(n):
    factor = 1
    for candidate in range(1, isqrt(n) + 1):
        if n % (candidate * candidate) == 0:
            factor = candidate
    return factor, n // (factor * factor)


def add(vector, radicand, coefficient):
    vector[radicand] = vector.get(radicand, Q(0)) + coefficient
    if vector[radicand] == 0:
        del vector[radicand]


def spectrum():
    """Return rate -> coefficients in the basis sqrt(d), all exactly.

    Completing the square in the m-fold Gaussian product gives rate
    2*r*(m-r)/m.  Rationalizing 1/m^(3/2) gives the coefficient below.
    """
    answer = {}
    binomial_terms = 0
    for m in range(2, 10):
        factor, radicand = squarefree_part(m)
        coefficient = Q(
            8 * (-1) ** (m - 2) * comb(7, m - 2) * factor,
            m**3 * (m - 1),
        )
        add(answer.setdefault(Q(0), {}), radicand, coefficient)
        for r in range(m + 1):
            rate = Q(2 * r * (m - r), m)
            add(
                answer.setdefault(rate, {}),
                radicand,
                -coefficient * Q(comb(m, r), 2**m),
            )
            binomial_terms += 1
    return {rate: vector for rate, vector in answer.items() if vector}, binomial_terms


def integrated_spectrum_at(spec, t):
    value = {}
    for rate, vector in spec.items():
        if rate < t:
            for radicand, coefficient in vector.items():
                add(value, radicand, coefficient * (t - rate))
    return value


def enclose_radical_sum(vector):
    lower = upper = Q(0)
    for radicand, coefficient in vector.items():
        lo_root, hi_root = ROOT_BRACKETS[radicand]
        require(lo_root * lo_root <= radicand <= hi_root * hi_root,
                f"invalid sqrt({radicand}) bracket")
        lower += coefficient * (lo_root if coefficient >= 0 else hi_root)
        upper += coefficient * (hi_root if coefficient >= 0 else lo_root)
    return lower, upper


def polynomial_control():
    """Check the coefficient identity behind the strict-Jensen proof."""
    for m in range(2, 10):
        require(
            Q(comb(9, m), 72) == Q(comb(7, m - 2), m * (m - 1)),
            "U coefficient does not reproduce beta",
        )

    # U(v)=sum_{m=2}^9 (-1)^m binom(9,m)v^m/72.
    # Differentiate twice as a coefficient array and compare with (1-v)^7.
    second = {
        m - 2: Q((-1) ** m * comb(9, m) * m * (m - 1), 72)
        for m in range(2, 10)
    }
    target = {j: Q((-1) ** j * comb(7, j)) for j in range(8)}
    require(second == target, "U'' is not (1-v)^7")


def main_record():
    spec, binomial_terms = spectrum()
    require(binomial_terms == 52, "wrong number of binomial terms")
    require(len(spec) == 19, "wrong number of collected rates")

    total_mass = {}
    for vector in spec.values():
        for radicand, coefficient in vector.items():
            add(total_mass, radicand, coefficient)
    require(not total_mass, "signed spectrum does not have zero mass")

    left, middle, right = Q(33, 25), Q(4, 3), Q(27, 20)
    internal = sorted(rate for rate in spec if left < rate < right)
    require(internal == [middle], "unaccounted knot in claimed window")

    enclosures = {}
    for point in (left, middle, right):
        lo, hi = enclose_radical_sum(integrated_spectrum_at(spec, point))
        require(hi < -Q(1, 125), "negative-window bound failed")
        enclosures[str(point)] = [str(lo), str(hi)]

    # Since the signed spectrum has zero mass,
    # |A(t)| <= integral a |nu|(da).  Use sqrt(m)>=1 to retain the exact
    # rational bound sum 4*binom(7,m-2)/m^2, rather than round it up to 128.
    global_bound = sum(Q(4 * comb(7, m - 2), m * m) for m in range(2, 10))
    require(global_bound == Q(954881, 45360), "global bound mismatch")

    mean, radius = Q(267, 200), Q(3, 200)
    require((mean - radius, mean + radius) == (left, right),
            "Gamma window mismatch")

    # First reproduce the author's conservative derivative certificate.
    author_order = 2**28
    author_outside = mean * mean / (radius * radius * (author_order + 1))
    author_upper = -Q(1, 125) + (Q(128) + Q(1, 125)) * author_outside
    require(author_outside == Q(7921, author_order + 1),
            "author Chebyshev probability mismatch")
    require(author_upper == -Q(141691536, 33554432125),
            "author expectation bound mismatch")
    require(author_upper < 0, "author derivative witness is not negative")

    # Refinement: use the exact rational global bound above.  Order 2^25 is
    # already enough, with a comfortable exact negative margin.
    refined_order = 2**25
    refined_outside = mean * mean / (radius * radius * (refined_order + 1))
    refined_upper = -Q(1, 125) + (global_bound + Q(1, 125)) * refined_outside
    require(refined_upper == -Q(115243646839, 38050727022000),
            "refined expectation bound mismatch")
    require(refined_upper < 0, "refined derivative witness is not negative")

    polynomial_control()

    return {
        "status": "ENDPOINT_SCATTER_INDEPENDENT_ACCEPT",
        "binomial_terms": binomial_terms,
        "collected_rates": len(spec),
        "internal_window_knots": [str(rate) for rate in internal],
        "negative_window_enclosures": enclosures,
        "global_absolute_bound": str(global_bound),
        "author_derivative_witness": {
            "order": author_order,
            "lambda": str(Q(author_order + 1, 1) / mean),
            "expectation_upper": str(author_upper),
        },
        "refined_derivative_witness": {
            "order": refined_order,
            "lambda": str(Q(refined_order + 1, 1) / mean),
            "expectation_upper": str(refined_upper),
        },
        "strict_jensen_polynomial_identity": True,
    }


if __name__ == "__main__":
    record = main_record()
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    require(record == expected, "output differs from pinned expected record")
    print(json.dumps(record, indent=2, sort_keys=True))
