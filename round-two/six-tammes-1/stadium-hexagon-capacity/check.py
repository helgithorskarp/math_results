"""Exact enclosures for five spherical-perimeter inequalities; geometry is separate."""
from fractions import Fraction as Q
from math import isqrt
import json

BITS = 80
TERMS = 32
GRID = 10**6


def need(ok, text):
    if not ok:
        raise ValueError(text)


def sqrt_bounds(x):
    need(x >= 0, "negative square-root argument")
    scale = 1 << BITS
    m = isqrt(x.numerator*scale*scale//x.denominator)
    lo = Q(m, scale)
    hi = lo if m*m*x.denominator == x.numerator*scale*scale else Q(m+1, scale)
    need(lo*lo <= x <= hi*hi, "invalid exact square-root bracket")
    return lo, hi


def atan_bounds(x, terms=TERMS):
    need(0 <= x <= 1, "atan argument outside declared domain")
    power = x
    total = Q(0)
    for j in range(terms):
        total += (-1)**j*power/(2*j+1)
        power *= x*x
    tail = power/(2*terms+1)
    return (total, total+tail) if terms % 2 == 0 else (total-tail, total)


def acos_bounds(x):
    lo, hi = (x, x) if isinstance(x, Q) else x
    need(0 <= lo <= hi <= 1, "acos argument outside [0,1]")
    # acos is decreasing; acos(t)=2atan(sqrt((1-t)/(1+t))).
    a = sqrt_bounds((1-hi)/(1+hi))[0]
    b = sqrt_bounds((1-lo)/(1+lo))[1]
    return 2*atan_bounds(a)[0], 2*atan_bounds(b)[1]


def scaled(x, s):
    need(s >= 0, "negative interval scale")
    return x[0]*s, x[1]*s


def rounded(x):
    lo = Q((x[0]*GRID).__floor__(), GRID)
    hi = Q((x[1]*GRID).__ceil__(), GRID)
    need(lo <= x[0] <= x[1] <= hi, "outward rounding")
    return lo, hi


def stadium_bounds(c, e, acos=acos_bounds):
    den = 1+c-e
    S2 = 1-2*c*c/den
    V2 = (1-c)*den/(4*c*c)
    A2 = (den-2*c*c)*(1-c)/(2*c*c*(1+c))
    need(0 < S2 < 1 and 0 < V2 < 1 and 0 < A2 < 1, "stadium branch domain")
    sr = sqrt_bounds(S2)
    alpha = acos(sqrt_bounds(A2))
    gamma = acos(sqrt_bounds(1-V2))
    need(alpha[0] > 0 and gamma[0] > 0, "positive angles")
    return 4*gamma[0]+4*sr[0]*alpha[0], 4*gamma[1]+4*sr[1]*alpha[1]


def cell_rows(acos=acos_bounds):
    e = Q(1, 100)
    endpoints = [Q(i, 125) for i in range(70, 76)]
    need(endpoints[0] == Q(14, 25) and endpoints[-1] == Q(3, 5), "domain endpoints")
    rows = []
    for a, b in zip(endpoints, endpoints[1:]):
        need(b-a == Q(1, 125), "contiguous fixed cells")
        stadium = stadium_bounds(b, e, acos)
        budget = scaled(acos(a-e), 6)
        p, length = rounded(stadium), rounded(budget)
        gap = p[0]-length[1]
        need(gap > Q(1, 25), "strict perimeter exclusion margin")
        rows.append({"c_lower":str(a), "c_upper":str(b),
                     "stadium_lower_at_upper":str(p[0]), "stadium_upper_at_upper":str(p[1]),
                     "six_edges_lower_at_lower":str(length[0]), "six_edges_upper_at_lower":str(length[1]),
                     "gap_lower":str(gap)})
    need(len(rows) == 5, "complete five-cell cover")
    return rows


def main():
    lo, hi, e = Q(14, 25), Q(3, 5), Q(1, 100)
    need(lo-e == Q(11, 20) > Q(1, 2), "hemisphere threshold")
    need(1-hi-e == Q(39, 100) > 0, "automatic simplicity")
    need(min(1+c-e-2*c*c for c in [lo,hi]) == Q(87, 100) > 0,
         "positive cap radius on whole domain by concavity")
    need(10*lo-e > 0, "stadium-domain polynomial is increasing")
    domain = 5*lo*lo-e*lo+e-1
    need(domain == Q(1431, 2500) > 0, "hemispherical stadium domain")
    rows = cell_rows()
    # This scalar route fails at the wider tolerance, not a geometric counterexample.
    e_bad = Q(1, 40)
    p = stadium_bounds(lo, e_bad)
    budget = scaled(acos_bounds(lo-e_bad), 6)
    bad_gap = rounded((p[0]-budget[1],p[1]-budget[0]))
    need(bad_gap[1] < 0, "wider tolerance control")
    need(sqrt_bounds(Q(9,16)) == (Q(3,4),Q(3,4)), "perfect square control")
    need(acos_bounds(Q(1)) == (0,0), "zero-angle control")
    try:
        acos_bounds(Q(1001,1000))
    except ValueError:
        pass
    else:
        raise ValueError("out-of-domain angle not rejected")
    print(json.dumps({"author":"six-tammes-1","role":"researcher",
                      "evidence":"exact endpoint enclosures; continuous geometry is a written proof",
                      "sqrt_bits":BITS,"atan_terms":TERMS,"outward_grid":GRID,
                      "edge_tolerance":"1/100","uniform_perimeter_gap_lower":"1/25",
                      "cells":rows,"stadium_domain_polynomial_lower":str(domain),
                      "wider_tolerance_1_40_same_endpoint_gap":[str(z) for z in bad_gap]},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
