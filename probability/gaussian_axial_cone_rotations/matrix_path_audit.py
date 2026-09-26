#!/usr/bin/env python3
"""Exact supplementary audits for MATRIX_PATHS.md; standard library only.

No sampled path or floating sign proves the universal assertions. Default
prints compact deterministic JSON; --check compares the published fixture.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial, isqrt
from pathlib import Path

from verify import (Poly, affine_rank, conjugate_product, determinant, dist2,
                    dot, hull, neg, pi_bound_audit, rank, require)
from composition_audit import certificate_values, diagonal, dual_vertices


BASE = Path(__file__).resolve().parent
ORIGINAL = "50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4"


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def transpose(a):
    return list(zip(*a))


def multiply(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def reduce_lift(poly):
    """Exact quotient: S^2=1-C^2, h^2=4r(1-r), d^2=1-c^2.

    Variables, by index: C,S,r,h,c,d,x,y,z,unused,unused.
    Do not invoke verify.Poly.reduced(), whose relations are different.
    """
    result = {}

    def visit(m, v):
        for index in (1, 3, 5):
            if m[index] >= 2:
                base = list(m)
                base[index] -= 2
                if index == 1:
                    visit(tuple(base), v)
                    base[0] += 2
                    visit(tuple(base), -v)
                elif index == 3:
                    base[2] += 1
                    visit(tuple(base), 4 * v)
                    base[2] += 1
                    visit(tuple(base), -4 * v)
                else:
                    visit(tuple(base), v)
                    base[4] += 2
                    visit(tuple(base), -v)
                return
        result[m] = result.get(m, F(0)) + v

    for m, v in poly.terms.items():
        visit(m, v)
    return Poly(result)


def symbolic_lift():
    C, S, r, h, c, d = [Poly.var(i) for i in range(6)]
    one, zero = Poly.const(1), Poly.const(0)
    rot = [[C, -S], [S, C]]
    a = multiply(multiply(rot, [[one, zero], [zero, 2*r-1]]), rot)
    rows = [[a[0][0], a[0][1], zero], [a[1][0], a[1][1], zero],
            [zero, zero, c], [h*S, h*C, zero], [zero, zero, d]]
    gram = multiply(transpose(rows), rows)
    identities = []
    for i in range(3):
        for j in range(i, 3):
            require(not reduce_lift(gram[i][j] - int(i == j)).terms,
                    f"lift Gram entry failed: {i},{j}")
            identities.append(f"Gram_{i}{j}")
    ar, ai, b = r*(C*C-S*S), 2*r*C*S, 1-r
    direct = [[ar+b, -ai], [ai, ar-b]]
    for i, j in product(range(2), repeat=2):
        require(not reduce_lift(a[i][j]-direct[i][j]).terms,
                "complex and rotated-diagonal forms disagree")
        identities.append(f"complex_matrix_{i}{j}")
    # The cross-pair derivative identity is bilinear and has no lift term.
    ax, ay, bx, by, az, bz, a11, a12, a21, a22, cc = [Poly.var(i) for i in range(11)]
    bracket = ax*(a11*bx+a12*by)+ay*(a21*bx+a22*by)+cc*az*bz
    require(not (bracket.diff(6)-ax*bx).terms, "cross derivative a11")
    require(not (bracket.diff(10)-az*bz).terms, "cross derivative c")
    identities += ["cross_derivative_a11", "cross_derivative_c"]
    # Independent free-ring identities for the general real-linear norm formula.
    ar, ai, br, bi = [Poly.var(i) for i in range(4)]
    general = [[ar+br, -ai+bi], [ai+bi, ar-br]]
    gg = multiply(transpose(general), general)
    alpha2, beta2 = ar*ar+ai*ai, br*br+bi*bi
    require(not (gg[0][0]+gg[1][1]-2*(alpha2+beta2)).terms,
            "general singular-value trace identity")
    require(not (gg[0][0]*gg[1][1]-gg[0][1]*gg[1][0]
                 -(alpha2-beta2)*(alpha2-beta2)).terms,
            "general singular-value determinant identity")
    identities += ["singular_trace", "singular_determinant"]
    missing_transverse = [row for i, row in enumerate(rows) if i != 3]
    bad = multiply(transpose(missing_transverse), missing_transverse)
    require(any(reduce_lift(bad[i][i]-1).terms for i in range(3)),
            "missing transverse lift control was accepted")
    return {"identities": identities, "count": len(identities),
            "relations": ["S^2=1-C^2", "h^2=4r(1-r)", "d^2=1-c^2"],
            "missing_transverse_coordinate": "rejected"}


def real_matrix_checks():
    """Direct real matrices from rational phases, distinct from the quotient audit."""
    phases = [(F(1), F(0)), (F(3,5), F(4,5)), (F(0), F(1)),
              (-F(3,5), F(4,5)), (-F(1), F(0))]
    radii = [(F(0), F(0)), (F(1), F(0)), (F(4,5), F(4,5)),
             (F(1,2), F(1)), (F(1,5), F(4,5)), (F(1,10), F(3,5))]
    axes = phases
    checked = 0
    for (C,S), (r,h), (c,d) in product(phases, radii, axes):
        require(C*C+S*S == c*c+d*d == 1 and h*h == 4*r*(1-r),
                "invalid rational lift parameters")
        ar, ai, b = r*(C*C-S*S), 2*r*C*S, 1-r
        rows = [[ar+b, -ai, F(0)], [ai, ar-b, F(0)],
                [F(0),F(0),c], [h*S,h*C,F(0)], [F(0),F(0),d]]
        gram = multiply(transpose(rows), rows)
        require(gram == [[F(i == j) for j in range(3)] for i in range(3)],
                "direct rational Gram failure")
        checked += 1
    for C,S,c,sign in [(F(0),F(1),F(-1),-1), (F(1),F(0),F(1),1)]:
        rows = [[C*C-S*S,-2*C*S,0],[2*C*S,C*C-S*S,0],
                [0,0,c],[0,0,0],[0,0,0]]
        require(rows == [[F(sign if i == j else 0) for j in range(3)]
                          for i in range(5)], "wrong motion endpoint")
    require(rank(diagonal((F(1),)*3)) == 3,
            "six-dimensional straight Gram shortcut control")
    return {"exact_rational_frames": checked, "endpoint_frames_checked": 2,
            "straight_midpoint_defect_rank": 3,
            "straight_R5_shortcut": "rejected: rank exceeds two"}


def rational_budgets():
    pi_bound_audit()
    pi_upper = "22/7"
    # Integral geometric-series truncation on [0,1]: even term count is a lower bound.
    pi_lower = 4*sum((F((-1)**j, 2*j+1) for j in range(128)), F(0))
    require(pi_lower > F(25,8), "insufficient exact pi lower bound")
    cosine_lower = sum((F((-1)**j, factorial(2*j)) for j in range(6)), F(0))
    cosine_upper = sum((F((-1)**j, factorial(2*j)) for j in range(5)), F(0))
    require(0 < cosine_lower < cosine_upper < 1, "bad cosine enclosure")
    require(2*(1+cosine_upper) < pi_lower, "new length not certified below pi")
    rho, tangent_height = F(4,5), F(12,25)
    left, right = (-rho*rho,tangent_height), (rho*rho,tangent_height)
    require(dot(left,left) == rho*rho and dot(right,right) == rho*rho,
            "tangent point is off the inner circle")
    require(dot((left[0]+1,left[1]),left) == 0
            and dot((right[0]-1,right[1]),right) == 0,
            "tangent direction not perpendicular to radius")
    require(dist2((-F(1),F(0)),left) == F(9,25)
            and dist2((F(1),F(0)),right) == F(9,25), "wrong tangent length")
    angle = F(9,14)
    lower = sum(((-1)**j*angle**(2*j)/factorial(2*j) for j in range(4)),F(0))
    require(lower-rho == F(232207,602362880), "cosine lower margin changed")
    length_bound = F(8,5)+rho*(F(22,7)-2*angle)
    kappa = F(81,125)
    require(length_bound == F(108,35), "rational path length bound changed")
    require(2-kappa*length_bound == F(2,4375), "positive cost reserve changed")
    require(kappa*F(25,8)-2 == F(1,40), "old circular budget not excluded")
    return {"rho":str(rho), "tangent_points":[list(map(str,left)),list(map(str,right))],
            "pi_upper":pi_upper, "pi_lower_coarse":"25/8",
            "pi_lower_series_terms":128, "cos_one_lower":str(cosine_lower),
            "cos_one_upper":str(cosine_upper),
            "optimal_length_formula":"2(1+cos(1))",
            "optimal_length_upper":str(2*(1+cosine_upper)),
            "arccos_rho_lower":str(angle), "cosine_lower_margin":str(lower-rho),
            "path_length_upper":str(length_bound), "kappa":str(kappa),
            "new_cost_reserve":str(2-kappa*length_bound),
            "old_cost_excess_lower":str(kappa*F(25,8)-2)}


def finite_fixture():
    data = (BASE/"EXPECTED.json").read_bytes()
    require(sha256(data).hexdigest() == ORIGINAL, "original directions changed")
    directions = [tuple(map(F,row)) for row in json.loads(data)["fixture"]["directions"]]
    p,q = F(4,5),F(81,100)
    a = [(p*x,p*y,F(1)) for x,y in directions]
    b = [(q*x,q*y,F(1)) for x,y in directions]
    origin = (F(0),)*3
    source,target = [origin]+a+[neg(v) for v in b], [origin]+a+b
    require(len(set(source)) == len(set(target)) == 25, "fixture collision")
    records = []
    for i,j in combinations(range(25),2):
        loss=dist2(source[i],source[j])-dist2(target[i],target[j])
        expected = 4*dot(a[i-1],b[j-13]) if 1 <= i <= 12 < j else 0
        require(loss == expected and loss >= 0, "fixture is not the claimed contraction")
        records.append([i,j,str(loss)])
    require(sum(F(row[2])>0 for row in records) == 144, "strict-pair count")
    paired=[u+v for u,v in zip(source,target)]
    require(affine_rank(paired)==6 and rank(a)==rank(b)==3, "fixture ranks")
    indices=(0,3,6)
    six=[list(a[i]+a[i]) for i in indices]+[list(neg(b[i])+b[i]) for i in indices]
    det6=determinant(six)
    require(det6 != 0, "vanishing paired minor")
    products=[tuple(p*q*t for t in conjugate_product(u,v))
              for u,v in product(directions,repeat=2)]
    polygon=hull(products)
    require(len(polygon)==20, "changed product hull")
    # Integer lower square roots, followed by their exact squared certificates.
    lengths=[]
    for u,v in zip(polygon,polygon[1:]+polygon[:1]):
        square=dist2(u,v)
        n=isqrt(square.numerator*10**12//square.denominator)
        lower=F(n,10**6)
        require(lower*lower <= square < (lower+F(1,10**6))**2,
                "incorrect integer square-root enclosure")
        lengths.append(lower)
    perimeter_lower=sum(lengths,F(0))
    require(perimeter_lower == F(253379,62500) and perimeter_lower>4,
            "finite perimeter did not escape the old test")
    dual_a,_=dual_vertices(directions,p)
    dual_b,_=dual_vertices(directions,q)
    h=diagonal((F(-8),F(-8),F(15)))
    values=certificate_values(dual_a,dual_b,h)
    require(min(values)>0, "dual certificate lacks strict margin")
    invalid=[]
    for name,bad in [("negative generator",diagonal((F(-1),F(-1),F(1)))),
                     ("nonnegative trace",diagonal((F(0),F(0),F(1))))]:
        try:
            certificate_values(dual_a,dual_b,bad)
        except ValueError:
            invalid.append(name+" rejected")
        else:
            raise ValueError("bad dual control accepted")
    return {"p":str(p),"q":str(q),"original_expected_sha256":ORIGINAL,
            "directions":len(directions),"sites":25,"pairs":len(records),
            "strict_pairs":144,"zero_pairs":156,
            "minimum_strict_loss":str(min(F(row[2]) for row in records if F(row[2])>0)),
            "pair_records_sha256":sha256(encode(records)).hexdigest(),
            "paired_affine_rank":6,"paired_minor":str(det6),
            "product_hull_vertices":len(polygon),"perimeter_lower":str(perimeter_lower),
            "perimeter_excess_lower":str(perimeter_lower-4),
            "dual_pairs":len(values),"dual_certificate_diagonal":[-8,-8,15],
            "dual_trace":-1,"dual_minimum":str(min(values)),
            "dual_values_sha256":sha256(encode(list(map(str,values)))).hexdigest(),
            "invalid_controls":invalid}


def run():
    return {"claim":"supplementary exact audits for the transverse matrix-path theorem",
            "trust_boundary":"universal path, length proof and external bridges are written mathematics",
            "symbolic":symbolic_lift(),"real_matrices":real_matrix_checks(),
            "budgets":rational_budgets(),"fixture":finite_fixture()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    output=encode(run())
    if args.check:
        require(output == (BASE/"EXPECTED_MATRIX_PATHS.json").read_bytes(),
                "matrix-path expected output mismatch")
        print("AXIAL_MATRIX_PATH_AUDITS_PASS",sha256(output).hexdigest())
    else:
        print(output.decode(),end="")


if __name__ == "__main__":
    main()
