#!/usr/bin/env python3
"""Exact supporting checks for the uniform dominant-atom window.

Python >=3.11, standard library only. No floating arithmetic or Gaussian
quadrature is used. The continuum theorem remains the written proof.
"""

from fractions import Fraction as F
from math import factorial
import json


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def trim(p):
    return {k: v for k, v in p.items() if v}


def poly_add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return trim(out)


def poly_mul(p, q):
    out = {}
    for (a,b), u in p.items():
        for (c,d), v in q.items():
            out[a+c,b+d] = out.get((a+c,b+d), F(0)) + u*v
    return trim(out)


def scaled(p, x):
    return trim({k: x*v for k,v in p.items()})


def perturbation_polynomial():
    # The two indeterminates are c and L.
    u = {(1,0): F(1), (0,1): F(5)}
    v = {(0,0): F(72), (1,0): F(12), (0,1): F(20)}
    j = poly_add(scaled(v, 3), scaled(poly_mul(u, {(1,0): F(1),
                                                 (0,0): F(4)}), 2))
    p = poly_add({(0,0): F(4)}, u, j)
    expected = {(0,0): F(220), (1,0): F(45), (0,1): F(105),
                (2,0): F(2), (1,1): F(10)}
    require(p == expected, "P=4+U+J formal identity")
    value = sum((coefficient * 16**i * 8**j
                 for (i,j), coefficient in p.items()), F(0))
    require(value == 3572, "P at rho=1,L=8")
    return int(value)


def elementary_constants(p):
    # Exponential upper bound from its positive series and geometric tail.
    e_upper = sum((F(1, factorial(j)) for j in range(5)), F(0)) + F(1,100)
    require(e_upper < F(11,4), "e<11/4 from an explicit remainder")
    require(F(33,8)**2 > 17, "sqrt(17)<33/8")
    exp_bound = F(11,4)**5 * F(8,7)
    require(exp_bound == F(161051,896) and exp_bound < 256,
            "exp(41/8) upper bound")
    alpha = F(1, 2**21)
    require(alpha <= F(1,4), "dominant mass range")
    budget = 2 * alpha * p * exp_bound
    require(budget == F(143818543,234881024) and budget < 1,
            "posterior curvature budget")
    e_lower = sum((F(1, factorial(j)) for j in range(4)), F(0))
    require(e_lower == F(8,3) and e_lower**8 > 2**11,
            "all dyadic thresholds enter the logarithmic window")
    require(1 - 2*alpha > F(3,4), "middle logarithmic distance from peak")
    require(F(3,4)**3 > F(1,2)**2, "three-halves power lower bound")
    middle_constant = F(1, 2**11 * 2 * 243 * 12)
    require(middle_constant > F(1,2**24), "rational normalized middle margin")
    return {
        "P": p,
        "alpha": str(alpha),
        "exp_41_over_8_upper": str(exp_bound),
        "curvature_budget_product_upper": str(budget),
        "hinge_floor_u": "1/2048",
        "middle_interval_u": ["1/2048", "1/4"],
        "certified_H_over_d_lower": "1/16777216",
    }


def perturbation_controls():
    # Rational sanity controls; the universal interval estimates are
    # established by the inequalities in PROOF.md, not by this grid.
    n = 0
    for k in range(1,17):
        delta = F(k,64)
        require((1+delta)**2 * (1-delta) >= 1, "radial inverse budget")
        for ia in range(17):
            a = 1-delta+delta*F(ia,16)
            for ib in range(17):
                b = 1-delta+delta*F(ib,16)
                q = 1+delta
                require(0 <= q**3/a**2-1 <= 12*delta,
                        "linear tilt coefficient budget")
                require(abs(a**-2-1) <= 4*delta, "inverse square budget")
                require(abs(b*a**-3-1) <= 11*delta, "inverse cube budget")
                require(abs(q*q*(5/a**2-b/a**3)-4) <= 71*delta,
                        "radial geometric coefficient budget")
                n += 1
    return n


