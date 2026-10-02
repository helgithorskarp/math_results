"""Reproduce the sole exceptional original matrix, not a quotient-only test."""
from fractions import Fraction as F
from itertools import combinations
import pins
from literal import core_data, action, quadratic
from corridor import scalars, require, digest


def run():
    q, k = 5, 3
    X, N, s, C, D, R, U = core_data(q, k, scan=True)
    generated = {0}
    for size in (1, 2, 3):
        for pts in combinations(range(8), size):
            A = sum(1 << i for i in pts)
            if size < 3 or len(set(pts) & {0, 1, 2}) >= 2:
                generated.add(A)
    generated -= {14, 22, 38}
    require(X == sorted(generated) and N == 50 and s == 19,
            'Complete original family including actual empty coordinate')
    n = N-1
    values = scalars(q, k)
    one = [F(1)]*n
    z = [F(1-bool(A & 2)-bool(A & 4)+((A & 7).bit_count() >= 2))
         for A in X[1:]]
    yz = [F(A & 7 == 1 and (A >> 3).bit_count() == 1 and bool(A & 56))
          for A in X[1:]]
    yw = [F(A & 7 == 1 and (A >> 3).bit_count() == 1 and not bool(A & 56))
          for A in X[1:]]
    extra = [F(A & 7 in (2, 3, 4, 5) and (A >> 3).bit_count() == 1)
             for A in X[1:]]
    require(not any(action(C, z)) and not any(action(R, z)) and
            quadratic(z, D) == values['alpha'] == F(159, 10),
            'Actual lower kernel and strictly positive derivative')
    vectors = [one, yz, yw, extra]

    def gram(A):
        images = [action(A, v) for v in vectors]
        return [[sum(x*y for x, y in zip(v, images[j])) for j in range(4)]
                for v in vectors]

    cross = [k*values['az'], (q-k)*values['aw'], 4*q*(1-k)]
    diagonals = [k*values['gap'], (q-k)*values['gap'], 4*q*values['d']]
    expected_U = [[values['e'], *cross]]
    expected_D = [[values['S'], k*values['h'], (q-k)*values['h'], 4*q*values['h']]]
    for i in range(3):
        expected_U.append([cross[i], *[diagonals[i] if i == j else F(0)
                                     for j in range(3)]])
        expected_D.append([expected_D[0][i+1], F(0), F(0), F(0)])
    counts = [sum(v) for v in vectors]
    dot_gram = [[sum(a*b for a, b in zip(v, wv)) for wv in vectors]
                for v in vectors]
    expected_C = [[N*dot_gram[i][j]-counts[i]*counts[j]-expected_U[i][j]
                   for j in range(4)] for i in range(4)]
    require(gram(C) == expected_C and gram(U) == expected_U and gram(D) == expected_D and
            gram(R) == [[F(0)]*4 for _ in range(4)],
            'All actual-coordinate four-vector Gram entries')
    w = [one[i]-values['az']/values['gap']*yz[i]
         -values['aw']/values['gap']*yw[i]+F(2, values['d'])*extra[i]
         for i in range(n)]
    require(quadratic(w, U) == values['Q0'] == F(-322737, 23870) < 0 and
            quadratic(w, D) == values['D4'] == F(939346, 59675) > 0 and
            quadratic(w, R) == 0, 'Original all-real upper dual')
    record = {'q': q, 'k': k, 'N': N, 's': s, 'nonempty_order': n,
              'original_input_positions': 4*n*n,
              'complete_original_family_match': True,
              'all_actual_gram_entries_match': True,
              'lower_Delta': '159/10', 'upper_U0': '-322737/23870',
              'upper_Delta': '939346/59675', 'upper_R': '0',
              'C_gram': [[str(x) for x in row] for row in expected_C],
              'U_gram': [[str(x) for x in row] for row in expected_U],
              'Delta_gram': [[str(x) for x in row] for row in expected_D],
              'actual_matrix_digest': digest([[[str(x) for x in row]
                                             for row in A] for A in (C, D, R, U)]),
              'status': 'Credited original baseline, not a new finite classification'}
    return record


def controls():
    rejected = []

    def reject(label, fn):
        try:
            fn()
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Damaged mathematical input accepted: '+label)

    from corridor import bound, region, check_positive_cubic, check_tail_root
    reject('k below theorem domain', lambda: bound(2))
    reject('boolean k', lambda: bound(True))
    reject('q below ground domain', lambda: scalars(3, 3))
    reject('more deletions than outside vertices', lambda: scalars(4, 5))
    reject('changed positive-cubic constant',
           lambda: check_positive_cubic([174, 269, 20, 12]))
    reject('ceil instead of floor in strict tail', lambda: check_tail_root(6, 29))
    reject('zero numerator treated as sufficient',
           lambda: require(scalars(40, 8)['B0'] > 0, 'Strict tail positivity'))
    reject('a necessary-test pass asserted sufficient',
           lambda: require(region(24, 6).startswith('constructively_feasible'),
                           'Threshold corridor has no sufficiency verdict'))
    reject('changed pinned original table',
           lambda: pins.setup({next(iter(pins.PINS)): '0'*64}))
    X, N, s, C, D, R, U = core_data(5, 3, scan=True)
    n = N-1
    reject('constant dual substituted for negative original dual',
           lambda: require(quadratic([F(1)]*n, U) < 0, 'Actual upper negativity'))
    z = [F(1-bool(A & 2)-bool(A & 4)+((A & 7).bit_count() >= 2)) for A in X[1:]]
    reject('reversed lower derivative orientation',
           lambda: require(quadratic(z, [[-x for x in row] for row in D]) > 0,
                           'Lower derivative positivity'))
    broken = [row[:] for row in R]
    index = {A: i for i, A in enumerate(X[1:])}
    broken[index[1]][index[2]] = broken[index[2]][index[1]] = F(-1)
    reject('one repair sign reversed',
           lambda: require(quadratic([F(1)]*n, broken) == 0, 'Repair cancellation'))
    return {'damage_rejections': len(rejected), 'rejected': rejected,
            'status': 'Same-author semantic controls, not external review'}
