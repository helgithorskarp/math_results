#!/usr/bin/env python3
"""Exact non-radial support certificate at n=(10,1,3)/sqrt(110).

Python 3.11+, standard library only. See TORQUE_PROOF.md for the geometric
bridge and the quantified local exclusion. The finite checks use Q(phi).
"""
from fractions import Fraction
from itertools import combinations
import argparse
import json

from verify import PHI, QPhi, ZERO, dot, require, vertices


def cross(v, w):
    return tuple(v[i]*w[j]-v[j]*w[i] for i, j in [(1, 2), (2, 0), (0, 1)])


def subtract(v, w):
    return tuple(x-y for x, y in zip(v, w))


def determinant(v, w, u):
    return dot(v, cross(w, u))


def probes():
    a, b = PHI**3, PHI**2
    return [
        ((QPhi(1), QPhi(1), -a),
         (QPhi(Fraction(11, 2), Fraction(1, 5)),
          QPhi(Fraction(-7, 10), 1), QPhi(Fraction(-181, 10), -1))),
        ((QPhi(1), QPhi(1), -a),
         (QPhi(Fraction(3, 2), Fraction(9, 5)),
          QPhi(Fraction(-63, 10), 9), QPhi(Fraction(-29, 10), -9))),
        ((PHI, 2*PHI, -b),
         (QPhi(Fraction(-33, 10), Fraction(13, 5)),
          QPhi(Fraction(87, 10), Fraction(-7, 5)),
          QPhi(Fraction(81, 10), Fraction(-41, 5)))),
        ((QPhi(-1), a, QPhi(-1)),
         (QPhi(Fraction(-1, 5)), QPhi(Fraction(37, 5)),
          QPhi(Fraction(-9, 5)))),
    ]


def check_radial_failure(V, normal):
    """A precise limitation of the radial-maxima spanning criterion."""
    N, R2 = dot(normal, normal), 7+8*PHI
    selected = []
    for v in V:
        axial = dot(normal, v)
        if axial.sign() <= 0:
            continue
        gaps = [N*(R2-dot(v, w))-axial*dot(normal, subtract(v, w))
                for w in V if w != v]
        if min(gaps).sign() > 0:
            selected.append(v)
    require(len(selected) == 6, "expected six positive radial maxima")
    separator = tuple(map(QPhi, (-1, -5, 5)))
    require(dot(separator, normal) == ZERO, "separator is not tangent")
    margin = min(dot(separator, v) for v in selected)
    require(margin.sign() > 0, "radial maxima not strictly separated")
    require(margin == -5+4*PHI, "unexpected radial separation margin")
    # Exclude accidental coincident projections at this exact direction.
    for v, w in combinations(V, 2):
        d = subtract(v, w)
        require((N*dot(d, d)-dot(normal, d)**2).sign() > 0,
                "coincident projection at residual direction")
    return {"positive_strict_radial_maxima": len(selected),
            "tangent_separator_integer_vector": [-1, -5, 5],
            "minimum_separator_dot_a_plus_b_phi": margin.encode(),
            "all_projected_vertices_distinct": True,
            "radial_maxima_spanning_criterion_applies": False}


def check(probe_input=None):
    V = vertices()
    normal = tuple(map(QPhi, (10, 1, 3)))
    require(dot(normal, normal) == QPhi(110), "normal normalization")
    require(len(V) == 60 and all(dot(v, v) == 7+8*PHI for v in V),
            "standard sphere-inscribed vertex input")
    require(all(tuple(-x for x in v) in V for v in V), "central symmetry")
    require(7+8*PHI < 25, "R<5 bound failed")

    chosen_probes = probes() if probe_input is None else probe_input
    require(len(chosen_probes) == 4, "four support probes required")
    T, output_probes = [], []
    minimum_gap = None
    for v, m in chosen_probes:
        require(v in V, "support vertex absent")
        require(dot(m, normal) == ZERO, "probe does not lie in base plane")
        require(dot(m, m) < 625, "probe norm is not less than 25")
        gap = min(dot(m, subtract(v, w)) for w in V if w != v)
        require(gap > Fraction(27, 100), "strict unique-support gap too small")
        minimum_gap = gap if minimum_gap is None or gap < minimum_gap else minimum_gap
        torque = cross(v, m)
        T.append(torque)
        output_probes.append({"vertex": [x.encode() for x in v],
                              "probe": [x.encode() for x in m],
                              "torque": [x.encode() for x in torque],
                              "unique_support_gap": gap.encode()})

    weights = [(-1)**i*determinant(*[t for j, t in enumerate(T) if j != i])
               for i in range(4)]
    if weights[0].sign() < 0:
        weights = [-w for w in weights]
    require(all(w.sign() > 0 for w in weights), "origin not in tetrahedron interior")
    require(all(sum((w*t[k] for w, t in zip(weights, T)), ZERO) == ZERO
                for k in range(3)), "positive torque equilibrium failed")
    affine_det = determinant(*[subtract(T[i], T[0]) for i in [1, 2, 3]])
    require(affine_det.sign() != 0, "degenerate torque tetrahedron")
    for ids in combinations(range(4), 3):
        a, b, c = [T[i] for i in ids]
        facet_normal = cross(subtract(b, a), subtract(c, a))
        require((dot(facet_normal, a)**2-dot(facet_normal, facet_normal)).sign() > 0,
                "torque tetrahedron facet distance is not greater than one")

    delta, theta, M, g, ball_radius = (Fraction(1, 1000), Fraction(1, 100),
                                     Fraction(125), Fraction(27, 100), Fraction(1))
    require(2*M*delta < g, "perturbed support uniqueness bound failed")
    require(M*(delta+theta/2) < ball_radius, "rotation exclusion bound failed")
    return {
        "agent": "six-rupert-3", "role": "researcher",
        "claim_status": "analytic_local_exclusion_with_exact_support_certificate",
        "global_non_rupert_proved": False,
        "normal_integer_vector": [10, 1, 3], "normal_squared_length": 110,
        "target_normal_distance_maximum": str(delta),
        "relative_rotation_angle_maximum_radians": str(theta),
        "support_probes": output_probes,
        "support_gap_comparisons": 4*59,
        "minimum_support_gap_a_plus_b_phi": minimum_gap.encode(),
        "positive_torque_equilibrium_weights": [w.encode() for w in weights],
        "torque_tetrahedron_contains_closed_unit_ball_in_interior": True,
        "all_four_facet_distances_greater_than_one": True,
        "R_times_maximum_probe_norm_strict_upper_bound": str(M),
        "perturbed_support_gap_strict_lower_bound": str(g-2*M*delta),
        "rotation_error_strict_upper_bound": str(M*(delta+theta/2)),
        "radial_criterion_limitation": check_radial_failure(V, normal),
    }


def self_test():
    originals = probes()
    reversed_probe = list(originals)
    v, m = reversed_probe[0]
    reversed_probe[0] = (v, tuple(-x for x in m))
    for invalid in [reversed_probe, [originals[0]]*4, originals[:3]]:
        try:
            check(invalid)
        except ValueError:
            pass
        else:
            raise ValueError("invalid support certificate accepted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    print(json.dumps(check(), indent=2, sort_keys=True))
