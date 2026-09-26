#!/usr/bin/env python3
"""Exact supplementary algebra; no Gaussian sign is inferred from samples."""

from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    require(len(a) == len(b), "dimension mismatch")
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, q):
    return tuple(q * x for x in a)


def sum_vectors(vectors):
    require(bool(vectors), "empty vector sum")
    return tuple(sum((v[j] for v in vectors), F(0))
                 for j in range(len(vectors[0])))


def orthogonal_basis(vectors):
    basis = []
    for vector in vectors:
        w = vector
        for b in basis:
            w = sub(w, scale(b, dot(w, b) / dot(b, b)))
        if dot(w, w):
            basis.append(w)
    return basis


def project(vector, basis):
    out = tuple(F(0) for _ in vector)
    for b in basis:
        term = scale(b, dot(vector, b) / dot(b, b))
        out = tuple(x + y for x, y in zip(out, term))
    return out


def pair_sum(vectors):
    return sum((dot(sub(a, b), sub(a, b))
                for a, b in combinations(vectors, 2)), F(0))


def projection_case(base, holes, dimension=5, damage=None):
    require(bool(base), "positive block is empty")
    center = scale(sum_vectors(base), F(1, len(base)))
    if damage == "center":
        center = tuple(x + (1 if j == 5 else 0)
                       for j, x in enumerate(center))
    centered = [sub(x, center) for x in base + holes]
    basis = orthogonal_basis(centered[len(base):])
    require(len(basis) <= dimension, "projection dimension exceeds premise")
    if damage == "projection":
        basis = []
    projected = [project(x, basis) for x in centered]
    residual = [sub(x, y) for x, y in zip(centered, projected)]
    require(all(dot(x, x) == 0 for x in residual[len(base):]),
            "a remaining point has a perpendicular component")
    require(all(x == 0 for x in sum_vectors(residual[:len(base)])),
            "positive-block perpendicular centroid did not cancel")
    energy = sum((dot(x, x) for x in residual[:len(base)]), F(0))
    if damage == "energy":
        energy += 1
    checks = 0
    for mask in range(1 << len(holes)):
        indices = list(range(len(base))) + [
            len(base) + j for j in range(len(holes)) if mask >> j & 1]
        original = [centered[i] for i in indices]
        reduced = [projected[i] for i in indices]
        m = len(indices)
        lhs = pair_sum(original) / m
        require(lhs == sum((dot(x, x) for x in original), F(0))
                - dot(sum_vectors(original), sum_vectors(original)) / m,
                "pair and centroid formulas disagree")
        require(lhs == pair_sum(reduced) / m + energy,
                "subset-independent energy identity failed")
        checks += 1
    affine = [sub(x, (base + holes)[0]) for x in base + holes]
    return {
        "base_size": len(base), "remaining_size": len(holes),
        "remaining_span_rank": len(basis),
        "whole_affine_rank": len(orthogonal_basis(affine)),
        "perpendicular_energy": str(energy), "subset_checks": checks,
    }


def projection_controls():
    axes = [tuple(F(i == j) for j in range(6)) for i in range(6)]
    base = [axes[5], scale(axes[5], -1)]
    records = {"full_rank_six": projection_case(base, axes[:5])}
    require(records["full_rank_six"]["whole_affine_rank"] == 6,
            "rank-six control collapsed")
    for h, r in [(2, 0), (3, 1), (4, 3), (7, 5), (11, 5)]:
        b = [tuple(F(((i + 2) * (j + 3)) % 13 - 6, i + 1)
                   for j in range(6)) for i in range(h)]
        l = [tuple(F(((i + 5) * (j + 1)) % 11 - 5, j + 1)
                   for j in range(6)) for i in range(r)]
        records[f"generic_{h}_{r}"] = projection_case(b, l)
    records["repeated_holes"] = projection_case(base, [axes[0]] * 5)
    records["zero_span"] = projection_case(base, [tuple(F(0) for _ in range(6))] * 5)

    # Actual R3 contraction: zero and the six signed axes, T=coordinatewise abs.
    x = [(F(0),) * 3]
    for j in range(3):
        x.extend(tuple(F(sign if q == j else 0) for q in range(3))
                 for sign in (1, -1))
    y = [tuple(abs(q) for q in v) for v in x]
    losses = [dot(sub(a, b), sub(a, b)) - dot(sub(c, d), sub(c, d))
              for (a, c), (b, d) in combinations(zip(x, y), 2)]
    require(all(v >= 0 for v in losses) and any(v > 0 for v in losses),
            "fold is not a nonisometric contraction")
    for p, q in [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(0), F(1))]:
        require(p * p + q * q == 1, "invalid rational lift")
        z = [scale(a, p) + scale(b, q) for a, b in zip(x, y)]
        b = [z[1], z[2]]
        l = [z[i] for i in (0, 3, 4, 5, 6)]
        records[f"fold_{p}_{q}"] = projection_case(b, l)
    require(records["fold_3/5_4/5"]["whole_affine_rank"] == 6,
            "genuine fold control lost paired rank")

    rejected = []
    for damage in ("center", "projection", "energy"):
        try:
            projection_case(base, axes[:5], damage=damage)
        except ValueError:
            rejected.append(damage)
        else:
            raise ValueError("corruption was accepted: " + damage)
    try:
        projection_case(base, axes)
    except ValueError:
        rejected.append("six_independent_remaining_vectors")
    else:
        raise ValueError("out-of-scope six-dimensional span was accepted")
    return records, rejected, {
        "points": len(x), "pair_checks": len(losses),
        "strict_pairs": sum(v > 0 for v in losses),
    }


