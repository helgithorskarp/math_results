#!/usr/bin/env python3
"""Exact symbolic face construction and rational constant checks. Python >=3.11."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1)]
B = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
IMPORTED = HERE.parent / "gaussian_majorisation_minimax_faces/CERTIFICATE.json"
IMPORTED_SHA = "702790f3ca82a3dfaf28ea0248536b125ab346b99388311ea6827924fc53486d"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def solve(rows, rhs):
    m = [[F(x) for x in row] + [F(y)] for row, y in zip(rows, rhs)]
    for j in range(3):
        pivot = next((i for i in range(j, 3) if m[i][j]), None)
        require(pivot is not None, "dependent ray triple")
        m[j], m[pivot] = m[pivot], m[j]
        d = m[j][j]
        m[j] = [x / d for x in m[j]]
        for i in range(3):
            if i != j:
                d = m[i][j]
                m[i] = [x - d * y for x, y in zip(m[i], m[j])]
    return [row[-1] for row in m]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sections(rays):
    """Normals are formal p*u_p+q*u_q, p=1/r0, q=1/r1, p!=q."""
    out = {}
    for triple in combinations(range(4), 3):
        for scales in product(range(2), repeat=3):
            up = solve([rays[i] for i in triple], [int(k == 0) for k in scales])
            uq = solve([rays[i] for i in triple], [int(k == 1) for k in scales])
            mask = 0
            for i, v in enumerate(rays):
                cp, cq = dot(up, v), dot(uq, v)
                require(cp + cq == 1 and cp in (-1, 0, 1, 2), "unexpected formal value")
                if cp == 1:
                    mask |= 1 << i
                if cp == 0:
                    mask |= 1 << (i + 4)
            row = {"mask": mask, "normal_p": list(map(str, up)), "normal_q": list(map(str, uq))}
            require(mask not in out or out[mask] == row, "inconsistent section")
            out[mask] = row
    require(Counter(x.bit_count() for x in out) == {3: 8, 4: 6}, "section count")
    return [out[k] for k in sorted(out)]


def lift_isometric(mask):
    a, b = mask & 15, mask >> 4
    return a | (a << 4) | (b << 8) | (b << 12)


def outside(weights, mask):
    return sum((w for i, w in enumerate(weights) if not (mask >> i & 1)), F(0))


def distance(weights, masks):
    return min(outside(weights, m) for m in masks)


def constant_checks():
    """Only rational inequalities supporting the written analytic proof."""
    peak_difference = 1 - F(1, 32) - F(1, 4)
    require(peak_difference == F(23, 32), "source peak minus threshold")
    z = F(7, 10)
    require(1 + z + z*z/2 + z*z*z/6 > 2, "log 2 upper bound")
    require(8*z < F(12, 5)**2, "sqrt(2 log 16) bound")
    exponent = (1 + F(12, 5))**2
    require(exponent == F(289, 25) < 12, "exponent bound")
    require(F(65, 24) + F(1, 100) == F(1631, 600) < F(11, 4), "e upper bound")
    require(F(8, 3)**5 > 32*F(22, 7), "Theorem H prefactor lower bound")
    gap_bound = F(1, 384) * peak_difference**4 * F(4, 11)**12
    require(gap_bound == F(279841, 75322281041304), "core gap arithmetic")
    eps = F(1, 10**9)
    full = (1-eps)*gap_bound-eps
    require(full > eps, "contamination exclusion")
    return {"source_peak_minus_threshold_lower": str(peak_difference), "exponent_upper": str(exponent),
            "core_gap_lower": str(gap_bound),
            "full_gap_lower": str(full), "claimed_full_gap_lower": str(eps)}


def derive():
    sa, sb = sections(A), sections(B)
    zero = set()
    for i, j in combinations(range(4), 2):
        two = (1 << i) | (1 << j) | (1 << (i+4)) | (1 << (j+4))
        zero.add(255 | (two << 8))
        zero.add(two | (255 << 8))
    nonzero = {a["mask"] | (b["mask"] << 8) for a in sa for b in sb}
    faces = sorted(zero | nonzero)
    require(len(faces) == 208 and not zero & nonzero, "face count")
    require(all(not (m != n and m & n == m) for m in faces for n in faces), "nonmaximal face")
    counts = dict(sorted(Counter(m.bit_count() for m in faces).items()))
    require(counts == {6: 64, 7: 96, 8: 36, 12: 12}, "face size distribution")
    raw = IMPORTED.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == IMPORTED_SHA, "imported certificate changed")
    old = [lift_isometric(r["mask"]) for r in json.loads(raw)["maximal_faces"]]
    require(len(old) == 10 and all(any(m & n == m for n in faces) for m in old), "isometric containment")
    uniform = [F(1, 16)]*16
    base = [F(1, 16)]*8 + [F(1, 8), F(1, 8), F(0), F(0)]*2
    eps = F(1, 1000)
    w = [(1-eps)*a + eps*b for a, b in zip(base, uniform)]
    require(sum(w) == 1 and min(w) == F(1, 16000), "example weights")
    require(distance(uniform, faces) == F(1, 4), "sharp reserve")
    require(distance(w, faces) == F(1, 4000), "example rank distance")
    require(distance(w, old) == F(1501, 4000), "example isometric distance")
    require(sum(w[i] for i in [0, 1, 2, 3, 8, 9, 10, 11]) == F(1, 2), "scale reserve")
    # Universal epsilon formula: all distances are affine in epsilon.
    # The proposed minimizer dominates every face at both interval endpoints.
    rank_min = 255 | (51 << 8)
    for endpoint in (F(0), F(1)):
        we = [(1-endpoint)*a + endpoint*b for a, b in zip(base, uniform)]
        require(outside(we, rank_min) == endpoint/4 == distance(we, faces), "rank distance segment")
    iso_min = min(old, key=lambda m: outside(base, m))
    for endpoint in (F(0), F(1, 2)):
        we = [(1-endpoint)*a + endpoint*b for a, b in zip(base, uniform)]
        require(outside(we, iso_min) == F(3, 8)+endpoint/4 == distance(we, old), "isometric segment")
    return {"schema": "two-scale-rank-five-faces-v1", "A_rays": A, "B_rays": B,
            "A_sections": sa, "B_sections": sb, "maximal_face_masks": faces,
            "face_size_counts": counts, "isometric_certificate_sha256": IMPORTED_SHA,
            "lifted_isometric_masks": old, "maximum_rank_reserve": "1/4",
            "separation_example": {"epsilon": str(eps), "weights": list(map(str, w)),
                "rank_reserve": "1/4000", "isometric_reserve": "1501/4000", "scale_masses": ["1/2", "1/2"]},
            "constant_checks": constant_checks()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate compact exact certificate")
    parser.add_argument("--certificate", type=Path, default=HERE / "CERTIFICATE.json")
    args = parser.parse_args()
    result = derive()
    canonical = json.loads(json.dumps(result))
    if args.write:
        args.certificate.write_text(json.dumps(result, indent=2) + "\n")
    require(json.loads(args.certificate.read_text()) == canonical, "certificate differs from exact derivation")
    print(json.dumps({"faces": len(result["maximal_face_masks"]), "sizes": result["face_size_counts"],
                      "constants": "PASS", "isometric_containment": "10/10", "separation_example": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
