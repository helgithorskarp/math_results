"""Separate literal rational Gaussian solve for the compression/energy checks."""
import bootstrap
from fractions import Fraction as F
from exact import require


def solve(matrix, rhs):
    n = len(matrix)
    require(n > 0 and all(len(r) == n for r in matrix), 'nonsquare linear system')
    require(len(rhs) == n and rhs and len({len(r) for r in rhs}) == 1, 'invalid rhs dimensions')
    require(all(isinstance(x, (int, F)) for r in matrix+rhs for x in r), 'inexact linear system')
    width = len(rhs[0])
    a = [[F(x) for x in matrix[i]+rhs[i]] for i in range(n)]
    for k in range(n):
        p = next((i for i in range(k, n) if a[i][k]), None)
        require(p is not None, 'singular linear system')
        a[k], a[p] = a[p], a[k]
        scale = a[k][k]
        a[k] = [x/scale for x in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                scale = a[i][k]
                a[i] = [x-scale*y for x, y in zip(a[i], a[k])]
    answer = [r[n:] for r in a]
    require(all(sum(matrix[i][j]*answer[j][h] for j in range(n)) == rhs[i][h]
                for i in range(n) for h in range(width)), 'linear solve residual')
    return answer


def inverse(matrix):
    n = len(matrix)
    return solve(matrix, [[F(int(i == j)) for j in range(n)] for i in range(n)])


def energy(matrix, columns, anchors):
    """Solve a PD principal quotient; supplied columns must annihilate the kernel."""
    n = len(matrix)
    keep = [i for i in range(n) if i not in anchors]
    solution = solve([[matrix[i][j] for j in keep] for i in keep],
                     [[v[i] for v in columns] for i in keep])
    extended = [[F(0)]*len(columns) for _ in range(n)]
    for i, row in zip(keep, solution):
        extended[i] = row
    require(all(sum(matrix[i][j]*extended[j][h] for j in range(n)) == columns[h][i]
                for i in range(n) for h in range(len(columns))), 'quotient solve/kernel residual')
    return [[sum(v[i]*extended[i][h] for i in range(n)) for h in range(len(columns))] for v in columns]
