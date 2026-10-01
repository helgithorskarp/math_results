#!/usr/bin/env python3
"""Independent exact checks of the analytic Book root-defect theorem.

Standard library only. No host enumeration, author input, or solver premise.
The written proof in REVIEW.md establishes completeness and the host bridge.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def action(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def determinant(a):
    """Leibniz expansion with subset dynamic programming; no elimination."""
    n = len(a)
    need(n <= 16 and all(len(row) == n for row in a), 'determinant domain/size')
    need(all(type(x) is int or isinstance(x, Q) for row in a for x in row), 'exact entries')
    dp = [0] * (1 << n)
    dp[0] = 1
    for mask in range((1 << n)-1):
        k = mask.bit_count()
        if not dp[mask]:
            continue
        for j in range(n):
            if mask >> j & 1 or not a[k][j]:
                continue
            inversions = k - (mask & ((1 << j)-1)).bit_count()
            dp[mask | (1 << j)] += (-1 if inversions % 2 else 1) * dp[mask] * a[k][j]
    return dp[-1]


def binary_rank(a):
    rows = [sum((x % 2) << j for j, x in enumerate(row)) for row in a]
    pivots = {}
    for word in rows:
        while word:
            p = word.bit_length()-1
            if p not in pivots:
                pivots[p] = word
                break
            word ^= pivots[p]
    return len(pivots)


def classes(m):
    return list(range(m)), list(range(m, 2*m-2)), list(range(2*m-2, 22))


def forced_form(m, weights):
    a, c, b = classes(m)
    leaves = [b[3*i:3*i+3] for i in range(3)]
    centers = b[9:12]
    rem = b[12:]
    f = [[0]*22 for _ in range(22)]
    for i, j in combinations(centers, 2):
        f[i][j] = f[j][i] = 1
    for center, triple in zip(centers, leaves):
        for leaf in triple:
            f[center][leaf] = f[leaf][center] = 1
    if m == 4:
        need(len(weights) == 3 and sum(weights) == 3 and min(weights) >= 0, 'small cubic parameters')
        x, y, z = weights
        for (i, j), weight in zip(combinations(rem, 2), (x, y, z, z, y, x)):
            f[i][j] = f[j][i] = weight
    elif m == 5:
        need(not weights, 'unexpected small parameters')
        f[rem[0]][rem[1]] = f[rem[1]][rem[0]] = 3
    else:
        need(m == 6 and not weights, 'histogram domain')
    u = [int(i in a) for i in range(22)]
    v = [int(i in c) for i in range(22)]
    normalized = [[4-u[i]-u[j]+v[i]+v[j]-f[i][j]+int(i == j)*(u[i]+v[i])
                   for j in range(22)] for i in range(22)]
    h = [[4*normalized[i][j]+21*int(i == j) for j in range(22)] for i in range(22)]
    return f, h, normalized, leaves, centers, rem


def form_audit(m, weights):
    f, h, normalized, leaves, centers, rem = forced_form(m, weights)
    a, c, b = classes(m)
    need([sum(f[i]) for i in b] == [1]*9+[5]*3+[3]*len(rem), 'forced row weights')
    delta = [0]*9+[2]*3+[1]*len(rem)
    need([sum(f[i][j]*(1+delta[b.index(j)]) for j in b) for i in b]
         == [3*(1+x) for x in delta], 'positive eigenvector')
    vectors = []
    for triple in leaves:
        for x, y in zip(triple, triple[1:]):
            z = [0]*22
            z[x], z[y] = 1, -1
            need(action(normalized, z) == [0]*22, 'literal leaf direction')
            vectors.append(z)
    need(binary_rank(normalized) == 16, 'full rank over F2')
    keep = [i for i in range(22) if i not in {j for t in leaves for j in t[1:]}]
    minor = [[normalized[i][j] for j in keep] for i in keep]
    exact = determinant(minor)
    wanted = 25*product_of([2*w-3 for w in weights]) if m == 4 else (-255 if m == 5 else 59)
    need(exact == wanted and exact % 2 == 1, 'closed odd minor formula')
    gram = [[sum(x*y for x, y in zip(v1, v2)) for v2 in vectors] for v1 in vectors]
    need(determinant(gram) == 27, 'full leaf lattice Gram')
    cc = m-2
    coupling = [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
    margins = [m, -Q(12-2*m, 3), cc]
    schur = [[int(i == j)+coupling[i][j]*margins[j] for j in range(3)] for i in range(3)]
    schur_det = determinant(schur)
    need(schur_det == {4: -Q(25, 3), 5: -Q(85, 3), 6: -59}[m], 'determinant lemma scalar')
    return {'m': m, 'weights': list(weights), 'F_sha256': digest(f), 'H_sha256': digest(h),
            'normalized_minor_determinant': exact, 'rank_mod2': 16, 'leaf_kernel_dimension': 6,
            'Gram_determinant': 27, 'Schur_determinant': str(schur_det)}


def product_of(items):
    value = 1
    for x in items:
        value *= x
    return value


def havel_hakimi(m):
    a, c, b = classes(m)
    remaining = [8 if i in a else 10 if i in c else 9 for i in range(22)]
    rows = [set() for _ in range(22)]
    while any(remaining):
        order = sorted(range(22), key=lambda i: (-remaining[i], i))
        i = order[0]
        amount = remaining[i]
        need(amount <= len(order)-1, 'graphical degree sequence')
        remaining[i] = 0
        for j in order[1:amount+1]:
            need(remaining[j] > 0 and j not in rows[i], 'HH step')
            rows[i].add(j)
            rows[j].add(i)
            remaining[j] -= 1
    return rows


def graph_audit(rows, m):
    n = len(rows)
    a, c, b = classes(m)
    d = [len(row) for row in rows]
    need(d == [8]*m+[10]*(m-2)+[9]*(24-2*m), 'control degree histogram')
    r = [[int(j in rows[i]) for j in range(n)] for i in range(n)]
    need(all(not r[i][i] and r[i][j] == r[j][i] for i in range(n) for j in range(n)), 'simple control')
    f = [[0]*n for _ in range(n)]
    codegrees = [[0]*n for _ in range(n)]
    all_vertices = set(range(n))
    for i, j in combinations(range(n), 2):
        common_red = len(rows[i] & rows[j])
        common_blue = len((all_vertices-rows[i]-{i}) & (all_vertices-rows[j]-{j}))
        value = 3-common_red if r[i][j] else 6-common_blue
        f[i][j] = f[j][i] = value
        codegrees[i][j] = codegrees[j][i] = common_red
        need(common_red == d[i]+d[j]-14+(17-d[i]-d[j])*r[i][j]-value, 'codegree identity')
    total = [sum(row) for row in f]
    u, v = [int(i in a) for i in range(n)], [int(i in c) for i in range(n)]
    h, k = action(r, u), action(r, v)
    need(total == [1-3*u[i]+v[i]+2*(h[i]-k[i]) for i in range(n)], 'incident identity')
    K = [[2*r[i][j]+int(i == j)*(2*d[i]-17) for j in range(n)] for i in range(n)]
    H = matmul(K, K)
    need(H == [[21*int(i == j)+16-4*(u[i]+u[j])+4*(v[i]+v[j])
                +4*int(i == j)*(u[i]+v[i])-4*f[i][j] for j in range(n)] for i in range(n)], 'entire square')
    Fu, Fv = action(f, u), action(f, v)
    ra, rc = sum(total[i] for i in a), sum(total[i] for i in c)
    p = [1+h[i]-k[i]-2*u[i] for i in range(n)]
    error = action(K, [Fu[i]-Fv[i] for i in range(n)])
    fp = action(f, p)
    need([2*(fp[i]-3*p[i]) for i in range(n)]
         == [(u[i]+v[i])*total[i]-ra+rc+error[i]-3*(Fu[i]-Fv[i]) for i in range(n)], 'unsaturated error identity')
    ea = sum(r[i][j] for i, j in combinations(a, 2))
    ec = sum(r[i][j] for i, j in combinations(c, 2))
    need(ra+rc == -4+4*(ea-ec), 'root budget identity')
    need(sum(total) == 60-6*m, 'total defect')
    need(all((total[i]-d[i]) % 2 == 0 for i in range(n)), 'signed parity')
    leaf_triples = [b[3*i:3*i+3] for i in range(3)]
    lhs = sum(Q(2, 3)*K[i][i] for t in leaf_triples for i in t)
    lhs -= sum(Q(K[i][j]+K[j][i], 3) for t in leaf_triples for i, j in combinations(t, 2))
    edges = sum(r[i][j] for t in leaf_triples for i, j in combinations(t, 2))
    need(lhs == 6-Q(4, 3)*edges, 'literal K projection trace')
    return digest(r), all(f[i][j] >= 0 for i, j in combinations(range(n), 2))


def graph_controls():
    records = []
    valid = 0
    for m in (4, 5, 6):
        rows = havel_hakimi(m)
        for sample in range(16):
            h, is_valid = graph_audit(rows, m)
            records.append([m, sample, h])
            valid += is_valid
            # A deterministic degree-preserving switch; these are validation samples.
            edges = list(combinations(range(22), 2))
            chosen = None
            for offset in range(len(edges)):
                i, j = edges[(offset+17*sample) % len(edges)]
                if j not in rows[i]:
                    continue
                for x, y in edges:
                    if len({i, j, x, y}) != 4 or y not in rows[x]:
                        continue
                    if x not in rows[i] and y not in rows[j]:
                        chosen = i, j, x, y
                        break
                if chosen:
                    break
            need(chosen is not None, 'switch exists')
            i, j, x, y = chosen
            for first, second in [(i, j), (x, y)]:
                rows[first].remove(second)
                rows[second].remove(first)
            for first, second in [(i, x), (j, y)]:
                rows[first].add(second)
                rows[second].add(first)
    need(valid == 0, 'signed controls are not host constructions')
    return {'graphs': len(records), 'distinct_graphs': len({x[2] for x in records}),
            'stream_sha256': digest(records), 'valid_book_hosts': valid,
            'off_diagonal_pairs': 48*231, 'square_entries': 48*484,
            'incident_rows': 48*22, 'unsaturated_error_rows': 48*22, 'root_budgets': 48}


def controls():
    # Definition-level determinant comparison on 625 signed two-by-two matrices.
    for a, b, c, d in product(range(-2, 3), repeat=4):
        need(determinant([[a, b], [c, d]]) == a*d-b*c, 'literal 2x2 determinant')
    # The entire eigenspace matters: removing the cubic remainder creates three extra directions.
    f, h, normalized, leaves, centers, rem = forced_form(4, (1, 1, 1))
    for i, j in combinations(rem, 2):
        normalized[i][j] += f[i][j]
        normalized[j][i] += f[j][i]
    need(normalized == [list(row) for row in zip(*normalized)], 'symmetric missing-block control')
    for first, second in zip(rem, rem[1:]):
        vector = [0]*22
        vector[first], vector[second] = 1, -1
        need(action(normalized, vector) == [0]*22, 'three additional missing-block directions')
    missing_rank = binary_rank(normalized)
    need(missing_rank <= 13, 'missing cubic block destroys full six-dimensional kernel')
    # A rational symmetric square root exists on one contrast plane when parity is relaxed.
    X = [[1, 0], [-1, 1], [0, -1]]
    Ginv = [[Q(2, 3), Q(1, 3)], [Q(1, 3), Q(2, 3)]]
    S = [[1, 4], [5, -1]]
    Xt = [list(row) for row in zip(*X)]
    T = matmul(matmul(matmul(X, S), Ginv), Xt)
    P = [[Q(int(i == j))-Q(1, 3) for j in range(3)] for i in range(3)]
    need(T == [list(row) for row in zip(*T)], 'symmetric contrast root')
    need(matmul(T, T) == [[21*x for x in row] for row in P], 'contrast square root')
    need(sum(T[i][i] for i in range(3)) == 0, 'rational trace zero')
    need(2*sum(T[i][i] for i in range(3)) == sum(T[i][j] for i in range(3) for j in range(3) if i != j), 'projection trace equation')
    need(not (all(x.denominator == 1 and x.numerator % 2 for x in [T[i][i] for i in range(3)])
              and all((T[i][j]+T[j][i]).denominator == 1 and (T[i][j]+T[j][i]).numerator % 4 == 0
                      for i, j in combinations(range(3), 2))), 'essential parity fails on positive root')
    nonsymmetric = matmul(matmul(matmul(X, [[0, 21], [1, 0]]), Ginv), Xt)
    need(nonsymmetric != [list(row) for row in zip(*nonsymmetric)], 'actual nonsymmetric control')
    need(matmul(nonsymmetric, nonsymmetric) == [[21*x for x in row] for row in P], 'nonsymmetric contrast root')
    need(2*sum(nonsymmetric[i][i] for i in range(3))
         == sum(nonsymmetric[i][j] for i in range(3) for j in range(3) if i != j), 'nonsymmetric trace condition')
    relabels = 0
    for m in (4, 5, 6):
        _, _, N, _, _, _ = forced_form(m, (0, 1, 2) if m == 4 else ())
        for shift in range(8):
            permutation = [(7*i+shift) % 22 for i in range(22)]
            need(binary_rank([[N[i][j] for j in permutation] for i in permutation]) == 16, 'rank survives actual relabeling')
            relabels += 1
    return {'signed_2x2_determinants': 625, 'relabelings': relabels,
            'missing_cubic_rank_mod2': missing_rank, 'contrast_positive_root': [[str(x) for x in row] for row in T],
            'nonsymmetric_positive_root': [[str(x) for x in row] for row in nonsymmetric],
            'all_passed': True}


def baseline():
    strings = Path(__file__).with_name('baseline21.rows').read_text().splitlines()
    need(len(strings) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in strings), 'baseline encoding')
    rows = [{j for j, value in enumerate(row) if value == '1'} for row in strings]
    need(all(i not in rows[i] and ((j in rows[i]) == (i in rows[j])) for i in range(21) for j in range(21)), 'simple baseline')
    red, blue = [], []
    universe = set(range(21))
    for i, j in combinations(range(21), 2):
        if j in rows[i]:
            red.append(len(rows[i] & rows[j]))
        else:
            blue.append(len((universe-rows[i]-{i}) & (universe-rows[j]-{j})))
    need((len(red), max(red), max(blue)) == (93, 3, 6), 'known positive book fixture')
    return {'vertices': 21, 'red_edges': len(red), 'red_page_maximum': max(red), 'blue_page_maximum': max(blue)}


def run():
    forms = []
    for m in (4, 5, 6):
        weights = [(x, y, 3-x-y) for x in range(4) for y in range(4-x)] if m == 4 else [()]
        forms.extend(form_audit(m, w) for w in weights)
    need(len(forms) == 12, 'complete parameter domain')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'method': 'analytic proof; normalized principal minor, F2 rank, subset determinant, local rational-root trace',
            'forms': forms, 'signed_controls': graph_controls(), 'controls': controls(),
            'known_baseline': baseline(), 'all_passed': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    output = run()
    if args.expected:
        need(output == json.loads(args.expected.read_text()), 'compact expected record mismatch')
    print(json.dumps(output, indent=2, sort_keys=True))
