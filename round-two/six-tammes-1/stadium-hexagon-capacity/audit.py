"""Separate exact arcsin/Machin enclosure of the five endpoint comparisons.

No primary-checker import. This is a second implementation by the author,
sharing CPython/Fraction, not an independent researcher review.
"""
from fractions import Fraction as Q
import json

STEPS = 96
TERMS = 64
GRID = 10**6


def need(ok, text):
    if not ok:
        raise ValueError(text)


def root(x):
    need(0 <= x <= 1, "audit root outside [0,1]")
    if x in (0, 1):
        return x, x
    a, b = Q(0), Q(1)
    for _ in range(STEPS):
        m = (a+b)/2
        if m*m == x:
            return m, m
        if m*m < x:
            a = m
        else:
            b = m
    need(a*a <= x <= b*b, "audit root bracket")
    return a, b


def atan_small(x):
    need(0 <= x <= Q(1,5), "Machin atan domain")
    power = x
    total = Q(0)
    for j in range(20):
        total += (-1)**j*power/(2*j+1)
        power *= x*x
    return total, total+power/41


def pi_bounds():
    a, b = atan_small(Q(1,5)), atan_small(Q(1,239))
    # tan(4atan(1/5))=120/119 and tan(4atan(1/5)-atan(1/239))=1.
    t = Q(120,119)
    need((t-Q(1,239))/(1+t/239) == 1, "Machin rational tangent identity")
    return 16*a[0]-4*b[1], 16*a[1]-4*b[0]


PI = pi_bounds()


def asin_positive(x):
    need(0 <= x <= Q(3,4), "positive-series endpoint domain")
    coefficient = Q(1)
    power = x
    total = Q(0)
    for n in range(TERMS):
        total += coefficient*power
        power *= x*x
        coefficient *= Q((2*n+1)**2,2*(n+1)*(2*n+3))
    return total, total+power/(1-x*x)


def angle(x):
    a, b = (x,x) if isinstance(x,Q) else x
    need(0 <= a <= b <= 1, "audit angle domain")
    if a == b == 1:
        return Q(0), Q(0)
    first, last = asin_positive(a), asin_positive(b)
    return PI[0]/2-last[1], PI[1]/2-first[0]


def perimeter(c, e):
    denominator = 1+c-e
    S2 = 1-2*c*c/denominator
    V2 = (1-c)*denominator/(4*c*c)
    A2 = (denominator-2*c*c)*(1-c)/(2*c*c*(1+c))
    need(0 < S2 < 1 and 0 < V2 < 1 and 0 < A2 < 1, "audit stadium domain")
    s = root(S2)
    alpha = angle(root(A2))
    gamma = angle(root(1-V2))
    need(alpha[0] > 0 and gamma[0] > 0, "audit positive angles")
    return 4*gamma[0]+4*s[0]*alpha[0], 4*gamma[1]+4*s[1]*alpha[1]


def rounded(x):
    a, b = Q((x[0]*GRID).__floor__(),GRID), Q((x[1]*GRID).__ceil__(),GRID)
    need(a <= x[0] <= x[1] <= b, "audit outward grid")
    return a,b


def main():
    e = Q(1,100)
    endpoints = [Q(i,125) for i in range(70,76)]
    rows = []
    for a,b in zip(endpoints,endpoints[1:]):
        p = rounded(perimeter(b,e))
        raw_l = angle(a-e)
        length = rounded((6*raw_l[0],6*raw_l[1]))
        gap = p[0]-length[1]
        need(gap > Q(1,25), "audit strict perimeter margin")
        rows.append({"c_lower":str(a), "c_upper":str(b),
                     "stadium_lower_at_upper":str(p[0]), "stadium_upper_at_upper":str(p[1]),
                     "six_edges_lower_at_lower":str(length[0]), "six_edges_upper_at_lower":str(length[1]),
                     "gap_lower":str(gap)})
    need(root(Q(9,16)) == (Q(3,4),Q(3,4)), "audit perfect square")
    need(3 < PI[0] < PI[1] < Q(22,7), "audit pi bounds")
    need(angle(Q(1)) == (0,0), "audit zero angle")
    bad = perimeter(Q(14,25),Q(1,40))
    bad_l = angle(Q(14,25)-Q(1,40))
    bad_gap = rounded((bad[0]-6*bad_l[1],bad[1]-6*bad_l[0]))
    need(bad_gap[1] < 0, "audit wider tolerance control")
    print(json.dumps({"author":"six-tammes-1", "role":"researcher",
                      "evidence":"separate exact series audit; geometric proof is external",
                      "root_bisection_steps":STEPS,"arcsin_terms":TERMS,
                      "pi_method":"Machin identity with two 20-term alternating atan brackets",
                      "outward_grid":GRID,"edge_tolerance":"1/100",
                      "uniform_perimeter_gap_lower":"1/25","cells":rows,
                      "wider_tolerance_1_40_same_endpoint_gap":[str(z) for z in bad_gap]},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
