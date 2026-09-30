"""Exact validation of the uniform STS construction and incidence bridge.

The proof of the infinite claim is CAPPED_PROOF.md; fixtures are not a census.
Python 3.11+, standard library only. No floating-point arithmetic is used.
"""
from fractions import Fraction as F
from itertools import combinations
import json

from certificates import (affine_sts9, capped_steiner_certificate,
                          cyclic_sts13, fano_blocks, mask, steiner_certificate)
from verify import check_definition, exact_psd_rank, matrix_hash, rejects


def incidence_bridge(v, blocks, D, s, Q):
    pairs = [mask(p) for p in combinations(range(v), 2)]
    points = [1 << i for i in range(v)]
    P = [[int(bool(a & p)) for p in points] for a in pairs]
    B = [[int(bool(a & p)) for p in points] for a in blocks]
    R = [[int(a & b == a) for b in blocks] for a in pairs]
    completing = []
    for a in pairs:
        containing = [b for b in blocks if a & b == a]
        assert len(containing) == 1
        completing.append(containing[0] ^ a)
    T = [[int(c == p) for p in points] for c in completing]
    r = (v - 1) // 2
    for i in range(v):
        for j in range(v):
            assert sum(row[i] * row[j] for row in P) == (v - 2) * (i == j) + 1
            assert sum(row[i] * row[j] for row in B) == (r - 1) * (i == j) + 1
            assert sum(T[k][i] * P[k][j] for k in range(len(pairs))) == (i != j)
        for j in range(len(blocks)):
            assert sum(P[k][i] * R[k][j] for k in range(len(pairs))) == 2 * B[j][i]
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            assert sum(row[i] * row[j] for row in R) == 3 * (i == j)
    for i in range(len(pairs)):
        for j in range(v):
            assert sum(R[i][k] * B[k][j] for k in range(len(blocks))) - P[i][j] == T[i][j]

    w = 1 + F(v + 3, (v - 3) * (v - 2))
    h = F(v + 3, v - 3)
    ppos = {a: i for i, a in enumerate(pairs)}
    bpos = {a: i for i, a in enumerate(blocks)}
    for i, a in enumerate(D[1:], 1):
        assert sum(Q[i][j] - 1 for j in range(1, len(D))) == 0
        for j, b in enumerate(D[1:], 1):
            aa, bb = a, b
            if aa.bit_count() > bb.bit_count():
                aa, bb = bb, aa
            sizes = (aa.bit_count(), bb.bit_count())
            common = (aa & bb).bit_count()
            if sizes == (1, 1):
                expected = s * (aa == bb) - 1
            elif sizes == (1, 2):
                expected = w - 1 - w * bool(aa & bb) - h * (aa == completing[ppos[bb]])
            elif sizes == (1, 3):
                expected = h - 1 - h * bool(aa & bb)
            elif sizes == (2, 2):
                expected = (s + w) * (aa == bb) - w * common + w - 1
            elif sizes == (2, 3):
                expected = h - 1 - h * common + h * R[ppos[aa]][bpos[bb]]
            elif sizes == (3, 3):
                expected = (s + 2) * (aa == bb) - common
            else:
                raise AssertionError("unexpected level")
            assert Q[i][j] - 1 == expected


def scalar_parameters(v):
    s = F(3 * v - 1, 2)
    n = F(2 * v * v + v + 3, 3)
    h = F(v + 3, v - 3)
    w = 1 + F(v + 3, (v - 3) * (v - 2))
    alpha = s - w * (v - 3)
    delta = s + w
    first = F((v + 3) ** 2 * (v - 4) ** 2, (v - 3) * (v * v + v - 16))
    assert first == v - F(4 * (v * v + 6 * v - 36), (v - 3) * (v * v + v - 16))
    second = h * h * v / ((v - 2) * delta)
    schur = v + 3 - first - second
    center_trace = s + alpha + delta + v + 3
    residual_determinant = delta * (s + 2) - 3 * h * h
    assert alpha > 0 and delta > 0 and schur > F(17, 8)
    assert first < v and second <= F(7, 8)
    assert center_trace < n and residual_determinant > 0
    assert 2 * s + w + 2 < n and F(v + 13, 2) < n and delta < n
    assert (27 * n == 8 * s * s + 14 * s + 32)
    assert int(n) % int(s) not in (0, 1)
    return {"center_schur": str(schur), "center_trace": str(center_trace),
            "triple_kernel_determinant": str(residual_determinant),
            "alpha": str(alpha), "delta": str(delta)}


def run():
    result = {"arithmetic": "fractions.Fraction", "capped_examples": []}
    D, s, Q = capped_steiner_certificate(3, [7])
    assert check_definition(D, s, Q) == 4
    assert exact_psd_rank([[F(len(D) if i == j else 0) - Q[i][j]
                           for j in range(len(D))] for i in range(len(D))]) == 4
    result["order_three_cube_ranks"] = [4, 4]
    for v, blocks in [(7, fano_blocks()), (9, affine_sts9()), (13, cyclic_sts13())]:
        D, s, Q = capped_steiner_certificate(v, blocks)
        n = len(D)
        incidence_bridge(v, blocks, D, s, Q)
        rank = check_definition(D, s, Q)
        assert rank == 4 * len(blocks)
        upper_rank = exact_psd_rank([[F(n if i == j else 0) - Q[i][j]
                                     for j in range(n)] for i in range(n)])
        assert upper_rank == n - 1
        result["capped_examples"].append({"v": v, "N": n, "s": s,
            "rank_Q": rank, "rank_upper": upper_rank,
            "matrix_sha256": matrix_hash(Q), **scalar_parameters(v)})
    # The old lower-bound construction is a real certificate, but does not cap.
    D, s, old = steiner_certificate(9, [affine_sts9()])
    assert old[0][0] == 379 and old[0][0] > len(D)
    result["layered_order_nine_empty_diagonal"] = str(old[0][0])
    # Perturb the special singleton/pair value while preserving support.
    D, s, bad = capped_steiner_certificate(7, fano_blocks())
    i = D.index(1); j = D.index(6)
    bad[i][j] += 1; bad[j][i] += 1
    rejects(lambda: check_definition(D, s, bad))
    rejects(lambda: capped_steiner_certificate(9, affine_sts9()[:-1]))
    result["new_rejection_controls"] = 2
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
