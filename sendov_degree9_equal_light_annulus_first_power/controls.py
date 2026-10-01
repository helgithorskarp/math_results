"""Exact definition-level and full-reference controls; no sampled sign proof.

Actual author six-sendov-1, researcher. The universal signs are separately
checked in certificate.py. Gaussian arithmetic here uses scalar Fractions,
not the symbolic complex helpers in kernel.py.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib, json
import algebra as A
import certificate as C
import kernel as K


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'),
                                     sort_keys=True).encode()).hexdigest()


def ga(p, q):
    return p[0]+q[0], p[1]+q[1]


def gm(p, q):
    return p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*q[0]


def gs(p, value):
    return p[0]*value, p[1]*value


def gp(p, n):
    value = F(1), F(0)
    for _ in range(n):
        value = gm(value, p)
    return value


def gn(p):
    return p[0]*p[0]+p[1]*p[1]


def direct_integral(b, heavy, s, t, k):
    """Integrate heavy^6 times the entire light quadratic coefficientwise."""
    qnum, denominator = (F(1), k), 1+k*k
    light = [(F(1), F(0)), gs(qnum, -2*b*t),
             gs(gp(qnum, 2), b*b*s*s/denominator)]
    total = F(0), F(0)
    for j in range(7):
        h = gs(gp(heavy, j), (-1)**j*comb(6, j)*b**j)
        for ell, coefficient in enumerate(light):
            total = ga(total, gs(gm(h, coefficient), F(9, j+ell+1)))
    return total


def definition_controls(data):
    evaluate = {key: [A.compile_evaluator(p) for p in data[key]]
                for key in ('E', 'O', 'G')}
    records, physical = [], 0
    for b, r, phase, ratio, k in product(
            [F(0), F(1, 20), F(1, 2), F(7, 8), F(9, 10), F(1)],
            [F(1), F(501, 500), F(7, 6)],
            [F(-1, 2), F(0), F(1, 16)],
            [F(1), F(9, 10)], [F(-4, 3), F(0), F(1, 3)]):
        s = 4-3*r
        x, y = r*(1-phase*phase)/(1+phase*phase), 2*r*phase/(1+phase*phase)
        t, point = s*ratio, [b, r, x, s*ratio]
        kap, den = k*k, 1+k*k
        even = sum(e(point)*kap**j for j, e in enumerate(evaluate['E']))
        skew = sum(e(point)*kap**j for j, e in enumerate(evaluate['O']))
        norms = []
        for sign in (-1, 1):
            actual = gn(direct_integral(b, (x, y), s, t, sign*k))*den*den-r**12*s**4*den*den
            K.require(actual == even+sign*y*k*skew, 'Direct integral/signed norm differs')
            norms.append(actual)
        gram = sum(e(point)*kap**j for j, e in enumerate(evaluate['G']))
        K.require(gram == norms[0]*norms[1], 'Direct signed norm product/Gram differs')
        if 0 < t <= s and kap <= s*s/(t*t)-1:
            physical += 1
        records.append([list(map(str, point)), str(k), str(norms[0]), str(norms[1]), str(gram)])
    # Audit the integer point evaluator against literal Fraction evaluation.
    comparisons = 0
    for point in ([F(0), F(1), F(1), F(1)],
                  [F(7, 8), F(33, 32), F(7, 8), F(3, 4)],
                  [F(1), F(2, 3), F(1, 3), F(2)]):
        for key in ('E', 'O', 'G'):
            for p, evaluate_p in zip(data[key], evaluate[key]):
                K.require(evaluate_p(point) == A.evaluate(p, point), 'Integer/Fraction evaluation differs')
                comparisons += 1
    return {'points': len(records), 'signed_norms': 2*len(records),
            'physical_angular_interval_points': physical,
            'integer_fraction_evaluation_comparisons': comparisons,
            'sha256': digest(records)}


def angular_controls(data):
    """Check complete coefficient dictionaries of both inverse angular bases."""
    t = A.variable(3)
    deficit = A.add(A.power(data['s'], 2), A.scale(A.power(t, 2), -1))
    profiles = []
    for name in ('E', 'G'):
        coefficients = data[name]
        degree = len(coefficients)-1
        controls = [A.mul(coefficients[0], A.power(t, 2*degree))]
        for index in range(1, degree+1):
            key = name+str(index)
            p, removed = K.angular_control(data, key)
            controls.append(A.mul(p, A.power(t, 2*degree-2*index+removed[3])))
            profiles.append({'key': key, 'terms': len(p),
                'degrees': list(map(max, zip(*p))), 'factored_powers': list(removed),
                'sha256': K.digest([p])})
        for j in range(degree+1):
            reconstructed = A.add(*[A.scale(controls[i],
                (-1)**(j-i)*comb(j, i)*comb(degree, j)) for i in range(j+1)])
            original = A.mul(A.mul(coefficients[j], A.power(t, 2*degree-2*j)), A.power(deficit, j))
            K.require(reconstructed == original, 'Whole angular Bernstein inverse differs')
    return {'profiles': profiles, 'full_inverse_identities': 11}


def cube_points():
    # All sixteen vertices plus two strictly interior points.
    return list(product((F(0), F(1)), repeat=4))+[
        (F(1, 2), F(1, 3), F(2, 5), F(4, 7)),
        (F(3, 4), F(2, 3), F(4, 5), F(1, 5))]


def map_point(point, chart):
    u, y, v, w = point
    b = (7+u)/8
    if chart == 'nearer':
        r = 1+b*y/(3*(1+b))
    elif chart == 'farther':
        r = 1-b*y/(1+b)
    else:
        raise ValueError('Unknown chart')
    eps, s = 1-b, 4-3*r
    x, t = r-F(4, 3)*eps*v, s-4*eps*(1-v)*w
    K.require(3*r+s == 4 and min(r, s) >= 1/(1+b), 'Radius map/floors failed')
    K.require(F(1, 32) <= t <= s and r*r-x*x >= 0, 'Positive-t/Y-square cube bounds failed')
    K.require(3*x+t >= 4*b, 'Actual-mean cube budget failed')
    if b == 1:
        K.require(x == r and t == s, 'Endpoint saturation failed')
    else:
        vv = 3*(r-x)/(4*eps)
        K.require(vv == v, 'Inverse phase-loss map failed')
        if vv != 1:
            K.require((s-t)/(4*eps*(1-vv)) == w, 'Inverse light-loss map failed')
        else:
            K.require(t == s, 'Zero light-loss budget failed')
        yy = (3*(1+b)*(r-1)/b if chart == 'nearer' else (1+b)*(1-r)/b)
        K.require(yy == y, 'Inverse radius map failed')
    return b, r, x, t


def cube_controls(data, raw, removed, mapped, factor, radius_degree, key, chart):
    raw_e, mapped_e = A.compile_evaluator(raw), A.compile_evaluator(mapped)
    family, index = key[0], int(key[1:])
    coefficients = [A.compile_evaluator(p) for p in data[family]]
    n, records = len(coefficients)-1, []
    for point in cube_points():
        original = map_point(point, chart)
        b, r, x, t = original
        s, deficit = 4-3*r, (4-3*r)**2-t*t
        value = raw_e(original)
        K.require(factor > 0, 'Nonpositive homogeneous scale')
        K.require(mapped_e(point)/factor == (1+b)**radius_degree*value,
                  'Original/cleared cube composition differs')
        # Scalar angular basis controls, retaining every cleared t power.
        angular = sum(F(comb(index, j), comb(n, j))*coefficients[j](original)
            *t**(2*n-2*j)*deficit**j for j in range(index+1))
        K.require(angular == t**(2*n-2*index+removed[3])*value,
                  'Scalar angular control/removed monomial differs')
        records.append([list(map(str, point)), list(map(str, original)), str(value), str(angular)])
    return {'points': len(records), 'all_cube_vertices': 16}


def reference_regression(data):
    """Compare every E1-nearer monomial and every tensor entry to Fraction maps."""
    raw, removed = K.angular_control(data, 'E1')
    mapped, factor, radius_degree = C.cube(raw, 'nearer')
    b, r, v, w = [A.variable(j) for j in range(4)]
    eps, den = A.add(A.ONE, A.scale(b, -1)), A.add(A.ONE, b)
    s = A.add(A.scale(A.ONE, 4), A.scale(r, -3))
    reference = K.substitute(A, raw, 2, A.add(r, A.scale(A.mul(eps, v), F(-4, 3))))
    reference = K.substitute(A, reference, 3,
        A.add(s, A.scale(A.mul(eps, A.mul(A.add(A.ONE, A.scale(v, -1)), w)), -4)))
    reference, degree = K.horner(A, reference, 1,
        A.add(den, A.scale(A.mul(b, r), F(1, 3))), den)
    reference = C.affine_cell_integer(reference, 0, F(7, 8), F(1))
    K.require(radius_degree == degree and {e: F(v)/factor for e, v in mapped.items()} == reference,
              'Whole integer/Fraction mapped polynomial differs')
    values, tensor_den, degrees = C.bernstein(mapped)
    C.inverse_identity(values, tensor_den, degrees, mapped)
    rvalues, rden, rdegrees = C.bernstein(reference)
    K.require(degrees == rdegrees and [F(v, tensor_den)/factor for v in values]
              == [F(v, rden) for v in rvalues], 'Whole integer/Fraction tensor differs')
    positive_index = next(i for i, v in enumerate(values) if v > 0)
    damaged = values.copy()
    damaged[positive_index] += 1
    try:
        C.inverse_identity(damaged, tensor_den, degrees, mapped)
    except ArithmeticError:
        pass
    else:
        raise ArithmeticError('Damaged positive tensor entry was accepted')
    return {'key': 'E1', 'chart': 'nearer', 'terms_compared': len(mapped),
            'coefficients_compared': len(values), 'scaled_reference_hash': K.digest([reference]),
            'damaged_positive_tensor_rejected': True}


def normalization_controls():
    """Communication from an independently integrated monic p with p(a)=0.

    These algebraic examples do not assert disk-root containment. The
    communication identity holds without it, for arbitrary positive m.
    """
    rho = F(9, 10)
    heavy = F(3), F(4)
    phase = F(5, 13), F(12, 13)
    lights = [gm(phase, (F(3, 5), sign*F(4, 5))) for sign in (-1, 1)]
    reciprocals = [heavy]*6+lights
    critical = [(rho-g[0]/gn(g), g[1]/gn(g)) for g in reciprocals]
    # p'(z)=9 product(z-zeta), constant chosen to make rho a root.
    derivative = [(F(9), F(0))]
    for zeta in critical:
        new = [(F(0), F(0))]*(len(derivative)+1)
        for j, coefficient in enumerate(derivative):
            new[j] = ga(new[j], gm(coefficient, gs(zeta, -1)))
            new[j+1] = ga(new[j+1], coefficient)
        derivative = new
    p0 = gs(tuple(sum(derivative[j][i]*rho**(j+1)/(j+1)
                       for j in range(9)) for i in range(2)), -1)
    records = []
    # Test the true reciprocal mean m=4 and an independent algebraic scale.
    for m in (F(4), F(1, 2)):
        b, r, s = m*rho, F(5)/m, F(1)/m
        heavy_m = gs(heavy, 1/m)
        k, c = F(12, 5), F(3, 5)
        t = s*c*F(5, 13)
        integral = direct_integral(b, heavy_m, s, t, k)
        ratio = gn(integral)/(r**12*s**4)
        expected = m**16*gn(p0)/(rho*rho)
        K.require(ratio == expected, 'Actual polynomial communication scale is not m^16')
        K.require(ratio != m**18*gn(p0)/(rho*rho), 'Scale test failed to distinguish m^18')
        records.append([str(m), list(map(str, p0)), str(ratio)])
    K.require(F(46643, 50000)*F(43750, 46643) == F(7, 8), 'Annulus cutoff product differs')
    # An antipodal light sum has t=0 and fails the necessary mean budget.
    for b in (F(7, 8), F(1)):
        maximal_r = (4-1/(1+b))/3
        K.require(4*b-3*maximal_r >= F(1, 32), 'Antipodal exclusion bound failed')
    return {'communication_examples': len(records), 'scale_exponent': 16,
            'antipodal_budget_rejections': 2, 'cutoff_product': '7/8', 'sha256': digest(records)}
