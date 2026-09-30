#!/usr/bin/env python3
"""Exact degree-nine local/global separation certificate.

Actual author six-sendov-3, researcher. Standard-library CPython3.11.
Full rational commutant projection and original residual-cubic recursion
are different algebraic routes from the earlier contour coefficients.
They are author checks, not independent review. Original-root recursion
retains credit to the local audit; commutant pinching retains credit to
angular/displacement sources. Analytic IFT and local strictness are written
mathematics. No campaign import, sampled eigenvalue or external solver.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb, factorial, isqrt
from pathlib import Path
import json
import sys

RECORDS = []
CONTROLS = []


def encode(value):
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, Quadratic):
        return {'rational': encode(value.a), 'radical': encode(value.b)}
    if isinstance(value, Complex):
        return {'re': encode(value.re), 'im': encode(value.im)}
    if isinstance(value, Polynomial):
        return encode(value.c)
    if isinstance(value, Jet):
        return encode(value.c)
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


def record(name, value, kind='coefficient'):
    RECORDS.append({'name': name, 'kind': kind, 'value': encode(value)})


def check(name, actual, expected):
    if actual != expected:
        raise RuntimeError('exact identity failed: ' + name)
    record(name, actual, 'identity')


def positive(name, value):
    if value <= 0:
        raise RuntimeError('strict positive sign failed: ' + name)
    record(name, value, 'positive')


def negative(name, value):
    if value >= 0:
        raise RuntimeError('strict negative sign failed: ' + name)
    record(name, value, 'negative')


def reject(name, actual, corrupted):
    if actual == corrupted:
        raise RuntimeError('corruption control failed: ' + name)
    CONTROLS.append(name)


class Polynomial:
    """Untruncated univariate Q[q], ascending coefficients."""
    def __init__(self, value=0):
        data = list(value.c) if isinstance(value, Polynomial) else list(value) if isinstance(value, (tuple, list)) else [Q(value)]
        self.c = [Q(x) for x in data]
        while len(self.c) > 1 and self.c[-1] == 0:
            self.c.pop()

    def __add__(self, other):
        other = Polynomial(other)
        return Polynomial([self.at(i) + other.at(i) for i in range(max(len(self.c), len(other.c)))])
    __radd__ = __add__

    def __neg__(self):
        return Polynomial([-x for x in self.c])

    def __sub__(self, other):
        return self + -Polynomial(other)

    def __rsub__(self, other):
        return Polynomial(other) + -self

    def __mul__(self, other):
        other = Polynomial(other)
        out = [Q(0)] * (len(self.c) + len(other.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                out[i+j] += a*b
        return Polynomial(out)
    __rmul__ = __mul__

    def __truediv__(self, rational):
        return Polynomial([x/Q(rational) for x in self.c])

    def __pow__(self, power):
        if type(power) is not int or power < 0:
            raise ValueError('nonnegative polynomial power required')
        out = Polynomial(1)
        for _ in range(power):
            out *= self
        return out

    def __eq__(self, other):
        return self.c == Polynomial(other).c

    def at(self, i):
        return self.c[i] if i < len(self.c) else Q(0)

    def evaluate(self, value):
        out = Q(0)
        for c in reversed(self.c):
            out = out*value+c
        return out


def profile(q):
    theta = [Q(7)] + [Q(-1)+4*q]*3 + [Q(-1)-3*q]*4
    mu2, mu3, mu4 = [sum(x**k for x in theta) for k in (2,3,4)]
    tr = 5+q
    gap = 49-14*q+7*q*q
    X = mu4/mu2**2
    eta = (1+(2*mu3-tr*mu2)**2/(gap*mu2**2))/2
    return theta, mu2, mu3, mu4, X, eta


def matrix_product(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def frobenius(a, b):
    return sum((x*y for rowa, rowb in zip(a,b) for x,y in zip(rowa,rowb)), Q(0))


def difference(a, b):
    return [[x-y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]


def nullspace(a, columns):
    """Exact rational RREF with free-coordinate basis, no eigenvalue input."""
    a = [list(row) for row in a]
    pivots = []
    row = 0
    for column in range(columns):
        pivot = next((i for i in range(row,len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row],a[pivot] = a[pivot],a[row]
        scale = a[row][column]
        a[row] = [x/scale for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][column]:
                scale = a[i][column]
                a[i] = [x-scale*y for x,y in zip(a[i],a[row])]
        pivots.append(column)
        row += 1
        if row == len(a):
            break
    basis = []
    for free in sorted(set(range(columns))-set(pivots)):
        v = [Q(0)]*columns
        v[free] = 1
        for j,pivot in enumerate(pivots):
            v[pivot] = -a[j][free]
        basis.append(v)
    return basis


def solve(a, b):
    n = len(b)
    a = [list(row)+[x] for row,x in zip(a,b)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if a[i][j]), None)
        if pivot is None:
            raise RuntimeError('singular Gram system')
        a[j],a[pivot] = a[pivot],a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                scale = a[i][j]
                a[i] = [x-scale*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]


def commutant_concentration(theta):
    n = 8
    P = [[Q(i==j)-Q(1,n) for j in range(n)] for i in range(n)]
    D = [[theta[i] if i==j else Q(0) for j in range(n)] for i in range(n)]
    C = matrix_product(matrix_product(P,D),P)
    W = [[theta[i]*theta[j]/8 for j in range(n)] for i in range(n)]
    CW,WC = matrix_product(C,W),matrix_product(W,C)
    if CW == WC:
        return frobenius(W,W), W, 0
    pairs = list(combinations_with_replacement(range(n),2))
    matrices = []
    for i,j in pairs:
        B = [[Q(0)]*n for _ in range(n)]
        B[i][j] = B[j][i] = Q(1)
        matrices.append(B)
    commutators = [difference(matrix_product(C,B),matrix_product(B,C)) for B in matrices]
    equations = [[commutators[k][i][j] for k in range(len(pairs))]
                 for i in range(n) for j in range(i+1,n)]
    basis_vectors = nullspace(equations,len(pairs))
    bases = [[[sum((v[k]*matrices[k][i][j] for k in range(len(pairs))),Q(0))
               for j in range(n)] for i in range(n)] for v in basis_vectors]
    gram = [[frobenius(B,Z) for Z in bases] for B in bases]
    coefficients = solve(gram,[frobenius(W,B) for B in bases])
    T = [[sum((c*B[i][j] for c,B in zip(coefficients,bases)),Q(0))
          for j in range(n)] for i in range(n)]
    if matrix_product(C,T) != matrix_product(T,C):
        raise RuntimeError('computed projection does not commute')
    for B in bases:
        if frobenius(difference(W,T),B):
            raise RuntimeError('projection residual not orthogonal')
    if any(sum(equation[k]*v[k] for k in range(len(pairs))) for equation in equations for v in basis_vectors):
        raise RuntimeError('invalid complete commutant kernel')
    return frobenius(T,T), T, len(bases)


RADICAND = 1256647
ORDER = 5


@dataclass(frozen=True)
class Quadratic:
    a: object = 0
    b: object = 0

    def __post_init__(self):
        object.__setattr__(self,'a',Q(self.a))
        object.__setattr__(self,'b',Q(self.b))

    def __add__(self, other):
        other = quadratic(other)
        return Quadratic(self.a+other.a,self.b+other.b)
    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a,-self.b)

    def __sub__(self, other):
        return self + -quadratic(other)

    def __rsub__(self, other):
        return quadratic(other) + -self

    def __mul__(self, other):
        other = quadratic(other)
        return Quadratic(self.a*other.a+RADICAND*self.b*other.b,
                         self.a*other.b+self.b*other.a)
    __rmul__ = __mul__

    def __truediv__(self, other):
        other = quadratic(other)
        denominator = other.a**2-RADICAND*other.b**2
        if not denominator:
            raise ZeroDivisionError('zero quadratic element')
        return self*Quadratic(other.a/denominator,-other.b/denominator)

    def __pow__(self, power):
        if type(power) is not int or power < 0:
            raise ValueError('nonnegative quadratic power required')
        out = Quadratic(1)
        for _ in range(power):
            out *= self
        return out

    def __bool__(self):
        return bool(self.a or self.b)

    def rational(self):
        if self.b:
            raise RuntimeError('uncancelled radical')
        return self.a


def quadratic(value):
    return value if isinstance(value,Quadratic) else Quadratic(value)


@dataclass(frozen=True)
class Complex:
    re: object = 0
    im: object = 0

    def __post_init__(self):
        object.__setattr__(self,'re',quadratic(self.re))
        object.__setattr__(self,'im',quadratic(self.im))

    def __add__(self, other):
        other = complex_value(other)
        return Complex(self.re+other.re,self.im+other.im)
    __radd__ = __add__

    def __neg__(self):
        return Complex(-self.re,-self.im)

    def __sub__(self, other):
        return self + -complex_value(other)

    def __rsub__(self, other):
        return complex_value(other) + -self

    def __mul__(self, other):
        other = complex_value(other)
        return Complex(self.re*other.re-self.im*other.im,
                       self.re*other.im+self.im*other.re)
    __rmul__ = __mul__

    def __truediv__(self, other):
        other = complex_value(other)
        den = other.re**2+other.im**2
        return Complex((self.re*other.re+self.im*other.im)/den,
                       (self.im*other.re-self.re*other.im)/den)

    def conjugate(self):
        return Complex(self.re,-self.im)

    def rational(self):
        if self.im:
            raise RuntimeError('uncancelled imaginary part')
        return self.re.rational()


def complex_value(value):
    return value if isinstance(value,Complex) else Complex(value)


class Jet:
    """Exact Q(sqrt1256647)[i][s]/(s^6), ascending coefficients."""
    def __init__(self,value=0):
        data = list(value.c) if isinstance(value,Jet) else list(value) if isinstance(value,(list,tuple)) else [value]
        self.c = [complex_value(x) for x in data[:ORDER+1]]
        self.c.extend(Complex() for _ in range(ORDER+1-len(self.c)))

    def __add__(self, other):
        other = Jet(other)
        return Jet([x+y for x,y in zip(self.c,other.c)])
    __radd__ = __add__

    def __neg__(self):
        return Jet([-x for x in self.c])

    def __sub__(self, other):
        return self + -Jet(other)

    def __rsub__(self, other):
        return Jet(other) + -self

    def __mul__(self, other):
        other = Jet(other)
        return Jet([sum((self.c[j]*other.c[k-j] for j in range(k+1)),Complex())
                    for k in range(ORDER+1)])
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other,Jet):
            return self*other.inverse()
        return Jet([x/other for x in self.c])

    def __pow__(self, power):
        if type(power) is not int or power<0:
            raise ValueError('nonnegative jet power required')
        out = Jet(1)
        for _ in range(power):
            out *= self
        return out

    def __eq__(self, other):
        return self.c == Jet(other).c

    def inverse(self):
        out = [Complex(1)/self.c[0]]
        for k in range(1,ORDER+1):
            out.append(-sum((self.c[j]*out[k-j] for j in range(1,k+1)),Complex())/self.c[0])
        return Jet(out)

    def conjugate(self):
        return Jet([x.conjugate() for x in self.c])

    def modulus(self):
        norm = self*self.conjugate()
        constant = self.c[0].rational()
        if constant<=0:
            raise RuntimeError('positive constant modulus required')
        out = [Complex(constant)]
        for k in range(1,ORDER+1):
            out.append((norm.c[k]-sum((out[j]*out[k-j] for j in range(1,k)),Complex()))/(2*constant))
        return Jet(out)


def exp_i(theta):
    out = [];term = Complex(1)
    for j in range(ORDER+1):
        out.append(term/factorial(j))
        term *= Complex(0,theta)
    return Jet(out)


def poly_product(a,b):
    out = [Jet() for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out


def poly_evaluate(coefficients,x):
    out = Jet()
    for c in reversed(coefficients):
        out = out*x+c
    return out


def original_residual(a,roots,masses):
    """p' divided by the five original repeated factors, in physical z."""
    factors = [[-root,Jet(1)] for root in roots]
    D = poly_product(poly_product(factors[0],factors[1]),factors[2])
    for i,m in enumerate(masses):
        term = [Jet(1)]
        for j,factor in enumerate(factors):
            if j!=i:
                term = poly_product(term,factor)
        term = poly_product([Jet(-a),Jet(1)],term)
        D = [x+m*y for x,y in zip(D,term)]
    value = poly_evaluate(D,Jet(a))
    C = [Jet() for _ in range(4)]
    for k,coefficient in enumerate(D):
        for j in range(k+1):
            C[3-j] += coefficient*(comb(k,j)*a**(k-j)*(-1)**j)
    return [x/value for x in C]


