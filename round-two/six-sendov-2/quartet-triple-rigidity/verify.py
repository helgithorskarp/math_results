#!/usr/bin/env python3
"""Exact finite bridges for the ordinary quartet proof; Python stdlib only.

Author six-sendov-2/researcher. No optimizer, root approximation or search.
The compactness, feasible curves and root-count argument are in PROOF.md.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import copy
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


class P:
    """Sparse Laurent polynomials over QQ; only monomials are inverted."""
    def __init__(self, names, terms=None):
        self.names = tuple(names)
        self.terms = {tuple(e): Q(c) for e, c in (terms or {}).items() if c}
        require(all(len(e) == len(self.names) for e in self.terms), 'dimension')

    @classmethod
    def constant(cls, names, value):
        return cls(names, {(0,) * len(names): Q(value)})

    @classmethod
    def variable(cls, names, name):
        e = [0] * len(names)
        e[names.index(name)] = 1
        return cls(names, {tuple(e): Q(1)})

    def coerce(self, other):
        if isinstance(other, P):
            require(other.names == self.names, 'same coefficient ring')
            return other
        return P.constant(self.names, other)

    def __add__(self, other):
        other = self.coerce(other)
        terms = dict(self.terms)
        for e, c in other.terms.items():
            terms[e] = terms.get(e, Q(0)) + c
        return P(self.names, terms)

    __radd__ = __add__

    def __neg__(self):
        return P(self.names, {e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                h = tuple(a + b for a, b in zip(e, f))
                terms[h] = terms.get(h, Q(0)) + c * d
        return P(self.names, terms)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(type(n) is int, 'integer polynomial power')
        if n < 0:
            require(len(self.terms) == 1, 'only a nonzero monomial is inverted')
            e, c = next(iter(self.terms.items()))
            return P(self.names, {tuple(a * n for a in e): c ** n})
        out = P.constant(self.names, 1)
        base = self
        while n:
            if n % 2:
                out = out * base
            base = base * base
            n //= 2
        return out

    def __truediv__(self, other):
        return self * self.coerce(other) ** -1

    def derivative(self, name):
        i = self.names.index(name)
        terms = {}
        for e, c in self.terms.items():
            if e[i]:
                f = list(e)
                f[i] -= 1
                terms[tuple(f)] = c * e[i]
        return P(self.names, terms)

    def substitute(self, name, value):
        i = self.names.index(name)
        value = self.coerce(value)
        out = P.constant(self.names, 0)
        for e, c in self.terms.items():
            f = list(e)
            power = f[i]
            f[i] = 0
            out += P(self.names, {tuple(f): c}) * value ** power
        return out

    def coefficient(self, name, power):
        i = self.names.index(name)
        terms = {}
        for e, c in self.terms.items():
            if e[i] == power:
                f = list(e)
                f[i] = 0
                terms[tuple(f)] = c
        return P(self.names, terms)

    def evaluate(self, values):
        require(set(values) == set(self.names), 'all variables assigned')
        return sum((c * product(Q(values[n]) ** e[i]
                               for i, n in enumerate(self.names))
                    for e, c in self.terms.items()), Q(0))

    def record(self):
        return {'variables': list(self.names),
                'whole_QQ_Laurent_terms': [[list(e), str(c)]
                                          for e, c in sorted(self.terms.items(), reverse=True)]}


def product(items):
    out = 1
    for item in items:
        out *= item
    return out


def variables(*names):
    return tuple(P.variable(names, n) for n in names)


def equal(a, b, label):
    require(not (a - b).terms, label)


def bernstein(p):
    require(p.names == ('x',), 'univariate Bernstein ring')
    require(all(e[0] >= 0 for e in p.terms), 'polynomial Bernstein input')
    n = max((e[0] for e in p.terms), default=0)
    # x=t/4; power-to-Bernstein conversion at the full natural degree.
    a = [p.terms.get((j,), Q(0)) / 4 ** j for j in range(n + 1)]
    return [sum((a[j] * Q(comb(i, j), comb(n, j))
                 for j in range(i + 1)), Q(0)) for i in range(n + 1)]


def boundary_case(k):
    x, = variables('x')
    a = 1 - x / k
    if k == 2:
        numerator = x * (4 - 2 * x - x ** 2)
        denominator = 8 - 4 * x
        gap_n, gap_d = 2 * (1 - x) ** 2, 2 - x
        gain_n, gain_d = 10 * x * (1 - x) ** 2, 2 - x
    elif k == 3:
        numerator = x * (27 - 9 * x - 8 * x ** 2)
        denominator = 54 - 18 * x
        gap_n, gap_d = 2 * x ** 3 + 9 * x ** 2 - 27 * x + 18, 18 - 6 * x
        gain_n = x * (30 * x ** 4 + 45 * x ** 3 - 10 * x ** 2 - 315 * x + 270)
        gain_d = 54 - 18 * x
    else:
        raise ValueError('only the complete two equal-support cases')
    equal(k * a + x, P.constant(('x',), k), 'entire first opening moment')
    equal(6 * a * numerator, (k - k * a ** 3 - x ** 3) * denominator,
          'entire exact pair split square')
    equal((a ** 2 * denominator - numerator) * gap_d, gap_n * denominator,
          'entire positive old-coordinate gap')
    fnum = (k * a ** 5 - k + x ** 5) * denominator ** 2
    fnum += 20 * a ** 3 * numerator * denominator + 10 * a * numerator ** 2
    equal(fnum * gain_d, gain_n * denominator ** 2, 'entire fifth opening gain')
    require(gain_n.evaluate({'x': 0}) == 0, 'gain vanishes at the old corner')
    derivative = gain_n.derivative('x').evaluate({'x': 0}) / gain_d.evaluate({'x': 0})
    require(derivative == 5, 'strict right fifth derivative')
    pp = {'delta_numerator_over_x': numerator / x,
          'delta_denominator': denominator,
          'old_positive_gap_numerator': gap_n,
          'old_positive_gap_denominator': gap_d,
          'fifth_gain_numerator_over_x': gain_n / x,
          'fifth_gain_denominator': gain_d}
    certs = {}
    for name, p in pp.items():
        bb = bernstein(p)
        require(all(b > 0 for b in bb), 'whole closed Bernstein positivity ' + name)
        certs[name] = {'polynomial': p.record(),
                       'all_Bernstein_coefficients_on_0_to_1_over_4': list(map(str, bb))}
    return {'positive_support': k, 'mean': a.record(),
            'pair_split_square': {'numerator': numerator.record(), 'denominator': denominator.record()},
            'old_positive_gap': {'numerator': gap_n.record(), 'denominator': gap_d.record()},
            'fifth_gain': {'numerator': gain_n.record(), 'denominator': gain_d.record()},
            'right_fifth_gain_derivative': str(derivative), 'all_positive_certificates': certs}


class E:
    """QQ[sqrt(57)], with the positive real embedding bounded separately."""
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def coerce(self, value):
        return value if isinstance(value, E) else E(value)

    def __add__(self, value):
        value = self.coerce(value)
        return E(self.a + value.a, self.b + value.b)

    __radd__ = __add__

    def __neg__(self):
        return E(-self.a, -self.b)

    def __sub__(self, value):
        return self + (-self.coerce(value))

    def __rsub__(self, value):
        return self.coerce(value) - self

    def __mul__(self, value):
        value = self.coerce(value)
        return E(self.a * value.a + 57 * self.b * value.b,
                 self.a * value.b + self.b * value.a)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'nonnegative extension power')
        out = E(1)
        for unused in range(n):
            out *= self
        return out

    def record(self):
        return [str(self.a), str(self.b)]


def fifth_control():
    a, b = E(Q(47, 32), Q(-3, 32)), E(Q(-29, 32), Q(9, 32))
    left = [E(1)] * 3 + [E(Q(1, 2))]
    right = [a] * 3 + [b]
    diffs = {str(j): (sum((v ** j for v in left), E())
                      - sum((v ** j for v in right), E())).record() for j in (1, 3, 5)}
    require(diffs['1'] == ['0', '0'] and diffs['3'] == ['0', '0'], 'matched first/cubic control')
    require(diffs['5'] == [str(Q(14592015, 262144)), str(Q(-1946835, 262144))],
            'entire fifth extension control')
    low, high = Q(15, 2), Q(38, 5)
    require(low ** 2 < 57 < high ** 2, 'positive square-root embedding bounds')
    require(a.a + a.b * high > 0 and b.a + b.b * low > 0, 'all four magnitudes positive')
    require(Q(diffs['5'][1]) < 0 and Q(diffs['5'][0]) + Q(diffs['5'][1]) * low < 0,
            'strict negative fifth difference over the whole root enclosure')
    return {'field_relation': 'r^2=57', 'positive_embedding_bounds': [str(low), str(high)],
            'left': [v.record() for v in left], 'right': [v.record() for v in right],
            'first_third_fifth_differences': diffs}


def simple_fiber_control():
    z, = variables('z')
    base = product(z - i for i in range(1, 5))
    q = z ** 2 - 10 * z + 30
    controls = []
    for eps in (Q(-1, 1000), Q(1, 1000)):
        g = base + eps * q
        brackets = []
        for i in range(1, 5):
            l, r = Q(i) - Q(1, 100), Q(i) + Q(1, 100)
            a, b = g.evaluate({'z': l}), g.evaluate({'z': r})
            require(l > 0 and a * b < 0, 'literal four disjoint positive root brackets')
            brackets.append({'interval': [str(l), str(r)], 'entire_endpoint_values': [str(a), str(b)]})
        controls.append({'A': str(Q(35) + eps), 'whole_quartic': g.record(), 'four_root_brackets': brackets})
    return {'S': '10', 'K': '100', 'L': '1300', 'T': '-300', 'U': '-1026',
            'R': '12600', 'quadratic': q.record(), 'distinct_actual_quartets': controls}


def build():
    z, t, b = variables('z', 't', 'b')
    lam, mu = Q(5, 3) * (t ** 2 + b ** 2), -5 * t ** 2 * b ** 2
    multiplier = 5 * z ** 4 - 3 * lam * z ** 2 - mu
    equal(multiplier, 5 * (z ** 2 - t ** 2) * (z ** 2 - b ** 2), 'full multiplier factor')
    lower = multiplier.derivative('z').substitute('z', t)
    upper = multiplier.derivative('z').substitute('z', b)
    equal(lower, 10 * t * (t ** 2 - b ** 2), 'lower constrained Hessian')
    equal(upper, 10 * b * (b ** 2 - t ** 2), 'upper constrained Hessian')
    S0, K0 = 3 * t + b, 3 * t ** 3 + b ** 3
    gaps = [16 * K0 - S0 ** 3, S0 ** 3 - K0, S0 ** 3 - 9 * K0]
    equals = [3 * (b - t) ** 2 * (5 * b + 7 * t),
              3 * t * (8 * t ** 2 + 9 * t * b + 3 * b ** 2),
              b * (27 * t ** 2 + 9 * t * b - 8 * b ** 2)]
    for left, right in zip(gaps, equals):
        equal(left, right, 'entire triple quartet moment range')
    universal = dict(zip(['multiplier', 'lower_Hessian', 'upper_Hessian',
                          'cube_min_gap', 'cube_max_gap', 'support3_cube_gap',
                          'regular_zero_opening_fifth_derivative'],
                         [p.record() for p in [multiplier, lower, upper, *gaps, -mu]]))

    z, S, T, U, A, d = variables('z', 'S', 'T', 'U', 'A', 'd')
    q = z ** 2 - S * z - T / S
    e3, e4 = S * A + T, U - T * A / S
    g = z ** 4 - S * z ** 3 + A * z ** 2 - e3 * z + e4
    R = -T ** 2 - S ** 2 * U
    p3 = S ** 3 - 3 * S * A + 3 * e3
    p5 = S ** 5 - 5 * S ** 3 * A + 5 * S ** 2 * e3 + 5 * S * A ** 2 - 5 * A * e3 - 5 * S * e4
    equal(p3, S ** 3 + 3 * T, 'Newton third pencil moment')
    equal(p5, S ** 5 + 5 * S ** 2 * T - 5 * S * U, 'Newton fifth pencil moment')
    equal(S * A * e3 - e3 ** 2 - S ** 2 * e4, R, 'whole Hurwitz invariant')
    equal(g, q * (z ** 2 + A + T / S) - R / S ** 2, 'whole quotient decomposition')
    cross = q * g.substitute('z', -z) - g * q.substitute('z', -z)
    equal(cross, 2 * R * z / S, 'entire odd cross part is linear')
    abar = S ** 2 / 2 - Q(1, 4)
    bar = g.substitute('A', abar)
    f = (bar + d * q) * (bar.substitute('z', -z) - d * q.substitute('z', -z))
    equal(f.coefficient('z', 8), P.constant(f.names, 1), 'monic full octic')
    equal(f.coefficient('z', 6), P.constant(f.names, Q(-1, 2)), 'full normalized second moment')
    for j in (7, 5, 3):
        equal(f.coefficient('z', j), P.constant(f.names, 0), 'full odd coefficient zero')
    equal(f.coefficient('z', 1), 2 * d * R / S, 'actual 8J versus pencil separation')

    vals = variables('v0', 'v1', 'v2', 'v3')
    ss = sum(vals)
    aa = sum((product(c) for c in combinations(vals, 2)), P.constant(vals[0].names, 0))
    bb = sum((product(c) for c in combinations(vals, 3)), P.constant(vals[0].names, 0))
    cc = product(vals)
    hurwitz = ss * aa * bb - bb ** 2 - ss ** 2 * cc
    pair_product = product(vals[i] + vals[j] for i, j in combinations(range(4), 2))
    equal(hurwitz, pair_product, 'entire classical six-pair Orlando product')

    # H(z)=z q(z)^2/(S-2z), on 0<z<S/2. Clear its positive denominator.
    hn, hd = z * q ** 2, S - 2 * z
    derivative_numerator = hn.derivative('z') * hd - hn * hd.derivative('z')
    N = S * q - 2 * z * (S - 2 * z) ** 2
    equal(derivative_numerator, q * N, 'whole H derivative numerator')
    equal(N, -8 * z ** 3 + 9 * S * z ** 2 - 3 * S ** 2 * z - T, 'whole critical cubic')
    equal(N.derivative('z'), -3 * (4 * z - S) * (2 * z - S), 'entire critical cubic derivative')
    K = S ** 3 + 3 * T
    n0, nquarter, nhalf = N.substitute('z', 0), N.substitute('z', S / 4), N.substitute('z', S / 2)
    equal(n0, -T, 'critical cubic at zero')
    equal(nquarter, (S ** 3 - 16 * K) / 48, 'critical cubic strict minimum')
    equal(nhalf, (S ** 3 - 4 * K) / 12, 'critical cubic at half sum')
    discriminant = S ** 2 + 4 * T / S
    equal(discriminant, (4 * K - S ** 3) / (3 * S), 'quadratic direction discriminant')
    # Psi'=R(S-2z)/(S^2 q^2)-2z; its numerator is the double-root equation.
    critical_equation = R * (S - 2 * z) - 2 * S ** 2 * z * q ** 2
    equal(g.derivative('z') * q - g * q.derivative('z'), -critical_equation / S ** 2,
          'entire pencil double-root equation independent of A')
    return {'schema': 'six-sendov-2.quartet-rigidity.v1',
            'exact_domains': ['QQ sparse polynomials', 'QQ[S,S^-1,T,U,A,d,z]', 'QQ[r]/(r^2-57)'],
            'universal_quartet_maps': universal,
            'all_equal_support_zero_openings': [boundary_case(k) for k in (2, 3)],
            'essential_fifth_moment_control': fifth_control(),
            'pencil': {'quartic': g.record(), 'quadratic': q.record(), 'third_power': p3.record(),
                       'fifth_power': p5.record(), 'Hurwitz_invariant': R.record(),
                       'full_Hurwitz_pair_product': hurwitz.record(),
                       'quotient_decomposition': (q * (z ** 2 + A + T / S) - R / S ** 2).record(),
                       'whole_odd_cross_part': cross.record(), 'normalized_Abar': abar.record(),
                       'all_nine_normalized_octic_coefficients_ascending': [f.coefficient('z', j).record() for j in range(9)],
                       'J': (d * R / (4 * S)).record()},
            'fiber_interval_bridges': {'H_numerator': hn.record(), 'H_denominator': hd.record(),
                       'H_derivative_numerator': derivative_numerator.record(),
                       'critical_cubic_N': N.record(), 'critical_cubic_derivative': N.derivative('z').record(),
                       'N_at_zero': n0.record(), 'N_at_quarter_sum': nquarter.record(), 'N_at_half_sum': nhalf.record(),
                       'direction_discriminant': discriminant.record(), 'entire_double_root_equation': critical_equation.record()},
            'literal_nonsingleton_positive_fiber': simple_fiber_control()}


def render(record):
    return (json.dumps(record, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def check_fixture(fixture, record):
    require(type(fixture) is dict, 'whole fixture must be a JSON object')
    require(render(fixture) == render(record), 'whole typed coefficient/certificate record mismatch')


def self_test(record):
    damages = []
    x = copy.deepcopy(record)
    x['all_equal_support_zero_openings'].pop()
    damages.append(x)
    x = copy.deepcopy(record)
    x['all_equal_support_zero_openings'][1]['all_positive_certificates']['delta_denominator']['all_Bernstein_coefficients_on_0_to_1_over_4'][0] = '0'
    damages.append(x)
    x = copy.deepcopy(record)
    x['pencil']['all_nine_normalized_octic_coefficients_ascending'][1]['whole_QQ_Laurent_terms'][0][1] = '1'
    damages.append(x)
    x = copy.deepcopy(record)
    x['fiber_interval_bridges']['critical_cubic_derivative']['whole_QQ_Laurent_terms'].pop()
    damages.append(x)
    x = copy.deepcopy(record)
    x['essential_fifth_moment_control']['first_third_fifth_differences']['5'][1] = '0'
    damages.append(x)
    for damaged in damages:
        try:
            check_fixture(damaged, record)
        except ValueError:
            continue
        raise ValueError('semantic damaged fixture accepted')
    return len(damages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-record', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    record = build()
    raw = render(record)
    if args.write_record:
        args.write_record.write_bytes(raw)
    else:
        check_fixture(json.loads(args.expected.read_text(encoding='utf-8')), record)
        require(args.expected.read_bytes() == raw, 'canonical whole expected bytes')
    rejected = self_test(record) if args.self_test else 0
    print(json.dumps({'status': 'PASS', 'whole_record_bytes': len(raw),
                      'sha256': hashlib.sha256(raw).hexdigest(), 'equal_support_cases': 2,
                      'positive_Bernstein_polynomials': 12, 'normalized_octic_coefficients': 9,
                      'nontrivial_positive_fiber_controls': 2, 'semantic_rejections': rejected}))


if __name__ == '__main__':
    main()
