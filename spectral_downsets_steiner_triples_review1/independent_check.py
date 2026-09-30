"""Independent STS Hoffman audit: integer polynomials and fraction-free PSD.

Author: six-reviewer-1, reviewer. CPython 3.11+, standard library only.
No researcher code, matrix fixtures, numerical eigensolver, or CAS is imported.
Run from this directory: python3 independent_check.py
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import math


def require(ok, message):
    if not ok:
        raise ValueError(message)


# Polynomials in v, low coefficient first; exact integer operations.
def poly(a):
    a = [a] if isinstance(a, int) else list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def add(a, b):
    a, b = poly(a), poly(b)
    return poly([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])


def mul(a, b):
    a, b = poly(a), poly(b)
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return poly(c)


def neg(a):
    return mul(-1, a)


def power(a, k):
    out = poly(1)
    for _ in range(k):
        out = mul(out, a)
    return out


def determinant(a):
    n = len(a)
    out = poly(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = poly((-1) ** inversions)
        for i, j in enumerate(p):
            term = mul(term, a[i][j])
        out = add(out, term)
    return out


def shift7(a):
    out = [0] * len(a)
    for i, c in enumerate(a):
        for j in range(i + 1):
            out[j] += c * math.comb(i, j) * 7 ** (i - j)
    return list(poly(out))


def uniform_check():
    v = poly((0, 1)); p = add(v, -2); t2 = add(v, -3); vp3 = add(v, 3)
    p2 = power(p, 2)
    # L=4(v-2)^2 G, G is the rational centered-point Gram block.
    L = [
        [mul(mul(2, p2), add(mul(3, v), -1)), mul(-4, power(p, 3)),
         mul(mul(-2, mul(v, p)), vp3), mul(mul(-2, p2), vp3)],
        [mul(-4, power(p, 3)), mul(mul(2, p2), add(add(power(v, 2), v), -16)),
         poly(0), mul(mul(mul(-2, p2), vp3), add(v, -4))],
        [mul(mul(-2, mul(v, p)), vp3), poly(0),
         mul(v, add(mul(mul(t2, add(mul(3, v), 1)), p), mul(2, vp3))),
         mul(mul(2, mul(v, p)), vp3)],
        [mul(mul(-2, p2), vp3), mul(mul(mul(-2, p2), vp3), add(v, -4)),
         mul(mul(2, mul(v, p)), vp3), mul(mul(mul(2, p2), t2), vp3)]]
    d = [mul(4, p2), mul(4, power(p, 3)), mul(mul(2, mul(v, p)), t2),
         mul(mul(2, p2), t2)]
    n3 = add(add(mul(2, power(v, 2)), v), 3)
    H = [[add(mul(n3, d[i]) if i == j else poly(0), mul(-3, L[i][j]))
          for j in range(4)] for i in range(4)]
    # Triple-kernel block with basis (Rz,z) and metric diag(3,1).
    a = mul(t2, p)
    T = [[mul(3, add(mul(a, add(mul(3, v), 1)), mul(2, vp3))),
          mul(mul(6, p), vp3)],
         [mul(mul(6, p), vp3), mul(mul(3, a), add(v, 1))]]
    dt = [mul(6, a), mul(2, a)]
    U = [[add(mul(n3, dt[i]) if i == j else poly(0), mul(-3, T[i][j]))
          for j in range(2)] for i in range(2)]
    cert = json.loads(Path(__file__).with_name('uniform_minors.json').read_text())
    result = {}
    for name, matrix in [('lower_center', L), ('upper_center', H),
                         ('lower_triple', T), ('upper_triple', U)]:
        got = []
        for k in range(1, len(matrix) + 1):
            minor = determinant([row[:k] for row in matrix[:k]])
            coefficients = shift7(minor)
            require(coefficients == cert[name][k - 1]['shifted_coefficients'],
                    'polynomial determinant certificate mismatch')
            if name == 'lower_center' and k == 4:
                require(coefficients == [0], 'centered nullity missing')
            else:
                require(coefficients[0] > 0 and all(x >= 0 for x in coefficients),
                        'uniform positivity failed')
            got.append({'order': k, 'degree': len(coefficients) - 1,
                        'constant_at_v7': coefficients[0]})
        result[name] = got
    # Exact star kernel; the other blocks' positive factors have v>=7.
    kernel = [1, 1, 0, 1]
    for row in L:
        require(sum_poly([mul(x, y) for x, y in zip(row, kernel)]) == poly(0),
                'star polynomial kernel')
    remaining_upper = add(add(add(mul(4, power(v, 3)), mul(-27, power(v, 2))),
                              mul(62, v)), -63)
    require(shift7(remaining_upper) == [420, 272, 57, 4], 'pair upper factor')
    result['remaining_pair_upper_factor_v_minus_7'] = [420, 272, 57, 4]
    result['parameter_domain'] = 'all real v>=7 for these blocks; STS existence separate'
    return result


def sum_poly(xs):
    out = poly(0)
    for x in xs:
        out = add(out, x)
    return out


def projective_blocks(d):
    points = range(1, 2 ** d)
    return sorted({tuple(sorted((a - 1, b - 1, (a ^ b) - 1)))
                   for a, b in combinations(points, 2)})


def affine_blocks():
    # Every pair of distinct F_3^2 points determines its unique third point.
    points = [(i // 3, i % 3) for i in range(9)]
    index = {x: i for i, x in enumerate(points)}
    return sorted({tuple(sorted((i, j, index[((-points[i][0] - points[j][0]) % 3,
                                             (-points[i][1] - points[j][1]) % 3)])))
                   for i, j in combinations(range(9), 2)})


def check_design(v, blocks):
    require(v >= 3 and len(blocks) == len(set(blocks)), 'design domain')
    coverage = {pair: 0 for pair in combinations(range(v), 2)}
    for b in blocks:
        require(len(set(b)) == 3 and all(0 <= x < v for x in b), 'triple domain')
        for p in combinations(sorted(b), 2):
            coverage[p] += 1
    require(all(x == 1 for x in coverage.values()), 'pair coverage')
    return len(blocks)


def build(v, blocks):
    b = check_design(v, blocks)
    pairs = list(combinations(range(v), 2))
    sets = [frozenset()] + [frozenset([i]) for i in range(v)]
    sets += [frozenset(p) for p in pairs] + [frozenset(t) for t in blocks]
    sets.sort(key=lambda a: (len(a), sum(1 << i for i in a)))
    n, s = len(sets), (3 * v - 1) // 2
    require(n == 1 + v + 4 * b, 'downset size')
    require(all(sum(i in a for a in sets) == s for i in range(v)), 'star sizes')
    h = F(v + 3, v - 3); w = 1 + h / (v - 2)
    triples = {frozenset(t) for t in blocks}
    Q = []
    for a in sets:
        row = []
        for c in sets:
            if a & c:
                x = F(s if a == c else 0)
            elif not a or not c:
                x = F(1)
            else:
                k = tuple(sorted((len(a), len(c))))
                x = { (1, 1): F(0), (2, 2): w, (3, 3): F(1) }.get(k, h)
                if k == (1, 2):
                    x = w - h if a | c in triples else w
            row.append(x)
        Q.append(row)
    require(all(sum(row) == n for row in Q), 'Q row sums')
    require(all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n)), 'symmetry')
    require(all(Q[i][j] == (s if i == j else 0)
                for i, a in enumerate(sets) for j, c in enumerate(sets) if a & c),
            'normalized support')
    return sets, s, Q


def fraction_free_psd_rank(Q):
    scale = math.lcm(*(x.denominator for row in Q for x in row))
    A = [[int(x * scale) for x in row] for row in Q]
    n = len(A); previous = 1; rank = 0
    while rank < n:
        require(all(A[i][i] >= 0 for i in range(rank, n)), 'negative diagonal')
        # A zero diagonal of a PSD matrix forces its entire row to vanish.
        for i in range(rank, n):
            if A[i][i] == 0:
                require(all(A[i][j] == 0 for j in range(rank, n)), 'zero-pivot cross term')
        k = next((i for i in range(rank, n) if A[i][i] > 0), None)
        if k is None:
            break
        if k != rank:
            A[rank], A[k] = A[k], A[rank]
            for row in A:
                row[rank], row[k] = row[k], row[rank]
        pivot = A[rank][rank]
        for i in range(rank + 1, n):
            for j in range(i, n):
                value = pivot * A[i][j] - A[i][rank] * A[j][rank]
                quotient, rem = divmod(value, previous)
                require(rem == 0, 'non-exact Bareiss division')
                A[i][j] = A[j][i] = quotient
        previous = pivot
        rank += 1
    return rank


def block_bridge(v, sets, Q):
    n = len(sets); p = v - 2; t = F(v - 3, 2)
    g = t * v / p; s = F(3 * v - 1, 2)
    h = F(v + 3, v - 3); w = 1 + h / p
    alpha = s - w * (v - 3); delta = s + w
    # Coordinate action in basis (u, Pu, Vu, Bu), Vu=RB u-(2t/p)Pu.
    A = [[s, -p, -h*g, -h*t], [-1, alpha, 0, -h*t*(v-4)/p],
         [-h, 0, delta, h], [-h, -h*(v-4), h*v/p, v+3]]
    # Our integral third basis vector is p Vu.
    scaling = [1, 1, p, 1]
    d = (v - 3) * p
    A = [[F(A[i][j]) * scaling[j] / scaling[i] * d for j in range(4)]
         for i in range(4)]
    require(all(x.denominator == 1 for row in A for x in row), 'block action denominators')
    C = [[int((Q[i+1][j+1] - 1) * d) for j in range(n-1)] for i in range(n-1)]
    nonempty = sets[1:]
    triples = [a for a in nonempty if len(a) == 3]
    completing = {a: next(z - a for z in triples if a <= z)
                  for a in nonempty if len(a) == 2}
    for k in range(v - 1):
        u = [int(i == k) - int(i == v-1) for i in range(v)]
        basis = [[0] * (n-1) for _ in range(4)]
        for i, a in enumerate(nonempty):
            value = sum(u[j] for j in a)
            if len(a) == 1:
                basis[0][i] = value
            elif len(a) == 2:
                basis[1][i] = value
                basis[2][i] = p * (value + sum(u[j] for j in completing[a])) - int(2*t)*value
            else:
                basis[3][i] = value
        for j, x in enumerate(basis):
            for i, row in enumerate(C):
                require(sum(a*b for a, b in zip(row, x)) ==
                        sum(int(A[q][j]) * basis[q][i] for q in range(4)),
                        'entry-to-centered-action bridge')
    return 4 * (v - 1)


def matrix_hash(Q):
    data = json.dumps([[str(x) for x in row] for row in Q], separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def fixture_check(v, blocks):
    sets, s, Q = build(v, blocks); n = len(sets)
    rank = fraction_free_psd_rank(Q)
    upper_rank = fraction_free_psd_rank([[F(n if i == j else 0) - Q[i][j]
                                         for j in range(n)] for i in range(n)])
    require(rank == 4*len(blocks) and upper_rank == n-1, 'endpoint ranks')
    # Explicit proposed entire lower-endpoint eigenspace of M.
    kernel = [[n*int(i == 0)-1 for i in range(n)]]
    kernel += [[n*int(k in a)-s for a in sets] for k in range(v)]
    for x in kernel:
        require(sum(x) == 0 and all(sum(a*b for a, b in zip(row, x)) == 0 for row in Q),
                'explicit Q nullspace')
    return {'v': v, 'N': n, 's': s, 'blocks': len(blocks), 'rank_Q': rank,
            'rank_upper': upper_rank, 'matrix_sha256': matrix_hash(Q),
            'centered_basis_images_checked': block_bridge(v, sets, Q),
            'nullspace_vectors_checked': len(kernel)}


def rejects(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('negative control was accepted')


def run():
    result = {'arithmetic': 'Python integers, integer polynomials, Fraction',
              'uniform': uniform_check(), 'fixtures': []}
    for v, blocks in [(7, projective_blocks(3)), (9, affine_blocks()),
                      (15, projective_blocks(4))]:
        result['fixtures'].append(fixture_check(v, blocks))
    # A zero diagonal with a nonzero off diagonal must not pass PSD.
    rejects(lambda: fraction_free_psd_rank([[F(0), F(1)], [F(1), F(1)]]))
    rejects(lambda: fraction_free_psd_rank([[F(1), F(2)], [F(2), F(1)]]))
    rejects(lambda: check_design(7, projective_blocks(3)[:-1]))
    _, _, Q = build(7, projective_blocks(3))
    Q[1][2] += 1; Q[2][1] += 1
    rejects(lambda: fraction_free_psd_rank(Q))
    # STS(3): complement permutation, ±1 each with multiplicity four.
    cube = [[F(4*((i == j)+(i ^ j == 7))) for j in range(8)] for i in range(8)]
    result['order_three_cube_ranks'] = [fraction_free_psd_rank(cube),
        fraction_free_psd_rank([[F(8*(i == j))-cube[i][j] for j in range(8)] for i in range(8)])]
    require(result['order_three_cube_ranks'] == [4, 4], 'cube boundary')
    result['negative_controls'] = 4
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
