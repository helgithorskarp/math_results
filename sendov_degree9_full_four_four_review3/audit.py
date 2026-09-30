"""Independent exact 4+4 audit by six-reviewer-3. Standard library only.

The original norm is expanded in two imaginary quadratic generators,
B^2=-Q(1-c^2), Y^2=-(1-x^2), BY=lambda. No author module is imported.
Cell tensors use direct monomial blossom matrices, without subdivision.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, lcm, prod
from pathlib import Path
import argparse, hashlib, json
from functools import lru_cache


def need(ok, message):
    if not ok:
        raise ArithmeticError(message)


def clean(p):
    return {e: v for e, v in p.items() if v}


def add(*polys):
    r = defaultdict(int)
    for p in polys:
        for e, v in p.items():
            r[e] += v
    return clean(r)


def scale(p, v):
    return clean({e: k*v for e, k in p.items()})


def variable(i, size=4):
    e = [0]*size
    e[i] = 1
    return {tuple(e): 1}


ONE = {(0, 0, 0, 0): 1}


def multiply(p, q):
    r = defaultdict(int)
    for e, v in p.items():
        for f, w in q.items():
            r[tuple(a+b for a, b in zip(e, f))] += v*w
    return clean(r)


def power(p, n):
    r = ONE
    for _ in range(n):
        r = multiply(r, p)
    return r


def ring_multiply(p, q):
    """Reduce each B,Y exponent immediately; coefficients remain integers."""
    r = defaultdict(int)
    for e, v in p.items():
        for f, w in q.items():
            base = [e[i]+f[i] for i in range(4)]
            b, y = e[4]+f[4], e[5]+f[5]
            pieces = [(base, v*w)]
            if b == 2:
                # B^2=-Q+Q*c^2.
                pieces = [(a[:3]+[a[3]+1], -k) for a, k in pieces] + [
                    ([a[0], a[1]+2, a[2], a[3]+1], k) for a, k in pieces]
            if y == 2:
                # Y^2=-1+x^2.
                pieces = [(a, -k) for a, k in pieces] + [
                    ([a[0], a[1], a[2]+2, a[3]], k) for a, k in pieces]
            for a, k in pieces:
                r[tuple(a)+(b % 2, y % 2)] += k
    return clean(r)


def original_norm():
    """Direct quadratic convolutions and conjugation in the radical ring."""
    unit = {(0,)*6: 1}
    b, c, x, q, B, Y = [variable(i, 6) for i in range(6)]
    w = add(x, Y)
    factors = [unit,
               scale(ring_multiply(b, ring_multiply(w, add(c, B))), -2),
               ring_multiply(ring_multiply(b, b),
                 ring_multiply(add(unit, scale(q, -1)), ring_multiply(w, w)))]
    coefficients = [unit]
    for _ in range(4):
        new = [{} for _ in range(len(coefficients)+2)]
        for j, a in enumerate(coefficients):
            for k, f in enumerate(factors):
                new[j+k] = add(new[j+k], ring_multiply(a, f))
        coefficients = new
    # 280 O = sum 2520/(k+1) * coefficient[k].
    integral = add(*(scale(p, 2520//(k+1)) for k, p in enumerate(coefficients)))
    conjugate = {e: v*(-1)**(e[4]+e[5]) for e, v in integral.items()}
    norm = ring_multiply(integral, conjugate)
    need(all(e[4] == e[5] for e in norm), 'Uncancelled imaginary component')
    even = {e[:4]: v for e, v in norm.items() if e[4] == 0}
    odd = {e[:4]: v for e, v in norm.items() if e[4] == 1}
    q4 = variable(3)
    delta = add(even, scale(power(add(ONE, scale(q4, -1)), 8), -78400))
    need((len(even), len(odd)) == (551, 295), 'Norm term inventory differs')
    return delta, odd


def weighted_reduce(delta, skew):
    """Coefficient substitution b=t(cx+lambda), lambda^2=Qg."""
    even, odd = defaultdict(int), defaultdict(int)
    for parity, p in enumerate((delta, skew)):
        for (n, c, x, q), v in p.items():
            for k in range(n+1):
                pairs, remainder = divmod(k+parity, 2)
                out = odd if remainder else even
                for i in range(pairs+1):
                    for j in range(pairs+1):
                        out[(n, c+n-k+2*i, x+n-k+2*j, q+pairs)] += (
                            v*comb(n, k)*comb(pairs, i)*comb(pairs, j)*(-1)**(i+j))
    return clean(even), clean(odd)


def q_scale(p, eta=False):
    return {(e[0], e[1], e[2], (2*e[3] if eta else e[3])):
            F(v, 78400*4**e[3]) for e, v in p.items()}


def envelope(even, odd):
    c, x, z = [variable(i) for i in (1, 2, 3)]
    s = add(ONE, scale(multiply(c, x), -1))
    g = multiply(add(ONE, scale(power(c, 2), -1)),
                 add(ONE, scale(power(x, 2), -1)))
    den = scale(multiply(s, add(power(s, 2), g)), 4)
    num = add(power(s, 4), scale(multiply(power(s, 2), g), 6), power(g, 2))
    return add(multiply(den, q_scale(even, True)),
               multiply(num, scale(multiply(z, q_scale(odd, True)), F(1, 2))))


def unweighted_margins(delta, skew):
    """Reconstruct both signs of the credited phase-sheet dependency."""
    def transport(p):
        return {(n, c+n, x+n, 2*q): F(v, 78400*4**q)
                for (n, c, x, q), v in p.items()}
    c, x, z = [variable(i) for i in (1, 2, 3)]
    s = add(ONE, scale(multiply(c, x), -1))
    g = multiply(add(ONE, scale(power(c, 2), -1)),
                 add(ONE, scale(power(x, 2), -1)))
    endpoint = scale(multiply(s, transport(delta)), 2)
    skew_bound = scale(multiply(multiply(z, add(power(s, 2), g)),
                                transport(skew)), F(1, 2))
    return add(endpoint, skew_bound), add(endpoint, scale(skew_bound, -1))


def canonical(p, denominator=1):
    return [[list(e), str(F(v, denominator))] for e, v in sorted(p.items())]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
          separators=(',', ':')).encode()).hexdigest()


@lru_cache(maxsize=None)
def blossom_matrix(n, low, high):
    """Cell coefficients of each monomial, from symmetric multi-affine lift.

    The i-th coefficient of z^k on [low,high] is the mean of all k-fold
    products from n slots, i equal to high and n-i equal to low.
    This is a different formula from affine power conversion/subdivision.
    """
    weights = [[sum(F(comb(i, j)*comb(n-i, k-j), comb(n, k)) *
                    high**j * low**(k-j)
                    for j in range(max(0, k-(n-i)), min(i, k)+1))
                for k in range(n+1)] for i in range(n+1)]
    # Invert every column by finite differences. This certifies the complete
    # univariate basis transformation, not a collection of sampled values.
    for k in range(n+1):
        for r in range(n+1):
            actual = comb(n, r)*sum((-1)**(r-i)*comb(r, i)*weights[i][k]
                                    for i in range(r+1))
            expected = (comb(k, r)*low**(k-r)*(high-low)**r if r <= k else F(0))
            need(actual == expected, 'Blossom basis identity failed')
    den = lcm(*(v.denominator for row in weights for v in row))
    return [[(k, int(v*den)) for k, v in enumerate(row) if v]
            for row in weights], den


def tensor(p, degrees, box):
    shape = tuple(n+1 for n in degrees)
    stride = tuple(prod(shape[i+1:]) for i in range(4))
    den = lcm(*(F(v).denominator for v in p.values()))
    data = [0]*prod(shape)
    for e, v in p.items():
        need(all(e[i] <= degrees[i] for i in range(4)), 'Degree too small')
        data[sum(e[i]*stride[i] for i in range(4))] = int(v*den)
    for axis, n in enumerate(degrees):
        matrix, factor = blossom_matrix(n, *box[axis])
        step = stride[axis]
        new = [0]*len(data)
        for outer in range(0, len(data), step*(n+1)):
            for inner in range(step):
                start = outer+inner
                for i, row in enumerate(matrix):
                    new[start+i*step] = sum(data[start+k*step]*v for k, v in row)
        data = new
        den *= factor
    return data, den


def cell_record(p, degrees, box, equality='phase'):
    values, den = tensor(p, degrees, box)
    need(min(values) >= 0, 'Negative cell coefficient')
    shape = [n+1 for n in degrees]
    stride = [prod(shape[i+1:]) for i in range(4)]
    zeros = [tuple((i//stride[j]) % shape[j] for j in range(4))
             for i, v in enumerate(values) if not v]
    zc = min(v for i, v in enumerate(values) if (i//stride[1]) % shape[1] == 0)
    zx = min(v for i, v in enumerate(values) if (i//stride[2]) % shape[2] == 0)
    if equality == 'phase':
        need(zc > 0 and zx > 0, 'Strict phase support failed')
    h = hashlib.sha256()
    for v in values:
        h.update((str(F(v, den))+'\n').encode())
    return {'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'coefficients': len(values),
            'minimum': str(F(min(values), den)),
            'minimum_positive': str(F(min(v for v in values if v > 0), den)),
            'zeros': len(zeros), 'zero_indices_sha256': digest(zeros),
            'zeroth_c_minimum': str(F(zc, den)),
            'zeroth_x_minimum': str(F(zx, den)), 'sha256': h.hexdigest()}, zeros


UNIT = (F(0), F(1))
LOW = (F(0), F(1, 2))
HIGH = (F(1, 2), F(1))


def check_cover(boxes, axes, allowed, area):
    """Check every endpoint and open grid stratum of the closed domain."""
    grids = []
    for axis in axes:
        edges = sorted({v for box in boxes for v in box[axis]})
        grids.append(edges+[(a+b)/2 for a, b in zip(edges, edges[1:])])
    for x in grids[0]:
        for y in grids[1]:
            covered = any(b[axes[0]][0] <= x <= b[axes[0]][1] and
                          b[axes[1]][0] <= y <= b[axes[1]][1] for b in boxes)
            need(covered == allowed(x, y), 'Closed cell coverage failed')
    for i, b in enumerate(boxes):
        need(all(b[j] == UNIT for j in range(4) if j not in axes),
             'Incomplete unused cell axis')
        for other in boxes[:i]:
            need(not all(max(b[j][0], other[j][0]) < min(b[j][1], other[j][1])
                         for j in axes), 'Overlapping cell interiors')
    need(sum(prod(b[j][1]-b[j][0] for j in axes) for b in boxes) == area,
         'Wrong covered area')


def mean_premise():
    """Fresh univariate proof of only the weak mean xi>a used by7833."""
    # Clear (1+a)^8 from H_a(a, 1+[a/(1+a)]^2).
    # Variables (a,t,dummy,dummy); integrate t exactly after fourth power.
    a, t = variable(0), variable(1)
    b = add(ONE, scale(power(a, 2), -1))
    denom = power(add(ONE, a), 2)
    base = add(multiply(power(a, 2), denom),
      scale(multiply(multiply(power(a, 2), b), multiply(t, denom)), 2),
      multiply(multiply(power(b, 2), power(t, 2)), add(denom, power(a, 2))))
    full = power(base, 4)
    integral = defaultdict(F)
    for e, v in full.items():
        integral[(e[0], 0, 0, 0)] += F(v, e[1]+1)
    numerator = add(power(add(ONE, a), 8), scale(clean(integral), -1))
    # Divide twice by (1-a), coefficient recurrence in ascending powers.
    coeff = [numerator.get((i, 0, 0, 0), F(0)) for i in range(25)]
    for _ in range(2):
        quotient, carry = [], F(0)
        for value in coeff[:-1]:
            carry += value
            quotient.append(carry)
        need(coeff[-1] == -carry, 'Mean numerator factor division failed')
        coeff = quotient
    need(len(coeff) == 23, 'Wrong weak mean degree')
    bern = [sum(coeff[k]*F(comb(i, k), comb(22, k))
                for k in range(i+1)) for i in range(23)]
    need(min(bern) == F(8, 9), 'Mean certificate positivity failed')
    return {'degree': 22, 'coefficients': 23, 'minimum': str(min(bern)),
            'power_coefficients': [str(v) for v in coeff],
            'bernstein_coefficients': [str(v) for v in bern]}


def gauss_multiply(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def direct_origin(b, u, v):
    """Eight distinct linear convolutions over exact Gaussian rationals."""
    coeff = [(F(1), F(0))]
    for root in [u]*4+[v]*4:
        new = [(F(0), F(0)) for _ in range(len(coeff)+1)]
        for i, z in enumerate(coeff):
            new[i] = tuple(new[i][j]+z[j] for j in range(2))
            z = gauss_multiply(z, root)
            new[i+1] = tuple(new[i+1][j]-b*z[j] for j in range(2))
        coeff = new
    z = tuple(sum(F(9, k+1)*v[j] for k, v in enumerate(coeff)) for j in range(2))
    return z[0]**2+z[1]**2


def evaluator(p):
    den = lcm(*(F(v).denominator for v in p.values()))
    entries = [(e, int(v*den)) for e, v in p.items()]
    degrees = [max(e[i] for e in p) for i in range(4)]
    def evaluate(values):
        powers = [[values[i]**k for k in range(degrees[i]+1)] for i in range(4)]
        return sum(v*prod(powers[i][e[i]] for i in range(4)) for e, v in entries)/den
    return evaluate


def definition_controls(delta, skew, even, odd):
    dval, jval = evaluator(delta), evaluator(skew)
    pval, tval = evaluator(even), evaluator(odd)
    phases = [(F(45, 53), F(28, 53), F(77, 85), F(36, 85)),
              (F(7, 25), F(24, 25), F(8, 17), F(15, 17)),
              (F(1), F(0), F(0), F(1)),
              (F(0), F(1), F(1), F(0)),
              (F(1), F(0), F(1), F(0))]
    rows = []
    for c, d, x, y in phases:
        need(c*c+d*d == x*x+y*y == 1, 'Nonunit definition control')
        for sign in (-1, 1):
            yy = sign*y
            for eta in (F(0), F(2, 9), F(3, 8), F(1, 2)):
                u0, v0 = gauss_multiply((x, yy), (c, d)), gauss_multiply((x, yy), (c, -d))
                u, v = tuple((1+eta)*z for z in u0), tuple((1-eta)*z for z in v0)
                lam, q = -eta*d*yy, eta*eta
                for t in (F(0), F(2, 7), F(1)):
                    b = t*(c*x+lam)
                    direct = direct_origin(b, u, v)-(1-q)**8
                    old = (dval((b, c, x, q))+lam*jval((b, c, x, q)))/78400
                    new = (pval((t, c, x, q))+lam*tval((t, c, x, q)))/78400
                    need(direct == old == new, 'Definition-level norm control failed')
                    rows.append([str(z) for z in (t, c, x, eta, lam, direct)])
    return {'count': len(rows), 'sha256': digest(rows)}


def geometry_controls():
    eta = variable(0)
    one_minus = add(ONE, scale(eta, -1))
    first = add(scale(power(eta, 2), 4),
        scale(multiply(power(one_minus, 2), add(ONE, scale(power(eta, 2), 3))), -1))
    second = add(scale(ONE, -1), scale(eta, 2),
                 scale(power(eta, 3), 6), scale(power(eta, 4), -3))
    need(first == second, 'Geometry separator identity failed')
    f = lambda v: -1+2*v+6*v**3-3*v**4
    lo, hi = F(3731802866, 10**10), F(3731802867, 10**10)
    need(f(lo) < 0 < f(hi) and f(F(3, 8)) == F(29, 4096), 'Root bracket failed')
    return {'separator_at_three_eighths': str(f(F(3, 8))),
            'unique_positive_root_bracket': [str(lo), str(hi)],
            'angular_necessary_bound': 'x^2 > eta^3(2-eta)/((1-eta)^3(1+eta))'}


def audit():
    delta, skew = original_norm()
    even, odd = weighted_reduce(delta, skew)
    need((len(even), len(odd)) == (7415, 5474), 'Weighted term count differs')
    H = envelope(even, odd)
    need(len(H) == 35890, 'Envelope term count differs')
    even_boxes = [(UNIT, UNIT, LOW, UNIT), (UNIT, LOW, HIGH, UNIT),
                  (UNIT, HIGH, HIGH, UNIT)]
    envelope_boxes = [(UNIT, UNIT, HIGH, UNIT), (UNIT, UNIT, LOW, LOW),
                      (UNIT, UNIT, LOW, (F(1, 2), F(3, 4)))]
    check_cover(even_boxes, (1, 2), lambda c, x: True, F(1))
    check_cover(envelope_boxes, (2, 3), lambda x, z: x >= F(1, 2) or z <= F(3, 4), F(7, 8))
    records = []
    for i, box in enumerate(even_boxes):
        rec, zeros = cell_record(q_scale(even), (16, 16, 16, 16), box)
        need(zeros == ([(16, 16, 16, 0)] if i == 2 else []),
             'Even equality support differs')
        records.append(rec)
    for i, box in enumerate(envelope_boxes):
        rec, zeros = cell_record(H, (16, 19, 19, 32), box)
        need((len(zeros) == 3374 and all(e[1] >= 16 and e[2] >= 16 for e in zeros))
             if i == 0 else not zeros, 'Envelope corner support differs')
        records.append(rec)
    plus, minus = unweighted_margins(delta, skew)
    plus_boxes = [(UNIT, UNIT, LOW, UNIT), (UNIT, UNIT, HIGH, UNIT)]
    minus_boxes = [(UNIT, UNIT, LOW, UNIT), (UNIT, LOW, HIGH, UNIT),
                   (UNIT, HIGH, (F(1, 2), F(3, 4)), UNIT),
                   (UNIT, HIGH, (F(3, 4), F(1)), UNIT)]
    dependency = []
    for label, p, boxes in [('plus', plus, plus_boxes), ('minus', minus, minus_boxes)]:
        check_cover(boxes, (1, 2), lambda c, x: True, F(1))
        for box in boxes:
            rec, zeros = cell_record(p, (16, 17, 17, 16), box)
            if zeros:
                expected = {(i, 17, 17, j) for i in range(17) for j in range(17)}
                expected |= {(16, 16, 17, j) for j in (0, 1)}
                expected |= {(16, 17, 16, j) for j in (0, 1)}
                need(set(zeros) == expected, 'Unweighted zero support differs')
            rec['sign'] = label
            dependency.append(rec)
    # The c=x=1 corner, after b=t,Q=q/4, is a two-variable certificate.
    corner = defaultdict(F)
    for (b, c, x, q), v in delta.items():
        corner[(b, 0, 0, q)] += F(v, 78400*4**q)
    rec, zeros = cell_record(clean(corner), (16, 0, 0, 8), (UNIT,)*4, 'corner')
    need(zeros == [(16, 0, 0, 0)] and F(rec['minimum_positive']) == F(1, 8),
         'Corner equality certificate failed')
    dependency.append(rec)
    return {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'method': 'two imaginary generators and direct symmetric blossom cell tensors',
            'weighted_sha256': digest([canonical(even, 78400), canonical(odd, 78400)]),
            'envelope_sha256': digest(canonical(H)),
            'target_cells': records, 'dependency_cells': dependency,
            'target_coefficients': sum(r['coefficients'] for r in records),
            'dependency_coefficients': sum(r['coefficients'] for r in dependency),
            'weak_mean': mean_premise(), 'geometry': geometry_controls(),
            'definition_controls': definition_controls(delta, skew, even, odd),
            'complete_univariate_basis_inversions': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    actual = audit()
    if args.expected:
        need(actual == json.loads(args.expected.read_text()), 'Independent manifest differs')
    if args.write:
        args.write.write_text(json.dumps(actual, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result': 'PASS', 'target_coefficients': actual['target_coefficients'],
          'dependency_coefficients': actual['dependency_coefficients'],
          'weighted_sha256': actual['weighted_sha256'],
          'envelope_sha256': actual['envelope_sha256'],
          'weak_mean_minimum': actual['weak_mean']['minimum'],
          'record_sha256': digest(actual)}, sort_keys=True))


if __name__ == '__main__':
    main()
