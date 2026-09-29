#!/usr/bin/env python3
"""Independent exact audit; imports no target code, data, or roots.

Newton's identity is checked by exact interpolation in the five-dimensional
space of symmetric homogeneous degree-four polynomials in eight variables.
The integrated polar prefactor is expanded as a dense univariate polynomial,
rather than using the target's pointwise binomial remainder calculation.
Universal analytic steps are the written proof in README.md.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb
import json

N = 8


class Checks:
    def __init__(self):
        self.count = 0
        self.mutations = []

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1

    def reject(self, check, name):
        try:
            check()
        except AssertionError:
            self.mutations.append(name)
            self.count += 1
        else:
            raise AssertionError("mutation accepted: " + name)


def elementary(values, degree):
    out = [F(1)] + [F(0)] * degree
    for x in values:
        for k in range(degree, 0, -1):
            out[k] += x * out[k-1]
    return out[degree]


def orbit_value(values, partition):
    result = F(0)
    exponents = sorted(set(permutations(partition)))
    for indices in combinations(range(N), len(partition)):
        for powers in exponents:
            term = F(1)
            for i, power in zip(indices, powers):
                term *= values[i] ** power
            result += term
    return result


def solve(matrix, values):
    """Exact row reduction; a zero pivot means these points do not certify."""
    rows = [list(map(F, row)) + [F(value)]
            for row, value in zip(matrix, values)]
    for col in range(len(rows)):
        pivot = next((i for i in range(col, len(rows)) if rows[i][col]), None)
        if pivot is None:
            raise AssertionError("singular interpolation matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [entry / divisor for entry in rows[col]]
        for i in range(len(rows)):
            if i != col:
                multiplier = rows[i][col]
                rows[i] = [x - multiplier*y for x, y in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def newton_certificate(checks):
    partitions = [(4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]
    points = [tuple(map(F, xs + [0]*(N-len(xs)))) for xs in
              [[1], [1, 1], [2, 1], [1, 1, 1], [1, 1, 1, 1]]]
    matrix = [[orbit_value(xs, part) for part in partitions] for xs in points]
    checks.require(matrix == [[1, 0, 0, 0, 0], [2, 2, 1, 0, 0],
                              [17, 10, 4, 0, 0], [3, 6, 3, 3, 0],
                              [4, 12, 6, 12, 1]], "orbit evaluation matrix")
    left, right, mutated = [], [], []
    for xs in points:
        e, L, M = [elementary(xs, k) for k in (1, 2, 3)]
        left.append(12*L*L - 21*e*M)
        mutated.append(12*L*L - 20*e*M)
        total = F(0)
        for i, j in combinations(range(N), 2):
            rest = [xs[k] for k in range(N) if k != i and k != j]
            total += (xs[i]-xs[j])**2 * (
                sum((x*x for x in rest), F(0)) + elementary(rest, 2))
        right.append(total)
    coefficients = solve(matrix, left)
    checks.require(coefficients == [0, 0, 12, 3, -12],
                   "left symmetric coefficient vector")
    checks.require(solve(matrix, right) == coefficients,
                   "universal Newton SOS identity by invertible interpolation")
    checks.reject(lambda: checks.require(solve(matrix, mutated) == coefficients,
                                        "changed Newton coefficient"),
                  "Newton coefficient 21 changed to 20")
    return list(map(int, coefficients))


def plus(p, q):
    result = [F(0)] * max(len(p), len(q))
    for terms in (p, q):
        for i, c in enumerate(terms):
            result[i] += c
    return result


def times(p, q):
    result = [F(0)] * (len(p)+len(q)-1)
    for i, c in enumerate(p):
        for j, d in enumerate(q):
            result[i+j] += c*d
    return result


def power(p, n):
    result = [F(1)]
    for _ in range(n):
        result = times(result, p)
    return result


def scale(p, c):
    return [c*x for x in p]


def polar_certificate(checks):
    gamma, h = F(1, 160), F(1, 100)
    a, b = [F(1), F(-1)], [F(0), F(2), F(-1)]
    c = times(b, [F(1), gamma])
    # Integral of (a + c*t)^8 from t=0 to 1, exactly as a polynomial in eta.
    H = [F(0)]
    for k in range(N+1):
        H = plus(H, scale(times(power(a, N-k), power(c, k)),
                          F(comb(N, k), k+1)))
    checks.require(len(H)-1 == 24 and H[-1] != 0,
                   "complete degree-24 integrated prefactor")
    checks.require(H[:4] == [1, 0, F(323, 60), F(-1109, 120)],
                   "integrated constant, linear, quadratic, cubic terms")
    tail = sum((abs(H[k])*h**(k-3) for k in range(3, len(H))), F(0))
    checks.require(tail < 10 < 128, "uniform integrated polar tail")
    # Every coefficient is represented: the eta^3 remainder bound is valid
    # on [0,h], by triangle inequality, rather than by parameter sampling.
    checks.reject(lambda: checks.require(abs(H[3]) <= F(9),
                                        "too small integrated tail constant"),
                  "integrated cubic remainder capped at nine")
    cleared = plus(power([1, F(-1, 2)], 2),
                   scale(times([1, -19], power([1, 9], 2)), -1))
    checks.require(cleared == [0, 0, F(1045, 4), 1539],
                   "polar lower-loss polynomial")
    checks.require(all(c >= 0 for c in cleared), "lower-loss positivity")
    checks.require((1+h)**8 < 2, "polar prefactor upper bound")
    checks.require(16/(1-h)**2 < 17, "polar exponent upper coefficient")
    checks.require(17*25 == 425 and 425**2 < 200000,
                   "finite exponential remainder constant")
    checks.require(8+19 < 30, "combined polar loss rounding")
    return H, tail


def bounds_and_refinement(checks):
    eta0, gamma = F(1, 10**6), F(1, 160)
    root_sum = sum((F(comb(N, k), k+1)*F(1, 7)**k
                    for k in range(1, N+1)), F(0))
    checks.require(root_sum == F(41980912, 51883209) < 1,
                   "other-root Cauchy exclusion")
    checks.require(7*(1+gamma*eta0) < 8, "reciprocal other-root radius")
    checks.require(8+eta0/20-F(7, 2) < 5, "critical reciprocal radius")
    checks.require(1-eta0 > F(99, 100), "distinguished root range")
    negative = F(64)/F(99, 100)
    real_l1 = 2*N*65+F(1, 40)
    checks.require(negative < 65, "negative real defect")
    checks.require(7*65+F(1, 40) < 456, "individual real defect")
    checks.require(real_l1 < 1100, "total real defect")
    checks.require(8+456*eta0 < 9, "projected reciprocal radius")
    real_defect = F(2*N*64-8)/F(99, 100)
    checks.require(real_defect < 1030, "reciprocal real-sum defect")
    checks.require(real_defect+F(1, 20) < 1100, "angular total defect")
    checks.require(F(1100, 8) < 140, "mean angular defect")
    checks.require(F(1030, 8) < 130 and gamma < 130, "mean drift")
    V = (1+F(3, 2)*gamma+24*eta0+37500*eta0**2)/(1-30*eta0)
    checks.require(1-30*eta0 > 0, "positive variance denominator")
    checks.require(V == F(80751923, 79997600) < F(5, 4),
                   "finite variance excludes collapsed branch")
    projection2, projection3 = [comb(7, k-1)*9**(k-1)*1100 for k in (2, 3)]
    angular2, angular3 = [k*comb(7, k-1)*5**(k-1)*1100 for k in (2, 3)]
    saturation = 4*(projection3+3*projection2)
    shifted_defect = saturation+angular3+4*angular2+F(35, 4)*1100
    checks.require(shifted_defect == 10366125 < 11000000,
                   "approximate Newton saturation defect")
    emin, emax = 4-1100*eta0, 4+eta0/20
    checks.require(F(7, 16)*emin**2-5 > 1, "Newton noncollapsed branch L>1")
    checks.require(F(7, 16)*emax**2 < 8, "Newton L<8")
    checks.require(F(7, 4)*emax < 8, "Newton prefactor upper bound")
    checks.require(F(7, 4)*1100*8+8*11000000 < 90000000,
                   "Newton defect bound")
    checks.require(F(7, 64)*(F(2, 5)+eta0/400) < 1,
                   "variance mean-square drift bound")
    checks.require(F(90000000, 4)+1 < 23000000, "linear variance rate")
    reciprocal_energy = N*(23000000+130**2*eta0+2*140)
    checks.require(reciprocal_energy < 190000000, "reciprocal energy rate")
    checks.require(2*N*eta0+8*190000000 < 1600000000,
                   "critical energy rate")
    h = F(1, 100)
    checks.require(F(3200, 999) < 4, "series remainder per cubic modulus")
    checks.require(F(32, 27)+4*h < 4, "coarse series energy coefficient")
    checks.require(8-F(1, 20) > 6, "relaxed failure implies eta bound")
    checks.require(F(8, 3)+F(16, 3)*h < 3, "eta at most three T")
    # Reused Schur bounds are valid under eta<=3T; compare every rounded
    # coefficient that differs from the target's larger Taylor remainder.
    checks.require(27+168*h < 29, "coefficient first-moment error")
    checks.require(F(243, 8)+216*h < 33, "constant-term moment error")
    checks.require(27*(1+13*h) < 31, "constant-term energy error")
    checks.require(124+F(72, 7) < 135, "Schur real-part error")
    checks.require(F(1042, 18) < 58, "Schur energy rounding")
    checks.require(58+24+4 == 86, "refined local energy loss")
    T = F(11, 25000)
    A, B = F(1, 16)-72*T, F(1, 14)-86*T
    checks.require(A == F(1541, 50000), "refined first-moment coefficient")
    checks.require(B == F(2939, 87500), "refined energy coefficient")
    checks.require(A-F(1, 60) == F(2123, 150000) > 0,
                   "strict first-moment margin for relaxed failure")
    checks.require(B-F(1, 30) == F(67, 262500) > 0,
                   "strict energy margin for relaxed failure")
    width = F(121, 10**18)
    checks.require(width < eta0, "refined annulus within stability range")
    checks.require(1600000000*width == T*T == F(121, 625000000),
                   "closed refined endpoint enters local theorem")
    checks.require(width/F(1, 10**18) == 121, "width ratio")
    checks.require(8/(F(3, 4)+T) > 8+F(1, 20), "small-root branch")
    checks.reject(lambda: checks.require(1600000000*F(122, 10**18) <= T*T,
                                        "oversized annulus at fixed T"),
                  "annulus numerator 121 changed to 122 at fixed T")
    return T, width, A, B


def controls(checks):
    for eta in [F(1, 10**6), F(1, 10**18), F(121, 10**18)]:
        a = 1-eta
        checks.require(8/a > 8+eta/20, "binomial interior margin")
        r = [1/(1+a)]*7+[9/(1+a)]
        mu = sum(r, F(0))/N
        v = sum(((x-mu)**2 for x in r), F(0))/N
        checks.require(sum(r, F(0)) == 16/(1+a) > 8+eta/20,
                       "collapsed interior margin")
        checks.require(v == 7/(1+a)**2 > F(5, 4),
                       "collapsed variance control")


def main():
    checks = Checks()
    newton = newton_certificate(checks)
    H, tail = polar_certificate(checks)
    T, width, A, B = bounds_and_refinement(checks)
    controls(checks)
    print(json.dumps({
        "agent": "six-reviewer-3", "role": "reviewer",
        "status": "PASS", "exact_checks": checks.count,
        "newton_basis_partitions": ["4", "31", "22", "211", "1111"],
        "newton_coefficients": newton,
        "polar_integral_degree": len(H)-1,
        "polar_first_coefficients": list(map(str, H[:4])),
        "polar_absolute_cubic_tail_less_than": 10,
        "local_threshold": str(T), "first_moment_coefficient": str(A),
        "energy_coefficient": str(B), "annulus_width": str(width),
        "annulus_width_ratio": 121, "mutations_rejected": checks.mutations,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
