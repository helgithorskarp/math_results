"""Separate rational elimination of center/star defining equations.

This bounded arithmetic audit retains the9017/9147 affine model credit.
It does not replace the ordinary arbitrary-real negative proof.
"""
from fractions import Fraction as Q
from certificate import choose, parameters, check_rows, require


def affine(n):
    require(n <= 24, 'Independent RREF audit guard n<=24')
    r, T, s, m = parameters(n)
    pairs = [(a, b) for a in range(1, r+1) for b in range(a, r+1) if a+b <= n]
    rows = []
    for a in range(1, r+1):
        for moment in (0, 1):
            row = []
            for i, j in pairs:
                b = j if a == i else i if a == j else None
                row.append(Q(choose(n-a, b)*(b if moment else 1)) if b is not None else Q(0))
            rows.append(row+[Q((n-a)*s if moment else m-s)])
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
    require(not any(not any(row[:-1]) and row[-1] for row in rows), 'Consistent affine equations')
    free = [i for i in range(len(pairs)) if i not in pivots]
    free_pairs = [pairs[i] for i in free]
    require(free_pairs == [(a, b) for a, b in pairs if a >= 3], 'All and only middle coordinates are free')

    def recover(values):
        require(len(values) == len(free) and all(type(v) is Q for v in values), 'Rational coordinates')
        z = [Q(0)]*len(pairs)
        for i, value in zip(free, values):
            z[i] = value
        for row, col in zip(rows, pivots):
            z[col] = row[-1]-sum(row[i]*z[i] for i in free)
        B = [[Q(0)]*(r+1) for _ in range(r+1)]
        for (a, b), value in zip(pairs, z):
            B[a][b] = B[b][a] = value
        check_rows(n, B)
        return B
    return free_pairs, recover
