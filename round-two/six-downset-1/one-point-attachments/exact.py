"""Credited exact primitives copied from the own published arbitrary-pendant packet.

Underlying core/whole checks originate in structural7578 and own verify.py;
Gram assembly in verify_two_marks.py. These copies supply no independent review.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

def require(condition, message):
    if not condition:
        raise ValueError(message)

def rational_matrix(a):
    n = len(a)
    require(n > 0 and all(len(row) == n for row in a), "nonsquare matrix")
    return [[F(x) for x in row] for row in a]

def psd_rank(a):
    """Exact symmetric Schur elimination, including singular residuals."""
    a = rational_matrix(a)
    n = len(a)
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            "nonsymmetric PSD input")
    rank = 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, "negative PSD pivot")
        if pivot == 0:
            require(all(a[k][j] == 0 for j in range(k + 1, n)),
                    "zero PSD pivot with nonzero residual")
            continue
        rank += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank

def family_star(family):
    require(family and family[0] == 0 and len(set(family)) == len(family),
            "bad family indexing")
    require(all(isinstance(a, int) and a >= 0 for a in family), "bad set mask")
    present = set(family)
    for a in family:
        sub = a
        while True:
            require(sub in present, "family is not a downset")
            if sub == 0:
                break
            sub = (sub - 1) & a
    require(len(family) >= 2, "trivial family")
    return max(sum(bool(a & (1 << i)) for a in family)
               for i in range(max(family).bit_length()))

def fingerprint(a):
    encoded = json.dumps([[str(x) for x in row] for row in a],
                         separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()

def lift(c, s):
    """Core constructor, distinct from the factor-entry union constructor."""
    c = rational_matrix(c)
    m = len(c)
    n = m + 1
    rows = [sum(row) for row in c]
    q = [[sum(rows)] + [-v for v in rows]]
    q += [[-rows[i]] + c[i] for i in range(m)]
    return [[(q[i][j] + 1 - s * int(i == j)) / (n - s)
             for j in range(n)] for i in range(n)]

def matvec(a, v):
    return [dot(row, v) for row in a]

def gram(a, coefficients, independent):
    images = [matvec(a, c) for c in coefficients]
    sparse = [[(i, x) for i, x in enumerate(c) if x] for c in coefficients]
    return [[sum(x*images[j][k] for k, x in sparse[i])+independent[i][j]
             for j in range(len(coefficients))] for i in range(len(coefficients))]

def dot(x,y):return sum(a*b for a,b in zip(x,y))
