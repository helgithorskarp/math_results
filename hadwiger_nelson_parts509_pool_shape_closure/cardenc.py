#!/usr/bin/env python3
"""Sinz sequential-counter cardinality encodings (self-contained, deterministic).

`atmost(lits, k, nv)` returns (clauses, nv') such that the clauses are satisfiable
exactly when at most k of `lits` are true, and every assignment of `lits` with at most k
true extends to a satisfying assignment (so UNSAT of a CNF containing them certifies that
no assignment of the original variables obeys the cardinality bound and the rest).
"""
from __future__ import annotations


def atmost(lits, k, nv):
    n = len(lits)
    cl = []
    if k >= n:
        return cl, nv
    if k == 0:
        return [[-x] for x in lits], nv
    s = [[0] * (k + 1) for _ in range(n)]           # s[i][j], 1-based j
    for i in range(n - 1):
        for j in range(1, k + 1):
            nv += 1
            s[i][j] = nv
    cl.append([-lits[0], s[0][1]])
    for j in range(2, k + 1):
        cl.append([-s[0][j]])
    for i in range(1, n - 1):
        cl.append([-lits[i], s[i][1]])
        cl.append([-s[i - 1][1], s[i][1]])
        for j in range(2, k + 1):
            cl.append([-lits[i], -s[i - 1][j - 1], s[i][j]])
            cl.append([-s[i - 1][j], s[i][j]])
        cl.append([-lits[i], -s[i - 1][k]])
    cl.append([-lits[n - 1], -s[n - 2][k]])
    return cl, nv


def atleast(lits, k, nv):
    return atmost([-x for x in lits], len(lits) - k, nv)


def equals(lits, k, nv):
    c1, nv = atmost(lits, k, nv)
    c2, nv = atleast(lits, k, nv)
    return c1 + c2, nv


def atleast_direct(lits, k, nv):
    """Direct 'at least k' sequential encoding, O(n*k) clauses (cheap for small k).

    y[i][j] means 'at least j of lits[:i]'.  The clauses force y[n][k] -> at least k true,
    and every assignment with at least k true literals extends by y[i][j] = [prefix >= j].
    """
    n = len(lits)
    cl = []
    if k <= 0:
        return cl, nv
    if k > n:
        return [[]], nv                      # unsatisfiable
    y = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            nv += 1
            y[i][j] = nv
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            prev_j = y[i - 1][j] if j <= min(i - 1, k) else 0
            prev_j1 = y[i - 1][j - 1] if j - 1 >= 1 else None   # None means "true"
            c = [-y[i][j], lits[i - 1]]
            if prev_j:
                c.append(prev_j)
            cl.append(c)
            if prev_j1 is not None:
                c2 = [-y[i][j], prev_j1]
                if prev_j:
                    c2.append(prev_j)
                cl.append(c2)
            elif not prev_j:
                pass                          # j == 1 and i == 1: clause above suffices
    cl.append([y[n][k]])
    return cl, nv


def equals_cheap(lits, k, nv):
    c1, nv = atmost(lits, k, nv)
    c2, nv = atleast_direct(lits, k, nv)
    return c1 + c2, nv


def totalizer(lits, nv, kmax=None):
    """Totalizer (Bailleux-Boufkhad) unary counter.

    Returns (clauses, out, nv) where out[i] (1 <= i <= min(len(lits), kmax)) is a literal
    equivalent to 'at least i of lits are true'.  Both implication directions are encoded,
    so asserting out[k] forces at least k true literals and asserting -out[k] forces at
    most k-1; every assignment of `lits` extends uniquely to the auxiliary variables.
    Propagation is much stronger than the sequential-counter encoding, which matters when
    the instance has to be refuted.
    """
    n = len(lits)
    if kmax is None or kmax > n:
        kmax = n
    cl = []

    def build(items):
        nonlocal nv
        if len(items) == 1:
            return [items[0]]
        mid = len(items) // 2
        A = build(items[:mid])
        B = build(items[mid:])
        m = min(len(A) + len(B), kmax)
        C = []
        for _ in range(m):
            nv += 1
            C.append(nv)
        for al in range(len(A) + 1):
            for be in range(len(B) + 1):
                s = al + be
                if 1 <= s <= m:
                    c = [C[s - 1]]
                    if al >= 1:
                        c.append(-A[al - 1])
                    if be >= 1:
                        c.append(-B[be - 1])
                    cl.append(c)
                if s + 1 <= m:
                    c = [-C[s]]
                    if al < len(A):
                        c.append(A[al])
                    if be < len(B):
                        c.append(B[be])
                    cl.append(c)
        return C

    out = build(list(lits))
    return cl, out, nv


def equals_tot(lits, k, nv):
    """Exactly k of lits, through a totalizer.  Unsatisfiable clauses if k > len(lits)."""
    n = len(lits)
    if k > n:
        return [[]], nv
    cl, out, nv = totalizer(lits, nv, kmax=min(k + 1, n))
    if k >= 1:
        cl.append([out[k - 1]])
    if k + 1 <= len(out):
        cl.append([-out[k]])
    return cl, nv
