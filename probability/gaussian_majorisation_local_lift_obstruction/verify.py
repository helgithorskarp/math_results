#!/usr/bin/env python3
"""Exact finite certificate for a LOCAL lifted-moment obstruction.

This is NOT a counterexample to Gaussian majorisation. See PROOF.md.
Python standard library only; rational outward bounds are reused from the
previous published certificate directory, at the explicit sibling path below.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gaussian_majorisation_hankel_transport"))
from bounds import I, exp_negative, sqrt_integer

GRID = tuple(F(9 * i, 4) for i in range(-3, 4))
EPS = F(1, 10**30)
L = 10**32
BETA = F(17, 10**6)
D = F(2187, 4)
DIGITS = 70


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ipow(value, n):
    ans = I.of(1)
    for _ in range(n):
        ans = (ans * value).rounded(DIGITS)
    return ans


def compositions(total, n):
    if n == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, n - 1):
            yield (first,) + rest


def ordered_histograms(k):
    ha, hb = defaultdict(F), defaultdict(F)
    count = 0
    for x in product(GRID, repeat=k):
        energy = sum((x[i] - x[j])**2 for i in range(k) for j in range(i)) / (2*k)
        ha[energy] += 1
        hb[energy] += (x[0] - x[1])**2
        count += 1
    return dict(ha), dict(hb), count


def count_histograms(k):
    ha, hb = defaultdict(F), defaultdict(F)
    count = 0
    for c in compositions(k, len(GRID)):
        multiplicity = factorial(k)
        for ci in c:
            multiplicity //= factorial(ci)
        pair_sum = sum(c[i]*c[j]*(GRID[i]-GRID[j])**2
                       for i in range(len(GRID)) for j in range(i))
        energy = pair_sum / (2*k)
        ha[energy] += multiplicity
        hb[energy] += multiplicity * 2 * pair_sum / (k*(k-1))
        count += 1
    return dict(ha), dict(hb), count


def enclose_histogram(hist, k):
    value = I.of(0)
    for energy, weight in sorted(hist.items()):
        value = (value + weight * exp_negative(-energy, DIGITS)).rounded(DIGITS)
    return (value / (7**k * sqrt_integer(k, DIGITS))).rounded(DIGITS)


def main_result():
    scalar = sorted((L*(a+EPS*b), b, a) for a in GRID for b in GRID)
    require(len({x for x, _, _ in scalar}) == 49, "encoding is not injective")
    pair_count = 0
    for i, (x, y, _) in enumerate(scalar):
        for xx, yy, _ in scalar[:i]:
            require(abs(y-yy) <= abs(x-xx)/100, "scalar contraction bound failed")
            pair_count += 1
    slopes = [(scalar[i+1][1]-scalar[i][1]) / (scalar[i+1][0]-scalar[i][0])
              for i in range(len(scalar)-1)]
    require(max(abs(v) for v in slopes) == F(1, 100), "unexpected sharp slope")

    distance_error = D*(2*EPS+EPS**2+F(2,L**2))
    loss_error = D*(2*EPS+EPS**2+F(1,L**2))
    moments, reference, records = [], [], []
    tuples = states = 0
    for k in (2, 3, 4):
        ha, hb, n = ordered_histograms(k)
        ca, cb, nn = count_histograms(k)
        require(ha == ca and hb == cb, "ordered/count histogram mismatch")
        require(sum(ha.values()) == 7**k, "wrong probability normalization")
        require(sum(hb.values()) == F(81, 2)*7**k,
                "unweighted pair variance mismatch")
        ak, bk = enclose_histogram(ha,k), enclose_histogram(hb,k)
        ref = (3*bk*ipow(ak,5)).rounded(DIGITS)
        error = (loss_error + D*(k-1)*distance_error/4) / k**3
        actual = I(ref.lo-error,ref.hi+error)
        require(actual.lo>0, "moment enclosure lost positivity")
        moments.append(actual)
        reference.append(ref)
        tuples += n
        states += nn
        records.append({"k":k, "distinct_exponents":len(ha),
                        "A":ak.strings(40), "B":bk.strings(40),
                        "reference_moment":ref.strings(40),
                        "perturbation_error":str(error),
                        "actual_moment":actual.strings(40)})

    root2, root3 = sqrt_integer(2,DIGITS), sqrt_integer(3,DIGITS)
    m0,m1,m2 = moments
    determinant = 2*root2*m0*m2 - 3*m1*m1
    quadratic = BETA**2*root2*m0 - 2*BETA*root3*m1 + 2*m2
    ratio = m0*m2/(m1*m1)
    require(determinant.hi < -F(18,10**21), "determinant margin failed")
    require(quadratic.hi < -F(198,10**18), "polynomial margin failed")
    require(ratio.hi < F(1053,1000), "ratio upper bound failed")
    require((I.of(3)/(2*root2)).lo > F(106,100), "threshold bound failed")
    return {"claim":"CERTIFIED_LOCAL_LIFT_OBSTRUCTION",
            "not_a_majorisation_counterexample":True,
            "parameters":{"grid":[str(x) for x in GRID],"epsilon":str(EPS),
                          "L":str(L),"variance":"1","beta":str(BETA),
                          "time":"L^2/(1+L^2)","atom_count":7**6},
            "checks":{"scalar_pairs":pair_count,"scalar_segments":len(slopes),
                      "sharp_lipschitz_constant":"1/100", "ordered_tuples":tuples,
                      "multinomial_states":states,"precision_decimal_digits":DIGITS},
            "moments":records,
            "first_hankel_determinant":determinant.strings(40),
            "rational_polynomial_quadratic":quadratic.strings(40),
            "moment_ratio":ratio.strings(30),
            "required_ratio":(I.of(3)/(2*root2)).strings(30),
            "trust_boundary":"Written reduction and perturbation proof; exact Python arithmetic and sibling bounds.py; no floating point, spatial quadrature, or exhaustive 6D enumeration."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare the complete result with EXPECTED.json")
    args = parser.parse_args()
    result = main_result()
    if args.check:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "complete result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))
