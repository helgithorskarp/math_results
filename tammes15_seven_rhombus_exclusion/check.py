#!/usr/bin/env python3
"""Exact auxiliary arithmetic for PROOF.md; CPython >=3.11, stdlib only.

No float, solver, external dataset, or planar-graph enumeration is used.
The geometric proof is written mathematics, not formalized by this script.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim([(p[i] if i < len(p) else 0)
                 + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def scale(p, a):
    return trim([a*x for x in p])


def mul(p, q):
    r = [F(0)]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return trim(r)


def power(p, n):
    require(n >= 0, "negative polynomial power")
    r = (F(1),)
    for _ in range(n):
        r = mul(r, p)
    return r


def derivative(p):
    return trim([i*p[i] for i in range(1, len(p))] or [0])


def evaluate(p, x):
    r = F(0)
    for a in reversed(p):
        r = r*x+a
    return r


def bernstein(p, lo, hi):
    """Exact Bernstein coefficients of p on [lo,hi]."""
    require(lo < hi, "empty interval")
    a = (F(0),)
    for v in reversed(p):
        a = add(mul(a, (lo, hi-lo)), (v,))
    n = len(p)-1
    a += (F(0),)*(n+1-len(a))
    return tuple(sum((a[k]*F(comb(j,k), comb(n,k))
                      for k in range(j+1)), F(0)) for j in range(n+1))


def root_reduce(p):
    """Remainder of p in Q[c]/(c^2-1/3), as (constant, c coefficient)."""
    return (sum((v/F(3)**(i//2) for i,v in enumerate(p) if i % 2 == 0), F(0)),
            sum((v/F(3)**(i//2) for i,v in enumerate(p) if i % 2 == 1), F(0)))


def arithmetic():
    c, one, H, D = trim((0,1)), trim((1,)), trim((1,2)), trim((1,2,-1))
    P = add(power(D,2), scale(mul(H,power(c,4)),4))
    N = add(add(mul(mul(c,H),derivative(D)), scale(mul(c,D),-1)),
            scale(mul(H,D),-2))
    require(N == trim((-2,-7,-6,1)), "y derivative numerator")
    fprime = add(P,scale(mul(mul(c,(1,1)),N),8))
    require(fprime == trim((1,-12,-70,-108,-35,16)), "(2y-alpha)' identity")
    bcoef = bernstein(fprime,F(1,2),F(3,5))
    require(all(v < 0 for v in bcoef), "independent negative Bernstein certificate")

    endpoint = F(4,7)
    h2 = evaluate(H,endpoint)
    d = evaluate(D,endpoint)
    U, R = d*d, 4*h2*endpoint**4
    cosine_margin = 2*(1+endpoint)*(U-R)**2-(U+R)**2
    require(U > R > 0, "cosine branch")
    require(cosine_margin == F(257867775,1977326743), "2y>pi+alpha endpoint")

    # Polynomial complex multiplication in Q[c,ih], with (ih)^2=-H.
    real, imag = one, trim((0,))
    for _ in range(6):
        real, imag = (add(mul(real,c),scale(mul(H,imag),-1)),
                      add(real,mul(imag,c)))
    R6 = add(add(power(c,6),scale(mul(power(c,4),H),-15)),
             add(scale(mul(power(c,2),power(H,2)),15),scale(power(H,3),-1)))
    N6 = add(add(scale(power(c,5),6),scale(mul(power(c,3),H),-20)),
             scale(mul(c,power(H,2)),6))
    require((real,imag) == (R6,N6), "sixth-power trigonometric identity")
    r6,n6 = evaluate(R6,endpoint),evaluate(N6,endpoint)
    require(r6 == F(1089271,117649) and n6 == F(136344,16807), "endpoint sixth power")
    square_margin = r6*r6-endpoint*h2*n6*n6
    require(square_margin == F(71130131281,13841287201), "K<b endpoint")
    require(r6 > 0 and n6 > 0 and square_margin > 0, "positive tangent branch")

    # The old w=A/2 root condition, followed by the new incompatible equality.
    root_equation = add(mul(power(c,2),(1,3)),scale(mul(H,(1,-1)),-1))
    require(root_equation == mul((1,1),(-1,0,3)), "w=A/2 root factor")
    last_equation = add(mul((1,0,-2),power(D,2)),scale(mul(H,power(c,4)),-4))
    require(root_reduce(last_equation) == (F(4,27),F(0)), "last equation is nonzero at c^2=1/3")
    require(root_reduce(add(scale(power(D,2),3),scale(H,-4))) == (F(4,3),F(0)),
            "3D^2-4H exact reduction")

    diagonal_num = add(mul(power(c,2),(3,2)),(-1,))
    require(diagonal_num == mul((-1,2),power((1,1),2)), "diagonal numerator factor")
    diagonal_bound = F(19,100)*F(319,200)**2/F(3,2)
    require(diagonal_bound == F(1933459,6000000) < F(1,3), "acute-leg cosine bound")
    refined_bound = F(1,5)*F(8,5)**2/(1+F(4,7)**2+2*F(4,7)**3)
    require(refined_bound == F(21952,72875) < F(1,3), "review-interval diagonal bound")
    require(F(1,9)-F(8,27) == -F(5,27), "obtuse-bisector base contradiction")
    require(F(119,319)**2 < F(1,7) and F(10,7)**2 > 2, "alpha>3pi/8 comparison")
    require(F(3,8)**2 < F(1,7), "review-interval alpha comparison")
    return {
        "two_y_minus_alpha_derivative_coefficients": list(map(str,fprime)),
        "negative_Bernstein_coefficients": list(map(str,bcoef)),
        "two_y_endpoint_cosine_margin": str(cosine_margin),
        "K_endpoint_tangent_margin": str(square_margin),
        "last_equation_remainder_mod_c_squared_minus_third": ["4/27","0"],
        "three_D_squared_minus_four_H_remainder": ["4/3","0"],
        "diagonal_cosine_upper_bound": str(diagonal_bound),
        "review_interval_diagonal_cosine_upper_bound": str(refined_bound),
        "forced_base_cosine_upper_bound": "-5/27",
    }


def covers():
    # Deficit columns: degree4 delta1, degree5 delta1, degree4 delta2, degree5 delta2.
    distributions = [v for v in product(range(3),repeat=4)
                     if v[0]+v[1]+2*v[2]+2*v[3] == 2]
    all_profiles, no_exceptional5 = [],[]
    for a in range(6):
        n4,n5 = 11-2*a,a+4
        for v in distributions:
            if v[0]+v[2] > n4 or v[1]+v[3] > n5:
                continue
            item = [a,n4,n5,*v]
            all_profiles.append(item)
            if v[1] == v[3] == 0:
                no_exceptional5.append(item)
    require(len(distributions) == 5 and len(all_profiles) == 29, "initial deficit cover")
    require(len(no_exceptional5) == 11, "exceptional5 exclusion profile count")

    # Section 5.1's integer inequalities; later star geometry forces j=2.
    unpaired = []
    for h,j,s,B in product(range(3),range(7),range(8),range(16)):
        if j <= 6-h and max(0,2-j) <= B <= h-j-2*s:
            unpaired.append([h,j,s,B])
    require(unpaired == [[2,0,0,2],[2,1,0,1],[2,2,0,0]], "Section 5.1 cover")

    # Section 6: face count, x-pair parity, available degree5 x, and marked-y capacity.
    def admissible(a,j,l):
        return (2 <= a <= 4 and a <= j+2*l and (a-j) % 2 == 0
                and a+4-j-2*l >= 0 and a+4+j <= 7+l)
    below = [[a,j,l] for a,j,l in product(range(2,5),range(3),range(3))
             if admissible(a,j,l) and j == l]
    less = [[a,0,0] for a in range(2,5) if admissible(a,0,0)]
    greater = [[a,j,0] for a,j in product(range(2,5),range(3)) if admissible(a,j,0)]
    require(less == greater == [], "u different from r0 capacity contradiction")
    require(below == [[2,2,2],[3,1,1]], "u=r0 exact surviving cover")
    return {
        "deficit_columns": ["n4_delta1","n5_delta1","n4_delta2","n5_delta2"],
        "five_deficit_distributions": [list(v) for v in distributions],
        "initial_degree_deficit_profiles": len(all_profiles),
        "profiles_without_exceptional_degree5": len(no_exceptional5),
        "Section_5_1_integer_cover_h_j_s_B": unpaired,
        "below_x_face_final_cover_a_j_l": below,
        "u_not_equal_r0_integer_cover": [],
        "geometry_status": "all q=7 branches excluded by the written PROOF.md",
        "enumeration_scope": "integer profiles/capacities only; no planar graphs enumerated",
    }


def selftest():
    """Definition checks differ from the Horner/Bernstein conversion."""
    p = trim((1,-12,-70,-108,-35,16))
    lo,hi = F(1,2),F(3,5)
    coeff = bernstein(p,lo,hi)
    n = len(p)-1
    comparisons = 0
    for j in range(17):
        t = F(j,16)
        from_basis = sum((coeff[k]*comb(n,k)*t**k*(1-t)**(n-k)
                          for k in range(n+1)),F(0))
        x = lo+(hi-lo)*t
        from_definition = sum((a*x**i for i,a in enumerate(p)),F(0))
        require(from_basis == from_definition, "Bernstein definition check")
        comparisons += 1
    # Independent binomial form of (c+i sqrt(H))^6 at rational c.
    for c in [F(1,2),F(4,7),F(119,200)]:
        H = 1+2*c
        real = sum((F(comb(6,k))*(-1)**(k//2)*c**(6-k)*H**(k//2)
                    for k in range(0,7,2)),F(0))
        imag_over_h = sum((F(comb(6,k))*(-1)**((k-1)//2)*c**(6-k)*H**((k-1)//2)
                           for k in range(1,7,2)),F(0))
        require(real == c**6-15*c**4*H+15*c*c*H*H-H**3, "binomial real part")
        require(imag_over_h == 6*c**5-20*c**3*H+6*c*H*H, "binomial imaginary part")
        comparisons += 2
    return {"exact_definition_comparisons":comparisons}


def main():
    require(sys.argv[1:] in ([],["--selftest"]), "usage: check.py [--selftest]")
    result = {"agent":"six-tammes-1","role":"researcher",
              "arithmetic":"exact integers and Fraction; no floating point",
              "arithmetic_checks":arithmetic(),"integer_covers":covers(),
              "global_optimality_claim":False,"formalized_geometry":False}
    if sys.argv[1:] == ["--selftest"]:
        result["selftest"] = selftest()
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
