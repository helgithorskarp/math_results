"""Exact complete-sector certificates and an original-index order247 audit.

Python3.11+ stdlib; two distinct PSD algorithms; no solver or assertions.
The unbounded n>=12 bridge is the cited ordinary LEMMA8843, not a finite
extrapolation. The harmonic exhaustion and lift remain ordinary proofs.
"""
import argparse
from dataclasses import replace
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys

from exact import psd_rank
from matrices import (choose, counts, inverse2, literal_matrix, parameters,
                      require, sectors, slack_entry, trade, validate_weights)


def schur_rank(A):
    """Independent rational Schur complements, with no denominator clearing."""
    d = len(A)
    require(all(len(row) == d for row in A), "Schur shape")
    require(all(type(v) in (int, Q) for row in A for v in row), "Schur exact input")
    require(all(A[i][k] == A[k][i] for i in range(d) for k in range(d)), "Schur symmetry")
    Z = [[Q(v) for v in row] for row in A]
    rank = 0
    while Z:
        require(all(Z[i][i] >= 0 for i in range(len(Z))), "Negative Schur pivot")
        p = next((i for i in range(len(Z)) if Z[i][i]), None)
        if p is None:
            require(all(v == 0 for row in Z for v in row), "Zero diagonal obstruction")
            break
        others = [i for i in range(len(Z)) if i != p]
        Z = [[Z[i][k]-Z[i][p]*Z[p][k]/Z[p][p] for k in others] for i in others]
        rank += 1
    return rank


def both(A, expected=None):
    a, b = psd_rank(A), schur_rank(A)
    require(a == b and (expected is None or a == expected), "Two exact PSD/rank checks agree")
    return a


def gram(g, K, shift=Q(0)):
    return [[g[i]*(v-shift*int(i == k)) for k, v in enumerate(row)]
            for i, row in enumerate(K)]


def multiply(A, B):
    return [[sum((v*w for v, w in zip(row, col)), Q(0)) for col in zip(*B)] for row in A]


def projected_gram(g, aa, j):
    """G times the metric-orthogonal projection off the forced seed kernel."""
    d = len(g)
    if j >= 2:
        return [[Q(g[i]*int(i == k)) for k in range(d)] for i in range(d)]
    if j == 1:
        return [[Q(g[i]*int(i == k))-Q(g[i]*g[k], sum(g))
                 for k in range(d)] for i in range(d)]
    M = [[sum(g[a]*aa[a]**(i+k) for a in range(d)) for k in range(2)] for i in range(2)]
    Mi = inverse2(M)
    return [[Q(g[i]*int(i == k))-g[i]*g[k]*sum(
        Q(aa[i]**u)*Mi[u][v]*aa[k]**v for u in range(2) for v in range(2))
        for k in range(d)] for i in range(d)]


