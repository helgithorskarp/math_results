#!/usr/bin/env python3
"""Independent exact controls for the finite-atomic low-noise review.

Python 3.11+, standard library only.  This checker deliberately does not
import the target checker or its fixtures.  It uses a new tight-leg triangle,
a new collision partition, direct count-vector enumeration, and rational
LDL/Gauss-Jordan calculations for the collision moment Gram matrix.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE_HASHES = {
    "probability/gaussian_atomic_low_noise_exclusion/.gitignore":
        "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "probability/gaussian_atomic_low_noise_exclusion/EXPECTED.json":
        "1721033d80534033fa1473edb060d19ca68c7ee40cb6f24cf50aab6d81595947",
    "probability/gaussian_atomic_low_noise_exclusion/PROOF.md":
        "7e07698f9892bd949d8009fa7b52d8f7e941c2c44061f708297918433ba079dd",
    "probability/gaussian_atomic_low_noise_exclusion/README.md":
        "93cc7939a336444bb71124c7ade45c19301f10a24eecb9933b0e3197ea72d012",
    "probability/gaussian_atomic_low_noise_exclusion/SHA256SUMS":
        "49b17a8ba177e472efbcf67d1b141560a005496afcd17600c091d17b54139629",
    "probability/gaussian_atomic_low_noise_exclusion/SOURCES.md":
        "51ac220b658dcb913a97a33b3b125de19645785024441c19e0ed0684f510c9cc",
    "probability/gaussian_atomic_low_noise_exclusion/verify.py":
        "5f396ffe7ca7961aee1b3707a95088db83cc9d345f05ab225ce07c45d2da281b",
    "probability/gaussian_majorisation_hankel_transport/PROOF.md":
        "2f2f653710bd9214fca898c82b7d56119ec83ea1238c6860ceeb310d657e7fae",
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil_log2_integer(n):
    need(isinstance(n, int) and n >= 1, "bad integer logarithm input")
    return (n - 1).bit_length()


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def squared_distances(points):
    return [[sum((u - v) ** 2 for u, v in zip(a, b)) for b in points]
            for a in points]


def inverse(matrix):
    n = len(matrix)
    work = [list(row) + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        need(pivot is not None, "singular matrix")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row != col:
                scale = work[row][col]
                work[row] = [x - scale * y
                             for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def ldl_positive(matrix):
    """Definition-level exact LDL test, with no eigenvalue library."""
    n = len(matrix)
    lower = [[Q(0) for _ in range(n)] for _ in range(n)]
    diagonal = [Q(0) for _ in range(n)]
    for i in range(n):
        lower[i][i] = Q(1)
        diagonal[i] = matrix[i][i] - sum(
            lower[i][k] ** 2 * diagonal[k] for k in range(i))
        need(diagonal[i] > 0, "nonpositive LDL pivot")
        for j in range(i + 1, n):
            numerator = matrix[j][i] - sum(
                lower[j][k] * lower[i][k] * diagonal[k]
                for k in range(i))
            lower[j][i] = numerator / diagonal[i]
    return diagonal


def pin_sources():
    for relative, expected in SOURCE_HASHES.items():
        data = (REPO / relative).read_bytes()
        need(sha256(data).hexdigest() == expected, f"source drift: {relative}")
        need(sha256(data + b"review-mutation").hexdigest() != expected,
             f"mutation unexpectedly accepted: {relative}")
    return {"files": len(SOURCE_HASHES), "mutations_rejected": len(SOURCE_HASHES)}


def tight_leg_triangle():
    """Check the dangerous three-label branch on a new 5-12-13 fixture."""
    x = [(Q(-1), Q(0), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(0))]
    y = [(Q(-12, 13), Q(5, 13), Q(0)),
         (Q(12, 13), Q(5, 13), Q(0)), (Q(0), Q(0), Q(0))]
    dx, dy = squared_distances(x), squared_distances(y)
    pairs = list(combinations(range(3), 2))
    need(all(dx[i][j] >= dy[i][j] for i, j in pairs), "not a contraction")
    active = [(i, j) for i, j in pairs if dx[i][j] > dy[i][j]]
    need(active == [(0, 1)], "unexpected active set")
    need(dx[0][2] == dy[0][2] == dx[1][2] == dy[1][2] == 1,
         "legs are not tight")
    beta = min(dy[0][1], dx[0][1] - dy[0][1])
    need(beta == Q(100, 169), "wrong curvature floor")

    digest = sha256()
    count_vectors = 0
    for m in range(2, 21):
        candidates = []
        for counts in compositions(m, 3):
            if counts[0] * counts[1] == 0:
                continue
            scatter = sum(counts[i] * counts[j] * dy[i][j] for i, j in pairs)
            loss = sum(counts[i] * counts[j] * (dx[i][j] - dy[i][j])
                       for i, j in pairs)
            need(loss >= beta, "active loss fell below beta")
            candidates.append(scatter / (2 * m))
            count_vectors += 1
        minimum = min(candidates)
        expected = Q(1) - Q(50, 169 * m)
        need(minimum == expected, f"wrong active minimum at m={m}")
        digest.update(f"{m}:{minimum}\n".encode())

    curvature_pairs = 0
    for i in range(25):
        for j in range(i + 1, 25):
            r, t, m = 2 * i + 2, 2 * j + 2, i + j + 2
            exponent = lambda n: Q(1) - Q(50, 169 * n)
            gap = exponent(m) - (exponent(r) + exponent(t)) / 2
            gamma = Q((i - j) ** 2,
                      8 * (i + 1) * (j + 1) * (i + j + 2))
            need(gap == beta * gamma, "curvature identity failed")
            curvature_pairs += 1
    return {
        "fixture": "new rational 5-12-13 tight-leg contraction",
        "beta": str(beta),
        "orders": 19,
        "active_count_vectors": count_vectors,
        "curvature_pairs": curvature_pairs,
        "minimum_digest": digest.hexdigest(),
    }


def collision_partition():
    """Directly reconstruct zero-scatter masses for a new collision pattern."""
    x = [(Q(0),), (Q(10),), (Q(20),), (Q(30),)]
    y = [(Q(0),), (Q(0),), (Q(1),), (Q(1),)]
    weights = [Q(1, 2), Q(1, 4), Q(1, 8), Q(1, 8)]
    groups = [(0, 1), (2, 3)]
    group_weights = [sum(weights[i] for i in group) for group in groups]
    dx, dy = squared_distances(x), squared_distances(y)
    pairs = list(combinations(range(4), 2))
    need(all(dx[i][j] >= dy[i][j] for i, j in pairs), "collision fixture fails")
    delta = min(value for matrix in (dx, dy) for row in matrix
                for value in row if value > 0)
    need(delta == 1, "wrong collision separation")

    checked = 0
    digest = sha256()
    for m in range(2, 11):
        zero_x = Q(0)
        zero_y = Q(0)
        for counts in compositions(m, 4):
            # Multinomial probability, computed without the target implementation.
            multiplicity = 1
            remaining = m
            for count in counts[:-1]:
                numerator = 1
                denominator = 1
                for k in range(count):
                    numerator *= remaining - k
                    denominator *= k + 1
                multiplicity *= numerator // denominator
                remaining -= count
            probability = Q(multiplicity)
            for weight, count in zip(weights, counts):
                probability *= weight ** count
            sx = sum(counts[i] * counts[j] * dx[i][j] for i, j in pairs)
            sy = sum(counts[i] * counts[j] * dy[i][j] for i, j in pairs)
            if sx == 0:
                zero_x += probability
            else:
                need(sx >= (m - 1) * delta, "source residual floor failed")
            if sy == 0:
                zero_y += probability
            else:
                need(sy >= (m - 1) * delta, "target residual floor failed")
            checked += 1
        need(zero_x == sum(w ** m for w in weights), "source grouping failed")
        need(zero_y == sum(w ** m for w in group_weights), "target grouping failed")
        need(zero_y > zero_x, "merger limit is not positive")
        digest.update(f"{m}:{zero_x}:{zero_y}\n".encode())

    p = Q(1, 8)
    hinge_checks = 0
    for q in (Q(1, 2), Q(2, 3), Q(1)):
        for t in (p / 4, Q(3, 8) * p, p / 2):
            merged = sum(max(W * q - t, 0) for W in group_weights)
            separate = sum(max(w * q - t, 0) for w in weights)
            need(merged - separate >= t, "merger hinge bound failed")
            hinge_checks += 1
    return {
        "fixture": "new four-atom two-collision partition",
        "delta": str(delta),
        "count_vectors": checked,
        "hinge_checks": hinge_checks,
        "zero_scatter_digest": digest.hexdigest(),
    }


def gram_and_budget_controls():
    """Check collision Gram margins by rational linear algebra, not Legendre code."""
    gram_cases = 0
    inverse_entries = 0
    digest = sha256()
    for b in (1, 3, 6):
        p = Q(1, 2 ** b)
        left, right = p / 4, p / 2
        for D in range(1, 9):
            gram = [[(right ** (i + j + 1) - left ** (i + j + 1)) /
                     (i + j + 1) for j in range(D + 1)] for i in range(D + 1)]
            pivots = ldl_positive(gram)
            inv = inverse(gram)
            for i in range(D + 1):
                for j in range(D + 1):
                    product = sum(gram[i][k] * inv[k][j] for k in range(D + 1))
                    need(product == Q(i == j), "Gram inverse failed")
                    inverse_entries += 1
            trace = sum(inv[i][i] for i in range(D + 1))
            upper = Q(4, p) * (D + 1) * (2 * D + 1) * Q(20, p) ** (2 * D)
            need(trace <= upper, "inverse-trace margin failed")
            digest.update(f"{b},{D}:{trace}:{min(pivots)}\n".encode())
            gram_cases += 1

    budget_cases = 0
    for D in range(1, 257):
        for b in range(1, 17):
            M = 2 * D + 2
            K = 8 * D * (D + 1) * (2 * D + 1)
            L = M * b + ceil_log2_integer(2 * D)
            need(K * L >= 2 * M, "distinct lower budget failed")
            need(K * L <= 288 * b * D ** 4, "degree-rate budget failed")
            need(Q(2) ** (b * M - L) <= Q(1, 2 * D),
                 "diagonal-dominance budget failed")

            log_factor = ceil_log2_integer((D + 1) ** 2 * (2 * D + 1))
            Lc = 9 + 10 * D + (2 * D + 2) * b + log_factor
            need(Lc <= 27 * b * D, "collision exponent budget failed")
            p = Q(1, 2 ** b)
            reciprocal_margin = (512 * (D + 1) ** 2 * (2 * D + 1) *
                                 Q(20, p) ** (2 * D) / p ** 2)
            need(Q(2) ** Lc >= reciprocal_margin,
                 "collision perturbation budget failed")
            budget_cases += 1
    return {
        "gram_cases": gram_cases,
        "inverse_entries": inverse_entries,
        "budget_cases": budget_cases,
        "gram_digest": digest.hexdigest(),
    }


def main():
    result = {
        "status": "INDEPENDENT_ATOMIC_LOW_NOISE_REVIEW_PASS",
        "source_commit": "02b579d7e9c77053d7399096fe9314b9fdfca6f1",
        "pins": pin_sources(),
        "distinct_target": tight_leg_triangle(),
        "target_collision": collision_partition(),
        "matrix_controls": gram_and_budget_controls(),
        "trust_boundary": (
            "Exact controls corroborate the universal written proof; they do not "
            "enumerate all contractions or formalize the analytic argument."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
