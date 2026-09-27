#!/usr/bin/env python3
"""Exact controls for STRONG_CLOSURE.md; no chain search or radius claim.

The old seven-site fixture is deliberately retained. This checker has no
imports from earlier packets. Compactness and the universal scalar-frame
argument remain written mathematics, not computer-assisted theorems.
"""

import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def determinant(rows):
    a = [list(map(F, row)) for row in rows]
    n = len(a)
    require(all(len(row) == n for row in a), "square determinant")
    result = F(1)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            result = -result
        v = a[k][k]
        result *= v
        for j in range(k + 1, n):
            t = a[j][k] / v
            for col in range(k + 1, n):
                a[j][col] -= t * a[k][col]
    return result


PAIRS = tuple(combinations(range(7), 2))


def distances(points):
    return tuple(dot(sub(points[i], points[j]), sub(points[i], points[j]))
                 for i, j in PAIRS)


def fixture():
    p = [tuple(map(F, x)) for x in (
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2))]
    normals = [(1, 1, 1), (1, -1, -1), (-1, 1, -1)]
    q = p[:4] + [tuple(x - F(8, 3) * v for x, v in zip(p[i+4], normals[i]))
                  for i in range(3)]
    return {"p": p, "q": q, "normals": normals,
            "faces": [(0, 2, 3), (0, 1, 3), (0, 1, 2)],
            "interval_bits": ["000", "111"]}


def check(data):
    p, q, normals, faces = (data[k] for k in ("p", "q", "normals", "faces"))
    require(len(set(p)) == len(set(q)) == 7, "distinct endpoints")
    require(p[:4] == q[:4], "fixed core")
    core_det = determinant([sub(x, p[0]) for x in p[1:4]])
    require(core_det == -2, "core determinant")
    d0, d1 = distances(p), distances(q)
    require(all(a >= b for a, b in zip(d0, d1)), "endpoint contraction")
    require(sum(a == b for a, b in zip(d0, d1)) == 15, "tight count")
    for i, (v, face) in enumerate(zip(normals, faces)):
        require(len(face) == len(set(face)) == 3, "three face anchors")
        require(all(dot(v, p[j]) == 0 for j in face), "anchor plane")
        a, b, c = (p[j] for j in face)
        face_normal = cross(sub(b, a), sub(c, a))
        require(dot(face_normal, face_normal) > 0, "noncollinear anchors")
        require(cross(face_normal, v) == (0, 0, 0), "face normal")
        require(dot(v, p[i+4]) == 4, "nonzero depth")
        require(sub(p[i+4], q[i+4]) == tuple(F(8, 3)*z for z in v),
                "reflection displacement")
        for j in face:
            anchor = p[j]
            require(dot(sub(p[i+4], anchor), sub(p[i+4], anchor)) ==
                    dot(sub(q[i+4], anchor), sub(q[i+4], anchor)), "tight attachment")
    require(determinant(normals) == 4, "independent normals")
    require(all(dot(normals[i], normals[j]) == -1
                for i, j in combinations(range(3), 2)), "nonorthogonal normals")
    require([dot(v, (1, 1, -1)) for v in normals] == [1, 1, 1],
            "hemisphere witness")
    for x in p:
        values = [dot(v, x) for v in normals]
        require(all(values[i] + 2*values[(i+1) % 3] <= 0 for i in range(3)),
                "whole-hull affine cap separators")
    table = [F(54), F(34, 3), F(130, 3), F(134, 9)]
    for i in range(3):
        j = (i+1) % 3
        actual = []
        for bi, bj in ((0, 0), (1, 0), (0, 1), (1, 1)):
            x = (p, q)[bi][i+4]
            y = (p, q)[bj][j+4]
            actual.append(dot(sub(x, y), sub(x, y)))
        require(actual == table, "cyclic table")
    interval, rejected = [], {}
    for bits in product((0, 1), repeat=3):
        points = p[:4] + [(p, q)[b][i+4] for i, b in enumerate(bits)]
        d = distances(points)
        label = "".join(map(str, bits))
        if all(lo <= v <= hi for lo, v, hi in zip(d1, d, d0)):
            interval.append(label)
        else:
            i = next(i for i in range(3) if bits[i] == 1 and bits[(i+1) % 3] == 0)
            rejected[label] = {"cyclic_pair": [i, (i+1) % 3],
                               "squared_shortfall": str(F(134, 9)-F(34, 3))}
    require(interval == data["interval_bits"], "complete interval")
    paired = [x+y for x, y in zip(p, q)]
    paired_det = determinant([sub(x, paired[0]) for x in paired[1:]])
    require(paired_det == F(4096, 27), "paired affine determinant")
    require(d0[PAIRS.index((0, 1))] == 2 and d1[PAIRS.index((0, 4))] == 30,
            "uniform contraction exclusion")
    return {"core_determinant": str(core_det), "paired_determinant": str(paired_det),
            "labels": 7, "endpoint_pairs": 21, "tight_pairs": 15,
            "interval_bits": interval, "excluded_states": rejected,
            "cyclic_table": list(map(str, table)),
            "normal_determinant": "4", "uniform_obstruction_squared": [2, 30]}


def record():
    data = fixture()
    result = check(data)
    bad = []
    altered = deepcopy(data)
    altered["q"][4] = tuple(x+F(1, 3) for x in altered["q"][4])
    bad.append(("changed_target", altered))
    altered = deepcopy(data)
    altered["faces"][0] = (0, 1, 3)
    bad.append(("wrong_tight_face", altered))
    altered = deepcopy(data)
    altered["interval_bits"] = ["000", "100", "111"]
    bad.append(("false_intermediate_state", altered))
    rejected = []
    for name, item in bad:
        try:
            check(item)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("damaged input accepted: " + name)
    return {"status": "FINITE_INTERVAL_STRONG_CLOSURE_CONTROLS_PASS",
            "control": result, "damaged_inputs_rejected": rejected,
            "scope": "Exact old fixture only; no numerical neighborhood, general-frame solver, chain enumeration or Gaussian sign calculation."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = record()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.emit:
        print(encoded, end="")
    else:
        expected = Path(__file__).with_name("STRONG_CLOSURE_EXPECTED.json")
        require(expected.read_text() == encoded, "frozen record differs")
        print(result["status"])
        print("expected_sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
