#!/usr/bin/env python3
"""Numerically build the rational certificate for one flexible-fish self-contact.

This discovery/regeneration script uses mpmath.  The output is verified using
only exact integer and rational arithmetic by verify.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp


TARGET = (10, 21)
FIXED = {0: (0, 0), 1: (1, 0)}
H = 10**50
D = 10**30
RADIUS_DENOMINATOR = 10**25
SOURCE_EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 9), (0, 21),
    (1, 4), (1, 5), (1, 10), (1, 16),
    (2, 5), (2, 8), (2, 12), (2, 13), (2, 17),
    (3, 6), (3, 11),
    (4, 6), (4, 12),
    (5, 7), (5, 11), (5, 18), (5, 22),
    (6, 7), (6, 8), (6, 14), (6, 15), (6, 19), (6, 20),
    (7, 9), (8, 10), (9, 11), (10, 12),
    (13, 14), (13, 15), (14, 17), (15, 16), (16, 17),
    (18, 19), (18, 20), (19, 22), (20, 21), (21, 22),
]
BLOCKED_WORD = "01110021022330110210021"
SURVIVING_WORD = "01110021022330110210012"


def circle_intersection_left(z1, z2, r1=1, r2=1):
    """Circle intersection on the left of the directed line z1 -> z2."""
    delta = z2-z1
    distance = abs(delta)
    cosine = (r1*r1-r2*r2+distance*distance)/(2*distance*r1)
    turn = mp.sqrt(1-cosine*cosine)
    return z1+r1*(delta/distance)*(cosine+1j*turn)


def fish(t):
    """Hochberg--O'Donnell fish in Shibuya's one-parameter coordinates."""
    cu = circle_intersection_left
    a, b = mp.mpc(0), mp.mpc(1)
    p0 = 1j*mp.exp(1j*t)

    def first(u, v):
        p1 = mp.exp(-1j*u)
        p2 = 1-mp.exp(1j*v)
        p3 = p0+1
        p4 = cu(p2, p1)
        p5 = cu(p4, p3)
        p6 = cu(p0, p4)
        p7 = cu(a, p5)
        p8 = cu(p6, b)
        p9 = cu(p7, p1)
        p10 = cu(p2, p8)
        return abs(p0-p10)**2-1, abs(p3-p9)**2-1

    u0 = mp.mpf("0.424082")-mp.mpf("0.311038")*t
    v0 = mp.mpf("0.424082")+mp.mpf("0.311038")*t
    u, v = mp.findroot(first, (u0, v0), tol=mp.mpf("1e-150"))
    p1 = mp.exp(-1j*u)
    p2 = 1-mp.exp(1j*v)
    p3 = p0+1
    p4 = cu(p2, p1)
    p5 = cu(p4, p3)
    p6 = cu(p0, p4)
    p7 = cu(a, p5)
    p8 = cu(p6, b)
    p9 = cu(p7, p1)
    p10 = cu(p2, p8)

    def qchain(w):
        q0 = p0+mp.exp(1j*w)
        q1 = cu(p4, q0)
        q2 = cu(q0, p4)
        q3 = cu(b, q2)
        q4 = cu(q3, q1)
        return q0, q1, q2, q3, q4

    w0 = mp.polyval([mp.mpf("-0.465329"), mp.mpf("0.516923"),
                     mp.mpf("0.320761"), mp.mpf("1.27248")], t)
    w = mp.findroot(lambda z: abs(p0-qchain(z)[4])**2-1, w0,
                    tol=mp.mpf("1e-150"))

    def rchain(x):
        r0 = p3-mp.exp(-1j*x)
        r1 = cu(r0, p4)
        r2 = cu(p4, r0)
        r3 = cu(r2, a)
        r4 = cu(r1, r3)
        return r0, r1, r2, r3, r4

    x0 = mp.polyval([mp.mpf("0.465329"), mp.mpf("0.516923"),
                     mp.mpf("-0.320761"), mp.mpf("1.27248")], t)
    x = mp.findroot(lambda z: abs(p3-rchain(z)[4])**2-1, x0,
                    tol=mp.mpf("1e-150"))
    points = (a, b, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
    return points+qchain(w)+rchain(x), (u, v, w, x)


def nearest_integer(value):
    if value >= 0:
        return int(mp.floor(value+mp.mpf("0.5")))
    return -int(mp.floor(-value+mp.mpf("0.5")))


def build(output):
    if output.exists():
        raise FileExistsError(output)
    mp.mp.dps = 180

    def contact(t):
        points, _ = fish(t)
        return abs(points[TARGET[0]]-points[TARGET[1]])**2-1

    t = mp.findroot(contact, (mp.mpf("-0.16"), mp.mpf("-0.15")),
                    tol=mp.mpf("1e-150"), verify=True)
    points, parameters = fish(t)
    full_edges = sorted(set(SOURCE_EDGES) | {TARGET})
    equations = [edge for edge in full_edges if edge != (0, 1)]
    free = [vertex for vertex in range(23) if vertex not in FIXED]
    where = {vertex: i for i, vertex in enumerate(free)}
    if len(equations) != 42 or len(free) != 21:
        raise RuntimeError("wrong square system dimensions")

    jacobian = mp.matrix(42, 42)
    for row, (a, b) in enumerate(equations):
        delta = points[a]-points[b]
        dx, dy = mp.re(delta), mp.im(delta)
        if a in where:
            jacobian[row, 2*where[a]] = 2*dx
            jacobian[row, 2*where[a]+1] = 2*dy
        if b in where:
            jacobian[row, 2*where[b]] = -2*dx
            jacobian[row, 2*where[b]+1] = -2*dy
    inverse = jacobian**-1
    certificate = {
        "schema": "fish-self-contact-root-v1",
        "target_contact": list(TARGET),
        "source_edges": [list(edge) for edge in SOURCE_EDGES],
        "source_blocked_word": BLOCKED_WORD,
        "surviving_complete_word": SURVIVING_WORD,
        "fixed_vertices": {str(i): list(point) for i, point in FIXED.items()},
        "midpoint_denominator": H,
        "midpoint_numerators": [
            [nearest_integer(mp.re(point)*H), nearest_integer(mp.im(point)*H)]
            for point in points
        ],
        "inverse_denominator": D,
        "inverse_numerators": [
            [nearest_integer(inverse[i, j]*D) for j in range(42)]
            for i in range(42)
        ],
        "radius_denominator": RADIUS_DENOMINATOR,
        "discovery_approximations": {
            "t": mp.nstr(t, 90),
            "u_v_w_x": [mp.nstr(value, 90) for value in parameters],
        },
    }
    output.write_text(json.dumps(certificate, separators=(",", ":"))+"\n")
    return {"output": str(output), "bytes": output.stat().st_size,
            "t": certificate["discovery_approximations"]["t"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path,
                        help="new output path (refuses to overwrite)")
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2, sort_keys=True))
