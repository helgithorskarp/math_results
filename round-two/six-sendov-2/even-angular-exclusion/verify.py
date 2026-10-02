#!/usr/bin/env python3
"""Exact even angular exclusion certificates. Author six-sendov-2.

Standard-library Fraction arithmetic. Complete polynomial identities and
finite sign certificates accompany the ordinary proof in PROOF.md.
The sparse arithmetic adapts the credited heat-tangent-rank checker.
No assert-based gates, CAS, numerical roots or external proof input.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse
from math import comb
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Sparse exact bivariate polynomial. No CAS and no polynomial division."""
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(a) for k, a in value.items() if a}
        else:
            self.c = {(0, 0): F(value)} if value else {}

    def __add__(self, other):
        other = P(other)
        out = dict(self.c)
        for k, a in other.c.items():
            out[k] = out.get(k, F(0)) + a
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -a for k, a in self.c.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        other = P(other)
        out = {}
        for (i, j), a in self.c.items():
            for (k, l), b in other.c.items():
                key = (i + k, j + l)
                out[key] = out.get(key, F(0)) + a * b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "bad power")
        out, base = P(1), self
        while exponent:
            if exponent & 1:
                out = out * base
            base = base * base
            exponent //= 2
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def at(self, d, v):
        return sum((a * d**i * v**j for (i, j), a in self.c.items()), F(0))

    def diff(self, variable):
        out = {}
        for key, value in self.c.items():
            if key[variable]:
                new = list(key)
                new[variable] -= 1
                out[tuple(new)] = value * key[variable]
        return P(out)

    def substitute(self, first, second):
        return sum((value * first**i * second**j for (i, j), value in self.c.items()), P(0))

    def encoded(self):
        return [[i, j, str(a)] for (i, j), a in sorted(self.c.items())]


