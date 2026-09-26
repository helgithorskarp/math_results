#!/usr/bin/env python3
"""Exact algebra accompanying PROOF.md; Python >=3.11, standard library only.

The universal Gaussian and compact-volume arguments are written proofs.
This program does not numerically test a Gaussian hinge or a ball volume.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def norm2(a):
    return dot(a, a)


def rref(rows):
    a = [list(map(Q, row)) for row in rows]
    if not a:
        return []
    pivot = 0
    for col in range(len(a[0])):
        candidate = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if candidate is None:
            continue
        a[pivot], a[candidate] = a[candidate], a[pivot]
        factor = a[pivot][col]
        a[pivot] = [x / factor for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][col]:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return [row for row in a if any(row)]


def rank(rows):
    return len(rref(rows))


def affine_rank(points):
    return rank([sub(p, points[0]) for p in points[1:]])


SIGNS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
PLANES = ((0, 1), (0, 2), (1, 2))
U = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
AXES = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1))


def make_ray(plane, signs):
    i, j = plane
    sigma, tau = signs
    v = [0, 0, 0]
    v[i], v[j] = sigma, tau
    s = [0, 0, 0]
    s[3 - i - j] = sigma * tau
    if i == 0:
        rematch = (sigma, 0, 0)
    else:
        rematch = (0, Q(sigma + tau, 2), Q(tau - sigma, 2))
    return {"plane": plane, "signs": signs, "v": tuple(v), "S": tuple(s),
            "R": rematch}


RAYS = [make_ray(plane, signs) for plane in PLANES for signs in SIGNS]


def coefficients(a, b, name):
    """Coefficients of r^2, rt, t^2, directly from the two distance squares."""
    v, w = a["v"], a[name]
    vv, ww = b["v"], b[name]
    return (norm2(v) - norm2(w), -2 * (dot(v, vv) - dot(w, ww)),
            norm2(vv) - norm2(ww))


def claimed_coefficients(a, b, name):
    """Independent branch descriptions in the geometric lemma's table."""
    pa, pb = a["plane"], b["plane"]
    sa, ta = a["signs"]
    sb, tb = b["signs"]
    if name == "S" and pa == pb:
        return (1, 6 if sa * sb == ta * tb == -1 else -2, 1)
    if name == "R":
        if pa == pb and pa != (1, 2):
            return (1, -2 * ta * tb, 1)
        if pa == pb:
            return (1, -(sa * sb + ta * tb), 1)
        if (1, 2) not in (pa, pb):
            return (1, 0, 1)
    shared = (set(pa) & set(pb)).pop()
    return (1, -2 * a["v"][shared] * b["v"][shared], 1)


def incidence(name):
    return [[int(ray[name] == axis) for ray in RAYS] for axis in AXES]


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def output_law(radial_weights, core_weights, name):
    result = defaultdict(Q)
    for r, weights in radial_weights.items():
        for ray, weight in zip(RAYS, weights):
            result[scale(r, ray[name])] += weight
    for point, weight in zip(U, core_weights):
        result[point] += weight
    return dict(result)


def effective_radii(radii, name, operation):
    return tuple(operation(radii[j] for j, ray in enumerate(RAYS)
                           if ray[name] == axis) for axis in AXES)