def coefficient_characteristic(us,masses):
    factors = [[-u,Jet(1)] for u in us]
    product = poly_product(poly_product(factors[0],factors[1]),factors[2])
    C = [9*x for x in product]
    for i,m in enumerate(masses):
        term = [Jet(1)]
        for j,factor in enumerate(factors):
            if j!=i:
                term = poly_product(term,factor)
        term = poly_product([Jet(),Jet(1)],term)
        C = [x-m*y for x,y in zip(C,term)]
    return C


def direct_cubic(a):
    slopes = [Q(7),Q(-41,40),Q(-157,160)]
    masses = [1,3,4]
    roots = [-exp_i(theta) for theta in slopes]
    us = [(Jet(a)-root).inverse() for root in roots]
    C = original_residual(a,roots,masses)
    label = 'direct original cubic a='+str(a)
    check(label+' reciprocal-characteristic identity',C,coefficient_characteristic(us,masses))
    check(label+' monic coefficient',C[3],Jet(1))
    derivative = [k*C[k] for k in range(1,4)]
    v = Q(1)/(1+a)
    lambdas = [Quadratic(Q(799,320),Q(sign,320)) for sign in [-1,1]]
    near = []
    for j,lam in enumerate(lambdas):
        root = Jet([v,Complex(0,-v*v*lam)])
        check(label+' near tangent '+str(j),poly_evaluate(C,root).c[2],Complex())
        linear = poly_evaluate(derivative,root).c[1]
        if not (linear.re or linear.im):
            raise RuntimeError('divided near derivative vanished')
        for k in range(2,5):
            root.c[k] = -poly_evaluate(C,root).c[k+1]/linear
        check(label+' complete near residual '+str(j),poly_evaluate(C,root),Jet())
        near.append(root)
    far = Jet(9*v)
    linear = poly_evaluate(derivative,far).c[0]
    check(label+' far implicit derivative',linear,Complex(64*v*v))
    for k in range(1,5):
        far.c[k] = -poly_evaluate(C,far).c[k]/linear
    check(label+' complete far residual through fourth order',poly_evaluate(C,far).c[:5],[Complex()]*5)
    F = 2*us[1].modulus()+3*us[2].modulus()+near[0].modulus()+near[1].modulus()+far.modulus()
    E = sum((m*(u-v)*(u-v).conjugate() for m,u in zip(masses,us)),Jet())
    mu2 = sum(m*t*t for m,t in zip(masses,slopes))
    check(label+' exact leading energy',E.c[2],Complex(v**4*mu2))
    check(label+' collapsed objective',F.c[0],Complex(16*v))
    kappa = (1+a)*(a-Q(5,8))
    check(label+' quadratic objective',F.c[2],E.c[2]*kappa)
    check(label+' objective odd coefficients through cubic',[F.c[1],F.c[3]],[Complex(),Complex()])
    Kdirect = -(F.c[4]-E.c[4]*kappa)/(E.c[2]*E.c[2])
    expected = coefficient_K(a,Q(-1,160))
    check(label+' true fixed-energy quartic',Kdirect,Complex(expected))
    record(label+' complete fourth-order F,E values',[F.c[4],E.c[4]])
    return Kdirect, F, E


