"""Exact fixed-energy moving-pair split calculation; no numeric proof inputs.

Actual author six-sendov-3, role researcher. This is the source layer for an
ordinary analytic proof, not a formalization of its analytic bridges.
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path


class Laurent:
    """Q[v,v^-1]; only nonzero monomials may be inverted here."""
    def __init__(self, x=0):
        if isinstance(x, Laurent):
            x = x.d
        elif isinstance(x, (int, F)):
            x = {0: F(x)}
        self.d = {k: F(c) for k, c in x.items() if c}

    def __add__(self, x):
        if isinstance(x, (Jet, Poly)):
            return NotImplemented
        x = Laurent(x)
        d = dict(self.d)
        for k, c in x.d.items():
            d[k] = d.get(k, F(0)) + c
        return Laurent(d)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({k: -c for k, c in self.d.items()})

    def __sub__(self, x):
        if isinstance(x, (Jet, Poly)):
            return NotImplemented
        return self + -Laurent(x)

    def __rsub__(self, x):
        return Laurent(x) + -self

    def __mul__(self, x):
        if isinstance(x, (Jet, Poly)):
            return NotImplemented
        x = Laurent(x)
        d = {}
        for k, c in self.d.items():
            for h, a in x.d.items():
                d[k + h] = d.get(k + h, F(0)) + c * a
        return Laurent(d)

    __rmul__ = __mul__

    def inverse(self):
        if len(self.d) != 1:
            raise ValueError('Laurent inversion needs a nonzero monomial')
        k, c = next(iter(self.d.items()))
        return Laurent({-k: 1 / c})

    def __truediv__(self, x):
        if isinstance(x, (Jet, Poly)):
            return NotImplemented
        return self * Laurent(x).inverse()

    def __rtruediv__(self, x):
        return Laurent(x) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Laurent(1)
        for _ in range(n):
            out *= self
        return out

    def derivative(self):
        return Laurent({k - 1: k * c for k, c in self.d.items() if k})

    def wire(self):
        return [[k, [c.numerator, c.denominator]]
                for k, c in sorted(self.d.items())]

    def endpoint(self):
        vv = Field(0, 1)
        return sum((Field(c) * vv ** k for k, c in self.d.items()), Field())


ORDER = 2


class Jet:
    """Q[v,v^-1][e]/(e^3)."""
    def __init__(self, x=0):
        if isinstance(x, Jet):
            x = x.c
        elif isinstance(x, (int, F, Laurent)):
            x = [Laurent(x)]
        self.c = [Laurent(x[i]) if i < len(x) else Laurent()
                  for i in range(ORDER + 1)]

    def __add__(self, x):
        x = Jet(x)
        return Jet([a + b for a, b in zip(self.c, x.c)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-a for a in self.c])

    def __sub__(self, x):
        return self + -Jet(x)

    def __rsub__(self, x):
        return Jet(x) + -self

    def __mul__(self, x):
        x = Jet(x)
        return Jet([sum((self.c[k] * x.c[n - k] for k in range(n + 1)),
                        Laurent()) for n in range(ORDER + 1)])

    __rmul__ = __mul__

    def inverse(self):
        c = [self.c[0].inverse()]
        for n in range(1, ORDER + 1):
            c.append(-c[0] * sum((self.c[k] * c[n - k]
                                 for k in range(1, n + 1)), Laurent()))
        return Jet(c)

    def __truediv__(self, x):
        return self * Jet(x).inverse()

    def __rtruediv__(self, x):
        return Jet(x) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Jet(1)
        for _ in range(n):
            out *= self
        return out

    def wire(self):
        return [a.wire() for a in self.c]


class Poly:
    """Exact full polynomials in (xi,e,f), with Laurent coefficients."""
    def __init__(self, x=0):
        if isinstance(x, Poly):
            x = x.d
        elif isinstance(x, (int, F, Laurent)):
            x = {(0, 0, 0): Laurent(x)}
        self.d = {k: Laurent(c) for k, c in x.items() if Laurent(c).d}

    def __add__(self, x):
        x = Poly(x)
        d = dict(self.d)
        for k, c in x.d.items():
            d[k] = d.get(k, Laurent()) + c
        return Poly(d)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -c for k, c in self.d.items()})

    def __sub__(self, x):
        return self + -Poly(x)

    def __rsub__(self, x):
        return Poly(x) + -self

    def __mul__(self, x):
        x = Poly(x)
        d = {}
        for k, c in self.d.items():
            for h, a in x.d.items():
                kh = tuple(kk + hh for kk, hh in zip(k, h))
                d[kh] = d.get(kh, Laurent()) + c * a
        return Poly(d)

    __rmul__ = __mul__

    def __truediv__(self, x):
        return self * Laurent(x).inverse()

    def __pow__(self, n):
        out = Poly(1)
        for _ in range(n):
            out *= self
        return out

    def derivative(self, variable):
        out = {}
        for k, c in self.d.items():
            if k[variable]:
                kk = list(k)
                kk[variable] -= 1
                out[tuple(kk)] = k[variable] * c
        return Poly(out)

    def at(self, variable, value):
        out = Poly()
        for k, c in self.d.items():
            kk = list(k)
            kk[variable] = 0
            out += Poly({tuple(kk): c}) * value ** k[variable]
        return out

    def wire(self):
        return [[list(k), c.wire()] for k, c in sorted(self.d.items())]


class Field:
    """Q[v]/(239v^2+184v-208); its real branch is isolated separately."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Field):
            a, b = a.a, a.b
        self.a, self.b = F(a), F(b)

    def __add__(self, x):
        x = Field(x)
        return Field(self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return Field(-self.a, -self.b)

    def __sub__(self, x):
        return self + -Field(x)

    def __rsub__(self, x):
        return Field(x) + -self

    def __mul__(self, x):
        x = Field(x)
        return Field(self.a * x.a + self.b * x.b * F(208, 239),
                     self.a * x.b + self.b * x.a
                     - self.b * x.b * F(184, 239))

    __rmul__ = __mul__

    def inverse(self):
        conj = Field(self.a - self.b * F(184, 239), -self.b)
        norm = self * conj
        if norm.b or not norm.a:
            raise ValueError('invalid field norm')
        return Field(conj.a / norm.a, conj.b / norm.a)

    def __truediv__(self, x):
        return self * Field(x).inverse()

    def __rtruediv__(self, x):
        return Field(x) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Field(1)
        for _ in range(n):
            out *= self
        return out

    def wire(self):
        return [[x.numerator, x.denominator] for x in (self.a, self.b)]

    def interval(self, lo, hi):
        return (self.a + self.b * lo, self.a + self.b * hi) if self.b >= 0 \
            else (self.a + self.b * hi, self.a + self.b * lo)


def certify():
    records = {}
    counts = {'identities': 0, 'signs': 0, 'damaged_math': 0}

    def zero(name, value):
        if isinstance(value, Jet):
            ok = not any(c.d for c in value.c)
        elif isinstance(value, Field):
            ok = not value.a and not value.b
        else:
            ok = not value.d
        if not ok:
            raise RuntimeError('nonzero exact identity: ' + name)
        counts['identities'] += 1

    def record(name, value):
        if name in records:
            raise RuntimeError('duplicate evidence name')
        records[name] = value.wire()

    v = Laurent({1: 1})
    a, b = 1 / v - 1, 1 - (1 / v - 1) ** 2
    xi, ee, ff = (Poly({tuple(int(i == j) for i in range(3)): 1})
                  for j in range(3))
    k = (1 + b * xi) / 2
    # Literal reciprocal transform of the actual opposite pair, with x=e/Dx.
    Dx = 4 * v ** 4 + 2 * a * v * v * ee
    h, j = v * v + a * ee / 2, 2 * v - b * ee / 2
    q = xi + v
    raw_pair = ((1 / (v * v)) * Dx - 2 * a * ee) * q * q \
        - (2 * Dx / v - 2 * ee) * q + Dx
    pair = xi * xi + ee * k
    zero('actual pair reciprocal polynomial', raw_pair - 4 * v * v * pair)
    zero('actual pair product', Dx - 4 * v * v * h)
    zero('actual pair sum', 2 * Dx / v - 2 * ee - 4 * v * v * j)
    zero('exact opposite pair energy', 2 * h - 2 * v * j + 2 * v * v - ee)
    root = xi ** 4 * (xi * xi + (ee - ff) * k) * (xi * xi + ff * k)
    expanded = xi ** 8 + ee * k * xi ** 6 + ff * (ee - ff) * k * k * xi ** 4
    zero('complete eight original reciprocal roots', root - expanded)
    A, B, C = -8 * v + b * ee, (7 * a - 4) * ee / 2, -3 * v * ee
    cubic = xi ** 3 + A * xi * xi + B * xi + C
    jj = (1 + b * xi) * (3 * b * xi * xi + (6 * a - 1) * xi - 4 * v) / 4
    jexpanded = 3 * b * b * xi ** 3 / 4 + b * (3 * a + 1) * xi * xi / 2 \
        + 5 * (2 * a - 1) * xi / 4 - v
    zero('full split perturbation', jj - jexpanded)
    quintic = xi * xi * cubic + ff * (ee - ff) * jj
    characteristic = 9 * root - (xi + v) * root.derivative(0)
    zero('complete eight critical reciprocal characteristic',
         characteristic - xi ** 3 * quintic)
    zero('all five collapsed critical multiplicities at f=0',
         characteristic.at(2, Laurent()) - xi ** 5 * cubic)
    s, p = (16 * a - 7) / (36 * v), F(1, 3)
    L1 = ee * (3 * b * b / 4 + s * b) - 8 * v * s - p
    L0 = ee * (b * (3 * a + 1) / 2 + s * (7 * a - 4) / 2 - b / 3) + 8 * v / 3
    ell = s * xi * xi + L1 * xi + L0
    zero('two-group factor derivative, every coefficient',
         ee * jj - (p - s * xi) * cubic - xi * xi * ell)
    zero('external product', -cubic.at(0, -v) - 9 * v * h)
    zero('far root at collapse', cubic.at(1, Laurent()).at(0, 8 * v))
    zero('far root simple derivative',
         cubic.derivative(0).at(1, Laurent()).at(0, 8 * v) - 64 * v * v)
    zero('auxiliary modulus derivative', s + p / v - (16 * a + 5) / (36 * v))
    for name, value in [('pair_reciprocal', pair), ('eight_root_polynomial', expanded),
                        ('eight_critical_characteristic', characteristic),
                        ('main_cubic', cubic), ('split_quintic', quintic),
                        ('split_J', jj), ('external_factor_derivative', ell)]:
        record(name, value)

    e = Jet([0, 1])
    AA, BB, CC = -8 * v + b * e, (7 * a - 4) * e / 2, -3 * v * e
    def cubic_jet(qf):
        r = qf - v
        return r ** 3 + AA * r * r + BB * r + CC
    qf = Jet(9 * v)
    for n in range(1, ORDER + 1):
        qf.c[n] = -cubic_jet(qf).c[n] / (64 * v * v)
    zero('whole formal far root through degree2', cubic_jet(qf))
    zero('independent first far-root implicit derivative',
         qf.c[1] - 9 * (4 * a - 5) / (64 * v))
    r = qf - v
    l1 = e * (3 * b * b / 4 + s * b) - 8 * v * s - p
    l0 = e * (b * (3 * a + 1) / 2 + s * (7 * a - 4) / 2 - b / 3) + 8 * v / 3
    lr = s * r * r + l1 * r + l0
    dC = 3 * r * r + 2 * AA * r + BB
    qf_f = -lr / dC
    zero('whole implicit f derivative through degree2', dC * qf_f + lr)
    product = 9 * v * (v * v + a * e / 2)
    product_f = -(s * v * v - l1 * v + l0)
    main_product = product / qf
    m = Jet(v)
    for n in range(1, ORDER + 1):
        m.c[n] = (main_product.c[n] - sum((m.c[k] * m.c[n - k]
                    for k in range(1, n)), Laurent())) / (2 * v)
    zero('whole positive main modulus square through degree2', m * m - main_product)
    H = (16 * a + 5) / (36 * v) + qf_f * (1 - m / qf) + m * product_f / product
    h1 = (208 - 184 * v - 239 * v * v) / (2304 * v ** 5)
    h2numerator = -245888 + 771984 * v - 786792 * v * v + 246931 * v ** 3
    h2 = h2numerator / (4718592 * v ** 8)
    zero('removable split constant', H.c[0])
    zero('complete leading coefficient', H.c[1] - h1)
    zero('complete finite-energy correction', H.c[2] - h2)
    oldL = (208 * a * a + 232 * a - 215) * v ** 5 / 1152
    zero('leading Hessian normalization', 2 * v ** 8 * h1 - oldL)
    for name, value in [('far_root_energy_jet', qf), ('main_modulus_energy_jet', m),
                        ('far_root_split_derivative_jet', qf_f),
                        ('external_product_split_derivative_jet', product_f),
                        ('split_derivative_energy_jet', H)]:
        record(name, value)

    vv = Field(0, 1)
    sqrt101 = (239 * vv + 92) / 24
    zero('positive threshold minimal polynomial', 239 * vv * vv + 184 * vv - 208)
    zero('positive sqrt101 square', sqrt101 * sqrt101 - 101)
    zero('leading coefficient at threshold', h1.endpoint())
    reduced_numerator = Field(F(-62608915584, 57121), F(99331992864, 57121))
    zero('complete correction numerator reduction', h2numerator.endpoint() - reduced_numerator)
    ha = (h1.derivative() * (-v * v)).endpoint()
    zero('leading coefficient radius derivative', ha - sqrt101 / (48 * vv ** 3))
    endpoint_h2 = h2.endpoint()
    slope = -endpoint_h2 / ha
    zero('stability curve slope identity', slope * ha + endpoint_h2)
    zero('slope closed form', slope + 1152 * vv ** 3 * endpoint_h2 / (239 * vv + 92))
    # Exact bisection selects the positive real branch; no float is used.
    lo, hi = F(3, 5), F(5, 8)
    def g(x):
        return 239 * x * x + 184 * x - 208
    if not (g(lo) < 0 < g(hi)):
        raise RuntimeError('threshold interval does not isolate the positive root')
    counts['signs'] += 1
    for _ in range(64):
        mid = (lo + hi) / 2
        gm = g(mid)
        if not gm:
            raise RuntimeError('unexpected rational threshold root')
        if gm < 0:
            lo = mid
        else:
            hi = mid
    def positive(name, value):
        bounds = Field(value).interval(lo, hi)
        if bounds[0] <= 0:
            raise RuntimeError('strict sign not certified: ' + name)
        records['positive_' + name] = [[x.numerator, x.denominator] for x in bounds]
        counts['signs'] += 1
    positive('sqrt101', sqrt101)
    positive('radius_derivative', ha)
    # A deliberately coarse rational bound already gives negativity.
    upper = (F(-62608915584) + F(99331992864) * F(5, 8)) / 57121
    if upper >= 0:
        raise RuntimeError('correction numerator upper bound is not negative')
    records['correction_numerator_upper_bound'] = [upper.numerator, upper.denominator]
    counts['signs'] += 1
    positive('minus_endpoint_h2', -endpoint_h2)
    positive('slope_lower', slope - F(112226, 1000000))
    positive('slope_upper', F(112227, 1000000) - slope)
    oldB = (69025 - 73880 * a - 66416 * a * a) * v ** 5 / 12288
    positive('relative_mean_stiffness_at_endpoint', oldB.endpoint())
    positive('common_mean_stiffness_at_endpoint', 10 * vv ** 3)
    positive('inward_gradient_at_endpoint', 2 * vv * vv)
    record('endpoint_correction_h2', endpoint_h2)
    record('stability_curve_slope', slope)
    records['positive_threshold_interval'] = [[x.numerator, x.denominator] for x in (lo, hi)]

    # Damage controls test complete expressions, not just selected coefficients.
    for name, damaged in [
        ('omit fixed critical multiplicity', characteristic - xi ** 2 * quintic),
        ('wrong critical transform', 8 * root - (xi + v) * root.derivative(0) - xi ** 3 * quintic),
        ('wrong pair energy', 2 * h - 2 * v * j + 2 * v * v - 2 * ee),
        ('wrong auxiliary product derivative', ee * jj - (F(1, 4) - s * xi) * cubic - xi * xi * ell),
        ('wrong finite-energy correction', H.c[2] - h2 - 1),
        ('wrong threshold branch equation', 239 * vv * vv + 184 * vv - 209),
    ]:
        if isinstance(damaged, Field):
            nonzero = bool(damaged.a or damaged.b)
        else:
            nonzero = bool(damaged.d)
        if not nonzero:
            raise RuntimeError('damaged mathematics unexpectedly accepted: ' + name)
        counts['damaged_math'] += 1
    return {'schema': 'sendov-moving-pair-split-correction-v1',
            'agent': 'six-sendov-3', 'role': 'researcher',
            'energy_jet_order': ORDER, 'counts': counts, 'records': records,
            'trust_boundary': 'exact coefficient/sign evidence; analytic proof is in PROOF.md'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture', type=Path,
                        help='explicit exact fixture generation; outside verification mode')
    args = parser.parse_args()
    result = certify()
    canonical = json.dumps(result['records'], sort_keys=True, separators=(',', ':')).encode()
    record_sha = hashlib.sha256(canonical).hexdigest()
    if args.write_fixture is not None:
        args.write_fixture.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    else:
        if not args.fixture.is_file():
            raise RuntimeError('mandatory complete fixture is missing')
        expected = json.loads(args.fixture.read_text())
        if expected != result:
            raise RuntimeError('mandatory complete evidence fixture differs')
    print(json.dumps({'agent': 'six-sendov-3', 'role': 'researcher',
                      'schema': result['schema'], 'counts': result['counts'],
                      'record_count': len(result['records']), 'record_sha256': record_sha,
                      'status': result['trust_boundary']}, sort_keys=True))


if __name__ == '__main__':
    main()