def sector_checks(n):
    P = parameters(n, Q(0))
    records, lower, upper, dimension = [], 0, 0, 0
    for j, aa, g, K, U in sectors(P):
        d = len(aa)
        require(all(v > 0 for v in g), "Positive harmonic metric")
        require(aa == list(range(max(1, j), min(6, n-j)+1)), "Actual truncated layer range")
        mult = comb(n, j)-choose(n, j-1)
        dimension += d*mult
        lr = both(gram(g, K), d-(2 if j == 0 else 1 if j == 1 else 0))
        ur = both(gram(g, U), d)
        lower += lr*mult
        upper += ur*mult
        vectors = ([1]*d, aa) if j == 0 else ([1]*d,) if j == 1 else ()
        require(all(all(sum(K[i][k]*x[k] for k in range(d)) == 0 for i in range(d))
                    for x in vectors), "Forced seed block kernels")
        proj = projected_gram(g, aa, j)
        if n <= 11:
            both([[g[i]*K[i][k]-proj[i][k] for k in range(d)] for i in range(d)])
            both(gram(g, U, Q(1, 4)))
        else:
            both(gram(g, [[2*P.s*int(i == k)-K[i][k] for k in range(d)] for i in range(d)]))
            both(gram(g, U, Q(1)))
            if j in (0, 1):
                both([[g[i]*K[i][k]-P.s*proj[i][k] for k in range(d)] for i in range(d)])
        D = [[Q((-1)**j*trade(n, a, b)*choose(n-a-j, b-j)) for b in aa] for a in aa]
        ev = P.alpha if j == 0 else -P.negative_trade if j == 1 else Q(1) if j == 2 else Q(0)
        require(multiply(D, D) == [[ev*v for v in row] for row in D], "Trade minimal polynomial")
        if j <= 2:
            both(gram(g, D if j != 1 else [[-v for v in row] for row in D]), 1)
        else:
            require(all(v == 0 for row in D for v in row), "Trade absent in degree>=3")
        both(gram(g, [[P.alpha*int(i == k)-D[i][k] for k in range(d)] for i in range(d)]))
        if j == 0:
            require(all(sum(D[i][k]*aa[k] for k in range(d)) == 0 for i in range(d)),
                    "Degree-zero trade kills cardinality")
            require(any(sum(row) for row in D), "Trade removes centered constant kernel")
        if j == 1:
            require(all(sum(row) == 0 for row in D), "Trade preserves degree-one kernel")
        records.append({"j": j, "layers": aa, "metric": g, "multiplicity": mult,
                        "seed_lower_rank": lr, "seed_upper_rank": ur})
    require(dimension == upper == P.N-1 and lower == P.N-n-2, "Complete weighted seed ranks")
    require(P.negative_trade/P.alpha < 1, "Degree-one repair bound")
    require(P.N-2*P.s == comb(n-1, 6) > 0, "Strict factor density")
    repaired = []
    for t in (1/(16*P.alpha), 1/(8*P.alpha)):
        R = parameters(n, t)
        lr, ur = 0, 0
        for j, aa, g, K, U in sectors(R):
            d = len(aa)
            expected = d-(1 if j in (0, 1) else 0)
            both(gram(g, K), expected)
            both(gram(g, U), d)
            both(gram(g, U, R.gap))
            mult = comb(n, j)-choose(n, j-1)
            lr += mult*expected
            ur += mult*d
        require((lr, ur) == (P.N-1-n, P.N-1), "Complete repaired ranks")
        repaired.append({"t": str(t), "core_lower_rank": lr, "core_upper_rank": ur,
                         "whole_lower_rank": lr+1, "whole_upper_rank": ur, "upper_floor": "1/8"})
    return {"n": n, "N": P.N, "s": P.s, "branch": P.branch,
            "alpha": str(P.alpha), "seed_core_lower_rank": lower,
            "seed_core_upper_rank": upper, "sectors": records, "repairs": repaired}


def validate_literal(P, V, L):
    N = len(V)
    require(N == P.N and V[0] == 0 and len(set(V)) == N, "Original vertex enumeration")
    require(all(len(row) == N for row in L), "Original matrix shape")
    require(all(type(v) is Q for row in L for v in row), "Original exact entries")
    require(all(L[i][k] == L[k][i] for i in range(N) for k in range(N)), "Original symmetry")
    require(all(sum(row) == N for row in L), "Empty-inclusive full row normalization")
    for i, A in enumerate(V):
        for k, B in enumerate(V):
            require(not (A & B) or L[i][k] == P.s*int(i == k), "Original intersecting support")
    require(L[0][0] == 1+P.t*P.delta, "Actual empty loop")
    for p in range(P.n):
        star = [Q(int(bool(A & (1 << p))))-Q(P.s, N) for A in V]
        require(all(sum(L[i][k]*star[k] for k in range(N)) == 0 for i in range(N)),
                "Every original centered star in kernel")