def determinant(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare matrix")
    out = 0
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = (-1)**inversions
        for i, j in enumerate(perm):
            term = term * matrix[i][j]
        out = out + term
    return out


def adjugate3(matrix):
    return [[(-1)**(i + j) * determinant([
        [matrix[r][c] for c in range(3) if c != i]
        for r in range(3) if r != j
    ]) for j in range(3)] for i in range(3)]


def ident(n):
    return [[P(int(i == j)) for j in range(n)] for i in range(n)]


def madd(left, right):
    return [[x+y for x, y in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]


def scale(value, matrix):
    return [[value*x for x in row] for row in matrix]


def mmul(left, right):
    return [[sum((left[i][k]*right[k][j] for k in range(len(right))), P(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def mpow(matrix, exponent):
    out = ident(len(matrix))
    for _ in range(exponent):
        out = mmul(out, matrix)
    return out


def tr(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), P(0))


def interior(damage=None):
    a, b = P({(1, 0): 1}), P({(0, 1): 1})
    eye = ident(3)
    x = [[P(0), P(0), -b*F(1, 4)],
         [P(1), P(0), -a*F(1, 2)],
         [P(0), P(1), P(F(3, 8))]]
    z = madd(madd(scale(3, mpow(x, 3)), scale(F(-3, 4), mpow(x, 2))),
             scale(a*F(1, 2), x))
    L = 256*a**3-18*a*a+432*a*b+864*b*b-27*b
    H = 512*a**3-36*a*a+736*a*b+1344*b*b-45*b
    U = 16*a*a-a+6*b
    W = 4096*a**4-512*a**3+7680*a*a*b+18*a*a-816*a*b+1440*b*b+27*b
    J = 8192*a**4-1024*a**3+13312*a*a*b+36*a*a-1376*a*b+2496*b*b+45*b
    V = 8192*a**4+13312*a*a*b-36*a*a+96*a*b+5184*b*b-45*b
    A = 32*a-3
    FF = 4*a*a-112*a*b+15*b
    GG = 256*a**3-20*a*a+208*a*b-15*b
    dz = determinant(z)
    require(dz == -b*L*F(1, 2048), 'interior inverse determinant')
    adj = adjugate3(z)
    require(mmul(z, adj) == scale(dz, eye), 'interior adjugate')
    p0 = madd(madd(madd(mpow(x, 4), scale(F(-1, 2), mpow(x, 3))),
                   scale(a, mpow(x, 2))), scale(b, x))
    y0, y1 = scale(-4, mmul(p0, adj)), scale(-4, adj)
    den = b*b*dz*dz
    ns = [2*b*b*tr(mmul(y0, y0)), 4*b*b*tr(mmul(y0, y1)),
          1024*dz*dz+2*b*b*tr(mmul(y1, y1))]
    e2 = 768*H if damage != 'quadratic' else -768*H
    require(2*L*ns[0] == -W*den, 'eta constant identity')
    require(L*ns[1] == -3072*U*den, 'eta linear identity')
    require(b*b*L*ns[2] == e2*den, 'eta quadratic identity')
    cstar_num = (2 if damage != 'center' else 1)*b*b*U
    require(1536*H*cstar_num == 3072*b*b*U*H, 'constant center identity')
    require(W*H+6144*b*b*U*U == L*J, 'centered eta identity')
    require(2*H+J == V, 'centered C identity')
    factor = 768*FF*GG if damage != 'gradient' else -768*FF*GG
    require(V.diff(1)*H-V*H.diff(1) == factor, 'factored b gradient')

    def substitute_b(poly, num, div):
        degree = max(j for i, j in poly.c)
        return sum((value*a**i*num**j*div**(degree-j)
                    for (i, j), value in poly.c.items()), P(0)), degree

    fb, fd = -4*a*a, 15-112*a
    vf, vd = substitute_b(V, fb, fd)
    hf, hd = substitute_b(H, fb, fd)
    require(vd == hd == 2, 'F branch denominator degrees')
    require(vf*(448*a-45) == (224*a+15)*A*hf, 'F branch centered C')
    num, div = -4*(224*a+15), 448*a-45
    require(num.diff(0)*div-num*div.diff(0) == 67200, 'F branch derivative')
    gn, gd = -4*a*a*(64*a-5), 208*a-15
    lg, degree = substitute_b(L, gn, gd)
    TT = 27648*a*a-4960*a+225
    if damage == 'discriminant':
        TT = TT+1
    require(degree == 2 and lg == 2*a*a*A*A*TT, 'G branch discriminant')
    require(TT == 27648*(a-F(155, 1728))**2+F(275, 108),
            'G branch positive square')
    special = F(15, 208)
    require((4*a*a*(64*a-5)).at(special, F(0)) == -F(20, 13)*special**2,
            'G exceptional linear denominator')
    signs = {'a_upper': F(3, 32), 'F_den_lower': F(9, 2),
             'F_C_den_upper': F(-3), 'G_square_lower': F(275, 108),
             'F_gradient_numerator': F(67200)}
    require(15-112*signs['a_upper'] == signs['F_den_lower'], 'F domain bound')
    require(448*signs['a_upper']-45 == signs['F_C_den_upper'], 'F C domain bound')
    return {'polynomials': {name: poly.encoded() for name, poly in
            [('L', L), ('H', H), ('U', U), ('W', W), ('J', J), ('V', V),
             ('F', FF), ('G', GG), ('T', TT)]},
            'eta_common_denominator': den.encoded(),
            'eta_coefficient_numerators': [n.encoded() for n in ns],
            'exact_sign_data': {k: str(v) for k, v in signs.items()}}


def collision(damage=None):
    s, t = P({(1, 0): 1}), P({(0, 1): 1})
    eye = ident(2)
    x = [[P(0), -(s+2*t)*F(1, 4)], [P(1), (3*s+2)*F(1, 4)]]
    z = madd(scale(2, mpow(x, 2)), scale(-(3*s+2)*F(1, 4), x))
    K, V = 9*s*s-4*s+4-32*t, 3*s*s-4*s+4-8*t
    dz = determinant(z)
    require(dz == -(s+2*t)*K*F(1, 64), 'collision inverse determinant')
    adj = [[z[1][1], -z[0][1]], [-z[1][0], z[0][0]]]
    require(mmul(z, adj) == scale(dz, eye), 'collision adjugate')
    y = scale(-1, mmul(mmul(madd(x, scale(-1, eye)),
                           madd(scale(2-s, x), scale(2*t-s, eye))), adj))
    if damage == 'residue':
        y = scale(2, y)
    den = (s+2*t)**2*dz*dz
    eta_num = 1024*t*t*dz*dz+2*(s+2*t)**2*tr(mmul(y, y))
    R = (9*s**6+36*s**5*t+96*s**5+36*s**4*t*t+384*s**4*t-104*s**4
         +384*s**3*t*t+32*s**3*t+64*s**3-7200*s*s*t*t+384*s*s*t
         +16*s*s-1792*s*t**3+768*s*t*t+64*s*t-512*t**4+18944*t**3-3008*t*t)
    require((4*(s+2)**2*den-eta_num)*(s+2*t)**2*K == 2*R*den,
            'collision rational C identity')
    W24 = (153*s**6+612*s**5*t-384*s**5+612*s**4*t*t-2544*s**4*t+488*s**4
           -5568*s**3*t*t+2464*s**3*t-256*s**3-4032*s*s*t**3+14112*s*s*t*t
           -2112*s*s*t+80*s*s+11776*s*t**3-5376*s*t*t+320*s*t+6656*t**4
           -22784*t**3+3392*t*t)
    require(6*(s+2*t)**2*V*K-R == W24, '24 gap numerator')
    w = P({(0, 1): 1})
    Q = W24.substitute(s, s*s*(1-w)*F(1, 4))
    require(all(i >= 2 for i, j in Q.c), 'gap S square division')
    pp = P({(i-2, j): value for (i, j), value in Q.c.items()})
    literal = (26*s**6*w**4-41*s**6*w**3+F(21, 4)*s**6*w*w+F(17, 2)*s**6*w
               +F(5, 4)*s**6-184*s**5*w**3+204*s**5*w*w-9*s**5*w-11*s**5
               +356*s**4*w**3-186*s**4*w*w-60*s**4*w+43*s**4-336*s**3*w*w
               +56*s**3*w-104*s**3+212*s*s*w*w+104*s*s*w+172*s*s-80*s*w-176*s+80)
    require(pp == literal, 'gap P identity')
    cap = 24 if damage != 'cap' else 23
    require(cap*(s+2*t)**2*V*K-4*R == 4*W24, 'gap cap normalization')
    require(K.substitute(s, s*s*(1-w)*F(1, 4)) == (s-2)**2+8*s*s*w,
            'positive K denominator')
    require(V.substitute(s, s*s*(1-w)*F(1, 4)) == (s-2)**2+2*s*s*w,
            'positive V denominator')
    return pp, {'R': R.encoded(), 'W24': W24.encoded(), 'P': pp.encoded(),
                'common_mass_denominator': den.encoded()}


def bernstein(poly, m, n):
    require(all(i <= m and j <= n for i, j in poly.c), 'Bernstein degrees')
    return [[sum((value*F(comb(i, k), comb(m, k))*F(comb(j, l), comb(n, l))
                  for (k, l), value in poly.c.items() if k <= i and l <= j), F(0))
             for j in range(n+1)] for i in range(m+1)]


def reconstruct_bernstein(coeffs):
    m, n = len(coeffs)-1, len(coeffs[0])-1
    x, y = P({(1, 0): 1}), P({(0, 1): 1})
    return sum((coeffs[i][j]*comb(m, i)*comb(n, j)*x**i*(1-x)**(m-i)
                *y**j*(1-y)**(n-j) for i in range(m+1) for j in range(n+1)), P(0))


def positivity(pp, damage=None):
    x, w = P({(1, 0): 1}), P({(0, 1): 1})
    rectangles = [(F(0), F(1, 2), F(0), F(1)),
                  (F(1, 2), F(1), F(0), F(1, 2)),
                  (F(1, 2), F(1), F(1, 2), F(1)),
                  (F(1), F(3, 2), F(0), F(1, 4)),
                  (F(1), F(3, 2), F(1, 4), F(1, 2)),
                  (F(1), F(3, 2), F(1, 2), F(1)),
                  (F(3, 2), F(2), F(0), F(1))]
    lower = []
    for index, (lo, hi, wl, wh) in enumerate(rectangles):
        pol = pp.substitute(lo+(hi-lo)*x, wl+(wh-wl)*w)
        bs = bernstein(pol, 6, 4)
        if damage == 'bernstein' and index == 0:
            bs[0][0] += 1
        require(reconstruct_bernstein(bs) == pol, 'Bernstein reconstruction')
        minimum = min(v for row in bs for v in row)
        require(minimum >= 0, 'lower gap positivity')
        if index < len(rectangles)-1:
            require(minimum > 0, 'first six patches strict')
        else:
            require(bs[0][0] > 0 and bs[0][4] > 0, 'last patch strict for S below 2')
        lower.append({'rectangle': [str(lo), str(hi), str(wl), str(wh)],
                      'minimum': str(minimum),
                      'coefficients': [[str(v) for v in row] for row in bs]})
    shifted = pp.substitute(2+x, w)
    by_w = []
    for j in range(5):
        p = sum((value*F(comb(j, l), comb(4, l))*x**i
                 for (i, l), value in shifted.c.items() if l <= j), P(0))
        require(all(v >= 0 for v in p.c.values()), 'upper coefficient positivity')
        by_w.append(p)
    require(sum((by_w[j]*comb(4, j)*w**j*(1-w)**(4-j) for j in range(5)), P(0))
            == shifted, 'upper Bernstein reconstruction')
    require(all(by_w[j].at(F(0), F(0)) > 0 for j in [2, 3, 4]),
            'strict upper at S2 w positive')
    require(by_w[0] == x**4*(5*x*x+16*x+32)*F(1, 4),
            'strict upper at S greater than 2 w zero')
    expected_rectangles = [list(r) for r in rectangles]
    for si in range(4):
        lo, hi = F(si, 2), F(si+1, 2)
        intervals = sorted((r[2], r[3]) for r in rectangles if r[0] == lo and r[1] == hi)
        require(intervals[0][0] == 0 and intervals[-1][1] == 1 and
                all(intervals[k][1] == intervals[k+1][0] for k in range(len(intervals)-1)),
                'complete rectangle cover')
    require(len(expected_rectangles) == 7, 'rectangle count')
    return {'lower_patches': lower, 'lower_signs': 245,
            'upper_power_coefficients': [p.encoded() for p in by_w],
            'strict_zero_exception': ['2', '0']}


def trim(poly):
    out = [F(v) for v in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def uadd(left, right):
    return trim([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
                 for i in range(max(len(left), len(right)))])


def uscale(value, poly):
    return trim([value*v for v in poly])


def umul(left, right):
    out = [F(0)]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] += a*b
    return trim(out)


def udiv(left, right):
    left, right = trim(left), trim(right)
    require(right != [F(0)], 'univariate zero divisor')
    out = [F(0)]*max(1, len(left)-len(right)+1)
    while left != [F(0)] and len(left) >= len(right):
        k, coeff = len(left)-len(right), left[-1]/right[-1]
        out[k] += coeff
        left = uadd(left, [F(0)]*k+uscale(-coeff, right))
    return trim(out), left


def uinv(poly, modulus):
    r0, r1, s0, s1 = trim(modulus), trim(poly), [F(0)], [F(1)]
    while r1 != [F(0)]:
        quotient, rem = udiv(r0, r1)
        r0, r1, s0, s1 = r1, rem, s1, uadd(s0, uscale(-1, umul(quotient, s1)))
    require(len(r0) == 1 and r0[0] != 0, 'critical polynomial must be squarefree')
    result = udiv(uscale(1/r0[0], s0), modulus)[1]
    require(udiv(umul(poly, result), modulus)[1] == [F(1)], 'inverse identity')
    return result


def full_eta(poly):
    """Seven-node Newton/Euclid computation independent of paired matrices."""
    f = trim(poly)
    require(len(f) == 9 and f[-1] == 1 and f[-2] == 0, 'balanced monic octic')
    h = [F(i, 8)*f[i] for i in range(1, 9)]
    hp = [i*h[i] for i in range(1, 8)]
    mass = udiv(uscale(-8, umul(f, uinv(hp, h))), h)[1]
    squared = udiv(umul(mass, mass), h)[1]
    moments = [F(7)]
    for k in range(1, 7):
        moments.append(-sum((h[7-i]*moments[k-i] for i in range(1, k)), F(0))-k*h[7-k])
    eta = sum((value*moments[i] for i, value in enumerate(squared)), F(0))
    N = -2*f[6]
    D = F(3, 8)*N*N-4*f[4]
    require(N > 0 and D > 0, 'nondegenerate sample domain')
    return N, D, eta, (N*N-eta)/D


def pair_polynomial(pairs):
    result = [F(1)]
    for radius in pairs:
        result = umul(result, [-F(radius)**2, F(0), F(1)])
    return result


def controls(interior_record, collision_record):
    ps = {key: P({(i, j): F(v) for i, j, v in values})
          for key, values in interior_record['polynomials'].items()}
    rr = P({(i, j): F(v) for i, j, v in collision_record['R']})
    out = []
    for radii in [(1, 2, 3, 4), (1, 3, 5, 7), (10, 11, 12, 13), (1, 2, 3, 20)]:
        f = pair_polynomial(radii)
        N, D, eta, C = full_eta(f)
        a, b, c = f[4]/N**2, f[2]/N**3, f[0]/N**4
        L, H, U, W = [ps[key].at(a, b) for key in ['L', 'H', 'U', 'W']]
        predicted = -W/(2*L)-3072*U*c/L+768*H*c*c/(b*b*L)
        require(eta/N**2 == predicted, 'independent interior full-node control')
        require(0 < a < F(3, 32) and b < 0 and c > 0 and L < 0 and H < 0,
                'feasible interior sample signs')
        out.append({'type': 'distinct', 'radii': list(radii), 'N': str(N),
                    'D': str(D), 'eta': str(eta), 'C': str(C)})
    for repeated, light, other in [(3, 1, 2), (5, 3, 4), (2, 1, 3), (1, 2, 3), (5, 1, 7)]:
        f = pair_polynomial([repeated, repeated, light, other])
        N, D, eta, C = full_eta(f)
        S = F(light*light+other*other, repeated*repeated)
        T = F(light*light*other*other, repeated**4)
        K, V = 9*S*S-4*S+4-32*T, 3*S*S-4*S+4-8*T
        require(K > 0 and V > 0 and T > 0 and 4*T < S*S, 'collision sample domain')
        predicted = 4*rr.at(S, T)/((S+2*T)**2*V*K)
        require(C == predicted and C < 24, 'independent paired full-node control')
        out.append({'type': 'paired_collision', 'radii': [repeated, repeated, light, other],
                    'S': str(S), 'T': str(T), 'C': str(C), 'eta': str(eta)})
    f = pair_polynomial([0, 1, 2, 3])
    N, D, eta, C = full_eta(f)
    require(eta >= N*N/6 and D >= N*N/F(6)-N*N/F(8) and C <= 20,
            'zero-original full-node control')
    out.append({'type': 'double_zero', 'N': str(N), 'D': str(D), 'eta': str(eta), 'C': str(C)})
    f = pair_polynomial([1, 3, 5, 7])
    f[0] -= F(1294848, 280993)
    N, D, eta, C = full_eta(f)
    a, b, c = f[4]/N**2, f[2]/N**3, f[0]/N**4
    require(c == 2*b*b*ps['U'].at(a, b)/ps['H'].at(a, b), 'credited legal center benchmark')
    require(C == F(2522064, 280993), 'credited centered benchmark C')
    out.append({'type': 'credited_9323_center', 'a': str(a), 'b': str(b), 'c': str(c),
                'C': str(C)})
    uniform = pair_polynomial([1, 1, 1, 1])
    N = -2*uniform[6]
    require(F(3, 8)*N*N-4*uniform[4] == 0, 'uniform denominator control')
    zero_bounds = {str(q): str(F(8*(q-1), 8-q)) for q in range(2, 7)}
    require(max(F(v) for v in zero_bounds.values()) == 20, 'zero-original dimension bound')
    return {'independent_full_node_samples': out, 'zero_original_C_bounds': zero_bounds,
            'uniform_N': str(N), 'uniform_continuous_C_from_8753': '16'}


def build_record():
    i = interior()
    pp, c = collision()
    return {'author': 'six-sendov-2', 'role': 'researcher',
            'scope': 'real reflection-symmetric original-root angular C<24; no first-power endpoint proof',
            'interior': i, 'collision': c, 'gap_positivity': positivity(pp),
            'controls': controls(i, c)}


def damage_checks():
    rejected = []
    for damage in ['quadratic', 'center', 'gradient', 'discriminant', 'residue', 'cap', 'bernstein']:
        try:
            interior(damage)
            pp, _ = collision(damage)
            positivity(pp, damage)
        except ValueError as err:
            rejected.append({'damage': damage, 'rejection': str(err)})
        else:
            raise ValueError('damage unexpectedly accepted: '+damage)
    return rejected


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit', action='store_true', help='emit current exact record, before publication')
    args = parser.parse_args()
    record = build_record()
    record['rejected_mathematical_damages'] = damage_checks()
    if args.emit:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    expected = json.loads(args.expected.read_text())
    require(expected == record, 'whole expected record mismatch')
    digest = hashlib.sha256(canonical(record)).hexdigest()
    print('PASS: universal interior and collision identities; seven complete exact gap patches;')
    print('245 nonnegative lower Bernstein coefficients and positive upper certificates;')
    print('11 independent full-node controls; seven rejected mathematical damages.')
    print('Record SHA256: '+digest)


if __name__ == '__main__':
    main()
