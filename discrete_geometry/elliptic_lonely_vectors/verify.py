#!/usr/bin/env python3
"""Exact corroboration of the elliptic LVP theorem. CPython 3.11+, no packages."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def scale(a, p):
    return a * p[0], a * p[1]


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def direction(p):
    need(p != (0, 0), 'zero vector')
    return (F(1), p[1] / p[0]) if p[0] else (F(0), F(1))


def entries(points):
    out = [(('original', i), p) for i, p in enumerate(points)]
    for i, j in combinations(range(len(points)), 2):
        for sign in (1, -1):
            out.append((('pair', i, j, sign), add(points[i], scale(sign, points[j]))))
    need(len(out) == len(points) ** 2, 'multiset size')
    return out


def validate(points):
    need(all(p != (0, 0) for p in points), 'zero input')
    for p, q in combinations(points, 2):
        need(p != q and p != scale(-1, q), 'equal or opposite input')


def multiplicities(points, independent=False):
    validate(points)
    data = entries(points)
    bucket = Counter(direction(v) for _, v in data)
    counts = [bucket[direction(v)] for _, v in data]
    if independent:
        direct = [sum(det(v, w) == 0 for _, w in data) for _, v in data]
        need(direct == counts, 'determinant/normalization disagreement')
    lonely = [tag for (tag, _), count in zip(data, counts) if count == 1]
    # Check every returned witness directly, including its label multiplicity.
    for index, ((tag, v), count) in enumerate(zip(data, counts)):
        if count == 1:
            need(all(j == index or det(v, w) != 0 for j, (_, w) in enumerate(data)),
                 'false lonely certificate')
    return lonely, counts


def rref(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return a, []
    pivots, r = [], 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        divisor = a[r][c]
        a[r] = [x / divisor for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                value = a[i][c]
                a[i] = [x - value * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def nullspace(matrix):
    a, pivots = rref(matrix)
    cols = len(matrix[0])
    vectors = []
    for free in sorted(set(range(cols)) - set(pivots)):
        v = [F(0)] * cols
        v[free] = F(1)
        for i, pivot in enumerate(pivots):
            v[pivot] = -a[i][free]
        vectors.append(v)
    return vectors


def fit_ellipse(points):
    """For three distinct projective directions, solve Q(p)=1 rationally."""
    for triple in combinations(points, 3):
        a, pivots = rref([[x*x, 2*x*y, y*y, 1] for x, y in triple])
        if pivots != [0, 1, 2]:
            continue
        A, B, C = (row[3] for row in a)
        if A <= 0 or A*C-B*B <= 0:
            return None
        if all(A*x*x+2*B*x*y+C*y*y == 1 for x, y in points):
            return A, B, C
        return None
    return None


def norm_unit(D, t):
    t = F(t)
    den = 1 + D*t*t
    return (1-D*t*t)/den, 2*t/den


def kmul(p, q, D):
    """Multiplication in Q(sqrt(-D)), represented by rational pairs."""
    return p[0]*q[0]-D*p[1]*q[1], p[0]*q[1]+p[1]*q[0]


def roots(D):
    if D == 1:
        root, order = (F(0), F(1)), 4
    elif D == 3:
        root, order = (F(1, 2), F(1, 2)), 6
    else:
        root, order = (F(-1), F(0)), 2
    values, u = [], (F(1), F(0))
    for _ in range(order):
        values.append(u)
        u = kmul(u, root, D)
    need(u == (1, 0) and len(set(values)) == order, 'torsion table')
    return values


def torsion_audit():
    cases = []
    for D in (2, 1, 3):
        mu = roots(D)
        m = len(mu)//2
        for mask in product((0, 1, -1), repeat=m):
            points = [scale(sign, mu[i]) for i, sign in enumerate(mask) if sign]
            if not points:
                continue
            lonely, counts = multiplicities(points, independent=True)
            need(lonely, 'torsion fiber lacks witness')
            if D != 3 or len(points) <= 2:
                need(sum(tag[0] == 'original' for tag in lonely) == len(points),
                     'small fiber original witnesses')
            else:
                need(len(lonely) == 3 and all(tag[0] == 'pair' for tag in lonely),
                     'Eisenstein triple directions')
            cases.append({'D': D, 'mask': mask, 'lonely': lonely, 'counts': counts})
    need(len(cases) == 36, 'torsion subset completeness')
    return cases


def distinct_antipodal(points):
    out = []
    for p in points:
        if p not in out and scale(-1, p) not in out:
            out.append(p)
    return out


def transform(points, matrix):
    a, b, c, d = map(F, matrix)
    need(a*d-b*c != 0, 'singular map')
    return [(a*x+b*y, c*x+d*y) for x, y in points]


def family_audit():
    cases = []
    for D in (1, 2, 3, 5, 7, 11):
        for size in (7, 19):
            points = distinct_antipodal(norm_unit(D, F(j, 13)) for j in range(size))
            need(len(points) == size, 'family size')
            for matrix in [(1, 0, 0, 1), (2, 3, -1, 1)]:
                p = transform(points, matrix)
                form = fit_ellipse(p)
                need(form is not None, 'rational ellipse reconstruction')
                lonely, counts = multiplicities(p, independent=size <= 7)
                need(len(lonely) >= 2, 'elliptic existence')
                if D != 3:
                    need(sum(t[0] == 'original' for t in lonely) >= 2, 'deletion witnesses')
                cases.append({'D': D, 'size': size, 'matrix': matrix,
                              'form': [str(x) for x in form], 'lonely': len(lonely),
                              'lonely_originals': sum(t[0] == 'original' for t in lonely),
                              'multiplicity_histogram': sorted(Counter(counts).items())})
    # Saturated Eisenstein fibers: all originals have a within-fiber collision.
    for size in (2, 4, 9):
        representatives = [norm_unit(3, F(j, 17)) for j in range(size)]
        p = distinct_antipodal(kmul(u, root, 3) for u in representatives for root in roots(3)[:3])
        need(len(p) == 3*size, 'saturated fiber size')
        lonely, counts = multiplicities(p, independent=size == 2)
        need(lonely and all(t[0] == 'pair' for t in lonely), 'diagonal-only family')
        cases.append({'D': 3, 'saturated_fibers': size, 'size': len(p),
                      'lonely': len(lonely), 'lonely_originals': 0,
                      'multiplicity_histogram': sorted(Counter(counts).items())})
    return cases


def gale_audit(points):
    n = len(points)
    U = nullspace([[p[j] for p in points] for j in (0, 1)])
    d = n-2
    need(len(U) == d and len(rref(U)[1]) == d, 'Gale rank')
    need(all(sum(row[i]*points[i][j] for i in range(n)) == 0
             for row in U for j in (0, 1)), 'Gale kernel')
    lonely, _ = multiplicities(points, independent=True)
    minors = []
    for tag in lonely:
        if tag[0] == 'original':
            _, i = tag
            minor = [[v for k, v in enumerate(row) if k != i] for row in U]
        else:
            _, i, j, sign = tag
            # w=p_i+sign*p_j selects the OPPOSITE sign on generator columns.
            minor = [[row[k] for k in range(n) if k not in (i, j)]
                     + [row[i]-sign*row[j]] for row in U]
        need(len(rref(minor)[1]) == d, 'minor lost rank')
        kernel = nullspace(minor)
        need(len(kernel) == 1, 'minor corank')
        v = kernel[0]
        need(all(v) and len({abs(x) for x in v}) == len(v), 'minor not cosimple')
        minors.append({'witness': tag, 'unique_relation': [str(x) for x in v]})
    deletions = []
    for i in range(n):
        minor = [[v for k, v in enumerate(row) if k != i] for row in U]
        kernel = nullspace(minor)
        good = (len(rref(minor)[1]) == d and len(kernel) == 1
                and all(kernel[0]) and len({abs(x) for x in kernel[0]}) == n-1)
        if good:
            deletions.append(i)
    need(deletions == [tag[1] for tag in lonely if tag[0] == 'original'],
         'all-deletion equivalence')
    return {'size': n, 'dimension': d, 'minor_count': len(minors),
            'cosimple_deletions': deletions, 'minors': minors}


def qadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def qneg(a):
    return -a[0], -a[1]


def qmul(a, b):
    """Q(sqrt(2)) for the real irrational octagon control."""
    return a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def octagon_control():
    z, one, s = (F(0), F(0)), (F(1), F(0)), (F(0), F(1, 2))
    points = [(one, z), (s, s), (z, one), (qneg(s), s)]
    for x, y in points:
        need(qadd(qmul(x, x), qmul(y, y)) == one, 'octagon circle')
    data = list(points)
    for p, q in combinations(points, 2):
        data.extend([(qadd(p[0], q[0]), qadd(p[1], q[1])),
                     (qadd(p[0], qneg(q[0])), qadd(p[1], qneg(q[1])))])
    counts = [sum(qadd(qmul(p[0], q[1]), qneg(qmul(p[1], q[0]))) == z
                  for q in data) for p in data]
    need(len(data) == 16 and min(counts) > 1, 'irrational octagon failure')
    return counts


def main():
    torsion = torsion_audit()
    families = family_audit()
    gale = [gale_audit([norm_unit(D, F(j, 7)) for j in range(size)])
            for D, size in [(1, 4), (1, 7), (2, 5), (3, 5), (5, 6)]]
    triple = roots(3)[:3]
    u, power = norm_unit(3, F(1, 7)), (F(1), F(0))
    powers = []
    for m in (1, 2, 3):
        powers.append(power)
        power = kmul(power, u, 3)
        g = gale_audit([kmul(v, root, 3) for v in powers for root in triple])
        need(not g['cosimple_deletions'], 'infinite-family deletion obstruction')
        need(g['minor_count'] > 0, 'infinite-family diagonal success')
        gale.append(g)
    rectangle = [(F(x), F(y)) for x in range(-3, 4) for y in range(-5, 6)
                 if y > 0 or y == 0 and x > 0]
    lonely, counts = multiplicities(rectangle)
    need(len(rectangle) == 38 and not lonely and fit_ellipse(rectangle) is None,
         'published rectangle negative control')
    invalid = 0
    for p in [[(F(0), F(0)), (F(1), F(0))],
              [(F(1), F(0)), (F(-1), F(0))],
              [(F(1), F(0)), (F(1), F(0))]]:
        try:
            validate(p)
        except ValueError:
            invalid += 1
    need(invalid == 3, 'invalid input rejection')
    payload = {'torsion_fibers': torsion, 'rational_families': families, 'gale_minors': gale,
               'irrational_octagon_multiplicities': octagon_control(),
               'rectangle_38_multiplicity_histogram': sorted(Counter(counts).items()),
               'invalid_controls': invalid}
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    report = {'status': 'VERIFIED', 'torsion_cases': len(torsion),
              'rational_family_cases': len(families), 'gale_cases': len(gale),
              'gale_minors': sum(g['minor_count'] for g in gale),
              'payload_sha256': hashlib.sha256(canonical).hexdigest(), 'evidence': payload}
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
