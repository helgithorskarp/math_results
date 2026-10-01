#!/usr/bin/env python3
"""Independent all-disk global-entry and evaluated variational audit.

Exact multivariate Laurent/Gaussian arithmetic, standard library only.
No author module is imported. The Laurent/Gaussian kernel openly reuses
this reviewer's earlier public checker. Joint moments stay symbolic.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import math
import sys

NAMES = ('v', 'z', 'A', 'I', 'X2', 'Y2', 'XY', 'XY2', 'Y3', 'Y4', 'theta', 'mean', 'radial', 'R', 'mu2', 'mu3', 'mu4', 'Psi', 'a', 'Delta', 'Gamma', 'u0', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7')
NV = len(NAMES)
ZERO = (0,)*NV
LABELS = []
RECORDS = []


def demand(ok, label):
    if not ok:
        raise ValueError(label)


class P:
    def __init__(self, value=0):
        self.terms = ({e: F(c) for e, c in value.items() if c}
                      if isinstance(value, dict) else ({ZERO: F(value)} if value else {}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, P) else P(x)

    def __add__(self, x):
        result = dict(self.terms)
        for e, c in P.cast(x).terms.items():
            result[e] = result.get(e, F(0))+c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.terms.items()})

    def __sub__(self, x):
        return self+-P.cast(x)

    def __rsub__(self, x):
        return P.cast(x)+-self

    def __mul__(self, x):
        result = defaultdict(F)
        for e, c in self.terms.items():
            for f, b in P.cast(x).terms.items():
                result[tuple(a+d for a, d in zip(e, f))] += c*b
        return P(result)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = P.cast(x)
        demand(len(x.terms) == 1, 'nonzero Laurent monomial divisor required')
        f, b = next(iter(x.terms.items()))
        return P({tuple(a-d for a, d in zip(e, f)): c/b for e, c in self.terms.items()})

    def __pow__(self, n):
        demand(type(n) is int, 'integer exponent required')
        if n < 0:
            return P(1)/(self**(-n))
        result, base = P(1), self
        while n:
            if n & 1:
                result = result*base
            base, n = base*base, n//2
        return result

    def coefficient(self, name, power):
        index = NAMES.index(name)
        result = {}
        for e, c in self.terms.items():
            if e[index] == power:
                f = list(e)
                f[index] = 0
                result[tuple(f)] = c
        return P(result)

    def substitute(self, values):
        result = P()
        for e, c in self.terms.items():
            remaining, factor = list(e), P(c)
            for name, value in values.items():
                index = NAMES.index(name)
                remaining[index] = 0
                factor = factor*P.cast(value)**e[index]
            result = result+P({tuple(remaining): 1})*factor
        return result

    def record(self):
        return [[*e, c.numerator, c.denominator] for e, c in sorted(self.terms.items())]

    def univariate_v(self):
        demand(all(not any(e[1:]) for e in self.terms), 'univariate coefficient expected')
        return [[e[0], c.numerator, c.denominator] for e, c in sorted(self.terms.items())]


def variable(name):
    e = list(ZERO)
    e[NAMES.index(name)] = 1
    return P({tuple(e): 1})


V, Z, A, I, X2, Y2, XY, XY2, Y3, Y4, TH, MEAN, RADIAL, R, MU2, MU3, MU4, PSI, AA, DELTA, GAMMA = [variable(name) for name in NAMES[:21]]
D = V**(-1)
B = 2*D-D**2
KAPPA = D*(D-F(13, 8))


class G:
    def __init__(self, re=0, im=0):
        self.re, self.im = P.cast(re), P.cast(im)

    @staticmethod
    def cast(x):
        return x if isinstance(x, G) else G(x)

    def __add__(self, x):
        x = G.cast(x)
        return G(self.re+x.re, self.im+x.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, x):
        return self+-G.cast(x)

    def __rsub__(self, x):
        return G.cast(x)+-self

    def __mul__(self, x):
        x = G.cast(x)
        return G(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)

    __rmul__ = __mul__

    def __pow__(self, n):
        demand(type(n) is int and n >= 0, 'nonnegative Gaussian power')
        result = G(1)
        for _ in range(n):
            result = result*self
        return result

    def __truediv__(self, x):
        x = G.cast(x)
        numerator = self*x.conjugate()
        norm = x.re*x.re+x.im*x.im
        return G(numerator.re/norm, numerator.im/norm)

    def conjugate(self):
        return G(self.re, -self.im)

    def substitute(self, values):
        return G(self.re.substitute(values), self.im.substitute(values))

    def record(self):
        return [self.re.record(), self.im.record()]


def identity(label, actual, expected=0):
    difference = G.cast(actual)-expected
    demand(not difference.re.terms and not difference.im.terms, label)
    LABELS.append(label)


def series(*values):
    demand(len(values) <= 5, 'too many truncated coefficients')
    return [G.cast(x) for x in values]+[G() for _ in range(5-len(values))]


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, x):
    return [v*x for v in a]


def mul(a, b):
    return [sum((a[k]*b[n-k] for k in range(n+1)), G()) for n in range(5)]


def power(a, n):
    result = series(1)
    for _ in range(n):
        result = mul(result, a)
    return result


def inverse(a):
    result = [G(1)/a[0]]
    for n in range(1, 5):
        result.append(-sum((a[k]*result[n-k] for k in range(1, n+1)), G())/a[0])
    return result


def real(a):
    return [G(x.re) for x in a]


def modulus(a, base):
    base = P.cast(base)
    demand(len(base.terms) == 1, 'positive monomial modulus base required')
    exponent, coefficient = next(iter(base.terms.items()))
    demand(coefficient > 0 and not any(exponent[1:]), 'base positive for all v>0')
    square = mul(a, [x.conjugate() for x in a])
    result = [G(base)]
    identity('modulus positive base', result[0]*result[0], square[0])
    for n in range(1, 5):
        result.append((square[n]-sum((result[k]*result[n-k] for k in range(1, n)), G()))/(2*result[0]))
    return result


def analytic_functional(moments, trace):
    value = add(trace, scale(real(moments[2]), -D/2))
    value = add(value, scale(real(moments[3]), D**2/6))
    value = add(value, scale(real(moments[4]), -D**3/8))
    return add(value, scale(power(real(moments[1]), 2), D/14))


DATA, ORIGINAL, STRICT = {}, {}, []


def named(poly):
    """Canonical complete named monomials, independent of author variable order."""
    result = {}
    for exponent, coefficient in P.cast(poly).terms.items():
        terms = tuple(sorted((name, power) for name, power in zip(NAMES, exponent) if power))
        demand(not any(name == 'z' for name, _ in terms), 'residue variable eliminated')
        result[terms] = coefficient
    return result


def canonical_jet(jet):
    result = {}
    rename = {'mean': 'm'}
    for order, value in enumerate(jet):
        for imaginary, poly in enumerate((value.re, value.im)):
            for terms, coefficient in named(poly).items():
                monomial = [(rename.get(name, name), exponent) for name, exponent in terms]
                if order:
                    monomial.append(('s', order))
                if imaginary:
                    monomial.append(('i', 1))
                key = tuple(sorted(monomial))
                result[key] = result.get(key, F(0)) + coefficient
    return {key: value for key, value in result.items() if value}


def wire_named(values):
    return [[[[name, power] for name, power in key],
             [coefficient.numerator, coefficient.denominator]]
            for key, coefficient in sorted(values.items())]


def save_jet(name, value, original_name=None):
    values = canonical_jet(value)
    DATA[name] = wire_named(values)
    if original_name:
        ORIGINAL[original_name] = values


def save_poly(name, value, original_name=None):
    save_jet(name, series(value), original_name)


def positive(label, value):
    demand(value > 0, label)
    STRICT.append(label)
    DATA[label] = [value.numerator, value.denominator]


def residue_moments(sums, prefix):
    """Near characteristic logarithm: no far secular recursion or word traces."""
    elementary = [series(1)]
    for degree in range(1, 5):
        value = series()
        for j in range(1, degree+1):
            value = add(value, scale(mul(elementary[degree-j], sums[j]),
                                     F((-1)**(j-1), degree)))
        elementary.append(value)
    inv_far = sum((-Z**j/(8*V)**(j+1) for j in range(5)), P())
    ratio = series()
    for degree in range(1, 5):
        factor = (-1)**degree*Z**(-degree)*((degree+1)*Z-(8-degree)*V)*inv_far
        ratio = add(ratio, scale(elementary[degree], factor))
    logarithm = series()
    for degree in range(1, 5):
        logarithm = add(logarithm, scale(power(ratio, degree), F((-1)**(degree+1), degree)))
    result = {}
    for k in range(1, 5):
        result[k] = [G(-k*x.re.coefficient('z', -k), -k*x.im.coefficient('z', -k))
                     for x in logarithm]
        for order in range(k):
            identity(prefix+' moment valuation '+str((k, order)), result[k][order])
        save_jet(prefix+' near moment '+str(k), result[k],
                 prefix+' near moment '+str(k))
    return result


def unbalanced():
    sums = [None, series(0, G(0, I), A),
            series(0, 0, -Y2, G(0, 2*XY), X2),
            series(0, 0, 0, G(0, -Y3), -3*XY2),
            series(0, 0, 0, 0, Y4)]
    moments = residue_moments(sums, 'unbalanced')
    lower = analytic_functional(moments, series(0, 0, 2*A))
    quartic = lower[4].re-3*D*X2/8
    quoted = (-59*D**3*Y4/512-47*D**2*XY2/64-83*D**3*Y2**2/14336
              -3*D*X2/4-59*D**3*I*Y3/4096+7*D**2*I*XY/128
              +1277*D**3*I**2*Y2/229376-677*D**3*I**4/1835008
              +23*D**2*A*Y2/512-D**2*A*I**2/128+3*D*A**2/64)
    for k in (0, 1, 3):
        identity('unbalanced lower coefficient '+str(k), lower[k])
    identity('complete unbalanced quadratic', lower[2], 2*A+3*D*Y2/8+D*I**2/128)
    identity('complete eleven joint coefficients', quartic, quoted)
    identity('unbalanced imaginary quartic', lower[4].im)
    save_jet('full unbalanced lower functional', lower, 'full unbalanced lower functional')
    save_poly('full eleven coefficient polynomial', quartic, 'full eleven coefficient polynomial')
    # The far branch is recovered from the exact full trace and near contour.
    far = add(series(9*V), add(scale(sums[1], 2), scale(moments[1], -1)))
    save_jet('unbalanced far jet', far, 'unbalanced far jet')
    majorants = [F(59,64), F(47,16), F(83,1792), F(3,2),
                 F(177,512), F(21,32), F(1277,3584), F(677,3584),
                 F(23,128), F(1,4), F(3,32)]
    bound = sum(majorants, F())
    demand(bound == F(26795,3584), 'complete coefficient majorant sum')
    positive('majorant slack below eight', F(8)-bound)
    DATA['eleven_absolute_majorants'] = [[x.numerator, x.denominator] for x in majorants]
    DATA['majorant_sum'] = [bound.numerator, bound.denominator]
    identity('real coordinate square completion',
             1-AA**2+(1+AA)*(AA-F(5,8))/2,
             F(361,512)-(AA-F(3,16))**2/2)
    positive('real coordinate slack', F(1)-F(489,512))
    return quartic


def aggregate_circle(poly):
    result = P()
    jt, jr = NAMES.index('theta'), NAMES.index('radial')
    for exponent, coefficient in poly.terms.items():
        th, rad = exponent[jt], exponent[jr]
        remaining = list(exponent)
        remaining[jt] = remaining[jr] = 0
        if rad:
            demand(rad == 1 and th == 0, 'retained independent radial term')
            factor = R
        elif th == 0:
            factor = P(8)
        elif th == 1:
            factor = P()
        else:
            demand(th in (2,3,4), 'retained angular point moment')
            factor = {2:MU2,3:MU3,4:MU4}[th]
        result = result+P({tuple(remaining):coefficient})*factor
    return result


def sum_circle(jet):
    return [G(aggregate_circle(x.re), aggregate_circle(x.im)) for x in jet]


def circle():
    phase = series(0, TH, MEAN)
    exponential = series()
    for k in range(5):
        exponential = add(exponential, scale(power(phase, k), G(0,1)**k/F(math.factorial(k))))
    denominator = add(series(D-1), mul(series(1,0,0,0,-RADIAL), exponential))
    u = inverse(denominator)
    for k, value in enumerate(mul(u, denominator)):
        identity('literal reciprocal inverse '+str(k), value, int(k == 0))
    delta = add(u, series(-V))
    sums = [None]+[sum_circle(power(delta,k)) for k in range(1,5)]
    moments = residue_moments(sums, 'circle mean radial')
    energy = sum_circle(mul(delta, [x.conjugate() for x in delta]))
    far = add(series(9*V), add(scale(sums[1],2), scale(moments[1],-1)))
    far_loss = add(modulus(far,9*V), scale(real(far),-1))
    c2, cr = V**2/2-V**3, V**2/2+V**3/8
    real_square = (c2**2*(MU4/2+MU2**2/32)
                   +2*c2*cr*(MU4/8-MU2**2/64)+cr**2*PSI)
    objective = scale(real(sums[1]),2)
    objective = add(objective, scale(real(moments[2]),-D/2))
    objective = add(objective, scale(real(moments[3]),D**2/6))
    objective = add(objective, scale(real(moments[4]),-D**3/8))
    objective = add(objective, series(0,0,0,0,real_square*D/2))
    objective = add(objective, far_loss)
    combined = add(objective, scale(energy,-KAPPA))
    ac = D**3*(48*D**2-40*D-53)/512
    bc = D**3*(16*D**2-104*D+203)/8192
    cc = D**3*(4*D+1)**2/8192
    want = -V**8*ac*MU4-V**8*bc*MU2**2+64*V**8*cc*PSI+5*V**3*MEAN**2+2*V**2*R
    for k in range(4):
        identity('circle lower coefficient '+str(k), combined[k])
    identity('complete mean inward angular quartic', combined[4], want)
    identity('far mean loss',far_loss[4],F(9,2)*V**3*MEAN**2)
    save_jet('circle mean radial far jet',far,'circle mean radial far jet')
    save_jet('full circle energy jet',energy,'full circle energy jet')
    save_poly('complete mean inward angular quartic',combined[4].re,
              'complete mean inward angular quartic')
    save_poly('near real square limiting expression',real_square,'near real square limiting expression')
    save_jet('far mean modulus loss',far_loss,'far mean modulus loss')
    k1 = D**3*(516*D**2-528*D-393)/7168
    kq = D**3*(784*D**2-856*D-443)/16384
    sigma = D**3*(2768*D**2-2456*D-3187)/30720
    x = F(43,56)-DELTA
    eta = (56*x-13)/30+GAMMA
    identity('singleton angular exact loss', k1-(ac*x+bc-cc*eta),sigma*DELTA+cc*GAMMA)
    identity('two family angular exact loss',k1-kq,D**3*(2768*D**2-2456*D-3187)/114688)
    identity('moving pair angular exact loss',
             kq-(ac*x+bc-cc*eta),sigma*(F(1,2)-x)+cc*GAMMA)
    save_poly('K1',k1,'K1')
    save_poly('angular gap factor',sigma,'angular gap factor')
    save_poly('KQ',kq)
    return combined[4].re


def inverse_matrix(matrix):
    n = len(matrix)
    augmented = [[F(x) for x in row]+[F(int(i == j)) for j in range(n)]
                 for i,row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if augmented[i][j]), None)
        demand(pivot is not None, 'invertible rational basis')
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        divisor = augmented[j][j]
        augmented[j] = [x/divisor for x in augmented[j]]
        for i in range(n):
            if i != j:
                multiple = augmented[i][j]
                augmented[i] = [x-multiple*y for x,y in zip(augmented[i],augmented[j])]
    return [row[n:] for row in augmented]


def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),P())
             for j in range(len(b[0]))] for i in range(len(a))]


def compression():
    # An explicit rational eight-dimensional basis, not eight sampled u vectors.
    basis = [[0]*8 for _ in range(8)]
    for j in range(6):
        basis[j+1][j] = 1
        basis[7][j] = -1
    for i in range(8):
        basis[i][6] = 7 if i == 0 else -1
        basis[i][7] = 1
    inv = inverse_matrix(basis)
    back = matmul(inv,basis)
    for i in range(8):
        for j in range(8):
            identity('rational basis inverse '+str((i,j)),back[i][j],int(i == j))
    us = [variable('u'+str(j)) for j in range(8)]
    n = [[us[i]*(1+int(i == j)) for j in range(8)] for i in range(8)]
    block = matmul(matmul(inv,n),basis)
    q = [[F(int(i == j))-F(1,7) for j in range(7)] for i in range(7)]
    embedding = [row[:6] for row in basis[1:]]
    ub, ua = us[1:], us[0]
    mean = sum(ub,P())/7
    a = matmul(matmul(q,[[ub[i]*int(i == j) for j in range(7)] for i in range(7)]),embedding)
    qu = [sum((q[i][j]*ub[j] for j in range(7)),P()) for i in range(7)]
    uq = [sum((ub[i]*embedding[i][j] for i in range(7)),P()) for j in range(6)]
    want = [a[i]+[-qu[i],9*qu[i]] for i in range(6)]
    want += [[-x/56 for x in uq]+[(7*ua+mean)/8,9*(ua-mean)/8],
             [x/8 for x in uq]+[7*(ua-mean)/8,9*(ua+7*mean)/8]]
    for i in range(8):
        for j in range(8):
            identity('complete symbolic compression '+str((i,j)),block[i][j],want[i][j])
    DATA['symbolic_compression'] = [[wire_named(named(x)) for x in row] for row in block]
    c0 = G(0,-V**2)
    kn = G(F(1,392))
    kf = -c0/(56*V)
    identity('near limiting graph equation',7*c0*kn,c0/56)
    identity('far limiting graph equation',7*c0*kn+kf*(8*V),-c0/8)
    identity('rankone Hermitian graph shear',-kn,-F(1,392))
    save_poly('leading graph kn scalar',kn.re,'leading graph kn scalar')
    save_jet('leading graph kf scalar',series(kf),'leading graph kf scalar')
    return c0, kn, kf


def root_signs():
    pg = lambda x: 2768*x*x+3080*x-2875
    pp = lambda x: 208*x*x+232*x-215
    ag = (F(604757,10**6),F(604758,10**6))
    ap = (F(601908,10**6),F(601909,10**6))
    for name,fun,interval in [('aG',pg,ag),('aP',pp,ap)]:
        positive(name+' bracket negative side',-fun(interval[0]))
        positive(name+' bracket positive side',fun(interval[1]))
        DATA[name+'_isolating_interval'] = [[x.numerator,x.denominator] for x in interval]
    positive('aP below aG',ag[0]-ap[1])
    positive('aG above local151/250',ag[0]-F(151,250))
    positive('aG below prior5/8',F(5,8)-ag[1])
    local = lambda x:1616*x*x+1800*x-1675
    positive('L positive at151/250',local(F(151,250)))
    derivative = -4848*AA**2-3968*AA+10175
    identity('L derivative global decomposition',
             derivative,1359+8816*(1-AA)+4848*AA*(1-AA))
    positive('L derivative floor',F(1359))
    identity('L exact derivative numerator',
             (3232*AA+1800)*(1+AA)-5*(1616*AA**2+1800*AA-1675),
             derivative)
    positive('global angular rounding coefficient',F(1,125))
    demand(F(1,125)*F(5,4)==F(1,100),'coarse distance cutoff equality')
    DATA['global_rounding_constant'] = [1,125]
    DATA['physical_half_costs'] = {'radial':[1,4],'mean':[5,16],'split':'L(minJ)/2'}


def invalid_controls(quartic, nonlinear, graph):
    bad = []
    for label,actual,wrong in [
        ('changed unbalanced coefficient',quartic,quartic+D**3*Y2**2/14336),
        ('missing far mean loss',nonlinear,nonlinear-F(9,2)*V**3*MEAN**2),
        ('half inward coefficient',nonlinear,nonlinear-V**2*R),
        ('wrong graph denominator64',graph[2],-graph[0]/(64*V))]:
        try:
            identity('reject '+label,actual,wrong)
        except ValueError:
            bad.append(label)
        else:
            raise ValueError('incorrect mathematical expression accepted')
    try:
        inverse_matrix([[1,1],[1,1]])
    except ValueError:
        bad.append('singular rational basis')
    else:
        raise ValueError('singular basis accepted')
    DATA['rejected_invalid_controls'] = bad


def compare_original(path):
    # Read only after all independent algebra and signs are complete.
    old = json.loads(path.read_text())
    records = old['records']
    for name,expected in ORIGINAL.items():
        value = records[name]
        if isinstance(value,list):
            got = {():F(*value)}
        else:
            got = {tuple(sorted((name,power) for name,power in key)):F(*value)
                   for key,value in value['terms']}
        demand(got == expected,'literal complete original record '+name)
    return len(ORIGINAL)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--original',type=Path)
    args = parser.parse_args()
    quartic = unbalanced()
    nonlinear = circle()
    graph = compression()
    root_signs()
    invalid_controls(quartic,nonlinear,graph)
    result = {
        'agent':'six-reviewer-3','role':'independent mathematical reviewer',
        'target_height':8212,
        'method':'Characteristic logarithmic residues; Gaussian coefficient arrays; trace recovery of far branch; universal symbolic rational change of basis.',
        'identity_count':len(LABELS),'identities':LABELS,
        'strict_sign_count':len(STRICT),'strict_signs':STRICT,
        'independent_records':DATA,
        'eligible_literal_original_records':len(ORIGINAL),
        'new_full_disk_variational_interval':'[aP,1]',
        'new_uniform_leading_pair_selection_interval':'[aP,aG]',
        'analytic_bridges_machine_checked':False,
    }
    encoded = json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.write:
        args.write.write_text(encoded)
    if args.check:
        demand(json.loads(args.check.read_text())==result,'complete independent expected summary')
    if args.original:
        print('Literal complete original records compared: '+str(compare_original(args.original)))
    print(json.dumps({'agent':'six-reviewer-3','verified':True,
                      'identities':len(LABELS),'strict_signs':len(STRICT),
                      'eligible_original_records':len(ORIGINAL),
                      'result_sha256':sha256(encoded.encode()).hexdigest()}))


if __name__ == '__main__':
    main()
