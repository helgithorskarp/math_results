"""Exact elementary arithmetic by six-reviewer-1; standard library only."""
from fractions import Fraction as F


def require(ok, message):
    if not ok:
        raise ValueError(message)


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in bt] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b, scale=1):
    return [[x+scale*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def rref(a, width):
    a = [[F(x) for x in row] for row in a]
    at = 0
    pivots = []
    for j in range(width):
        pivot = next((i for i in range(at, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[at], a[pivot] = a[pivot], a[at]
        t = a[at][j]
        a[at] = [x/t for x in a[at]]
        for i in range(len(a)):
            if i != at and a[i][j]:
                t = a[i][j]
                a[i] = [x-t*y for x, y in zip(a[i], a[at])]
        pivots.append(j)
        at += 1
        if at == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a, len(a[0]))[1]) if a and a[0] else 0


def inverse(a):
    n = len(a)
    z, piv = rref([r+s for r, s in zip(a, eye(n))], n)
    require(piv == list(range(n)), "singular inverse")
    return [r[n:] for r in z]


def solve(rows, width):
    z, piv = rref(rows, width)
    require(all(any(r[:width]) or not r[-1] for r in z), "inconsistent equations")
    free = [j for j in range(width) if j not in piv]
    base = [F(0)]*width
    for i, j in enumerate(piv):
        base[j] = z[i][-1]
    null = []
    for j in free:
        v = [F(0)]*width
        v[j] = 1
        for i, t in enumerate(piv):
            v[t] = -z[i][j]
        null.append(v)
    return base, null


def psd(a):
    """Exact symmetric Schur elimination, including singular pivots."""
    a = [[F(x) for x in row] for row in a]
    while a:
        require(a == tr(a), "asymmetric PSD input")
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        i = next((i for i in range(len(a)) if a[i][i]), None)
        if i is None:
            return not any(any(row) for row in a)
        ids = [j for j in range(len(a)) if j != i]
        t = a[i][i]
        a = [[a[j][k]-a[j][i]*a[i][k]/t for k in ids] for j in ids]
    return True


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x
