#!/usr/bin/env python3
"""Independent exact 3+3+1+1 audit; no researcher-source imports.

Actual reviewer: six-reviewer-1. SymPy 1.14.0 builds a compressed operator
and a subresultant PRS. Fraction/integer code independently certifies the
resultant by degree-bounded point determinants, root counts, and signs.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path
import sys
import sympy as s


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def divrem(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], 'zero polynomial divisor')
    q = [F(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        j, c = len(a) - len(b), a[-1] / b[-1]
        q[j] += c
        for i, v in enumerate(b):
            a[i+j] -= c * v
        a = trim(a)
    return trim(q), a


def evaluate(p, x):
    a = 0
    for c in reversed(p):
        a = a*x + c
    return a


def sturm(p):
    def norm(a):
        return [x / abs(a[-1]) for x in a]
    a = norm(list(map(F, p)))
    b = norm([i*a[i] for i in range(1, len(a))])
    out = [a, b]
    while True:
        r = [-c for c in divrem(a, b)[1]]
        if r == [0]:
            return out
        r = norm(r)
        out.append(r)
        a, b = b, r


def variation(chain, x):
    v = [p[-1] if x is None else evaluate(p, x) for p in chain]
    signs = [1 if a > 0 else -1 for a in v if a]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def integer_det(a):
    """Literal integer Bareiss determinant, with exact-division guards."""
    a = [list(row) for row in a]
    previous, sign, n = 1, 1, len(a)
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = p*a[i][j] - a[i][k]*a[k][j]
                require(numerator % previous == 0, 'inexact determinant division')
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = p
    return sign*a[-1][-1]


def ia(a, b):
    return a[0]+b[0], a[1]+b[1]


def im(a, b):
    v = [x*y for x in a for y in b]
    return min(v), max(v)


def iq(a, b):
    require(b[0] > 0 or b[1] < 0, 'interval divisor contains zero')
    return im(a, (1/b[1], 1/b[0]))


def coarse(box, digits=9):
    unit = 10**digits
    return [str(F((box[0]*unit).__floor__(), unit)),
            str(F((box[1]*unit).__ceil__(), unit))]


def ascending(poly):
    return [F(str(v)) for v in reversed(poly.all_coeffs())]


def interval_univariate(poly, box):
    out = F(0), F(0)
    for c in poly.all_coeffs():
        c = F(str(c))
        out = ia(im(out, box), (c, c))
    return out


def interval_bivariate(poly, k, U, kb, ub):
    out = F(0), F(0)
    for c in s.Poly(poly.as_expr(), U).all_coeffs():
        out = ia(im(out, ub), interval_univariate(s.Poly(c, k), kb))
    return out


def homogeneous_remainder(poly, f, A, B, U, k):
    """A^degree poly(k,-B/A) modulo f, without an inverse or division."""
    degree = poly.degree(U)
    aa, bb = A.rem(f), (-B).rem(f)
    ap, bp = [s.Poly(1, k)], [s.Poly(1, k)]
    for _ in range(degree):
        ap.append((ap[-1]*aa).rem(f))
        bp.append((bp[-1]*bb).rem(f))
    out = s.Poly(0, k)
    pu = s.Poly(poly.as_expr(), U)
    for j in range(degree+1):
        out = (out+s.Poly(pu.nth(j), k)*bp[j]*ap[degree-j]).rem(f)
    return out


FACTORS = {
    4: [64, -4369, -30195, -49900, 250000],
    6: [1, 14, 1633, 9530, 19874, 11100, 3625],
    7: [64, 3241, -6416, -34966, 23828, 109985, 82500, 22500],
    16: [5038848, -12189970584, -207098915535, 16450339488516,
         -199286026683996, -1179788998549176, 40227992581570522,
         -175059981086037512, -1187369990398617128, -1528684269391186496,
         -1529810534666677091, -3713341102056530540, -7154447918441392100,
         -7346176678195664000, -3691662594253760000, -634889742720000000,
         52034400000000000],
}
RESULTANT_CONSTANT = 899679616715369403548229400563231388599310834535159790285851983872


def verify():
    require(s.__version__ == '1.14.0', 'requires SymPy 1.14.0')
    records = {}
    def check(name, condition, detail=True):
        require(condition, name)
        records[name] = detail
    c, x, y, k, U, V, z = s.symbols('c x y k U V z')
    m = [3, 3, 1, 1]
    levels = [c+x, c-x, -3*c+y, -3*c-y]
    G = s.diag(*[s.Rational(1, a) for a in m[:3]]) + s.ones(3)
    B = s.diag(*[levels[i]/m[i] for i in range(3)]) + levels[3]*s.ones(3)
    H = G.inv()*B
    v = s.Matrix([m[i]*levels[i] for i in range(3)])
    check('weighted selfadjointness', H.T*G == G*H)
    expected_h = z**3+4*c*z*z+(c*c-(x*x+3*y*y)/4)*z-6*c**3+3*c*(y*y-x*x)/4
    check('compressed characteristic', s.expand(H.charpoly(z).as_expr()-expected_h) == 0)
    powers = [s.eye(3), H]
    for _ in range(2, 5):
        powers.append(powers[-1]*H)
    traces = [s.expand(a.trace()) for a in powers]
    K = s.Matrix(3, 3, lambda i, j: traces[i+j])
    mu = s.Matrix([s.expand((v.T*G*powers[i]*v)[0]) for i in range(3)])
    D, E = s.expand(K.det()), s.expand((mu.T*K.adjugate()*mu)[0])
    N = 24*c*c+6*x*x+2*y*y
    S3 = c*(18*(x*x-y*y)-48*c*c)
    S4 = 168*c**4+36*c*c*x*x+108*c*c*y*y+6*x**4+2*y**4
    check('full coupling moments', (mu-s.Matrix([N, S3, S4-N*N/8])).applyfunc(s.expand) == s.zeros(3, 1))
    def squares(a):
        out = 0
        for exponents, coefficient in s.Poly(a, c, x, y).terms():
            require(all(e % 2 == 0 for e in exponents), 'odd square-reduction exponent')
            i, j, t = exponents
            out += coefficient*k**(i//2)*U**(j//2)*V**(t//2)
        return s.expand(out)
    Num = squares(s.expand(s.Rational(32, 3)*(N*N*D-E)))
    Den = squares(s.expand(s.Rational(32, 3)*mu[2]*D))
    M = 64*k*k+64*k*V+(U-V)**2
    Delta = 2304*k**3-32*k*k*U+6624*k*k*V-23*k*U*U+942*k*U*V-855*k*V*V+(U+3*V)**3
    check('full denominator identity', s.expand(Den-M*Delta) == 0)
    check('full discriminant identity', s.expand(16*squares(D)-Delta) == 0)
    check('full moment-gap identity', s.expand(2*squares(s.expand(mu[2]))-3*M) == 0)
    check('numerator support', len(s.Poly(Num, k, U, V).terms()) == 20, 20)
    records['complete numerator polynomial'] = [[list(e), str(a)] for e, a in sorted(s.Poly(Num, k, U, V).terms())]
    check('zero kappa-fifth coefficient', s.Poly(Num, k, U, V).coeff_monomial(k**5) == 0)
    boundary = 4*(3*U**3+67*U*U*V+177*U*V*V+9*V**3)
    check('full symmetric cancellation', s.expand(Num.subs(k, 0)-boundary*(U-V)**2) == 0)
    check('full symmetric square', s.expand(208*(U+3*V)**3-9*boundary-4*(U+3*V)*(5*U-21*V)**2) == 0)
    n, d = Num.subs(V, 1), Den.subs(V, 1)
    P, Q = s.expand(s.diff(n, k)*d-n*s.diff(d, k)), s.expand(s.diff(n, U)*d-n*s.diff(d, U))
    p, q = s.Poly(P, U, k).primitive()[1], s.Poly(Q, U, k).primitive()[1]
    check('gradient bidegrees', (p.degree(U), p.degree(k), q.degree(U), q.degree(k)) == (9, 8, 8, 9), [9, 8, 8, 9])
    seq = s.subresultants(s.Poly(p.as_expr(), U, domain=s.QQ.poly_ring(k)),
                          s.Poly(q.as_expr(), U, domain=s.QQ.poly_ring(k)))
    check('complete PRS degrees', [a.degree() for a in seq] == list(range(9, -1, -1)), list(range(9, -1, -1)))
    fs = {j: s.Poly(sum(a*k**i for i, a in enumerate(v)), k) for j, v in FACTORS.items()}
    R = s.Poly(seq[-1].as_expr(), k)
    product = RESULTANT_CONSTANT*k**7*(16*k-1)**14*(125*k+81)**5
    for f in fs.values():
        product *= f.as_expr()
    check('full resultant factorization', R == s.Poly(product, k))
    check('resultant degree', R.degree() == 59, 59)
    integers = [int(a) for a in reversed(R.all_coeffs())]
    records['resultant_coefficient_sha256'] = hashlib.sha256(json.dumps(integers, separators=(',', ':')).encode()).hexdigest()
    # Each determinant term selects eight p rows and nine q rows.
    bound = 8*p.degree(k)+9*q.degree(k)
    pc, qc = [s.Poly(a, k) for a in s.Poly(p.as_expr(), U).all_coeffs()], [s.Poly(a, k) for a in s.Poly(q.as_expr(), U).all_coeffs()]
    for value in range(bound+1):
        pv, qv = [int(a.eval(value)) for a in pc], [int(a.eval(value)) for a in qc]
        matrix = [[0]*i+pv+[0]*(7-i) for i in range(8)]
        matrix += [[0]*i+qv+[0]*(8-i) for i in range(9)]
        require(integer_det(matrix) == evaluate(integers, value), 'independent point determinant mismatch')
    records['independent resultant degree bound and nodes'] = [bound, bound+1]
    L = s.Poly(seq[-2].as_expr(), U)
    A, B0 = s.Poly(L.nth(1), k), s.Poly(L.nth(0), k)
    check('linear PRS coefficient degrees', [A.degree(), B0.degree()] == [48, 49], [48, 49])
    # Verify actual polynomial pseudo-remainder identities and that all
    # multipliers remain nonzero at every relevant parameter root.
    gamma_degrees = []
    for a, b, next_poly in zip(seq, seq[1:], seq[2:-1]):
        quotient, remainder = a.pdiv(b)
        gamma, rem = s.div(s.Poly(remainder.LC(), k), s.Poly(next_poly.LC(), k))
        require(rem.is_zero, 'nonpolynomial PRS multiplier')
        require(remainder == next_poly.mul_ground(gamma.as_expr()), 'full PRS remainder identity')
        require(a.mul_ground(b.LC()**(a.degree()-b.degree()+1))-quotient*b == remainder, 'full pseudo-division identity')
        require(all(s.gcd(gamma, fs[j]).degree() == 0 for j in [4, 16]), 'exceptional PRS multiplier')
        gamma_degrees.append(gamma.degree())
    check('specialization-safe linear propagation', len(gamma_degrees) == 7, gamma_degrees)
    check('exceptional kappa1/16 gcd', s.gcd(p.as_expr().subs(k, s.Rational(1, 16)), q.as_expr().subs(k, s.Rational(1, 16))) == U**2)
    check('degree-six positivity', all(a > 0 for a in FACTORS[6]))
    for degree in [4, 7, 16]:
        chain = sturm(FACTORS[degree]); counts = [variation(chain, F(0)), variation(chain, None)]
        check('degree-'+str(degree)+' complete positive count', counts[0]-counts[1] == (0 if degree == 7 else 2), counts)
    collision = s.Poly((U-1-16*k)**2-64*k, U, k)
    H00, H01, H11 = s.Poly(s.diff(P, k), U, k), s.Poly(s.diff(P, U), U, k), s.Poly(s.diff(Q, U), U, k)
    HD = s.Poly(s.expand(H00.as_expr()*H11.as_expr()-H01.as_expr()**2), U, k)
    check('stationary Hessian symmetry identity', s.expand(d*(s.diff(P, U)-s.diff(Q, k))-2*(P*s.diff(d, U)-Q*s.diff(d, k))) == 0)
    for degree in [4, 16]:
        f = fs[degree]
        check('degree-'+str(degree)+' nonzero lift coefficient', s.gcd(A, f).degree() == 0)
        for name, poly in [('first', p), ('second', q)]:
            check('degree-'+str(degree)+' '+name+' equation existence', homogeneous_remainder(poly, f, A, B0, U, k).is_zero)
        cr = homogeneous_remainder(collision, f, A, B0, U, k)
        check('degree-'+str(degree)+' collision status', cr.is_zero if degree == 4 else s.gcd(cr, f).degree() == 0)
    for i, item in enumerate(ROOT_BOXES, 1):
        degree, endpoints, kind, hsign = item
        kb = tuple(map(F, endpoints)); chain = sturm(FACTORS[degree])
        check('root'+str(i)+' positive isolation', 0 < kb[0] < kb[1] and variation(chain, kb[0])-variation(chain, kb[1]) == 1)
        ub = iq(interval_univariate(-B0, kb), interval_univariate(A, kb))
        require(ub[0] > 0, 'nonpositive lift')
        nb = interval_bivariate(s.Poly(n, U, k), k, U, kb, ub)
        db = interval_bivariate(s.Poly(d, U, k), k, U, kb, ub)
        require(db[0] > 0, 'nonpositive shape denominator')
        value = iq(nb, db)
        a = interval_bivariate(H00, k, U, kb, ub)
        det = interval_bivariate(HD, k, U, kb, ub)
        require(a[1] < 0 if hsign == '-' else a[0] > 0, 'uncertified Hessian diagonal sign')
        require(det[0] > 0 if kind == 'maximum' else det[1] < 0, 'uncertified Hessian determinant sign')
        lo, hi = [(F('24.53389668'), F('24.53389670')), (F(4), F(5)), (F(23), F(24)), (F(7), F(8))][i-1]
        require(lo < value[0] < value[1] < hi, 'candidate value separation')
        records['root'+str(i)+' complete certified classification'] = {'factor_degree': degree, 'kappa': list(endpoints), 'U': coarse(ub), 'C': coarse(value), 'H00': coarse(a), 'Hdet': coarse(det), 'type': kind}
    for shape, expected in [((1, 300, 100), F(3504016400, 147654727)), ((121, 19321, 9025), F(27899524, 1137183))]:
        sub = dict(zip([k, U, V], shape))
        check('exact benchmark '+str(shape), F(str(Num.subs(sub)/Den.subs(sub))) == expected, str(expected))
    damage = 0
    damaged = [integer_det([[1, 2], [3, 4]]) == -1,
               evaluate(integers, 2)+1 == integer_det([[0]*i+[int(a.eval(2)) for a in pc]+[0]*(7-i) for i in range(8)]+[[0]*i+[int(a.eval(2)) for a in qc]+[0]*(8-i) for i in range(9)]),
               variation(sturm(FACTORS[16]), F(0))-variation(sturm(FACTORS[16]), None) == 1,
               homogeneous_remainder(s.Poly(p.as_expr()+1, U, k), fs[16], A, B0, U, k).is_zero]
    for condition in damaged:
        try:
            require(condition, 'damaged mathematical certificate')
        except ValueError:
            damage += 1
    require(damage == 4, 'damage controls did not reject')
    return {'records': records, 'checks': len(records), 'damage_controls': damage}


ROOT_BOXES = [[4, ['92228127418236937168863643500616508997180921184/6890447324558341533386195119259971085954099645365', '1394457695866250428055030633013666193969161245/104181203377565797913885768395016591629956845236'], 'maximum', '-'], [4, ['316207479269554762061162016207399485102969556267/625933720911546824897414953941675776572378161541', '95652817183649645161901279367859901093579381410/189345058863692800509813901426568722814779960827'], 'saddle', '+'], [16, ['146048144766244336916666683851628416464649049/355704006781755806386537375004666201962478374197', '173363828428785065383817886909701121454654157/422232055750128473925556347512635326504616274672'], 'saddle', '-'], [16, ['12907241754998094811020557594232524651645496602464/762948537992145132717019400798239828927387522547', '2260981124338690449689692011507495227483141757051/133646853137624136124042356505565339053367957114'], 'maximum', '-']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = verify()
    result['record_sha256'] = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if args.emit:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        fixture = args.expected or Path(__file__).with_name('expected.json')
        require(json.loads(fixture.read_text()) == result, 'complete fixture mismatch')
        print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print('verification failed: '+str(error), file=sys.stderr)
        sys.exit(1)
