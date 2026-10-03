"""PRIVATE rational inverse energies for the fixed original three-pair line.

Actual author six-downset-1, researcher. The seed sector functions and exact
field are unchanged credited source2252bca. No finite fixture or endpoint
ordering is asserted to prove a uniform statement.
"""
from fractions import Fraction as F
from sectors import sectors


def require(ok, message):
    if not ok:
        raise ValueError(message)


def solve_many(matrix, right, register=lambda z: None):
    """Exact Gaussian elimination with shared pivots and two right sides."""
    a = [list(row) + list(rhs) for row, rhs in zip(matrix, right)]
    n = len(a)
    count = len(right[0])
    pivots = []
    for k in range(n):
        pivot = a[k][k]
        require(bool(pivot), 'nonzero original normalized pivot')
        register(pivot)
        pivots.append(pivot)
        for i in range(k + 1, n):
            multiplier = a[i][k] / pivot
            for j in range(k + 1, n + count):
                a[i][j] = a[i][j] - multiplier * a[k][j]
            a[i][k] = F(0)
    solved = [[F(0) for j in range(count)] for i in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(count):
            solved[i][j] = (
                a[i][n + j]
                - sum((a[i][k] * solved[k][j] for k in range(i + 1, n)), F(0))
            ) / a[i][i]
    for i in range(n):
        for j in range(count):
            require(sum((matrix[i][k] * solved[k][j] for k in range(n)), F(0)) == right[i][j],
                    'entire compact inverse equation')
    return solved, pivots


def energies(q, h, register=lambda z: None):
    if type(q) is int:
        q = F(q)
    if type(h) is int:
        h = F(h)
    p, grams, frames, ignored = sectors(q, h)
    N, s, beta, nu, c, b = [p[name] for name in ('N', 's', 'beta', 'nu', 'c', 'b')]
    g = grams['standard']
    frame = frames['standard']
    normalized = [[N * int(i == j) - frame[i][j] / g[i][i] for j in range(4)] for i in range(4)]
    zu = [F(0), c * h / (3 * (h - 1)), F(0), F(3)]
    zv = [b, c / (3 * (h - 1)), F(1), F(1)]
    standard, standard_pivots = solve_many(normalized, [[zu[i], zv[i]] for i in range(4)], register)
    eu = sum((g[i][i] * zu[i] * standard[i][0] for i in range(4)), F(0))
    ev = sum((g[i][i] * zv[i] * standard[i][1] for i in range(4)), F(0))
    trace = [[12 * s * (N - s * (1 + c * c)), 6 * c * s * beta],
             [6 * c * s * beta, beta * (2 * N - 3 * beta)]]
    paired = [-2 * s * c, beta]
    # Divide rows by the positive trace metric, just as for the standard solve.
    trace_metric = [12 * s, 2 * beta]
    trace_normal = [[trace[i][j] / trace_metric[i] for j in range(2)] for i in range(2)]
    trace_rhs = [[paired[i] / trace_metric[i]] for i in range(2)]
    trace_solution, trace_pivots = solve_many(trace_normal, trace_rhs, register)
    et = sum((paired[i] * trace_solution[i][0] for i in range(2)), F(0)) / h
    mean = nu / (2 * h * (N - 3 * nu))
    gamma = (h - 1) / (2 * h)
    A = (12 + gamma * eu + 9 * mean) / N
    B = (2 + gamma * ev + 2 * et + mean) / N
    D = (3 - 3 * mean) / N
    kappa = 2 / nu + 4 / beta
    return dict(parameters=p, standard_matrix=normalized, standard_rhs=[zu, zv],
                standard_solution=standard, standard_pivots=standard_pivots,
                trace_matrix=trace_normal, trace_rhs=trace_rhs,
                trace_solution=trace_solution, trace_pivots=trace_pivots,
                Eu=eu, Ev=ev, Et=et, mean=mean, A=A, B=B, D=D, kappa=kappa)
