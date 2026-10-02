"""six-reviewer-1: independent exact checks of the 9629 collar proof.

Python 3.11+, standard library, rational coefficients, characteristic zero.
Written target proof visible; target executables/fixtures unread at first seal.
No finite computation certifies the analytic and actual-disk proof bridges.
"""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from fractions import Fraction as Q


class P:
    """Sparse polynomial; keys are sorted multisets of literal variable names."""
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): Q(v) for k, v in value.items() if v}
        else:
            self.c = {(): Q(value)} if value else {}

    def __add__(self, other):
        result = dict(self.c)
        for k, v in P(other).c.items():
            result[k] = result.get(k, Q(0)) + v
        return P(result)
    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, other):
        result = {}
        for k, v in self.c.items():
            for l, u in P(other).c.items():
                key = tuple(sorted(k + l))
                result[key] = result.get(key, Q(0)) + v * u
        return P(result)
    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1 / Q(other))

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError('polynomial power')
        result = P(1)
        for _ in range(n):
            result = result * self
        return result

    def substitute(self, mapping):
        out = P()
        for key, v in self.c.items():
            term = P(v)
            for symbol in key:
                term = term * mapping.get(symbol, var(symbol))
            out = out + term
        return out

    def record(self):
        return [[list(k), str(v)] for k, v in sorted(self.c.items())]


def var(name):
    return P({(name,): Q(1)})


def bar(poly):
    return P({tuple(sorted(s[1:] if s.startswith('~') else '~' + s
                           for s in k)): v for k, v in P(poly).c.items()})


def re(poly):
    return (P(poly) + bar(poly)) / 2


def equal(left, right, name):
    if P(left).c != P(right).c:
        raise ValueError('identity: ' + name)
    return P(left).record()


def positive(value, name):
    if not isinstance(value, Q) or value <= 0:
        raise ValueError('strict rational margin: ' + name)
    return str(value)


def endpoint(poly, e, h):
    """Termwise full-window majorant nu*eta+mu*H, not interpolation."""
    nu = mu = Q(0)
    for symbols, coeff in poly.c.items():
        if coeff < 0 or not symbols or set(symbols) - {'eta', 'H'}:
            raise ValueError('endpoint domain / nonnegative polynomial')
        i, j = symbols.count('eta'), symbols.count('H')
        if j:
            mu += coeff * e**i * h**(j - 1)
        else:
            nu += coeff * e**(i - 1)
    return nu, mu


def kernel_identities():
    d = [var('d' + str(k)) for k in range(9)]
    # Expand the defining product and its conjugate separately at z^9=1.
    pp = {0: P(9)}
    p = {k: d[k] for k in range(9)}
    for k in range(1, 9):
        pp[k] = k * d[k]
    rows = [P() for _ in range(9)]
    for k, a in pp.items():
        for l, b in p.items():
            rows[(k - l) % 9] += a * bar(b)
            rows[(l - k) % 9] += bar(a) * b
    for k, a in p.items():
        for l, b in p.items():
            rows[(k - l) % 9] -= 9 * a * bar(b)
    identities = {}
    for m in range(9):
        expected = 9 * d[m] + 9 * bar(d[(-m) % 9])
        for k in range(9):
            for l in range(9):
                if (k - l) % 9 == m:
                    expected += (k + l - 9) * d[k] * bar(d[l])
        identities['Fourier-row-' + str(m)] = equal(rows[m], expected, str(m))
    rho = lambda k: Q(1) if k % 3 == 0 else Q(-1, 2)
    pair = sum((rho(m) * rows[m] for m in range(9)), P())
    linear = 18 * re(sum((rho(k) * d[k] for k in range(9)), P()))
    quadratic = sum(((k + l - 9) * rho(k - l) * d[k] * bar(d[l])
                     for k in range(9) for l in range(9)), P())
    identities['paired-whole-kernel'] = equal(pair, linear + quadratic, 'pair')
    t = var('delta')
    top = sum(((k + l - 9) * rho(k - l) * d[k] * bar(d[l])
               for k in [0, 7, 8] for l in [0, 7, 8]), P())
    top = top.substitute({'d0': t - d[7] - d[8],
                          '~d0': bar(t - d[7] - d[8])})
    right = (-3 * d[8] * bar(d[8]) - 6 * d[7] * bar(d[7])
             - 27 * re(d[8] * bar(d[7]))
             + re((19 * d[8] + 20 * d[7]) * bar(t)) - 9 * t * bar(t))
    identities['entire-complex-top-reduction'] = equal(top, right, 'top')
    a = var('a')
    anchored = linear.substitute({'d0': 1 - a**9 - sum(
        (d[k] * a**k for k in range(1, 9)), P()),
        '~d0': 1 - a**9 - sum((bar(d[k]) * a**k for k in range(1, 9)), P())})
    # bar(a) is not introduced: actual a is real, an explicit substitution.
    explicit = (18 * (1 - a**9) - 27 * re(d[8] + d[7])
                + 18 * (1 - a**8) * re(d[8])
                + 18 * (1 - a**7) * re(d[7])
                + 18 * sum(((rho(k) - a**k) * re(d[k]) for k in range(1, 7)), P()))
    identities['whole-anchored-pair-linear'] = equal(anchored, explicit, 'anchor')
    # Every lower cross coefficient is covered, including both orientations.
    maxima = {}
    for top_index, limit in [(0, 16), (8, 10), (7, 8)]:
        m = max(abs(2 * (top_index + k - 9) * rho(top_index - k))
                for k in range(1, 7))
        if m > limit:
            raise ValueError('lower cross bound')
        maxima[str(top_index)] = {'actual_max': str(m), 'used_bound': limit}
    lower_max = max(abs((k + l - 9) * rho(k - l))
                    for k in range(1, 7) for l in range(1, 7))
    if lower_max > 7:
        raise ValueError('lower Hermitian bound')
    maxima['lower_block'] = {'actual_max': str(lower_max), 'used_bound': 7}
    return identities, maxima


