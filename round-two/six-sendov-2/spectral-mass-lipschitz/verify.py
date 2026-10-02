#!/usr/bin/env python3
"""Exact certificates for sharp mass continuity and an angular symmetry tube.

Author six-sendov-2, researcher. Standard-library Fraction only.
Universal identities supplement the ordinary proof; no asserted gates.
Sparse polynomial and univariate helpers adapt this author's9353/9398.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Sparse rational polynomial in sixteen independent variables."""
    zero = (0,)*16

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
            require(all(len(k) == 16 for k in self.c), 'polynomial variable count')
        else:
            self.c = {self.zero: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in P(other).c.items():
            out[k] = out.get(k, F(0))+v
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for k, a in self.c.items():
            for l, b in P(other).c.items():
                key = tuple(i+j for i, j in zip(k, l))
                out[key] = out.get(key, F(0))+a*b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'bad power')
        out = P(1)
        for _ in range(exponent):
            out = out*self
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def encoded(self):
        return [[list(k), str(v)] for k, v in sorted(self.c.items())]


def variable(index):
    key = [0]*16
    key[index] = 1
    return P({tuple(key): 1})


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()


def polynomial_identities(damage=None):
    r = [variable(i) for i in range(8)]
    v = [variable(i+8) for i in range(8)]
    S = sum((x*x for x in r), P(0))
    B = sum((x**3 for x in r), P(0))
    C = sum((x*x*y for x, y in zip(r, v)), P(0))
    A = sum((x**3*y for x, y in zip(r, v)), P(0))
    R4 = sum((x**4 for x in r), P(0))
    V2 = sum((x*x*y*y for x, y in zip(r, v)), P(0))
    covariance = sum((r[i]**2*r[j]**2*(r[i]-r[j])*(v[i]-v[j])
                      for i, j in combinations(range(8), 2)), P(0))
    if damage == 'covariance_sign':
        covariance = -covariance
    require(S*A-B*C == covariance, 'universal covariance identity')
    vr = sum((r[i]**2*r[j]**2*(r[i]-r[j])**2
              for i, j in combinations(range(8), 2)), P(0))
    vv = sum((r[i]**2*r[j]**2*(v[i]-v[j])**2
              for i, j in combinations(range(8), 2)), P(0))
    require(S*R4-B*B == vr, 'universal reciprocal variance identity')
    require(S*V2-C*C == vv, 'universal velocity variance identity')
    # Clear S in r_i'=-r_i^2(v_i-C/S), then differentiate S.
    sdot_numerator = -2*sum((x**3*(S*y-C) for x, y in zip(r, v)), P(0))
    require(-64*sdot_numerator == 128*(S*A-B*C), 'mass derivative numerator')
    n, s, delta = [variable(i) for i in range(3)]
    expanded = 2*delta*(delta-n)+(n-2)*(delta*delta-s*s)
    expected = n*delta*delta-2*n*delta-(n-2)*s*s
    if damage == 'sharp_quadratic':
        expected = expected+s*s
    require(expanded == expected, 'universal sharp-family critical quadratic')
    polys = {'covariance': covariance, 'reciprocal_variance': vr,
             'velocity_variance': vv, 'mass_derivative_numerator': 128*covariance,
             'sharp_family_quadratic': expected}
    return {k: {'terms': len(p.c), 'sha256': hashlib.sha256(canonical(p.encoded())).hexdigest()}
            for k, p in polys.items()}


