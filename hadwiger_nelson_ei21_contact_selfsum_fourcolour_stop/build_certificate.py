#!/usr/bin/env python3
"""Untrusted numerical producer for the EI21 contact certificate.

The EI21 parametrisation and left-circle-intersection convention are adapted
from Shibuya at commit 218097c9971db2b60ab94a0b8dae20d76741cc43.
The generated file is proved using exact arithmetic by ``verify.py``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp


TARGET = (0, 14)
FIXED = {0: (0, 0), 1: (0, -1)}
SOURCE_EDGES = (
    (0, 1), (0, 3), (0, 4),
    (1, 5), (1, 6), (1, 9), (1, 15),
    (2, 3), (2, 4), (2, 5), (2, 6),
    (3, 7), (3, 20), (4, 8), (4, 14),
    (5, 8), (5, 16), (5, 19),
    (6, 7), (6, 10), (6, 13),
    (7, 8), (7, 9), (8, 15),
    (9, 11), (9, 12), (10, 11), (10, 12),
    (11, 13), (12, 14), (13, 14),
    (15, 17), (15, 18), (16, 17), (16, 18),
    (17, 19), (18, 20), (19, 20),
)
BLOCKED_WORD = "010112203201130001102"
SURVIVING_WORD = "010112203201102001102"
H = 10**50
D = 10**30
RADIUS_DENOMINATOR = 10**25


def cu(z1, z2, r1=1, r2=1):
    """Point left of z1 -> z2 at the prescribed two radii."""
    delta = z2 - z1
    distance = abs(delta)
    cosine = (r1*r1-r2*r2+distance*distance)/(2*distance*r1)
    return z1+r1*(delta/distance)*(cosine+1j*mp.sqrt(1-cosine*cosine))


def ei21_vertices(t, u, v, w):
    a, b = mp.mpc(0), -1j
    p0 = mp.mpc(t, u)
    p1 = cu(a, p0); p2 = cu(p0, a)
    p3 = cu(b, p0); p4 = cu(p0, b)
    p5 = cu(p4, p1); p6 = cu(p2, p3)
    q1 = cu(b, p5); q2 = p4+mp.exp(1j*v)
    q3 = cu(q1, q2); q4 = cu(q2, q1)
    q5 = cu(p4, q3); q6 = cu(q4, q5)
    r1 = cu(p6, b); r2 = p3+mp.exp(1j*w)
    r3 = cu(r2, r1); r4 = cu(r1, r2)
    r5 = cu(r3, p3); r6 = cu(r5, r4)
    points = (a, b, p0, p1, p2, p3, p4, p5, p6,
              q1, q2, q3, q4, q5, q6, r1, r2, r3, r4, r5, r6)
    return points, abs(p5-p6)-1, abs(p2-q6)-1, abs(p1-r6)-1


def nearest_integer(value):
    if value >= 0:
        return int(mp.floor(value+mp.mpf("0.5")))
    return -int(mp.floor(-value+mp.mpf("0.5")))


def build(output):
    if output.exists():
        raise FileExistsError(output)
    mp.mp.dps = 180

    def system(t, u, v, w):
        points, *residuals = ei21_vertices(t, u, v, w)
        return (*residuals, abs(points[0]-points[14])**2-1)

    parameters = mp.findroot(
        system,
        (mp.mpf("0.0885"), mp.mpf("0.8199"), mp.mpf("2.6160"), mp.mpf("0.3342")),
        tol=mp.mpf("1e-150"), verify=True, maxsteps=100)
    points, *residuals = ei21_vertices(*parameters)
    if max(abs(x) for x in residuals) > mp.mpf("1e-140"):
        raise RuntimeError("source closure residual")

    full_edges = sorted(set(SOURCE_EDGES) | {TARGET})
    equations = [edge for edge in full_edges if edge != (0, 1)]
    free = [v for v in range(21) if v not in FIXED]
    where = {v: i for i, v in enumerate(free)}
    if len(equations) != 38 or len(free) != 19:
        raise RuntimeError("wrong square system dimensions")
    jacobian = mp.matrix(38, 38)
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
        "schema": "ei21-contact-root-v1",
        "provenance": {
            "repository": "https://github.com/Parcly-Taxel/Shibuya",
            "commit": "218097c9971db2b60ab94a0b8dae20d76741cc43",
            "source_path": "shibuya/graphs/pegg.py",
        },
        "target_contact": list(TARGET),
        "source_edges": [list(edge) for edge in SOURCE_EDGES],
        "source_blocked_word": BLOCKED_WORD,
        "surviving_complete_word": SURVIVING_WORD,
        "fixed_vertices": {str(i): list(p) for i, p in FIXED.items()},
        "midpoint_denominator": H,
        "midpoint_numerators": [[nearest_integer(mp.re(p)*H), nearest_integer(mp.im(p)*H)]
                                  for p in points],
        "inverse_denominator": D,
        "inverse_numerators": [[nearest_integer(inverse[i, j]*D) for j in range(38)]
                               for i in range(38)],
        "radius_denominator": RADIUS_DENOMINATOR,
        "discovery_approximations": {
            "t_u_v_w": [mp.nstr(x, 90) for x in parameters],
        },
    }
    output.write_text(json.dumps(certificate, separators=(",", ":"))+"\n")
    return {"output": str(output), "bytes": output.stat().st_size}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2, sort_keys=True))