def newton_identities():
    z = [var('z' + str(i)) for i in range(8)]
    elementary = [P(1)] + [P() for _ in range(8)]
    for t in z:
        for j in range(8, 0, -1):
            elementary[j] += t * elementary[j - 1]
    moments = [sum((t**j for t in z), P()) for j in range(1, 5)]
    u, t2, t3, t4 = moments
    return {
        'Newton-1': equal(u, elementary[1], 'Newton1'),
        'Newton-2': equal(Q(9, 7) * elementary[2], Q(9, 14) * (u*u-t2), 'Newton2'),
        'Newton-3': equal(-Q(3, 2)*elementary[3], -u**3/4+3*u*t2/4-t3/2, 'Newton3'),
        'Newton-4': equal(Q(9, 5)*elementary[4], 3*u**4/40-9*u*u*t2/20
                         +9*t2*t2/40+3*u*t3/5-9*t4/20, 'Newton4'),
    }


def scalar_reductions():
    eta,x,y,L,c1,H = [var(k) for k in ['eta','x','y','L','c1','H']]
    kappa=Q(19,96);S=var('S');a=1-eta;D0=9*eta+x+y+L
    difference=8*a*a-(8+3*eta)*a**3
    records={'full-low-F-anchor-gap':equal(difference,5*eta-7*eta**2-eta**3+3*eta**4,'anchor gap')}
    Dupper=162*eta-18*S+144*eta*x+126*eta*y+18*L+7*x*x+5*y*y+3*L*L
    Qupper=D0*x+6*x*y+8*D0*c1+8*L*L+4*y*L
    base=(Dupper+Qupper)/9+c1
    S8=Q(45,8)*eta+Q(9,8)*kappa*H-Q(5,16)*y-9*eta*eta-Q(2,3)*x*x-eta*x
    S9=Q(45,8)*eta+Q(13,384)*y-9*eta*eta-Q(8,9)*x*x-eta*x
    # Only the positive linear y term is replaced by Newton; all other y remain.
    first=base.substitute({'S':S8})-Q(5,8)*y+Q(5,8)*(Q(9,14)*H+Q(32,63)*x*x)
    M0=(Q(27,4)*eta+18*eta*eta+19*eta*x+14*eta*y+2*L
        +(Q(45,112)-Q(9,4)*kappa)*H+Q(160,63)*x*x+Q(5,9)*y*y
        +Q(7,9)*x*y+L*x/9+Q(11,9)*L*L+Q(4,9)*y*L+c1*(1+Q(8,9)*D0))
    records['complete-first-mean-reduction']=equal(first,M0,'M0')
    M1=(Q(27,4)*eta+18*eta*eta+19*eta*x+14*eta*y+2*L
        +Q(8,3)*x*x+Q(5,9)*y*y+Q(7,9)*x*y+L*x/9
        +Q(11,9)*L*L+Q(4,9)*y*L+c1*(1+Q(8,9)*D0))
    records['complete-second-mean-reduction']=equal(base.substitute({'S':S9})+Q(13,192)*y,M1,'M1')
    return records