def literal_checks():
    P = parameters(8)
    V, L = literal_matrix(P)
    validate_literal(P, V, L)
    print("Exact order247: both algorithms on original lower form", file=sys.stderr, flush=True)
    both(L, P.N-P.n)
    upper = [[P.N*int(i == k)-L[i][k] for k in range(P.N)] for i in range(P.N)]
    margin = [[upper[i][k]-P.gap*(int(i == k)-Q(1, P.N)) for k in range(P.N)]
              for i in range(P.N)]
    print("Exact order247: both algorithms on original upper gap form", file=sys.stderr, flush=True)
    both(margin, P.N-1)
    require(all(sum(row) == 0 for row in upper), "Original upper constant kernel")
    F = V[1:]
    C = [[L[i+1][k+1]-1 for k in range(len(F))] for i in range(len(F))]
    actions, absent = 0, 0
    for j, aa, g, K, U in sectors(P):
        pol = []
        for A in F:
            v = 1
            for p in range(j):
                v *= int(bool(A & (1 << (2*p))))-int(bool(A & (1 << (2*p+1))))
            pol.append(v)
        for a in range(1, 7):
            if a not in aa:
                require(all(v == 0 for A, v in zip(F, pol) if A.bit_count() == a),
                        "Matching harmonic vanishes on absent layers")
                absent += 1
        for col, b in enumerate(aa):
            support = [(k, v) for k, (A, v) in enumerate(zip(F, pol)) if A.bit_count() == b and v]
            require(sum(v*v for k, v in support) == 2**j*comb(P.n-2*j, b-j), "Original harmonic norm")
            actual = [sum((C[i][k]*v for k, v in support), Q(0)) for i in range(len(F))]
            expected = [Q(v)*K[aa.index(A.bit_count())][col] if A.bit_count() in aa else Q(0)
                        for A, v in zip(F, pol)]
            require(actual == expected, "Every original coordinate of harmonic action")
            actions += 1
    payload = json.dumps([[str(v) for v in row] for row in L], separators=(",", ":")).encode()
    return {"n": P.n, "N": P.N, "s": P.s, "endpoint": str(P.t),
            "full_lower_rank": P.N-P.n, "full_upper_rank": P.N-1,
            "upper_gap_form_rank": P.N-1, "upper_nonzero_floor": "1/8",
            "full_forms_checked_by_both_algorithms": 2,
            "matching_action_columns": actions, "matching_absent_layer_checks": absent,
            "full_lower_matrix_sha256": sha256(payload).hexdigest()}


def rejection_controls():
    names = []
    def reject(name, f):
        try:
            f()
        except (ValueError, TypeError, ZeroDivisionError):
            names.append(name)
            return
        raise ValueError("Corruption accepted: "+name)
    for n in (7, 6, 8.0, True):
        reject("n="+str(n), lambda n=n: parameters(n))
    P = parameters(8, Q(0))
    for t in (-1, Q(1, 8*P.alpha)+Q(1, 1000000), 0.0, True):
        reject("t="+str(t), lambda t=t: parameters(8, t))
    reject("original matrix order guard", lambda: literal_matrix(parameters(9)))
    reject("vertex too large", lambda: slack_entry(P, 1 << 8, 0))
    reject("vertex too many points", lambda: slack_entry(P, 127, 0))
    for alg in (psd_rank, schur_rank):
        for label, A in (("negative", [[-1]]), ("off diagonal zero pivot", [[0, 1], [1, 0]]),
                         ("asymmetric", [[1, 2], [0, 1]]), ("ragged", [[1, 0], [0]]),
                         ("float", [[1.0]]), ("boolean", [[True]])):
            reject(alg.__name__+":"+label, lambda A=A, alg=alg: alg(A))
    for label, a, b in (("row identity", 1, 1), ("unsupported layer", 6, 6),
                        ("zero-index layer", 0, 1), ("asymmetry", 1, 2)):
        beta = [list(row) for row in P.beta]
        beta[a][b] += 1
        if label != "asymmetry":
            beta[b][a] = beta[a][b]
        R = replace(P, beta=tuple(tuple(row) for row in beta))
        reject("weights:"+label, lambda R=R: validate_weights(R))
    beta = [list(row) for row in P.beta]
    beta[1][1] = float(beta[1][1])
    R = replace(P, beta=tuple(tuple(row) for row in beta))
    reject("weights:float", lambda: validate_weights(R))
    j, aa, g, K, U = sectors(parameters(8))[0]
    reject("nonsymmetric unweighted degree-zero block", lambda: both(K))
    require([len(aa) for j, aa, g, K, U in sectors(P)] == [6, 6, 5, 3, 1],
            "Nonstable harmonic-range regression")
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--blocks-only", action="store_true", help="Development subset, not full expected record")
    args = parser.parse_args()
    cases = [sector_checks(n) for n in (8, 9, 10, 11, 12, 16, 32)]
    controls = rejection_controls()
    original = None if args.blocks_only else literal_checks()
    result = {"agent": "six-downset-2", "role": "researcher", "schema": 1,
              "arithmetic": ["integer Bareiss", "rational Schur complements"],
              "finite_coverage": "Four boundary seeds plus three stable corroboration orders",
              "infinite_scope": "Ordinary truncated-harmonic exhaustion and cited LEMMA8843, not enumeration",
              "boundary_orders": [8, 9, 10, 11], "stable_corroboration_orders": [12, 16, 32],
              "cases": cases, "literal": original, "rejections": controls}
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        Path(args.output).write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
