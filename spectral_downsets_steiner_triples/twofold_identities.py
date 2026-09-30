"""Portable exact coefficient checks over Q(v), independent of the CAS.

Polynomial coefficients are ascending integer tuples. Rational functions are
not simplified: equality is checked after clearing their denominators.
Strict positivity certificates use positive coefficients in v-13>=0.
"""
from math import comb


def add(a, b):
    return tuple((a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b))))


def multiply(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return tuple(out)


class RationalFunction:
    def __init__(self, numerator, denominator=(1,)):
        self.n = (numerator,) if isinstance(numerator, int) else tuple(numerator)
        self.d = tuple(denominator)
        assert any(self.d)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, RationalFunction) else RationalFunction(value)

    def __add__(self, other):
        other = self.coerce(other)
        return RationalFunction(add(multiply(self.n, other.d),
                                    multiply(other.n, self.d)), multiply(self.d, other.d))

    __radd__ = __add__

    def __neg__(self):
        return RationalFunction(tuple(-x for x in self.n), self.d)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        return RationalFunction(multiply(self.n, other.n), multiply(self.d, other.d))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        return RationalFunction(multiply(self.n, other.d), multiply(self.d, other.n))

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out = RationalFunction(1)
        for _ in range(exponent):
            out *= self
        return out

    def is_zero(self):
        return not any(self.n)


def shifted(coefficients, base=13):
    return [sum(coefficients[j]*comb(j, i)*base**(j-i)
                for j in range(i, len(coefficients))) for i in range(len(coefficients))]


def run():
    v = RationalFunction((0, 1))
    den = (v-3)*(v-4)
    a = RationalFunction(-2, (3,))
    b = 1+4*v*(2*v-5)/(3*(v-2)*den)
    c = 1+4/(3*(v-2)*(v-3))
    d = (v*v-v-4)/den
    h = (v*v-7)/den
    t = (v-1)/(v-4)
    s, N = 2*v-1, (5*v*v+v+6)/6
    m, B = v*(v-1)/2, v*(v-1)/3
    alpha1, alpha2 = s-c*(v-3), s+c
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    reduced = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu = v*(3*v**3-13*v*v+32)/((v-3)*(v-2)*(3*v*v-16))
    k = (v-2)*(v-3)/2
    delta = N-7*v
    eta = delta/(8*m*k)
    equations = {
        'triple_star': h+(v-4)*d+(v-7)*t-s,
        'triple_row': 1+s+(v-3)*h-3*t+(v-3)*(v-4)*d/2+(v-4)*(v-6)*t/3-N,
        'pair_star': b+(v-3)*c+(v-5)*d-s,
        'pair_row': 1+s+(v-2)*b-2*d+(v-2)*(v-3)*c/2+(v-3)*(v-4)*d/3-N,
        'point_star': a+(v-2)*b-2*d+(v-3)*h-3*t-s,
        'point_row': 1+s+(v-1)*a+(v-1)*(v-2)*b/2-(v-1)*d+(v-1)*(v-3)*h/3-(v-1)*t-N,
        'K_pair_constant': s+c-2*c*(v-1)+(c-1)*m-RationalFunction(8, (3,)),
        'K_cross_constant': 2*d-2*d*(v-1)+(d-1)*B+RationalFunction(4, (3,)),
        'K_triple_constant': s+5*t-3*t*(v-1)+(t-1)*B-1,
        'alpha1': alpha1-(3*v*v-16)/(3*(v-2)),
        'Schur_reduction': gamma-4*beta/(v-2)-reduced,
        'Schur_lower_bound': s-t-(v-3)*reduced-mu,
        'cap_gap': N-7*v-(5*v*v-41*v+6)/6,
        'eta_formula': eta-(5*v*v-41*v+6)/(12*v*(v-1)*(v-2)*(v-3)),
        'mu_gt_one': mu-1-2*(v-4)*(v*v+3*v-12)/((v-3)*(v-2)*(3*v*v-16)),
        'pair_norm_denominator': 8*m*k-v**4-v*(v**3-12*v*v+22*v-12),
    }
    for name, expression in equations.items():
        assert expression.is_zero(), name
    # These are the displayed, positive-denominator numerators in the proof.
    certificates = {
        'b_le_3_over_2': (-72, 118, -43, 3),
        'c_le_4_over_3': (2, -5, 1),
        'd_le_2': (28, -13, 1),
        'h_le_2': (31, -14, 1),
        'alpha1_positive': (-16, 0, 3),
        'mu_positive': (32, 0, -13, 3),
        'cap_gap_positive': (6, -41, 5),
        'row2_strict_gap': (-32, 11),
        'row3_strict_gap': (-96, 14),
        'eight_mk_gt_v4_cubic': (-12, 22, -12, 1),
        'delta_lt_v2': (-6, 41, 1),
    }
    positive = {name: shifted(poly) for name, poly in certificates.items()}
    assert all(xs[0] > 0 and all(x >= 0 for x in xs) for xs in positive.values())
    assert (RationalFunction(3, (2,))-b-
            RationalFunction(certificates['b_le_3_over_2'])/(6*(v-2)*den)).is_zero()
    assert (RationalFunction(4, (3,))-c-
            RationalFunction(certificates['c_le_4_over_3'])/(3*(v-2)*(v-3))).is_zero()
    assert (2-d-RationalFunction(certificates['d_le_2'])/den).is_zero()
    assert (2-h-RationalFunction(certificates['h_le_2'])/den).is_zero()
    return {'domain': 'Q(v)', 'zero_polynomial_identities': len(equations)+4,
            'identity_names': list(equations), 'positive_coefficients_in_v_minus_13': positive}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