def gauss(real=0,imag=0):
    return (Q(real),Q(imag))


def gadd(a,b):
    return (a[0]+b[0],a[1]+b[1])


def gmul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def gbar(a):
    return (a[0],-a[1])


def laurent_add(a,b):
    result=dict(a)
    for k,v in b.items():
        result[k]=gadd(result.get(k,gauss()),v)
    return {k:v for k,v in result.items() if v!=gauss()}


def laurent_scale(a,c):
    return {k:gmul(v,gauss(c)) for k,v in a.items() if v!=gauss() and c}


def laurent_mul(a,b):
    result={}
    for k,v in a.items():
        for l,u in b.items():
            result[k+l]=gadd(result.get(k+l,gauss()),gmul(v,u))
    return {k:v for k,v in result.items() if v!=gauss()}


def laurent_bar(a):
    return {-k:gbar(v) for k,v in a.items()}


def root_product(roots):
    p={0:gauss(1)}
    for r in roots:
        p=laurent_mul(p,{1:gauss(1),0:gmul(gauss(-1),r)})
    return p


def weight_polynomial(p):
    zp={k:gmul(gauss(k),v) for k,v in p.items() if k}
    first=laurent_mul(zp,laurent_bar(p))
    return laurent_add(laurent_add(first,laurent_bar(first)),
                       laurent_scale(laurent_mul(p,laurent_bar(p)),-9))


def literal_controls():
    zero,one,i=gauss(),gauss(1),gauss(0,1)
    cases=[('all-zero collision',[zero]*9),
           ('boundary and repeated originals',[one]*3+[gauss(-1)]*2+[i]*2+[zero,gauss(Q(3,5),Q(4,5))]),
           ('complex nonconjugate originals',[gauss(Q(1,3),Q(2,3)),gauss(Q(-1,2),Q(1,4)),
             gauss(Q(2,5),Q(-1,5)),gauss(Q(1,7),Q(-2,7)),zero,zero,one,i,gauss(-1)]),
           ('outside-disk necessity control',[gauss(Q(5,4))]+[zero]*8)]
    controls=[]
    for name,roots in cases:
        p=root_product(roots);left=weight_polynomial(p);right={}
        for j,r in enumerate(roots):
            q=root_product(roots[:j]+roots[j+1:])
            norm=r[0]**2+r[1]**2
            right=laurent_add(right,laurent_scale(laurent_mul(q,laurent_bar(q)),1-norm))
        if left!=right:raise ValueError('full literal division-free weight')
        encode=lambda a:[[k,str(v[0]),str(v[1])] for k,v in sorted(a.items())]
        controls.append({'name':name,'original_roots':[[str(r[0]),str(r[1])] for r in roots],
                         'polynomial':encode(p),'whole_weight':encode(left),
                         'disk_feasibility':all(r[0]**2+r[1]**2<=1 for r in roots)})
    eta=Q(1,65536);a=1-eta;c8=Q(9,256)
    p={9:gauss(1),8:gauss(c8),0:gauss(-a**9-c8*a**8)}
    weight=weight_polynomial(p)
    # Negative powers at -1 remain exactly integral; do not use float ** here.
    at_minus_one=sum((v[0]*(1 if k%2==0 else -1) for k,v in weight.items()),Q(0))
    F=7/a+1/(a+Q(1,32));H=Q(1,1024)
    margins={'low-F':positive(8+3*eta-F,'nondisk low F'),
             'radius-1/25':positive(Q(1,25)-Q(1,32),'nondisk collar'),
             'violates-H25':positive(H-25*eta,'nondisk H25'),
             'negative-root-weight':positive(-at_minus_one,'nondisk disk weight')}
    if sum((gmul(v,gauss(a**k))[0] for k,v in p.items()),Q(0))!=0:
        raise ValueError('nondisk anchor')
    derivative={k-1:gmul(gauss(k),v) for k,v in p.items() if k}
    if derivative!={8:gauss(9),7:gauss(Q(9,32))}:raise ValueError('all counted criticals')
    controls.append({'name':'credited q from own9631/9669, not a new counterexample',
                     'eta':str(eta),'a':str(a),'c8':str(c8),'H':str(H),'F':str(F),
                     'critical_multiset':['0']*7+['-1/32'],'polynomial':[[k,str(v[0]),str(v[1])] for k,v in sorted(p.items())],
                     'weight_at_minus_one':str(at_minus_one),'margins':margins,'disk_feasibility':False})
    return controls


