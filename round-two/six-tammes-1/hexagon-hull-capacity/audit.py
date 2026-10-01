#!/usr/bin/env python3
"""Separate clipping enumeration of the certificate's complete vertex sets.

No imports from check.py. Start from the cube and add each halfspace, deriving
new vertices by segment-plane intersections. All arithmetic is rational.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product, permutations
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inner(a, b):
    answer = F(0)
    for j in range(3):
        answer += a[j]*b[j]
    return answer


def det(matrix):
    # Leibniz expansion, independent of the primary Cramer implementation.
    answer = F(0)
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3)
                         for j in range(i+1, 3))
        term = F((-1)**inversions)
        for i in range(3):
            term *= matrix[i][perm[i]]
        answer += term
    return answer


def is_vertex(x, rows):
    active = [normal for normal, rhs in rows if inner(normal, x) == rhs]
    return any(det(triple) != 0 for triple in combinations(active, 3))


def clipping_vertices(additional_rows):
    axes = [tuple(F(int(i == j)) for i in range(3)) for j in range(3)]
    processed = []
    for axis in axes:
        processed.extend([(axis, F(1)), (tuple(-t for t in axis), F(1))])
    vertices = set(product((F(-1), F(1)), repeat=3))
    progression = [len(vertices)]
    for normal, rhs in additional_rows:
        require(rhs > 0, "clipping must preserve a strict interior origin")
        values = {x: inner(normal, x)-rhs for x in vertices}
        inside = sorted(x for x in vertices if values[x] <= 0)
        outside = sorted(x for x in vertices if values[x] > 0)
        candidates = set(inside)
        # Trying every inside-outside pair includes every crossing old edge.
        # Extra segment intersections are removed by the active-normal rank.
        for a in inside:
            if values[a] == 0:
                continue
            for b in outside:
                t = -values[a]/(values[b]-values[a])
                require(0 < t < 1, "invalid clipping intersection")
                candidates.add(tuple((1-t)*a[j]+t*b[j] for j in range(3)))
        processed.append((normal, rhs))
        for x in candidates:
            require(all(inner(n, x) <= z for n, z in processed),
                    "clipping produced an infeasible candidate")
        vertices = {x for x in candidates if is_vertex(x, processed)}
        require(vertices, "empty clipped bounded body")
        progression.append(len(vertices))
    return vertices, progression


def parse_rows(cert, coords, pattern):
    ids = pattern["boundary"]
    eps = F(cert["epsilon"])
    c = F(cert["packing_cosine_max"])
    h = [sum(coords[i][j] for i in ids) for j in range(3)]
    denominator = sum(abs(z) for z in h)
    require(denominator > 0, "zero hemisphere sum")
    h = tuple(z/denominator for z in h)
    b = min(inner(h, coords[i]) for i in ids)
    require(b > eps, "hemisphere margin fails")
    slack = eps/(b-eps)
    rows = [(coords[i], c+eps) for i in ids]
    unit_axes = [tuple(F(int(i == j)) for i in range(3)) for j in range(3)]
    for a, b0 in pattern["support_pairs"]:
        n = [det([coords[a], coords[b0], e]) for e in unit_axes]
        values = [inner(n, coords[i]) for i in ids]
        if all(t <= 0 for t in values) and any(t < 0 for t in values):
            n = [-t for t in n]
        else:
            require(all(t >= 0 for t in values) and any(t > 0 for t in values),
                    "invalid supporting plane")
        denominator = sum(abs(z) for z in n)
        require(denominator > 0, "zero supporting normal")
        n = tuple(z/denominator for z in n)
        require(sum(abs(z) for z in n) == 1 and
                all(inner(n, coords[i]) >= 0 for i in ids),
                "support validity fails")
        rows.append((tuple(-z for z in n), slack))
    rows.append((coords[pattern["center"]], F(cert["projection_cut"])))
    return rows


def vertex_hash(vertices):
    data = [[str(t) for t in x] for x in sorted(vertices)]
    return sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()


def small_controls():
    # A clipped cube has exactly 8 vertices after x <= 1/2.
    v, _ = clipping_vertices([((F(1), F(0), F(0)), F(1, 2))])
    expected = set(product((F(-1), F(1, 2)), (F(-1), F(1)),
                           (F(-1), F(1))))
    require(v == expected, "small cube slice regression failed")
    # Cutting off one cube corner adds the three edge-plane intersections.
    v, _ = clipping_vertices([((F(1), F(1), F(1)), F(2))])
    expected = set(product((F(-1), F(1)), repeat=3))
    expected.remove((F(1), F(1), F(1)))
    expected.update([(F(0), F(1), F(1)), (F(1), F(0), F(1)),
                     (F(1), F(1), F(0))])
    require(v == expected, "small cube-corner regression failed")


def main():
    small_controls()
    cert = json.loads((BASE/"certificate.json").read_text())
    data = (BASE/"coordinates.txt").read_bytes()
    require(sha256(data).hexdigest() == cert["coordinates_sha256"],
            "coordinate hash differs")
    tokens = data.decode("ascii").split()
    require(len(tokens) == 45, "invalid coordinate count")
    coords = [tuple(F(tokens[3*i+j]) for j in range(3)) for i in range(15)]
    norms = [inner(x, x) for x in coords]
    require(all(F(cert["template_vector_norm_lower"])**2 <= n <=
                F(cert["template_vector_norm_bound"])**2
                for n in norms), "template vector norm bound fails")
    seed_c = F(cert["reference_normalized_packing_cosine"])
    require(0 < seed_c < 1, "invalid reference packing cosine")
    for i, j in combinations(range(15), 2):
        d = inner(coords[i], coords[j])
        require(d <= 0 or d*d <= seed_c*seed_c*norms[i]*norms[j],
                "reference pair inequality fails")
    primary = json.loads((BASE/"EXPECTED.json").read_text())
    require(len(primary["patterns"]) == len(cert["patterns"]) == 9,
            "invalid pattern count")
    records = []
    for pattern, expected in zip(cert["patterns"], primary["patterns"]):
        cyc = pattern["boundary"]
        require(all(inner(coords[a], coords[b]) >=
                    F(cert["template_cycle_edge_dot_lower"])
                    for a, b in zip(cyc, cyc[1:]+cyc[:1])),
                "cycle edge lower bound fails")
        center = coords[pattern["center"]]
        require(inner(center, center) <= F(cert["template_center_norm_bound"])**2,
                "center norm bound fails")
        vertices, progression = clipping_vertices(parse_rows(cert, coords, pattern))
        maximum = max(inner(x, x) for x in vertices)
        require(maximum < F(cert["vertex_norm_squared_bound"]),
                "clipping vertex norm exclusion fails")
        hashed = vertex_hash(vertices)
        require(expected["boundary"] == pattern["boundary"] and
                expected["center"] == pattern["center"] and
                expected["vertices"] == len(vertices) and
                expected["vertex_set_sha256"] == hashed,
                "full vertex-set mismatch between the two algorithms")
        records.append({"boundary": pattern["boundary"],
                        "center": pattern["center"],
                        "vertices": len(vertices),
                        "vertex_set_sha256": hashed,
                        "clipping_vertex_count_progression": progression})
    output = {"status": "separate_clipping_matches_all_nine_full_vertex_sets",
              "arithmetic": "fractions.Fraction; no primary-code imports",
              "small_clipping_controls": 2,
              "total_distinct_vertices": sum(r["vertices"] for r in records),
              "patterns": records}
    path = BASE/"AUDIT_EXPECTED.json"
    if path.exists():
        require(output == json.loads(path.read_text()), "audit output mismatch")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
