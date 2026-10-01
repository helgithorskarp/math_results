"""Reviewer QQ polynomial arithmetic and division-free minor reconstruction.

No author imports, integer packing, supplied factors, saved sign polynomials,
interpolation or floating point. Uses SymPy's sparse polynomial ring for
multiplication, factorization and exact division. Denominators are tracked as
primitive factors, discovered at each division. A subset recurrence computes
determinants; it does not use the author's permutation implementation.
"""
import hashlib
import json
from fractions import Fraction
from math import lcm
from sympy import QQ
from sympy.polys.rings import ring

POLY, Q, T, B = ring('Q,T,B', QQ)
ZERO = (0, 0, 0)
ATOMS = {}
CACHE = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def factors(p):
    require(bool(p), 'nonzero rational divisor')
    unit, out = p.factor_list()
    answer = {}
    for a, power in out:
        # monic normalization separates a rational scalar; no sign is lost.
        lead = a.LC
        a = a / lead
        unit *= lead ** power
        key = tuple(sorted((k, str(v)) for k, v in a.items()))
        ATOMS[key] = a
        answer[key] = answer.get(key, 0) + power
    return unit, answer


def product(d):
    key = tuple(sorted(d.items()))
    if key not in CACHE:
        p = POLY.one
        for k, e in key:
            p *= ATOMS[k] ** e
        CACHE[key] = p
    return CACHE[key]


class Rat:
    def __init__(self, n=0, d=None):
        if isinstance(n, Rat) and d is None:
            self.n, self.d = n.n, n.d.copy()
            return
        self.n = POLY(n)
        self.d = dict(d or {})
        if not self.n:
            self.d = {}
            return
        for k in tuple(self.d):
            while self.d[k]:
                quo, rem = self.n.div(ATOMS[k])
                if rem:
                    break
                self.n = quo
                self.d[k] -= 1
            if not self.d[k]:
                del self.d[k]
        require(len(self.n) <= 30000, 'fixed polynomial term guard')

    def __add__(self, other):
        other = Rat(other)
        den = self.d.copy()
        for k, e in other.d.items():
            den[k] = max(den.get(k, 0), e)
        left = {k: e - self.d.get(k, 0) for k, e in den.items() if e > self.d.get(k, 0)}
        right = {k: e - other.d.get(k, 0) for k, e in den.items() if e > other.d.get(k, 0)}
        return Rat(self.n * product(left) + other.n * product(right), den)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.n, self.d)

    def __sub__(self, other):
        return self + -Rat(other)

    def __rsub__(self, other):
        return Rat(other) + -self

    def __mul__(self, other):
        other = Rat(other)
        den = self.d.copy()
        for k, e in other.d.items():
            den[k] = den.get(k, 0) + e
        return Rat(self.n * other.n, den)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rat(other)
        unit, den = factors(other.n)
        return self * Rat(product(other.d) / unit, den)

    def __rtruediv__(self, other):
        return Rat(other) / self

    def __pow__(self, power):
        require(type(power) is int and power >= 0, 'nonnegative integral power')
        return Rat(self.n ** power, {k: e * power for k, e in self.d.items()})

    def __eq__(self, other):
        other = Rat(other)
        return self.n * product(other.d) == other.n * product(self.d)


def determinant(a):
    """Exterior row recurrence with a subset state, no divisions or permutations."""
    require(all(len(row) == len(a) for row in a), 'square determinant')
    values = {0: Rat(1)}
    for row in a:
        new = {}
        for mask, value in values.items():
            for j, entry in enumerate(row):
                if mask & (1 << j):
                    continue
                # Insert column j after the previously selected columns.
                sign = (-1) ** (mask >> (j + 1)).bit_count()
                out = mask | (1 << j)
                new[out] = new.get(out, Rat()) + sign * value * entry
        values = new
    return values[(1 << len(a)) - 1]


def dot(metric, x, y):
    return sum((x[i] * metric[i][j] * y[j] for i in range(len(x))
                for j in range(len(y)) if metric[i][j] != 0), Rat())


def linear(*terms):
    return [sum((c * v[i] for c, v in terms), Rat()) for i in range(len(terms[0][1]))]


def digest(p):
    payload = sorted((list(k), str(v)) for k, v in p.items())
    return hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest()


def portable_digest(p):
    """Exact encoding comparison only; independent sign arithmetic is unchanged."""
    d = 1
    for v in p.values():
        d = lcm(d, Fraction(str(v)).denominator)
    payload = {'den': d, 'terms': sorted((list(k), str(int(Fraction(str(v)) * d))) for k, v in p.items())}
    return hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest()