def product_controls():
    checks = 0
    for r in range(6):
        for values in product((F(0), F(1, 3), F(1)), repeat=r):
            expanded = sum(((-1) ** len(subset)
                            * prod(values[j] for j in subset)
                            for size in range(r + 1)
                            for subset in combinations(range(r), size)), F(0))
            require(expanded == prod(1 - q for q in values),
                    "alternating product coefficient failed")
            checks += 1
    return checks


def weight(seq, weights):
    return prod(weights[j] for j in seq)


def toy_kernel(seq):
    # A rational symmetric kernel tests only multiplicities, not Gaussian signs.
    return F(1, len(seq) + 9 * sum(a != b for a, b in combinations(seq, 2)))


def loss(a, b):
    return 8 * (a != b)


def pair_expectation(m, weights):
    return sum((weight(seq, weights) * loss(seq[0], seq[1]) * toy_kernel(seq)
                for seq in product(range(2), repeat=m)), F(0))


def normalization_controls():
    exchangeability = 0
    for weights in [(F(1, 3), F(2, 3)), (F(0), F(1))]:
        for m in range(2, 8):
            direct = sum((weight(seq, weights) * toy_kernel(seq)
                          * sum(loss(a, b) for a, b in combinations(seq, 2))
                          for seq in product(range(2), repeat=m)), F(0))
            require(direct == comb(m, 2) * pair_expectation(m, weights),
                    "distinguished-pair exchangeability failed")
            require(F(comb(m, 2), 2 * m * m * (m - 1)) == F(1, 4 * m),
                    "replica derivative normalization failed")
            exchangeability += 1
    dummy_checks = 0
    weights = (F(1, 3), F(2, 3))
    for k, r in [(0, 0), (0, 5), (2, 3), (3, 5), (6, 1)]:
        b, m = k + 2, k + r + 2
        direct = sum(((-1) ** l * comb(r, l) * pair_expectation(b + l, weights)
                      for l in range(r + 1)), F(0))
        coupled = F(0)
        for seq in product(range(2), repeat=m):
            if not loss(seq[0], seq[1]):
                continue
            inner = F(0)
            for mask in range(1 << r):
                subtuple = seq[:b] + tuple(seq[b + j] for j in range(r) if mask >> j & 1)
                inner += (-1) ** mask.bit_count() * toy_kernel(subtuple)
            coupled += weight(seq, weights) * loss(seq[0], seq[1]) * inner
        require(coupled == direct, "unused-replica coupling lost a multiplicity")
        dummy_checks += 1
    coefficient_checks = 0
    for n in range(17):
        for k in range(n + 1):
            for q in range(k, n + 1):
                lhs = F((n + 1) * comb(n, k) * comb(n - k, q - k),
                        (q + 2) * (q + 1) * comb(n + 2, q + 2))
                require(lhs == F(comb(q, k), n + 2),
                        "polarized coefficient normalization failed")
                coefficient_checks += 1
    return {"exchangeability_checks": exchangeability,
            "unused_replica_checks": dummy_checks,
            "polarization_coefficient_checks": coefficient_checks}


def build_record():
    projections, rejected, fold = projection_controls()
    return {
        "status": "GAUSSIAN_BETA_PROJECTION_EXACT_AUDIT_PASS",
        "projection_cases": projections,
        "projection_subset_checks": sum(r["subset_checks"] for r in projections.values()),
        "genuine_contraction_control": fold,
        "finite_product_checks": product_controls(),
        "normalizations": normalization_controls(),
        "rejected_controls": rejected,
        "scope": "Exact finite algebra only; universal Gaussian sign is the written proof.",
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare every expected output field")
    args = parser.parse_args()
    record = build_record()
    encoded = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_bytes()
        require(encoded == expected, "expected record differs")
        print(record["status"], sha256(encoded).hexdigest())
    else:
        print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
