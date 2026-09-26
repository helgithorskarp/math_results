#!/usr/bin/env python3
"""Reconstruct compact rational packets and audit the rank-face boundary."""
from fractions import Fraction as F
import json
from pathlib import Path
from certify import A, B, derive, distance, dot, outside, require, solve

HERE = Path(__file__).resolve().parent


def rank(rows):
    m = [list(map(F, row)) for row in rows]
    k = 0
    for j in range(len(m[0])):
        pivot = next((i for i in range(k, len(m)) if m[i][j]), None)
        if pivot is None:
            continue
        m[k], m[pivot] = m[pivot], m[k]
        v = m[k][j]
        m[k] = [x/v for x in m[k]]
        for i in range(k+1, len(m)):
            v = m[i][j]
            m[i] = [x-v*y for x, y in zip(m[i], m[k])]
        k += 1
        if k == len(m):
            break
    return k


def norm2(v):
    return dot(v, v)


def run():
    cert = derive()
    packets = json.loads((HERE / "PACKETS.json").read_text())
    require(packets["schema"] == "historical-two-scale-packets-v1", "packet schema")
    out = []
    for p in packets["packets"]:
        matrix = [list(map(F, row)) for row in p["matrix"]]
        require(rank(matrix) == 3, "singular polar matrix")
        radii = list(map(F, p["radii"]))
        require(len(radii) == 2 and min(radii) > 0 and radii[0] != radii[1], "radii")
        w = list(map(F, p["weights"]))
        require(len(w) == 16 and min(w) > 0 and sum(w) == 1, "probability weights")
        aa = [[r*dot(row, v) for row in matrix] for r in radii for v in A]
        bb = [[r*x for x in solve(list(zip(*matrix)), v)] for r in radii for v in B]
        xx = aa + [[-x for x in v] for v in bb]
        yy = aa + bb
        losses = [[norm2([x-y for x, y in zip(xx[i], xx[j])])
                   - norm2([x-y for x, y in zip(yy[i], yy[j])]) for j in range(16)] for i in range(16)]
        require(min(map(min, losses)) >= 0, "not a contraction")
        paired = [[1]+x+y for x, y in zip(xx, yy)]
        require(rank(paired) == 7, "full paired rank")
        mask = min(cert["maximal_face_masks"], key=lambda m: (outside(w, m), m))
        indices = [i for i in range(16) if mask >> i & 1]
        require(rank([paired[i] for i in indices]) == 6, "conditional rank")
        eps = outside(w, mask)
        q = 1-eps
        means = [[sum(w[i]*z[i][j] for i in indices)/q for j in range(3)] for z in (xx, yy)]
        r2 = max(norm2([z[i][j]-mu[j] for j in range(3)]) for z, mu in zip((xx, yy), means) for i in indices)
        d = sum(w[i]*w[j]*losses[i][j] for i in indices for j in indices)/(q*q)
        require(0 < d <= 2*r2, "distance loss and radius")
        out.append({"name": p["name"], "paired_rank": 6, "closest_face": mask,
                    "face_size": len(indices), "core_paired_rank": 5,
                    "rank_reserve": str(eps), "isometric_reserve": str(distance(w, cert["lifted_isometric_masks"])),
                    "core_D_at_variance_one": str(d), "core_R_squared_at_variance_one": str(r2)})
    return out


if __name__ == "__main__":
    actual = run()
    expected = json.loads((HERE / "PACKET_AUDIT.json").read_text())
    require(actual == expected, "packet audit differs")
    print(json.dumps({"packets": len(actual), "pair_checks": 120*len(actual),
                      "full_rank": "6", "closest_core_rank": "5", "status": "PASS; no Gaussian sign asserted"}, sort_keys=True))