def positivity(name, value):
    n, d = value.n, product(value.d)
    require(n.get(ZERO, 0) > 0 and all(v >= 0 for v in n.values()), name + ' positive numerator')
    require(d.get(ZERO, 0) > 0 and all(v >= 0 for v in d.values()), name + ' positive denominator')
    content, primitive_den = d.primitive()
    require(content > 0, 'positive primitive denominator normalization')
    normalized_num = n / content
    return {'name': name, 'numerator_terms': len(n), 'denominator_terms': len(d),
            'numerator_degree': max(map(sum, n)), 'denominator_degree': max(map(sum, d)),
            'numerator_constant': str(n.get(ZERO)), 'denominator_constant': str(d.get(ZERO)),
            'numerator_sha256': digest(n), 'denominator_sha256': digest(d),
            'primitive_denominator_numerator_sha256': portable_digest(normalized_num),
            'primitive_denominator_sha256': portable_digest(primitive_den),
            'positive_constants_and_nonnegative_coefficients': True}


def construct():
    """Derive singleton corrections and Schur budgets from the six Gram generators."""
    q, t = Rat(Q + 2), Rat(T + 1)
    D = t + B + 1
    m, w = D + t, q + D - 1
    N, h = 2 * q + 2 * (D + t), 2 * q + 2 * (D + t) - 1
    c = [m * (w - load - m - 1) / ((m + 1) * ((m - 1) * w - 1 + load)) for load in (D, t)]
    # basis: G' , h0 , A1 , A2 , Z , Wbar_heavy . At q=2 A1+A2=0.
    gram = [[Rat() for _ in range(6)] for _ in range(6)]
    gram[0][0], gram[1][1] = q - 1, D
    for i in (2, 3):
        for j in (2, 3):
            gram[i][j] = D * (q * int(i == j) - 1)
    gram[4][4] = (q + D) * (1 / t - 1 / D)
    H = [[Rat(0), Rat(1), Rat(1), Rat(0), Rat(0), Rat(0)],
         [Rat(0), Rat(1), Rat(0), Rat(1), Rat(0), Rat(0)]]
    G = [Rat(1), Rat(-1), Rat(0), Rat(0), Rat(0), Rat(0)]
    Z = [Rat(i == 4) for i in range(6)]
    L2 = linear((1 / D, H[1]), (1, Z))
    K = linear((1, G), (1, H[0]), (t, L2))
    y = linear((t * c[0] / (m * D), H[0]), (-t * c[1] / m, L2))
    require(dot(gram, K, K) == w + m * (q + D) - D ** 2 - t ** 2 - 2 * m,
            'K norm independently from Gram')
    singleton_mean = [linear((-1 / (m + 1), K), (1, y)),
                      linear((-1 / (m + 1), K), (-D / t, y))]
    eta = [w - dot(gram, v, v) - ci ** 2 * (q + D) * (1 - 1 / load)
           for v, ci, load in zip(singleton_mean, c, (D, t))]
    E = D * eta[0] + t * eta[1]
    zeta = [m / (m - 2) * (e - E / (m * (m - 1))) for e in eta]
    gram[5][5] = t * (t * zeta[0] + D * zeta[1]) / (D * m ** 2)
    functions = {'zeta_heavy': zeta[0], 'zeta_light': zeta[1]}
    for name, ci, zi in zip(('heavy', 'light'), c, zeta):
        functions[name + '_within_slack'] = 1 - ci ** 2 * (q + D) / (h - q - D) - zi / h
    # Obtain the resolvent of the old two-plane by exact 2x2 inversion.
    action = [[q + 1, D], [q - 1, D]]
    a = [[h * int(i == j) - action[i][j] for j in range(2)] for i in range(2)]
    delta = determinant(a)
    inverse = [[a[1][1] / delta, -a[0][1] / delta],
               [-a[1][0] / delta, a[0][0] / delta]]
    resolvent = [[Rat() for _ in range(6)] for _ in range(6)]
    for i in range(2):
        for j in range(2):
            resolvent[i][j] = sum((gram[i][k] * inverse[k][j] for k in range(2)), Rat())
    for i in (2, 3):
        for j in (2, 3):
            resolvent[i][j] = gram[i][j] / (h - 2 * D)
    resolvent[4][4], resolvent[5][5] = gram[4][4] / h, gram[5][5] / h
    W = [Rat(i == 5) for i in range(6)]
    vectors = [H[0], L2, K, linear((1, y), (1, W))]
    inverse_weights = [D, 1 / t, m + 1, t / (D * m)]
    budget = [[inverse_weights[i] * int(i == j) - dot(resolvent, vectors[i], vectors[j])
               for j in range(4)] for i in range(4)]
    require(all(budget[i][j] == budget[j][i] for i in range(4) for j in range(4)),
            'symmetric Schur budget from independently inverted old action')
    return functions, budget