def collar_record(radius, stages, mean_steps, e=Q(1, 65536)):
    kappa = Q(19, 96)
    h = 8 * radius * radius
    b = {k: Q(9 * math.comb(8, 9-k), 8*k) * radius**(7-k) for k in range(1, 8)}
    ell = sum(b[k] for k in range(1, 7))
    C = Q(27, 4) + 18*e
    N = (63*e + 2*ell + Q(45, 112) - Q(9, 4)*kappa
         +(Q(5, 9)*Q(9, 2)**2+Q(11, 9)*ell**2+Q(4, 9)*Q(9, 2)*ell)*h
         +b[1]*(1+Q(8, 9)*(9*e+Q(9, 2)*h+ell*h)))
    margins = {'analytic-radius-below-1/24': positive((1-e)/24-radius, 'collar'),
               'positive-static-energy': positive(h, 'static H')}
    stage_records = []
    x0 = 9 * radius
    for j, (X, Y) in enumerate(stages):
        lam = (19*e+Q(160, 63)*x0+Q(7, 9)*Q(9, 2)*h+ell*h/9+Q(8, 9)*b[1]*h)
        div = 1-lam
        for name, value in [('divisor', div), ('eta', X*div-C), ('energy', Y*div-N)]:
            margins['linear-'+str(j)+'-'+name] = positive(value, name)
        stage_records.append({'input_x0': str(x0), 'X': str(X), 'Y': str(Y),
                              'lambda': str(lam), 'C': str(C), 'N': str(N)})
        x0 = X*e+Y*h
    eta, H = var('eta'), var('H')

    def inputs(X, Y):
        x = X*eta+Y*H
        u = Q(8, 9)*x
        y = Q(9, 14)*(H+u*u)
        coeff = {k: b[k]*H for k in range(1, 5)}
        coeff[6] = u**3/4+3*u*H/4+radius*H/2
        coeff[5] = (3*u**4/40+9*u*u*H/20+9*H*H/40
                    +3*radius*u*H/5+9*radius*radius*H/20)
        L = sum(coeff.values(), P())
        return x,u,y,coeff,L

    def M1(X, Y):
        x,u,y,coeff,L = inputs(X,Y)
        D0 = 9*eta+x+y+L
        return (Q(27, 4)*eta+18*eta*eta+19*eta*x+14*eta*y+2*L
                +Q(8, 3)*x*x+Q(5, 9)*y*y+Q(7, 9)*x*y+L*x/9
                +Q(11, 9)*L*L+Q(4, 9)*y*L+coeff[1]*(1+Q(8, 9)*D0))

    X,Y = stages[-1]
    polys, majorants = {}, {}
    for j,(next_X,next_Y) in enumerate(mean_steps):
        poly = M1(X,Y);nu,mu = endpoint(poly,e,h)
        name = 'whole-M1-'+str(j)
        polys[name] = poly.record()
        majorants[name] = {'input': [str(X), str(Y)], 'nu': str(nu), 'mu': str(mu),
                           'output': [str(next_X), str(next_Y)]}
        margins[name+'-eta'] = positive(next_X-nu, name)
        margins[name+'-energy'] = positive(next_Y-mu, name)
        X,Y = next_X,next_Y
    x,u,y,coeff,L = inputs(X,Y)
    Delta = 9*eta+8*eta*x+7*eta*y+L
    Qplus = 27*x*y+(19*x+20*y)*Delta+16*(x+y+Delta)*L+10*x*L+8*y*L+7*L*L
    Splus = (6*eta+Q(16, 3)*eta*x+Q(14, 3)*eta*y
             +sum((coeff[k] for k in [1,2,4,5]), P())
             +2*eta*coeff[3]+4*eta*coeff[6]+Qplus/27)
    T = Q(8, 9)*Splus+Q(5, 18)*y+Q(8, 9)*eta*x+3*u*u/4+8*eta*eta
    for name,poly in [('whole-Splus',Splus),('whole-Qplus',Qplus),('whole-T',T)]:
        polys[name] = poly.record()
        nu,mu = endpoint(poly,e,h)
        majorants[name] = {'nu':str(nu),'mu':str(mu)}
    nu,mu = endpoint(T,e,h);nu-=5;g=kappa-mu
    margins['energy-feedback-divisor'] = positive(g,'feedback g')
    margins['fixed-energy-entry-numerical-only'] = positive(Q(1,512)-25*e,'H25 numerical energy threshold; eta hypothesis still required')
    return {'R':str(radius),'e':str(e),'h':str(h),'kappa':str(kappa),
            'b':{str(k):str(v) for k,v in b.items()},'ell':str(ell),
            'linear_stages':stage_records,'polynomials':polys,'majorants':majorants,
            'nu':str(nu),'g':str(g),'ratio':str(nu/g),'margins':margins}