class Dual:
    def __init__(self, value=0, derivative=0):
        if isinstance(value, Dual):
            self.value, self.derivative = value.value, value.derivative
        else:
            self.value, self.derivative = F(value), F(derivative)

    def __add__(self, other):
        other = Dual(other)
        return Dual(self.value+other.value, self.derivative+other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self+-Dual(other)

    def __rsub__(self, other):
        return Dual(other)+-self

    def __mul__(self, other):
        other = Dual(other)
        return Dual(self.value*other.value,
                    self.derivative*other.value+self.value*other.derivative)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Dual(other)
        require(other.value != 0, 'dual nonunit division')
        return Dual(self.value/other.value,
                    (self.derivative*other.value-self.value*other.derivative)/other.value**2)

    def __rtruediv__(self, other):
        return Dual(other)/self


def matmul(left, right):
    return [[sum((left[i][k]*right[k][j] for k in range(len(right))), Dual())
             for j in range(len(right[0]))] for i in range(len(left))]


def mateval(coefficients, x):
    n = len(x)
    out = [[Dual() for _ in range(n)] for _ in range(n)]
    for coefficient in reversed(coefficients):
        out = matmul(out, x)
        for i in range(n):
            out[i][i] += coefficient
    return out


def matinv(matrix):
    n = len(matrix)
    a = [[Dual(x) for x in row]+[Dual(int(i == j)) for j in range(n)]
         for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j].value != 0), None)
        require(pivot is not None, 'squarefree critical sample')
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [x/divisor for x in a[j]]
        for i in range(n):
            if i == j:
                continue
            factor = a[i][j]
            a[i] = [x-factor*y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def dual_eta(originals, velocities, damage=None):
    n = len(originals)
    f = [Dual(1)]
    for u, v in zip(originals, velocities):
        out = [Dual()]*(len(f)+1)
        for i, value in enumerate(f):
            out[i] -= Dual(u, v)*value
            out[i+1] += value
        f = out
    h = [F(i, n)*f[i] for i in range(1, n+1)]
    hp = [i*h[i] for i in range(1, n)]
    x = [[Dual() for _ in range(n-1)] for _ in range(n-1)]
    for i in range(n-1):
        x[i][-1] = -h[i]
        if i:
            x[i][i-1] += 1
    if damage == 'freeze_nodes':
        x = [[Dual(q.value) for q in row] for row in x]
    m = matmul(mateval(f, x), matinv(mateval(hp, x)))
    factor = -n if damage != 'mass_scale' else F(-n, 2)
    m = [[factor*x for x in row] for row in m]
    square = matmul(m, m)
    eta = sum((square[i][i] for i in range(n-1)), Dual())
    return eta, [q.value for q in f], [q.derivative for q in f]


def trim(poly):
    out = [F(x) for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def add(left, right):
    return trim([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
                 for i in range(max(len(left), len(right)))])


def scale(value, poly):
    return trim([value*x for x in poly])


def mul(left, right):
    out = [F(0)]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] += a*b
    return trim(out)


def divide(left, right):
    left, right = trim(left), trim(right)
    require(right != [F(0)], 'zero polynomial divisor')
    out = [F(0)]*max(1, len(left)-len(right)+1)
    while left != [F(0)] and len(left) >= len(right):
        k, a = len(left)-len(right), left[-1]/right[-1]
        out[k] += a
        left = add(left, [F(0)]*k+scale(-a, right))
    return trim(out), left


def inverse(poly, modulus):
    r0, r1, s0, s1 = trim(modulus), trim(poly), [F(0)], [F(1)]
    while r1 != [F(0)]:
        q, rem = divide(r0, r1)
        r0, r1, s0, s1 = r1, rem, s1, add(s0, scale(-1, mul(q, s1)))
    require(len(r0) == 1 and r0[0] != 0, 'squarefree quotient control')
    result = divide(scale(1/r0[0], s0), modulus)[1]
    require(divide(mul(poly, result), modulus)[1] == [F(1)], 'Euclid inverse control')
    return result


def derivative(poly):
    return trim([i*poly[i] for i in range(1, len(poly))] or [F(0)])


def quotient_gradient(f, q):
    n = len(f)-1
    h = scale(F(1, n), derivative(f))
    hp, hpp = derivative(h), derivative(derivative(h))
    inv = inverse(hp, h)

    def rem(p):
        return divide(p, h)[1]

    m = rem(scale(-n, mul(f, inv)))
    m2 = rem(mul(m, m))
    qp, qpp = derivative(q), derivative(derivative(q))
    # General-n form of the credited9271 full moving-node variation.
    value = add(scale(-2*n, mul(mul(m, q), inv)),
                scale(F(-2, n), mul(mul(m2, qpp), inv)))
    value = add(value, scale(F(2, n), mul(mul(mul(m2, hpp), qp), mul(inv, inv))))
    moments = [F(n-1)]
    for k in range(1, n-1):
        moments.append(-sum((h[n-1-i]*moments[k-i] for i in range(1, k)), F(0))
                       -k*h[n-1-k])

    def trace(poly):
        return sum((a*moments[i] for i, a in enumerate(rem(poly))), F(0))

    return trace(m2), trace(value)


def differential_controls(damage=None):
    cases = [
        ([-4, -3, -2, -1, 1, 2, 3, 4], [1, 0, -1, 2, -2, 1, 0, -1]),
        ([-7, -5, -3, -1, 2, 3, 4, 7], [1, 2, -3, 4, -4, 3, -2, -1]),
        ([-5, -3, -2, -1, 0, 1, 4, 6], [-2, 1, 3, -1, 2, -3, 1, -1]),
        ([-3, -3, -1, 1, 3, 3, -2, 2], [0, 0, 1, -1, 0, 0, 2, -2]),
        ([-F(11, 10), -1, -F(9, 10), 0, 0, F(9, 10), 1, F(11, 10)],
         [-1, 0, 1, 0, 0, -1, 0, 1]),
    ]
    out = []
    for u, v in cases:
        require(sum(u) == sum(v) == 0 and len(u) == len(v) == 8, 'balanced control')
        eta, f, q = dual_eta(u, v, damage)
        exact_eta, exact_derivative = quotient_gradient(f, q)
        require(eta.value == exact_eta, 'independent mass-square trace value')
        require(eta.derivative == exact_derivative, 'independent full moving-node derivative')
        N = sum(F(x)**2 for x in u)
        speed = max(abs(F(x)) for x in v)
        require(eta.derivative**2 <= 512*N**3*speed**2, 'eta differential bound')
        Gdot = 16*N*sum(F(x)*F(y) for x, y in zip(u, v))-eta.derivative
        Gdot -= 96*sum(F(x)**3*F(y) for x, y in zip(u, v))
        require(Gdot**2 < 164**2*N**3*speed**2, 'angular gap differential bound')
        out.append({'originals': [str(x) for x in u], 'velocities': [str(x) for x in v],
                    'N': str(N), 'eta': str(eta.value), 'eta_dot': str(eta.derivative),
                    'G24_dot': str(Gdot)})
    return out


def scalar_certificates(damage=None):
    delta = F(69, 5000) if damage != 'large_variance' else F(1, 1000)
    upper = 164 if damage != 'gap_constant' else 163
    require(upper > 96 and (upper-96)**2 > 2*48**2, 'rational gap Lipschitz constant')
    require(F(7, 8)*delta < F(11, 100)**2, 'small variance squared-root bound')
    require(F(3, 200) > F(3, 25)**2, 'positive root lower magnitude')
    require(F(1, 8) > F(7, 20)**2, 'uniform radius lower magnitude')
    require(delta/F(47, 100)**2 < F(1, 16), 'balanced sign-count contradiction')
    require(F(1, 224) < delta, 'complete large-variance case')
    # Range variance, collision gap and sharp n2 controls.
    reciprocal_variance = F(1)
    claimed_variance = F(1) if damage != 'range_constant' else F(1, 2)
    require(reciprocal_variance <= claimed_variance, 'two-pole sharp variance control')
    gap_bound = F(1, 8) if damage != 'collision_gap' else F(1, 16)
    require(F(2) <= 4*4*gap_bound, 'two-root collision gap bound')
    T = F(24531, 1000)
    d0 = (T-16)**2/(56*T*T)
    rho = (T-24)*d0/F(164)
    require(rho == F(4293899699, 614072813536000), 'exact symmetry tube radius')
    require(rho > F(1, 144000) and rho < F(1, 143000), 'reader-friendly radius bracket')
    strong_upper = 162 if damage != 'review_gap_constant' else 161
    require(strong_upper > 94 and (strong_upper-94)**2 > 2*F(95, 2)**2,
            'review-based rational gap Lipschitz constant')
    strong_rho = (T-F(47, 2))*d0/strong_upper
    require(strong_rho == F(75034077791, 5459257086192000),
            'review-based exact symmetry tube radius')
    require(F(1, 73000) < strong_rho < F(1, 72000),
            'review-based reader-friendly radius bracket')
    thresholds = [{'T': str(t), 'variance_lower': str((t-16)**2/(56*t*t)),
                   'asymmetry_lower_original24': str((t-24)*(t-16)**2/(9184*t*t)),
                   'asymmetry_lower_review47over2': str((t-F(47, 2))*(t-16)**2/(9072*t*t))}
                  for t in [F(49, 2), T, F(25), F(32)]]
    # The all-T proof uses monotonicity (T-16)/T and the exact endpoint1/224.
    return {'Delta': str(delta), 'gap_Lipschitz_rational': upper,
            'irrational_square_margin': str(F((upper-96)**2-2*48**2)),
            'sign_count_margin': str(F(1, 16)-delta/F(47, 100)**2),
            'large_variance_margin': str(delta-F(1, 224)),
            'thresholds': thresholds, 'rho_T24531': str(rho),
            'rho_comparison_margin': str(rho-F(1, 144000)),
            'review_gap_Lipschitz_rational': strong_upper,
            'review_irrational_square_margin': str((strong_upper-94)**2-2*F(95, 2)**2),
            'rho_review_T24531': str(strong_rho),
            'rho_review_comparison_margin': str(strong_rho-F(1, 73000))}


def collision_and_pairing_controls(damage=None):
    records = []
    for u in [[-1, -1, -1, 0, 0, 1, 1, 1], [-1]*4+[1]*4]:
        gaps = [F(u[i+1]-u[i]) for i in range(7)]
        masses = [F(0)]*7
        if u[3] == 0:
            masses[2] = masses[4] = F(3)
            nodes = [F(-1), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(1)]
        else:
            masses[3] = F(8)
            nodes = [F(-1)]*3+[F(0)]+[F(1)]*3
        if damage == 'collision_weight':
            masses[0] = 1
        f = [F(1)]
        for value in u:
            f = mul(f, [-F(value), F(1)])
        hp = derivative(f)
        for j, (lam, mass, gap) in enumerate(zip(nodes, masses, gaps)):
            require(sum(a*lam**k for k, a in enumerate(hp)) == 0,
                    'exact collision critical node')
            if gap:
                require(F(u[j]) < lam < F(u[j+1]), 'exact active interlacing node')
                reciprocals = [1/(F(x)-lam) for x in u]
                require(sum(reciprocals) == 0, 'exact active reciprocal equation')
                require(mass == 64/sum(x*x for x in reciprocals),
                        'independently computed active collision mass')
            else:
                require(lam == u[j] == u[j+1] and mass == 0,
                        'exact collapsed gap has zero whole-projection mass')
        require(all(m <= 8*g*g for m, g in zip(masses, gaps)), 'whole collision zero weight')
        require(sum(masses) == sum(F(x)**2 for x in u), 'whole collision total mass')
        records.append({'originals': u, 'ordered_critical_nodes': [str(x) for x in nodes],
                        'ordered_masses': [str(m) for m in masses],
                        'eta': str(sum(m*m for m in masses))})
    u = [F(x) for x in [-7, -5, -3, -1, 2, 3, 4, 7]]
    v = [(u[i]-u[7-i])/2 for i in range(8)]
    if damage == 'pairing':
        v = [(u[i]-u[7-i]) for i in range(8)]
    epsilon = max(abs(u[i]+u[7-i]) for i in range(8))/2
    require(v == [-x for x in reversed(v)] and sum(v) == 0, 'symmetric projection')
    require(all(v[i] <= v[i+1] for i in range(7)), 'ordered symmetric projection')
    require(max(abs(x-y) for x, y in zip(u, v)) == epsilon, 'closest symmetric bottleneck metric')
    require(sum(x*x for x in v) <= sum(x*x for x in u), 'projection norm contraction')
    return {'collisions': records, 'pairing': {'originals': [str(x) for x in u],
            'projection': [str(x) for x in v], 'asymmetry': str(epsilon)}}


def build_record(damage=None):
    record = {'author': 'six-sendov-2', 'role': 'researcher',
              'scope': 'all real balanced profiles, collisions included; sharp ordered square-root mass map',
              'stationarity_assumption': False,
              'general_n_sharp_sqrt_mass_Lipschitz': 'n/sqrt(2)',
              'general_n_eta_Lipschitz': '2*sqrt(2)*n*R^3',
              'eight_root_G24_Lipschitz': '(96+48*sqrt(2))*R^3 <164*R^3',
              'eight_root_G47over2_Lipschitz': '(94+95*sqrt(2)/2)*R^3 <162*R^3',
              'review47over2_is_explicit_prior_premise': True,
              'root_mass_polynomial_identities': polynomial_identities(damage),
              'exact_differential_controls': differential_controls(damage),
              'scalar_certificate': scalar_certificates(damage),
              'collision_and_projection_controls': collision_and_pairing_controls(damage)}
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    record = build_record()
    rejected = []
    for damage in ['covariance_sign', 'sharp_quadratic', 'freeze_nodes', 'mass_scale',
                   'large_variance', 'gap_constant', 'review_gap_constant', 'range_constant', 'collision_gap',
                   'collision_weight', 'pairing']:
        try:
            build_record(damage)
        except ValueError as err:
            rejected.append({'damage': damage, 'rejection': str(err)})
        else:
            raise ValueError('unchecked mathematical damage: '+damage)
    record['rejected_mathematical_damages'] = rejected
    if args.emit:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    require(json.loads(args.expected.read_text()) == record, 'whole expected record mismatch')
    print(json.dumps({'status': 'PASS', 'record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
                      'universal_polynomial_identities': 5, 'dual_and_Euclid_differential_controls': 5,
                      'collision_controls': 2, 'mathematical_damages': len(rejected)}))


if __name__ == '__main__':
    main()
