"""STAR-ONLY real-affine completion; no centering equation is imposed.

six-downset-2, researcher. Adapted with explicit credits from9269, sourcecf5c6a44575e61993a35e75e6516dc0de4bdb476. A direct singleton-row solve is audited by a
separate exact RREF of all cardinality/star equations. Neither decoder
calls the earlier centered-face decoder. Bounded audits are not a proof
by enumeration of unbounded orders.
"""
from fractions import Fraction as Q
from model import choose, require, parameters as raw_parameters


def parameters(n):
    N, s, h = raw_parameters(n)
    return n-2, N, s, h


def supported_pairs(n):
    r, _, _, _ = parameters(n)
    return [(a, b) for a in range(1, r+1) for b in range(a, r+1) if a+b <= n]


def check_stars(n, B):
    r, _, s, _ = parameters(n)
    require(len(B) == r+1 and all(len(row) == r+1 for row in B), 'Star table shape')
    require(all(type(v) is Q for row in B for v in row), 'Exact rational table')
    require(all(B[a][b] == B[b][a] for a in range(r+1) for b in range(r+1)), 'Star table symmetry')
    require(all(B[a][b] == 0 for a in range(1, r+1) for b in range(1, r+1) if a+b > n), 'Star table support')
    for a in range(1, r+1):
        require(sum(b*B[a][b]*choose(n-a, b) for b in range(1, r+1)) == (n-a)*s, 'Star moment, without centering')


def direct(n, values):
    r, _, s, _ = parameters(n)
    pairs = [(a, b) for a, b in supported_pairs(n) if a >= 2]
    require(len(values) == len(pairs) and all(type(v) is Q for v in values), 'All size-two and larger coordinates')
    B = [[Q(0)]*(r+1) for _ in range(r+1)]
    for (a, b), value in zip(pairs, values):
        B[a][b] = B[b][a] = value
    for a in range(2, r+1):
        B[1][a] = B[a][1] = Q((n-a)*s-sum(b*B[a][b]*choose(n-a, b) for b in range(2, r+1)), n-a)
    B[1][1] = Q((n-1)*s-sum(b*B[1][b]*choose(n-1, b) for b in range(2, r+1)), n-1)
    check_stars(n, B)
    return B


def rref(n):
    require(type(n) is int and n <= 24, 'Independent star-only RREF guard n<=24')
    pairs = supported_pairs(n)
    r, _, s, _ = parameters(n)
    rows = []
    for a in range(1, r+1):
        row = []
        for i, j in pairs:
            b = j if a == i else i if a == j else None
            row.append(Q(b*choose(n-a, b)) if b is not None else Q(0))
        rows.append(row+[Q((n-a)*s)])
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
        pivots.append(col); position += 1
    require(len(pivots) == r and not any(not any(row[:-1]) and row[-1] for row in rows), 'Rank n-2 star-only affine system')
    free = [i for i in range(len(pairs)) if i not in pivots]
    free_pairs = [pairs[i] for i in free]
    require(free_pairs == [(a, b) for a, b in pairs if a >= 2], 'Only singleton coordinates are eliminated')

    def recover(values):
        require(len(values) == len(free) and all(type(v) is Q for v in values), 'Exact free star-only coordinates')
        z = [Q(0)]*len(pairs)
        for i, value in zip(free, values):
            z[i] = value
        for row, col in zip(rows, pivots):
            z[col] = row[-1]-sum(row[i]*z[i] for i in free)
        B = [[Q(0)]*(r+1) for _ in range(r+1)]
        for (a, b), value in zip(pairs, z):
            B[a][b] = B[b][a] = value
        check_stars(n, B)
        return B
    return free_pairs, recover