def dynamic_stages(radius, count=4, e=Q(1,65536)):
    """Choose finite rational proof constants by upward integer rounding."""
    h,kappa=8*radius**2,Q(19,96)
    b={k:Q(9*math.comb(8,9-k),8*k)*radius**(7-k) for k in range(1,8)}
    ell=sum(b[k] for k in range(1,7));C=Q(27,4)+18*e
    N=(63*e+2*ell+Q(45,112)-Q(9,4)*kappa
       +(Q(5,9)*Q(9,2)**2+Q(11,9)*ell**2+Q(4,9)*Q(9,2)*ell)*h
       +b[1]*(1+Q(8,9)*(9*e+Q(9,2)*h+ell*h)))
    x0=9*radius;result=[]
    for _ in range(count):
        div=1-19*e-Q(160,63)*x0-Q(7,9)*Q(9,2)*h-ell*h/9-Q(8,9)*b[1]*h
        if div<=0:raise ValueError('dynamic initial divisor')
        X=Q(C//div+1);Y=Q(N//div+1)
        result.append((X,Y));x0=X*e+Y*h
    return result


def output():
    kernel,maxima=kernel_identities();newton=newton_identities()
    original=collar_record(Q(1,25),[(Q(169),Q(26)),(Q(66),Q(10)),(Q(11),Q(2))],
                           [(Q(7),Q(1,4)),(Q(7),Q(1,8))])
    original['margins']['original-H25'] = positive(25*Q(original['g'])-Q(original['nu']),'H25')
    r=Q(1,25);extended_e=Q(1,16384)
    stages=[(Q(173),Q(26)),(Q(83),Q(13)),(Q(14),Q(2)),(Q(8),Q(2))]
    extension=collar_record(r,stages,[(Q(7),Q(1,4)),(Q(7),Q(1,8)),(Q(7),Q(1,16))],e=extended_e)
    extension['margins']['extended-H25'] = positive(25*Q(extension['g'])-Q(extension['nu']),'H25 extended eta window')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'domain':'Q, characteristic zero; bar tokens independent until explicit real/anchor substitution',
            'identities':dict(kernel,**newton,**scalar_reductions()),'complete_cross_bounds':maxima,
            'literal_controls':literal_controls(),'original':original,'extension':extension}


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()


def strict_load(path):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate fixture key')
            result[key]=value
        return result
    def reject(value):
        raise ValueError('nonfinite fixture token')
    p=Path(path)
    if p.stat().st_size>1000000:raise ValueError('fixture exceeds compact limit')
    return json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=reject)


def same_typed(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same_typed(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same_typed(x,y) for x,y in zip(a,b))
    return a==b


def main():
    try:
        result=output()
        if len(sys.argv)==2 and sys.argv[1]=='--record':
            print(json.dumps(result,sort_keys=True,indent=2))
        else:
            if len(sys.argv)==3 and sys.argv[1]=='--expect':
                if not same_typed(result,strict_load(sys.argv[2])):raise ValueError('complete typed record mismatch')
            elif len(sys.argv)!=1:raise ValueError('arguments')
            print(json.dumps({'status':'PASS','full_record_sha256':hashlib.sha256(canonical(result)).hexdigest(),
                              'whole_identities':len(result['identities']),
                              'strict_margins':len(result['original']['margins'])+len(result['extension']['margins']),
                              'full_literal_controls':len(result['literal_controls']),
                              'original_eta_endpoint':result['original']['e'],
                              'extended_eta_endpoint':result['extension']['e']}))
    except (ValueError,TypeError,ZeroDivisionError) as error:
        print('FAIL:',error,file=sys.stderr);raise SystemExit(1)


if __name__=='__main__':
    main()
