#!/usr/bin/env python3
"""Exact three-level angular optimization and transverse stability certificate.

Rational kernel adapted from the author's triple-angular-persistence checker,
source4587f5f3776a0ec8c22d43ec8b264c8b48915218. New all-multiplicity,
Sturm, uniform-tangent and asymmetric splitting checks are implemented here.
The analytic projection/compactness arguments remain written proofs.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys


def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def pa(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)


def ps(p,c):return trim([x*c for x in p])


def pm(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)


def pd(p):return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def pe(p,x):
    value=Q(0)
    for c in reversed(p):value=value*x+c
    return value


def pdiv(p,q):
    p,q=trim(p),trim(q)
    require(q!=[0],'zero polynomial denominator')
    quotient=[Q(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k,c=len(p)-len(q),p[-1]/q[-1]
        quotient[k]+=c;p=pa(p,ps([Q(0)]*k+q,-c))
    return trim(quotient),p


def pgcd(p,q):
    while q!=[0]:p,q=q,pdiv(p,q)[1]
    return ps(p,1/p[-1])


def poly(value):
    return trim([Q(x) for x in value]) if isinstance(value,(list,tuple)) else [Q(value)]


class RF:
    """Canonical rational function of one indeterminate t, over Q."""
    def __init__(self,n=0,d=1):
        if isinstance(n,RF) and d==1:
            self.n,self.d=n.n,n.d;return
        n,d=poly(n),poly(d)
        require(d!=[0],'identically zero rational denominator')
        if n==[0]:self.n,self.d=(Q(0),),(Q(1),);return
        common=pgcd(n,d)
        n,rn=pdiv(n,common);d,rd=pdiv(d,common)
        require(rn==[0] and rd==[0],'gcd division not exact')
        factor=1/d[-1]
        self.n,self.d=tuple(ps(n,factor)),tuple(ps(d,factor))
    def __bool__(self):return self.n!=(Q(0),)
    def __eq__(self,other):
        other=RF(other);return self.n==other.n and self.d==other.d
    def __add__(self,other):
        other=RF(other);return RF(pa(pm(self.n,other.d),pm(other.n,self.d)),pm(self.d,other.d))
    __radd__=__add__
    def __neg__(self):return RF(ps(self.n,-1),self.d)
    def __sub__(self,other):return self+-RF(other)
    def __rsub__(self,other):return RF(other)+-self
    def __mul__(self,other):
        other=RF(other);return RF(pm(self.n,other.n),pm(self.d,other.d))
    __rmul__=__mul__
    def __truediv__(self,other):
        other=RF(other);require(bool(other),'zero rational divisor')
        return RF(pm(self.n,other.d),pm(self.d,other.n))
    def __rtruediv__(self,other):return RF(other)/self
    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'invalid rational power')
        out=RF(1)
        for _ in range(n):out=out*self
        return out
    def derivative(self):
        return RF(pa(pm(pd(self.n),self.d),ps(pm(self.n,pd(self.d)),-1)),pm(self.d,self.d))
    def at(self,r):
        den=pe(self.d,r);require(bool(den),'evaluation at rational pole')
        return pe(self.n,r)/den
    def record(self):return {'numerator':[str(x) for x in self.n],'denominator':[str(x) for x in self.d]}


T=RF([0,1])


def ppow(p,k):
    out=[Q(1)]
    for _ in range(k):out=pm(out,p)
    return out


def zinverse(p,h):
    a,b=h,pdiv(p,h)[1];u,v=[RF(0)],[RF(1)]
    while b!=[0]:
        quo,nxt=pdiv(a,b)
        a,b=b,nxt;u,v=v,pa(u,ps(pm(quo,v),-1))
    require(len(a)==1 and bool(a[0]),'noninvertible active derivative')
    out=pdiv(ps(u,1/a[0]),h)[1]
    require(pdiv(pm(out,p),h)[1]==[1],'inverse certificate failed')
    return out


def zprod(h,*polys):
    out=[RF(1)]
    for p in polys:out=pdiv(pm(out,p),h)[1]
    return out


def ztrace(q,h):
    q=pdiv(q,h)[1]
    return 2*q[0]-(q[1] if len(q)>1 else RF(0))*h[1]


def companion_square_trace(q,h):
    """Direct trace of the 2x2 matrix q(C_h)^2, no Newton reduction."""
    q=pdiv(q,h)[1];a=q[0];b=q[1] if len(q)>1 else RF(0)
    matrix=[[a,-b*h[0]],[b,a-b*h[1]]]
    return sum(matrix[i][j]*matrix[j][i] for i in range(2) for j in range(2))


def real_moments(mult):
    m,n,k=mult;levels=[T,RF(1),-(m*T+n)/k]
    moments=[sum(a*r**j for a,r in zip(mult,levels)) for j in (1,2,3,4)]
    trace=sum(levels)
    beta=sum(a*levels[(i+1)%3]*levels[(i+2)%3] for i,a in enumerate(mult))/8
    N,S3,S4=moments[1:];disc=trace**2-4*beta;delta=S4-N*N/8
    eta=(N*N+(2*S3-N*trace)**2/disc)/2
    return levels,moments,[beta,-trace,RF(1)],(N*N-eta)/delta


def displayed_ratios():
    t=T
    return {
      (4,3,1):8*(t-1)**2*(5*t+3)**2/((15*t*t+24*t+10)*(35*t*t+38*t+11)),
      (4,2,2):8*(t-1)**2*(3*t+1)**2/((3*t*t+4*t+2)*(9*t*t+2*t+1)),
      (5,2,1):20*(t-1)**2*(3*t+1)**2*(5*t+3)**2/((21*t*t+22*t+6)*(1035*t**4+1700*t**3+1010*t*t+260*t+27)),
      (3,3,2):6*(t-1)**2*(3*t+5)**2*(5*t+3)**2/((5*t*t+8*t+5)*(5*t*t+14*t+13)*(13*t*t+14*t+5)),
      (6,1,1):4*(t-1)**2*(3*t+1)**2*(7*t+1)**2/((28*t*t+18*t+3)*(721*t**4+492*t**3+118*t*t+12*t+1))}


def sturm(p):
    def normalize(a):return ps(a,1/abs(a[-1]))
    a,b=normalize(trim(p)),normalize(pd(p));out=[a,b]
    while True:
        r=ps(pdiv(a,b)[1],-1)
        if r==[0]:break
        r=normalize(r);out.append(r);a,b=b,r
    return out


def variations(chain,x):
    signs=[]
    for p in chain:
        if x in ('-inf','+inf'):
            a=p[-1]*(-1 if x=='-inf' and (len(p)-1)%2 else 1)
        else:a=pe(p,x)
        if a:signs.append(1 if a>0 else -1)
    return sum(a!=b for a,b in zip(signs,signs[1:]))


def roots_between(chain,a,b):return variations(chain,a)-variations(chain,b)


def ia(a,b):return a[0]+b[0],a[1]+b[1]
def im(a,b):
    values=[x*y for x in a for y in b]
    return min(values),max(values)
def ip(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):out=ia(im(out,x),(c,c))
    return out
def iq(n,d,x):
    a,b=ip(n,x),ip(d,x)
    require(b[0]>0 or b[1]<0,'interval division spans zero')
    return im(a,(1/b[1],1/b[0]))


def splitting_coefficients():
    """Differentiate persistent active residues in Q(t)[z]/h, not roots."""
    t=T;levels=[t,RF(1),-4*t-3];mult=[4,3,1]
    f=[RF(1)];inactive=[RF(1)]
    for r,m in zip(levels,mult):
        f=pm(f,ppow([-r,RF(1)],m))
        inactive=pm(inactive,ppow([-r,RF(1)],m-1))
    g=ps(pd(f),Q(1,8));h,rem=pdiv(g,inactive)
    require(rem==[0] and len(h)==3,'active factorization failed')
    ig=zinverse(pd(g),h);q0=ps(zprod(h,f,ig),-8)
    eta0=ztrace(zprod(h,q0,q0),h)
    require(eta0==companion_square_trace(q0,h),'companion trace disagrees')
    # The z derivative is taken BEFORE reduction modulo h.
    qprime=pa(ps(zprod(h,pd(f),ig),-8),ps(zprod(h,f,pd(pd(g)),ig,ig),8))
    N=20*t*t+24*t+12;S4=4*t**4+3+(4*t+3)**4;delta=S4-N*N/8
    out=[]
    for r in levels[:2]:
        F,rem=pdiv(f,ppow([-r,RF(1)],2));require(rem==[0],'pair removal failed')
        f2=ps(F,-1);g2=ps(pd(f2),Q(1,8));lam2=ps(zprod(h,g2,ig),-1)
        q2=pa(pa(ps(zprod(h,f2,ig),-8),ps(zprod(h,f,pd(g2),ig,ig),8)),zprod(h,lam2,qprime))
        eta2=2*ztrace(zprod(h,q0,q2),h)
        C2=((4*N-eta2)*delta-(N*N-eta0)*(12*r*r-N/2))/delta**2
        out.append(C2)
    return h,eta0,out


def encode(x):
    if isinstance(x,RF):return x.record()
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,Q):return str(x)
    return x


def verify():
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    ratios=displayed_ratios()
    infinity={(4,3,1):Q(8,21),(4,2,2):Q(8,3),(5,2,1):Q(100,483),(3,3,2):Q(54,13),(6,1,1):Q(63,721)}
    for mult,r in ratios.items():
        levels,moments,h,derived=real_moments(mult)
        check(str(mult)+' balanced',moments[0],RF(0))
        check(str(mult)+' universal ratio identity',derived,r)
        check(str(mult)+' infinite chart limit',r.n[-1]/r.d[-1],infinity[mult])
    q=list(map(Q,[746,4737,11175,11695,4575]));r=ratios[(4,3,1)]
    den=(15*T*T+24*T+10)*(35*T*T+38*T+11)
    check('stationary factor identity',r.derivative(),16*(T-1)*(5*T+3)*RF(q)/den**2)
    chain=sturm(q)
    alpha=(Q(-853410556973738,10**15),Q(-853410556973736,10**15))
    beta=(Q(-443370119245,10**12),Q(-443370119244,10**12))
    check('quartic real root count',roots_between(chain,'-inf','+inf'),2)
    check('alpha unique isolated root',roots_between(chain,*alpha),1)
    check('beta unique isolated root',roots_between(chain,*beta),1)
    cbox=iq(r.n,r.d,alpha)
    require(Q(2453389668,10**8)<cbox[0]<cbox[1]<Q(2453389670,10**8),'sharp constant enclosure failed')
    records['sharp constant rational enclosure']=encode(cbox)
    bbox=iq(r.n,r.d,beta);require(Q(4)<bbox[0]<bbox[1]<Q(5),'other maximum not separated')
    records['other stationary value enclosure']=encode(bbox)
    check('vanishing stationary values',[r.at(1),r.at(Q(-3,5))],[Q(0),Q(0)])
    check('uniform removable value',r.at(-1),Q(16))
    pK=list(map(Q,[587202560,-103317504,-7974720,-50108,20667]))
    identity=[Q(0)]
    for i,c in enumerate(pK):identity=pa(identity,ps(pm(ppow(r.n,i),ppow(r.d,4-i)),c))
    check('constant polynomial divisibility',pdiv(identity,q)[1],[Q(0)])
    check('constant unique isolated root',roots_between(sturm(pK),Q(2453389668,10**8),Q(2453389670,10**8)),1)
    require(ip(pd(q),alpha)[1]<0,'quartic derivative sign failed')
    records['fixed-family strict curvature']=encode(ip(pd(q),alpha))
    for mult in [(5,2,1),(3,3,2),(6,1,1)]:
        rr=ratios[mult];p=pa(ps(rr.d,16),ps(rr.n,-1))
        check(str(mult)+' upper16 real root count',roots_between(sturm(p),'-inf','+inf'),0)
        require(pe(p,0)>0,'upper16 positive seed failed')
        records[str(mult)+' upper16 positive seed']=encode(pe(p,0))
    rr=ratios[(4,2,2)];p=pa(ps(rr.d,16),ps(rr.n,-1))
    expected=pm(ppow([Q(1),Q(1)],2),[Q(1),Q(2),Q(15)])
    require(len(RF(p,expected).n)==1 and RF(p,expected).d==(Q(1),),'factor quotient not constant')
    factor=RF(p,expected).at(0);require(factor>0,'factor not positive')
    check('(4,2,2) upper16 factor',p,ps(expected,factor))
    check('(4,2,2) quadratic discriminant',Q(2)**2-4*15,Q(-56))
    h,eta0,split=splitting_coefficients()
    A=list(map(Q,[12684,103380,366599,751299,993954,872170,470475,117375]))
    B=list(map(Q,[42424,326238,1074965,2064611,2726970,2646100,1685625,496875]))
    check('fourfold block splitting identity',split[0],4*RF(A)/(3*(T+1)*den**2))
    check('threefold block splitting identity',split[1],4*RF(B)/(9*(T+1)*den**2))
    for name,co in zip(['fourfold','threefold'],split):
        enclosure=iq(co.n,co.d,alpha)
        require(enclosure[1]<0,name+' transverse curvature not negative')
        records[name+' transverse strict curvature']=encode(enclosure)
    # An exact integer-root witness, checked by the active residue and matrix routes.
    t0=Q(-64,75);N=4*t0*t0+3+(-4*t0-3)**2;S4=4*t0**4+3+(-4*t0-3)**4
    eta=eta0.at(t0);scale=Q(75)
    check('integer witness moments',[N*scale**2,S4*scale**4],[Q(34220),Q(162954260)])
    check('integer witness unnormalized eta',eta*scale**4,Q(63435273160,83))
    check('integer witness normalized X and eta',[S4/N**2,eta/N**2],[Q(8147713,58550420),Q(1585881829,2429842430)])
    check('integer witness ratio',r.at(t0),Q(27899524,1137183))
    check('integer witness defect24',eta/N**2-1+24*(S4/N**2-Q(1,8)),Q(-18365743,2429842430))
    require(r.at(t0)>Q(49,2),'integer benchmark not separated from49/2')
    # Universal linearized uniform calculation on a basis of the 6D tangent.
    signs=[Q(1)]*4+[-Q(1)]*4
    basis=[]
    for block in [0,4]:
        for i in range(3):
            v=[Q(0)]*8;v[block+i]=Q(1);v[block+3]=-Q(1);basis.append(v)
    def H(v,x):
        projected=[a-sum(x)/8 for a in x]
        y=[a*b for a,b in zip(v,projected)]
        return [a-sum(y)/8 for a in y]
    check('uniform full tangent eigenvector differential',
          [pa(H(signs,ps(v,-1)),H(v,signs)) for v in basis],[[Q(0)] for _ in basis])
    gram=[[sum(a*b for a,b in zip(v,w)) for w in basis] for v in basis]
    def projection(lam,x):
        if lam==0:return [s*sum(a*b for a,b in zip(signs,x))/8 for s in signs]
        block=range(4) if lam==1 else range(4,8)
        mean=sum(x[i] for i in block)/4
        return [x[i]-mean if i in block else Q(0) for i in range(8)]
    def projection_differential(lam,v,x):
        out=[Q(0)]*8
        for other in [-1,0,1]:
            if other==lam:continue
            left=projection(lam,H(v,projection(other,x)))
            right=projection(other,H(v,projection(lam,x)))
            out=[a+(b+c)/(lam-other) for a,b,c in zip(out,left,right)]
        return out
    leaked=[]
    for v in basis:
        pair=[]
        for lam in [-1,1]:
            direct=projection(lam,v);response=projection_differential(lam,v,signs)
            pair.extend(a+b for a,b in zip(direct,response))
        leaked.append(pair)
    leakage=[[sum(a*b for a,b in zip(v,w)) for w in leaked] for v in leaked]
    check('uniform full tangent leakage quadratic form',leakage,[[4*x for x in row] for row in gram])
    check('uniform ratio leading constant',Q(1)/Q(1,16),Q(16))
    controls=0
    for actual,wrong in [(r,RF(pa(r.n,[Q(1)]),r.d)),
                         (r.derivative(),16*(T-1)*(5*T+3)*RF(pa(q,[Q(1)]))/den**2),
                         (split[0],4*RF(pa(A,[Q(1)]))/(3*(T+1)*den**2)),
                         (r.at(t0),Q(27899525,1137183))]:
        try:require(actual==wrong,'damaged certificate rejected')
        except ValueError:controls+=1
    require(controls==4,'damage control failed')
    return {'records':records,'checks':len(records),'damage_controls':controls}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',type=Path)
    parser.add_argument('--write-expected',action='store_true');args=parser.parse_args()
    output=verify();raw=json.dumps(output,sort_keys=True,separators=(',',':')).encode()
    output['record_sha256']=hashlib.sha256(raw).hexdigest()
    fixture=args.expected or Path(__file__).with_name('expected.json')
    if args.write_expected:fixture.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    else:require(json.loads(fixture.read_text())==output,'expected fixture differs')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:
        print('verification failed: '+str(error),file=sys.stderr);sys.exit(1)