def coefficient_K(a,q):
    _,_,_,_,X,eta = profile(q)
    d = 1+a
    A = d**3*(48*d*d-40*d-53)/512
    B = d**3*(16*d*d-104*d+203)/8192
    C = d**3*(4*d+1)**2/8192
    return A*X+B-C*eta


def coefficient_K1(a):
    d = 1+a
    return d**3*(516*d*d-528*d-393)/7168


def symbolic_profile():
    q = Polynomial([0,1])
    slopes = [Polynomial(7)]+[Polynomial(-1)+4*q]*3+[Polynomial(-1)-3*q]*4
    mu2,mu3,mu4 = [sum((t**k for t in slopes),Polynomial()) for k in (2,3,4)]
    check('universal balanced profile',sum(slopes,Polynomial()),Polynomial())
    check('complete profile second moment',mu2,Polynomial([56,0,84]))
    check('complete profile third moment',mu3,Polynomial([336,0,-252,84]))
    check('complete profile fourth moment',mu4,Polynomial([2408,0,504,-336,1092]))
    A,B,C = slopes[0],slopes[1],slopes[4]
    trace = A+B+C
    determinant = (B*C+3*A*C+4*A*B)/8
    gap = trace**2-4*determinant
    check('active compression trace',trace,5+q)
    check('active compression determinant',determinant,Polynomial([-6,6,Q(-3,2)]))
    check('active compression gap squared',gap,Polynomial([49,-14,7]))
    check('all-real-parameter positive gap identity',gap,7*(q-1)**2+42)
    Delta_n = Q(43,56)*mu2**2-mu4
    eta_n = (gap*mu2**2+(2*mu3-trace*mu2)**2)/2
    Gamma_n = eta_n-(56*mu4-13*mu2**2)*gap/30
    residual_n = Gamma_n-Q(4,105)*Delta_n*gap
    if any(residual_n.at(j) for j in range(3)):
        raise RuntimeError('local ratio cubic divisibility failed')
    record('complete local-line-defect numerator',residual_n)
    check('local-line-defect exact cubic factor',residual_n,
          q**3*Polynomial(residual_n.c[3:]))
    return residual_n


