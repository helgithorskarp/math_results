"""Definition-level exact checks; no numerical eigensolver or SDP dependency."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json

from certificates import (affine_sts9, check_sts, complement_cube,
                          cyclic_sts13, fano_blocks, fano_certificate,
                          mask, normalized, steiner_certificate)


def exact_psd_rank(Q):
    """Symmetric Schur elimination over Q with exact zero-row handling.

    Each positive pivot is a congruence step. If all diagonal entries vanish,
    positivity holds precisely when the remaining matrix is identically zero.
    """
    A = [list(row) for row in Q]
    rank = 0
    while A:
        p = max(range(len(A)), key=lambda i: A[i][i])
        d = A[p][p]
        if d < 0:
            raise ValueError("negative diagonal in residual")
        if d == 0:
            if any(x != 0 for row in A for x in row):
                raise ValueError("nonzero residual with zero diagonal")
            return rank
        keep = [i for i in range(len(A)) if i != p]
        A = [[A[i][j] - A[i][p] * A[p][j] / d for j in keep] for i in keep]
        rank += 1
    return rank


def check_definition(D, s, Q, psd=True):
    n = len(D)
    assert len(set(D)) == n and D[0] == 0
    v = max(D).bit_length()
    for a in D:
        b = a
        while True:
            assert b in D, "not a downset"
            if b == 0:
                break
            b = (b - 1) & a
    star_sizes = [sum(bool(a & (1 << i)) for a in D) for i in range(v)]
    assert s == max(star_sizes) and 0 < s < n
    assert len(Q) == n and all(len(row) == n for row in Q)
    for i, a in enumerate(D):
        assert sum(Q[i]) == n, "wrong row sum"
        for j, b in enumerate(D):
            assert Q[i][j] == Q[j][i], "asymmetric"
            if a & b:
                assert Q[i][j] == (s if i == j else 0), "support/diagonal failure"
    M = normalized(D, s, Q)
    for i, a in enumerate(D):
        assert sum(M[i]) == 1
        for j, b in enumerate(D):
            assert not a & b or M[i][j] == 0
            assert Q[i][j] == (n - s) * M[i][j] + (s if i == j else 0)
    for b, star_size in enumerate(star_sizes):
        if star_size == s:
            for i in range(n):
                assert sum(Q[i][j] for j, a in enumerate(D) if a & (1 << b)) == s
    return exact_psd_rank(Q) if psd else None


def matrix_hash(Q):
    data = json.dumps([[str(x) for x in row] for row in Q], separators=(",", ":"))
    return sha256(data.encode()).hexdigest()


def all_sts7():
    """Exhaustive exact-cover branching on the first uncovered pair.

    The unique block containing that pair must occur in one branch. Selected
    blocks never overlap in a pair; when no pair remains, every pair is covered.
    No symmetry constraints or heuristic pruning are imposed.
    """
    pairs = [mask(p) for p in combinations(range(7), 2)]
    triples = [mask(t) for t in combinations(range(7), 3)]
    triple_pairs = {t: frozenset(p for p in pairs if p & t == p) for t in triples}
    choices = {p: [t for t in triples if p in triple_pairs[t]] for p in pairs}
    solutions = set()

    def recurse(uncovered, chosen):
        if not uncovered:
            solutions.add(tuple(sorted(chosen)))
            return
        p = min(uncovered)
        for t in choices[p]:
            if triple_pairs[t] <= uncovered:
                recurse(uncovered - triple_pairs[t], chosen + (t,))

    recurse(frozenset(pairs), ())
    return solutions


def relabel(a, perm):
    return sum(1 << perm[i] for i in range(len(perm)) if a & (1 << i))


def fano_coverage(D, s, Q):
    blocks = fano_blocks()
    orbit = {}
    for p in permutations(range(7)):
        key = tuple(sorted(relabel(t, p) for t in blocks))
        orbit.setdefault(key, p)
    enumerated = all_sts7()
    assert set(orbit) == enumerated and len(enumerated) == 30
    # PSD transfers by permutation congruence. Check all definition conditions.
    for blocks, p in sorted(orbit.items()):
        check_sts(7, blocks)
        mapped = sorted(range(len(D)), key=lambda i: (D[i].bit_count(), relabel(D[i], p)))
        Dp = [relabel(D[i], p) for i in mapped]
        Qp = [[Q[i][j] for j in mapped] for i in mapped]
        check_definition(Dp, s, Qp, psd=False)
    digest = sha256(json.dumps(sorted(enumerated), separators=(",", ":")).encode()).hexdigest()
    return {"labelled_systems": len(enumerated), "isomorphism_classes": 1,
            "enumeration_sha256": digest}


def second_disjoint_sts9(first):
    # Deterministic search for a compact two-system example, not a nonexistence test.
    first_set = set(first)
    for p in permutations(range(9)):
        second = sorted(relabel(t, p) for t in first)
        if first_set.isdisjoint(second):
            return second, p
    raise RuntimeError("fixture construction failed")


def rejects(call):
    try:
        call()
    except (ValueError, AssertionError):
        return
    raise AssertionError("bad certificate was accepted")


def run():
    result = {"arithmetic": "fractions.Fraction", "baseline_cube_ranks": {}}
    for v in range(1, 6):
        D, s, Q = complement_cube(v)
        rank = check_definition(D, s, Q)
        assert rank == s
        result["baseline_cube_ranks"][str(v)] = rank
    D, s, Q = fano_certificate()
    rank = check_definition(D, s, Q)
    assert (len(D), s, rank) == (36, 10, 28)
    upper = [[F(len(D) if i == j else 0) - Q[i][j]
              for j in range(len(D))] for i in range(len(D))]
    upper_rank = exact_psd_rank(upper)
    assert upper_rank == 35
    result["fano"] = {"N": len(D), "s": s, "rank": rank, "matrix_sha256": matrix_hash(Q),
                      "upper_slack_rank": upper_rank, **fano_coverage(D, s, Q)}
    D0, s0, Q0 = fano_certificate(balanced=False)
    assert check_definition(D0, s0, Q0) == 29
    result["fano_initial"] = {"rank": 29, "matrix_sha256": matrix_hash(Q0)}
    first = affine_sts9()
    second, perm = second_disjoint_sts9(first)
    result["union9_relabel_permutation"] = list(perm)
    cases = [(9, [first]), (13, [cyclic_sts13()]), (9, [first, second])]
    result["layered_examples"] = []
    for v, systems in cases:
        D, s, Q = steiner_certificate(v, systems)
        rank = check_definition(D, s, Q)
        expected_rank = v * (v - 1) // 2 - v + 2 + len(systems) * (v * (v - 1) // 6 - v + 1)
        assert rank == expected_rank
        result["layered_examples"].append({"v": v, "systems": len(systems), "N": len(D), "s": s,
                                          "rank": rank, "matrix_sha256": matrix_hash(Q)})
    rejects(lambda: exact_psd_rank([[F(0), F(1)], [F(1), F(0)]]))
    rejects(lambda: exact_psd_rank([[F(-1)]]))
    rejects(lambda: check_sts(7, fano_blocks()[:-1]))
    rejects(lambda: steiner_certificate(9, [first, first]))
    rejects(lambda: steiner_certificate(7, [fano_blocks()]))
    D, s, Q = fano_certificate()
    Q[0][1] += 1
    rejects(lambda: check_definition(D, s, Q))
    result["rejection_controls"] = 6
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
