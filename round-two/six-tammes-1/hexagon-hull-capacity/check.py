#!/usr/bin/env python3
"""Exact active-plane enumeration for the nine robust hull-capacity certificates.

The geometric theorem and its hypotheses are in PROOF.md. This program checks
the finite rational norm-exclusion obligations, without numerical decisions.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def scale(t, a):
    return tuple(t*x for x in a)


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def determinant(a, b, c):
    return dot(a, cross(b, c))


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def vertex_digest(vertices):
    return digest([[str(t) for t in x] for x in sorted(vertices)])


def read_vectors(data):
    tokens = data.decode("ascii").split()
    need(len(tokens) == 45, "expected 15 triples of exact decimal tokens")
    v = [tuple(Q(t) for t in tokens[3*i:3*i+3]) for i in range(15)]
    need(all(dot(x, x) > 0 for x in v), "zero template vector")
    return v


def build_rows(cert, vectors, pattern):
    boundary, center = pattern["boundary"], pattern["center"]
    need(len(boundary) == 6 and len(set(boundary)) == 6,
         "boundary must have six distinct labels")
    need(all(type(i) is int and 0 <= i < 15 for i in boundary),
         "invalid boundary label")
    need(type(center) is int and 0 <= center < 15 and center not in boundary,
         "invalid center label")
    eps, c = Q(cert["epsilon"]), Q(cert["packing_cosine_max"])
    need(eps > 0 and c > 0, "nonpositive parameter")
    total = tuple(sum(vectors[i][a] for i in boundary) for a in range(3))
    l1 = sum(abs(t) for t in total)
    need(l1 > 0, "zero hemisphere witness")
    h = scale(1/l1, total)
    b = min(dot(h, vectors[i]) for i in boundary)
    need(b > eps, "hemisphere perturbation margin fails")
    gamma = eps/(b-eps)
    rows = [(vectors[i], c+eps) for i in boundary]
    oriented_supports = []
    need(len(pattern["support_pairs"]) >= 3, "missing cone supports")
    for a, b0 in pattern["support_pairs"]:
        need(a in boundary and b0 in boundary and a != b0,
             "invalid support pair")
        n = cross(vectors[a], vectors[b0])
        values = [dot(n, vectors[i]) for i in boundary]
        if all(t >= 0 for t in values) and any(t > 0 for t in values):
            oriented = (a, b0)
        elif all(t <= 0 for t in values) and any(t < 0 for t in values):
            n = scale(-1, n)
            oriented = (b0, a)
        else:
            raise ValueError("pair does not support the template ray hull")
        n = scale(1/sum(abs(t) for t in n), n)
        need(sum(abs(t) for t in n) == 1, "support normalization failed")
        need(all(dot(n, vectors[i]) >= 0 for i in boundary),
             "invalid cone support")
        rows.append((scale(-1, n), gamma))
        oriented_supports.append(list(oriented))
    # Unit vectors are in this cube. Its inclusion also proves boundedness.
    for a in range(3):
        axis = tuple(Q(int(j == a)) for j in range(3))
        rows.extend([(axis, Q(1)), (scale(-1, axis), Q(1))])
    rows.append((vectors[center], Q(cert["projection_cut"])))
    need(all(rhs > 0 for _, rhs in rows), "origin is not strictly interior")
    return rows, b, gamma, oriented_supports


def enumerate_vertices(rows, bound):
    vertices, transcript = set(), []
    counts = {"singular": 0, "infeasible": 0, "feasible": 0}
    max_norm = Q(0)
    for indices in combinations(range(len(rows)), 3):
        (a, aa), (b, bb), (c, cc) = [rows[i] for i in indices]
        d = determinant(a, b, c)
        if d == 0:
            counts["singular"] += 1
            transcript.append([*indices, "singular"])
            continue
        numerator = plus(plus(scale(aa, cross(b, c)),
                              scale(bb, cross(c, a))), scale(cc, cross(a, b)))
        x = scale(1/d, numerator)
        violated = next((i for i, (n, rhs) in enumerate(rows)
                         if dot(n, x) > rhs), None)
        if violated is not None:
            counts["infeasible"] += 1
            transcript.append([*indices, "infeasible", violated])
            continue
        counts["feasible"] += 1
        transcript.append([*indices, "feasible"])
        vertices.add(x)
        norm = dot(x, x)
        need(norm < bound, "a feasible vertex violates the strict norm bound")
        max_norm = max(max_norm, norm)
    need(vertices, "no vertices in a full-dimensional bounded polytope")
    need(sum(counts.values()) == len(rows)*(len(rows)-1)*(len(rows)-2)//6,
         "incomplete active-plane enumeration")
    # An exact rational ceiling; no decimal approximation enters the proof.
    scaled = max_norm*1000000
    ceiling = (scaled.numerator+scaled.denominator-1)//scaled.denominator
    return {"triple_status_counts": counts, "vertices": len(vertices),
            "vertex_set_sha256": vertex_digest(vertices),
            "triple_status_sha256": digest(transcript),
            "max_norm_squared_rational_upper": str(Q(ceiling, 1000000))}


def verify(cert, coordinate_data):
    need(sha256(coordinate_data).hexdigest() == cert["coordinates_sha256"],
         "coordinate input hash mismatch")
    vectors = read_vectors(coordinate_data)
    norms = [dot(x, x) for x in vectors]
    need(all(Q(cert["template_vector_norm_lower"])**2 <= n <=
             Q(cert["template_vector_norm_bound"])**2 for n in norms),
         "template vector norm bound fails")
    seed_c = Q(cert["reference_normalized_packing_cosine"])
    need(0 < seed_c < 1, "invalid reference packing cosine")
    for i, j in combinations(range(15), 2):
        d = dot(vectors[i], vectors[j])
        need(d <= 0 or d*d <= seed_c*seed_c*norms[i]*norms[j],
             "reference normalized packing inequality fails")
    bound = Q(cert["vertex_norm_squared_bound"])
    center_norm = Q(cert["template_center_norm_bound"])
    cap = Q(cert["unit_cap_cosine_lower"])
    cut, c = Q(cert["projection_cut"]), Q(cert["packing_cosine_max"])
    need(0 < bound < 1, "norm-exclusion bound must be below one")
    need(0 < cap < 1 and cut/center_norm > cap,
         "projection-to-unit-cap scalar bridge fails")
    need(2*cap*cap-1 > c, "two-point separation bridge fails")
    patterns = []
    need(len(cert["patterns"]) == 9, "expected nine explicit patterns")
    for pattern in cert["patterns"]:
        p = vectors[pattern["center"]]
        need(dot(p, p) <= center_norm*center_norm,
             "template center norm bound fails")
        cyc = pattern["boundary"]
        need(all(dot(vectors[a], vectors[b]) >=
                 Q(cert["template_cycle_edge_dot_lower"])
                 for a, b in zip(cyc, cyc[1:]+cyc[:1])),
             "template cycle edge lower bound fails")
        rows, b, gamma, supports = build_rows(cert, vectors, pattern)
        finite = enumerate_vertices(rows, bound)
        patterns.append({"boundary": pattern["boundary"],
                         "center": pattern["center"],
                         "oriented_support_pairs": supports,
                         "rows": len(rows),
                         "hemisphere_minimum": str(b),
                         "cone_slack": str(gamma), **finite})
    return {"status": "all_nine_strict_norm_exclusions_verified",
            "arithmetic": "fractions.Fraction; no floating-point decisions",
            "coordinates_sha256": cert["coordinates_sha256"],
            "reference_normalized_pair_inequalities_checked": 105,
            "reference_normalized_packing_cosine": str(seed_c),
            "epsilon": cert["epsilon"],
            "packing_cosine_max": cert["packing_cosine_max"],
            "vertex_norm_squared_bound": cert["vertex_norm_squared_bound"],
            "unit_cap_cosine_lower": cert["unit_cap_cosine_lower"],
            "pair_dot_strict_lower": str(2*cap*cap-1),
            "pair_dot_margin_over_code_bound": str(2*cap*cap-1-c),
            "total_distinct_vertices": sum(p["vertices"] for p in patterns),
            "patterns": patterns}


def main():
    cert = json.loads((ROOT/"certificate.json").read_text())
    output = verify(cert, (ROOT/"coordinates.txt").read_bytes())
    expected_path = ROOT/"EXPECTED.json"
    if expected_path.exists():
        need(output == json.loads(expected_path.read_text()),
             "entry-level expected output mismatch")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
