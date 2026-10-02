#!/usr/bin/env python3
"""Exact global REAL rank-one exclusion for the complete angular pencil.

Actual six-sendov-2, researcher. Same-author9602/9550 kernels are credited;
this is neither independent review nor proof-assistant formalization.
Runtime: Python standard library only. All matrix and elimination coefficients
are regenerated. Resultant identities use fixed Sylvester matrices and proved
degree bounds; finite evaluations certify identities, not root nonexistence.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd, lcm, isqrt
import argparse, hashlib, importlib.util, json

INPUT_COMMIT = '134a00737a4f0f8cbd5e33197590f131d74baa4a'
INPUT_FILES = {
    'verify.py': '7c2c7add938771629bd6765acc052efb55796a4a3061b6b40b3be6096e7ea6f2',
    'expected.json': '574264c6c1ae0a2851e63db94137aff44c5cd0102d36cd2f5dec0c69ecd7862a'}
INPUT_RECORD = 'c9668ae809521be840196d962c7563e1a89718a50ce122a144e93b525cdbba44'
PRIME = 257
# Candidate integer factors, coefficients in ascending powers of x. Their
# ENTIRE product is checked against the characteristic-zero determinant.
S5 = [
    1878249696897024,
    137517513338916480,
    -949012690531122084,
    -47045003408526384373,
    -516919826627115107546,
    4665265033450726317767,
]
P20 = [
    -5447729122472491706796885548483935511329357824,
    -18751569283013198358543394803820494102457860096,
    -1399264772618767249232318505952440605523949811712,
    -311226691728316776765339146124968371171025932899840,
    -4758581175168707062102303551439389627223127922788000,
    -39237629418609879120015659371263781004490858525765888,
    -244472609700574621568604326595399388278378546856247444,
    -5445091184157448178991762582166793385933991777758098456,
    -84498547627843093029999031638307152437952918908843787887,
    -56705855069279089584088199862975347726268747154489440128,
    -2529092016473167757971489408466827723176502541846977424946,
    32225603765356606506714538422361042425814452235118650026484,
    -111092625555161377675646882342400467971872479000710890019071,
    1427302882478033146138226440073550343482606962425437752779980,
    -4670102578642665736076180945258640135239571505245052420315860,
    -862956175294290038577498974318917638200780174803625530353600,
    -2890890919793879257978181941610722480169352920767138438078800,
    -74223824133605734972022945777786853235784711160613065539880000,
    324176982834203168592859987003286455173752242697298679812360000,
    -262401506181336494047747344872516983291851759804314897563200000,
    1682406513386732369627639529362524119993790686195129083280000000,
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def same_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_typed(x, y) for x, y in zip(a, b))
    return a == b


class Capture:
    def write_text(self, value):
        self.data = json.loads(value)


def input9602():
    directory = Path(__file__).resolve().parent.parent/'regular-linear-pencil'
    for name, digest in INPUT_FILES.items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
                'pinned9602 source '+name)
    spec = importlib.util.spec_from_file_location('sendov9602_rank_input', directory/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    capture = Capture()
    record = module.certificate(capture)
    require(same_typed(record, json.loads((directory/'expected.json').read_text())),
            'entire typed9602 fixture')
    require(hashlib.sha256(canonical(record)).hexdigest() == INPUT_RECORD,
            'entire9602 record digest')
    # The preceding call also byte-pins9550 and regenerates its entire fixture.
    kernel, data = module.parent_input()
    require(data == capture.data['parent_reconstruction'], 'both complete input regenerations agree')
    return kernel, data, capture.data


class Poly:
    """Sparse QQ[q,r,x], only nonnegative integral exponents."""
    zero = (0, 0, 0)

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            require(all(len(k) == 3 and all(type(e) is int and e >= 0 for e in k)
                        for k in value), 'ordinary three-variable domain')
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
        else:
            self.c = {self.zero: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for key, c in Poly(other).c.items():
            out[key] = out.get(key, F(0))+c
            if not out[key]:
                del out[key]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+-Poly(other)

    def __rsub__(self, other):
        return Poly(other)+-self

    def __mul__(self, other):
        out = {}
        for k, a in self.c.items():
            for j, b in Poly(other).c.items():
                key = tuple(x+y for x, y in zip(k, j))
                out[key] = out.get(key, F(0))+a*b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(type(exponent) is int and exponent >= 0, 'nonnegative integer power')
        out = Poly(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        return self.c == Poly(other).c

    def degree(self, index):
        return max((key[index] for key in self.c), default=0)

    def coefficients(self, index):
        out = [Poly(0) for _ in range(self.degree(index)+1)]
        for key, c in self.c.items():
            new = list(key)
            new[index] = 0
            out[key[index]] += Poly({tuple(new): c})
        return out

    def encoded(self):
        return [[list(k), str(c)] for k, c in sorted(self.c.items())]


def variable(index):
    key = [0, 0, 0]
    key[index] = 1
    return Poly({tuple(key): 1})


def primitive(poly, positive_leading=False):
    poly = Poly(poly)
    require(bool(poly.c), 'primitive input nonzero')
    den = lcm(*(c.denominator for c in poly.c.values()))
    common = 0
    for c in poly.c.values():
        common = gcd(common, abs(int(c*den)))
    if positive_leading and poly.c[max(poly.c)] < 0:
        common = -common
    content = F(common, den)
    out = F(1)/content*poly
    require(all(c.denominator == 1 for c in out.c.values()), 'integer primitive result')
    require(content*out == poly, 'whole primitive content identity')
    return out, content


def divide_x_linear(poly, slope, constant):
    """Complete long division in x, over QQ[q,r]; no pointwise division."""
    a = Poly(poly).coefficients(2)
    quotient = [Poly(0) for _ in range(max(1, len(a)-1))]
    while len(a) > 1:
        c, j = F(1, slope)*a[-1], len(a)-2
        quotient[j] = c
        a[j] -= constant*c
        a.pop()
    x = variable(2)
    out = sum((c*x**j for j, c in enumerate(quotient)), Poly(0))
    require(out*(slope*x+constant)+a[0] == poly, 'whole linear division identity')
    return out, a[0]


def remove_positive_factors(poly):
    out, factors = Poly(poly), []
    for slope, constant in [(49, 2), (7, 4)]:
        multiplicity = 0
        while out.degree(2) > 0:
            quotient, rest = divide_x_linear(out, slope, constant)
            if rest != 0:
                break
            out = quotient
            multiplicity += 1
        factors.append([slope, constant, multiplicity])
    normalized, content = primitive(out, positive_leading=True)
    x = variable(2)
    reconstructed = content*normalized
    for slope, constant, multiplicity in factors:
        reconstructed *= (slope*x+constant)**multiplicity
    require(reconstructed == poly, 'whole positive-factor normalization identity')
    return normalized, {'nonzero_rational_content': str(content),
                        'removed_real_positive_factors': factors}


def regenerate_equations(kernel, data, linear):
    K = kernel.P
    B, E, r, s = [kernel.variable(i) for i in range(4)]

    def decode(raw):
        require(all(len(key) == 5 and all(type(e) is int and e >= 0 for e in key)
                    and key[4] == 0 for key, c in raw), 'complete four-parameter matrix domain')
        return K({tuple(key+[0]*5): F(c) for key, c in raw})

    M = [[decode(a) for a in row] for row in data['matrix_rows_ABC']]
    U = [M[0][j]-14*M[4][j] for j in range(3)]
    V = 924672*B*r*s-848736*B*s**3+302976*B*s
    V += 3849440*r*r*s*s+219520*r*r-4602080*r*s**4+2603440*r*s*s+146880*r
    V += 1286250*s**6-1694385*s**4+403500*s*s+22860
    denominator = 21120*(49*s*s+2)
    require(-3360*decode(linear['linear_b'][3]) == denominator*E+V,
            'complete rank-one E equation from regenerated input')
    require(U[2] == -48*(7*s*s+4), 'complete real reference constant')
    equations, normalizations = {}, {}
    for name, row, column, s_power in [('f', 0, 1, 1), ('g', 1, 1, 0),
                                      ('f2', 2, 1, 1), ('A0', 0, 0, 0)]:
        wedge = U[2]*M[row][column]-M[row][2]*U[column]
        degree = max((key[1] for key in wedge.c), default=0)
        require(degree <= 2, 'bounded E-degree of necessary wedge')
        cleared = K(0)
        for key, c in wedge.c.items():
            new = list(key)
            new[1] = 0
            cleared += K({tuple(new): c})*(-V)**key[1]*denominator**(degree-key[1])
        # B=q*s; only then cancel the explicitly known nonzero s power.
        # Exponent parity is checked for EVERY coefficient before x=s².
        output = {}
        for key, c in cleared.c.items():
            require(key[1] == 0 and all(e == 0 for e in key[4:]), 'cleared ordinary B,r,s domain')
            spower = key[3]+key[0]-s_power
            require(spower >= 0 and spower % 2 == 0, 'entire s division and even-parity reduction')
            new = (key[0], key[2], spower//2)
            output[new] = output.get(new, F(0))+c
        raw = Poly(output)
        equations[name], factors = remove_positive_factors(raw)
        normalizations[name] = {'matrix_row': row, 'matrix_column': column,
            'cleared_E_denominator_power': degree, 'canceled_known_nonzero_s_power': s_power,
            **factors, 'raw_cleared_sha256': hashlib.sha256(canonical(raw.encoded())).hexdigest()}
    return equations, normalizations


def trim(a, prime=None):
    a = [x % prime for x in a] if prime else list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def add(a, b, prime=None):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))], prime)


def scale(c, a, prime=None):
    return trim([c*x for x in a], prime)


def multiply(a, b, prime=None):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out, prime)


def evaluate(a, x, prime=None):
    out = 0
    for c in reversed(a):
        out = out*x+c
        if prime:
            out %= prime
    return out


def sylvester_data(left, right):
    left, right = Poly(left), Poly(right)
    require(all(key[0] == 0 for poly in [left, right] for key in poly.c),
            'univariate r resultant over QQ[x]')

    def coeffs(poly):
        out = [[0]*(poly.degree(2)+1) for _ in range(poly.degree(1)+1)]
        for (q, r, x), c in poly.c.items():
            require(c.denominator == 1, 'integer Sylvester coefficient')
            out[r][x] = int(c)
        return [trim(a) for a in out]

    a, b = coeffs(left), coeffs(right)
    n = len(a)+len(b)-2
    degree_bound = n*max(left.degree(2), right.degree(2))
    return a, b, n, degree_bound


def fixed_sylvester(a, b, x, prime=None):
    """Dimensions use formal r degrees, NEVER degrees after evaluation."""
    m, n = len(a)-1, len(b)-1
    size = m+n
    av, bv = [evaluate(c, x, prime) for c in a], [evaluate(c, x, prime) for c in b]
    rows = []
    for coeff, count in [(av, n), (bv, m)]:
        for j in reversed(range(count)):
            row = [0]*size
            for k, c in enumerate(coeff):
                row[size-1-k-j] = c
            rows.append(row)
    require(len(rows) == size and all(len(row) == size for row in rows), 'fixed Sylvester size')
    return rows


def determinant_integer(rows):
    """Pivoted fraction-free Bareiss; every division checked exact."""
    a = [list(row) for row in rows]
    n, previous, sign = len(a), 1, 1
    for k in range(n-1):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        value = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*value-a[i][k]*a[k][j]
                quotient, rest = divmod(numerator, previous)
                require(rest == 0, 'every Bareiss division exact')
                a[i][j] = quotient
            a[i][k] = 0
        previous = value
    return sign*a[-1][-1]


def determinant_finite(rows, prime):
    a = [[c % prime for c in row] for row in rows]
    answer, n = 1, len(a)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            answer = -answer
        value = a[k][k]
        answer = answer*value % prime
        inverse = pow(value, -1, prime)
        for i in range(k+1, n):
            factor = a[i][k]*inverse % prime
            for j in range(k+1, n):
                a[i][j] = (a[i][j]-factor*a[k][j]) % prime
            a[i][k] = 0
    return answer % prime


def is_prime(prime):
    return type(prime) is int and prime >= 2 and all(prime % d for d in range(2, isqrt(prime)+1))


def interpolate_finite(values, prime):
    """Newton forward differences at 0..D, with D<prime."""
    require(is_prime(prime) and len(values) <= prime, 'prime and distinct interpolation points')
    difference, basis, result = list(values), [1], [0]
    for k in range(len(values)):
        result = add(result, scale(difference[0], basis, prime), prime)
        difference = [(difference[i+1]-difference[i]) % prime for i in range(len(difference)-1)]
        if k+1 < len(values):
            basis = scale(pow(k+1, -1, prime), multiply(basis, [-k, 1], prime), prime)
    require(all(evaluate(result, x, prime) == y for x, y in enumerate(values)),
            'whole finite interpolation values')
    return result


def finite_resultant(left, right, prime):
    a, b, size, bound = sylvester_data(left, right)
    require(is_prime(prime) and bound < prime, 'proved determinant bound below prime')
    values = [determinant_finite(fixed_sylvester(a, b, x, prime), prime) for x in range(bound+1)]
    out = interpolate_finite(values, prime)
    require(len(out)-1 <= bound, 'entire reconstructed determinant degree bound')
    return out, {'fixed_r_degrees': [len(a)-1, len(b)-1], 'Sylvester_size': size,
                 'proved_x_degree_bound': bound, 'exact_distinct_evaluations': len(values),
                 'actual_reconstructed_degree': len(out)-1,
                 'full_values_sha256': hashlib.sha256(canonical(values)).hexdigest()}


def divide_finite(a, b, prime):
    a, b = trim(a, prime), trim(b, prime)
    require(b != [0], 'finite polynomial divisor nonzero')
    q = [0]*max(1, len(a)-len(b)+1)
    inverse = pow(b[-1], -1, prime)
    while a != [0] and len(a) >= len(b):
        j, c = len(a)-len(b), a[-1]*inverse % prime
        q[j] = c
        a = add(a, [0]*j+scale(-c, b, prime), prime)
    return trim(q, prime), a


def verify_unit(factor, resultant, u, v, prime):
    require(add(multiply(factor, u, prime), multiply(resultant, v, prime), prime) == [1],
            'ENTIRE finite unit coefficient identity')


def finite_unit(factor, resultant, prime):
    original = list(factor)
    require(all(type(c) is int for c in original) and original[-1] % prime != 0,
            'Gauss bridge: integer factor leading degree preserved')
    factor, resultant = trim(factor, prime), trim(resultant, prime)
    require(len(factor) == len(original), 'entire factor degree preserved modulo prime')
    a0, a1 = factor, resultant
    u0, u1, v0, v1 = [1], [0], [0], [1]
    while a1 != [0]:
        q, rest = divide_finite(a0, a1, prime)
        a0, a1 = a1, rest
        u0, u1 = u1, add(u0, scale(-1, multiply(q, u1, prime), prime), prime)
        v0, v1 = v1, add(v0, scale(-1, multiply(q, v1, prime), prime), prime)
    require(len(a0) == 1 and a0[0] != 0, 'univariate modular gcd is a unit')
    inverse = pow(a0[0], -1, prime)
    u, v = scale(inverse, u0, prime), scale(inverse, v0, prime)
    verify_unit(factor, resultant, u, v, prime)
    return {'prime': prime, 'factor': factor, 'resultant': resultant,
            'factor_multiplier': u, 'resultant_multiplier': v, 'whole_product': [1],
            'integer_factor_degree_preserved': True}


def factored_resultant(values, bound, s5, p20, s_power=5, factor_power=2):
    require(len(values) == bound+1, 'entire identity uses bound+1 distinct rational points')
    rhs = [0]*s_power+[1]
    for _ in range(factor_power):
        rhs = multiply(rhs, s5)
    rhs = multiply(rhs, p20)
    require(len(rhs)-1 <= bound and evaluate(rhs, 1) != 0, 'factor candidate degree and nonzero calibration')
    content = F(values[1], evaluate(rhs, 1))
    require(content != 0, 'characteristic-zero determinant scale nonzero')
    require(all(F(value) == content*evaluate(rhs, x) for x, value in enumerate(values)),
            'ENTIRE characteristic-zero resultant factorization')
    return content, len(rhs)-1


def clear_quadratic(poly, affine):
    # Necessity only, valid also when the affine slope VANISHES.
    coeff, linear = Poly(poly).coefficients(0), Poly(affine).coefficients(0)
    require(len(coeff) == 3 and len(linear) == 2, 'formal quadratic and affine degrees')
    b, a = linear
    return coeff[2]*b*b-coeff[1]*a*b+coeff[0]*a*a


def clearing_syzygy(poly, affine):
    coeff = Poly(poly).coefficients(0)
    b, a = Poly(affine).coefficients(0)
    q = variable(0)
    cleared = clear_quadratic(poly, affine)
    require(a*a*poly-cleared == affine*(a*coeff[2]*q+a*coeff[1]-b*coeff[2]),
            'whole necessity syzygy, including zero affine slope')


def controls():
    q, r, x = [variable(i) for i in range(3)]
    result = []
    # These are algebraic bridge controls, NOT enumerated stationary profiles.
    for name, f, h, g in [('first_pivot_zero', Poly(0), q-1, q*q-1),
                         ('second_pivot_zero', q-1, Poly(0), q*q-1),
                         ('both_pivots_zero', Poly(0), Poly(0), q*q+1)]:
        def padded(poly):
            out = poly.coefficients(0)
            return out+[Poly(0)]*(2-len(out))
        b, a = padded(f)
        d, c = padded(h)
        gc = g.coefficients(0)
        Cf = gc[2]*b*b-gc[1]*a*b+gc[0]*a*a
        Ch = gc[2]*d*d-gc[1]*c*d+gc[0]*c*c
        if name == 'both_pivots_zero':
            require(Cf == Ch == 0, 'clears are necessary only, not sufficient')
        else:
            require(Cf == Ch == 0, 'zero-pivot bridge retains a genuine finite root')
        result.append(name)
    # A specialized leading coefficient can vanish; the formal matrix stays 2x2.
    a, b, size, bound = sylvester_data(x*r, r-1)
    rows = fixed_sylvester(a, b, 0)
    require(size == 2 and rows == [[0, 0], [1, -1]] and determinant_integer(rows) == 0,
            'fixed degree-loss resultant necessity')
    result.append('specialized_leading_coefficient_zero')
    known = [3, 5, 2]
    samples = [evaluate(known, j, PRIME) for j in range(3)]
    require(interpolate_finite(samples, PRIME) == known, 'finite reconstruction independent small control')
    result.append('finite_interpolation_small_polynomial')
    require(determinant_integer([[0, 1], [1, 0]]) == -1,
            'integer determinant row-pivot sign')
    require(determinant_finite([[0, 1], [1, 0]], PRIME) == PRIME-1,
            'finite determinant row-pivot sign')
    result.append('both_determinant_pivot_signs')
    return result


def certificate(export=None):
    kernel, data, linear = input9602()
    equations, normalizations = regenerate_equations(kernel, data, linear)
    f, g, f2, A0 = [equations[name] for name in ['f', 'g', 'f2', 'A0']]
    h = f2-6*g
    require(f.degree(0) == h.degree(0) == 1 and g.degree(0) == A0.degree(0) == 2,
            'entire two-pivot affine/quadratic degree cancellation')
    b, a = f.coefficients(0)
    d, c = h.coefficients(0)
    cross = a*d-c*b
    require(a*h-c*f == cross, 'whole affine cross necessity')
    for poly, affine in [(g, f), (g, h), (A0, f)]:
        clearing_syzygy(poly, affine)
    x = variable(2)
    P5, rest = divide_x_linear(F(1, 17740800)*cross, 49, 2)
    require(rest == 0 and cross == 17740800*(49*x+2)*P5,
            'whole P5 cross factorization')
    P7, rest = divide_x_linear(F(-1, 35481600)*clear_quadratic(g, f), 49, 2)
    require(rest == 0 and clear_quadratic(g, f) == -35481600*(49*x+2)*P7,
            'whole P7 first-pivot quadratic factorization')
    bh, ch = primitive(clear_quadratic(g, h))
    bA, cA = primitive(clear_quadratic(A0, f))
    aa, bb, size, bound = sylvester_data(P5, P7)
    require([len(aa)-1, len(bb)-1, size, bound] == [5, 7, 12, 84],
            'proved characteristic-zero fixed degrees and determinant bound')
    values = [determinant_integer(fixed_sylvester(aa, bb, j)) for j in range(bound+1)]
    content, degree = factored_resultant(values, bound, S5, P20)
    Rh, rh_data = finite_resultant(P5, bh, PRIME)
    RA, ra_data = finite_resultant(P5, bA, PRIME)
    units = {'S5_branch': finite_unit(S5, Rh, PRIME), 'P20_branch': finite_unit(P20, RA, PRIME)}
    require(set(units) == {'S5_branch', 'P20_branch'}, 'every nonzero resultant factor branch retained')
    damages = []

    def damaged_factor():
        changed = list(P20)
        changed[7] += 1
        factored_resultant(values, bound, S5, changed)

    def damaged_unit(name):
        unit = units[name]
        u = list(unit['factor_multiplier'])
        u[-1] = (u[-1]+1) % PRIME
        verify_unit(unit['factor'], unit['resultant'], u, unit['resultant_multiplier'], PRIME)

    def lost_factor_degree():
        changed = list(S5)
        changed[-1] *= PRIME
        finite_unit(changed, Rh, PRIME)

    def damaged_determinant_degree():
        damaged_bound = bound-1
        require(damaged_bound >= size*max(P5.degree(2), P7.degree(2)),
                'understated degree-bound damage')

    def damaged_cross():
        require(a*h-c*f == cross+1, 'damaged cross identity')

    def damaged_syzygy():
        gc = g.coefficients(0)
        q = variable(0)
        require(a*a*g-clear_quadratic(g, f) == f*(a*gc[2]*q+a*gc[1]+b*gc[2]),
                'damaged no-division necessity syzygy')

    probes = {
        'wrong_degree20_factor_coefficient': damaged_factor,
        'omit_x5_factor': lambda: factored_resultant(values, bound, S5, P20, s_power=0),
        'omit_S5_multiplicity': lambda: factored_resultant(values, bound, S5, P20, factor_power=1),
        'only_bound_evaluations': lambda: factored_resultant(values[:-1], bound, S5, P20),
        'understate_determinant_bound': damaged_determinant_degree,
        'wrong_affine_cross': damaged_cross,
        'wrong_clearing_syzygy_sign': damaged_syzygy,
        'wrong_S5_unit_coefficient': lambda: damaged_unit('S5_branch'),
        'wrong_P20_unit_coefficient': lambda: damaged_unit('P20_branch'),
        'factor_degree_lost_mod_prime': lost_factor_degree,
        'composite_interpolation_modulus': lambda: interpolate_finite([1, 2, 3], 255),
        'missing_singular_factor_branch': lambda: require({'P20_branch'} == set(units), 'incomplete branch cover')}
    for name, probe in probes.items():
        try:
            probe()
        except ValueError:
            damages.append(name)
        else:
            raise ValueError('mathematical damage survived '+name)
    all_polys = {**equations, 'h': h, 'P5': P5, 'P7': P7, 'bh': bh, 'bA': bA}
    metadata = {name: {'terms': len(poly.c), 'q_degree': poly.degree(0),
                      'r_degree': poly.degree(1), 'x_degree': poly.degree(2),
                      'whole_coefficients_sha256': hashlib.sha256(canonical(poly.encoded())).hexdigest()}
                for name, poly in all_polys.items()}
    record = {
        'actual_agent': 'six-sendov-2', 'role': 'researcher',
        'input9602': {'source_commit': INPUT_COMMIT, 'file_sha256': INPUT_FILES,
                     'whole_record_sha256': INPUT_RECORD, 'entire_typed_input_fixture_regenerated': True,
                     'nested9550_pins_and_entire_fixture_regenerated': True,
                     'same_author_reuse_not_independent_review': True},
        'ring': 'QQ[q,r,x]; REAL interpretation q=B/s, x=s²>0 in the s!=0 branch',
        'regenerated_necessary_equations': metadata, 'normalizations': normalizations,
        'quadratic_clear_primitive_contents': {'bh': str(ch), 'bA': str(cA)},
        'no_affine_slope_divided': True, 'both_zero_affine_slope_cases_retained': True,
        'characteristic_zero_resultant': {'fixed_r_degrees': [5, 7], 'Sylvester_size': size,
            'proved_x_degree_bound': bound, 'exact_distinct_rational_evaluations': len(values),
            'full_evaluations_sha256': hashlib.sha256(canonical(values)).hexdigest(),
            'nonzero_exact_content': str(content), 'certified_resultant_degree': degree,
            'x_multiplicity': 5, 'S5': S5, 'S5_multiplicity': 2, 'P20': P20,
            'whole_identity_established_by_degree_bound': True},
        'modular_resultants': {'S5_branch': rh_data, 'P20_branch': ra_data},
        'complete_modular_units': units, 'bridge_controls': controls(),
        'rejected_mathematical_damages': damages,
        'global_real_rank_at_least_two': True,
        'nonzero_scalar_common_root_unique_real_and_jointly_simple': True,
        'positive_scalar_criterion': ['T<0', 'SU-T²=0', 'alpha*T²-beta*T*S+S²=0'],
        'unique_positive_scalar': 't=-T/S; T<0 forces S>0 over REAL parameters',
        'feasibility_still_required': ['balanced norm-one normalization', 'eight DISTINCT REAL originals',
            'seven SIMPLE REAL h roots', 'STRICT p(lambda)>0', 'all five pencil equations', 't=p5>0'],
        'all_stationary_profiles_classified': False, 'uniform_global_slope_bound_proved': False,
        'complex_first_power_proved': False,
        'ordinary_unformalized_bridges': '9602 s0 complex rank exclusion and unit/Gram theorem, rank-one wedge necessity, legal real E/s/positive-factor cancellations, fixed Sylvester evaluation-vector necessity including degree loss, degree-bounded determinant identities, integer Gauss lemma with preserved factor degree, real scalar uniqueness and joint simplicity; no independent review claimed'}
    if export is not None:
        export.write_text(json.dumps({'variables': ['q', 'r', 'x'],
            'format': '[nonnegative integral exponent triple, exact rational coefficient]',
            'all_necessary_polynomials': {name: poly.encoded() for name, poly in all_polys.items()},
            'normalizations': normalizations, 'complete_record_sha256': hashlib.sha256(canonical(record)).hexdigest()},
            indent=2, sort_keys=True)+'\n')
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    record = certificate(args.export)
    if args.emit:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    else:
        require(same_typed(record, json.loads(args.expected.read_text())), 'ENTIRE typed expected record mismatch')
    print(json.dumps({'status': 'PASS', 'record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
        'global_real_rank_at_least_two': True, 'char0_identity_evaluations': 85,
        'modular_identity_evaluations': [record['modular_resultants'][name]['exact_distinct_evaluations']
                                       for name in ['S5_branch', 'P20_branch']],
        'complete_modular_units': len(record['complete_modular_units']),
        'bridge_controls': len(record['bridge_controls']),
        'rejected_mathematical_damages': len(record['rejected_mathematical_damages']),
        'entire_pinned9602_and9550_fixtures_regenerated': True}))


if __name__ == '__main__':
    main()