def stereographic(u, v):
    u, v = F(u), F(v)
    denominator = 1+u*u+v*v
    return ((1-u*u-v*v)/denominator, 2*u/denominator, 2*v/denominator)


def distance_squared(x, y):
    return sum(((a-b)**2 for a,b in zip(x,y)), F(0))


def determinant(matrix):
    a = [list(map(F,row)) for row in matrix]
    product = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i,len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i],a[pivot] = a[pivot],a[i]
            product = -product
        entry = a[i][i]
        product *= entry
        for j in range(i+1,len(a)):
            ratio = a[j][i]/entry
            for k in range(i+1,len(a)):
                a[j][k] -= ratio*a[i][k]
            a[j][i] = F(0)
    return product


def permutation_determinant(matrix):
    # Independent integer/rational Leibniz evaluation of the small determinant.
    from itertools import permutations
    total = F(0)
    for perm in permutations(range(len(matrix))):
        inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                         for j in range(i+1,len(perm)))
        value = F((-1)**inversions)
        for i,j in enumerate(perm):
            value *= matrix[i][j]
        total += value
    return total


def zero_radial_loss_control():
    zero = (F(0),)*3
    xs = [zero] + [tuple(map(F,x)) for x in
                   [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
    parameters = [(0,0),(F(1,8),0),(0,F(1,8)),(F(-1,8),0),
                  (0,F(-1,8)),(F(1,8),F(1,8))]
    ys = [zero] + [stereographic(u,v) for u,v in parameters]
    require(all(isinstance(c,F) for x in xs+ys for c in x), "exact coordinates")
    require(all(distance_squared(x,zero)==distance_squared(y,zero)==1
                for x,y in zip(xs[1:],ys[1:])), "zero anchor losses")
    losses = {(i,j): distance_squared(xs[i],xs[j])-distance_squared(ys[i],ys[j])
              for i in range(7) for j in range(i)}
    require(all(v >= 0 for v in losses.values()), "finite contraction")
    rare = [value for (i,j),value in losses.items() if j>0]
    require(min(rare) == F(730,429), "minimum rare-pair loss")
    matrix = [x+y for x,y in zip(xs[1:],ys[1:])]
    det = determinant(matrix)
    require(det == permutation_determinant(matrix) == F(-15616,9062625),
            "paired-rank-six determinant")
    rare_mean = 2*sum(rare,F(0))/36
    require(rare_mean == F(2366536,1254825), "rare-pair expectation")
    alpha = F(1,2**21)
    weights = [1-alpha]+[alpha/6]*6
    loss = 2*sum((weights[i]*weights[j]*value
                  for (i,j),value in losses.items()),F(0))
    require(loss == alpha*alpha*rare_mean == F(295817,689847339162009600),
            "loss begins at order alpha squared")
    return {
        "source": [[str(c) for c in x] for x in xs],
        "target": [[str(c) for c in y] for y in ys],
        "weights": [str(w) for w in weights],
        "pairs_checked": len(losses),
        "anchor_losses": [str(losses[i,0]) for i in range(1,7)],
        "min_rare_loss": str(min(rare)),
        "paired_determinant": str(det),
        "mean_rare_loss": str(rare_mean),
        "mean_full_loss": str(loss),
        "middle_hinge_lower": str(loss/F(2**24)),
        "scope": "finite control under the uniform analytic theorem; no tail sign below 1/2048",
    }


def main():
    p = perturbation_polynomial()
    result = {
        "schema": "uniform-dominant-atom-window-v1",
        "status": "EXACT_MIDDLE_CONSTANTS_PASS",
        "formal_budget_identity": "P=4+U+3V+2U(c+4)",
        "constant_certificate": elementary_constants(p),
        "rational_perturbation_controls": perturbation_controls(),
        "zero_radial_loss_control": zero_radial_loss_control(),
        "trust_boundary": "analytic continuum proof is written, not formalized or numerically sampled",
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
