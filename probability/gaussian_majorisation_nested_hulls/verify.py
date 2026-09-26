#!/usr/bin/env python3
"""Exact supplementary certificate for PROOF.md; Python 3.11+, stdlib only.

No numerical integration and no sampling substitute for the written proof.
Polynomial coefficients are Fractions in increasing powers of depth b.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def poly(*a):
    a = list(map(F, a)) or [F(0)]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


ZERO = poly(0)
ONE = poly(1)
DEPTH = poly(0, 1)


def add(a, b):
    return poly(*(sum(t) for t in zip(
        a + (F(0),) * max(0, len(b) - len(a)),
        b + (F(0),) * max(0, len(a) - len(b)))))


def scale(a, b):
    return poly(*(b * x for x in a))


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return poly(*out)


def evaluate(a, x):
    out = F(0)
    for c in reversed(a):
        out = out * x + c
    return out


def vec_sub(a, b):
    return tuple(sub(x, y) for x, y in zip(a, b))


def dot(a, b):
    out = ZERO
    for x, y in zip(a, b):
        out = add(out, mul(x, y))
    return out


def determinant(matrix):
    """Definition-level Leibniz determinant over rational polynomials."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare matrix")
    out = ZERO
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = ONE
        for i, j in enumerate(p):
            term = mul(term, matrix[i][j])
        out = add(out, scale(term, (-1) ** inversions))
    return out


def strings(a):
    return [str(x) for x in a]


U = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def build():
    labels = ["origin"] + [f"anchor{i}" for i in range(4)]
    source = [(ZERO,) * 3] + [tuple(poly(x) for x in u) for u in U]
    target = list(source)
    kinds = [("origin",)] + [("anchor", i) for i in range(4)]
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            labels.append(f"flap{i}{j}")
            kinds.append(("flap", i, j))
            source.append(tuple(poly(U[j][k], -U[i][k]) for k in range(3)))
            target.append(tuple(poly(U[j][k], U[i][k]) for k in range(3)))
    return labels, kinds, source, target


def expected_deficit(a, b):
    if a[0] != "flap" and b[0] != "flap":
        return ZERO
    if a[0] == "flap" and b[0] != "flap":
        a, b = b, a
    if a[0] == "origin":
        return scale(DEPTH, 4)
    if a[0] == "anchor":
        return scale(DEPTH, 16 * (a[1] == b[1]))
    _, i, j = a
    _, k, l = b
    return scale(DEPTH, 16 * ((j == k) + (l == i)))


