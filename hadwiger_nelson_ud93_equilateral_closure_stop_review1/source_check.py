#!/usr/bin/env python3
"""Networked numerical provenance check against the pinned Shibuya source.

This is corroboration only.  The exact theorem is proved by verify.py without
network access, mpmath, or an upstream floating-point predicate.
"""

from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from urllib.request import urlopen

from mpmath import mp

import verify as V


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_ud93_equilateral_closure_stop"
COMMIT = "218097c9971db2b60ab94a0b8dae20d76741cc43"
URL = ("https://raw.githubusercontent.com/Parcly-Taxel/Shibuya/" + COMMIT
       + "/shibuya/graphs/pegg.py")
SOURCE_SHA256 = "2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def circle_intersection_left(first, second, first_radius=1, second_radius=1):
    distance = abs(second - first)
    base_angle = mp.arg(second - first)
    offset = mp.acos((first_radius**2 - second_radius**2 + distance**2)
                     / (2 * distance * first_radius))
    return first + first_radius * mp.exp(mp.j * (base_angle + offset))


def main():
    source_bytes = urlopen(URL, timeout=30).read()
    require(sha256(source_bytes).hexdigest() == SOURCE_SHA256, "upstream source hash")
    source_text = source_bytes.decode()
    require("def ud93_vertices(t):" in source_text
            and "return all_unit_distances(vertices)" in source_text,
            "upstream UD9-3 source markers")

    certificate = loads((TARGET / "certificate.json").read_text())
    require(V.file_hash(TARGET / "certificate.json") == V.TARGET_HASHES["certificate.json"],
            "target certificate hash")
    mp.dps = 100
    denominator = mp.mpf(certificate["midpoint_denominator"])
    x, y, u, v = (mp.mpf(value) / denominator
                  for value in certificate["midpoint_numerators"])
    rho = mp.exp(mp.j * mp.pi / 3)
    z = x + y * rho
    w = u + v * rho
    alpha = (1 + rho) / 3
    p3 = -rho + (1 + rho) * w
    formal = (
        0, 1, z, w, z * (1 - rho), p3,
        (1 - alpha) * z + alpha * w,
        alpha * z + (1 - alpha) * w,
        (1 - rho) * w + rho * p3,
    )

    angle = mp.mpf(certificate["source_parameter_approximation"])
    a, b = 0, 1
    p0 = mp.exp(mp.j * angle)
    p1 = circle_intersection_left(p0, b, mp.sqrt(3), 1)
    p2 = circle_intersection_left(p0, a)
    p3 = circle_intersection_left(p2, p1)
    p4 = circle_intersection_left(p0, p1)
    p5 = circle_intersection_left(p1, p0)
    p6 = circle_intersection_left(p1, p3)
    upstream = (a, b, p0, p1, p2, p3, p4, p5, p6)

    maximum_error = max(abs(left - right) for left, right in zip(formal, upstream))
    closure_residual = abs(abs(b - p3) - mp.sqrt(3))
    edges = tuple((left, right) for left in range(9) for right in range(left + 1, 9)
                  if abs(abs(upstream[left] - upstream[right]) - 1) < mp.mpf("1e-50"))
    require(maximum_error < mp.mpf("1e-80"), "ordered source correspondence")
    require(closure_residual < mp.mpf("1e-90"), "upstream closure residual")
    require(edges == V.SOURCE_EDGES, "upstream complete unit edge list")

    print(dumps({
        "all_source_checks_passed": True,
        "maximum_ordered_coordinate_error_lt_1e80_inverse": True,
        "source_file_sha256": SOURCE_SHA256,
        "source_unit_edges": len(edges),
        "upstream_closure_residual_lt_1e90_inverse": True,
        "upstream_commit": COMMIT,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
