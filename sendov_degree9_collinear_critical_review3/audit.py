#!/usr/bin/env python3
"""Direct tensor Bernstein audit and exact quadratic phase-loss bounds.

No author implementation, certificate, root approximation or external package
is imported. Optional --compare checks the independently regenerated matrix
against the author's JSON; default reproduction needs no external input.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


class Checks:
    def __init__(self):
        self.count = 0
        self.mutations = []

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1

    def reject(self, operation, name):
        try:
            operation()
        except AssertionError:
            self.count += 1
            self.mutations.append(name)
        else:
            raise AssertionError("altered certificate accepted: " + name)


def multiply(left, ld, right, rd):
    """Bernstein product identity in three variables (a,u,t).

    B_i^d B_j^e = C(d,i)C(e,j)/C(d+e,i+j) B_(i+j)^(d+e).
    This calculation never converts to a power basis or interpolates a grid.
    """
    degree = tuple(x+y for x, y in zip(ld, rd))
    out = {}
    weights = [{
        (i, j): F(comb(ld[v], i)*comb(rd[v], j), comb(degree[v], i+j))
        for i in range(ld[v]+1) for j in range(rd[v]+1)
    } for v in range(3)]
    for i, c in left.items():
        for j, e in right.items():
            idx = tuple(x+y for x, y in zip(i, j))
            term = c*e
            for v in range(3):
                term *= weights[v][i[v], j[v]]
            out[idx] = out.get(idx, F(0))+term
    return {idx: c for idx, c in out.items() if c}, degree


def repeat(poly, degree, count):
    out, od = {(0, 0, 0): F(1)}, (0, 0, 0)
    for _ in range(count):
        out, od = multiply(out, od, poly, degree)
    return out, od


def profile(k):
    m = 8-k
    # A=1+a-at, of degrees (1,0,1).
    A = {(i, 0, s): F(1+i*(1-s)) for i in range(2) for s in range(2)}
    # B=1+a-at-(8/m)a^2*u*t, of degrees (2,1,1).
    B = {(i, j, s): 1+F(i, 2)*(1-s)-F(8, m)*int(i == 2)*j*s
         for i in range(3) for j in range(2) for s in range(2)}
    PA, da = repeat(A, (1, 0, 1), k)
    PB, db = repeat(B, (2, 1, 1), m)
    integrated, d = multiply(PA, da, PB, db)
    if d != (16-k, m, 8):
        raise AssertionError("incorrect full tensor degrees")
    # Integral B_s^8(t)=1/9. The leading factor nine therefore cancels:
    # the (a,u) coefficient is the sum over all t coefficients.
    matrix = [[sum((integrated.get((i, j, s), F(0)) for s in range(9)), F(0))
               for j in range(m+1)] for i in range(17-k)]
    # C=(1+(8/m)a*u)^m. Elevate its a degree from m to 16-k by
    # multiplying by the all-one Bernstein representation of constant one.
    C = {(i, j, 0): 1+F(8, m)*i*j for i in range(2) for j in range(2)}
    PC, dc = repeat(C, (1, 1, 0), m)
    one = {(i, 0, 0): F(1) for i in range(9)}
    PC, dc = multiply(PC, dc, one, (8, 0, 0))
    if dc != (16-k, m, 0):
        raise AssertionError("incorrect elevated subtraction degrees")
    return [[v-PC.get((i, j, 0), F(0)) for j, v in enumerate(row)]
            for i, row in enumerate(matrix)]


def validate_profile(matrix, k, checks):
    d, e = 16-k, 8-k
    checks.require(len(matrix) == d+1 and all(len(row) == e+1 for row in matrix),
                   "complete profile dimensions")
    zeros = [(i, j) for i, row in enumerate(matrix) for j, x in enumerate(row)
             if not x]
    checks.require(zeros == ([(d, e)] if k in (0, 7) else []),
                   "all and only certified corner zeros")
    for row in matrix:
        for c in row:
            checks.require(c == 0 or c >= 8, "coefficient positivity threshold")
    checks.require(matrix[0] == [F(8)]*(e+1), "origin row normalization")
    return zeros


def rational_bounds(checks):
    intervals = [(F(0), F(1, 2)), (F(1, 2), F(5, 8)), (F(5, 8), F(3, 4))]
    polar = []
    for lo, hi in intervals:
        peak = min(hi, max(lo, F(3, 8)))
        top = 1+F(3, 4)*peak-peak*peak
        bottom = 1-hi*hi-hi/4
        bound = top**9/(9*bottom)
        checks.require(bottom > 0 and bound < 1, "negative-branch polar bound")
        polar.append(str(bound))
    # Check the cleared-denominator linear origin-gap identity separately.
    lhs = [F(256)]*9
    rhs = [F(0)]*9
    for s, weight in enumerate([9, 84, 126, 36, 1]):
        for i in range(2*s+1):
            for j in range(9-2*s):
                rhs[i+j] += weight*comb(2*s, i)*(-1)**i*comb(8-2*s, j)
    checks.require(lhs == rhs, "linear gap binomial identity")
    K1 = 9*sum((F(comb(7, j), j+2)*F(8, 7)**j for j in range(8)), F(0))
    K2 = 9*sum((F(comb(6, j), j+3)*F(4, 3)**j for j in range(7)), F(0))
    checks.require(K1 == F(570801247, 1647086) < 500,
                   "uniform first derivative integral")
    checks.require(K2 == F(1199851, 5103) and K2 < 2*K1,
                   "uniform mixed second derivative integral")
    checks.require(F(9, 32)-K1/1250 == F(66019399, 16470860000) > 0,
                   "strict quadratic phase margin")
    checks.require(F(1, 2000)**2 < F(1, 1250),
                   "original linear cone lies within quadratic cone")
    checks.reject(lambda: checks.require(F(9, 32)-K1/1000 > 0,
                                        "unsafe relaxed square threshold"),
                  "square-threshold denominator 1250 changed to 1000")
    return polar, K1, K2


# Gaussian rationals as exact pairs. These controls validate the algebraic
# expansion behind the phase estimate; they are not a sampling proof.
def cadd(z, w):
    return z[0]+w[0], z[1]+w[1]


def cmul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def cscale(z, c):
    return z[0]*c, z[1]*c


def origin(q, a):
    coeff = [(F(1), F(0))]
    for z in q:
        nxt = [(F(0), F(0))]*(len(coeff)+1)
        for i, c in enumerate(coeff):
            nxt[i] = cadd(nxt[i], c)
            nxt[i+1] = cadd(nxt[i+1], cmul(c, cscale(z, -a)))
        coeff = nxt
    out = (F(0), F(0))
    for i, c in enumerate(coeff):
        out = cadd(out, cscale(c, F(9, i+1)))
    return out


def phase_controls(checks, K1):
    count = 0
    for a in [F(0), F(1, 3), F(3, 4), F(999, 1000)]:
        for parameter in [F(0), F(1, 10), F(1, 2), F(2)]:
            unit = ((1-parameter**2)/(1+parameter**2),
                    2*parameter/(1+parameter**2))
            q = [unit, (unit[0], -unit[1])]+[(F(1), F(0))]*6
            delta2 = sum(((z[0]-1)**2+z[1]**2 for z in q), F(0))
            # The two nonzero deviations have equal norm:
            # (sum |delta|)^2 = 4|delta_0|^2 = 2 sum |delta|^2.
            eps2 = 2*delta2
            for z in q:
                checks.require(z[0]**2+z[1]**2 == 1, "exact modulus control")
                checks.require((z[0]-1)**2+z[1]**2 == 2*(1-z[0]),
                               "real phase defect is quadratic")
            loss = origin([(F(1), F(0))]*8, a)[0]-origin(q, a)[0]
            checks.require(loss <= K1*eps2, "quadratic real-part loss control")
            checks.require(origin(q, a)[1] == 0, "conjugate-pair real integral")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare", type=Path,
                        help="optional author certificate; compare every rational entry")
    args = parser.parse_args()
    checks = Checks()
    matrices = []
    summaries = []
    for k in range(8):
        matrix = profile(k)
        zeros = validate_profile(matrix, k, checks)
        matrices.append([[str(x) for x in row] for row in matrix])
        summaries.append({"k": k, "degrees": [16-k, 8-k],
                          "entries": (17-k)*(9-k), "zeros": zeros,
                          "minimum_positive": str(min(x for row in matrix for x in row if x))})
    corrupted = [list(map(F, row)) for row in matrices[0]]
    corrupted[0][0] -= 1
    checks.reject(lambda: validate_profile(corrupted, 0, checks),
                  "origin coefficient eight changed to seven")
    polar, K1, K2 = rational_bounds(checks)
    controls = phase_controls(checks, K1)
    if args.compare:
        author = json.loads(args.compare.read_text())
        if len(author["profiles"]) != 8:
            raise AssertionError("incomplete author profile list")
        for k, p in enumerate(author["profiles"]):
            if (p["k"], p["a_degree"], p["u_degree"], p["coefficients"]) != (
                    k, 16-k, 8-k, matrices[k]):
                raise AssertionError("entry-level independent comparison failed")
    packed = json.dumps(matrices, separators=(",", ":")).encode()
    print(json.dumps({
        "agent": "six-reviewer-3", "role": "reviewer", "status": "PASS",
        "method": "direct tensor Bernstein multiplication and integration",
        "exact_checks": checks.count, "profiles": summaries,
        "coefficients": 636, "positive_coefficients": 634,
        "matrix_sha256": hashlib.sha256(packed).hexdigest(),
        "negative_branch_upper_bounds": polar,
        "first_derivative_bound": str(K1), "mixed_second_derivative_bound": str(K2),
        "phase_square_threshold": "(1-a)/1250",
        "strict_margin_coefficient": str(F(9, 32)-K1/1250),
        "gaussian_rational_phase_controls": controls,
        "mutations_rejected": checks.mutations,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