def check_geometry():
    labels, kinds, source, target = build()
    records = []
    count = Counter()
    for i, j in combinations(range(len(labels)), 2):
        p = vec_sub(source[i], source[j])
        q = vec_sub(target[i], target[j])
        deficit = sub(dot(p, p), dot(q, q))
        require(deficit == expected_deficit(kinds[i], kinds[j]), "pair identity failed")
        require(all(x >= 0 for x in deficit), "negative depth coefficient")
        coefficient = deficit[1] if len(deficit) == 2 else F(0)
        count[str(coefficient)] += 1
        records.append([labels[i], labels[j], strings(deficit)])
    require(len(records) == 136, "incorrect pair coverage")
    require(count == {"0": 82, "4": 12, "16": 36, "32": 6}, "incorrect pair census")

    for name, p, q in zip(labels, source, target):
        if not name.startswith("flap"):
            continue
        require(dot(p, p) == poly(3, 2, 3), "source radius identity")
        require(dot(q, q) == poly(3, -2, 3), "target radius identity")
    require(sub(poly(3, 2, 3), poly(3)) == poly(0, 2, 3), "anchor radius gap")

    chosen = [f"anchor{i}" for i in range(3)] + [f"flap{i}3" for i in range(3)]
    rows = [source[labels.index(name)] + target[labels.index(name)] for name in chosen]
    det = determinant(rows)
    require(det == poly(0, 0, 0, 128), "rank-six minor")
    # Check the block-determinant derivation against direct six-by-six expansion.
    det_u = determinant([tuple(poly(x) for x in U[i]) for i in range(3)])
    block = mul(poly(0, 0, 0, 8), mul(det_u, det_u))
    require(det == block and det_u == poly(4), "independent block factorization")

    # At b=1, independently certify each output by an explicit convex combination
    # of source points, without using the sorted support-function formula.
    p1 = {name: tuple(evaluate(x, F(1)) for x in p) for name, p in zip(labels, source)}
    q1 = {name: tuple(evaluate(x, F(1)) for x in q) for name, q in zip(labels, target)}
    barycentric = []
    for name, kind in zip(labels, kinds):
        if kind[0] == "flap":
            _, i, j = kind
            k, l = [t for t in range(4) if t not in (i, j)]
            terms = [(f"flap{k}{j}", F(1, 2)), (f"flap{l}{i}", F(1, 2))]
        else:
            terms = [(name, F(1))]
        require(sum(w for _, w in terms) == 1, "barycentric mass")
        require(all(w >= 0 for _, w in terms), "barycentric positivity")
        decoded = tuple(sum(w * p1[label][k] for label, w in terms) for k in range(3))
        require(decoded == q1[name], "barycentric output mismatch")
        barycentric.append([name, [[label, str(w)] for label, w in terms]])

    # Depth zero is a rigid control, excluded by strict-radius hypotheses.
    require(all(tuple(evaluate(c, F(0)) for c in p) ==
                tuple(evaluate(c, F(0)) for c in q)
                for p, q in zip(source, target)), "depth-zero equality")
    encoded = json.dumps({"pairs": records, "hull": barycentric}, sort_keys=True, separators=(",", ":"))
    return {
        "labels": len(labels), "pairs": len(records), "deficit_coefficient_counts": dict(count),
        "rank_minor_labels": chosen, "rank_minor_coefficients": strings(det),
        "barycentric_images_checked": len(barycentric),
        "geometry_records_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }


def check_support():
    # Coefficients of A,B,C,D in u=A-B, v=B-C, w=C-D, with sum zero.
    projections = [tuple(map(F, a)) for a in
                   [(F(3, 4), F(1, 2), F(1, 4)),
                    (F(-1, 4), F(1, 2), F(1, 4)),
                    (F(-1, 4), F(-1, 2), F(1, 4)),
                    (F(-1, 4), F(-1, 2), F(-3, 4))]]
    A, B, C, D = projections
    require(all(sum(row[k] for row in projections) == 0 for k in range(3)), "projection sum")
    require(tuple(A[k] - B[k] for k in range(3)) == (1, 0, 0), "first gap")
    require(tuple(B[k] - C[k] for k in range(3)) == (0, 1, 0), "second gap")
    require(tuple(C[k] - D[k] for k in range(3)) == (0, 0, 1), "third gap")
    outward = [poly(A[k], -D[k]) for k in range(3)]
    inward_low = [poly(A[k], B[k]) for k in range(3)]
    inward_high = [poly(B[k], A[k]) for k in range(3)]
    low = [sub(a, b) for a, b in zip(outward, inward_low)]
    high = [sub(a, b) for a, b in zip(outward, inward_high)]
    require(low == [poly(0, F(1, 2)), ZERO, poly(0, F(1, 2))], "low-depth support identity")
    require(high == [poly(1, F(-1, 2)), ZERO, poly(0, F(1, 2))], "high-depth support identity")
    # These coefficients are affine in b. Endpoint checks certify the entire
    # indicated intervals, not just the endpoint configurations.
    for coefficients, left, right in [(low, F(0), F(1)), (high, F(1), F(2))]:
        require(all(len(p) <= 2 for p in coefficients), "unexpected support degree")
        require(all(evaluate(p, left) >= 0 and evaluate(p, right) >= 0 for p in coefficients),
                "negative affine coefficient on depth interval")
    # Directly evaluate all labelled projections in the direction u0 at b=3.
    _, _, source, target = build()
    direction = U[0]
    hp = max(sum(evaluate(p[k], F(3)) * direction[k] for k in range(3)) for p in source)
    hq = max(sum(evaluate(q[k], F(3)) * direction[k] for k in range(3)) for q in target)
    require(hp == 6 and hq == 8, "depth-three nesting failure control")
    return {"gap_coefficients_depth_0_to_1": [strings(x) for x in low],
            "gap_coefficients_depth_1_to_2": [strings(x) for x in high],
            "depth_three_support_gap": str(hp - hq)}


def check_tail_certificate():
    source_norm_squared, target_norm_squared = F(8), F(4)
    cap_cosine, support_lower, cut = F(15, 16), F(21, 8), F(5, 2)
    require(source_norm_squared * cap_cosine ** 2 > support_lower ** 2,
            "cap support lower bound")
    require(support_lower - cut == F(1, 8), "cap clearance")
    require(target_norm_squared == 2 ** 2 and cut >= 2, "target support bound")
    cap_fraction = (1 - cap_cosine) / 2  # spherical cap area divided by 4*pi
    normalized_geometric_gap = cap_fraction * F(1, 8)
    require(normalized_geometric_gap == F(1, 256), "normalized cap margin")

    # Positive exponential Taylor terms give exp(7/10)>2, hence log(2)<7/10.
    exp_lower = sum((F(7, 10) ** k / factorial(k) for k in range(4)), F(0))
    require(exp_lower == F(12013, 6000) and exp_lower > 2, "rational logarithm bound")
    lhat, big_b, wmin = F(3), F(4), F(1, 16)
    require(lhat ** 2 > source_norm_squared, "enclosing radius")
    require(2 / wmin == 2 ** 5, "logarithm normalization")
    e_bound = 5 * F(7, 10) + lhat * big_b + lhat ** 2 / 2 + big_b ** 2 / 2
    require(e_bound == 28, "boundary error constant")
    pair_error_coefficient = 2 * (e_bound + big_b ** 2 + big_b ** 3 / 3 + 40)
    require(pair_error_coefficient == F(632, 3), "pair error constant")
    radius = F(65536)
    require(radius >= 2 * big_b, "finite asymptotic domain")
    margin = normalized_geometric_gap - pair_error_coefficient / radius
    require(margin == F(17, 24576) and margin > 0, "continuous tail positivity margin")
    return {"epsilon_range": "0 < epsilon <= 1/2", "variance": 1,
            "rare_weights": "sixteen weights, each 1/16", "depth": 1,
            "minimum_reference_radius": str(radius), "maximum_log_mass_over_radius": str(cut),
            "normalized_geometric_gap_lower": str(normalized_geometric_gap),
            "normalized_hinge_gap_lower": str(margin),
            "normalized_hinge_gap_denominator": "4*pi*a*R^2",
            "all_threshold_epsilon_bound": "not supplied"}


def factorial(k):
    out = 1
    for i in range(2, k + 1):
        out *= i
    return out


def main():
    result = {"status": "all exact supplementary checks passed",
              "claim_status": "author proof; independent review pending",
              "geometry": check_geometry(), "support": check_support(),
              "tail_certificate": check_tail_certificate(),
              "universal_analytic_proof": "PROOF.md Sections 2-5; not formalized"}
    expected = Path(__file__).with_name("EXPECTED.json")
    if expected.exists():
        require(result == json.loads(expected.read_text()), "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
