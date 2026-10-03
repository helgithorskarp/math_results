"""Exact near-full affine completion and complete harmonic blocks.

Author six-downset-2, researcher. Counts/lift/harmonics/trade retain the
credits in PROOF.md. Standard library only; no solver is a proof input.
"""
from fractions import Fraction as Q
from math import comb


def require(test, message):
    if not test:
        raise ValueError(message)


def choose(n, k):
    require(type(n) is int and n >= 0, "Nonnegative binomial upper index")
    return comb(n, k) if 0 <= k <= n else 0


def parameters(n):
    require(type(n) is int and n >= 6, "Constructor domain n>=6")
    return n-2, 2**n-n-1, 2**(n-1)-n


def affine(n):
    """Every invariant centered star-annihilating supported core, over Q."""
    r, N, s = parameters(n)
    pairs = [(a, b) for a in range(1, r+1) for b in range(a, r+1)
             if a+b <= n]
    rows = []
    for a in range(1, r+1):
        for moment in (0, 1):
            row = []
            for i, j in pairs:
                b = j if a == i else i if a == j else None
                row.append(Q(choose(n-a, b)*(b if moment else 1))
                           if b is not None else Q(0))
            row.append(Q((n-a)*s if moment else N-1-s))
            rows.append(row)
    position, pivots = 0, []
    for col in range(len(pairs)):
        hit = next((i for i in range(position, len(rows)) if rows[i][col]), None)
        if hit is None:
            continue
        rows[position], rows[hit] = rows[hit], rows[position]
        pivot = rows[position][col]
        rows[position] = [v/pivot for v in rows[position]]
        for i in range(len(rows)):
            if i != position and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [v-factor*w for v, w in zip(rows[i], rows[position])]
        pivots.append(col)
        position += 1
    require(not any(not any(row[:-1]) and row[-1] for row in rows),
            "Inconsistent affine equations")
    free = [i for i in range(len(pairs)) if i not in pivots]

    def recover(values):
        require(len(values) == len(free) and all(type(v) is Q for v in values),
                "Exact free coordinates")
        z = [Q(0)]*len(pairs)
        for i, v in zip(free, values):
            z[i] = v
        for k, col in enumerate(pivots):
            z[col] = rows[k][-1]-sum(rows[k][i]*z[i] for i in free)
        beta = [[Q(0)]*(r+1) for _ in range(r+1)]
        for (a, b), v in zip(pairs, z):
            beta[a][b] = beta[b][a] = v
        check_affine(n, beta)
        return beta

    meta = {"n": n, "r": r, "N": N, "s": s, "affine_rank": len(pivots),
            "pairs": pairs, "free_pairs": [pairs[i] for i in free]}
    return meta, recover


def check_affine(n, beta):
    r, N, s = parameters(n)
    require(len(beta) == r+1 and all(len(row) == r+1 for row in beta), "Table shape")
    require(all(type(v) is Q for row in beta for v in row), "Rational table")
    require(all(beta[a][b] == beta[b][a] for a in range(r+1) for b in range(r+1)),
            "Symmetric table")
    for a in range(1, r+1):
        require(sum(beta[a][b]*choose(n-a, b) for b in range(1, r+1)) == N-1-s,
                "Center equation")
        require(sum(b*beta[a][b]*choose(n-a, b) for b in range(1, r+1)) == (n-a)*s,
                "Star equation")


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def blocks(n, beta, t=Q(0)):
    r, N, s = parameters(n)
    require(type(t) is Q, "Exact parameter")
    out = []
    for j in range(n//2+1):
        aa = list(range(max(1, j), min(r, n-j)+1))
        g = [comb(n-2*j, a-j) for a in aa]
        K = [[Q(s*int(a == b)-(comb(n, b) if j == 0 else 0))
              +(-1)**j*(beta[a][b]+t*trade(n, a, b))*choose(n-a-j, b-j)
              for b in aa] for a in aa]
        U = [[Q(N*int(i == k)-(comb(n, b) if j == 0 else 0))-K[i][k]
              for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        out.append((j, aa, g, K, U))
    return out


def original(n, beta, t=Q(0)):
    """Small definition-level check only; never allocate the n=16 matrix."""
    r, N, s = parameters(n)
    require(N <= 247, "Literal matrix guard N<=247")
    F = [a for a in range(1, 1 << n) if a.bit_count() <= r]
    C = [[Q(s*int(i == k)-1)
          +(beta[a.bit_count()][b.bit_count()]+t*trade(n, a.bit_count(), b.bit_count()))
          *int(not (a & b)) for k, b in enumerate(F)] for i, a in enumerate(F)]
    sums = [sum(row) for row in C]
    L = [[Q(1)+sum(sums)]+[Q(1)-v for v in sums]]
    L += [[Q(1)-sums[i]]+[Q(1)+v for v in row] for i, row in enumerate(C)]
    require(len(L) == N, "Literal count")
    return F, C, L
