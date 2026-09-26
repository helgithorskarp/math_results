#!/usr/bin/env python3
"""Exact supplementary checks for PROOF.md; Python >=3.11, standard library.

No floating point or search-completeness claim. The analytic proof establishes
the universal theorem and moving-mode uniformity. This program audits finite
geometry, two routes to spherical moments, and normalized variation values.
"""

from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import factorial
from pathlib import Path


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        lead = a[r][j]
        a[r] = [x/lead for x in a[r]]
        for i in range(r+1, len(a)):
            lead = a[i][j]
            a[i] = [x-lead*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def double_factorial(n):
    require(n >= -1, "invalid double factorial")
    value = 1
    for k in range(n, 0, -2):
        value *= k
    return value


def sphere_moment(v, k):
    """Exact average of (theta dot v)^(2k) on S^2 via coordinate monomials."""
    result = F(0)
    for a in range(k+1):
        for b in range(k-a+1):
            c = k-a-b
            multinomial = factorial(2*k)
            denominator = factorial(2*a)*factorial(2*b)*factorial(2*c)
            coefficient = F(multinomial, denominator)
            spherical = F(
                double_factorial(2*a-1)*double_factorial(2*b-1)
                * double_factorial(2*c-1), double_factorial(2*k+1))
            monomial = v[0]**(2*a)*v[1]**(2*b)*v[2]**(2*c)
            result += coefficient*spherical*monomial
    return result


@lru_cache(maxsize=None)
def exp_interval(x, terms=100):
    """Outward rational bounds, using a positive Taylor series and tail ratio."""
    if x < 0:
        lo, hi = exp_interval(-x, terms)
        return 1/hi, 1/lo
    term = F(1)
    total = term
    for k in range(1, terms):
        term *= x/F(k)
        total += term
    next_term = term*x/F(terms)
    ratio = x/F(terms+1)
    require(ratio < 1, "exponential Taylor order insufficient")
    return total, total+next_term/(1-ratio)


@lru_cache(maxsize=None)
def spherical_laplace_interval(x, terms=100):
    """Bounds S(sqrt(x))=sum x^k/(2k+1)! without square roots."""
    require(x >= 0, "negative squared argument")
    term = F(1)
    total = term
    for k in range(1, terms):
        term *= x/F((2*k)*(2*k+1))
        total += term
    next_term = term*x/F((2*terms)*(2*terms+1))
    ratio = x/F((2*terms+2)*(2*terms+3))
    require(ratio < 1, "spherical Taylor order insufficient")
    return total, total+next_term/(1-ratio)


def linear_combination(coefficients, intervals):
    lower = upper = F(0)
    for c, (lo, hi) in zip(coefficients, intervals):
        lower += c*(lo if c >= 0 else hi)
        upper += c*(hi if c >= 0 else lo)
    return lower, upper


def multiply_positive(a, b):
    require(a[0] >= 0 and b[0] >= 0, "positive interval multiplication required")
    return a[0]*b[0], a[1]*b[1]


def compact_interval(interval, digits=24):
    scale = 10**digits
    return [str(F((interval[0]*scale).__floor__(), scale)),
            str(F((interval[1]*scale).__ceil__(), scale))]


def fixture():
    p = [tuple(F(sign if i == j else 0) for j in range(3))
         for i in range(3) for sign in (-1, 1)]
    parameters = [(F(0), F(0)), (F(1, 10), F(0)), (F(0), F(1, 10)),
                  (-F(1, 10), F(0)), (F(0), -F(1, 10)),
                  (F(1, 10), F(1, 10))]
    q = [(2*u/(1+u*u+v*v), 2*v/(1+u*u+v*v),
          (1-u*u-v*v)/(1+u*u+v*v)) for u, v in parameters]
    return p, q


def mean(points, weights):
    return tuple(sum(w*x[j] for w, x in zip(weights, points)) for j in range(3))


def variation_checks(p, q, weights):
    require(sum(weights) == 1 and min(weights) > 0, "invalid weights")
    n = len(p)
    differences = [norm2(sub(p[i], p[j]))-norm2(sub(q[i], q[j]))
                   for i in range(n) for j in range(n)]
    require(min(differences) >= 0, "not a contraction")
    pair_weights = [weights[i]*weights[j] for i in range(n) for j in range(n)]
    mean_gap = norm2(mean(q, weights))-norm2(mean(p, weights))
    weighted_deficit = sum(w*d for w, d in zip(pair_weights, differences))
    require(weighted_deficit == 2*mean_gap, "weighted Gram identity failed")
    vp = [norm2(add(p[i], p[j])) for i in range(n) for j in range(n)]
    vq = [norm2(add(q[i], q[j])) for i in range(n) for j in range(n)]
    require([b-a for a, b in zip(vp, vq)] == differences,
            "norm-preserving distance/sum identity failed")
    coefficients = []
    for k in range(1, 13):
        c = sum(w*(b**k-a**k) for w, a, b in zip(pair_weights, vp, vq))
        c /= factorial(2*k+1)
        require(c > 0, "quadratic-variation series coefficient is not positive")
        coefficients.append(c)
    require(coefficients[0] == mean_gap/3, "small-radius coefficient failed")
    # After stripping pi*C*exp(-1)/s, both routes to the leading hinge gap
    # are: (1/2)B from the sphere, and maximum shift times ball volume.
    require(2*coefficients[0] == F(4, 3)*(mean_gap/2),
            "moving-mode/Taylor factor normalization failed")
    samples = []
    signed_weights = pair_weights + [-w for w in pair_weights]
    for radius in (F(1, 4), F(1, 2), F(1), F(2), F(3), F(4)):
        intervals = [spherical_laplace_interval(radius*radius*v) for v in vq+vp]
        enclosed = linear_combination(signed_weights, intervals)
        require(enclosed[0] > 0, "quadratic variation enclosure not positive")
        require(enclosed[1]-enclosed[0] < F(1, 10**45), "wide spherical enclosure")
        samples.append([str(radius), *compact_interval(enclosed)])
    # Integrating the spherical formula over all thresholds is the L2 gap.
    # The radial Gaussian moments turn each 1/(2k+1)! into 1/(4^k k!).
    for k in range(13):
        radial = F(double_factorial(2*k+1), 2**k)
        require(radial/factorial(2*k+1) == F(1, 4**k*factorial(k)),
                "integrated spherical coefficient failed")
    direct = linear_combination(signed_weights,
        [exp_interval(-norm2(sub(q[i], q[j]))/4) for i in range(n) for j in range(n)]
        + [exp_interval(-norm2(sub(p[i], p[j]))/4) for i in range(n) for j in range(n)])
    integrated = linear_combination(signed_weights,
        [exp_interval(v/4) for v in vq+vp])
    require(integrated[0] > 0, "integrated comparison not positive")
    integrated = multiply_positive(exp_interval(F(-1)), integrated)
    require(direct[0] > 0 and max(direct[0], integrated[0]) <= min(direct[1], integrated[1]),
            "direct overlap and integrated-sphere L2 routes disagree")
    require(direct[1]-direct[0] < F(1, 10**45), "wide overlap enclosure")
    return {"weighted_mean_square_gap": str(mean_gap),
            "weighted_pair_deficit": str(weighted_deficit),
            "positive_series_coefficients": len(coefficients),
            "normalized_quadratic_samples": samples,
            "L2_coefficient_times_4pi_to_three_halves": compact_interval(direct)}


def flap_check():
    u = [(F(1), F(1), F(1)), (F(1), F(-1), F(-1)),
         (F(-1), F(1), F(-1)), (F(-1), F(-1), F(1))]
    p, q = list(u), list(u)
    for i in range(4):
        for j in range(4):
            if i != j:
                p.append(sub(u[j], u[i]))
                q.append(add(u[j], u[i]))
    radial = [norm2(x)-norm2(y) for x, y in zip(p, q)]
    require(radial == [0]*4+[4]*12, "flap origin constraints failed")
    p = [(F(0),)*3]+p
    q = [(F(0),)*3]+q
    deficits = [norm2(sub(p[i], p[j]))-norm2(sub(q[i], q[j]))
                for i, j in combinations(range(17), 2)]
    require(min(deficits) >= 0, "augmented flap is not a contraction")
    require(rank([x+y for x, y in zip(p, q)]) == 6, "augmented flap paired rank")
    maximum_linear = linear_combination([F(3, 4), -F(3, 4)],
                                       [exp_interval(F(-2)), exp_interval(F(-4))])
    require(maximum_linear[0] > 0, "flap maximum coefficient sign failed")
    return {"points": 17, "pair_constraints": len(deficits),
            "strict_pair_constraints": sum(d > 0 for d in deficits),
            "strict_radial_constraints": sum(d > 0 for d in radial),
            "paired_rank": 6,
            "maximum_linear_coefficient_over_C": compact_interval(maximum_linear)}


def main():
    p, q = fixture()
    require(all(norm2(x) == norm2(y) == 1 for x, y in zip(p, q)), "unit norms failed")
    require(rank([x+y for x, y in zip(p, q)]) == 6, "rank with dominant origin failed")
    deficits = [norm2(sub(p[i], p[j]))-norm2(sub(q[i], q[j]))
                for i, j in combinations(range(6), 2)]
    require(min(deficits) > 0, "rare pairs must be strictly contracted")
    persisted = json.loads(Path(__file__).with_name("fixture.json").read_text())
    require(persisted["input"] == [[str(t) for t in x] for x in p]
            and persisted["output"] == [[str(t) for t in x] for x in q],
            "fixture differs from rational stereographic construction")
    require(persisted["uniform_weights"] == ["1/6"]*6
            and persisted["weighted_weights"] == [str(F(i, 21)) for i in range(1, 7)],
            "fixture weights differ from the two audited cases")
    vectors = [add(x, y) for points in (p, q) for x in points for y in points]
    checks = 0
    for v in vectors:
        for k in range(7):
            require(sphere_moment(v, k) == norm2(v)**k/F(2*k+1),
                    "coordinate and polar spherical moments disagree")
            checks += 1
    rigid_q = [(-x[1], x[0], x[2]) for x in p]
    require(all(norm2(sub(x, y)) == norm2(sub(a, b))
                for x, a in zip(p, rigid_q) for y, b in zip(p, rigid_q)),
            "orthogonal equality control failed")
    uniform = variation_checks(p, q, [F(1, 6)]*6)
    weighted = variation_checks(p, q, [F(i, 21) for i in range(1, 7)])
    records = {"uniform": uniform, "weighted": weighted}
    sample_bytes = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    report = {"status": "SMALL_MASS_GEOMETRY_CHECKS_PASS",
              "paired_rank_with_origin": 6, "rare_strict_pairs": 15,
              "spherical_moment_identity_checks": checks,
              "sample_records_sha256": hashlib.sha256(sample_bytes).hexdigest(),
              "variations": records, "augmented_flap": flap_check()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
