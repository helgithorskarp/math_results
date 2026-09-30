#!/usr/bin/env python3
"""Exact author checks for the complete balanced four-double angular class.

Author six-sendov-2, researcher. Sparse rational polynomials and the full
compression commutant checker openly adapt the author's asymmetric
four-block source; the quartic-invariant restoration is new here.
Standard library only, no campaign import or floating proof input.
Written coverage and the cited polynomial asymptotics remain outside a
formal kernel. Independent review of this extension is pending.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse, hashlib, json

CHECKS=0
def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

class P:
    """Sparse exact Q[x0,x1,x2]; exponent order is explicit and fixed."""
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}
        if any(len(e) != 3 or any(k < 0 for k in e) for e in self.t):
            raise ValueError('invalid polynomial exponent')

    def __add__(self, other):
        out = dict(self.t)
        for e, c in P(other).t.items():
            out[e] = out.get(e, F(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x+y for x, y in zip(e, h))
                out[k] = out.get(k, F(0)) + c*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out, a = P(1), self
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]

def subst(poly, variables):
    powers = []
    for axis, v in enumerate(variables):
        degree = max((e[axis] for e in poly.t), default=0)
        row = [P(1)]
        for _ in range(degree):
            row.append(row[-1]*P(v))
        powers.append(row)
    out = P(0)
    for e, c in poly.t.items():
        term = P(c)
        for axis, k in enumerate(e):
            term *= powers[axis][k]
        out += term
    return out

def scalar(poly, values):
    out = subst(poly, values)
    require(not any(any(e) for e in out.t), 'evaluation is scalar')
    return out.t.get((0, 0, 0), F(0))

def derivative(poly, axis):
    return P({tuple(k-1 if i == axis else k for i, k in enumerate(e)):
              e[axis]*c for e, c in poly.t.items() if e[axis]})

def remove_monomial(poly, axis, power, name):
    require(all(e[axis] >= power for e in poly.t), name+' divisibility')
    reduced = P({tuple(k-power if i == axis else k for i, k in enumerate(e)):
                 c for e, c in poly.t.items()})
    variable = (X, H, U)[axis]
    require(reduced*variable**power == poly, name+' reconstruction')
    return reduced

def prod(values):
    out = P(1)
    for v in values:
        out *= v
    return out

def affine_power(poly, box):
    """Binomial affine substitution performed one axis at a time."""
    data = dict(poly.t)
    for axis, (a, b) in enumerate(box):
        out = {}
        for e, c in data.items():
            for k in range(e[axis]+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(e[axis], k)*a**(e[axis]-k)*(b-a)**k
        data = {e: c for e, c in out.items() if c}
    return data

def bernstein(poly, box):
    degrees = tuple(max((e[i] for e in poly.t), default=0) for i in range(3))
    normalized = affine_power(poly, box)
    data = dict(normalized)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in data.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*F(comb(k, e[axis]), comb(degree, e[axis]))
        data = {e: c for e, c in out.items() if c}
    indices = list(product(*(range(n+1) for n in degrees)))
    coefficients = [data.get(e, F(0)) for e in indices]
    # Independent inverse basis identity in the normalized power coordinates.
    inverse = dict(data)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in inverse.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(degree, k)*comb(k, e[axis])*(-1)**(k-e[axis])
        inverse = {e: c for e, c in out.items() if c}
    require(inverse == normalized, 'complete inverse Bernstein reconstruction')
    return coefficients, degrees

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def certificate(name, poly, box, strict=False):
    require(len(box) == 3 and all(a < b for a, b in box), name+' genuine box')
    coefficients, degrees = bernstein(poly, box)
    for value in coefficients:
        require(value > 0 if strict else value >= 0, name+' Bernstein sign')
    return {'name': name, 'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'entries': len(coefficients),
            'zero': sum(c == 0 for c in coefficients), 'minimum': str(min(coefficients)),
            'polynomial_sha256': digest(poly.dump()),
            'coefficient_sha256': digest(list(map(str, coefficients)))}

def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        pivots = [i for i in range(j, n) if a[i][j]]
        require(bool(pivots), 'nonzero Gaussian pivot')
        i = pivots[0]
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out

def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected

def pinching(theta):
    """Rational Frobenius projection of ww* to the symmetric commutant."""
    n = 8
    require(len(theta) == n and sum(theta) == 0, 'balanced definition control')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'original commutation constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)

def interval_add(a, b):
    return a[0]+b[0], a[1]+b[1]

def interval_mul(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)

def interval_poly(coefficients, box):
    out = F(0), F(0)
    for c in reversed(coefficients):
        out = interval_add(interval_mul(out, box), (F(c), F(c)))
    return out
X,H,U=[P({tuple(int(i==j) for j in range(3)):1}) for i in range(3)]
k,r=X,H


def mm(a,b):
    return [[sum((a[i][j]*b[j][h] for j in range(3)),P(0))
             for h in range(3)] for i in range(3)]

def madd(a,b):
    return [[a[i][j]+b[i][j] for j in range(3)] for i in range(3)]

def scale(a,c):
    return [[v*c for v in row] for row in a]

def trace(a):
    return sum((a[i][i] for i in range(3)), P(0))

def det(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def adj(a):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rows=[h for h in range(3) if h!=j]
            cols=[h for h in range(3) if h!=i]
            row.append((-1)**(i+j)*(a[rows[0]][cols[0]]*a[rows[1]][cols[1]]
                                     -a[rows[0]][cols[1]]*a[rows[1]][cols[0]]))
        out.append(row)
    return out

def exact_div(poly,divisor):
    """Exact lexicographic multivariate long division; check reconstruction."""
    divisor=P(divisor)
    if not divisor.t:
        raise ValueError('zero divisor')
    lead=max(divisor.t)
    q,out=P(0),P(poly)
    while out.t:
        e=max(out.t)
        if any(x<y for x,y in zip(e,lead)):
            raise ValueError('nonzero polynomial remainder')
        mon=P({tuple(x-y for x,y in zip(e,lead)):
               out.t[e]/divisor.t[lead]})
        q+=mon
        out-=mon*divisor
    if q*divisor!=poly:
        raise ValueError('division reconstruction')
    return q


def strict_certificate(name,poly,box):
    values,degrees=bernstein(poly,box)
    for value in values:
        require(value>0,name+' strict Bernstein sign')
    return {'name':name,'degrees':list(degrees),
            'box':[[str(a),str(b)] for a,b in box],
            'entries':len(values),'minimum':str(min(values)),
            'polynomial_sha256':digest(poly.dump()),
            'coefficients':list(map(str,values)),
            'coefficient_sha256':digest(list(map(str,values)))}


def oracle():
    # g(t)=t^4+a t^2-b t+c, Q=g'=4t^3+2a t-b.
    a,b,c=X,H,U
    eye=[[P(int(i==j)) for j in range(3)] for i in range(3)]
    m=[[P(0),P(0),b/4],[P(1),P(0),-a/2],[P(0),P(1),P(0)]]
    m2=mm(m,m)
    require(madd(madd(scale(mm(m2,m),4),scale(m,2*a)),scale(eye,-b))
            ==scale(eye,0),'companion cubic relation')
    y=madd(scale(m2,12),scale(eye,2*a))
    delta=-128*a**3-432*b*b
    require(det(y)==-delta/4,'resultant / discriminant identity')
    f=madd(madd(scale(m2,-2*a),scale(m,3*b)),scale(eye,-4*c))
    full=madd(madd(mm(m2,m2),scale(m2,a)),madd(scale(m,-b),scale(eye,c)))
    require(scale(full,-4)==f,'quartic quotient residue -4g')
    ad=adj(y)
    require(mm(y,ad)==scale(eye,-delta/4),'adjugate inverse identity')
    cleared=16*trace(mm(mm(f,f),mm(ad,ad)))
    pn=exact_div(cleared,delta)
    target=-16*a**5+128*a**3*c-36*a*a*b*b-768*a*c*c+864*b*b*c
    require(pn==target and cleared==delta*target,'complete trace cancellation')
    mu2,mu4=-4*a,4*a*a-8*c
    n=(122*mu2*mu2+224*mu4)*delta-5760*pn
    d=mu2*delta
    aa=-a
    psi0=aa**4-8*aa*aa*c+48*c*c
    require(8*aa*aa*pn-psi0*delta==144*b*b*(aa*aa+12*c)**2,
            'nonnegative pinching asymmetry penalty')
    base=532*aa**4+992*c*aa*aa-8640*c*c
    require(n*aa**3-base*d==-25920*b*b*(aa*aa+12*c)**2*mu2,
            'exact J restoration decomposition')
    require(532-992*H+25920*H*H==
            F(211616,405)+25920*(H-F(31,1620))**2,
            'uniform positive base derivative square')
    return n,d,pn,delta,mu2,mu4


def jn(r):
    return 532+3120*r-3464*r*r+3120*r**3+532*r**4


def jd(r):
    return (1+r)**3


def quartic(r):
    return 381-3292*r+3206*r*r+532*r**3+133*r**4


def value(poly,point):
    return scalar(poly,[*point,0])


def build():
    n,d,pn,delta,mu2,mu4=oracle()
    # Complete ordering chart: s=(3x-1)/2, v in [0,1].
    s,v=X,H
    x=(1+2*s)/3
    y=(1-x)/2+(3*x-1)*v/2
    z=1-x-y
    e2=x*y+x*z+y*z-1
    e3=x*y*z-x*y-x*z-y*z
    e4=-x*y*z
    require(-1+x+y+z==0,'whole ordered chart balance')
    require(1+e2+e4==(1-x)*(1-y)*(1-z),
            'saturation gives the nonnegative restoration parameter')
    require(e3==-(1-x)*(1-y)*(1-z),'e3=-t on the saturated chart')
    slopes=[P(-1)]*2+[x]*2+[y]*2+[z]*2
    require(sum((q*q for q in slopes),P(0))==-4*e2,'symbolic second moment')
    require(sum((q**4 for q in slopes),P(0))==4*e2*e2-8*e4,
            'symbolic fourth moment')
    g=(U+1)*(U-x)*(U-y)*(U-z)
    require(g==U**4+e2*U*U-e3*U+e4,'balanced quartic coefficients')
    q=4*U**3+2*e2*U-e3
    require(derivative(g*g,2)==2*g*q,'all active roots from H derivative')
    chart=[e2,e3,e4]
    nn,dd,pp,disc=[subst(poly,chart) for poly in (n,d,pn,delta)]
    dr=remove_monomial(disc,0,2,'only singular corner')
    unit=(F(0),F(1))
    discriminant=strict_certificate('discriminant_over_s_squared',dr,[unit]*3)
    require(discriminant['entries']==35 and F(discriminant['minimum'])==F(1024,9),
            'complete 35-coefficient discriminant certificate')
    require(subst(nn,[1,v,0])*jd(v*v)==subst(dd,[1,v,0])*jn(v*v),
            'whole centrally symmetric curve recovery')

    r,u=X,H
    require(derivative(jn(r),0)*(1+r)-3*jn(r)==4*quartic(r),
            'scalar stationary quartic')
    coefficients=[133,532,3206,-3292,381]
    require(sum(a*b<0 for a,b in zip(coefficients,coefficients[1:]))==2,
            'two positive-root Descartes variations')
    signs={str(q):value(quartic(r),(q,F(0)))
           for q in (F(0),F(1,8),F(7,50),F(3,4),F(1))}
    require(signs['0']>0 and signs['1/8']>0 and signs['7/50']<0
            and signs['3/4']<0 and signs['1']>0,
            'both positive critical roots have disjoint isolating intervals')
    require(value(jn(r),(F(1,8),F(0)))>600*(1+F(1,8))**3,
            'interior maximum beats both endpoints')
    require(jn(F(0))/jd(F(0))==532 and jn(F(1))/jd(F(1))==480,
            'scalar endpoints')
    diff=jn(r)*jd(u)-jn(u)*jd(r)
    hh=exact_div(diff+4*quartic(r)*(1+r)**2*(u-r),(u-r)**2)
    require(diff==(u-r)**2*hh-4*quartic(r)*(1+r)**2*(u-r),
            'critical divided difference multiply-back')
    curvature=strict_certificate('global_scalar_quadratic_loss',
        hh-100*jd(r)*jd(u),[(F(1,8),F(7,50)),unit,unit])
    require(curvature['entries']==24 and
            F(curvature['minimum'])==F(67837093119,78125000),
            'complete 24-coefficient curvature certificate')
    require(100*(F(1,27)+F(7,50))**2<600-532,
            'negative-product extension of scalar quadratic loss')

    controls=[]
    points=[(0,0),(0,1),(1,0),(1,1),(1,F(1,4)),(1,F(3,8)),
            (1,F(1,2)),(1,F(3,4)),(F(1,2),0),(F(1,2),1),
            (F(1,2),F(1,3)),(F(1,4),F(2,3)),
            (F(3,4),F(1,5)),(F(7,8),F(4,7))]
    for ss,vv in points:
        ss,vv=F(ss),F(vv)
        theta=[value(h,(ss,vv)) for h in slopes]
        require(sum(theta)==0 and max(map(abs,theta))==1,'definition control normalized')
        psi,rank=pinching(theta)
        m2,m4=sum(h*h for h in theta),sum(h**4 for h in theta)
        jj=(122*m2*m2+224*m4-5760*psi)/m2
        den=value(disc,(ss,vv))
        if den:
            require(den>0 and value(pp,(ss,vv))/den==psi,
                    'independent full compression versus cubic trace')
            require(value(nn,(ss,vv))/value(dd,(ss,vv))==jj,
                    'independent full compression versus J oracle')
        else:
            require(ss==0 and theta==[F(-1)]*2+[F(1,3)]*6,
                    'singular profile never divided')
            require(value(pp,(ss,vv))==0 and value(nn,(ss,vv))==0,
                    'singular cleared trace vanishing')
            require(psi==F(1,9) and jj==F(2336,9),'definition at the unique singular profile')
        cc=value(e4,(ss,vv))
        tt=-value(e3,(ss,vv))
        require(jn(cc)/jd(cc)-jj>=F(211616,405)*tt,
                'global product-preserving restoration control, including singularity')
        controls.append({'s':str(ss),'v':str(vv),'theta':list(map(str,theta)),
                         'Psi':str(psi),'J':str(jj),'commutant_rank':rank,
                         'generic':bool(den)})

    lo,hi=F(1,8),F(7,50)
    for _ in range(40):
        mid=(lo+hi)/2
        if value(quartic(r),(mid,F(0)))>0:
            lo=mid
        else:
            hi=mid
    require(value(quartic(r),(lo,F(0)))>0 and value(quartic(r),(hi,F(0)))<0,
            'exact root bracket after 40 rational bisections')
    ni=interval_poly([532,3120,-3464,3120,532],(lo,hi))
    require(ni[0]>0,'positive scalar numerator enclosure')
    ji=(ni[0]/(1+hi)**3,ni[1]/(1+lo)**3)
    bi=(F(106496,5)/ji[1],F(106496,5)/ji[0])
    require(F('614.123304860')<ji[0]<=ji[1]<F('614.123304861'),
            'displayed rigorous optimal J bounds')
    require(F('34.682285839')<bi[0]<=bi[1]<F('34.682285840'),
            'displayed rigorous original-root basin bounds')
    require(F('614.123304861')<615<F(5472,7),
            'strict cohort exclusion relative to the credited 3+3+1+1 value')
    require(F(13,8)**4/F(10985,33554432)==F(106496,5),
            'credited displacement normalization')
    return {'author':'six-sendov-2','role':'researcher',
            'claim':'whole balanced 2+2+2+2 angular optimizer and paired-phase displacement basin',
            'proof_status':'ordinary author proof plus exact certificate; independent review pending',
            'oracle':{'Psi_numerator':pn.dump(),'discriminant':delta.dump()},
            'certificates':[discriminant,curvature],
            'new_bernstein_entries':59,'full_compression_controls':controls,
            'quartic_signs':{q:str(t) for q,t in signs.items()},
            'root_interval':[str(lo),str(hi)],'J_interval':list(map(str,ji)),
            'basin_interval':list(map(str,bi)),'checks':CHECKS}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,
                        default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',action='store_true',
                        help='author regeneration only; never needed for verification')
    args=parser.parse_args()
    if not args.write_manifest and not args.manifest.is_file():
        raise ValueError('required manifest is absent')
    result=build()
    if args.write_manifest:
        args.manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        require(result==json.loads(args.manifest.read_text()),'complete manifest equality')
    print(json.dumps({'status':'PASS','checks':CHECKS,
                      'new_bernstein_entries':result['new_bernstein_entries'],
                      'full_compression_controls':len(result['full_compression_controls']),
                      'canonical_record_sha256':digest(result)},sort_keys=True))


if __name__=='__main__':
    main()
