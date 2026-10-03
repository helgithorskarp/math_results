"""Exact author corroboration of the parity descent theorem; stdlib only.

Ordinary positivity, differentiation, hyperbolicity and constrained-extremum
arguments are in PROOF.md. Finite controls do not enumerate a real domain.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time


def require(condition, label):
    if not condition:
        raise ValueError(label)


class Poly:
    """Sparse QQ[E,G,J,c] polynomials with complete coefficient records."""
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {(0, 0, 0, 0): F(terms)}
        self.terms = {m: F(a) for m, a in terms.items() if a}

    def __add__(self, other):
        d = dict(self.terms)
        for m, a in Poly(other).terms.items():
            d[m] = d.get(m, F(0)) + a
        return Poly(d)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -a for m, a in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        d = {}
        for m, a in self.terms.items():
            for n, b in Poly(other).terms.items():
                k = tuple(x + y for x, y in zip(m, n))
                d[k] = d.get(k, F(0)) + a * b
        return Poly(d)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(power >= 0, 'nonnegative polynomial power')
        out = Poly(1)
        for _ in range(power):
            out *= self
        return out

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def derivative(self, index):
        out = {}
        for m, a in self.terms.items():
            if m[index]:
                n = list(m)
                n[index] -= 1
                out[tuple(n)] = a * m[index]
        return Poly(out)

    def evaluate(self, values):
        out = F(0)
        for m, a in self.terms.items():
            for index, exponent in enumerate(m):
                a *= values[index] ** exponent
            out += a
        return out

    def record(self):
        return [[list(m), str(a)] for m, a in sorted(self.terms.items())]


class Dual:
    """QQ[eps]/(eps^2), retaining moving critical-node derivatives."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Dual):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = Dual(other)
        return Dual(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.a, -self.b)

    def __sub__(self, other):
        return self + -Dual(other)

    def __rsub__(self, other):
        return Dual(other) - self

    def __mul__(self, other):
        other = Dual(other)
        return Dual(self.a * other.a, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Dual(other)
        require(other.a != 0, 'dual divisor is a unit')
        return Dual(self.a / other.a,
                    (self.b * other.a - self.a * other.b) / other.a ** 2)

    def __rtruediv__(self, other):
        return Dual(other) / self

    def __bool__(self):
        return bool(self.a or self.b)

    def __eq__(self, other):
        other = Dual(other)
        return self.a == other.a and self.b == other.b


def transpose(a):
    return [list(row) for row in zip(*a)]


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def matmul(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def solve(a, b):
    n = len(a)
    aug = [list(row) + [value] for row, value in zip(a, b)]
    for col in range(n):
        def unit(value):
            return value.a != 0 if isinstance(value, Dual) else bool(value)
        pivot = next((r for r in range(col, n) if unit(aug[r][col])), None)
        require(pivot is not None, 'nonsingular exact linear system')
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[-1] for row in aug]


def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return p


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def divrem(a, b):
    a, b = trim(a), trim(b)
    require(bool(b), 'polynomial divisor nonzero')
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        k = len(a) - len(b)
        factor = a[-1] / b[-1]
        q[k] += factor
        for i, x in enumerate(b):
            a[i + k] -= factor * x
        a = trim(a)
    return trim(q), a


def derivative(p):
    return [i * p[i] for i in range(1, len(p))]


def newton(h, count):
    n = len(h) - 1
    out = [n]
    for k in range(1, count + 1):
        if k <= n:
            value = -sum(h[n - i] * out[k - i] for i in range(1, k)) - k * h[n - k]
        else:
            value = -sum(h[n - i] * out[k - i] for i in range(1, n + 1))
        out.append(value)
    return out


def sturm_count(p):
    chain = [trim(p), trim(derivative(p))]
    while chain[-1]:
        _, remainder = divrem(chain[-2], chain[-1])
        if not remainder:
            break
        chain.append([-x for x in remainder])
    def variations(signs):
        signs = [x for x in signs if x]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    positive = [1 if q[-1] > 0 else -1 for q in chain]
    negative = [v * (-1) ** (len(q) - 1) for q, v in zip(chain, positive)]
    return variations(negative) - variations(positive)


def original_poly(e, g, j, c):
    return [c, 8 * j, 4 * g, 0, 2 * e, 0, -F(1, 2), 0, F(1)]


def critical_poly(e, g, j):
    return [j, g, 0, e, 0, -F(3, 8), 0, F(1)]


def eta_from_quotient(e, g, j, c, direction=None, freeze_nodes=False):
    values = [e, g, j, c]
    if direction is not None:
        values = [Dual(x, int(i == direction)) for i, x in enumerate(values)]
    f = original_poly(*values)
    h = critical_poly(*values[:3])
    if freeze_nodes:
        h = [Dual(x.a) if isinstance(x, Dual) else x for x in h]
    hp = derivative(h)
    columns = []
    for k in range(7):
        remainder = divrem([0] * k + hp, h)[1]
        columns.append(remainder + [0] * (7 - len(remainder)))
    target = divrem([-8 * x for x in f], h)[1]
    target += [0] * (7 - len(target))
    p = solve(transpose(columns), target)
    pp = mul(p, p)
    tau = newton(h, 12)
    eta = sum(x * tau[k] for k, x in enumerate(pp))
    return eta, p


def universal():
    e, g, j, c = [Poly({tuple(int(i == k) for i in range(4)): 1}) for k in range(4)]
    h = critical_poly(e, g, j)
    tau = [Poly(x) for x in newton(h, 11)]
    explicit = [7, 0, F(3, 4), 0, F(9, 32) - 4 * e, 0,
                F(27, 256) - F(9, 4) * e - 6 * g, -7 * j,
                F(81, 2048) - F(9, 8) * e + 4 * e ** 2 - 3 * g,
                -F(27, 8) * j,
                F(243, 16384) - F(135, 256) * e + F(15, 4) * e ** 2
                - F(45, 32) * g + 10 * e * g,
                F(11) * e * j - F(99, 64) * j]
    require(all(x == y for x, y in zip(tau, explicit)), 'all twelve Newton traces')
    # Laurent division of 8(zh-f)/h: m_k is the coefficient of z^(-k-1).
    numerator = [1, 0, -8 * e, 0, -24 * g, -56 * j, -8 * c]
    reversed_h = list(reversed(h))
    moments = []
    for k in range(7):
        moments.append(Poly(numerator[k]) - sum(reversed_h[i] * moments[k - i]
                                               for i in range(1, k + 1)))
    explicit_mu = [1, 0, F(3, 8) - 8 * e, 0,
                   F(9, 64) - 4 * e - 24 * g, -56 * j,
                   F(27, 512) - F(15, 8) * e + 8 * e ** 2 - 10 * g - 8 * c]
    require(all(x == y for x, y in zip(moments, explicit_mu)), 'all seven coupling moments')
    gram = [[tau[i + k] for k in range(6)] for i in range(6)]
    perm = [0, 2, 4, 1, 3, 5]
    parity = [[gram[i][k] for k in perm] for i in perm]
    u0 = [[0, 0, 0], [0, 0, -7], [0, -7, -F(27, 8)]]
    require(all(parity[i][k + 3] == j * u0[i][k] for i in range(3) for k in range(3)),
            'whole parity cross block')
    require(all(parity[i][k].derivative(2) == 0 for i in range(3) for k in range(3)), 'A independent of J')
    require(all(parity[i + 3][k + 3].derivative(2) == 0 for i in range(3) for k in range(3)), 'B independent of J')
    exceptional_e = F(25, 448)
    require(F(3, 8) - 8 * exceptional_e == -F(1, 14), 'exception outside D>0')
    require(7 * -F(5, 7) + 8 * F(3, 4) == 1, 'exception first normal equation')
    require(-F(5, 7) * F(3, 4) + 8 * (F(9, 32) - 4 * exceptional_e)
            == F(3, 8) - 8 * exceptional_e, 'exception second normal equation')
    k = tau[4] - F(9, 112)
    ell = tau[6] - F(3, 28) * tau[4]
    delta = moments[2] - F(3, 28) - 8 * k
    d = F(3, 8) - 8 * e
    require(delta == -3 * (d + F(1, 14)), 'complete quantitative mismatch')
    q1 = ell * F(1, 7) - k * F(27, 392)
    q2 = k * F(1, 7)
    # These CLOSED rational budgets bound |q1|,|q2| from the real traces.
    require(F(9, 16) - F(9, 112) == F(27, 56), 'k upper budget')
    require(F(27, 64) + F(3, 28) * F(9, 16) == F(27, 56), 'ell absolute budget')
    require(F(27, 392) + F(27, 392) * F(27, 56) == F(2241, 21952), 'q1 absolute budget')
    require(F(2241, 21952) < F(3, 28) and F(27, 392) < F(1, 14), 'q coordinate bounds')
    require(F(3, 28) ** 2 + F(1, 14) ** 2 == F(13, 784) < F(1, 49), 'strict q norm bound')
    require(F(4, 9) * 49 * 9 == 196, 'Schur derivative lower coefficient')
    require(49 * 4 * F(1, 14) == 14, 'uniform linear gradient coefficient')
    require(56 ** 2 / F(4) == 784 and 56 ** 2 / F(56) == 56, 'seventh moment conversion')
    record = {'traces': [x.record() for x in tau], 'coupling_moments': [x.record() for x in moments],
              'gram': [[x.record() for x in row] for row in gram],
              'all_four_gram_derivatives': [[[x.derivative(index).record() for x in row]
                                            for row in gram] for index in range(4)],
              'all_four_moment_derivatives': [[x.derivative(index).record() for x in moments[:6]]
                                              for index in range(4)],
              'U': [[str(x) for x in row] for row in u0],
              'mismatch': delta.record(), 'q1': q1.record(), 'q2': q2.record(),
              'exception_E_D': [str(exceptional_e), '-1/14'],
              'closed_bounds': ['27/56', '27/56', '2241/21952', '27/392', '13/784', '1/49', '9/4', '196', '14']}
    return record, tau, moments, gram


def control(squares, j, universal_data, require_actual=True):
    f0 = [F(1)]
    for square in squares:
        f0 = mul(f0, [-square, 0, 1])
    require(f0[6] == -F(1, 2), 'original square normalization')
    require(sturm_count(f0) == 8, 'base eight real distinct original roots')
    e, g = f0[4] / 2, f0[2] / 4
    h = critical_poly(e, g, j)
    require(sturm_count(h) == 7, 'seven actual real simple criticals')
    _, tau_polys, mu_polys, gram_polys = universal_data
    values = [e, g, j, F(0)]
    tau = [p.evaluate(values) for p in tau_polys]
    mu = [p.evaluate(values) for p in mu_polys[:6]]
    gram = [[p.evaluate(values) for p in row] for row in gram_polys]
    beta = solve(gram, mu)
    r6 = dot(mu, beta)
    cstar = (F(27, 512) - F(15, 8) * e + 8 * e ** 2 - 10 * g
             - dot(tau[6:12], beta)) / 8
    f = original_poly(e, g, j, cstar)
    originals = sturm_count(f)
    if require_actual:
        require(originals == 8, 'eight actual distinct real originals at center')
    eta, p = eta_from_quotient(e, g, j, cstar)
    require(eta == r6, 'complete quotient trace equals six-moment projection')
    require(p[6] == 0 and p[:6] == beta, 'complete degree-five centered mass interpolant')
    d = F(3, 8) - 8 * e
    require(d > 0, 'positive angular denominator')
    cbar = (1 - r6) / d
    eta_grad = []
    c_grad = []
    for index in range(4):
        actual, _ = eta_from_quotient(e, g, j, cstar, index)
        require(actual.a == eta, 'dual constant term agrees')
        gm = [[p.derivative(index).evaluate(values) for p in row] for row in gram_polys]
        mm = [p.derivative(index).evaluate(values) for p in mu_polys[:6]]
        expected = 2 * dot(beta, mm) - dot(beta, matvec(gm, beta))
        require(actual.b == expected, 'full moving-node derivative agrees with Gram derivative')
        eta_grad.append(actual.b)
        c_grad.append((8 * cbar - actual.b) / d if index == 0 else -actual.b / d)
        dual_c = (1 - actual) / Dual(d, -8 if index == 0 else 0)
        require(dual_c.a == cbar and dual_c.b == c_grad[-1], 'whole quotient C derivative including D motion')
    require(eta_grad[3] == 0, 'actual constant derivative vanishes')
    perm = [0, 2, 4, 1, 3, 5]
    ag = [[gram[i][k] for k in perm[:3]] for i in perm[:3]]
    bg = [[gram[i][k] for k in perm[3:]] for i in perm[3:]]
    u0 = [[F(0), F(0), F(0)], [F(0), F(0), F(-7)], [F(0), F(-7), -F(27, 8)]]
    u = [mu[i] for i in perm[:3]]
    y = solve(ag, u)
    w = [a - b for a, b in zip([0, 0, -56], matvec(transpose(u0), y))]
    aiu = transpose([solve(ag, col) for col in transpose(u0)])
    q = matmul(transpose(u0), aiu)
    schur = [[bg[i][k] - j ** 2 * q[i][k] for k in range(3)] for i in range(3)]
    v = solve(schur, w)
    hh = dot(v, matvec(bg, v))
    require(hh > 196 * (d + F(1, 14)) ** 2, 'strict universal Schur derivative budget')
    require(c_grad[2] == -2 * j * hh / d, 'full J derivative has claimed strict factor')
    if j:
        require(j * c_grad[2] / 8 < -14 * j ** 2, 'actual signed linear-coefficient gradient bound')
        frozen, _ = eta_from_quotient(e, g, j, cstar, 2, freeze_nodes=True)
        require(frozen.b != eta_grad[2], 'frozen criticals give a wrong J derivative')
    return {'squares': [str(x) for x in squares], 'base_c': str(f0[0]),
            'base_original_real_distinct_count': 8,
            'E_G_J_cstar': [str(x) for x in [e, g, j, cstar]],
            'critical_real_distinct_count': 7, 'original_real_distinct_count': originals,
            'whole_beta': [str(x) for x in beta], 'whole_mass_interpolant': [str(x) for x in p],
            'R6_D_Cbar': [str(x) for x in [r6, d, cbar]],
            'all_four_moving_eta_derivatives': [str(x) for x in eta_grad],
            'all_four_centered_C_derivatives': [str(x) for x in c_grad],
            'w_Schur_positive_factor': [*[str(x) for x in w], str(hh)],
            'center_is_actual_eight_real': originals == 8}


def build_record():
    data = universal()
    squares = [F(x, 168) for x in [1, 9, 25, 49]]
    controls = [control(squares, F(0), data),
                control(squares, F(1, 10 ** 7), data),
                control(squares, -F(1, 10 ** 7), data),
                control([F(x, 20) for x in [1, 2, 3, 4]], F(0), data, require_actual=False)]
    require(controls[1]['R6_D_Cbar'] == controls[2]['R6_D_Cbar'], 'whole reflection scalar control')
    positive = [F(x) for x in controls[1]['all_four_centered_C_derivatives']]
    negative = [F(x) for x in controls[2]['all_four_centered_C_derivatives']]
    require(negative == [positive[0], positive[1], -positive[2], positive[3]], 'whole reflected gradient')
    penalty = F(controls[0]['R6_D_Cbar'][2]) - F(controls[1]['R6_D_Cbar'][2])
    require(penalty > 56 * F(controls[1]['E_G_J_cstar'][2]) ** 2, 'whole integrated penalty control')
    require(controls[3]['base_c'] == '3/20000' and controls[3]['E_G_J_cstar'][3] == '1/7040'
            and controls[3]['original_real_distinct_count'] == 4, 'center can be infeasible within two-moment locus')
    infeasible_constant = F(9, 2560000) - F(7, 880000)
    require(infeasible_constant < 0 and F(1, 64) ** 2 - F(1, 160) * F(1, 64) + infeasible_constant > 0,
            'elementary exact four-real-root factor signs')
    damages = {}
    def rejected(label, callback):
        try:
            callback()
        except ValueError:
            damages[label] = 'rejected'
        else:
            raise ValueError('damage escaped: ' + label)
    record = data[0]
    rejected('missing parity cross block', lambda: require(record['U'][1][2] == '0', 'literal nonzero U'))
    rejected('wrong fifth coupling moment', lambda: require(data[2][5] == 0, 'literal -56J'))
    rejected('wrong Schur derivative sign', lambda: require(positive[2] > 0, 'positive J has negative derivative'))
    rejected('wrong exception regarded feasible', lambda: require(F(record['exception_E_D'][1]) > 0, 'D=-1/14'))
    rejected('removed moving-node term', lambda: require(eta_from_quotient(*[F(x) for x in controls[1]['E_G_J_cstar']], 2, freeze_nodes=True)[0].b
                                                       == F(controls[1]['all_four_moving_eta_derivatives'][2]), 'frozen node damage'))
    rejected('reversed strict budget', lambda: require(F(13, 784) >= F(1, 49), 'exact strict norm budget'))
    # A derivative spectrum is insufficient to assert eight real originals.
    e, g, j, c = [F(x) for x in controls[1]['E_G_J_cstar']]
    outside = original_poly(e, g, j, F(1))
    outside_count = sturm_count(outside)
    require(outside_count < 8 and sturm_count(critical_poly(e, g, j)) == 7,
            'actual primitive feasibility obstruction retained')
    rejected('seven real criticals imply eight real originals', lambda: require(outside_count == 8, 'Sturm primitive obstruction'))
    rejected('unconstrained center always feasible on two-moment locus', lambda: require(controls[3]['center_is_actual_eight_real'], 'exact four-real-root center'))
    rejected('omitted angular denominator derivative', lambda: require(-F(controls[0]['all_four_moving_eta_derivatives'][0])
                                                                      / F(controls[0]['R6_D_Cbar'][1])
                                                                      == F(controls[0]['all_four_centered_C_derivatives'][0]), 'missing D_E=-8'))
    return {'actual_agent': 'six-sendov-2', 'role': 'researcher',
            'status': 'ordinary author proof; exact finite corroboration; unformalized and independently unreviewed',
            'universal': record, 'controls': controls,
            'primitive_feasibility_obstruction': {'same_seven_real_criticals': True, 'changed_c': '1', 'original_distinct_real_count': outside_count},
            'damage_controls': damages,
            'proof_boundaries': ['positivity of real Vandermonde Gram and Schur complement',
                                 'ordinary derivative and constant-term least-squares bridges',
                                 'local legality of four constrained coefficient directions',
                                 'odd horizontal-level hyperbolicity interval',
                                 'credited even stationary exclusion and continuous compactness']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true', help='print entire recomputed record without fixture comparison')
    parser.add_argument('--fixture', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    started = time.monotonic()
    record = build_record()
    encoded = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if args.record:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        expected = json.loads(args.fixture.read_text())
        require(record == expected, 'entire external fixture differs, including missing/extra fields')
        print(json.dumps({'whole_record_sha256': digest, 'universal_traces': 12, 'coupling_moments': 7,
                          'gram_entries': 36, 'gram_derivative_entries': 144, 'moment_derivatives': 24,
                          'center_controls': len(record['controls']),
                          'actual_centered_profiles': sum(r['center_is_actual_eight_real'] for r in record['controls']),
                          'full_moving_derivatives': 4 * len(record['controls']),
                          'semantic_damages_rejected': len(record['damage_controls']),
                          'elapsed_seconds': round(time.monotonic() - started, 6)}))


if __name__ == '__main__':
    main()
