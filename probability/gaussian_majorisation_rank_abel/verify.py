#!/usr/bin/env python3
"""Exact algebra and rational-enclosure checks for PROOF.md; Python >=3.11.

No floating point is used. Universal assertions use the written proof; the
Gamma samples below are cross-checks, not a replacement for the four regimes.
"""
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def norm2(v):
    return sum(x*x for x in v)


def subtract(a, b):
    return tuple(x-y for x, y in zip(a, b))


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][c]
        a[r] = [x/value for x in a[r]]
        for i in range(r+1, len(a)):
            value = a[i][c]
            a[i] = [x-value*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def paired_rank(p, q):
    rows = [tuple(x)+tuple(y) for x, y in zip(p, q)]
    return rank([subtract(row, rows[0]) for row in rows[1:]])


def deficits(p, q):
    return [norm2(subtract(p[i], p[j]))-norm2(subtract(q[i], q[j]))
            for i, j in combinations(range(len(p)), 2)]


def flap_fixture():
    u = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    p, q = list(u), list(u)
    labels = [f"anchor_{i}" for i in range(4)]
    for i in range(4):
        for j in range(4):
            if i != j:
                p.append(subtract(u[j], u[i]))
                q.append(tuple(a+b for a, b in zip(u[j], u[i])))
                labels.append(f"flap_{i}_{j}")
    return {"source": "Cheng--Tan--Zheng 1107.0140, reversed expansion; depth 1",
            "labels": labels, "input": [list(x) for x in p],
            "output": [list(x) for x in q], "weights": ["1/16"]*16}


def geometry_checks():
    fixture = flap_fixture()
    persisted = json.loads(Path(__file__).with_name("flap_fixture.json").read_text())
    require(fixture == persisted, "fixture differs from explicit construction")
    p, q = fixture["input"], fixture["output"]
    observed = deficits(p, q)
    require(min(observed) == 0 and max(observed) == 32, "flap contraction failed")
    require(paired_rank(p, q) == 6, "flap rank failed")
    # Check the displayed deficit formula against direct squared coordinates.
    labels = [None]*4 + [(i, j) for i in range(4) for j in range(4) if i != j]
    for a, b in combinations(range(16), 2):
        if b < 4:
            expected = 0
        elif a < 4:
            expected = 16 * (a == labels[b][0])
        else:
            i, j = labels[a]
            k, l = labels[b]
            expected = 16*((j == k)+(i == l))
        actual = norm2(subtract(p[a], p[b]))-norm2(subtract(q[a], q[b]))
        require(actual == expected, "flap deficit formula failed")
    # A rank-five global contraction with more than six support points.
    grid = list(product((-1, 0, 1), repeat=3))
    image = [(F(x, 2), F(abs(y+z), 4), F(abs(x-y), 4)) for x, y, z in grid]
    require(min(deficits(grid, image)) >= 0, "rank-five contraction failed")
    require(paired_rank(grid, image) == 5, "rank-five fixture rank failed")
    # Rank six is only a necessary condition for a counterexample. This fold
    # has full rank but is a composition of ordinary hyperplane foldings.
    cross = [(0, 0, 0)] + [tuple(sign*(i == j) for j in range(3))
                           for i in range(3) for sign in (-1, 1)]
    subsets = 0
    for size in range(1, 8):
        for indices in combinations(range(7), size):
            a = [cross[i] for i in indices]
            b = [tuple(abs(x) for x in v) for v in a]
            require(all(d >= 0 for d in deficits(a, b)), "fold contraction failed")
            require(paired_rank(a, b) <= size-1, "affine rank bound failed")
            subsets += 1
    require(paired_rank(cross, [tuple(abs(x) for x in v) for v in cross]) == 6,
            "full-rank positive-control fold failed")
    return {"flap_pairs": len(observed), "flap_paired_rank": 6,
            "flap_positive_deficits": sum(x > 0 for x in observed),
            "rank_five_points": len(grid), "fold_subsets": subsets}


def log2_interval(terms=96):
    # log 2 = 2 atanh(1/3); bound the positive tail geometrically.
    r = F(1, 3)
    lower = 2*sum(r**(2*k+1)/F(2*k+1) for k in range(terms))
    error = 2*r**(2*terms+1)/(F(2*terms+1)*(1-r*r))
    return lower, lower+error


def sqrt_interval(x, bits=200):
    require(x >= 0, "negative square root")
    if not x:
        return F(0), F(0)
    scale = 1 << bits
    k = isqrt((x.numerator*scale*scale)//x.denominator)
    lower, upper = F(k, scale), F(k+1, scale)
    require(lower*lower <= x <= upper*upper, "square root enclosure failed")
    return lower, upper


def gamma_integral_at_rational(x):
    """Enclose integral_0^x sqrt(u)exp(-u)du, for rational x>=0.

    Taylor polynomials of degrees 100 and 101 bound exp(-u) from above and
    below for every u>=0, by the sign of the Lagrange remainder. Integrate
    them exactly, factoring x*sqrt(x). No alternating-tail heuristic is used.
    """
    if x <= 0:
        return F(0), F(0)
    term, total = F(1), F(0)
    upper_polynomial = None
    for k in range(102):
        total += term*F(2, 2*k+3)
        if k == 100:
            upper_polynomial = total
        term *= -x/F(k+1)
    lower_polynomial = total
    require(lower_polynomial >= 0, "fixed Taylor order insufficient")
    root_low, root_high = sqrt_interval(x)
    return x*root_low*lower_polynomial, x*root_high*upper_polynomial


@lru_cache(maxsize=None)
def gamma_at_log_power(multiplier):
    if multiplier <= 0:
        return F(0), F(0)
    lo, hi = log2_interval()
    # The integral is increasing, so use opposite argument endpoints.
    return (gamma_integral_at_rational(multiplier*lo)[0],
            gamma_integral_at_rational(multiplier*hi)[1])


def interval_combination(coefficients, intervals):
    lo = hi = F(0)
    for c, (a, b) in zip(coefficients, intervals):
        lo += c*(a if c >= 0 else b)
        hi += c*(b if c >= 0 else a)
    return lo, hi


def round_out(interval, digits=30):
    scale = 10**digits
    lo, hi = interval
    return [str(F((lo*scale).__floor__(), scale)),
            str(F((hi*scale).__ceil__(), scale))]


def energy_checks():
    f = [(F(1), F(1, 5)), (F(4), F(4, 5))]
    g = [(F(2), F(1, 2)), (F(8), F(1, 2))]
    require(sum(m for v, m in f) == sum(m for v, m in g) == 1, "mass normalization failed")
    def hinge(distribution, a):
        return sum(m*max(F(0), 1-a/v) for v, m in distribution)
    gap = hinge(g, F(2))-hinge(f, F(2))
    require(gap == -F(1, 40), "hinge obstruction failed")
    polynomial = [0]*4
    for i, a in enumerate((-1, 1)):
        for j, b in enumerate((2, -3, 5)):
            polynomial[i+j] += a*b
    require(polynomial == [-2, 5, -8, 5], "Renyi polynomial factorization failed")
    require((-3)**2-4*5*2 == -31, "quadratic positivity certificate failed")
    require(F(1, 2)+3*F(1, 2)-2*F(4, 5) == F(2, 5), "Shannon identity failed")
    # Exact checks of all irrational constant comparisons used by the proof.
    require(F(6, 16) > F(9, 25), "sqrt(6)/4 > 3/5 failed")
    require(F(1, 2) > F(9, 25), "1/sqrt(2) > 3/5 failed")
    require(2 < 9, "2/5-(1+sqrt(2))/10 > 0 failed")
    records = []
    minimum = None
    coefficients = [-F(1, 5), F(1, 2), -F(4, 5), F(1, 2)]
    for k in range(-20, 12):
        exponent = F(k, 4)  # threshold a=2**exponent
        values = [gamma_at_log_power(F(j)-exponent) for j in range(4)]
        interval = interval_combination(coefficients, values)
        require(interval[0] > 0, f"Gamma-order sample failed at exponent {exponent}")
        require(interval[1]-interval[0] < F(1, 10**40), "enclosure too wide")
        minimum = interval[0] if minimum is None else min(minimum, interval[0])
        records.append([str(exponent), *round_out(interval)])
    encoded = json.dumps(records, separators=(",", ":")).encode()
    return {"hinge_gap_at_2": str(gap), "gamma_threshold_samples": len(records),
            "all_order_Renyi_factorization": "PASS",
            "gamma_samples_sha256": hashlib.sha256(encoded).hexdigest(),
            "sample_unnormalized_gap_lower": str(F((minimum*10**12).__floor__(), 10**12))}


def main():
    result = geometry_checks()
    result.update(energy_checks())
    result["status"] = "RANK_ABEL_CHECKS_PASS"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
