"""Exact helpers retained from the credited public9017 checker.

Author six-downset-2, researcher. See PROOF.md for bridge provenance.
"""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from math import comb
from model import parameters,choose,require
from exact import bareiss_rank,schur_rank

def rational_strings(values):
    require(all(type(v) is str for v in values), "Rational strings required")
    return [Q(v) for v in values]

def digest(matrix):
    raw = json.dumps([[str(v) for v in row] for row in matrix],
                     separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def closed_complete(n, meta, values):
    """Independent direct two-row completion, without using RREF."""
    r, N, s = parameters(n)
    beta = [[Q(0)]*(r+1) for _ in range(r+1)]
    require(len(values) == len(meta["free_pairs"]), "Closed free-value count")
    for (a, b), value in zip(meta["free_pairs"], values):
        require(a >= 3 and b >= 3, "Closed decoder free face")
        beta[a][b] = beta[b][a] = value
    for a in range(3, r+1):
        b = n-a
        total = sum(beta[a][k]*choose(b, k) for k in range(3, r+1))
        star = sum(beta[a][k]*choose(b-1, k-1) for k in range(3, r+1))
        v = Q(b*(s-star)-(N-1-s-total), comb(b, 2))
        u = s-star-(b-1)*v
        beta[2][a] = beta[a][2] = v
        beta[1][a] = beta[a][1] = u
    total = sum(beta[2][a]*choose(n-2, a) for a in range(3, r+1))
    star = sum(beta[2][a]*choose(n-3, a-1) for a in range(3, r+1))
    beta[2][2] = Q((n-2)*(s-star)-(N-1-s-total), comb(n-2, 2))
    beta[1][2] = beta[2][1] = s-star-(n-3)*beta[2][2]
    beta[1][1] = s-sum(beta[1][a]*choose(n-2, a-1) for a in range(2, r+1))
    for a in range(1, r+1):
        require(sum(beta[a][b]*choose(n-a, b) for b in range(1, r+1)) == N-1-s,
                "Closed center residual")
        require(sum(beta[a][b]*choose(n-a-1, b-1) for b in range(1, r+1)) == s,
                "Direct excluding-point star residual")
    return beta

def decoded(n, meta, recover, values):
    beta = recover(values)
    require(beta == closed_complete(n, meta, values), "Independent completion agreement")
    return beta

def projection_gram(g, aa, j):
    d = len(g)
    if j >= 2:
        return [[Q(g[i]*int(i == k)) for k in range(d)] for i in range(d)]
    if j == 1:
        return [[Q(g[i]*int(i == k))-Q(g[i]*g[k], sum(g))
                 for k in range(d)] for i in range(d)]
    M = [[sum(g[a]*aa[a]**(i+k) for a in range(d)) for k in range(2)] for i in range(2)]
    det = M[0][0]*M[1][1]-M[0][1]**2
    require(det > 0, "Positive constant/cardinality moment determinant")
    Mi = [[Q(M[1][1], det), Q(-M[0][1], det)],
          [Q(-M[0][1], det), Q(M[0][0], det)]]
    return [[Q(g[i]*int(i == k))-g[i]*g[k]*sum(
        aa[i]**a*Mi[a][b]*aa[k]**b for a in range(2) for b in range(2))
        for k in range(d)] for i in range(d)]

def determinant_small(A):
    d = len(A)
    total = 0
    for permutation in itertools.permutations(range(d)):
        sign = (-1)**sum(permutation[i] > permutation[k] for i in range(d) for k in range(i+1, d))
        value = sign
        for i in range(d):
            value *= A[i][permutation[i]]
        total += value
    return total

def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    return False

def arithmetic_audit():
    positive = 0
    for values in itertools.product((-1, 0, 1), repeat=6):
        A = [[0]*3 for _ in range(3)]
        for (i, k), v in zip(((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)), values):
            A[i][k] = A[k][i] = v
        criterion = all(determinant_small([[A[i][k] for k in subset] for i in subset]) >= 0
                        for size in (1, 2, 3) for subset in itertools.combinations(range(3), size))
        outcomes = [not rejected(lambda method=method: method(A))
                    for method in (bareiss_rank, schur_rank)]
        require(outcomes == [criterion, criterion], "Separate all-principal-minor PSD audits")
        positive += criterion
    require(positive == 24, "Ternary audit count")
    return {"all_symmetric_ternary_3x3": 729, "PSD": positive}
