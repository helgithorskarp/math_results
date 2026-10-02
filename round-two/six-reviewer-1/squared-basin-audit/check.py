"""Independent rational certificate for the new part of Lemma9189.

No author executable or data is imported. Only fractions/math/json/hashlib
and other Python standard-library modules are used. Derivative budgets use
one-variable directional Taylor coefficients plus polarization, rather
than the author's rectangular multivariate quotient ring.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json
import signal

MU = Q(22096964222976, 21378414915091)
ALPHA, BETA = Q(8, 13), Q(39, 64)
T, S0 = Q(1, 32), Q(1, 128)


def require(condition, label):
    if not condition:
        raise ValueError(label)


def trim(a):
    a = list(map(Q, a))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    c = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def scale(a, x):
    return trim([Q(x) * y for y in a])


def mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x * y
    return trim(c)


def power(a, k):
    c = [Q(1)]
    for _ in range(k):
        c = mul(c, a)
    return c


def shift(a, left, width):
    """Coefficient list of a(left+width*y)."""
    c = [Q(0)] * len(a)
    for j, x in enumerate(a):
        for k in range(j+1):
            c[k] += x * comb(j, k) * left**(j-k) * width**k
    return trim(c)


def bernstein(a, left, right, degree=None):
    n = len(a)-1 if degree is None else degree
    require(n >= len(trim(a))-1, 'Bernstein degree')
    shifted = shift(a, left, right-left)
    values = [sum((shifted[j] * Q(comb(i, j), comb(n, j))
                   for j in range(min(i, len(shifted)-1)+1)), Q(0))
              for i in range(n+1)]
    # Independent reconstruction in the power basis followed by inverse shift.
    back = [Q(0)]
    for i, v in enumerate(values):
        back = add(back, scale(mul([Q(0)]*i+[Q(1)],
                                  power([Q(1), Q(-1)], n-i)),
                               v*comb(n, i)))
    require(back == shifted, 'whole Bernstein power reconstruction')
    require(shift(back, -left/(right-left), 1/(right-left)) == trim(a),
            'whole Bernstein inverse coordinate reconstruction')
    return values


def integral_i(k, n):
    return [Q((-1)**j * comb(n, j), k+j+1) for j in range(n+1)]


def integral_j(k, n):
    result = [Q(0)]
    for j in range(n+1):
        result = add(result, scale(mul([Q(0)]*(n-j)+[Q(1)],
                                       power([Q(1), Q(-1)], j)),
                                   Q(comb(n, j), k+j+1)))
    return result


def primitive_coefficients():
    records = []
    caps = {name: {} for name in ['k', 'm', 'c', 'd']}
    identity_count = 0
    for family, indices in [('k', range(1, 8)), ('m', range(8)),
                            ('c', range(1, 8)), ('d', range(8))]:
        for k in indices:
            if family == 'k':
                poly = scale(mul([Q(0)]*k+[Q(1)],
                                 add(integral_i(k, 7-k),
                                     scale(mul([Q(0), Q(1)], integral_i(k+1, 7-k)), -9))), 9)
                den = power([Q(1), Q(-1)], k)
                left, right = Q(5, 13), Q(1, 2)
            elif family == 'm':
                poly = scale(mul([Q(0)]*(k+1)+[Q(1)], integral_i(k+1, 7-k)), 9)
                den = power([Q(1), Q(-1)], k+1)
                left, right = Q(5, 13), Q(1, 2)
            elif family == 'c':
                poly = mul(power([Q(1), Q(0), Q(-1)], k-1),
                           add(integral_j(k, 8-k),
                               scale(mul([Q(1), Q(-1)], integral_j(k+1, 7-k)), 8)))
                den = [Q(1)]
                left, right = Q(5, 8), Q(1)
            else:
                poly = mul(power([Q(1), Q(0), Q(-1)], k), integral_j(k+1, 7-k))
                den = [Q(1)]
                left, right = Q(5, 8), Q(1)
            degree = max(len(poly), len(den))-1
            bp, bd = bernstein(poly, left, right, degree), bernstein(den, left, right, degree)
            require(all(x > 0 for x in bd), 'positive rational cap denominator')
            cap = max(abs(x)/y for x, y in zip(bp, bd))
            require(cap > 0, 'nonzero cap')
            caps[family][k] = cap
            records.append({'family': family, 'index': k, 'numerator': poly,
                            'denominator': den, 'degree': degree,
                            'numerator_bernstein': bp, 'denominator_bernstein': bd,
                            'cap': cap})
    # Literal integration of the bivariate integrands is a second route to
    # every origin coefficient, including both model constants.
    for k in range(8):
        terms = []
        for j in range(8-k):
            terms.append(Q((-1)**j * comb(7-k, j), k+j+1))
        literal = add(terms, scale(mul([Q(0), Q(1)],
                                      [Q((-1)**j*comb(7-k, j), k+j+2)
                                       for j in range(8-k)]), -9))
        if k == 0:
            require(literal == power([Q(1), Q(-1)], 8), 'origin model integral')
        else:
            rec = next(r for r in records if r['family'] == 'k' and r['index'] == k)
            require(scale(mul([Q(0)]*k+[Q(1)], literal), 9) == rec['numerator'],
                    'literal origin coefficient')
        identity_count += 1
    # The polar model integrand is the derivative of t*(a+(1-a)*t)^8.
    require(add(mul([Q(0), Q(1)], integral_j(0, 7)),
                scale(mul([Q(1), Q(-1)], integral_j(1, 7)), 9)) == [Q(1)],
            'polar model integral')
    identity_count += 1
    return records, caps, identity_count


class Jet:
    """One-variable rational Taylor coefficients, variable degree <= n."""
    def __init__(self, value, n=4):
        self.n = n
        self.c = list(value)[:n+1] if isinstance(value, (list, tuple)) else [Q(value)]
        self.c = list(map(Q, self.c)) + [Q(0)]*(n+1-len(self.c))

    def cast(self, x):
        if isinstance(x, Jet):
            require(x.n == self.n, 'jet degree compatibility')
            return x
        return Jet(x, self.n)

    def __add__(self, x):
        x = self.cast(x)
        return Jet([a+b for a, b in zip(self.c, x.c)], self.n)
    __radd__ = __add__

    def __neg__(self):
        return Jet([-a for a in self.c], self.n)

    def __sub__(self, x):
        return self + -self.cast(x)

    def __rsub__(self, x):
        return self.cast(x) + -self

    def __mul__(self, x):
        x = self.cast(x)
        return Jet([sum((self.c[j]*x.c[k-j] for j in range(k+1)), Q(0))
                    for k in range(self.n+1)], self.n)
    __rmul__ = __mul__

    def inverse(self):
        require(self.c[0] != 0, 'zero jet denominator')
        result = [1/self.c[0]]
        for k in range(1, self.n+1):
            result.append(-sum((self.c[j]*result[k-j] for j in range(1, k+1)), Q(0))/self.c[0])
        inv = Jet(result, self.n)
        require((self*inv).c == [Q(1)]+[Q(0)]*self.n, 'whole jet inverse identity')
        return inv

    def __truediv__(self, x):
        return self*self.cast(x).inverse()

    def __rtruediv__(self, x):
        return self.cast(x)*self.inverse()

    def __pow__(self, k):
        require(isinstance(k, int) and k >= 0, 'jet integral power')
        out = Jet(1, self.n)
        for _ in range(k):
            out = out*self
        return out


def exp_bound(t):
    return 1+t+t*t/2+t**3/6+t**4/(24*(1-t/5))


def radial_bound(t):
    y = t*t
    return (y/4+ALPHA**2*y*y/(3*(1-5*y/3)))/(1-y/2-ALPHA*y*y/(3*(1-5*y/3)))


def majorants(t, s, z, caps):
    ee, hh = exp_bound(t), radial_bound(t)
    small = ALPHA*(Q(8, 3)*t+ee-1-t)+ee*(hh+s)
    heavy = 9*ALPHA*(ee-1)+ee*(hh+s+z)
    origin = sum((caps['k'][k]*small**k/factorial(k) for k in range(1, 8)), 0)
    origin += heavy*sum((caps['m'][k]*small**k/factorial(k) for k in range(8)), 0)
    polar = sum((caps['c'][k]*small**k/factorial(k) for k in range(1, 8)), 0)
    polar += heavy*sum((caps['d'][k]*small**k/factorial(k) for k in range(8)), 0)
    u = hh+s
    w = origin+Q(128, 9)*origin*origin
    w += Q(9, 2)*ALPHA**8*((1+Q(2, 9)*(u+z))**2*exp_bound(4*u)-1)
    w += MU*(polar+BETA*polar*polar/2)
    oa = sum((caps['m'][k]*small**k/factorial(k) for k in range(1, 8)), 0)
    pa = sum((caps['d'][k]*small**k/factorial(k) for k in range(1, 8)), 0)
    wb = Q(128, 9)*(2*caps['m'][0]*oa+oa*oa)
    wb += ALPHA**6/Q(18)*(exp_bound(4*u)-1)
    wb += MU*BETA/2*(2*caps['d'][0]*pa+pa*pa)
    return w, wb


def directional(caps, center, direction, degree, which=0):
    args = [Jet([v, dv], degree) for v, dv in zip(center, direction)]
    return majorants(*args, caps)[which].c[degree]


def derivative_budgets(caps):
    a = directional(caps, (0, S0, 0), (0, 1, 0), 2)
    # D^3(t+s)-D^3(t-s)-2D^3(s) = 6 W_tts.
    b = (directional(caps, (T, S0, 0), (1, 1, 0), 3)
         -directional(caps, (T, S0, 0), (1, -1, 0), 3)
         -2*directional(caps, (T, S0, 0), (0, 1, 0), 3))/2
    c = directional(caps, (T, 0, 0), (1, 0, 0), 4)
    d = (directional(caps, (0, S0, 0), (0, 1, 1), 2)
         -directional(caps, (0, S0, 0), (0, 1, 0), 2)
         -directional(caps, (0, S0, 0), (0, 0, 1), 2))
    e = (directional(caps, (T, S0, 0), (1, 0, 1), 3)
         -directional(caps, (T, S0, 0), (1, 0, -1), 3)
         -2*directional(caps, (T, S0, 0), (0, 0, 1), 3))/2
    f = directional(caps, (0, S0, 0), (0, 1, 0), 1, 1)
    g = directional(caps, (T, S0, 0), (1, 0, 0), 2, 1)
    values = dict(zip(['M_S', 'M_mix', 'M_4', 'M_KS', 'M_Kt', 'M_BS', 'M_Bt'],
                      [a, b, c, d, e, f, g]))
    bounds = dict(zip(values, [19, 800, 1200, 16, 210, 4, 11]))
    for name, v in values.items():
        require(0 < v < bounds[name], 'derivative bound '+name)
    return values, bounds


def heavy_curvature():
    ih = [Q(0)]
    for j in range(8):
        ih = add(ih, scale(mul([Q(0)]*j+[Q(1)], power([Q(1), Q(1)], 7-j)),
                           Q((-1)**j*comb(7, j), j+2)))
    jh = integral_j(1, 7)
    num = add(scale(mul([Q(0), Q(0), Q(1)], power(ih, 2)), 81), [Q(-1)])
    num = add(num, scale(mul(mul([Q(1), Q(0), Q(-1)], power([Q(1), Q(1)], 6)),
                             power(jh, 2)), -9*MU))
    positive = add(num, scale(power([Q(1), Q(1)], 6), Q(-9, 2)))
    values = bernstein(positive, Q(5, 8), Q(1))
    require(len(values) == 23 and min(values) > 0, 'full heavy curvature >1/4')
    return {'cleared_numerator': num, 'cleared_quarter_margin': positive,
            'bernstein_margin': values, 'I1_h': ih, 'J1': jh}


def controls():
    total = 0
    for n in range(1, 6):
        for m in range(1, 7):
            for a in [Q(1, 2), Q(2, 3), Q(3, 4)]:
                p = Jet([a, -1], n)**m
                inv = p.inverse()
                for k in range(n+1):
                    require(inv.c[k] == Q(comb(m+k-1, k))*a**(-m-k),
                            'closed negative-binomial reciprocal')
                    total += 1
    # Exact polarization on every monomial of total degree <=4.
    for i in range(5):
        for j in range(5-i):
            tt, ss = Q(2, 5), Q(3, 7)
            fun = lambda dt, ds, n: ((Jet([tt, dt], n)**i)*(Jet([ss, ds], n)**j)).c[n]
            got = (fun(1, 1, 3)-fun(1, -1, 3)-2*fun(0, 1, 3))/2
            expected = Q(i*(i-1)*j, 2)*tt**max(i-2, 0)*ss**max(j-1, 0)
            require(got == expected, 'mixed-third derivative polarization')
            total += 1
            got = fun(1, 1, 2)-fun(1, 0, 2)-fun(0, 1, 2)
            expected = i*j*tt**max(i-1, 0)*ss**max(j-1, 0)
            require(got == expected, 'mixed-second derivative polarization')
            total += 1
    return total


def domain_checks():
    records = {}
    gamma_max = Q(3, 8)
    for label, sd, td in [('original', 64, 160000), ('enlarged', 52, 96000)]:
        s, t2 = gamma_max/sd, gamma_max/td
        gaps = {'S_majorant': S0-s, 'phase_majorant': T*T-t2,
                'slack_remainder': Q(3, 4)-Q(19, sd)-Q(800, td)-Q(3, 8),
                'phase_remainder': Q(1, 40)-Q(1200, td)-Q(1, 80),
                'heavy_derivative': Q(1, 8)-16*s-210*t2,
                'heavy_curvature': Q(1, 8)-4*s-11*t2}
        require(all(v >= 0 for v in gaps.values()), 'domain budget '+label)
        require(gaps['heavy_derivative'] > 0 and gaps['heavy_curvature'] > 0,
                'strict heavy margins '+label)
        records[label] = {'slack_denominator': sd, 'phase_squared_denominator': td,
                          'gaps': gaps}
    # A real collapsed polynomial at a=1 gives S=1/160, zero phases.
    r = Q(561, 1120)
    slack = 7*(r-Q(1, 2))
    other_root = 1-1/r
    require(slack == Q(1, 160) and abs(other_root) < 1, 'real collapsed witness')
    require(slack > gamma_max/64 and slack <= gamma_max/52, 'strict slack enlargement')
    # Unit root -exp(-2i*theta), theta=1/1600 gives S=0 and eight equal phases.
    theta = Q(1, 1600)
    phases = 8*theta*theta
    require(phases > gamma_max/160000 and phases <= gamma_max/96000,
            'strict phase enlargement')
    records['strict_witnesses'] = {'slack': {'a': 1, 'small_reciprocal': r,
                                           'other_original_root': other_root, 'S': slack},
                                  'phase': {'a': 1, 'theta': theta, 'rho_squared': phases,
                                            'other_original_root': '-exp(-2i*theta)'}}
    # Same original domain, retain all certified losses and actual K upper bound.
    kup = Q(9, 8)+16*gamma_max/64+210*gamma_max/160000
    cs = (Q(3, 4)-Q(19, 64)-Q(800, 160000))/kup
    cp = (Q(1, 40)-Q(1200, 160000))/kup
    require(cs == Q(19120, 52021) and cp == Q(2240, 156063), 'exact improved original weights')
    records['original_improved_weights'] = {'K_upper': kup, 'S_weight': cs, 'phase_weight': cp}
    require(radial_bound(T) < Q(1, 4000), 'radial series convergence margin')
    require(radial_bound(T)+S0 < Q(1, 100), 'radial series plus slack')
    records['radial_majorant_at_T'] = radial_bound(T)
    return records


def serialize(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serialize(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serialize(v) for v in x]
    return x


def same_typed(actual, expected, location='root'):
    require(type(actual) is type(expected), 'fixture type '+location)
    if isinstance(actual, dict):
        require(actual.keys() == expected.keys(), 'fixture keys '+location)
        for k in actual:
            same_typed(actual[k], expected[k], location+'.'+str(k))
    elif isinstance(actual, list):
        require(len(actual) == len(expected), 'fixture length '+location)
        for k, (a, e) in enumerate(zip(actual, expected)):
            same_typed(a, e, location+'.'+str(k))
    else:
        require(actual == expected, 'fixture value '+location)


def build():
    cap_records, caps, identities = primitive_coefficients()
    values, bounds = derivative_budgets(caps)
    return serialize({'version': 1, 'mu': MU, 'caps': cap_records,
                      'heavy_curvature': heavy_curvature(), 'derivatives': values,
                      'integer_bounds': bounds, 'primitive_identity_controls': identities,
                      'jet_and_polarization_controls': controls(), 'domains': domain_checks()})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    signal.alarm(45)
    record = build()
    text = json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n'
    if args.expected:
        same_typed(record, json.loads(args.expected.read_text()))
    if args.write:
        args.write.write_text(text)
    print(json.dumps({'status': 'PASS', 'record_sha256': hashlib.sha256(text.encode()).hexdigest(),
                      'record_bytes': len(text.encode()), 'caps': len(record['caps']),
                      'Bernstein_entries': sum(2*(r['degree']+1) for r in record['caps'])+23,
                      'controls': record['jet_and_polarization_controls'],
                      'domains': record['domains']}))


if __name__ == '__main__':
    main()