def fixture():
    if isqrt(RADICAND)**2 == RADICAND:
        raise RuntimeError('quadratic radicand unexpectedly square')
    symbolic_profile()
    for q in [Q(-1,160),Q(-1,100),Q(1,160),Q(0),Q(2),Q(-8,3),Q(1,2)]:
        theta,mu2,mu3,mu4,X,eta = profile(q)
        label = 'full matrix pinching q='+str(q)
        check(label+' balance',sum(theta),Q(0))
        Psi,T,dimension = commutant_concentration(theta)
        check(label+' defining concentration',64*Psi/mu2**2,eta)
        record(label+' full projected matrix digest',sha256(json.dumps(encode(T),sort_keys=True,separators=(',',':')).encode()).hexdigest())
        record(label+' commutant dimension, zero denotes direct commuting case',dimension)
    q = Q(-1,160)
    _,_,_,_,X,eta = profile(q)
    Delta = Q(43,56)-X
    Gamma = eta-(56*X-13)/30
    positive('selected angular moment deficit',Delta)
    positive('selected spectral Gram surplus',Gamma)
    a_upper = Q(301769,500000)
    d_upper = 1+a_upper
    delta = coefficient_K(a_upper,q)-coefficient_K1(a_upper)
    positive('actual rational endpoint quartic advantage',delta)
    check('credited rational endpoint advantage',delta,
          Q(372644481775755927899517226268859477,
            52713772239171568000000000000000000000000000000))
    ell = [Q(-3187,30720)*Delta+Q(1,8192)*Gamma,
           Q(-2456,30720)*Delta+Q(8,8192)*Gamma,
           Q(2768,30720)*Delta+Q(16,8192)*Gamma]
    ell_poly = Polynomial(ell)
    check('complete normalized angular deficit at endpoint',ell_poly.evaluate(d_upper),-delta/d_upper**3)
    positive('monotone normalized-deficit derivative at d=1',ell[1]+2*ell[2])
    positive('monotone normalized-deficit derivative slope',2*ell[2])
    gap_lower = delta/d_upper**3
    positive('uniform quartic gap lower bound on all0<=a<=a_upper',gap_lower)
    record('uniform actual-energy dominance coefficient gamma',gap_lower/2)
    stiffness = 1616*a_upper*a_upper+1800*a_upper-1675
    check('positive rational local stiffness numerator',stiffness,Q(148715461,15625000000))
    positive('upper radius below cutoff',Q(5,8)-a_upper)
    negative('local stiffness at three-fifths',1616*Q(3,5)**2+1800*Q(3,5)-1675)
    positive('local stiffness derivative at zero',Q(1800))
    a = Polynomial([0,1])
    check('exact algebraic local-threshold relation',(404*a+225)**2-219800,
          101*(1616*a**2+1800*a-1675))
    _,_,_,_,Xg,etag = profile(Q(-1,100))
    line_residual = etag-(56*Xg-13)/30-Q(4,105)*(Q(43,56)-Xg)
    check('exact failure of the proposed local-ratio line',line_residual,
          -Q(79197273,6881762064193205))
    negative('strict proposed-line obstruction',line_residual)
    for a in [Q(0),a_upper,Q(5,8)]:
        direct,F,E = direct_cubic(a)
        if a == a_upper:
            reject('omit exact energy elimination',direct, -F.c[4]/(E.c[2]*E.c[2]))
            reject('omit original within-block critical multiplicities',F.c[0],Complex(11/(1+a)))
    reject('replace pinching by unprojected rank-one concentration',eta,Q(1))
    reject('change squared active spectral gap',Q(49)-14*q+7*q*q,Q(49))
    reject('replace endpoint stiffness by zero',stiffness,Q(0))
    reject('incorrect strengthened Gram slope',line_residual,Q(0))
    digest = sha256(json.dumps(RECORDS,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    reject('alter exact complete-record digest',digest,'0'*64)
    return {'schema':1,'agent':'six-sendov-3','role':'researcher',
            'arithmetic':'exact Q and Q(sqrt1256647)[i] jets modulo s^6; rational full8x8 commutant projection',
            'claim_status':'complete exact algebra certificate; actual-energy inversion and local/global analytic proof separate',
            'identity_count':sum(r['kind']=='identity' for r in RECORDS),
            'strict_sign_count':sum(r['kind'] in ['positive','negative'] for r in RECORDS),
            'complete_record_count':len(RECORDS),'full_matrix_profile_count':7,
            'direct_original_cubic_radius_count':3,'corruption_control_count':len(CONTROLS),
            'corruption_controls':CONTROLS,'records_sha256':digest,'complete_records':RECORDS}


def main():
    if sys.argv[1:] not in [[],['--emit-fixture']]:
        raise SystemExit('usage: python3 -I -B verify.py [--emit-fixture]')
    path = Path(__file__).with_name('expected.json')
    if sys.argv[1:] != ['--emit-fixture']:
        try:
            expected = json.loads(path.read_text())
        except (OSError,ValueError) as exc:
            raise RuntimeError('required expected.json absent or malformed') from exc
    result = fixture()
    if sys.argv[1:] == ['--emit-fixture']:
        path.write_text(json.dumps(result,indent=2)+'\n')
    elif result != expected:
        raise RuntimeError('complete exact fixture differs')
    print(json.dumps({k:v for k,v in result.items() if k!='complete_records'},sort_keys=True))


if __name__ == '__main__':
    main()
