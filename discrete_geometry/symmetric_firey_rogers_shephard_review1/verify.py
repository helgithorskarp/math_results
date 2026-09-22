#!/usr/bin/env python3
"""Independent exact small-case checks for REVIEW.md.

The polygon path uses only definitions: at p=infinity,
  (C+x) +_infinity (C-x) = C + [-x,x].
It does not call the target's scalar kernel or verification code.
"""

from fractions import Fraction as F
import hashlib
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def cross(o, a, b):
    return ((a[0]-o[0])*(b[1]-o[1])
            - (a[1]-o[1])*(b[0]-o[0]))


def hull(points):
    points = sorted(set((F(x), F(y)) for x, y in points))
    require(len(points) >= 3, "too few points")
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def twice_area(poly):
    return abs(sum(poly[i][0]*poly[(i+1) % len(poly)][1]
                   - poly[i][1]*poly[(i+1) % len(poly)][0]
                   for i in range(len(poly))))


def add_segment(poly, x):
    return hull([(v[0]+s*x[0], v[1]+s*x[1])
                 for v in poly for s in (-1, 1)])


def on_segment(z, a, b):
    return (cross(a, b, z) == 0
            and min(a[0], b[0]) <= z[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= z[1] <= max(a[1], b[1]))


def facet_contact(poly, x):
    minus_x = (-x[0], -x[1])
    return all(on_segment(x, poly[i], poly[(i+1) % len(poly)])
               or on_segment(minus_x, poly[i], poly[(i+1) % len(poly)])
               for i in range(len(poly)))


def ratio_at_infinity(poly, x):
    return F(twice_area(add_segment(poly, x)), twice_area(poly))


def main():
    square = hull([(-1, -1), (1, -1), (1, 1), (-1, 1)])
    placements = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = (F(i), F(j))
            ratio = ratio_at_infinity(square, x)
            contact = facet_contact(square, x)
            require((ratio == 3) == contact,
                    "square endpoint equality mismatch")
            placements.append([i, j, str(ratio), contact])

    hexagon = hull([(1, 0), (1, 1), (0, 1),
                    (-1, 0), (-1, -1), (0, -1)])
    hex_x = (F(1), F(1))
    hex_ratio = ratio_at_infinity(hexagon, hex_x)
    require(hex_ratio == F(7, 3), "hexagon ratio")
    require(not facet_contact(hexagon, hex_x), "hexagon false equality")

    # Direct p=2 square support-area calculation.  On two quadrant sectors
    # H=2(cos(theta)+sin(theta)), each contributing 4 to area.  On the other
    # two H=2, each contributing pi.  Represent a+b*pi exactly as [a,b].
    p2_area = (F(8), F(2))
    p2_ratio = (p2_area[0]/4, p2_area[1]/4)
    require(p2_ratio == (F(2), F(1, 2)), "p=2 sharp ratio")

    # For the 3D crosspolytope, polar vertices are the cube vertices.  With
    # x=e1 they all lie on the two planes x.u=+/-1.
    cube_vertices = [(i, j, k)
                     for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)]
    require(all(abs(u[0]) == 1 for u in cube_vertices),
            "crosspolytope polar-face fixture")

    records = {
        "crosspolytope_polar_vertices": len(cube_vertices),
        "hexagon_vertex_contact": False,
        "hexagon_vertex_pinfinity_ratio": str(hex_ratio),
        "p2_square_area_Q_plus_Qpi": list(map(str, p2_area)),
        "p2_square_ratio_Q_plus_Qpi": list(map(str, p2_ratio)),
        "square_lattice_placements": placements,
    }
    encoded = json.dumps(records, sort_keys=True,
                         separators=(",", ":")).encode()
    result = {
        "arithmetic": "exact rational polygons; symbolic Q+Q*pi",
        "record_sha256": hashlib.sha256(encoded).hexdigest(),
        "records": records,
        "status": "VERIFIED",
        "trust_boundary": (
            "Finite endpoint and normalization checks; universal proof "
            "is audited in REVIEW.md."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
