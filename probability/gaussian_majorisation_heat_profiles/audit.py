#!/usr/bin/env python3
"""Exact finite audit for PROOF.md; no quadrature or PDE discretization."""

import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exp_negative(q):
    """Alternating-series enclosure valid on the entire stated domain."""
    require(Q(0) <= q <= Q(1, 2), "Taylor parameter outside proved range")
    upper = sum((-q)**j / factorial(j) for j in range(17))
    lower = upper - q**17 / factorial(17)
    return lower, upper


def norm2(vector):
    return sum(x*x for x in vector)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def ratio_cube(x, y):
    require(x > 0 and y > 0, "nonpositive precision")
    return (x+2*y)**3 / (27*x*y*y)


def audit():
    points = [tuple(Q(sign if j == axis else 0) for j in range(3))
              for axis in range(3) for sign in (-1, 1)]
    r, t = Q(99, 100), Q(1, 100)
    image = [(r*p[0], t*p[1], t*p[2]) for p in points]
    losses = []
    for i, j in combinations(range(6), 2):
        source = norm2(sub(points[i], points[j]))
        target = norm2(sub(image[i], image[j]))
        require(target > 0, "image atoms are not distinct")
        require(target <= r*r*source < source, "strict contraction failed")
        losses.append(source-target)
    covariance = [[sum(p[i]*p[j] for p in points)/6
                   for j in range(3)] for i in range(3)]
    require(covariance == [[Q(i == j, 3) for j in range(3)] for i in range(3)],
            "source posterior covariance at zero differs")

    al, au = exp_negative(r*r/2)
    bl, bu = exp_negative(t*t/2)
    # Positive-fraction monotonicity, keeping a repeated variable together.
    xlo, xhi = 1-r*r*au/(au+2*bl), 1-r*r*al/(al+2*bu)
    ylo, yhi = 1-t*t*bu/(al+2*bu), 1-t*t*bl/(au+2*bl)
    xl, xu = Q(77017949, 10**8), Q(77017950, 10**8)
    yl, yu = Q(99996172, 10**8), Q(99996173, 10**8)
    require(0 < xl < xlo <= xhi < xu < yl < ylo <= yhi < yu < 1,
            "published outward precision bounds failed")
    lower = (xl+2*yl)**3 / (27*xu*yu*yu)
    upper = (xu+2*yu)**3 / (27*xl*yl*yl)
    require(lower > Q(511, 500) > Q(1007, 1000)**3,
            "coefficient ratio gap not certified")
    require(Q(511, 500)-Q(1007, 1000)**3 == Q(852657, 10**9),
            "last rational margin differs")
    require(ratio_cube(Q(2, 3), Q(2, 3)) == 1, "source isotropy control")
    for scale in (Q(1), Q(1, 2)):
        precision = 1-scale*scale/3
        require(ratio_cube(precision, precision) == 1,
                "isometric/isotropic contraction control")

    # An independent exact limit control: project onto the first axis.
    # exp(1/2) <= 3/2 + (1/8)/(1-1/6) = 33/20 < 5/3,
    # so a=exp(-1/2)>3/5 and c=a/(2+a)>3/13.
    require(Q(3, 2)+Q(1, 8)/(1-Q(1, 6)) == Q(33, 20) < Q(5, 3),
            "geometric Taylor tail control")
    c = Q(3, 13)
    projection_cube = (3-c)**3/(27*(1-c))
    require(projection_cube == Q(864, 845) > Q(1007, 1000)**3,
            "projection-limit control")
    return {
        "status": "EXACT_HEAT_PROFILE_OBSTRUCTION_AUDIT_PASSED",
        "dimension": 3, "variance": "1", "atoms": 6, "weights": "1/6",
        "map_diagonal": [str(r), str(t), str(t)],
        "strict_pairs": len(losses), "minimum_squared_distance_loss": str(min(losses)),
        "distinct_target_atoms": len(set(image)), "lipschitz_squared": str(r*r),
        "source_peak_precision": ["2/3", "2/3", "2/3"],
        "target_peak_precision_bounds": {"x": [str(xl), str(xu)],
                                         "y": [str(yl), str(yu)]},
        "exponential_taylor_degree": 16,
        "ratio_cube_bounds": [str(lower), str(upper)],
        "ratio_cube_lower_simplification": "511/500",
        "limiting_coefficient_ratio_strict_lower_bound": "1007/1000",
        "last_cubed_margin": "852657/1000000000",
        "projection_limit_cubed_lower_bound": "864/845",
        "isotropic_control_ratio_cube": "1",
        "explicit_volume_cutoff_supplied": False,
        "pde_or_coarea_formalized": False,
        "full_conjecture_resolved": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.check:
        require(result == json.loads(args.check.read_text()), "expected record differs")
    print(json.dumps(result, indent=2, sort_keys=True))
