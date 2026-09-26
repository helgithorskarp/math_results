#!/usr/bin/env python3
"""Exact finite audits of PROOF.md, not a finite proof of its quantifiers."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
from random import Random
import json
import sys

ROOT = Path(__file__).resolve().parent
PROBABILITY = ROOT.parent
DEPENDENCIES = {
    "gaussian_majorisation_hankel_transport/bounds.py":
        "60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7",
    "gaussian_majorisation_hankel_transport/certify.py":
        "71af430dbbecc055471b9f72b288cf4ff4d60ff797aacce8acd08ce7ca14551e",
    "gaussian_majorisation_hankel_transport/example.json":
        "0c96a1d144417e0a4262e7d6d8a5a1d6d206d10679d627a474fcad16c16bc8c9",
    "gaussian_majorisation_rank_abel/flap_fixture.json":
        "2edec28b8738cb0713c0ba70e4e8ec80147857503fbe2d801b43dbef4861ac08",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for name, digest in DEPENDENCIES.items():
    require(sha256((PROBABILITY/name).read_bytes()).hexdigest() == digest,
            "changed dependency: " + name)
sys.path.insert(0, str(PROBABILITY/"gaussian_majorisation_hankel_transport"))
from bounds import I, exp_negative, sqrt_integer  # noqa: E402
from certify import difference_histogram, distance_matrix, moment_gap  # noqa: E402


def norm2(vector):
    return sum(x*x for x in vector)


def averaging_audit():
    random = Random(26092612)
    count = 0
    for m in range(2, 11):
        for _ in range(12):
            points = [[F(random.randrange(-3, 4), 8) for _ in range(6)]
                      for _ in range(5)]
            weights = [F(random.randrange(1, 12)) for _ in points]
            weights = [w/sum(weights) for w in weights]
            b = [F(random.randrange(-3, 4), 8) for _ in range(6)]
            mean = [sum(w*z[j] for w, z in zip(weights, points)) for j in range(6)]
            var = sum(w*norm2([x-y for x, y in zip(z, mean)])
                      for w, z in zip(weights, points))
            total = F(0)
            for i, j in product(range(5), repeat=2):
                h = [(x-y)/2 for x, y in zip(points[i], points[j])]
                k = [(x+y)/2-z for x, y, z in zip(points[i], points[j], b)]
                total += weights[i]*weights[j]*(F(2, m+1)*norm2(h)
                         - F(2*m, (m+1)*(m+2))*norm2(k))
            expected = F(2, (m+1)*(m+2))*(var-m*norm2([x-y for x, y in zip(mean, b)]))
            require(total == expected, "averaged variance identity")
            require(var <= 1 and total <= F(2, (m+1)*(m+2)), "radius bound")
            count += 1
    return count


def multiply(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def algebra_audit():
    poly = [F(v) for v in [-1, -2, -4, -6, -9, -12, 12, 36, 33, 46, 32, 34, 21, 24, 12]]
    factored = multiply(multiply([-1, 3, -3, 1], [1, 1]), poly)
    target = [F(0)]*19
    for j, c in {0:1, 6:-28, 8:54, 9:-16, 12:-12, 15:16, 16:-27, 18:12}.items():
        target[j] = F(c)
    require(factored == target, "exact two-atom factorization")
    positive = sum(c for c in poly if c > 0)
    negative = -sum(c for c in poly if c < 0)
    require((positive, negative) == (250, 34), "coefficient sums")
    require(positive*F(9, 10)**14-negative > 0, "whole-interval sign certificate")
    curvature = multiply([1, -4, 4], [1, 4, 12, 18, 24, 24])
    require(curvature == [1, 0, 0, -14, 0, 0, 0, 96], "degree-nine convexity")
    prefix = I.of(1)/(128*sqrt_integer(2, 70))-I.of(7)/(400*sqrt_integer(5, 70))
    require(prefix.hi < 0, "preceding prefix cone does not include the example")
    require(F(5, 2)*(F(2, 17)+F(2, 3*17**3))-F(5, 17) == F(5, 14739),
            "strict quartic constant")
    a = [F(1), F(1, 2), F(1, 3), F(1, 4), F(19, 100)]
    require(all(a[i]*a[i+2] > a[i+1]**2 for i in range(3)), "abstract log-convexity")
    determinant = a[0]*a[2]*a[4]+2*a[1]*a[2]*a[3]-a[0]*a[3]**2-a[2]**3-a[4]*a[1]**2
    require(determinant == -F(1, 2700), "log-convexity is not full Hankel positivity")
    return {"whole_interval_polynomial_lower_bound": str(positive*F(9,10)**14-negative),
            "negative_prefix_interval": prefix.strings(24),
            "abstract_non_Gaussian_Hankel_determinant": str(determinant)}


def sparse_moment_audit():
    # Construct the representing measure directly with rational parameters;
    # no fractional-power floating-point reconstruction is used.
    count = 0
    for p, u, v in product([0, 1, 4], [1, 2, 3], [4, 5, 7]):
        point, theta, mass = F(2, 3), F(3, 5), F(p+2)
        moments = [mass, mass*theta*point**u, mass*theta*point**v]
        # A nonnegative trinomial: derivative has the sign of t^(v-u)-r^(v-u).
        r = F(1, 2)
        coefficients = [(v-u)*r**v, -v*r**(v-u), F(u)]
        value = sum(c*a for c, a in zip(coefficients, moments))
        h0 = coefficients[0]
        hx = sum(c*point**j for c, j in zip(coefficients, [0, u, v]))
        require(value == mass*((1-theta)*h0+theta*hx), "three-moment representation")
        require(value > 0 and hx >= 0, "sparse curvature comparison control")
        count += 1
    return count


def bernoulli_b(lam, s):
    u = 1/s
    def e(c):
        return exp_negative(-c*lam*lam*u, 75)-exp_negative(-c*u, 75)
    return {2:2*s*e(F(1)), 3:F(3,2)*s*e(F(4,3)),
            4:F(2,3)*s*e(F(3,2))+F(1,2)*s*e(F(2))}


def sharpness_audit():
    sharp_checks = 0
    negative_checks = 0
    for lam, s in product([F(0), F(1,2), F(99,100)],
                           [F(1,10), F(1), F(5,3), F(10), F(100), F(1000)]):
        b = bernoulli_b(lam, s)
        margin = b[2]*b[4]-exp_negative(-F(1,12)/s, 75)*b[3]*b[3]
        require(margin.lo > 0, "sharp replica bound control")
        sharp_checks += 1
        if lam == 0 and s >= F(5,3):
            require((b[2]*b[4]-b[3]*b[3]).hi < 0, "exact log-convexity obstruction")
            negative_checks += 1
    b = bernoulli_b(F(99,100), F(100))
    failed_improvement = b[2]*b[4]-exp_negative(-F(1,1300), 75)*b[3]*b[3]
    require(failed_improvement.hi < 0, "constant 1/13 must fail on this exact fixture")
    taylor_checks = 0
    for lam in [F(0), F(1,2), F(99,100)]:
        linear = {}
        for m in (2,3,4):
            leading = second = F(0)
            for tup in product([-1,1], repeat=m):
                exponent = sum((tup[i]-tup[j])**2 for i in range(m) for j in range(i))/F(2*m)
                leading += exponent*(1-lam**2)/2**m
                second += exponent**2*(lam**4-1)/(2*2**m)
            require(F(4,m-1)*leading == 2*(1-lam**2), "Bernoulli replica leading term")
            linear[m] = second/leading
        require(linear[2]+linear[4]-2*linear[3] == -(1+lam**2)/24,
                "optimal first-order curvature coefficient")
        taylor_checks += 1
    return {"sharp_bound_controls": sharp_checks, "non_log_convex_controls": negative_checks,
            "independent_ordered_replica_Taylor_checks": taylor_checks,
            "failed_constant_1_over_13": {"lambda": "99/100", "variance": "100",
                 "radius_squared": "1", "negative_margin": failed_improvement.strings(30)}}


def fixture_audit(name, x, y, weights, radius2, s, maximum):
    x = [[F(c) for c in z] for z in x]
    y = [[F(c) for c in z] for z in y]
    w = [F(v) for v in weights]
    require(sum(w) == 1 and all(v > 0 for v in w), "fixture weights")
    require(max(map(norm2, x)) <= radius2, "fixture radius")
    dx, dy = distance_matrix(x), distance_matrix(y)
    require(all(dx[i][j] >= dy[i][j] for i, j in product(range(len(w)), repeat=2)), "contraction")
    gaps = {m:moment_gap(difference_histogram(dx, dy, w, m, s), m, 70)
            for m in range(2, maximum+1)}
    b = {m:(4*s*m*sqrt_integer(m,70)*gap/(m-1)).rounded(65) for m, gap in gaps.items()}
    margins = []
    for m in range(2, maximum-1):
        margin = (b[m]*b[m+2]-exp_negative(-radius2/((m+1)*(m+2)*s),70)*b[m+1]*b[m+1]).rounded(60)
        require(margin.lo > 0, "averaged curvature inequality")
        margins.append(margin)
    a = {j:gaps[j+2]/((j+1)*(j+2)) for j in range(maximum-1)}
    quartic = (a[0]*a[2]-(1+F(5,14739))*a[1]*a[1]).rounded(60)
    require(s >= F(17,60)*radius2 and quartic.lo > 0, "new quartic threshold")
    out = {"name": name, "variance": str(s), "radius_squared": str(radius2),
           "replicas_through": maximum, "new_curvature_margins": [v.strings(24) for v in margins],
           "strengthened_quartic_margin": quartic.strings(24)}
    if s >= F(2,5)*radius2:
        minors = []
        for p in range(maximum-1):
            for u in range(1, maximum):
                for v in range(1, maximum):
                    if p+u+v > maximum-2:
                        continue
                    margin = a[p]*a[p+u+v]-a[p+u]*a[p+v]
                    require(margin.lo > 0, "arbitrary-offset Hankel minor")
                    minors.append(margin)
        out["positive_arbitrary_offset_minors"] = len(minors)
        if maximum >= 9:
            energy = (a[0]/32-F(7,16)*a[3]+3*a[7]).rounded(60)
            require(energy.lo > 0, "degree-nine energy outside preceding prefix cone")
            out["degree_nine_energy_gap"] = energy.strings(24)
    return out


def main():
    report = {"status":"ALL_FINITE_CHECKS_PASSED", "arithmetic":"exact rational and outward rational intervals",
              "scope":"Universal theorems rely on PROOF.md; finite cases alone prove no majorisation claim.",
              "dependencies":DEPENDENCIES, "averaging_identity_checks":averaging_audit(),
              "algebra":algebra_audit(), "sparse_moment_controls":sparse_moment_audit(),
              "sharpness":sharpness_audit()}
    fold = json.loads((PROBABILITY/"gaussian_majorisation_hankel_transport/example.json").read_text())
    flap = json.loads((PROBABILITY/"gaussian_majorisation_rank_abel/flap_fixture.json").read_text())
    report["fixtures"] = [
        fixture_audit("fold at degree-independent threshold", fold["x"], fold["y"],fold["weights"],F(1),F(2,5),9),
        fixture_audit("fold at new quartic threshold", fold["x"],fold["y"],fold["weights"],F(1),F(17,60),4),
        fixture_audit("simplex flap at degree-independent threshold",flap["input"],flap["output"],flap["weights"],F(8),F(16,5),4),
    ]
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
