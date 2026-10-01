#!/usr/bin/env python3
"""six-reviewer-3: independent radial-sixfold and complex-polar audit."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from math import comb, gcd, lcm, prod
from pathlib import Path
import hashlib
import json
import time


class Failure(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Failure(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


class P:
    """Four-variable integer coefficients with a reduced common denominator."""
    def __init__(self, coeff=None, denominator=1):
        need(isinstance(denominator, int) and denominator > 0, 'positive integer denominator')
        need(all(isinstance(v, int) for v in (coeff or {}).values()), 'integer coefficients')
        coeff = {e: v for e, v in (coeff or {}).items() if v}
        need(all(len(e) == 4 and all(isinstance(k, int) and k >= 0 for k in e)
                 for e in coeff), 'nonnegative four-variable powers')
        g = denominator
        for v in coeff.values():
            g = gcd(g, abs(v))
        self.c = {e: v//g for e, v in coeff.items()}
        self.d = denominator//g

    def __add__(self, other):
        other = scalar(other) if not isinstance(other, P) else other
        den = lcm(self.d, other.d)
        out = defaultdict(int)
        for e, v in self.c.items():
            out[e] += v*(den//self.d)
        for e, v in other.c.items():
            out[e] += v*(den//other.d)
        return P(out, den)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -v for e, v in self.c.items()}, self.d)

    def __sub__(self, other):
        return self + -(scalar(other) if not isinstance(other, P) else other)

    def __rsub__(self, other):
        return scalar(other) + -self

    def __mul__(self, other):
        other = scalar(other) if not isinstance(other, P) else other
        out = defaultdict(int)
        for e, v in self.c.items():
            for f, w in other.c.items():
                out[(e[0]+f[0], e[1]+f[1], e[2]+f[2], e[3]+f[3])] += v*w
        return P(out, self.d*other.d)

    __rmul__ = __mul__

    def __pow__(self, n):
        need(isinstance(n, int) and n >= 0, 'nonnegative polynomial power')
        out, base = scalar(1), self
        while n:
            if n % 2:
                out = out*base
            n //= 2
            if n:
                base = base*base
        return out

    def __eq__(self, other):
        return isinstance(other, P) and self.d == other.d and self.c == other.c

    def degrees(self):
        return tuple(max((e[j] for e in self.c), default=0) for j in range(4))

    def evaluate(self, values):
        need(len(values) == 4, 'four evaluation coordinates')
        values = list(map(Q, values))
        degrees = self.degrees()
        powers = [[v.numerator**k*v.denominator**(n-k) for k in range(n+1)]
                  for v, n in zip(values, degrees)]
        den = self.d*prod(v.denominator**n for v, n in zip(values, degrees))
        return Q(sum(c*prod(powers[j][e[j]] for j in range(4))
                     for e, c in self.c.items()), den)

    def canonical(self):
        return [[list(e), str(Q(c, self.d))] for e, c in sorted(self.c.items())]


def scalar(x):
    x = Q(x)
    return P({(0, 0, 0, 0): x.numerator}, x.denominator)


def variable(i):
    e = [0]*4
    e[i] = 1
    return P({tuple(e): 1})


def integrate(p, axis):
    need(0 <= axis < 4, 'integration axis')
    norm = lcm(*(e[axis]+1 for e in p.c))
    out = defaultdict(int)
    for e, v in p.c.items():
        f = list(e)
        f[axis] = 0
        out[tuple(f)] += v*(norm//(e[axis]+1))
    return P(out, p.d*norm)


def affine(p, axis, lo, hi):
    lo, span = Q(lo), Q(hi)-Q(lo)
    need(span > 0, 'positive affine interval')
    n = p.degrees()[axis]
    den = lcm(lo.denominator, span.denominator)
    u, v = int(lo*den), int(span*den)
    weights = [[comb(k,j)*u**(k-j)*v**j*den**(n-k)
                for j in range(k+1)] for k in range(n+1)]
    out = defaultdict(int)
    for e, c in p.c.items():
        for j, w in enumerate(weights[e[axis]]):
            if w:
                f = list(e)
                f[axis] = j
                out[tuple(f)] += c*w
    return P(out, p.d*den**n)


def tensor(p, degrees=None):
    """Power-to-Bernstein transform by repeated adjacent Pascal additions."""
    degrees = p.degrees() if degrees is None else tuple(degrees)
    need(all(x <= y for x,y in zip(p.degrees(), degrees)), 'tensor covers every power')
    shape = tuple(n+1 for n in degrees)
    strides = tuple(prod(shape[j+1:]) for j in range(4))
    data = [0]*prod(shape)
    for e, c in p.c.items():
        data[sum(e[j]*strides[j] for j in range(4))] = c
    den = p.d
    for axis, n in enumerate(degrees):
        norm = lcm(*(comb(n,k) for k in range(n+1)))
        step, block = strides[axis], strides[axis]*(n+1)
        for outer in range(0, len(data), block):
            for inner in range(step):
                offset = outer+inner
                line = [data[offset+k*step]*(norm//comb(n,k)) for k in range(n+1)]
                for level in range(1,n+1):
                    for j in range(n,level-1,-1):
                        line[j] += line[j-1]
                for k,v in enumerate(line):
                    data[offset+k*step] = v
        den *= norm
    return data, den, degrees


def invert(data, den, degrees):
    """Undo the Pascal additions by exact adjacent subtraction."""
    data = list(data)
    shape = tuple(n+1 for n in degrees)
    strides = tuple(prod(shape[j+1:]) for j in range(4))
    need(len(data) == prod(shape), 'inverse tensor size')
    for axis in range(3,-1,-1):
        n, step = degrees[axis], strides[axis]
        block = step*(n+1)
        for outer in range(0,len(data),block):
            for inner in range(step):
                offset = outer+inner
                line = [data[offset+k*step] for k in range(n+1)]
                for level in range(n,0,-1):
                    for j in range(level,n+1):
                        line[j] -= line[j-1]
                for k,v in enumerate(line):
                    data[offset+k*step] = v*comb(n,k)
    return P({tuple((i//strides[j])%shape[j] for j in range(4)):v
              for i,v in enumerate(data) if v},den)


def summarize_tensor(p, degrees, label):
    values, den, got = tensor(p, degrees)
    need(invert(values, den, got) == p, 'complete Pascal inverse '+label)
    need(min(values) >= 0, 'negative complete coefficient '+label)
    indices = list(product(*(range(n+1) for n in got)))
    zeros = [list(e) for e,v in zip(indices,values) if not v]
    return {'degrees':list(got), 'coefficients':len(values),
            'minimum':str(Q(min(values),den)),
            'minimum_positive':str(Q(min(v for v in values if v > 0),den)),
            'zeros':len(zeros), 'zero_indices':zeros,
            'zero_indices_sha256':digest(zeros),
            'sha256':digest([str(Q(v,den)) for v in values])}


def radial_targets():
    b, x, y, z = [variable(j) for j in range(4)]
    D = 1+b
    Rn = 1+Q(4,3)*b*x
    Sn = 1+4*b*(1-x)*y
    Tn = 1+8*b*(1-x)-4*b*(1-x)*y
    need(6*Rn+Sn+Tn == 8*D, 'entire normalized radial budget')
    # Direct cleared moments on the cube: Wk = D^6 * Mk / b^k.
    W = [sum(9*Q((-1)**j*comb(6,j),j+k+1)*b**j*Rn**j*D**(6-j)
             for j in range(7)) for k in range(3)]
    T = D**2-(1-b**2)*Sn**2
    T = T+(2*b*Sn*D-T)*z
    PA = D**2*W[0]**2 + Sn**2*b**2*W[1]**2-W[0]*W[1]*T
    PJ = D**2*b**2*W[1]**2+Sn**2*b**4*W[2]**2-b**2*W[1]*W[2]*T
    RR = Rn**12*Sn**2*Tn**2
    L = D**2*PA+Tn**2*PJ-RR
    # Alternative discriminant factorization, instead of squaring L.
    F = (D**2*PA-Tn**2*PJ-RR)**2-4*RR*Tn**2*PJ
    PA1 = (D*W[0]-Sn*b*W[1])**2
    PJ1 = (D*b*W[1]-Sn*b**2*W[2])**2
    H = D**2*PA1+Tn**2*PJ1-Q(9,8)*RR
    need(H.degrees() == (32,16,4,0) and F.degrees() == (64,32,8,2),
         'complete cleared polynomial degrees')
    return {'H':H, 'disk':F}, (W, L, RR)


def radial_signs(targets, full_evidence=None):
    cells = [(Q(0),Q(3,4)),(Q(3,4),Q(1))]
    need(cells[0][0] == 0 and cells[0][1] == cells[1][0] and cells[1][1] == 1,
         'closed full cube coverage')
    rows = []
    for cell,(lo,hi) in enumerate(cells):
        for label,p in targets.items():
            cp = affine(p,1,lo,hi)
            record = summarize_tensor(cp,p.degrees(),str(cell)+label)
            if full_evidence is not None:
                values,den,g = tensor(cp,p.degrees())
                full_evidence.append({'cell':cell,'target':label,
                                      'values':[str(Q(v,den)) for v in values]})
            record.update(cell=cell,target=label,alpha=[str(lo),str(hi)])
            if label == 'H':
                need(record['minimum'] == '639/8' and not record['zeros'],
                     'strict entire first-sign tensor')
            else:
                expected = {(64,i,j,2) for i in ([31,32] if cell == 0 else [0,1])
                            for j in (7,8)}
                if cell == 0:
                    expected |= {(64,0,0,k) for k in range(3)}
                need({tuple(e) for e in record['zero_indices']} == expected,
                     'all and only equality zeros')
            rows.append(record)
    need(sum(r['coefficients'] for r in rows) == 121440,'entire origin tensor inventory')
    return rows


def polar(full_evidence=None):
    a, v, theta, tau = [variable(j) for j in range(4)]
    eps, D = 1-a, 1-a**2
    Rn, Sn = 1+Q(4,3)*a*v, 1+8*a*(1-v)
    r = Rn
    # Squared moduli after D/(1+a)=1-a, including the full light variance cap.
    X = a**2+(2*a*eps*r-Q(8,3)*a*eps**2*(1+a)*theta)*tau+eps**2*r**2*tau**2
    Y = 2*a**2+(2*a*eps*(1+Sn)-16*a*eps**2*(1+a)*(1-theta))*tau \
        +eps**2*(1+Sn**2)*tau**2
    I = integrate(X**3*Y*Q(1,2),3)
    deficit = 1-I
    # Taylor expansion at a=1 makes exact division transparent.
    shifted = affine(deficit,0,1,2)
    need(all(e[0] >= 2 for e in shifted.c),'polar deficit has exact double zero')
    quotient_shifted = P({(e[0]-2,e[1],e[2],e[3]):c
                          for e,c in shifted.c.items()},shifted.d)
    # Substitute h=a-1 by a full coefficient translation.
    quotient = affine(quotient_shifted,0,-1,0)
    need((1-a)**2*quotient == deficit,'complete polar quotient identity')
    record = summarize_tensor(quotient,(14,8,4,0),'polar')
    if full_evidence is not None:
        values,den,g = tensor(quotient,(14,8,4,0))
        full_evidence.append({'target':'polar','values':[str(Q(v,den)) for v in values]})
    need(record['minimum'] == '8/9' and not record['zeros'],'polar entire strict signs')
    record.update(power_sha256=digest(quotient.canonical()),
                  integral_monomials=len(I.c),quotient_monomials=len(quotient.c))
    return record,I


def integrated_gap():
    a, tau = variable(0), variable(3)
    heavy = a+(1-a)*(1+Q(4,3)*a)*tau
    light = a+(1-a)*(1+8*a)*tau
    J = integrate(tau*heavy**4*light**2,3)
    # Fixed bounded rational cells certify a convenient uniform derivative cap.
    cells = []
    limit = Q(5)
    for k in range(16):
        lo,hi = Q(k,16),Q(k+1,16)
        record = summarize_tensor(affine(limit-J,0,lo,hi),(12,0,0,0),'integrated-gap-'+str(k))
        cells.append({'interval':[str(lo),str(hi)],'minimum':record['minimum'],
                      'sha256':record['sha256']})
    need(all(Q(r['minimum']) > 0 for r in cells),'strict uniform integral cap')
    need(J.evaluate([0,0,0,0]) == Q(1,8) and J.evaluate([1,0,0,0]) == Q(1,2),
         'integrated endpoint values')
    return {'J_power':[str(Q(J.c.get((k,0,0,0),0),J.d)) for k in range(13)],
            'J_half':str(J.evaluate([Q(1,2),0,0,0])),
            'uniform_J_cap':str(limit),'uniform_gamma':str(1/(9*limit)),
            'cells':cells,'coefficients':208,'pointwise_gamma':'1/(9*J(a))'}


def gaussian_mul(u,v):
    return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0])


def gaussian_integral(factors,offset,slope,weight=Q(1)):
    coefficients=[(Q(1),Q(0))]
    for u in factors:
        out=[(Q(0),Q(0))]*(len(coefficients)+1)
        for j,c in enumerate(coefficients):
            out[j]=(out[j][0]+offset*c[0],out[j][1]+offset*c[1])
            d=gaussian_mul(c,u)
            out[j+1]=(out[j+1][0]+slope*d[0],out[j+1][1]+slope*d[1])
        coefficients=out
    return tuple(weight*sum(c[k]/(j+1) for j,c in enumerate(coefficients)) for k in range(2))


def norm(u):
    return sum(x*x for x in u)


def nonreal_example():
    a=Q(19,20)
    d=(Q(0),Q(1,40))
    e=(Q(1,50),Q(1,25))
    de=gaussian_mul(d,e)
    c8=tuple(-Q(9,8)*(u+v) for u,v in zip(d,e))
    c7=tuple(Q(9,7)*v for v in de)
    need(tuple(8*v for v in c8)==tuple(-9*(u+v) for u,v in zip(d,e))
         and tuple(7*v for v in c7)==tuple(9*v for v in de),
         'complete derivative coefficients')
    constant=tuple(-v for v in (a**9+c8[0]*a**8+c7[0]*a**7,
                                c8[1]*a**8+c7[1]*a**7))
    bound=sum(abs(v) for v in c8+c7+constant)
    need(bound==Q(217919198409239,286720000000000)<1,'exact nonreal Rouche bound')
    need(c8[1]!=0 and d!=e and d!=(e[0],-e[1]),'genuinely nonreal unrelated light points')
    derivative=(9*a**8+8*c8[0]*a**7+7*c7[0]*a**6,
                8*c8[1]*a**7+7*c7[1]*a**6)
    direct=gaussian_mul((a-d[0],-d[1]),(a-e[0],-e[1]))
    need(derivative==tuple(9*a**6*v for v in direct) and norm(derivative)>0,
         'marked root simple and derivative factorization control')
    need(6/a+2/(1+a)<8,'nontrivial example beyond radius-only lower bound')
    return {'marked_root':str(a),'c8':list(map(str,c8)),'c7':list(map(str,c7)),
            'constant':list(map(str,constant)),'Rouche_L1_bound':str(bound)}


def convolution(u,v):
    out=[Q(0)]*(len(u)+len(v)-1)
    for i,x in enumerate(u):
        for j,y in enumerate(v):
            out[i+j]+=x*y
    return out


def polar_envelope(a,radii,projections):
    D=1-a*a
    X,Y,Z=[[a*a,2*a*D*x,D*D*r*r] for r,x in zip(radii,projections)]
    integrand=convolution(convolution(convolution(X,X),X),[x+y for x,y in zip(Y,Z)])
    return sum(v/Q(2*(j+1)) for j,v in enumerate(integrand))


def polar_controls(I,gap):
    rows=[];low=high=0
    patterns=[[(Q(1),Q(0))]*3,
              [(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13)),(Q(5,13),Q(-12,13))]]
    for a,v,split,amount in product((Q(1,4),Q(1,2),Q(3,4)),
                                    (Q(0),Q(1,2),Q(1)),(Q(0),Q(1,3),Q(1)),(Q(1,2),Q(1))):
        D=1-a*a;eps=1-a;floor=1/(1+a)
        r=(1+Q(4,3)*a*v)/(1+a)
        total=(2+8*a*(1-v))/(1+a)
        s=floor+(total-2*floor)*split;t=total-s
        saturated=[r,s,t]
        need(6*r+s+t==8 and min(saturated)>=floor,'physical saturated radial budget')
        radii=[floor+amount*(x-floor) for x in saturated]
        for units in patterns:
            complex_points=[(x*u[0],x*u[1]) for x,u in zip(radii,units)]
            original=[x[0] for x in complex_points]
            xi=(6*original[0]+original[1]+original[2])/8
            before=polar_envelope(a,radii,original)
            saturated_before=polar_envelope(a,saturated,original)
            need(before<=saturated_before,'radius-only envelope monotonicity')
            after_projection=original.copy()
            required=8*(a-xi)
            for k,weight in enumerate([6,1,1]):
                if required>=0:
                    change=min(required/weight,saturated[k]-after_projection[k])
                else:
                    change=-min(-required/weight,after_projection[k]+saturated[k])
                after_projection[k]+=change;required-=weight*change
            need(required==0 and 6*after_projection[0]+after_projection[1]+after_projection[2]==8*a,
                 'full coordinate path reaches mean')
            need(all(abs(x)<=r for x,r in zip(after_projection,saturated)),
                 'entire coordinate path remains in radius intervals')
            theta=6*(r-after_projection[0])/(8*eps)
            need(0<=theta<=1,'endpoint defect coordinate')
            after=polar_envelope(a,saturated,after_projection)
            upper=I.evaluate([a,v,theta,0])
            need(0<=after<=upper<=1-Q(8,9)*eps**2,'exact endpoint envelope and variance bound')
            jj=sum(Q(c)*a**k for k,c in enumerate(gap['J_power']))
            if xi<=a:
                low+=1;need(saturated_before<=after,'projection-increase envelope monotonicity')
            else:
                high+=1
                need(saturated_before-after<=8*a*D*jj*(xi-a),'improved integrated derivative bound')
            ii=gaussian_integral([complex_points[0]]*6+complex_points[1:],a,D)
            need(norm(ii)<=before**2,'literal polar integral versus triangle envelope')
            rows.append(list(map(str,[a,v,split,amount,xi,before,after,upper,*ii])))
    need(low>0 and high>0 and len(rows)==108,'both mean directions and all physical controls')
    return {'controls':len(rows),'low_mean':low,'high_mean':high,'sha256':digest(rows),
            'new_integrated_derivative_bound_checked':True}


def controls(targets,W):
    units=[(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(5,13),Q(-12,13))]
    rows=[]
    for b,x,y in product((Q(1,4),Q(1,2),Q(1)),(Q(0),Q(3,4),Q(1)),(Q(0),Q(2,3),Q(1))):
        r=(1+Q(4,3)*b*x)/(1+b)
        s=(1+4*b*(1-x)*y)/(1+b)
        t=8-6*r-s
        floor=(1-(1-b*b)*s*s)/(2*b*s)
        moments=[b**k*w.evaluate([b,x,y,0])/(1+b)**6 for k,w in enumerate(W)]
        need(all(v>0 for v in moments),'positive original moments')
        for v in units:
            if v[0]<floor:
                continue
            z=(v[0]-floor)/(1-floor) if floor!=1 else Q(0)
            AA,BB,CC=moments
            K=(AA-s*BB*v[0],-s*BB*v[1])
            jj=(BB-s*CC*v[0],-s*CC*v[1])
            RR=r**12*s*s*t*t
            PA,PJ=norm(K),norm(jj)
            L=PA+t*t*PJ-RR
            raw=L*L-4*t*t*PA*PJ
            need(targets['disk'].evaluate([b,x,y,z])==(1+b)**32*raw,'literal cube/origin discriminant')
            H=(AA-s*BB)**2+t*t*(BB-s*CC)**2-Q(9,8)*RR
            need(targets['H'].evaluate([b,x,y,z])==(1+b)**16*H,'literal first sign')
            for w in units+[(Q(-1),Q(0))]:
                integral=gaussian_integral([(r,Q(0))]*6+[(s*v[0],s*v[1]),(t*w[0],t*w[1])],1,-b,Q(9))
                rotated=gaussian_mul(w,jj)
                need(integral==(K[0]-t*rotated[0],K[1]-t*rotated[1]),'literal eight-factor origin integral')
                ratio=norm(integral)/RR
                need(ratio>=1 and (b==1 or ratio>1),'physical radial origin conclusion')
                rows.append([str(v) for v in [b,r,s,t,*integral,ratio]])
    # Exact failed relaxation from the source, independently integrated.
    v=(Q(99,101),Q(20,101));w=(Q(999831,1000169),Q(26000,1000169))
    ii=gaussian_integral([(Q(1,2),Q(0))]*6+[(v[0]/2,v[1]/2),(Q(9,2)*w[0],Q(9,2)*w[1])],1,-1,Q(9))
    ratio=norm(ii)/(Q(1,2)**14*Q(9,2)**2)
    need(ratio==Q(3059391541,4949836381)<1 and v[0]<1,'failed disk-free relaxation')
    return {'origin_integral_controls':len(rows),'origin_stream_sha256':digest(rows),
            'free_both_light_phases_N':str(ratio)}


def small_backend_controls():
    x,y,z,w=[variable(j) for j in range(4)]
    p=(2*x-3*y+z*w+1)**3
    data,den,degree=tensor(p)
    need(invert(data,den,degree)==p,'small exact full tensor inverse')
    for a,b,c,d in product((Q(0),Q(1,3),Q(1)),repeat=4):
        need(p.evaluate([a,b,c,d])==(2*a-3*b+c*d+1)**3,'literal polynomial backend control')
    # A distinct Fraction direct Bernstein formula on a small four-variable polynomial.
    indices=list(product(*(range(n+1) for n in degree)))
    reference=[]
    for e in indices:
        reference.append(sum(Q(v,p.d)*prod(Q(comb(e[j],f[j]),comb(degree[j],f[j]))
                                               for j in range(4))
                             for f,v in p.c.items() if all(f[j]<=e[j] for j in range(4))))
    need(reference==[Q(v,den) for v in data],'full small independent Fraction forward transform')
    rejected=[]
    for label,call in [('zero denominator',lambda:P({(0,0,0,0):1},0)),
                       ('incomplete tensor',lambda:invert(data[:-1],den,degree)),
                       ('wrong degree',lambda:tensor(p,(1,1,1,1))),
                       ('reversed cell',lambda:affine(p,0,1,0)),
                       ('missing disk',lambda:need(Q(99,101)>=1,'false disk claim'))]:
        try:
            call()
        except Failure:
            rejected.append(label)
        else:
            raise Failure('negative control accepted '+label)
    return {'literal_evaluations':81,'fraction_forward_entries':len(reference),
            'rejected_controls':rejected}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--original',type=Path)
    parser.add_argument('--full-original',type=Path)
    args=parser.parse_args()
    backend=small_backend_controls()
    targets,(W,L,RR)=radial_targets()
    print('Independent direct-cleared origin polynomials complete',flush=True)
    full_evidence=[] if args.full_original else None
    signs=radial_signs(targets,full_evidence)
    print('All121440 origin signs and complete inverses passed',flush=True)
    polar_record,I=polar(full_evidence)
    gap=integrated_gap()
    ctrl=controls(targets,W)
    example=nonreal_example()
    physical=polar_controls(I,gap)
    if args.original:
        original=json.loads(args.original.read_text())
        need({k:digest(p.canonical()) for k,p in targets.items()}==original['mapped_sha256'],
             'every cleared power polynomial matches original after independent generation')
        for own,old in zip(signs,original['cells']):
            for k in ['cell','target','degrees','coefficients','minimum','minimum_positive',
                      'zeros','zero_indices','zero_indices_sha256','sha256']:
                need(own[k]==old[k],'complete original sign tensor comparison '+k)
        for k in ['degrees','coefficients','minimum','sha256','power_sha256','integral_monomials','quotient_monomials']:
            need(polar_record[k]==original['polar'][k],'full original polar comparison '+k)
        print('Original complete power/sign tensor digests and zero inventories agree',flush=True)
    if args.full_original:
        original=json.loads(args.full_original.read_text())
        need(original['powers']=={k:p.canonical() for k,p in targets.items()},
             'every original cleared power entry')
        need(original['tensors']==full_evidence,'every original Bernstein coefficient entry')
        print('Every original power coefficient and122115 sign coefficient entries agree',flush=True)
    result={'agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'method':'Direct common-denominator cube moments and alternative discriminant; Pascal addition/subtraction tensors, no author import.',
            'backend':backend,'radial_cells':signs,'polar':polar_record,
            'integrated_mean_gap':gap,'controls':ctrl,'nonreal_example':example,
            'polar_physical_controls':physical,
            'complete_signs':sum(r['coefficients'] for r in signs)+polar_record['coefficients'],
            'mapped_power_sha256':{k:digest(p.canonical()) for k,p in targets.items()}}
    output=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.write:
        args.write.write_text(output)
    if args.check:
        need(json.loads(args.check.read_text())==json.loads(output),'whole expected summary')
    print(json.dumps({'verified':True,'agent':'six-reviewer-3',
                      'complete_signs':result['complete_signs'],'uniform_mean_gap_gamma':gap['uniform_gamma'],
                      'result_sha256':hashlib.sha256(output.encode()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
