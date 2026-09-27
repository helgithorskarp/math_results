#!/usr/bin/env python3
"""Exact controls for the written Brownian equality-contact example.

No Gaussian quadrature, path simulation or analytic theorem verification.
"""

import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def square_norm(v):
    return sum(x*x for x in v)


def exp_upper(x, degree):
    require(x >= 0 and degree >= 0, "positive exponential parameters")
    term = F(1)
    partial = term
    for j in range(1, degree+1):
        term *= x/j
        partial += term
    first_omitted = term*x/(degree+1)
    ratio = x/(degree+2)
    require(ratio < 1, "geometric remainder must converge")
    return partial + first_omitted/(1-ratio)


def audit():
    delta, kmax = F(1,8), F(1,256)
    smin = F(47,48)
    require(1-delta == F(7,8), "inner top-set radius")
    require(1+delta == F(9,8), "outer top-set radius")
    require((1-2*delta)/2 == F(3,8) > 0, "regular top boundary")
    corners = list(product((F(3,4), F(1)), (F(-1,8), F(1,8)), (F(-1,8), F(1,8))))
    max_norm = max(square_norm(z) for z in corners)
    max_difference = max(square_norm(tuple(a-b for a,b in zip(z,w))) for z in corners for w in corners)
    min_sum_first = min(z[0]+w[0] for z in corners for w in corners)
    require(max_norm == F(33,32), "box squared norm")
    require(max_difference == F(3,16) < F(1,4), "box difference norm")
    require(min_sum_first == F(3,2), "box sum coordinate")
    # Squared norms are convex in each coordinate; their maxima on the box
    # occur at vertices. The first-coordinate minimum is affine.
    require(2*max_norm == F(33,16) < 4, "bounded six-dimensional state")
    require(delta+F(1,2) == F(5,8), "target mean radius")
    require(F(3,2)-delta == F(11,8), "source mean radius")
    require(F(5,8)+F(1,4) == F(7,8), "strict target radius remains inside inner ball")
    require(F(11,8)-F(1,4) == F(9,8), "source remains outside outer ball")
    require(1-kmax*kmax/48 >= smin, "clock range")
    q_at_max = kmax*kmax/24
    one_tail = 3*q_at_max/F(1,4)**2
    require(one_tail == 2*kmax*kmax, "one marginal Markov tail")
    h_lower = 1-2*one_tail
    n_upper = max_norm-3*smin
    require(n_upper == -F(61,32), "noise energy bound")
    require(h_lower == 1-4*kmax*kmax > kmax/16, "first-hit amplitude")
    require(n_upper*h_lower < -1 < -kmax/4, "signed event margin")
    exponent = max_norm/smin
    require(exponent == F(99,94), "density exponent")
    exponential_upper = exp_upper(exponent, 12)
    require(exponential_upper < 4, "validated positive-series bound")
    require(2*F(22,7) < 7, "Archimedes bound implies 2pi<7")
    density_lower = F(1,4*7**3)
    box_volume = F(1,4)**6
    probability_lower = density_lower*box_volume
    require(box_volume == F(1,4096), "box volume")
    require(probability_lower == F(1,5619712), "state probability budget")
    require(probability_lower > kmax*kmax/96, "witness event probability")
    # Reject a consequential wrong threshold rather than only checking
    # a duplicate true equality. kappa=1 would fail this probability budget.
    require(not probability_lower >= F(1,96), "invalid extended kappa range")
    return {
        "status":"EXACT_FIRST_HIT_GEOMETRY_CONTROLS_PASS",
        "delta":str(delta), "kappa_upper":str(kmax),
        "box_vertex_pairs":len(corners)**2,
        "max_single_state_squared_norm":str(max_norm),
        "max_state_difference_squared_norm":str(max_difference),
        "h_lower_at_max_kappa":str(h_lower),
        "noise_energy_upper":str(n_upper),
        "signed_product_upper":str(n_upper*h_lower),
        "density_exponential_upper":str(exponential_upper),
        "box_probability_lower":str(probability_lower),
        "required_probability_at_max_kappa":str(kmax*kmax/96),
        "strict_contraction":False, "adverse_contact_constructed":False,
        "full_majorisation_proved":False,
        "analytic_proof_checked_by_code":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    result=audit()
    if not args.emit:
        expected=json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result==expected,"EXPECTED.json mismatch")
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
