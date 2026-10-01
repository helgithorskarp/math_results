#!/usr/bin/env python3
"""Standalone exact checker; --full-psd also eliminates both full slacks.

six-downset-3, researcher. The all-order reduction is ordinary mathematics
in PROOF.md. No float, CAS, numerical optimizer or external dataset is used.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import comb, lcm
from pathlib import Path

from matrices import construct, parameters, rational, require


def psd_rank(a):
    """Positive integer Bareiss pivots; exact Schur test including zero residuals.

    This arithmetic mechanism is reused from the credited graph7980 checker.
    The negative controls also compare it to principal-minor definitions.
    """
    require(a and all(len(row) == len(a) for row in a), 'PSD shape')
    d = 1
    for row in a:
        for value in row:
            d = lcm(d, rational(value).denominator)
    z = [[int(rational(value)*d) for value in row] for row in a]
    n = len(z)
    require(all(z[i][j] == z[j][i] for i in range(n) for j in range(n)), 'PSD asymmetry')
    previous, rank = 1, 0
    for k in range(n):
        require(all(z[i][i] >= 0 for i in range(k, n)), 'negative Schur diagonal')
        pivot_row = next((i for i in range(k, n) if z[i][i] > 0), None)
        if pivot_row is None:
            require(all(z[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                    'zero diagonal with nonzero residual')
            break
        if pivot_row != k:
            z[k], z[pivot_row] = z[pivot_row], z[k]
            for row in z:
                row[k], row[pivot_row] = row[pivot_row], row[k]
        pivot = z[k][k]
        for i in range(k+1, n):
            for j in range(i, n):
                value = pivot*z[i][j]-z[i][k]*z[k][j]
                require(value % previous == 0, 'nonexact Bareiss division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, n):
            z[i][k] = z[k][i] = 0
        previous = pivot
        rank += 1
    return rank


def inverse(a):
    n = len(a)
    b = [[rational(x) for x in row]+[Q(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    require(n and all(len(row) == 2*n for row in b), 'inverse shape')
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        require(pivot is not None, 'singular inverse')
        b[j], b[pivot] = b[pivot], b[j]
        scale = b[j][j]
        b[j] = [x/scale for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x-scale*y for x, y in zip(b[i], b[j])]
    result = [row[n:] for row in b]
    require(all(sum(a[i][k]*result[k][j] for k in range(n)) == (i == j)
                for i in range(n) for j in range(n)), 'inverse residual')
    return result


def matrix_hash(a):
    return sha256(json.dumps([[str(rational(x)) for x in row] for row in a],
                             separators=(',', ':')).encode()).hexdigest()


def reference_lift(n, z, epsilon, members):
    """Construct every full entry from middle Q and the forced-star lift.

    Does not call the production closed-entry formulas or their completion.
    """
    N, s, full = len(members), 2**(n-1)-n, (1 << n)-1
    middle = [a for a in members if a.bit_count() >= 2]
    core = []
    for a in middle:
        row = []
        for b in middle:
            value = Q(s-1) if a == b else Q(-1)
            if b == (full ^ a):
                value += s-z[a.bit_count()]
            elif not a & b and a.bit_count() == b.bit_count() == 2:
                value += epsilon
            row.append(value)
        core.append(row)
    incidence = [[j for j, a in enumerate(middle) if a >> i & 1] for i in range(n)]
    rq = [[sum(core[j][k] for j in incidence[i]) for k in range(len(middle))]
          for i in range(n)]
    index = {a: i for i, a in enumerate(members)}
    L = [[Q(0) for _ in members] for _ in members]
    for i, a in enumerate(middle):
        for j, b in enumerate(middle):
            L[index[a]][index[b]] = core[i][j]+1
        for point in range(n):
            L[index[1 << point]][index[a]] = L[index[a]][index[1 << point]] = 1-rq[point][i]
    for i in range(n):
        for j in range(n):
            L[index[1 << i]][index[1 << j]] = 1+sum(rq[i][k] for k in incidence[j])
    for i in range(1, N):
        L[0][i] = L[i][0] = N-sum(L[i][1:])
    L[0][0] = N-sum(L[0][1:])
    return L, middle, core


def blocks(n, z, epsilon):
    layers = list(range(2, n-1))
    d = len(layers)
    N, s = 2**n-n-1, 2**(n-1)-n
    b = [comb(n, k) for k in layers]
    alpha = [comb(n-2, k-1) for k in layers]
    g0 = [[Q(b[i] if i == j else 0)+Q(k*l*b[i]*b[j], n)
           +(k-1)*(l-1)*b[i]*b[j] for j, l in enumerate(layers)] for i, k in enumerate(layers)]
    g1 = [[Q(alpha[i] if i == j else 0)+alpha[i]*alpha[j]
           for j in range(d)] for i in range(d)]
    q0 = [[Q(s*b[i] if i == j else 0)-b[i]*b[j]
           for j in range(d)] for i in range(d)]
    q1 = [[Q(s*alpha[i] if i == j else 0) for j in range(d)] for i in range(d)]
    for i, k in enumerate(layers):
        j = layers.index(n-k)
        q0[i][j] += b[i]*(s-z[k])
        q1[i][j] -= alpha[i]*(s-z[k])
    q0[0][0] += comb(n-2, 2)*b[0]*epsilon
    q1[0][0] -= (n-3)*alpha[0]*epsilon
    inv0, inv1 = inverse(g0), inverse(g1)
    u0 = [[N*b[i]*b[j]*inv0[i][j]-q0[i][j] for j in range(d)] for i in range(d)]
    u1 = [[N*alpha[i]*alpha[j]*inv1[i][j]-q1[i][j] for j in range(d)] for i in range(d)]
    q2 = [[s+epsilon, s-z[2]], [s-z[2], Q(s)]]
    u2 = [[Q(N if i == j else 0)-q2[i][j] for j in range(2)] for i in range(2)]
    return {'Q0': q0, 'Q1': q1, 'U0': u0, 'U1': u1, 'B2': q2, 'U2': u2}, g0, g1


def literal_block_checks(n, middle, core, g0, g1, expected):
    layers = list(range(2, n-1)); d = len(layers)
    sizes = [layers.index(a.bit_count()) for a in middle]
    signs = [int(bool(a & 1))-int(bool(a & 2)) for a in middle]
    literal0 = [[Q(0) for _ in layers] for _ in layers]
    literal1 = [[Q(0) for _ in layers] for _ in layers]
    for i, a in enumerate(middle):
        for j, b in enumerate(middle):
            literal0[sizes[i]][sizes[j]] += core[i][j]
            literal1[sizes[i]][sizes[j]] += signs[i]*signs[j]*core[i][j]
    require(literal0 == expected['Q0'], 'constant Q block differs')
    require(literal1 == [[2*x for x in row] for row in expected['Q1']], 'standard Q block differs')
    images0, images1 = [], []
    for k in layers:
        group = [i for i, a in enumerate(middle) if a.bit_count() == k]
        images0.append([sum(middle[i].bit_count()-1 for i in group)]
                       +[-sum(int(bool(middle[i] >> point & 1)) for i in group) for point in range(n)]
                       +[int(i in group) for i in range(len(middle))])
        images1.append([sum((k-1)*signs[i] for i in group)]
                       +[-sum(signs[i] for i in group if middle[i] >> point & 1) for point in range(n)]
                       +[signs[i] if i in group else 0 for i in range(len(middle))])
    gram = lambda vectors: [[sum(x*y for x, y in zip(a, b)) for b in vectors] for a in vectors]
    require(gram(images0) == g0, 'constant Gram block differs')
    require(gram(images1) == [[2*x for x in row] for row in g1], 'standard Gram block differs')
    return 4*d*d


def interval(n, z):
    zero, _, _ = blocks(n, z, Q(0)); one, _, _ = blocks(n, z, Q(1))
    lower, upper, detail = {'positive_epsilon': Q(0)}, {}, {}
    for name, a in zero.items():
        rest = [row[1:] for row in a[1:]]
        require(psd_rank(rest) == len(rest), 'interval requires positive definite principal remainder')
        inv = inverse(rest); cross = a[0][1:]
        constant = a[0][0]-sum(cross[i]*inv[i][j]*cross[j] for i in range(len(cross)) for j in range(len(cross)))
        slope = one[name][0][0]-a[0][0]
        require(slope != 0 and all(one[name][i][j] == a[i][j]
                for i in range(len(a)) for j in range(len(a)) if (i, j) != (0, 0)), 'interval affine support')
        endpoint = -constant/slope
        (lower if slope > 0 else upper)[name] = endpoint
        detail[name] = {'constant': str(constant), 'slope': str(slope), 'endpoint': str(endpoint)}
    return max(lower.values()), min(upper.values()), detail


def check_definition(n, members, L):
    N, s = len(members), 2**(n-1)-n
    require(N == 2**n-n-1 and members[0] == 0, 'complete canonical vertex set')
    for i, a in enumerate(members):
        require(sum(L[i]) == N, 'row normalization')
        require(a == 0 or L[i][i] == s, 'nonempty diagonal')
        for j, b in enumerate(members):
            require(L[i][j] == L[j][i], 'symmetry')
            require(i == j or not a & b or L[i][j] == 0, 'intersecting support')
        for point in range(n):
            require(sum(L[i][j] for j, b in enumerate(members) if b >> point & 1) == s, 'forced star equation')
    star_gram = [[sum(int(bool(a >> i & 1) and bool(a >> j & 1)) for a in members)-Q(s*s, N)
                  for j in range(n)] for i in range(n)]
    require(psd_rank(star_gram) == n, 'centered stars independent')


def incidence_controls():
    result = []
    for n in range(6, 11):
        members = [a for a in range(1 << n) if 2 <= a.bit_count() <= n-2]
        residual = 0
        for k in range(2, n-1):
            layer = [a for a in members if a.bit_count() == k]
            gram = [[sum(int(bool(a >> i & 1) and bool(a >> j & 1)) for a in layer)
                     for j in range(n)] for i in range(n)]
            require(all(gram[i][j] == (comb(n-1, k-1) if i == j else comb(n-2, k-2))
                        for i in range(n) for j in range(n)), 'literal incidence Gram')
            require(psd_rank(gram) == n, 'layer incidence rank')
            residual += len(layer)-n
        pairs = [a for a in members if a.bit_count() == 2]
        for a in pairs:
            for b in pairs:
                require(int(not a & b) == int(a == b)-(a & b).bit_count()+1, 'pair adjacency identity')
        require(n*(n-3)+residual == len(members), 'complete subspace dimensions')
        result.append({'n': n, 'middle': len(members), 'constant_dimension': n-3,
                       'standard_dimension': (n-1)*(n-3), 'residual_dimension': residual,
                       'pair_adjacency_entries': len(pairs)**2})
    return result


def negative_controls():
    rejected = []
    def reject(name, function):
        try:
            function()
        except (ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('corrupt input accepted: '+name)
    reject('float_coefficient', lambda: rational(0.4))
    reject('decimal_coefficient', lambda: rational('0.4'))
    reject('invalid_order', lambda: construct(5, {2: 1}, 0))
    reject('missing_layer', lambda: construct(8, {2: 6, 3: '179/100'}, '37/25'))
    reject('extra_layer', lambda: construct(7, {2: 2, 3: 2, 4: 2}, 1))
    reject('indefinite_zero_diagonal', lambda: psd_rank([[0, 1], [1, 0]]))
    reject('asymmetric_PSD_input', lambda: psd_rank([[1, 1], [0, 1]]))
    z, _ = parameters(7, {2: '12/5', 3: '12/5'}, '2/5')
    bad, _, _ = blocks(7, z, Q(0))
    reject('removed_extra_orbit', lambda: psd_rank(bad['Q0']))
    members, L = construct(6, {2: '9/4', 3: '9/4'}, '1/4')
    L[1][3] = L[3][1] = Q(1)
    reject('corrupted_intersecting_entry', lambda: check_definition(6, members, L))
    psd_count = 0
    for entries in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = entries
        matrix = [[a, b, c], [b, d, e], [c, e, f]]
        expected = (a >= 0 and d >= 0 and f >= 0 and a*d-b*b >= 0
                    and a*f-c*c >= 0 and d*f-e*e >= 0
                    and a*(d*f-e*e)-b*(b*f-c*e)+c*(b*e-c*d) >= 0)
        try:
            psd_rank(matrix); actual = True
        except ValueError:
            actual = False
        require(actual == expected, 'PSD engine differs from all principal minors')
        psd_count += actual
    return rejected, {'ternary_symmetric_3x3': 729, 'PSD_count': psd_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--full-psd', action='store_true')
    parser.add_argument('--full-output', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    fixture = json.loads((root/'CERTIFICATES.json').read_text())
    records, full_records = [], []
    for case in fixture['cases']:
        n = case['n']; z, epsilon = parameters(n, case['z'], case['epsilon'])
        members, L = construct(n, case['z'], case['epsilon'])
        reference, middle, core = reference_lift(n, z, epsilon, members)
        require(L == reference, 'closed full matrix differs from forced-face lift')
        check_definition(n, members, L)
        require(matrix_hash(L) == case['L_sha256'], 'literal matrix fingerprint')
        sector, g0, g1 = blocks(n, z, epsilon)
        ranks = {name: psd_rank(a) for name, a in sector.items()}
        require(all(ranks[name] == len(a) for name, a in sector.items()), 'strict sector positivity')
        require(all(0 < z[k] < 2*(2**(n-1)-n) for k in range(3, n//2+1)), 'residual strict scalar bounds')
        entries = literal_block_checks(n, middle, core, g0, g1, sector)
        lo, hi, thresholds = interval(n, z)
        require(lo < epsilon < hi, 'epsilon outside strict Schur interval')
        N, s = len(members), 2**(n-1)-n
        require(case['lower_rank'] == N-n and case['upper_rank'] == N-1, 'claimed rank mismatch')
        record = {'n': n, 'N': N, 's': s, 'z': case['z'], 'epsilon': str(epsilon),
                  'lower_rank': N-n, 'upper_rank': N-1, 'L_sha256': matrix_hash(L),
                  'literal_full_entries': N*N, 'literal_sector_Gram_entries': entries,
                  'sector_ranks': ranks, 'epsilon_interval': {'lower': str(lo), 'upper': str(hi),
                  'thresholds': thresholds}}
        records.append(record)
        if args.full_psd:
            lower = psd_rank(L)
            upper = psd_rank([[Q(N if i == j else 0)-L[i][j] for j in range(N)] for i in range(N)])
            require(lower == N-n and upper == N-1, 'independent full PSD/rank mismatch')
            full_records.append({'n': n, 'N': N, 'lower_rank': lower,
                                 'upper_rank': upper, 'L_sha256': matrix_hash(L)})
    rejected, backend = negative_controls()
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'proof_status': 'Author-checked unformalized all-order reduction and exact finite certificates; not independently reviewed.',
              'cases': records, 'incidence_controls': incidence_controls(),
              'negative_controls': rejected, 'PSD_backend_controls': backend,
              'trust_boundary': 'Default checks the full literal matrices and six strict reduced PSD blocks. Complete reduction is written in PROOF.md. Optional full elimination is independent of that reduction.'}
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
    if args.full_psd:
        full = {'agent': 'six-downset-3', 'role': 'researcher',
                'method': 'Exact positive-pivot integer Bareiss elimination of both complete slacks.',
                'cases': full_records}
        if args.full_output:
            args.full_output.write_text(json.dumps(full, indent=2)+'\n')
        else:
            print(json.dumps(full, indent=2))


if __name__ == '__main__':
    main()
