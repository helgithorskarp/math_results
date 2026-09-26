#!/usr/bin/env python3
"""Exact supplementary audit; no imported author code or numerical signs."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inverse(matrix):
    n = len(matrix)
    a = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        require(pivot is not None, 'singular matrix')
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale*y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][j]
        a[r] = [x / scale for x in a[r]]
        for i in range(r + 1, len(a)):
            scale = a[i][j]
            a[i] = [x - scale*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def distance_matrix(points):
    return [[sum((F(x)-F(y))**2 for x, y in zip(a, b))
             for b in points] for a in points]


def pair_sum(d, indices):
    return sum((d[i][j] for i, j in combinations(indices, 2)), F(0))


def subsets(indices):
    for size in range(len(indices) + 1):
        yield from combinations(indices, size)


def distance_projection(d, base_size, bad_center=False):
    """Center the entire fixed tuple from distances; use a Schur complement."""
    n = len(d)
    require(0 < base_size <= n, 'empty or invalid positive block')
    require(all(len(row) == n for row in d), 'non-square distance matrix')
    require(all(d[i][i] == 0 and d[i][j] == d[j][i] and d[i][j] >= 0
                for i in range(n) for j in range(n)), 'invalid distances')
    b = tuple(range(base_size))
    holes = tuple(range(base_size, n))
    # This differs from centering at the positive block in the author proof.
    # Remaining vectors have zero perpendicular component, so centering the
    # full tuple still makes the sum of positive perpendicular vectors zero.
    scatter = pair_sum(d, tuple(range(n))) / (n * n)
    q = [sum(d[i][j] for j in range(n))/n - scatter for i in range(n)]
    if bad_center:
        q = [d[i][0] for i in range(n)]
    gram = [[(q[i]+q[j]-d[i][j])/2 for j in range(n)] for i in range(n)]
    selected = []
    for i in holes:
        trial = selected + [i]
        block = [[gram[j][k] for k in trial] for j in trial]
        if rank(block) > len(selected):
            selected = trial
    require(len(selected) <= 5, 'remaining span exceeds five')
    if selected:
        inv = inverse([[gram[i][j] for j in selected] for i in selected])
        h = [[sum(gram[i][a]*inv[u][v]*gram[c][j]
                  for u, a in enumerate(selected) for v, c in enumerate(selected))
              for j in range(n)] for i in range(n)]
    else:
        h = [[F(0) for _ in range(n)] for _ in range(n)]
    projected = [[h[i][i]+h[j][j]-2*h[i][j] for j in range(n)] for i in range(n)]
    energy = sum(gram[i][i]-h[i][i] for i in b)
    return projected, energy, len(selected), rank(gram)


def projection_case(d, base_size):
    p, energy, remaining_rank, whole_rank = distance_projection(d, base_size)
    checks = 0
    for j in subsets(tuple(range(base_size, len(d)))):
        a = tuple(range(base_size)) + j
        require((pair_sum(d, a)-pair_sum(p, a))/len(a) == energy,
                'orthogonal energy depends on the selected subset')
        checks += 1
    return {'positive_block': base_size, 'remaining_positions': len(d)-base_size,
            'remaining_rank': remaining_rank, 'whole_rank': whole_rank,
            'orthogonal_energy': str(energy), 'subsets': checks}


def affine_case(d, base_size):
    """Recover the affine-offset norm using only centered distance Gram data."""
    n = len(d)
    b = tuple(range(base_size))
    holes = tuple(range(base_size, n))
    require(holes, 'this affine control needs a remaining point')
    scatter = pair_sum(d, b)/(base_size*base_size)
    norms = [sum(d[i][j] for j in b)/base_size-scatter for i in range(n)]
    gram = [[(norms[i]+norms[j]-d[i][j])/2 for j in range(n)] for i in range(n)]
    anchor = holes[0]
    directions = [[gram[i][j]-gram[i][anchor]-gram[anchor][j]+gram[anchor][anchor]
                   for j in holes] for i in holes]
    selected = []
    for i in range(len(holes)):
        trial = selected+[i]
        if rank([[directions[j][k] for k in trial] for j in trial]) > len(selected):
            selected = trial
    require(len(selected) <= 5, 'remaining affine dimension exceeds five')
    offset = gram[anchor][anchor]
    if selected:
        inv = inverse([[directions[i][j] for j in selected] for i in selected])
        g = [gram[holes[i]][anchor]-gram[anchor][anchor] for i in selected]
        offset -= sum(g[i]*inv[i][j]*g[j] for i in range(len(g)) for j in range(len(g)))
    require(offset >= 0, 'negative squared affine offset')
    projected = {(i, j): gram[i][j]-offset for i in holes for j in holes}
    q0 = pair_sum(d, b)/base_size
    checks = 0
    for chosen in subsets(holes):
        size = len(chosen)
        m = base_size+size
        rhs = (q0 + sum(projected[i, i] for i in chosen)
               - sum((projected[i, j] for i in chosen for j in chosen), F(0))/m
               + F(base_size*size, m)*offset)
        require(pair_sum(d, b+chosen)/m == rhs, 'affine offset update mismatch')
        checks += 1
    radius2 = max(d[0])
    require(q0 <= base_size*radius2, 'base scatter bound')
    require(offset <= 4*radius2, 'offset radius bound')
    require(all(0 <= projected[i, i] <= 4*radius2 for i in holes), 'direction radius bound')
    return {'base_size': base_size, 'remaining_size': len(holes),
            'remaining_affine_rank': len(selected), 'full_rank': rank(gram),
            'offset_squared': str(offset), 'subsets': checks}


def coefficient_maps(n, k, mutation=None):
    """Expand both definitions into symbols (distinguished pair, subset)."""
    m_total = n + 2
    positions = tuple(range(m_total))
    direct, grouped = defaultdict(F), defaultdict(F)
    for size in range(k+2, m_total+1):
        denominator = size*(size-1)*comb(m_total, size)
        if mutation == 'omit_subset_average':
            denominator = size*(size-1)
        coefficient = F((n+1)*comb(n, k)*(-1)**(size-k-2)*comb(n-k, size-k-2),
                        denominator)
        for a in combinations(positions, size):
            for pair in combinations(a, 2):
                direct[pair, a] += coefficient
    for pair in combinations(positions, 2):
        rest = tuple(i for i in positions if i not in pair)
        for positive in combinations(rest, k):
            holes = tuple(i for i in rest if i not in positive)
            for negative in subsets(holes):
                a = tuple(sorted(pair + positive + negative))
                denominator = m_total-1 if mutation == 'wrong_total' else m_total
                grouped[pair, a] += F((-1)**len(negative), denominator)
    return dict(direct), dict(grouped)


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    return False


def run():
    cases = {}
    generator = lambda count: [tuple(F(((i+2)**(j+1) % 37)-18, i+j+3)
                                    for j in range(6)) for i in range(count)]
    matrices = {
        'noncentral_4_plus_5': (distance_matrix(generator(9)), 4),
        'large_positive_block_9_plus_5': (distance_matrix(generator(14)), 9),
        'no_remaining_positions': (distance_matrix(generator(6)), 6),
        'singleton_positive': (distance_matrix(generator(6)), 1),
        'all_coincident': (distance_matrix([(3, -2, 1)]*7), 2),
        'repeated_remaining': (distance_matrix(generator(3)+[generator(1)[0]]*5), 3),
    }
    x = [(0, 0, 0), (2, 1, 0), (-1, 2, 1), (1, -2, 2),
         (3, 0, -1), (-2, -1, 1), (-1, 1, -3), (2, -1, -2)]
    y = [tuple(abs(a) for a in p) for p in x]
    dx, dy = distance_matrix(x), distance_matrix(y)
    losses = [dx[i][j]-dy[i][j] for i, j in combinations(range(len(x)), 2)]
    require(all(v >= 0 for v in losses) and any(v > 0 for v in losses),
            'fold is not a nonisometric contraction')
    mid = [[(a+b)/2 for a, b in zip(row_a, row_b)] for row_a, row_b in zip(dx, dy)]
    matrices['genuine_fold_midpoint'] = (mid, 3)
    for name, (d, b) in matrices.items():
        cases[name] = projection_case(d, b)
    require(cases['genuine_fold_midpoint']['whole_rank'] == 6,
            'control must have full paired rank')
    require(cases['noncentral_4_plus_5']['orthogonal_energy'] != '0',
            'control must test the discarded energy')

    affine = {}
    for name, d, b in [
            ('six_remaining_full_rank', distance_matrix(generator(10)), 4),
            ('fold_six_remaining', mid, 2),
            ('one_remaining', distance_matrix(generator(5)), 4),
            ('repeated_remaining', distance_matrix(generator(3)+[generator(1)[0]]*6), 3)]:
        affine[name] = affine_case(d, b)
    require(affine['six_remaining_full_rank']['full_rank'] == 6 and
            affine['six_remaining_full_rank']['remaining_affine_rank'] == 5 and
            affine['six_remaining_full_rank']['offset_squared'] != '0',
            'affine control does not exercise the sixth direction')

    # Exact moment-exponent and quantitative exponent checks. These finite
    # controls supplement the all-parameter identities in the review.
    scalar_checks = 0
    for p in range(2, 10):
        for ell in range(7):
            require(F(p, p+ell)-1 == -F(ell, p+ell), 'Poisson exponent')
            require(F(p*ell, p+ell) == ell-F(ell*ell, p+ell), 'offset coefficient')
            scalar_checks += 2
    for p in range(2, 10):
        for r in (F(0), F(1, 5), F(2), F(7, 3)):
            require(F(p, 2)*r*r+2*p*r*r+F(p, 2)*((2*r+2)**2+4)
                    == F(p, 2)*(9*r*r+8*r+8), 'box exponent')
            scalar_checks += 1
    require(8**5 < 256**2 and F(13, 8) > F(3, 2) and F(49, 18) < 4,
            'elementary bound constants')
    scalar_checks += 3

    expansions = []
    for n in range(8):
        for k in range(n+1):
            left, right = coefficient_maps(n, k)
            require(left == right, 'polarized coefficients differ term by term')
            expansions.append({'N': n, 'k': k, 'distinct_symbols': len(left)})

    d, b = matrices['noncentral_4_plus_5']
    p, energy, _, _ = distance_projection(d, b, bad_center=True)
    wrong_center_rejected = any((pair_sum(d, a)-pair_sum(p, a))/len(a) != energy
                               for j in subsets(tuple(range(b, len(d))))
                               for a in [tuple(range(b))+j])
    require(wrong_center_rejected, 'off-center mutation was not detected')
    p, energy, _, _ = distance_projection(d, b)
    require(energy != 0 and pair_sum(d, tuple(range(b))) != pair_sum(p, tuple(range(b))),
            'omitted-energy mutation was not detected')
    e = [tuple(int(i == j) for j in range(6)) for i in range(6)]
    rank_six = distance_matrix([(0,)*6]+e)
    require(rejected(lambda: distance_projection(rank_six, 1)), 'rank-six misuse accepted')
    require(rejected(lambda: distance_projection(d, 0)), 'empty positive block accepted')
    require(rejected(lambda: affine_case(distance_matrix(generator(9)), 2)),
            'seven affine-independent remaining points accepted')
    for mutation in ('omit_subset_average', 'wrong_total'):
        left, right = coefficient_maps(4, 1, mutation)
        require(left != right, 'normalization mutation was not detected')
    return {
        'status': 'INDEPENDENT_GAUSSIAN_BETA_GEOMETRY_REVIEW_PASS',
        'arithmetic': 'Python integers and Fraction; no numerical Gaussian sign evaluation',
        'distance_cases': cases,
        'affine_cases': affine,
        'affine_subset_checks': sum(c['subsets'] for c in affine.values()),
        'affine_scalar_checks': scalar_checks,
        'projection_subset_checks': sum(c['subsets'] for c in cases.values()),
        'polarization_expansions': expansions,
        'polarization_symbol_checks': sum(c['distinct_symbols'] for c in expansions),
        'fold_pairs': len(losses), 'fold_strict_pairs': sum(v > 0 for v in losses),
        'rejected_mutations': ['off-center Gram', 'omitted orthogonal energy',
                               'six independent remaining vectors', 'empty positive block',
                               'omitted subset average', 'wrong total-position divisor',
                               'seven affine-independent remaining points'],
        'scope': 'Finite algebra controls only; universal sign and strictness use the written review.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare with compact EXPECTED.json')
    args = parser.parse_args()
    result = run()
    data = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        require(data == Path(__file__).with_name('EXPECTED.json').read_bytes(), 'expected record mismatch')
        print(result['status'])
        print(hashlib.sha256(data).hexdigest())
    else:
        print(data.decode(), end='')


if __name__ == '__main__':
    main()
