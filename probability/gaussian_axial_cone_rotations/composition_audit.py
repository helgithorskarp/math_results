#!/usr/bin/env python3
"""Exact finite audits for COMPOSITIONS.md, using only the standard library.

Default: deterministic JSON; --check compares EXPECTED_COMPOSITIONS.json.
This verifies a dual-cone certificate, not an enumeration of possible chains.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from verify import cross, dist2, dot, neg, norm2, require, sub


BASE = Path(__file__).resolve().parent
ORIGINAL = "50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4"


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    return tuple(tuple(dot(row, col) for col in transpose(b)) for row in a)


def matvec(a, v):
    return tuple(dot(row, v) for row in a)


def diagonal(v):
    return tuple(tuple(v[i] if i == j else F(0) for j in range(3)) for i in range(3))


def matrix_add(a, b):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(a, c):
    return tuple(tuple(c * x for x in row) for row in a)


def outer(u, v):
    return tuple(tuple(x * y for y in v) for x in u)


def dual_vertices(directions, slope):
    """Enumerate all intersections of two active constraints, not adjacent pairs.

    The cardinal inequalities bound the polygon. Every vertex of this
    full-dimensional bounded polygon has two independent active constraints.
    """
    normals = [tuple(slope * x for x in d) for d in directions]
    require(all(v in directions for v in ((1, 0), (-1, 0), (0, 1), (0, -1))),
            "cardinal bounding constraints missing")
    vertices = set()
    independent_pairs = 0
    for a, b in combinations(normals, 2):
        determinant = cross(a, b)
        if not determinant:
            continue
        independent_pairs += 1
        v = ((b[1] - a[1]) / determinant, (a[0] - b[0]) / determinant)
        if all(dot(n, v) <= 1 for n in normals):
            vertices.add(v)
    require(len(vertices) == 12, "dual polygon vertex count changed")
    for v in vertices:
        active = [n for n in normals if dot(n, v) == 1]
        require(any(cross(a, b) for a, b in combinations(active, 2)), "spurious dual vertex")
    return sorted(vertices), independent_pairs


def certificate_values(vertices_a, vertices_b, h):
    require(sum(h[i][i] for i in range(3)) < 0, "certificate has no negative trace")
    values = [dot(u + (F(1),), matvec(h, v + (F(1),)))
              for u, v in product(vertices_a, vertices_b)]
    require(min(values) >= 0, "certificate is negative on a dual generator pair")
    return values


def dual_certificate():
    data = (BASE / "EXPECTED.json").read_bytes()
    require(sha256(data).hexdigest() == ORIGINAL, "original fixture changed")
    fixture = json.loads(data)["fixture"]
    directions = [tuple(map(F, d)) for d in fixture["directions"]]
    p, q = F(fixture["p"]), F(fixture["q"])
    va, pairs_a = dual_vertices(directions, p)
    vb, pairs_b = dual_vertices(directions, q)
    h = diagonal((F(-8), F(-8), F(15)))
    values = certificate_values(va, vb, h)
    require((min(values), max(values)) == (F(5, 27), F(805, 27)), "certificate margin changed")
    maximum_dot = max(dot(u, v) for u, v in product(va, vb))
    require(maximum_dot == F(50, 27), "transverse product bound changed")
    require(max(map(norm2, va)) == F(160, 81), "first dual circumradius changed")
    require(max(map(norm2, vb)) == F(125, 72), "second dual circumradius changed")
    controls = []
    for name, invalid in [
            ("negative generator despite negative trace", diagonal((F(-1), F(-1), F(1)))),
            ("nonnegative trace", diagonal((F(0), F(0), F(1))))]:
        try:
            certificate_values(va, vb, invalid)
        except ValueError:
            controls.append(name + " rejected")
        else:
            raise ValueError("invalid certificate accepted: " + name)
    encoded = json.dumps([str(x) for x in values], separators=(",", ":")).encode()
    return {
        "p": str(p), "q": str(q), "original_expected_sha256": ORIGINAL,
        "dual_vertices_a": [[str(x) for x in v] for v in va],
        "dual_vertices_b": [[str(x) for x in v] for v in vb],
        "independent_boundary_pairs_examined": [pairs_a, pairs_b],
        "dual_generator_pairs": len(values),
        "all_pairs_strictly_positive": all(x > 0 for x in values),
        "certificate_diagonal": [-8, -8, 15], "trace": -1,
        "minimum_generator_value": str(min(values)), "maximum_generator_value": str(max(values)),
        "maximum_transverse_dot": str(maximum_dot),
        "generator_values_sha256": sha256(encoded).hexdigest(), "invalid_controls": controls,
    }


def fold_control():
    identity = diagonal((F(1),) * 3)
    zero = (F(0),) * 3
    c, s = F(3, 5), F(4, 5)
    q = ((c, -s, F(0)), (s, c, F(0)), (F(0), F(0), F(1)))
    ry = ((F(1), F(0), F(0)), (F(0), c, -s), (F(0), s, c))
    frames = [identity, q, ry, identity]
    translations = [zero, (F(1), F(2), F(-1)), (F(-1), F(0), F(3)), zero]
    for frame in [q, *frames]:
        require(matmul(transpose(frame), frame) == identity, "nonorthogonal control frame")
    a = list(transpose(q))
    b = [tuple((i + 2) * x for x in v) for i, v in enumerate(a)]
    relative = [matmul(matmul(q, diagonal(tuple(F(1 if i < j else -1) for i in range(3)))),
                       transpose(q)) for j in range(4)]
    clouds = [[zero] + a + [matvec(l, v) for v in b] for l in relative]
    physical = [[tuple(x + t for x, t in zip(matvec(frame, v), shift)) for v in cloud]
                for cloud, frame, shift in zip(clouds, frames, translations)]
    require(relative[0] == scale(identity, -1) and relative[-1] == identity, "wrong control endpoints")
    require(all(len(set(cloud)) == 7 for cloud in physical), "control has a collision")
    accumulated = scale(identity, 0)
    coordinate_checks = 0
    strict_pair_losses = []
    for j in range(3):
        # Independent physical endpoint frames, also with target coordinate signs.
        source_frame = matmul(transpose(q), transpose(frames[j]))
        target_frame = matmul(diagonal((F(-1), F(1), F(-1))),
                              matmul(transpose(q), transpose(frames[j + 1])))
        for i, k in combinations(range(7), 2):
            dx = sub(physical[j][i], physical[j][k])
            dy = sub(physical[j + 1][i], physical[j + 1][k])
            px, py = matvec(source_frame, dx), matvec(target_frame, dy)
            require(all(abs(y) <= abs(x) for x, y in zip(px, py)), "fold control is not strong")
            coordinate_checks += 3
            loss = dot(dx, dx) - dot(dy, dy)
            require(loss >= 0, "fold control expands a pair")
            if loss:
                strict_pair_losses.append(str(loss))
        u = a[j]
        v = neg(matvec(transpose(relative[j]), u))
        require(all(dot(u, point) >= 0 for point in a), "control u outside A dual")
        require(all(dot(v, point) >= 0 for point in b), "control v outside B dual")
        term = outer(u, v)
        difference = matrix_add(relative[j + 1], scale(relative[j], -1))
        require(difference == scale(term, 2), "rank-one increment identity fails")
        accumulated = matrix_add(accumulated, term)
    require(accumulated == identity, "rank-one increments do not telescope to identity")
    require(strict_pair_losses == ["8", "12", "16"], "control contraction losses changed")
    return {"sites": 7, "steps": 3, "coordinate_inequalities_checked": coordinate_checks,
            "strict_squared_pair_losses": strict_pair_losses,
            "independent_rigid_frames_and_moving_origin": True,
            "rank_one_sum": [[str(x) for x in row] for row in accumulated]}


def run():
    return {"status": "AXIAL_STRONG_COMPOSITION_AUDITS_PASS",
            "arithmetic": "integers and fractions.Fraction",
            "dual_certificate": dual_certificate(), "rotated_orthant_positive_control": fold_control(),
            "trust_boundary": "Written theorem excludes every finite length; code audits its rational certificate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = (json.dumps(run(), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        require(output == (BASE / "EXPECTED_COMPOSITIONS.json").read_bytes(), "composition output mismatch")
        print("AXIAL_STRONG_COMPOSITION_AUDITS_PASS " + sha256(output).hexdigest())
    else:
        print(output.decode(), end="")


if __name__ == "__main__":
    main()
