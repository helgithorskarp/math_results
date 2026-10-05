"""NEW exact original upper-resolvent and FIRST reader.

six-downset-1 / researcher. Same author, fresh full original elimination;
not independent review. The input geometry is the previously validated
construction credited to source b7d26214d61e1aba86367ce2162ccf2a4e1aa749.
No predecessor program, factor, inverse or result record is imported.
These controls validate the new count formulas, not infinite coverage.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
import resource
import signal
import time

LIMIT_BYTES = 32 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def barrier():
    root = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if root:
        require(not any((Path(root) / name).exists() for name in
                ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                'operational barrier')


def rat(text):
    require(type(text) is str, 'canonical rational string')
    value = F(text)
    require(str(value) == text, 'canonical rational spelling')
    return value


def vector(raw, dimension):
    require(type(raw) is list and len(raw) == dimension, 'whole vector dimension')
    return [rat(value) for value in raw]


def matrix(raw, n, d):
    require(type(raw) is list and len(raw) == n, 'whole matrix row count')
    return [vector(row, d) for row in raw]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def original_gram(rows, metric):
    """All original row pairs; sparsity only skips exact zero coefficients."""
    sparse = [[(j, v) for j, v in enumerate(row) if v] for row in rows]
    products = []
    for row in sparse:
        products.append([sum((v * metric[j][k] for j, v in row
                              if metric[j][k]), F(0))
                         for k in range(len(metric))])
    return [[sum((products[i][j] * value for j, value in row
                  if products[i][j]), F(0)) for row in sparse]
            for i in range(len(rows))]


def full_positive_solve(form, rhs, original_centered=True):
    """Full original Sylvester/Bareiss elimination and two exact RHS solves.

    Every symmetric trailing position and every RHS position is updated;
    every division is checked. No invariant-subspace inverse is used.
    """
    n = len(form)
    require(all(form[i][j] == form[j][i] for i in range(n) for j in range(n)),
            'full original upper form symmetry')
    denominator = 1
    for row in form + rhs:
        for value in row:
            denominator = lcm(denominator, value.denominator)
    integers = [[value.numerator * (denominator // value.denominator)
                 for value in form[i] + [column[i] for column in rhs]]
                for i in range(n)]
    previous, minors, divisions = 1, [], 0
    for k in range(n):
        pivot = integers[k][k]
        require(pivot > 0, 'full original V positive leading minor')
        minors.append(hex(pivot))
        for i in range(k + 1, n):
            factor = integers[i][k]
            for j in range(i, n):
                numerator = integers[i][j] * pivot - factor * integers[k][j]
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, 'full original exact Bareiss division')
                integers[i][j] = integers[j][i] = value
                divisions += 1
            for j in range(n, n + len(rhs)):
                numerator = integers[i][j] * pivot - factor * integers[k][j]
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, 'full original exact RHS division')
                integers[i][j] = value
                divisions += 1
            integers[i][k] = 0
        previous = pivot
    solutions = []
    for j in range(len(rhs)):
        x = [F(0)] * n
        for i in reversed(range(n)):
            x[i] = (F(integers[i][n + j]) -
                    sum((integers[i][k] * x[k] for k in range(i + 1, n)), F(0))) \
                   / integers[i][i]
        require([dot(row, x) for row in form] == rhs[j],
                'EVERY original inverse RHS product')
        if original_centered:
            require(sum(x, F(0)) == 0, 'original inverse image centered')
        solutions.append(x)
    return solutions, dict(dimension=n, denominator=str(denominator),
                           positive_leading_minors=n,
                           complete_positive_leading_minors_sha256=digest(minors),
                           exact_divisions=divisions, whole_rhs_products=n * len(rhs))


def count_formula(n, counts):
    h, q, total = counts[0], 2 ** (n - 1), sum(counts)
    s, N, ell = q + 3 * h, 2 * q + 6 * total, 3 * total + 1
    c0 = F(q * ell + 9 * sum(k * (h - k) for k in counts[1:])
           + 3 * h - 6 * total - 1, ell ** 2)
    R = [F(ell + 1 - q - 3 * (h - k), ell) for k in counts]
    mu = [F(s - 3, 3) - c0 - F(9, 2 * s * (k - 1)) * Rg ** 2
          for k, Rg in zip(counts, R)]
    beta = [F(2 * s, 3) - F(3 * (k + 3), s * (k - 1)) * Rg ** 2
            for k, Rg in zip(counts, R)]
    cg = [F(9, 2 * s) * Rg for Rg in R]
    S = sum((k * u for k, u in zip(counts, mu)), F(0))
    SL = S - h * mu[0]
    WL = sum((k * u * u for k, u in zip(counts[1:], mu[1:])), F(0))
    kappa = 1 / (h * mu[0]) + 1 / SL + 4 * sum(
        (k * u * u / (SL * SL * bg) for k, u, bg in
         zip(counts[1:], mu[1:], beta[1:])), F(0))
    d = [N - 3 * u for u in mu]
    T = sum((k * u * u / dg for k, u, dg in zip(counts, mu, d)), F(0))
    TL = T - h * mu[0] ** 2 / d[0]
    Z = S / 3 + T
    H = [N * N - N * (s * (1 + c * c) + 3 * b / 2) + 3 * s * b / 2
         for c, b in zip(cg, beta)]
    E = [k * (b * (N - s) + F(2 * N, 3) * c * c * s) / Hg
         for k, b, c, Hg in zip(counts, beta, cg, H)]
    Abar = 9 + F(3 * N, h) / d[0] - 3 * N * mu[0] ** 2 / (d[0] ** 2 * Z)
    Bbar = 1 + 2 * WL / (3 * SL ** 2) + N * (TL - TL ** 2 / Z) / (3 * SL ** 2) \
           + sum((u * u * e / (SL ** 2) for u, e in zip(mu[1:], E[1:])), F(0))
    Cbar = 3 - N * mu[0] * TL / (d[0] * SL * Z)
    require(all(value > 0 for value in mu + beta + d + H + [S, SL, Z, kappa]),
            'every count denominator positive')
    require(Abar > 0 and Bbar > 0 and Abar * Bbar > Cbar ** 2,
            'strict original two-RHS Gram')
    require(Cbar >= 6 or Abar * Bbar > (6 - Cbar) ** 2,
            'exact positive root before N/6')
    require(kappa * N < 36, 'N/6 strictly before lower boundary')
    return dict(q=q, s=s, N=N, mu=mu, beta=beta, S=S, SL=SL, WL=WL,
                kappa=kappa, d=d, T=T, TL=TL, Z=Z, H=H, E=E,
                Abar=Abar, Bbar=Bbar, Cbar=Cbar)


def quadratic_endpoint(V, A, B, u, v, alpha, beta, mixed, sign):
    """EVERY original row of BOTH radical endpoints in Q[sqrt(beta/alpha)]."""
    t = beta / alpha
    den = mixed * mixed - alpha * beta
    delta = (mixed / den, -sign * alpha / den)
    x = [(vi, sign * ui) for ui, vi in zip(u, v)]
    def multiply(a, b):
        return (a[0] * b[0] + a[1] * b[1] * t,
                a[0] * b[1] + a[1] * b[0])
    ax = (dot(A, v), sign * dot(A, u))
    bx = (dot(B, v), sign * dot(B, u))
    for i, row in enumerate(V):
        vx = (dot(row, v), sign * dot(row, u))
        dx = (A[i] * bx[0] + B[i] * ax[0],
              A[i] * bx[1] + B[i] * ax[1])
        require(vx == multiply(delta, dx), 'whole original algebraic endpoint kernel')
    square = multiply(delta, delta)
    polynomial = (1 - 2 * mixed * delta[0] + den * square[0],
                  -2 * mixed * delta[1] + den * square[1])
    require(polynomial == (0, 0), 'whole quadratic upper endpoint polynomial')
    require(sum((a for a, _ in x), F(0)) == 0 and
            sum((b for _, b in x), F(0)) == 0,
            'whole algebraic original endpoint vector centered')
    return dict(sign=sign, radical_square=str(t), delta_coefficients=list(map(str, delta)),
                centered_kernel_coefficients=[[str(a), str(b)] for a, b in x],
                original_zero_pairs=len(V), polynomial_zero=True)


def read(data):
    barrier()
    n, counts = data.get('n'), data.get('counts')
    require(type(n) is int and 4 <= n <= 6, 'n preflight BEFORE original arrays')
    require(type(counts) is list and 3 <= len(counts) <= n and
            all(type(k) is int for k in counts), 'literal mark/count preflight')
    h = counts[0]
    require(3 <= h <= 10 and all(2 <= k < h for k in counts[1:]) and sum(counts) >= 9,
            'literal unique-heavy h/count preflight')
    N = 2 ** n + 6 * sum(counts)
    require(N <= 80 and data.get('N') == N and data.get('dimension') == N - 3,
            'original N80 preflight BEFORE construction')
    d = N - 3
    metric, rows = matrix(data['metric'], d, d), matrix(data['rows'], N, d)
    require(all(metric[i][j] == metric[j][i] for i in range(d) for j in range(d)),
            'complete physical metric symmetry')
    A, B = [F(-3)] + vector(data['a'], N - 1), [F(-1)] + vector(data['b'], N - 1)
    require(sum(A, F(0)) == sum(B, F(0)) == 0, 'both repair vectors centered')
    original = original_gram(rows, metric)
    V = [[N * F(i == j) - original[i][j] for j in range(N)] for i in range(N)]
    require(all(sum(row, F(0)) == N for row in V), 'complete original constant action')
    (u, v), factor = full_positive_solve(V, [A, B])
    alpha, beta, mixed = dot(A, u), dot(B, v), dot(A, v)
    require(mixed == dot(B, u), 'BOTH original mixed products')
    f = count_formula(n, counts)
    require(alpha == f['Abar'] / N and beta == f['Bbar'] / N and mixed == f['Cbar'] / N,
            'three new count scalars equal FULL original inverse Gram')
    require(rat(data['kappa']) == f['kappa'], 'credited lower-bound scalar identification')
    first_width = 2 ** n - 1
    first_basis = [[F(i == j) for i in range(d)] for j in range(first_width)]
    offset = first_width
    for group, count in enumerate(counts):
        width = count - 1 if group == 0 else count
        if group:
            first_basis.append([F(offset <= i < offset + width) for i in range(d)])
        offset += width
    first_cross_actions = 0
    for direction in first_basis:
        metric_direction = [dot(row, direction) for row in metric]
        image = [dot(row, metric_direction) for row in rows]
        require(dot(A, image) == dot(B, image) == 0,
                'full original FIRST repair annihilation')
        frame_image = [sum((row[j] * x for row, x in zip(rows, image)), F(0))
                       for j in range(d)]
        require(all(value == 0 for value in frame_image[offset:]),
                'entire FIRST frame no T/residual cross action')
        at = first_width
        for group, count in enumerate(counts):
            width = count - 1 if group == 0 else count
            values = frame_image[at:at + width]
            require((all(value == 0 for value in values) if group == 0 else
                     all(value == values[0] for value in values)),
                    'entire FIRST frame no group-standard cross action')
            at += width
        first_cross_actions += d
    endpoints = [quadratic_endpoint(V, A, B, u, v, alpha, beta, mixed, sign)
                 for sign in (1, -1)]
    return dict(agent='six-downset-1', role='researcher', status='NEW ORIGINAL UPPER/FIRST VALIDATED',
                n=n, counts=counts, N=N, original_pairs=N * N,
                original_V_sha256=digest([[str(x) for x in row] for row in V]),
                full_original_positive_solve=factor,
                original_inverse_images=[[str(x) for x in y] for y in (u, v)],
                original_inverse_Gram=[str(alpha), str(beta), str(mixed)],
                all_count_scalars={name: [str(x) for x in value] if type(value) is list else
                                   str(value) for name, value in f.items()},
                original_endpoint_kernels=endpoints,
                original_first_dimension=len(first_basis),
                first_annihilations=2 * len(first_basis),
                whole_first_cross_actions=first_cross_actions,
                upper_positive_root_before_N_over_6=True,
                lower_boundary_strictly_after_N_over_6=True,
                infinite_completeness='ORDINARY UNFORMALIZED; controls do not prove all counts',
                independently_reviewed=False, new_source_commit=None, new_graph_ref=None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'unique output')
    require(args.input.stat().st_size <= LIMIT_BYTES, '32MiB BEFORE data read')
    def expire(_signal, _frame):
        raise TimeoutError('unchanged60s; incomplete work is not mathematical nonexistence')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    started = time.monotonic()
    data = args.input.read_bytes()
    result = read(json.loads(data))
    mathematical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode() + b'\n'
    require(len(mathematical) <= LIMIT_BYTES, '32MiB whole mathematical output')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(mathematical)
    signal.alarm(0)
    print(json.dumps(dict(status=result['status'], input_sha256=sha256(data).hexdigest(),
                         mathematical_bytes=len(mathematical), mathematical_sha256=sha256(mathematical).hexdigest(),
                         seconds=time.monotonic() - started,
                         peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == '__main__':
    main()