def main():
    records = []
    distribution = {}
    for name in ("S", "R"):
        counts = Counter()
        for ia, ib in product(range(12), repeat=2):
            a, b = RAYS[ia], RAYS[ib]
            coeff = coefficients(a, b, name)
            require(coeff == claimed_coefficients(a, b, name),
                    f"Ray identity failed: {name}, {ia}, {ib}")
            # (r-t)^2 + (coeff[1]+2)*rt is a nonnegative certificate for r,t>=0.
            require(coeff[0] == coeff[2] == 1 and coeff[1] >= -2,
                    "Nonnegative polynomial certificate failed")
            counts[int(coeff[1])] += 1
            records.append([name, ia, ib, list(map(int, coeff))])
        distribution[name] = dict(sorted(counts.items()))

    expected_core_vectors = {
        "S": {scale(-1, u) for u in U}, "R": set(AXES[2:])}
    for name in ("S", "R"):
        vectors = [sub(ray["v"], ray[name]) for ray in RAYS]
        require(set(vectors) == expected_core_vectors[name], "Fixed-region normals")
        require(all(n == 3 for n in Counter(vectors).values()), "Core multiplicities")
        for ray, vector in zip(RAYS, vectors):
            require(norm2(ray["v"]) - norm2(ray[name]) == 1, "Core r^2 coefficient")
            require(max(dot(u, vector) for u in U) == 1, "Tetrahedral support bound")
    require(all(ray["v"][0] == ray["R"][0] for ray in RAYS), "Preserved coordinate")
    for name in ("S", "R"):
        a, v, w = U[0], RAYS[0]["v"], RAYS[0][name]
        require(norm2(sub(v, a)) - norm2(sub(w, a)) == -1, "Cutoff control")
    outside = (2, 0, 0)
    ray = RAYS[0]
    require(norm2(sub(scale(2, ray["v"]), outside))
            - norm2(sub(scale(2, ray["S"]), outside)) == -4, "Outside-core control")

    ranks = {}
    for name in ("S", "R"):
        paired = [u + u for u in U]
        paired += [scale(2, ray["v"]) + scale(2, ray[name]) for ray in RAYS]
        ranks[name] = affine_rank(paired)
    require(ranks == {"S": 6, "R": 5}, "Paired affine ranks")
    source_to_target = {scale(2, ray["v"]): scale(2, ray["S"]) for ray in RAYS}
    for i, j in product(range(4), repeat=2):
        if i != j:
            target = tuple(a + b for a, b in zip(U[i], U[j]))
            require(source_to_target[sub(U[j], U[i])] == target, "Classical flap labels")

    smat, rmat = incidence("S"), incidence("R")
    difference = [sub(a, b) for a, b in zip(smat, rmat)]
    # Five equations (6), with sign order ++,+-,-+,-- in each plane.
    equations = []
    for terms in ({8: 1, 4: -1, 7: -1}, {11: 1, 5: -1, 6: -1},
                  {10: 1, 0: -1, 3: -1}, {9: 1, 1: -1, 2: -1},
                  {0: 1, 1: 1, 6: -1, 7: -1}):
        equations.append([terms.get(j, 0) for j in range(12)])
    require(rref(equations) == rref(difference), "Additive balance row-space equivalence")
    require(rank(equations) == 5, "Five independent balances")
    positive = (1,) * 8 + (2,) * 4
    require(matvec(equations, positive) == (0,) * 5, "Positive interior point")
    require(matvec(smat, positive) == (4, 4, 2, 2, 2, 2), "Simple output weights")
    require(matvec(rmat, positive) == matvec(smat, positive), "Simple measure matching")
    require(matvec(smat, (1,) * 12) != matvec(rmat, (1,) * 12), "Uniform-weight control")
    second_moment_defect = [[sum(ray["v"][i] * ray["v"][j]
                                - ray["S"][i] * ray["S"][j] for ray in RAYS)
                             for j in range(3)] for i in range(3)]
    require(second_moment_defect == [[4 * int(i == j) for j in range(3)]
                                    for i in range(3)], "Uniform-ray moment defect")

    varied = (1, 2, 3, 4, 5, 6, 1, 2, 7, 5, 5, 7)
    require(matvec(equations, varied) == (0,) * 5, "Varied positive radial weights")
    laws = {Q(2): list(positive), Q(3): list(varied)}
    core_weights = (2, 3, 5, 7)
    require(output_law(laws, core_weights, "S") == output_law(laws, core_weights, "R"),
            "Whole radial law matching with independent core masses")
    bad_laws = {r: weights.copy() for r, weights in laws.items()}
    bad_laws[Q(2)][0] -= 1
    bad_laws[Q(3)][0] += 1
    totals = [sum(weights[j] for weights in bad_laws.values()) for j in range(12)]
    require(matvec(equations, totals) == (0,) * 5, "Control must balance total masses")
    require(output_law(bad_laws, core_weights, "S")
            != output_law(bad_laws, core_weights, "R"), "Radial-mass-only control")

    unequal_radii = (1, 2, 3, 4, 5, 6, 1, 2, 5, 3, 4, 6)
    maximum = effective_radii(unequal_radii, "S", max)
    require(maximum == (6, 4, 5, 6, 4, 3), "Unequal-radius expected maximum vector")
    require(maximum == effective_radii(unequal_radii, "R", max), "Maximum balances")
    unequal_minima = (1, 2, 3, 4, 5, 6, 1, 2, 2, 2, 1, 1)
    require(effective_radii(unequal_minima, "S", min)
            == effective_radii(unequal_minima, "R", min), "Unequal-radius minimum balances")
    for op in (min, max):
        require(effective_radii((Q(7, 3),) * 12, "S", op)
                == effective_radii((Q(7, 3),) * 12, "R", op), "Common shell radius")
    bad_radii = list(unequal_radii)
    bad_radii[8] = 8
    require(effective_radii(bad_radii, "S", max) != effective_radii(bad_radii, "R", max),
            "Maximum-balance rejection control")
    for r in (Q(2), Q(5, 2), Q(3)):
        targets_s = {scale(r, ray["S"]) for ray in RAYS}
        targets_r = {scale(r, ray["R"]) for ray in RAYS}
        require(targets_s == targets_r == {scale(r, axis) for axis in AXES}, "Shell set equality")

    digest = sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    result = {
        "status": "all exact checks passed",
        "ray_polynomial_identities": len(records),
        "middle_coefficient_counts": distribution,
        "pair_coefficient_sha256": digest,
        "core_support_checks": 24,
        "paired_affine_ranks": ranks,
        "classical_flap_correspondences": 12,
        "independent_additive_balances": rank(equations),
        "positive_cone_dimension": 12 - rank(equations),
        "uniform_ray_unnormalized_second_moment_defect": second_moment_defect,
        "whole_radial_law_matching": True,
        "unequal_radius_maximum_vector": maximum,
        "rejection_controls": ["below_cutoff", "outside_tetrahedron",
                               "uniform_ray_weights", "total_masses_only", "bad_maximum_balance"],
        "trust_boundary": "Exact finite algebra only; universal analytic claims use PROOF.md and its cited planar theorems."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
