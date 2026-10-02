"""Independent original-index finite controls; uniformity is proved separately.

Fraction/Bareiss/lift primitives reuse six-reviewer-1's own published 9049
checker. The literal family construction extends it to arbitrary mark
multiplicities; no researcher executable, fixture or polynomial is imported.
No all-parameter sign proof is supplied by finite fixtures.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
import json
from itertools import product

CHECKS = 0


class Failure(ValueError):
    pass


def need(ok, label):
    global CHECKS
    if not ok:
        raise Failure(label)
    CHECKS += 1


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F())


def image(a, x):
    return [dot(row, x) for row in a]


def lin(*terms):
    return [sum((c * v[i] for c, v in terms), F()) for i in range(len(terms[0][1]))]


def unit(n, k):
    return [F(i == k) for i in range(n)]


def psd(a):
    """Pivoted fraction-free positive congruence, requiring a zero full residual."""
    n = len(a)
    need(n > 0 and all(len(row) == n for row in a), 'square PSD matrix')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'symmetric PSD matrix')
    denominator = 1
    for row in a:
        for x in row:
            denominator = lcm(denominator, F(x).denominator)
    b = [[int(x * denominator) for x in row] for row in a]
    rank, previous = 0, 1
    while b:
        size = len(b)
        need(all(b[i][i] >= 0 for i in range(size)), 'nonnegative congruence diagonal')
        k = max(range(size), key=lambda i: b[i][i])
        pivot = b[k][k]
        if not pivot:
            need(all(x == 0 for row in b for x in row), 'complete zero PSD residual')
            break
        idx = [i for i in range(size) if i != k]
        new = [[0] * len(idx) for _ in idx]
        for ii, i in enumerate(idx):
            for jj in range(ii, len(idx)):
                j = idx[jj]
                value, rem = divmod(pivot * b[i][j] - b[i][k] * b[k][j], previous)
                need(rem == 0, 'exact Bareiss congruence division')
                new[ii][jj] = new[jj][ii] = value
        rank += 1
        previous, b = pivot, new
    return rank


def kernel(a):
    a = [[F(x) for x in row] for row in a]
    width = len(a[0])
    pivots, r = [], 0
    for j in range(width):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        a[r] = [x / a[r][j] for x in a[r]]
        for i in range(len(a)):
            if i != r:
                a[i] = [x - a[i][j] * y for x, y in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    out = []
    for j in range(width):
        if j in pivots:
            continue
        v = unit(width, j)
        for i, p in enumerate(pivots):
            v[p] = -a[i][j]
        out.append(v)
    return out


def lift(c):
    rows = [sum(row) for row in c]
    return [[sum(rows), *[-x for x in rows]], *[[-rows[i], *row] for i, row in enumerate(c)]]


def gram(base, coefficients, residual=None):
    imgs = [image(base, v) for v in coefficients]
    out = [[dot(v, img) for img in imgs] for v in coefficients]
    if residual is not None:
        out = [[x + residual[i][j] for j, x in enumerate(row)] for i, row in enumerate(out)]
    return out


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in row] for row in a], separators=(',', ':')).encode()).hexdigest()


def build(n, k, r, D, t, positions):
    need(type(n) is int and 3 <= n <= 6, 'literal cube guard')
    need(type(D) is int and type(t) is int and D > t >= 1, 'strict positive integer load domain')
    need(type(k) is int and type(r) is int and k >= 2 and r >= 1 and k + r <= n, 'new multiple-heavy finite domain')
    need(len(positions) == k + r and len(set(positions)) == k + r and
         all(type(x) is int and 0 <= x < n for x in positions), 'distinct literal marks')
    loads = [D] * k + [t] * r
    q, m = 1 << (n - 1), k * D + r * t
    N, s = 2 * q + 2 * m, q + D
    need(N <= 80, 'fixed original-index size guard')
    w, old = F(s - 1), list(range(1, 2 * q))
    oldn = len(old)
    oldC = [[F((q + D) * int(a == b) + (q - D) * int(a ^ b == 2 * q - 1) - 1)
             for b in old] for a in old]
    need(psd(oldC) == oldn, 'old cube PD')
    H = [[-F(bool(a & (1 << p))) for a in old] for p in positions]
    Himages = [image(oldC, x) for x in H]
    need([[dot(x, y) for y in Himages] for x in H] == [[q * D * int(i == j) for j in range(k + r)] for i in range(k + r)], 'all marked old Gram')
    labels = [i for i, load in enumerate(loads) for _ in range(load)]
    coefficients = [unit(oldn, i) for i in range(oldn)]
    coefficients += [lin((F(1, D), H[k])) for k in labels]
    base = gram(oldC, coefficients)
    for i in range(m):
        for j in range(m):
            if labels[i] == labels[j]:
                base[oldn + i][oldn + j] += (q + D) * (int(i == j) - F(1, D))
    width = oldn + m
    S = [unit(width, oldn + j) for j in range(m)]
    K = [F(1)] * width
    cs = [F(m * (w - load - m - 1), m + 1) / ((m - 1) * w - 1 + load)
          for load in [loads[i] for i in labels]]
    Csum = [F(0)] * oldn + cs
    U = [lin((-F(1, m + 1), K), (cs[j], S[j]), (-F(1, m), Csum)) for j in range(m)]
    eta = [w - dot(v, image(base, v)) for v in U]
    E = sum(eta)
    zeta = [F(m, m - 2) * (e - E / (m * (m - 1))) for e in eta]
    W = [[zeta[i] * int(i == j) - (zeta[i] + zeta[j]) / m + sum(zeta) / m ** 2
          for j in range(m)] for i in range(m)]
    need(all(x > 0 for x in zeta), 'positive W weights')
    need([W[i][i] for i in range(m)] == eta and all(sum(row) == 0 for row in W), 'all W diagonal/row identities')
    need(psd(W) == m - 1, 'W exact rank')
    canonical = [0, *old]
    seedco = [unit(width, i) for i in range(oldn)]
    rawco = [unit(width, i) for i in range(oldn)]
    singleton_indices, spoke_indices = [], []
    for j, label in enumerate(labels):
        fresh = 1 << (n + j)
        canonical.extend([fresh | (1 << positions[label]), fresh])  # spoke BEFORE leaf
        spoke_indices.append(len(seedco))
        singleton_indices.append(len(seedco) + 1)
        seedco.extend([S[j], U[j]])
        rawco.extend([S[j], lin((-1 / w, S[j]))])
    residual = [[F(0)] * (N - 1) for _ in range(N - 1)]
    rawresidual = [[F(0)] * (N - 1) for _ in range(N - 1)]
    for i, row in enumerate(W):
        for j, value in enumerate(row):
            residual[singleton_indices[i]][singleton_indices[j]] = value
        rawresidual[singleton_indices[i]][singleton_indices[i]] = w - 1 / w
    seed, raw = gram(base, seedco, residual), gram(base, rawco, rawresidual)
    B0 = w + m * (q + D) - sum(load ** 2 for load in loads) - 2 * m
    need(sum(map(sum, seed)) == B0 / (m + 1) ** 2, 'actual seed empty energy')
    rawB = w + (1 - 1 / w) ** 2 * (m * (q + D) - sum(load ** 2 for load in loads)) - 2 * m * (1 - 1 / w) + m * (w - 1 / w)
    need(sum(map(sum, raw)) == rawB and rawB >= 0, 'actual raw empty energy')
    return {'n': n, 'k': k, 'r': r, 'q': q, 'D': D, 't': t, 'm': m, 'N': N, 's': s, 'w': w,
            'canonical': canonical, 'seed': seed, 'raw': raw, 'oldC': oldC,
            'H': H, 'Sindices': spoke_indices, 'Uindices': singleton_indices,
            'c': [cs[0], cs[-1]], 'zeta': [zeta[0], zeta[-1]],
            'B0': B0, 'rawB': rawB, 'raw_trace': (N - 1) * w + rawB}


def validate(family, Q, s, lower_rank, margin):
    N = len(family)
    M = [[(Q[i][j] + 1 - s * int(i == j)) / (N - s) for j in range(N)] for i in range(N)]
    need(family[0] == 0 and len(set(family)) == N, 'actual empty and distinct family')
    need(all(sum(row) == 1 for row in M), 'all exact row sums')
    need(all(M[i][j] == M[j][i] and (not (a & b) or M[i][j] == 0)
             for i, a in enumerate(family) for j, b in enumerate(family)), 'all original set support/symmetry')
    need(psd([[x + 1 for x in row] for row in Q]) == lower_rank, 'full lower PSD rank')
    if margin is not None:
        need(psd([[(N - margin) * (int(i == j) - F(1, N)) - Q[i][j] for j in range(N)]
                  for i in range(N)]) == N - 1, 'full scaled upper cap and rank')
    index = sorted(range(N), key=lambda i: (family[i].bit_count(), family[i]))
    return {'lower_rank': lower_rank, 'upper_rank': N - 1 if margin is not None else None,
            'scaled_gap': str(margin), 'matrix_sha256': fingerprint([[M[i][j] for j in index] for i in index])}

