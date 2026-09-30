#!/usr/bin/env python3
"""Exact author certificate for all balanced degree-nine 3+3+1+1 directions.

Author six-sendov-2, researcher. The sparse Q[x0,x1,x2] and rational
commutant kernel openly adapts the author's real-displacement checker.
The new cubic trace is derived here. Standard library only: no campaign
import, external CAS, floating proof input or solver. Analytic and
spectral interpretation is in PROOF.md; independent review pending.
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

def angular_oracle():
    # Q(l)=4l^3-7kl^2+(3k^2-3r-1)l+k.
    c0,c1,c2=k/4,(3*k*k-3*r-1)/4,-7*k/4
    m=[[P(0),P(0),-c0],[P(1),P(0),-c1],[P(0),P(1),-c2]]
    eye=[[P(int(i==j)) for j in range(3)] for i in range(3)]
    m2=mm(m,m)
    qprime=madd(madd(scale(m2,12),scale(m,-14*k)),scale(eye,3*k*k-3*r-1))
    delta=det(qprime)
    disc=((-7*k)**2*(3*k*k-3*r-1)**2-16*(3*k*k-3*r-1)**3
          -4*(-7*k)**3*k-432*k*k+72*(-7*k)*(3*k*k-3*r-1)*k)
    if delta*4!=-disc:
        raise ValueError('resultant / discriminant identity')
    aa=3*k*k+4*r+12
    bb=3*k*(k*k-r+9)
    cc=16*r-15*k*k
    f=madd(madd(scale(m2,-aa),scale(m,bb)),scale(eye,cc))
    # F(l)=(l^2-1)((l-k)^2-r) reduces to f(l)/16.
    full=madd(madd(mm(m2,m2),scale(mm(m2,m),-2*k)),
               madd(scale(m2,k*k-r-1),madd(scale(m,2*k),scale(eye,r-k*k))))
    if scale(full,16)!=f:
        raise ValueError('quartic quotient remainder')
    ad=adj(qprime)
    if mm(qprime,ad)!=scale(eye,delta):
        raise ValueError('adjugate identity')
    n0=trace(mm(mm(f,f),mm(ad,ad)))
    psi_num=exact_div(n0,disc)
    # Psi=psi_num/disc for the canonical half-separation=1 vector.
    m2theta=aa/2
    m4theta=6+F(9,4)*k*k+F(21,32)*k**4+F(27,4)*k*k*r+2*r*r
    nn=(122*m2theta*m2theta+224*m4theta)*disc-5760*psi_num
    dd=m2theta*disc*(1+k/4)**2
    # Check reflection evenness of the canonical J, before max normalization.
    if subst(psi_num,[-k,r,U])!=psi_num or subst(disc,[-k,r,U])!=disc:
        raise ValueError('reflection parity')
    return nn,dd,psi_num,disc,m2theta,m4theta

def homogenize(poly,degree,d,t,v):
    out=P(0)
    for (i,j,h),c in poly.t.items():
        if h or degree<i+2*j:
            raise ValueError('homogeneous reconstruction degree')
        out+=c*(4*t)**i*v**(2*j)*d**(degree-i-2*j)
    return out

def singleton_oracle():
    _,_,ps,disc,_,_=angular_oracle()
    t,d=k,r
    v=1-3*t
    delta=homogenize(disc,6,d,t,v)
    pn=homogenize(ps,10,d,t,v)
    mu2=6*d*d+24*t*t+2*v*v
    mu4=6*d**4+36*d*d*t*t+168*t**4+108*t*t*v*v+2*v**4
    nn=(122*mu2*mu2+224*mu4)*delta-5760*pn
    dd=mu2*delta
    return nn,dd,pn,delta
def cover_check(boxes,full,name):
    # Check every open cell cut out by all rectangle boundaries, plus area.
    require(all(len(b)==3 and b[2]==(F(0),F(1)) for b in boxes),
            name+' dummy axis')
    axes=[sorted({x for box in boxes for x in box[i]}|
                 {full[i][0],full[i][1]}) for i in range(2)]
    for box in boxes:
        require(all(full[i][0]<=box[i][0]<box[i][1]<=full[i][1]
                    for i in range(2)),name+' box containment')
    for i in range(len(axes[0])-1):
        for j in range(len(axes[1])-1):
            mid=((axes[0][i]+axes[0][i+1])/2,
                 (axes[1][j]+axes[1][j+1])/2)
            require(sum(all(b[h][0]<mid[h]<b[h][1] for h in range(2))
                        for b in boxes)==1,name+' coverage/disjoint interiors')
    area=sum((b[0][1]-b[0][0])*(b[1][1]-b[1][0]) for b in boxes)
    require(area==(full[0][1]-full[0][0])*(full[1][1]-full[1][0]),
            name+' total area')


def control(theta,psi_num,disc,n,d,point,label):
    require(len(theta)==8 and sum(theta)==0,label+' balance')
    psi,rank=pinching(theta)
    mu2=sum(v*v for v in theta)
    mu4=sum(v**4 for v in theta)
    max2=max(v*v for v in theta)
    jj=(122*mu2*mu2+224*mu4-5760*psi)/mu2/max2
    den=scalar(disc,point)
    if den:
        require(den>0 and scalar(psi_num,point)/den==psi,
                label+' grouped definition versus cubic trace')
        require(scalar(n,point)/scalar(d,point)==jj,
                label+' max-normalized objective')
    else:
        require(scalar(psi_num,point)==0 and scalar(n,point)==0,
                label+' singular formulas never divided')
    return {'label':label,'parameters':list(map(str,point[:2])),
            'theta':list(map(str,theta)),'Psi':str(psi),'J':str(jj),
            'commutant_rank':rank,'generic':bool(den)}


def build():
    records=[]
    n,d,pn,disc,mu2,mu4=angular_oracle()
    require(disc==(k*k-1)**2*(9*k*k+16)+144*r+
            r*(87*k*k+414*k**4+432*r+432*r*r+855*k*k*(1-r)),
            'positive discriminant decomposition on r<=1')
    # Differentiate the shifted degree-eight root polynomial exactly.
    hp=(U*U-1)**3*((U-k)**2-r)
    q=4*U**3-7*k*U*U+(3*k*k-3*r-1)*U+k
    require(derivative(hp,2)==2*(U*U-1)**2*q,
            'three active compression roots via H derivative')
    theta=[1-k/4]*3+[-1-k/4]*3+[3*k/4+U,3*k/4-U]
    require(sum(theta,P(0))==0,'symbolic canonical balance')
    require(sum((t*t for t in theta),P(0))==subst(mu2,[k,U*U,U]),
            'symbolic second moment')
    require(sum((t**4 for t in theta),P(0))==subst(mu4,[k,U*U,U]),
            'symbolic fourth moment')
    jn=2058+21912*r-15876*r*r+19224*r**3+3402*r**4
    jd=(3+r)*(1+3*r)**2
    n0,d0=subst(n,[0,r,U]),subst(d,[0,r,U])
    require(n0*jd==d0*jn,'whole credited symmetric curve recovery')
    nk,dk=subst(derivative(n,0),[0,r,U]),subst(derivative(d,0),[0,r,U])
    require(2*(nk*d0-n0*dk)*jd+jn*d0*d0==0,
            'exact one-sided boundary derivative -j(r)/2')
    comp=remove_monomial(jn*d-jd*n,0,1,'cap k')
    unit=(F(0),F(1))
    records.append(certificate('majority_cap',comp,
                               [(F(0),F(1,4)),(F(0),F(1,4)),unit],True))
    require(F(records[-1]['minimum'])==98784,'cap coefficient minimum')
    require(F(343,4)+F(942,64)+F(414,1024)+F(9,4096)<102,
            'cap discriminant upper bound')
    require(F(211,32)<7 and F(289,256)<F(8,7) and F(637,64)<10,
            'cap moment/normalizer/scalar denominator bounds')
    require(7*102*F(8,7)==816 and 98784>12*816*10,
            'quantitative j(r)-J >=12k')
    outside=subst(780*d-n,[2*k,(1-k)**2*r,0])
    boxes=[
        [(F(1,2),F(1)),unit,unit],
        [(F(1,32),F(1,2)),(F(1,2),F(1)),unit],
        [(F(17,64),F(1,2)),(F(0),F(1,2)),unit],
        [(F(1,32),F(17,64)),(F(1,4),F(1,2)),unit],
        [(F(19,128),F(17,64)),(F(0),F(1,4)),unit],
        [(F(1,32),F(19,128)),(F(0),F(1,8)),unit],
        [(F(1,32),F(19,128)),(F(1,8),F(1,4)),unit],
    ]
    cover_check(boxes,[(F(1,32),F(1)),unit,unit],'majority exterior')
    for i,box in enumerate(boxes):
        records.append(certificate(f'majority_exterior_{i}',outside,box))
    records.append(certificate('majority_large_r',780*d-n,
                               [(F(0),F(1,16)),(F(1,4),F(1)),unit],True))
    sn,sd,sp,sdisc=singleton_oracle()
    ts,ds=k,r
    st=[ds-ts]*3+[-ds-ts]*3+[P(1),6*ts-1]
    require(sum(st,P(0))==0,'singleton symbolic balance')
    require(sum((t*t for t in st),P(0))==
            6*ds*ds+24*ts*ts+2*(1-3*ts)**2,'singleton second moment')
    singleton_gap=subst(780*sd-sn,[k,(1-k)*r,0])
    sb=[[(F(0),F(1,7)),unit,unit],[(F(1,7),F(1,3)),unit,unit]]
    cover_check(sb,[(F(0),F(1,3)),unit,unit],'singleton')
    for i,box in enumerate(sb):
        records.append(certificate(f'singleton_{i}',singleton_gap,box))
    require(sum(row['entries'] for row in records)==860,
            'complete new certificate entry count')
    # Credited one-variable loss, reproduced as a small exact check.
    tp=derivative(jn,1)*jd-jn*derivative(jd,1)
    tc=[26634,-231084,-907290,376920,971190,224532,30618]
    require(tp==sum((c*r**i for i,c in enumerate(tc)),P(0)),
            'credited scalar derivative polynomial')
    records.append(certificate('credited_scalar_derivative_loss',
        -(derivative(tp,1)+90000),[unit,(F(0),F(1,4)),unit],True))
    require(F(637,64)<10 and F(90000,100)==900,
            'credited 450 squared scalar loss')
    require(scalar(jn,[0,F(1,9),0])/scalar(jd,[0,F(1,9),0])==F(5472,7),
            'credited rational competitor')
    require(F(5472,7)-780==F(12,7),'global losing-region gap')
    require(F(4,3)/F(2,25)==F(50,3) and F(50,3)/450==F(1,27),
            'cap normalized direction loss')
    require(F(1,16)/12<F(1,27) and F(7,6)*F(12,7)==2,
            'global direction-to-orbit coefficient')
    require(F(13,8)**4/F(10985,33554432)==F(106496,5),
            'restricted basin scale identity')
    controls=[]
    cases=[(F(0),F(1,3)),(F(1,4),F(1,3)),(F(1,2),F(1,4)),
           (F(1),F(1,3)),(F(3,2),F(1,8)),(F(2),F(0)),
           (F(1,3),F(0)),(F(0),F(0)),(F(0),F(1)),
           (F(1),F(0)),(F(1,4),F(2,3))]
    for i,(kv,v) in enumerate(cases):
        theta=[1-kv/4]*3+[-1-kv/4]*3+[3*kv/4+v,3*kv/4-v]
        require(0<=kv<=2 and 0<=v<=1-kv/2,'majority control domain')
        controls.append(control(theta,pn,disc,n,d,[kv,v*v,0],f'majority_{i}'))
    require(F(controls[9]['J'])==F(8096,25) and
            F(controls[9]['Psi'])==F(225,256),'five/three collision control')
    require(F(controls[0]['J'])==F(5472,7) and
            F(controls[0]['Psi'])==F(17,81),'known symmetric rational control')
    for i,(tv,dv) in enumerate([
            (F(0),F(1)),(F(0),F(1,2)),(F(1,3),F(0)),
            (F(1,7),F(0)),(F(1,4),F(1,2)),(F(1,8),F(0))]):
        theta=[dv-tv]*3+[-dv-tv]*3+[F(1),6*tv-1]
        require(0<=tv<=F(1,3) and 0<=dv<=1-tv,'singleton control domain')
        controls.append(control(theta,sp,sdisc,sn,sd,[tv,dv,0],f'singleton_{i}'))
    require(F(controls[14]['J'])==F(1632,7) and
            F(controls[14]['Psi'])==F(1,49),'singleton/seven collision control')
    # A precise failed shortcut, not a polynomial counterexample.
    kv,v=F(1,4),F(2,3)
    rr=v*v
    ja=F(controls[10]['J'])
    js=scalar(jn,[0,rr,0])/scalar(jd,[0,rr,0])
    difference=ja-js
    require(js==F(848970,1519) and
            difference==F(101512976116319958,21297992197237903) and
            difference>0,'global fixed-r comparison obstruction')
    lo,hi=F(2,25),F(9,100)
    require(scalar(tp,[0,lo,0])>0 and scalar(tp,[0,hi,0])<0,
            'credited optimizer initial bracket')
    for _ in range(40):
        mid=(lo+hi)/2
        if scalar(tp,[0,mid,0])>0:lo=mid
        else:hi=mid
    require(scalar(tp,[0,lo,0])>0 and scalar(tp,[0,hi,0])<0,
            'credited optimizer final bracket')
    ni=interval_poly([2058,21912,-15876,19224,3402],(lo,hi))
    di=interval_poly([3,19,33,9],(lo,hi))
    require(ni[0]>0 and di[0]>0,'positive interval division')
    basin=F(106496,5)*di[0]/ni[1],F(106496,5)*di[1]/ni[0]
    require(F('27.106707')<basin[0]<basin[1]<F('27.106708'),
            'credited basin value interval')
    return {'agent':'six-sendov-2','role':'researcher',
            'status':'exact author certificate; analytic premises explicit; independent review pending',
            'checks':CHECKS,'new_Bernstein_coefficients':860,
            'total_Bernstein_coefficients':866,'new_certificate_boxes':11,
            'certificates':records,'coefficient_manifest_sha256':digest(records),
            'oracle_polynomial_sha256':{name:digest(poly.dump()) for name,poly in
                [('N',n),('D',d),('Psi_numerator',pn),('discriminant',disc),
                 ('singleton_N',sn),('singleton_D',sd)]},
            'Psi_numerator':pn.dump(),'discriminant':disc.dump(),
            'controls':controls,'optimizer_interval':list(map(str,(lo,hi))),
            'basin_interval':list(map(str,basin)),
            'failed_global_comparison':{'k':str(kv),'v':str(v),'r':str(rr),
                 'J':str(ja),'j(r)':str(js),'difference':str(difference)}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',type=Path)
    args=parser.parse_args()
    actual=build()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(actual,indent=2)+'\n')
    else:
        expected=json.loads(args.expected.read_text())
        if expected!=actual:raise ValueError('complete expected manifest mismatch')
    print(json.dumps({'agent':actual['agent'],'role':actual['role'],
                      'checks':actual['checks'],'new_Bernstein_coefficients':860,
                      'total_Bernstein_coefficients':866,'new_certificate_boxes':11,
                      'definition_controls':len(actual['controls']),
                      'coefficient_manifest_sha256':actual['coefficient_manifest_sha256'],
                      'manifest_match':not bool(args.write_expected)},indent=2))


if __name__=='__main__':
    main()
