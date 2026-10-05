"""Literal affine-action audit; no author code/data, no floating point or solver.

The coefficients are formal independent variables, not a sampled certificate.
Each basis vector lies in one orbit. Its image therefore contains at most one
coefficient per original coordinate. Checks use explicit errors, surviving -O.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, lcm, isqrt
import hashlib
import json
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def rank_mod(rows, p=1009):
    need(p >= 2 and all(p % d for d in range(2, isqrt(p) + 1)), 'modular rank prime')
    a = [[v % p for v in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, p)
        a[rank] = [v * inv % p for v in a[rank]]
        for i in range(rank + 1, len(a)):
            if a[i][col]:
                factor = a[i][col]
                a[i] = [(v - factor * w) % p for v, w in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def pair_kernel(n):
    pairs = list(combinations(range(n), 2))
    a = [[Fraction(int(i in pair)) for pair in pairs] for i in range(n)]
    pivots = []
    row = 0
    for col in range(len(pairs)):
        pivot = next((i for i in range(row, n) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(n):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == n:
            break
    need(row == (1 if n == 2 else n), 'unsigned pair incidence rank, including K2 boundary')
    answer = []
    for col in range(len(pairs)):
        if col in pivots:
            continue
        v = [Fraction(0)] * len(pairs)
        v[col] = Fraction(1)
        for i, pivot in enumerate(pivots):
            v[pivot] = -a[i][col]
        scale = lcm(*(x.denominator for x in v))
        ints = [int(x * scale) for x in v]
        need(all(sum(ints[j] for j, pair in enumerate(pairs) if i in pair) == 0
                 for i in range(n)), 'kernel original incidence')
        answer.append(dict(zip(pairs, ints)))
    need(len(answer) == max(0, n * (n - 3) // 2), 'kernel dimension')
    return answer


def carrier(k, m):
    ground = range(3 + k + m)
    vertices = [frozenset(c) for size in range(3) for c in combinations(ground, size)]
    vertices.append(frozenset((0, 1, 2)))
    for x in range(3, 3 + k + m):
        vertices.extend((frozenset((0, 1, x)), frozenset((0, 2, x))))
        if x >= 3 + k:
            vertices.append(frozenset((1, 2, x)))
    need(len(vertices) == len(set(vertices)), 'literal carrier uniqueness')
    return sorted(vertices, key=lambda a: (len(a), tuple(sorted(a))))


def audit(k, m, damage=None):
    need(k >= 2 and m >= 2, 'declared boundary domain')
    V = carrier(k, m)
    N = len(V)
    s = sum(0 in v for v in V)
    h = N - s
    need((N, s) == (((k + m) ** 2 + 13 * (k + m) + 16) // 2 - k,
                    3 * (k + m) + 4), 'original counts')
    Q = [v for v in V if v not in (frozenset(), frozenset((0,)))]
    n = len(Q)
    types_of = [(sum(1 << i for i in a if i < 3),
                 sum(3 <= i < 3 + k for i in a), sum(i >= 3 + k for i in a)) for a in Q]
    types = sorted(set(types_of))
    need(len(types) == 22, 'twenty-two literal orbits')
    orbit = [[i for i, t in enumerate(types_of) if t == u] for u in types]
    w = [len(o) for o in orbit]
    r = [int(0 in a) for a in Q]
    b = [1 - x for x in r]
    ti = [types.index(t) for t in types_of]
    disjoint = [[not (a & c) for c in Q] for a in Q]
    formal_pairs = [(i, j) for i, t in enumerate(types) for j, u in enumerate(types)
                    if i <= j and not t[0] & u[0]]
    # A core-disjoint pair may nevertheless be impossible at low counts.
    formal_pairs = [(i, j) for i, j in formal_pairs
                    if types[i][1] + types[j][1] <= 4
                    and types[i][2] + types[j][2] <= 4]
    # This is the list of active pairs at generic counts >= 4.
    need(len(formal_pairs) == 143, 'generic parameter census')
    index = {pair: z for z, pair in enumerate(formal_pairs)}
    d = [[choose(k - t[1], u[1]) * choose(m - t[2], u[2])
          if not t[0] & u[0] else 0 for u in types] for t in types]
    if damage == 'count':
        d[0][0] += 1
    for i, o in enumerate(orbit):
        need(w[i] == choose(k, types[i][1]) * choose(m, types[i][2]), 'orbit metric')
        for a in o:
            for j, oo in enumerate(orbit):
                need(sum(disjoint[a][c] for c in oo) == d[i][j], 'every original disjoint incidence')

    basis = []

    def put(sector, t, values, auxiliary=None):
        sparse = {a: value for a, value in zip(orbit[t], values) if value}
        need(sparse, 'nonzero literal basis vector')
        basis.append(dict(sector=sector, orbit=t, sparse=sparse, auxiliary=auxiliary))

    for t, o in enumerate(orbit):
        put('constant', t, [1] * len(o))
    for sector, start, size, slot in (('X', 3, k, 1), ('Y', 3 + k, m, 2)):
        for t, o in enumerate(orbit):
            if types[t][slot] == 0 or (size == 2 and types[t][slot] == 2):
                continue
            for z in range(size - 1):
                f = [int(i == z) - int(i == size - 1) for i in range(size)]
                put(sector, t, [sum(f[i - start] for i in Q[a] if start <= i < start + size)
                                for a in o], f)
    for sector, start, size, wanted in (('XX', 3, k, (0, 2, 0)),
                                       ('YY', 3 + k, m, (0, 0, 2))):
        t = types.index(wanted)
        for kernel in pair_kernel(size):
            put(sector, t, [kernel[tuple(sorted(i - start for i in Q[a]))] for a in orbit[t]])
    t = types.index((0, 1, 1))
    for x in range(k - 1):
        for y in range(m - 1):
            put('XY', t, [(int(3 + x in Q[a]) - int(3 + k - 1 in Q[a])) *
                          (int(3 + k + y in Q[a]) - int(3 + k + m - 1 in Q[a]))
                          for a in orbit[t]])
    need(len(basis) == n, 'full square physical basis')
    if damage == 'basis':
        basis[-1] = basis[-2]
    dense = [[v['sparse'].get(a, 0) for v in basis] for a in range(n)]
    need(rank_mod(dense) == n, 'complete basis determinant nonzero modulo 1009')
    if damage == 'metric':
        w[0] += 1
    gram_checks = 0
    for v in basis:
        for u in basis:
            gram = sum(value * u['sparse'].get(a, 0) for a, value in v['sparse'].items())
            if v['sector'] != u['sector'] or v['orbit'] != u['orbit']:
                expected = 0
            elif v['sector'] == 'constant':
                expected = w[v['orbit']]
            elif v['sector'] in ('X', 'Y'):
                mask, i, j = types[v['orbit']]
                metric = choose(k - 2, i - 1) * choose(m, j) if v['sector'] == 'X' else \
                         choose(k, i) * choose(m - 2, j - 1)
                expected = metric * sum(x * y for x, y in zip(v['auxiliary'], u['auxiliary']))
            else:
                # The three harmonic sectors have the actual Euclidean metric.
                expected = gram
            need(gram == expected, 'every cross-sector and declared standard Gram entry')
            gram_checks += 1

    action_checks = 0
    formal_action_digest = hashlib.sha256()
    for v in basis:
        u = v['orbit']
        mu, iu, ju = types[u]
        vsum = sum(v['sparse'].values())
        for a in range(n):
            t = ti[a]
            mt, it, jt = types[t]
            ds = sum(value for c, value in v['sparse'].items() if disjoint[a][c])
            value = v['sparse'].get(a, 0)
            actual_constant = s * value - vsum + ds
            if v['sector'] == 'constant':
                predicted_ds = d[t][u]
                expected_constant = s * int(t == u) - w[u] + predicted_ds
            elif v['sector'] in ('X', 'Y'):
                if v['sector'] == 'X':
                    fvalue = sum(v['auxiliary'][x - 3] for x in Q[a] if 3 <= x < 3 + k)
                    coefficient = -choose(k - it - 1, iu - 1) * choose(m - jt, ju)
                else:
                    fvalue = sum(v['auxiliary'][x - 3 - k] for x in Q[a] if x >= 3 + k)
                    coefficient = -choose(k - it, iu) * choose(m - jt - 1, ju - 1)
                predicted_ds = coefficient * fvalue if not mt & mu else 0
                expected_constant = s * value + predicted_ds
            else:
                predicted_ds = value  # scalar block, zero outside its orbit
                expected_constant = (s + 1) * value
            if damage == 'standard-sign' and v['sector'] == 'X':
                predicted_ds = -predicted_ds
            if damage == 'harmonic-sign' and v['sector'] in ('XX', 'YY', 'XY'):
                predicted_ds = -predicted_ds
            need(ds == predicted_ds and actual_constant == expected_constant,
                 'full symbolic physical row action, constant and coefficient separately')
            formal_id = index.get(tuple(sorted((t, u))))
            need(not ds or formal_id is not None, 'every nonzero coefficient belongs to defining parameter')
            formal_action_digest.update(json.dumps([v['sector'], u, a, actual_constant,
                                                    formal_id if ds else None, ds], separators=(',', ':')).encode())
            action_checks += 1

    denominator = lcm(s, h)
    inv = [[denominator * int(i == j) - denominator // s * r[i] * r[j]
            - denominator // h * b[i] * b[j] for j in range(n)] for i in range(n)]
    if damage == 'upper-metric':
        inv = [[denominator * int(i == j) for j in range(n)] for i in range(n)]
    inverse_checks = 0
    row_s = [sum(inv[i][j] for j in range(n) if r[j]) for i in range(n)]
    row_b = [sum(inv[i][j] for j in range(n) if b[j]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            product = inv[i][j] + row_s[i] * r[j] + row_b[i] * b[j]
            reverse = inv[i][j] + row_s[j] * r[i] + row_b[j] * b[i]
            need(product == reverse == denominator * int(i == j), 'both literal Gram-inverse products')
            inverse_checks += 2
    for v in basis:
        u = v['orbit']
        for a in range(n):
            actual = sum(inv[a][c] * value for c, value in v['sparse'].items())
            if v['sector'] == 'constant':
                sr = int(types[u][0] & 1 != 0)
                expected = denominator * int(ti[a] == u) - denominator // s * r[a] * sr * w[u] \
                           - denominator // h * b[a] * (1 - sr) * w[u]
            else:
                expected = denominator * v['sparse'].get(a, 0)
            need(actual == expected, 'full inverse-Gram basis action and trivial J0 metric')
            inverse_checks += 1

    # Entire literal original lifts at a reproducible integer coefficient vector.
    # Symbolic actions above already cover ALL real coefficient choices.
    coeff = {(i, j): ((z + 3) ** 2 * 17 + z * 7) % 97 - 48
             for z, (i, j) in enumerate(formal_pairs)}
    T = [[s - 1 if i == j else (coeff[tuple(sorted((ti[i], ti[j])))] if disjoint[i][j] else -1)
          for j in range(n)] for i in range(n)]
    proper = [v for v in V if v]
    anchor = proper.index(frozenset((0,)))
    qpos = [proper.index(v) for v in Q]
    C = [[0] * len(proper) for _ in proper]
    for i, pi in enumerate(qpos):
        for j, pj in enumerate(qpos):
            C[pi][pj] = T[i][j]
    for i, pi in enumerate(qpos):
        C[pi][anchor] = C[anchor][pi] = -sum(T[i][j] for j in range(n) if r[j])
    C[anchor][anchor] = s - 1
    need(all(sum(row[j] for j, v in enumerate(proper) if 0 in v) == 0 for row in C),
         'whole proper star kernel')
    Vlift = [frozenset()] + proper
    phi = [[int(v == a) - int(v == (frozenset((0,)) if 0 in a else frozenset())) for a in Q]
           for v in Vlift]
    csums = [sum(row) for row in C]
    total = sum(csums)
    L = [[1 + (total if i == j == 0 else -csums[j - 1] if i == 0 else
               -csums[i - 1] if j == 0 else C[i - 1][j - 1])
          for j in range(N)] for i in range(N)]
    need(all(sum(row) == N for row in L), 'actual stochastic lift row sums')
    z = [N * int(0 in v) - s for v in Vlift]
    need(sum(x * x for x in z) == N * s * h, 'centered-star norm')
    need(all(sum(L[i][j] * z[j] for j in range(N)) == 0 for i in range(N)), 'actual star kernel')
    lift_checks = 0
    nzphi = [[(j, x) for j, x in enumerate(row) if x] for row in phi]
    for i in range(N):
        for j in range(N):
            lower = sum(x * T[u][v] * y for u, x in nzphi[i] for v, y in nzphi[j])
            upper = sum(x * (N * inv[u][v] - denominator * T[u][v]) * y
                        for u, x in nzphi[i] for v, y in nzphi[j])
            need(L[i][j] == 1 + lower, 'entire independent E and Phi original lower lifts')
            need(Fraction(N * int(i == j) - L[i][j]) == Fraction(upper, denominator) +
                 Fraction(z[i] * z[j], s * h), 'entire original upper endpoint with star projector')
            metric = sum(x * inv[u][v] * y for u, x in nzphi[i] for v, y in nzphi[j])
            pu = Fraction(int(i == j)) - Fraction(1, N) - Fraction(z[i] * z[j], N * s * h)
            need(Fraction(metric, denominator) == pu, 'entire original U projector')
            gamma = Fraction(3, 7)
            window = Fraction(lower) - gamma * Fraction(metric, denominator)
            need(window == L[i][j] - 1 - gamma * pu, 'exact original spectral window lower identity')
            window_upper = Fraction(upper, denominator) - gamma * Fraction(metric, denominator)
            need(window_upper == N * int(i == j) - L[i][j] - Fraction(z[i] * z[j], s * h) - gamma * pu,
                 'exact original spectral window upper identity')
            lift_checks += 5
    active_pairs = sum(d[i][j] > 0 for i, j in formal_pairs)
    ghost = [z for z, (i, j) in enumerate(formal_pairs) if not d[i][j]]
    need(all((not d[i][j]) == (types[i][1] + types[j][1] > k or types[i][2] + types[j][2] > m)
             for i, j in formal_pairs), 'exact unused coefficients at both boundaries')
    for t, o in enumerate(orbit):
        mt, it, jt = types[t]
        predicted = h - (0 if mt & 1 else s) - sum(d[t][u] *
                    (1 + coeff[tuple(sorted((t, u)))]) for u in range(len(types))
                    if not types[u][0] & 1 and d[t][u])
        need(all(L[0][1 + qpos[a]] == predicted for a in o), 'every original empty budget')
    star_budget = s - sum(w[t] * L[0][1 + qpos[o[0]]] for t, o in enumerate(orbit) if types[t][0] & 1)
    need(L[0][anchor + 1] == star_budget, 'actual anchor budget')
    loop_budget = h - s - sum(w[t] * L[0][1 + qpos[o[0]]] for t, o in enumerate(orbit) if not types[t][0] & 1)
    need(L[0][0] - s == loop_budget, 'actual empty loop budget')
    return dict(k=k, m=m, N=N, s=s, h=h, physical_dimension=n,
                sectors={sector: sum(v['sector'] == sector for v in basis)
                         for sector in ('constant', 'X', 'Y', 'XX', 'YY', 'XY')},
                generic_parameters=143, active_parameters=active_pairs, unused_parameters=ghost,
                all_coefficient_affine_actions=action_checks, full_Gram_entries=gram_checks,
                inverse_metric_checks=inverse_checks, full_original_lift_entries=lift_checks,
                whole_affine_action_sha256=formal_action_digest.hexdigest(), basis_rank_mod1009=n,
                literal_matrix_sha256=hashlib.sha256(json.dumps(T, separators=(',', ':')).encode()).hexdigest())


def main():
    need(len(sys.argv) <= 2, 'checker argument count')
    damage = sys.argv[1] if len(sys.argv) > 1 else None
    need(damage in (None, 'count', 'basis', 'metric', 'standard-sign',
                    'harmonic-sign', 'upper-metric'), 'declared checker mode')
    cases = [(2, 2), (2, 3), (3, 2), (2, 4), (4, 2), (2, 6), (6, 2),
             (3, 3), (3, 4), (4, 3), (4, 4), (4, 5), (5, 4), (3, 6), (6, 3)]
    if damage:
        cases = [(4, 4)]
    result = dict(actual_agent='six-reviewer-5', role='independent mathematical reviewer',
                  exactness='Python arbitrary-precision integers and Fraction; symbolic independent coefficients',
                  cases=[audit(k, m, damage) for k, m in cases])
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
