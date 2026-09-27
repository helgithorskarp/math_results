#!/usr/bin/env python3
"""Exact supplementary checks, not a substitute for PROOF.md.

Standard-library CPython 3.11.2; no assert-based proof obligations, external
data, floating point, solver, or CAS. Sparse polynomials have rational
coefficients and variables (a,b,c,d,t,h,g). Fractions serialize canonically.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import json


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


class Poly:
    n = 7

    def __init__(self, value=0):
        terms = value if isinstance(value, dict) else {(0,) * self.n: Q(value)}
        self.terms = {m: Q(v) for m, v in terms.items() if v}
        need(all(len(m) == self.n and all(isinstance(k, int) and k >= 0 for k in m)
                 for m in self.terms), "bad polynomial monomial")

    @classmethod
    def variable(cls, i):
        m = [0] * cls.n
        m[i] = 1
        return cls({tuple(m): 1})

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Poly) else Poly(x)

    def __add__(self, other):
        out = dict(self.terms)
        for m, v in self.coerce(other).terms.items():
            out[m] = out.get(m, 0) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -v for m, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        out = {}
        for m, v in self.terms.items():
            for n, w in self.coerce(other).terms.items():
                p = tuple(x + y for x, y in zip(m, n))
                out[p] = out.get(p, 0) + v * w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        need(isinstance(power, int) and power >= 0, "bad exponent")
        ans = Poly(1)
        for _ in range(power):
            ans = ans * self
        return ans

    def derivative(self, index):
        out = {}
        for m, v in self.terms.items():
            if m[index]:
                n = list(m)
                n[index] -= 1
                out[tuple(n)] = v * m[index]
        return Poly(out)

    def at(self, values):
        need(len(values) == self.n, "bad evaluation dimension")
        ans = Q(0)
        for m, v in self.terms.items():
            term = v
            for x, p in zip(values, m):
                term *= Q(x) ** p
            ans += term
        return ans


def zero(poly, label):
    need(not poly.terms, label + " failed")


def dot(x, y):
    need(len(x) == len(y), "dot dimension")
    return sum((a * b for a, b in zip(x, y)), Q(0))


def scale(a, x):
    return tuple(a * b for b in x)


def dist2(x, y):
    z = tuple(a - b for a, b in zip(x, y))
    return dot(z, z)


def determinant(rows):
    mat = [[Q(x) for x in row] for row in rows]
    n = len(mat)
    need(all(len(row) == n for row in mat), "determinant is not square")
    ans = Q(1)
    for col in range(n):
        pivot = next((i for i in range(col, n) if mat[i][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            mat[pivot], mat[col] = mat[col], mat[pivot]
            ans = -ans
        value = mat[col][col]
        ans *= value
        for i in range(col + 1, n):
            ratio = mat[i][col] / value
            for j in range(col + 1, n):
                mat[i][j] -= ratio * mat[col][j]
            mat[i][col] = 0
    return ans


def identities():
    a, b, c, d, t, h, g = [Poly.variable(i) for i in range(7)]
    zero((a + t)**2 + (1 - a*a)*(1 - t*t) - (1 + a*t)**2, "norm")
    numerator = c*(a+t)*(b+t) + d*(1-t*t)
    denominator = (1+a*t)*(1+b*t)
    actual = numerator.derivative(4)*denominator - numerator*denominator.derivative(4)
    factor = (a+b)*(1+t*t) + 2*t*(1+a*b)
    claimed = factor*(c*(1-a*b)-d)
    zero(actual-claimed, "inner product derivative")
    # Reject a deliberately reversed sign in the claimed factorization.
    wrong = factor*(c*(1-a*b)+d)
    need(bool((actual-wrong).terms), "bad identity was accepted")
    need((actual-wrong).at([0, 0, 0, 1, 1, 0, 0]) == -4,
         "bad identity witness changed")
    # Use b as the norm bound q, and g as the shear parameter.
    shear_det = (b*b-a*a)*(b*b-a*a-g*g) - a*a*g*g
    zero(shear_det-((b*b-a*a)**2-b*b*g*g), "shear determinant")
    # Use a=E, b=F for the two limiting scalar-defect inequalities.
    plus = 1-h*h*a*a-(1-h*b*a)**2
    minus = 1-h*h*a*a-(1+h*b*a)**2
    zero(plus+minus+2*h*h*a*a*(1+b*b), "opposite derivative sum")
    # Independent differentiation of the squared last-coordinate distance.
    zero(((1-t)**2*(a-b)**2).derivative(4)+2*(1-t)*(a-b)**2, "lowering")
    return {
        "norm_identity": "PASS",
        "pair_derivative_factorization": "PASS",
        "shear_determinant": "PASS",
        "opposite_derivative_defect_sum": "PASS",
        "lowering_identity": "PASS",
        "wrong_derivative_sign_rejected_at_exact_witness": "-4",
    }


def angular_example():
    axes = [(Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1))]
    oblique = [tuple(Q(v, 3) for v in row) for row in [(1, 2, 2), (2, 1, 2), (2, 2, 1)]]
    sites = [(Q(0),)*3] + axes + oblique + [(Q(2), Q(3), Q(6))]
    radii = [Q(0)] + [Q(1)]*6 + [Q(7)]
    directions, alphas, targets = [], [], []
    for x, r in zip(sites, radii):
        need(dot(x, x) == r*r, "rational radius mismatch")
        u = scale(1/r, x) if r else (Q(0),)*3
        a = abs(u[0]*u[1]*u[2])
        directions.append(u)
        alphas.append(a)
        targets.append(scale(a, x))
    margins = []
    cone_checks = 0
    for i, j in combinations(range(len(sites)), 2):
        loss = dist2(sites[i], sites[j])-dist2(targets[i], targets[j])
        need(loss >= 0, "endpoint contraction failed")
        margins.append(loss)
        if radii[i] and radii[j]:
            a, b = alphas[i], alphas[j]
            c = dot(directions[i], directions[j])
            need(c <= 0 or c*c*(1-a*b)**2 <= (1-a*a)*(1-b*b), "full cone failed")
            cone_checks += 1
    rank_det = determinant([x+y for x, y in zip(sites[1:7], targets[1:7])])
    need(rank_det == Q(320, 531441), "paired rank determinant")
    q = Q(2, 3)
    bound = q - Q(1, 27)/q
    reserve = bound*bound-Q(1, 3)
    need(bound == Q(11, 18) and reserve == Q(13, 324), "differential reserve")
    return {
        "sites": [[str(v) for v in x] for x in sites],
        "alphas": [str(v) for v in alphas],
        "endpoint_pairs": len(margins),
        "full_cone_ray_pairs": cone_checks,
        "least_endpoint_squared_loss": str(min(margins)),
        "paired_rank_determinant": str(rank_det),
        "global_derivative_bound": str(q),
        "squared_derivative_reserve": str(reserve),
        "coordinate_plane_one_sided_factor": str(Q(3, 5)*Q(4, 5)),
    }


def rational_motion():
    # Factors and their nonnegative complementary square roots.
    factors = [(Q(0), Q(1)), (Q(3, 5), Q(4, 5)),
               (Q(4, 5), Q(3, 5)), (Q(5, 13), Q(12, 13)), (Q(1), Q(0))]
    # Ordered (cos(theta), sin(theta)), theta from zero to pi/2.
    angles = [(Q(1), Q(0)), (Q(12, 13), Q(5, 13)), (Q(4, 5), Q(3, 5)),
              (Q(3, 5), Q(4, 5)), (Q(5, 13), Q(12, 13)), (Q(0), Q(1))]
    cosines = [Q(-1), Q(-3, 5), Q(0), Q(3, 5), Q(1)]
    cases = 0
    endpoint_checks = 0
    for a, sa in factors:
        for b, sb in factors:
            need(a*a+sa*sa == 1 and b*b+sb*sb == 1, "factor normalization")
            for c in cosines:
                if c*(1-a*b) > sa*sb:
                    continue
                # Arbitrary unequal radii exercise the full-cone distance.
                r, q = Q(2), Q(7, 3)
                distances = []
                for tau, sine in angles:
                    need(tau*tau+sine*sine == 1, "angle normalization")
                    aa, ba = (a+tau)/(1+a*tau), sa*sine/(1+a*tau)
                    ab, bb = (b+tau)/(1+b*tau), sb*sine/(1+b*tau)
                    need(aa*aa+ba*ba == 1 and ab*ab+bb*bb == 1, "lifted norm")
                    distances.append(r*r+q*q-2*r*q*(c*aa*ab+ba*bb))
                need(all(x >= y for x, y in zip(distances, distances[1:])), "raise monotonicity")
                target = r*r*a*a+q*q*b*b-2*r*q*c*a*b
                lowered = [target+(1-t)**2*(r*sa-q*sb)**2 for t in [Q(0), Q(1, 2), Q(1)]]
                need(distances[-1] == lowered[0], "stage join")
                need(all(x >= y for x, y in zip(lowered, lowered[1:])), "lower monotonicity")
                need(distances[0] == r*r+q*q-2*r*q*c and lowered[-1] == target, "endpoints")
                cases += 1
                endpoint_checks += 2
    return {"admissible_factor_pair_cosine_cases": cases,
            "raise_samples_per_case": len(angles), "lower_samples_per_case": 3,
            "endpoint_checks": endpoint_checks,
            "scope": "finite calibration; polynomial identity proves the continuum sign"}


def invalid_cone():
    # Unit-radius representatives contract, but extending both rays fails.
    a, b, c, d = Q(0), Q(4, 5), Q(13, 20), Q(3, 5)
    loss = lambda r, q: (1-a*a)*r*r+(1-b*b)*q*q-2*c*(1-a*b)*r*q
    unit_loss = loss(Q(1), Q(1))
    unequal_loss = loss(Q(13, 20), Q(1))
    derivative = (a+b)*(c*(1-a*b)-d)  # k'(0)
    need(unit_loss == Q(3, 50) and unequal_loss == Q(-1, 16), "invalid cone witness")
    need(derivative == Q(1, 25), "invalid cone derivative witness")
    return {"unit_radius_squared_loss": str(unit_loss),
            "unequal_radius_squared_loss": str(unequal_loss),
            "wrong_way_inner_product_derivative_at_tau_zero": str(derivative),
            "rejected": True}


def classical_motion_control():
    r, q, a, b, c = Q(3, 5), Q(1), Q(0), Q(4, 5), Q(3, 5)
    need(c*(1-a*b) == Q(3, 5), "admissible tight cone")
    source = r*r+q*q-2*r*q*c
    target = (a*r)**2+(b*q)**2-2*a*b*r*q*c
    ar, aq = r*(1+a)/2, q*(1+b)/2
    midpoint = ar*ar+aq*aq-2*c*ar*aq+(r*(1-a)-q*(1-b))**2/4
    need(source == target == Q(16, 25) and midpoint == Q(77, 125),
         "classical motion comparison")
    need(midpoint < target, "classical motion unexpectedly monotone")
    return {"source_and_target_distance_squared": str(source),
            "classical_midpoint_distance_squared": str(midpoint),
            "classical_motion_is_not_contracting": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = {"schema": "angular-ray-author-checks-v1", "arithmetic": "exact rational",
              "identities": identities(), "angular_example": angular_example(),
              "rational_motion_controls": rational_motion(),
              "invalid_full_cone_control": invalid_cone(),
              "classical_motion_comparison": classical_motion_control(),
              "status": "AUTHOR_CHECKS_PASS_NOT_INDEPENDENT_REVIEW"}
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        need(output == expected, "EXPECTED.json differs from canonical output")
        print("AUTHOR_CHECKS_PASS: identities, angular example, rational motions, rejected invalid inputs")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
