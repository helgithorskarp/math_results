#!/usr/bin/env python3
"""Independent exact interpolation and literal-affine audit, six-reviewer-1.

Imports no author executable, solver, CAS, or floating-point package.
The written degree bound in REVIEW.md is part of the interpolation proof.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return c


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def interpolate(values, start):
    """Newton forward differences at consecutive integral abscissae."""
    differences = list(map(F, values))
    result, falling = [F(0)], [F(1)]
    for k in range(len(values)):
        result = add(result, [differences[0] * x / factorial(k) for x in falling])
        differences = [b - a for a, b in zip(differences, differences[1:])]
        falling = mul(falling, [-(start + k), 1])
    return result


def evaluate(row, x):
    value = F(0)
    for c in reversed(row):
        value = value * x + c
    return value


def rational_data(n, X=None):
    if X is None:
        X = 2 ** n
    N, s, m = X - n - 1, F(X, 2) - n, X - 2 * n - 2
    e = F(n * (n - 1), 2)
    c = F(n * (n * n - 3 * n + 4), 4)
    C2 = F(n * X, 4) - 2 * c
    C4 = F((3 * n * n - 2 * n) * X, 16) - F(n ** 4 + n * (n - 2) ** 4, 8)
    V = N * (C2 + c) - e * e
    a = F(2 * n + 5, n * n)
    HL = m + a * a * C2 / 2 - a ** 4 * C4 / 8
    DL = e * HL + N * a * C2
    HH = m + 2 * a * a * C2
    E = (N - s) * HH + m * (s - m)
    return dict(n=n, N=N, s=s, m=m, e=e, c=c, C2=C2, C4=C4,
                V=V, a=a, HL=HL, DL=DL, HH=HH, E=E)


def polynomial_value(n, X):
    d = rational_data(n, X)
    return 65536 * n ** 12 * (d['DL'] ** 2 - d['V'] * d['E'])


def polynomial_certificate():
    # Proven degree bounds are deg_X <= 3 and deg_n <= 18.
    x_rows = [interpolate([polynomial_value(n, X) for X in range(4)], 0)
              for n in range(1, 20)]
    rows = [interpolate([row[k] for row in x_rows], 1) for k in range(4)]
    for row in rows:
        while row and not row[-1]:
            row.pop()
        require(all(x.denominator == 1 for x in row), 'integer polynomial coefficients')
    rows = [[int(x) for x in row] for row in rows]
    require([len(r) for r in rows] == [19, 18, 16, 13], 'polynomial degrees')
    # Supplementary evaluations independently catch indexing/implementation defects.
    for n, X in [(20, -3), (23, 7), (31, 2 ** 31), (5, 100), (2, -7)]:
        require(sum(evaluate(r, n) * X ** k for k, r in enumerate(rows))
                == polynomial_value(n, X), 'outside-grid evaluation')
    tests = {'c0': rows[0][:], 'c2': rows[2][:],
             'c3_lower': rows[3][:], 'c1_lower': rows[1][:]}
    tests['c3_lower'][12] -= 8192
    tests['c1_lower'][17] += 8192
    shifted = {}
    for name, row in tests.items():
        while row and not row[-1]:
            row.pop()
        shifted[name] = [sum(row[k] * comb(k, j) * 8 ** (k - j)
                             for k in range(j, len(row))) for j in range(len(row))]
        require(all(x > 0 for x in shifted[name]), 'strict shifted positivity')
    require(sum(len(r) for r in shifted.values()) == 65, 'complete sign certificate')
    require(4 ** 8 > 8 ** 5 and 9 ** 5 < 4 * 8 ** 5, 'induction base and ratio')
    # Exact universal square-bound identity in QQ[x].
    square = mul([1, F(1, 2), F(-1, 8)], [1, F(1, 2), F(-1, 8)])
    require(add([1, 1], [-x for x in square]) == [0, 0, 0, F(1, 8), F(-1, 64)],
            'square-bound polynomial')
    return {'interpolation_grid': {'n': [1, 19], 'X': [0, 3], 'evaluations': 76},
            'degree_bound': [18, 3], 'coefficient_arrays': rows,
            'positive_shifted_coefficients': shifted,
            'nonzero_coefficients': sum(bool(x) for row in rows for x in row),
            'induction_checks': [4 ** 8, 8 ** 5, 9 ** 5, 4 * 8 ** 5]}


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def quadratic(L, x):
    return sum(x[i] * x[j] * L[i][j] for i in range(len(x)) for j in range(len(x)))


def literal_affine_audit(n):
    """Direct original-index star/row completion, with arbitrary signed weights."""
    D = [A for A in range(2 ** n) if A.bit_count() <= n - 2]
    index = {A: i for i, A in enumerate(D)}
    T = [A for A in D if 2 <= A.bit_count()]
    N, s, m = len(D), sum(bool(A & 1) for A in D), len(T)
    edges = [(A, B) for t, A in enumerate(T) for B in T[t + 1:] if not A & B]
    L = [[F(0) for _ in D] for _ in D]
    for A in D[1:]:
        L[index[A]][index[A]] = s
    for t, (A, B) in enumerate(edges):
        L[index[A]][index[B]] = L[index[B]][index[A]] = F(t % 9 - 4, 7)
    for i in range(n):
        pi = index[1 << i]
        for A in T:
            val = s - sum(L[index[A]][index[B]] for B in T if B & (1 << i))
            L[pi][index[A]] = L[index[A]][pi] = val
    for i in range(n):
        for j in range(i + 1, n):
            pi, pj = index[1 << i], index[1 << j]
            val = s - sum(L[pi][index[A]] for A in T if A & (1 << j))
            require(val == s - sum(L[pj][index[A]] for A in T if A & (1 << i)),
                    'symmetric singleton completion')
            L[pi][pj] = L[pj][pi] = val
    for i in range(1, N):
        L[0][i] = L[i][0] = N - sum(L[i][1:])
    L[0][0] = N - sum(L[0][1:])
    for i, A in enumerate(D):
        require(sum(L[i]) == N, 'all row sums')
        for j, B in enumerate(D):
            require(not A & B or L[i][j] == (s if A == B else 0), 'all support entries')
        for p in range(n):
            require(sum(L[i][j] for j, B in enumerate(D) if B & (1 << p)) == s,
                    'all forced star equations')
    h = {k: F(k * k + (-1) ** k, n + 1) for k in range(2, n - 1)}
    f = list(map(int.bit_count, D))
    g = [h[A.bit_count()] if A in T else F(0) for A in D]
    tau, gamma = F(3, 7), F(5, 11)
    w = [tau * x - y for x, y in zip(f, g)]
    u = [F(int(A in T)) - F(m, N) for A in D]
    A0, B0, H, FH, HH = sum(f), dot(f, f), sum(g), dot(f, g), dot(g, g)
    V, D0 = N * B0 - A0 * A0, N * FH - A0 * H
    left = N * dot(w, w) - quadratic(L, w) + gamma * quadratic(L, u)
    constant = V * tau * tau - 2 * D0 * tau + (N - s) * HH + gamma * m * (s - m)
    right = constant + 2 * sum((gamma - h[A.bit_count()] * h[B.bit_count()])
                               * L[index[A]][index[B]] for A, B in edges)
    require(left == right, 'full original-index dual identity')
    derivative_rows = []
    # Each free-entry perturbation is built in original coordinates; no author lift.
    for A, B in edges:
        vA = {index[A]: 1, 0: A.bit_count() - 1}
        vB = {index[B]: 1, 0: B.bit_count() - 1}
        for p in range(n):
            if A & (1 << p):
                vA[index[1 << p]] = -1
            if B & (1 << p):
                vB[index[1 << p]] = -1
        dw = 2 * sum(w[i] * w[j] * x * y for i, x in vA.items() for j, y in vB.items())
        du = 2 * sum(u[i] * u[j] * x * y for i, x in vA.items() for j, y in vB.items())
        expected = 2 * (gamma - h[A.bit_count()] * h[B.bit_count()])
        require(-dw + gamma * du == expected, 'every free dual coefficient')
        derivative_rows.append([A, B, str(expected)])
    # Verify the centered Euclidean projection norm independently of the dual.
    t = D0 / V
    z = [t * (x - F(A0, N)) - (y - H / N) for x, y in zip(f, g)]
    require(sum(z) == 0 and dot(z, [x - F(A0, N) for x in f]) == 0,
            'centered optimized projection')
    require(dot(z, z) == HH - H * H / N - D0 * D0 / (N * V), 'residual norm identity')
    digest = sha256(json.dumps(derivative_rows, separators=(',', ':')).encode()).hexdigest()
    return {'n': n, 'N': N, 's': s, 'free_coefficients': len(edges),
            'derivative_sha256': digest, 'dual_left': str(left), 'dual_right': str(right),
            'PSD_claim_for_control_matrix': False}


def moments_and_gap():
    records = []
    for n in range(4, 81):
        d = rational_data(n)
        counts = [comb(n, k) for k in range(n - 1)]
        N = sum(counts)
        A0 = sum(k * counts[k] for k in range(n - 1))
        B0 = sum(k * k * counts[k] for k in range(n - 1))
        C2 = sum(comb(n, k) * F(2 * k - n, 2) ** 2 for k in range(2, n - 1))
        C4 = sum(comb(n, k) * F(2 * k - n, 2) ** 4 for k in range(2, n - 1))
        require((N, A0, N * B0 - A0 * A0, C2, C4) ==
                (d['N'], n * d['s'], d['V'], d['C2'], d['C4']), 'literal binomial moments')
        if n < 6:
            continue
        Phi = d['E'] - d['DL'] ** 2 / d['V']
        R = d['HH'] - d['HL'] ** 2 / d['N'] - d['DL'] ** 2 / (d['N'] * d['V'])
        beta = -Phi / (2 * (d['N'] - d['s']))
        require(Phi < 0 and R > 0, 'supplementary rational sign controls')
        if n in (6, 7, 8, 16):
            records.append({'n': n, 'Phi_upper': str(Phi), 'beta': str(beta),
                            'R_upper': str(R), 'spectral_excess_bound': str(2 * beta / R)})
    return {'moment_orders': [4, 80], 'selected_rational_bounds': records,
            'scope': 'Supplementary finite controls; unbounded proof is written.'}


def backend_controls():
    for start, row in [(0, [1, 2, 3]), (1, [7, -3, 0, 9]), (-2, [1, 0, -5, 0, 2])]:
        values = [evaluate(row, start + j) for j in range(len(row))]
        require(interpolate(values, start) == row, 'known-polynomial interpolation')
    damaged = [polynomial_value(1, X) for X in range(4)]
    damaged[2] += 1
    require(interpolate(damaged, 0) != interpolate([polynomial_value(1, X) for X in range(4)], 0),
            'corruption control')
    return {'known_polynomials': 3, 'damaged_evaluation_rejected': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--author-certificate', type=Path)
    args = parser.parse_args()
    result = {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
              'polynomial': polynomial_certificate(), 'backend_controls': backend_controls(),
              'literal_affine_checks': [literal_affine_audit(n) for n in (6, 7)],
              'moments_and_spectral_refinement': moments_and_gap()}
    if args.author_certificate:
        author = json.loads(args.author_certificate.read_text())
        require(result['polynomial']['coefficient_arrays'] ==
                [[int(x) for x in r] for r in author['coefficient_arrays']], 'author coefficient match')
        require(result['polynomial']['positive_shifted_coefficients'] ==
                {k: list(map(int, v)) for k, v in author['positive_shifted_coefficients'].items()},
                'author shifted coefficient match')
    raw = json.dumps(result, indent=2) + '\n'
    if args.check:
        require(raw == args.check.read_text(), 'complete expected output mismatch')
    print(raw, end='')


if __name__ == '__main__':
    main()
