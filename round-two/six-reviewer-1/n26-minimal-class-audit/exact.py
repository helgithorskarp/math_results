"""Fresh exact square-completion and elementary linear algebra; no native imports."""
from fractions import Fraction as Q


def need(ok, message):
    if not ok:
        raise ValueError(message)


def matmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def transpose(a):
    return [list(col) for col in zip(*a)]


def solve(a, b):
    n = len(a)
    m = [list(map(Q, row))+[Q(b[i])] for i, row in enumerate(a)]
    for k in range(n):
        p = next((i for i in range(k, n) if m[i][k]), None)
        need(p is not None, 'singular defining linear system')
        m[k], m[p] = m[p], m[k]
        d = m[k][k]
        m[k] = [v/d for v in m[k]]
        for i in range(n):
            if i != k:
                d = m[i][k]
                m[i] = [x-d*y for x, y in zip(m[i], m[k])]
    return [row[-1] for row in m]


def pivot_rows(columns):
    if not columns:
        return []
    m = [list(map(Q, c)) for c in columns]
    r = 0
    pivots = []
    for k in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][k]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        d = m[r][k]
        m[r] = [v/d for v in m[r]]
        for i in range(len(m)):
            if i != r:
                d = m[i][k]
                m[i] = [x-d*y for x, y in zip(m[i], m[r])]
        pivots.append(k)
        r += 1
        if r == len(m):
            break
    need(r == len(columns), 'dependent prescribed kernel')
    return pivots


def psd(a, positive=False):
    """Symmetric diagonal pivoting and exact completion of squares, recording pivots."""
    n = len(a)
    need(all(len(row) == n for row in a), 'nonsquare')
    need(a == transpose(a), 'asymmetric form')
    m = [list(map(Q, row)) for row in a]
    labels = list(range(n))
    pivots = []
    while m:
        need(all(m[i][i] >= 0 for i in range(len(m))), 'negative diagonal')
        p = next((i for i in range(len(m)) if m[i][i] > 0), None)
        if p is None:
            need(all(v == 0 for row in m for v in row), 'zero diagonal with cross')
            break
        d = m[p][p]
        pivots.append([labels[p], str(d)])
        keep = [i for i in range(len(m)) if i != p]
        m = [[m[i][j]-m[i][p]*m[p][j]/d for j in keep] for i in keep]
        labels = [labels[i] for i in keep]
    need(not positive or len(pivots) == n, 'singular positive floor')
    return pivots


def cut(a, keep):
    return [[a[i][j] for j in keep] for i in keep]


def subtract(a, b, scale=Q(1)):
    return [[x-scale*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def pack(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, list):
        return [pack(v) for v in x]
    if isinstance(x, dict):
        return {k: pack(v) for k, v in x.items()}
    return x
