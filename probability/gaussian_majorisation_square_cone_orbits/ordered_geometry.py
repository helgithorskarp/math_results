#!/usr/bin/env python3
"""Exact rational strictness and exposed-sphere fixture for ORDERED_WEIGHTS.md.

This checks the fixture, not the universal orbit comparison: that premise
comes from the finite correlation certificate and the analytic proof.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path
import argparse
import hashlib
import json

A = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))
X = ((0,0,0),) + A + tuple(tuple(-v for v in b) for b in B)
Y = ((0,0,0),) + A + B
R = tuple(Q(n,40) for n in (32,52,51,50,49,44,43,42,41))


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def squared_distance(x,y):
    return sum((a-b)**2 for a,b in zip(x,y))


def orbit(x):
    return [tuple(signs[i]*x[perm[i]] for i in range(3))
            for perm in permutations(range(3)) for signs in product((-1,1), repeat=3)]


def audit():
    need(len(set(R)) == 9 and R[1] > R[2] > R[3] > R[4]
         and R[5] > R[6] > R[7] > R[8] > 0, "Wrong radii ordering")
    losses = [squared_distance(X[i],X[j])-squared_distance(Y[i],Y[j])
              for i in range(9) for j in range(i)]
    need(min(losses) == 0 and max(losses) == 8 and losses.count(8) == 8,
         "Contraction fixture failed")
    for centers in (X,Y):
        need(all(squared_distance(centers[0],centers[i]) < (R[0]+R[i])**2
                 for i in range(1,9)), "Origin ball is not linked to every other ball")
    # A*=cone(B), B*=cone(A). This is the dual witness used with the
    # existing finite-strong-composition theorem, not a new motion theorem.
    dual_values = [-u[0]*v[0]-u[1]*v[1]+u[2]*v[2] for u in B for v in A]
    need(sorted(set(dual_values)) == [0,2], "Dual matrix witness failed")
    probe = (1,0,1)
    points = orbit(probe)
    counts = {}
    boundary_margin = None
    for name,centers in (("source",X),("target",Y)):
        counts[name] = 0
        for point in points:
            differences = [squared_distance(point,c)-r*r for c,r in zip(centers,R)]
            counts[name] += int(min(differences) <= 0)
            margin = min(map(abs,differences))
            boundary_margin = margin if boundary_margin is None else min(boundary_margin,margin)
    need(counts == {"source":48,"target":32}, "Wrong exact orbit coverage")
    need(boundary_margin == Q(81,1600), "Wrong boundary margin")
    epsilon = Q(1,1000)
    distance_change_bound = 8*epsilon + epsilon*epsilon
    need(distance_change_bound < boundary_margin, "Strictness neighborhood is not certified")

    # All normals are rational unit vectors; every ball has an exposed sphere patch.
    normals_a = ((1,0,0),(0,1,0),(-1,0,0),(0,-1,0))
    normals_b = tuple((Q(3*b[0],5),Q(4*b[1],5),0) for b in B)
    normals_y = ((0,0,-1),) + normals_a + normals_b
    normals_x = ((0,0,-1),) + normals_a + tuple(tuple(-v for v in n) for n in normals_b)
    exposure = {}
    for name,centers,normals in (("source",X,normals_x),("target",Y,normals_y)):
        witnesses = []
        clearances = []
        for i,(center,radius,normal) in enumerate(zip(centers,R,normals)):
            need(sum(v*v for v in normal) == 1, "A normal is not a unit vector")
            witness = tuple(c+radius*n for c,n in zip(center,normal))
            need(squared_distance(witness,center) == radius*radius, "Not on its own sphere")
            gap = min(squared_distance(witness,other)-R[j]*R[j]
                      for j,other in enumerate(centers) if j != i)
            need(gap > 0, "A claimed sphere patch is covered by another ball")
            witnesses.append([str(v) for v in witness])
            clearances.append(str(gap))
        exposure[name] = {"witnesses":witnesses, "squared_clearances":clearances}
    return {
        "status":"ORDERED_RADII_GEOMETRY_FIXTURE_PASS",
        "radii":[str(r) for r in R], "probe":list(probe),
        "group_label_counts":counts, "orbit_gap":counts["source"]-counts["target"],
        "squared_boundary_margin":str(boundary_margin),
        "strictness_ball_radius":str(epsilon),
        "squared_distance_change_bound":str(distance_change_bound),
        "volume_gap_lower_bound":"4*pi/9000000000",
        "strong_composition_dual_diagonal":[-1,-1,1],
        "strong_composition_dual_trace":-1,
        "strong_composition_generator_values":sorted(set(dual_values)),
        "all_spheres_exposed":exposure,
        "origin_ball_overlaps_all_eight_others_at_both_endpoints":True,
        "trust_boundary":"Exact rational fixture only. Global nonnegative orbit gaps and the volume transfer use ORDERED_WEIGHTS.md and its finite correlation certificate.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = encoded(audit())
    if args.check:
        need(result == Path(__file__).with_name("ORDERED_GEOMETRY_EXPECTED.json").read_bytes(),
             "Geometry fixture record differs")
        print("ORDERED_RADII_GEOMETRY_FIXTURE_PASS",hashlib.sha256(result).hexdigest())
    else:
        print(result.decode(),end="")


if __name__ == "__main__":
    main()
