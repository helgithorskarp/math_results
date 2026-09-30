#!/usr/bin/env python3
"""Exact finite validation of the written near-cube certificate proof.

Author six-downset-3, role researcher. CPython 3.11.2 standard library.
No floating point, external inputs, imported campaign code or solvers.
PROOF.md, not extrapolation from these samples, proves the all-n claims.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def form(a, v):
    return sum(v[i]*dot(row, v) for i, row in enumerate(a))


def psd_rank(matrix):
    """Exact symmetric Schur elimination with zero-pivot handling.

    The basic elimination algorithm was also used in the author's
    spectral_downset_uniform_coupling checker; no file is imported.
    Here its verdict is independently tested against principal minors.
    """
    size = len(matrix)
    require(all(len(row) == size for row in matrix), 'PSD square input')
    require(all(matrix[i][j] == matrix[j][i]
                for i in range(size) for j in range(size)), 'PSD symmetry')
    a = [[Q(x) for x in row] for row in matrix]
    rank = 0
    while a:
        require(all(a[i][i] >= 0 for i in range(len(a))), 'negative diagonal')
        pivot = next((i for i in range(len(a)) if a[i][i]), None)
        if pivot is None:
            require(all(not x for row in a for x in row),
                    'zero diagonal with nonzero image')
            break
        indices = [i for i in range(len(a)) if i != pivot]
        d = a[pivot][pivot]
        a = [[a[i][j]-a[i][pivot]*a[pivot][j]/d
              for j in indices] for i in indices]
        rank += 1
    return rank


def rejects(operation):
    try:
        operation()
    except ValueError:
        return True
    return False


def parameters(n):
    require(isinstance(n, int) and n >= 4, 'n>=4')
    p, s, N, q = 2**(n-1)-n-1, 2**(n-1)-n, 2**n-n-1, 2**(n-2)-2
    require(p == s-1 == 2*q-n+3 and N == 2*s+n-1, 'parameter identities')
    K = s*(n-2)**2-(n-1)*(n-3)
    D = (n-1)*((n-4)*q+2*(n-3))
    require(D > 0 and N-2*(q+1) == s+1 > 0, 'positive scalar bounds')
    return p, s, N, q, K, D


def vertices(n):
    p, _, N, _, _, _ = parameters(n)
    all_points = (1 << n)-1
    singles = [1 << i for i in range(n)]
    middle = [a for a in range(1 << n) if 2 <= a.bit_count() <= n-2]
    pairs = [(a, all_points ^ a) for a in middle if a < (all_points ^ a)]
    F = singles+middle
    index = {a: i for i, a in enumerate(F)}
    require(len(pairs) == p and len(F)+1 == N, 'literal vertex counts')
    signs = [[2*int(bool(a & (1 << i)))-1 for a, _ in pairs] for i in range(n)]
    return F, pairs, index, signs


def core(n, z, F=None):
    p, s, _, q, _, _ = parameters(n)
    if F is None:
        F = vertices(n)[0]
    all_points = (1 << n)-1
    K = []
    for A in F:
        row = []
        for B in F:
            if A == B:
                value = s
            elif A.bit_count() == B.bit_count() == 1:
                value = s-q*z
            elif min(A.bit_count(), B.bit_count()) == 1:
                value = z*int(not A & B)
            else:
                value = (s-z)*int(A ^ B == all_points)
            row.append(value-1)
        K.append(row)
    require(len(K) == n+2*p, 'core dimension')
    return K


def lift(C):
    m = len(C)
    sums = [sum(row) for row in C]
    return [[1+sum(sums)]+[1-x for x in sums]] + [
        [1-sums[i]]+[1+x for x in row] for i, row in enumerate(C)]


def check_literal(n, z, C, L, F):
    _, s, N, q, K, D = parameters(n)
    require(all(len(row) == N for row in L), 'full dimension')
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)),
            'full symmetry')
    require(all(sum(row) == N for row in L), 'full row sums')
    require(all(L[i][i] == s for i in range(1, N)), 'nonempty M diagonal zero')
    require(all(L[i+1][j+1] == 0 for i, A in enumerate(F)
                for j, B in enumerate(F) if i != j and A & B), 'intersecting support')
    for i in range(n):
        x = [int(bool(A & (1 << i))) for A in F]
        require(sum(x) == s and all(dot(row, x) == 0 for row in C), 'core star kernel')
        w = [-Q(s, N)]+[Q(a)-Q(s, N) for a in x]
        require(all(dot(row, w) == 0 for row in L), 'full centered star kernel')
    require(L[0][0] == K-D*z, 'empty diagonal formula')
    for j, A in enumerate(F, 1):
        expected = (N-n*s+((n-1)*q-(s-1))*z if A.bit_count() == 1
                    else n-1-(n-A.bit_count()-1)*z)
        require(L[0][j] == expected, 'empty row formula')


def outer_add(matrix, entries, weight):
    for i, a in entries:
        for j, b in entries:
            matrix[i][j] += weight*a*b


def sos_coefficients(n, F, pairs, index, signs):
    """Construct 2C=G0+zG1 from independent integer square factors.

    f_P=v[A]-v[Ac]-sum_i u_iP v[{i}],
    g_P=v[A]+v[Ac]-sum_i v[{i}], w_P=v[A]+v[Ac].
    Equation (6) becomes 2C=2(p sum w_P^2-(sum w_P)^2)
    +2 sum g_P^2+z(sum f_P^2-sum g_P^2).
    """
    m, p = len(F), len(pairs)
    G0 = [[0]*m for _ in F]
    G1 = [[0]*m for _ in F]
    middle_indices = list(range(n, m))
    for i in middle_indices:
        for j in middle_indices:
            G0[i][j] -= 2
    for k, (A, B) in enumerate(pairs):
        ia, ib = index[A], index[B]
        f = [(i, -signs[i][k]) for i in range(n)]+[(ia, 1), (ib, -1)]
        g = [(i, -1) for i in range(n)]+[(ia, 1), (ib, 1)]
        outer_add(G0, [(ia, 1), (ib, 1)], 2*p)
        outer_add(G0, g, 2)
        outer_add(G1, f, 1)
        outer_add(G1, g, -1)
    return G0, G1


def partition_average(n, F, pairs, index):
    p, s, _, _, _, _ = parameters(n)
    base = [list(range(n))]+[[index[A], index[B]] for A, B in pairs]
    partitions = [base]
    for k, (A, B) in enumerate(pairs):
        partitions.append([[index[A]]+[i for i in range(n) if not A & (1 << i)],
                           [index[B]]+[i for i in range(n) if A & (1 << i)]] +
                          [base[j+1] for j in range(p) if j != k])
    counts = [[0]*len(F) for _ in F]
    for partition in partitions:
        require(len(partition) == s and sorted(sum(partition, [])) == list(range(len(F))),
                'literal partition coverage')
        for group in partition:
            require(group and all(not F[i] & F[j] for i in group for j in group if i != j),
                    'clique class consists of disjoint sets')
            require(all(sum(bool(F[j] & (1 << i)) for j in group) == 1 for i in range(n)),
                    'every class meets every star once')
            outer_add(counts, [(j, 1) for j in group], 1)
    require(len(partitions) == s, 'number of averaged partitions')
    return [[x-1 for x in row] for row in counts]


def upper_schur(n, z, C, F, pairs, index, signs):
    """Check the literal sum/difference congruence, without square roots."""
    p, s, N, q, _, _ = parameters(n)
    V = [[N*int(i == j)-1-C[i][j] for j in range(len(F))] for i in range(len(F))]
    for k, (A, B) in enumerate(pairs):
        a, b = index[A], index[B]
        require(all(V[i][a]+V[i][b] == -z and V[i][a]-V[i][b] == z*signs[i][k]
                    for i in range(n)), 'upper singleton cross congruence')
        for ell, (X, Y) in enumerate(pairs):
            x, y = index[X], index[Y]
            require(V[a][x]+V[a][y]+V[b][x]+V[b][y] ==
                    2*(n-1+z)*int(k == ell), 'upper middle sum block')
            require(V[a][x]-V[a][y]-V[b][x]+V[b][y] ==
                    2*(N-z)*int(k == ell), 'upper middle difference block')
            require(V[a][x]-V[a][y]+V[b][x]-V[b][y] == 0, 'upper cross block zero')
    A = Q(N*(N-(q+1)*z), N-z)
    B = -s+q*z+Q(z*z*(n-3), 2*(N-z))-Q(z*z*p, 2*(n-1+z))
    require(A > 0, 'positive upper nonconstant Schur eigenvalue')
    for i in range(n):
        for j in range(n):
            schur = (V[i][j]-Q(p*z*z, 2*(n-1+z))
                     -Q(z*z*dot(signs[i], signs[j]), 2*(N-z)))
            require(schur == A*int(i == j)+B, 'literal upper Schur block')
    return A+n*B


def polyadd(a, b):
    result = [0]*max(len(a), len(b))
    for i, x in enumerate(a):
        result[i] += x
    for i, x in enumerate(b):
        result[i] += x
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polymul(a, b):
    result = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return polyadd(result, [])


def cap_polynomials():
    for n in (4, 5):
        p, s, N, q, _, _ = parameters(n)
        d1, d2 = [N, -1], [n-1, 1]
        denominator = polymul([2], polymul(d1, d2))
        numerator = polyadd(polymul([2*(N-n*s), 2*(n-1)*q], polymul(d1, d2)),
                            polymul([0, 0, 1], polyadd(
                                polymul([n*(n-3)-2*q], d2), polymul([-n*p], d1))))
        target_num, target_den = ([ -15, 13], [3, 1]) if n == 4 else (
            [3016, -1858, 97], polymul([-26, 1], [4, 1]))
        require(polymul(numerator, target_den) == polymul(denominator, target_num),
                'cap rational function coefficient identity')
    require(1858**2-4*97*3016 == 4*570489, 'exact algebraic discriminant')
    require(97-1858+3016 == 1255 and 4*97-2*1858+3016 == -312,
            'algebraic cap root in (1,2)')
    require(194*2-1858 < 0 and 755**2 < 570489 < 756**2,
            'root monotonicity and exact radical bracket')


def scalar_cases():
    for n in range(4, 81):
        _, _, N, q, K, D = parameters(n)
        require(K-2*D == 2*n*q-n*n*(n-3)+1, 'minimum empty diagonal identity')
        F = (n-2)*2**(n-1)-(n-1)**3+1
        require(K-2*D-N == F, 'empty dual witness identity')
        if n >= 6:
            Fnext = (n-1)*2**n-n**3+1
            require(F > 0 and Fnext-2*F == 2**n+n**3-6*n*n+6*n-3 > 0,
                    'inductive cap obstruction validation')


def engine_audit():
    count = 0
    for a, b, c, d, e, f in itertools.product((-1, 0, 1), repeat=6):
        matrix = [[a, b, c], [b, d, e], [c, e, f]]
        minors = [a, d, f, a*d-b*b, a*f-c*c, d*f-e*e,
                  a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b]
        verdict = not rejects(lambda: psd_rank(matrix))
        require(verdict == all(x >= 0 for x in minors), 'PSD verdict vs all principal minors')
        count += verdict
    require(count == 24, 'ternary PSD enumeration count')
    return {'symmetric_ternary_3x3': 729, 'PSD_count': count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    cap_polynomials()
    scalar_cases()
    audit = engine_audit()
    coefficient_records, dense_records, cap_records = [], [], []
    controls = []
    for n in range(4, 9):
        F, pairs, index, signs = vertices(n)
        p, s, N, q, _, _ = parameters(n)
        require(all(dot(signs[i], signs[j]) == 2*q*int(i == j)-(n-3)
                    for i in range(n) for j in range(n)), 'literal sign Gram identity')
        C0, C1 = core(n, 0, F), core(n, 1, F)
        G0, G1 = sos_coefficients(n, F, pairs, index, signs)
        require(all(G0[i][j] == 2*C0[i][j] and G1[i][j] == 2*(C1[i][j]-C0[i][j])
                    for i in range(len(F)) for j in range(len(F))), 'full SOS coefficient equality')
        require(partition_average(n, F, pairs, index) == C1, 'full integer partition average')
        for z in (Q(0), Q(1), Q(2)):
            C, L = core(n, z, F), lift(core(n, z, F))
            check_literal(n, z, C, L, F)
            T = upper_schur(n, z, C, F, pairs, index, signs)
            if n <= 6:
                expected = p if z == 0 else 2*p-1 if z == 2 else 2*p
                require(psd_rank(C) == expected and psd_rank(L) == expected+1, 'dense lower ranks')
                dense_records.append({'n': n, 'z': str(z), 'core_rank': expected,
                                      'lower_rank': expected+1, 'upper_T': str(T)})
            mid = [int(A.bit_count() >= 2) for A in F]
            if z == 2:
                require(all(dot(row, mid) == 0 for row in C), 'endpoint extra middle kernel')
            if z == 0:
                v = [0]*len(F)
                v[index[pairs[0][0]]], v[index[pairs[0][1]]] = 1, -1
                require(all(dot(row, v) == 0 for row in C), 'zero endpoint pair-difference kernel')
            if n >= 6:
                require(N-L[0][0] < 0 and T < 0, 'whole-interval sampled cap obstruction')
        for z in (Q(-1), Q(3)):
            C = core(n, z, F)
            v = [0]*len(F)
            if z < 0:
                v[index[pairs[0][0]]], v[index[pairs[0][1]]] = 1, -1
                require(form(C, v) == 2*z < 0, 'negative-parameter exact witness')
            else:
                v = [int(A.bit_count() >= 2) for A in F]
                require(form(C, v) == 2*p*(2-z) < 0, 'over-two exact witness')
            if n <= 6:
                require(rejects(lambda: psd_rank(C)), 'PSD engine rejects out-of-interval case')
        coefficient_records.append({'n': n, 'N': N, 's': s, 'middle_pairs': p,
                                    'partitions': s, 'SOS_coefficient_entries': 2*len(F)**2,
                                    'upper_congruence_parameters': ['0', '1', '2']})
    for n, values in ((4, (Q(15, 13), Q(3, 2), Q(2))), (5, (Q(19, 10), Q(2)))):
        F, pairs, index, signs = vertices(n)
        _, _, N, _, _, _ = parameters(n)
        for z in values:
            C = core(n, z, F)
            L = lift(C)
            check_literal(n, z, C, L, F)
            T = upper_schur(n, z, C, F, pairs, index, signs)
            V = [[N*int(i == j)-1-C[i][j] for j in range(len(F))] for i in range(len(F))]
            upper = [[N*int(i == j)-L[i][j] for j in range(N)] for i in range(N)]
            unit = 2 if T == 0 else 1
            require(T >= 0 and psd_rank(V) == N-unit and psd_rank(upper) == N-unit,
                    'dense capped rank and full unit multiplicity')
            require(psd_rank(L) == N-n-int(z == 2), 'dense capped lower rank')
            cap_records.append({'n': n, 'z': str(z), 'upper_T': str(T),
                                'lower_rank': N-n-int(z == 2), 'unit_multiplicity': unit})
    F = vertices(4)[0]
    C = core(4, Q(1), F)
    L = lift(C)
    mutations = []
    bad = [row[:] for row in L]
    bad[0][0] += 1
    mutations.append(('changed empty loop', C, bad))
    bad = [row[:] for row in L]
    bad[1][1] += 1
    mutations.append(('changed nonempty diagonal', C, bad))
    bad = [row[:] for row in L]
    i, j = next((i+1, j+1) for i, A in enumerate(F) for j, B in enumerate(F)
                if i != j and A & B)
    bad[i][j] = bad[j][i] = 1
    mutations.append(('intersecting support insertion', C, bad))
    badC = [row[:] for row in C]
    badC[0][1] += 1
    badC[1][0] += 1
    mutations.append(('broken singleton star weights', badC, lift(badC)))
    for name, c, l in mutations:
        require(rejects(lambda: check_literal(4, Q(1), c, l, F)), 'malformed control: '+name)
        controls.append(name)
    for n, z in ((4, Q(1)), (5, Q(1)), (6, Q(2))):
        _, _, N, _, _, _ = parameters(n)
        l = lift(core(n, z))
        upper = [[N*int(i == j)-l[i][j] for j in range(N)] for i in range(N)]
        require(rejects(lambda: psd_rank(upper)), 'cap negative control')
        controls.append('cap rejected n='+str(n)+' z='+str(z))
    result = {
        'agent': 'six-downset-3', 'role': 'researcher',
        'status': 'Exact finite validation of the written all-n, all-real-parameter proof; not independently reviewed.',
        'arithmetic': 'integers and fractions.Fraction; CPython 3.11.2 standard library',
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'all_orders_bridge': 'PROOF.md Sections 3-8; no inference from finite samples',
        'coefficient_and_partition_cases': coefficient_records,
        'dense_lower_cases': dense_records, 'dense_capped_cases': cap_records,
        'algebraic_threshold': {'n': 5, 'expression': '(929-sqrt(570489))/97',
                                'discriminant': 2281956, 'P_at_1': 1255, 'P_at_2': -312,
                                'literal_algebraic_matrix_evaluated': False},
        'scalar_identity_orders': [4, 80],
        'out_of_interval_witness_orders': [4, 8],
        'PSD_engine_audit': audit, 'rejected_controls': controls,
    }
    data = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(data)
    print(data, end='')


if __name__ == '__main__':
    main()
