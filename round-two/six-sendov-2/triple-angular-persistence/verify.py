#!/usr/bin/env python3
"""Universal rational identities for the triple angular family.

Exact arithmetic in Q(r)[mu]/(mu²-(3/8-2r)), with independent finite
normalization/Hessian checks. Analytic theorems are in PROOF.md.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb
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
    """Canonical rational function of one indeterminate r, over Q."""
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


RVAR=RF([0,1])
V=RF(Q(3,8))-2*RVAR


class Quad:
    """Exact quadratic extension: a+b mu, mu²=V."""
    def __init__(self,a=0,b=0):self.a,self.b=RF(a),RF(b)
    def __add__(self,other):
        if not isinstance(other,Quad):other=Quad(other)
        return Quad(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return Quad(-self.a,-self.b)
    def __sub__(self,other):return self+-other if isinstance(other,Quad) else self+-Quad(other)
    def __rsub__(self,other):return -self+other
    def __mul__(self,other):
        if not isinstance(other,Quad):other=Quad(other)
        return Quad(self.a*other.a+V*self.b*other.b,self.a*other.b+self.b*other.a)
    __rmul__=__mul__
    def __truediv__(self,other):
        if not isinstance(other,Quad):other=Quad(other)
        den=other.a*other.a-V*other.b*other.b
        return self*Quad(other.a/den,-other.b/den)
    def __pow__(self,n):
        out=Quad(1)
        for _ in range(n):out=out*self
        return out
    def rational(self):
        require(not self.b,'quadratic trace did not become rational')
        return self.a


# Polynomial operations in the separate root variable z; coefficients in Q(r).
def za(p,q):
    out=[RF(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]=out[i]+c
    for i,c in enumerate(q):out[i]=out[i]+c
    return trim(out)


def zs(p,c):return trim([x*c for x in p])


def zm(p,q):
    out=[RF(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]=out[i+j]+c*d
    return trim(out)


def zd(p):return trim([p[i]*i for i in range(1,len(p))] or [RF(0)])


def ze(p,x):
    out=Quad(0)
    for c in reversed(p):out=out*x+c
    return out


def weights(F,h1,h2,root):
    g=zs(zd(F),Q(1,8));g1=zs(zd(h1),Q(1,8));g2=zs(zd(h2),Q(1,8))
    gp=ze(zd(g),root);gpp=ze(zd(zd(g)),root)
    l1=-ze(g1,root)/gp
    l2=-(ze(g2,root)+ze(zd(g1),root)*l1+gpp*l1*l1/2)/gp
    n0=ze(F,root);n1=ze(h1,root)
    n2=ze(h2,root)+ze(zd(h1),root)*l1+ze(zd(zd(F)),root)*l1*l1/2
    d1=ze(zd(g1),root)+gpp*l1
    d2=ze(zd(g2),root)+ze(zd(zd(g1)),root)*l1+gpp*l2+ze(zd(zd(zd(g))),root)*l1*l1/2
    w0=-8*n0/gp
    w1=-8*(n1/gp-n0*d1/(gp**2))
    w2=-8*(n2/gp-n1*d1/(gp**2)+n0*(d1*d1/(gp**3)-d2/(gp**2)))
    return w0,w1,w2


def eta2(F,h1,h2):
    out=Quad(0)
    for root in [Quad(0),Quad(0,1),Quad(0,-1)]:
        w0,w1,w2=weights(F,h1,h2,root)
        out=out+w1*w1+2*w0*w2
    return out.rational()


def bernstein(p,lo,hi):
    out=[Q(0)]
    for c in reversed(p):out=pa(pm(out,[lo,hi-lo]),[c])
    degree=len(p)-1
    out=out+[Q(0)]*(degree+1-len(out))
    return [sum(out[j]*Q(comb(k,j),comb(degree,j)) for j in range(k+1)) for k in range(degree+1)]


def encode(value):
    if isinstance(value,RF):return value.record()
    if isinstance(value,(tuple,list)):return [encode(x) for x in value]
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    return str(value)


def verify():
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    r=RVAR;t=RF(Q(1,2))-3*r;v=V
    A=[-r,RF(0),RF(1)];B=[-t,RF(0),RF(1)]
    F=zm(zm(zm(A,A),A),B)
    g=zm(zm(zm([RF(0),RF(1)],A),A),[-v,RF(0),RF(1)])
    check('full_triple_compression_polynomial',zs(zd(F),Q(1,8)),g)
    check('full_triple_norm_coefficients',[F[8],F[7],F[6]],[RF(1),RF(0),RF(-Q(1,2))])
    X=24*r*r-6*r+Q(1,2);p=8*r*t/v;eta=p*p+(1-p)**2/2
    for label,root,want in [('zero',Quad(0),p),('plus',Quad(0,1),(1-p)/2),('minus',Quad(0,-1),(1-p)/2)]:
        w0,_,_=weights(F,[RF(0)],[RF(0)],root)
        check('active_weight_'+label,w0.rational(),want)
    R=eta.derivative()/X.derivative()
    Rclosed=16*(4*r-1)*(576*r*r-112*r+3)/(16*r-3)**3
    check('universal_stationary_equation',R,Rclosed)
    check('universal_stationary_derivative',R.derivative(),-64*(1088*r*r-544*r+57)/(16*r-3)**4)

    # The normalization, reflection average, and first two root coefficients
    # are explicit; the weight-root Taylor formulas above independently derive
    # the closed all-parameter Hessian identities.
    z=[RF(0),RF(1)];z2=[RF(0),RF(0),RF(1)]
    hsplit=za(za(zm(z,zd(F)),zs(F,-8)),zs(zm(zm(A,[r,RF(0),RF(1)]),B),-1))
    split_e2=eta2(F,[RF(0)],hsplit)
    qs=(split_e2-R*(12*r-4*X))/2
    qs_closed=-64*r*(8*r-1)*(6592*r*r-2384*r+213)/(3*(16*r-3)**3)
    check('universal_split_loss_per_norm',qs,qs_closed)

    hodd1=zs(zm(z,zm(A,A)),6*(t-r))
    hodd2=za(za(zm(za(zs(zm(A,A),3),zs(zm(z2,A),12)),B),zs(zm(z2,zm(A,A)),-36)),zs(zm(zm(A,A),A),9))
    hodd2=za(za(hodd2,zs(zm(z,zd(F)),12)),zs(F,-96))
    odd_e2=eta2(F,hodd1,hodd2)
    qo=(odd_e2-R*(36*r+108*t-48*X))/24
    P=21331968*r**5+14127104*r**4-10310656*r**3+1855104*r*r-103176*r-243
    qo_closed=-(8*r-1)*P/(8*(16*r-3)**5)
    check('universal_odd_hard_loss_per_norm',qo,qo_closed)
    qe=4*r*t*(8*r-1)*R.derivative()
    qe_closed=128*r*(6*r-1)*(8*r-1)*(1088*r*r-544*r+57)/(16*r-3)**4
    check('universal_even_hard_loss_per_norm',qe,qe_closed)

    r3=Q(9,56);R3=-Q(80,9)
    check('triple_point_X_eta_R',[X.at(r3),eta.at(r3),R.at(r3)], [Q(61,392),Q(17,49),R3])
    check('triple_point_value',(R*X-eta).at(r3),-Q(763,441))
    check('triple_point_three_Hessian_losses',[qs.at(r3),qo.at(r3),qe.at(r3)],[Q(32,21),Q(16,3),Q(304,21)])
    # A different derivation at the equality point: linearize the ODE square
    # at the three simple scaled roots0,+/-sqrt(3), and treat repeated slots
    # by the exact compressed three-coordinate matrix trace.
    a=[-Q(9),Q(0),Q(1)];bb=[-Q(1),Q(0),Q(1)]
    fscaled=pm(pm(pm(a,a),a),bb);gscaled=ps(pd(fscaled),Q(1,8))
    def lscaled(h):
        return pa(pa(pm([Q(3),Q(0),-Q(1,3)],pd(pd(h))),
                     ps(pm([Q(0),Q(1)],pd(h)),Q(4,3))),ps(h,8))
    ho=ps(pm([Q(0),Q(1)],pm(a,a)),-48);he=ps(pm(a,a),-144)
    def pairvalue(poly):
        return [sum(poly[2*k]*(Q(3)**k) for k in range((len(poly)+1)//2)),
                sum(poly[2*k+1]*(Q(3)**k) for k in range(len(poly)//2))]
    def point_residual(h):
        Lh=lscaled(h);den=pairvalue(pd(gscaled));require(den[1]==0,'point denominator parity')
        pair=[-c/(56*den[0]) for c in pairvalue(Lh)]
        zero=-pe(Lh,Q(0))/(56*pe(pd(gscaled),Q(0)))
        return zero,pair
    check('independent_odd_active_residual',point_residual(ho),(Q(0),[Q(0),Q(4,7)]))
    check('independent_even_active_residual',point_residual(he),(-Q(40,7),[Q(16,7),Q(0)]))
    # Repeated eigenvalue first-order traces: P3 diag(v) P3.
    P3=[[Q(int(i==j))-Q(1,3) for j in range(3)] for i in range(3)]
    probes=[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1]]
    traces=[]
    for vector in probes:
        K=[[sum(P3[i][k]*vector[k]*P3[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        actual=sum(K[i][j]*K[j][i] for i in range(3) for j in range(3))
        want=sum(Q(x*x,3) for x in vector)+Q(sum(vector)**2,9)
        require(actual==want,'block trace coefficient failed');traces.append(actual)
    check('complete_quadratic_block_trace_coefficients',traces,[Q(4,9)]*3+[Q(10,9)]*3)
    repeated_const=Q(32,7)*Q(4,56)
    odd_point_loss=repeated_const+2*(Q(4,7)**2)*3
    even_point_loss=repeated_const+Q(40,7)**2+2*Q(16,7)**2
    split_point_loss=Q(32,7)*Q(2,3*56)
    check('independent_point_Hessian_losses',
          [split_point_loss/Q(2,56),odd_point_loss/Q(24,56),even_point_loss/Q(168,56)],
          [qs.at(r3),qo.at(r3),qe.at(r3)])
    check('triple_point_R_derivative',R.derivative().at(r3),Q(119168,27))
    check('triple_branch_r_response',1/R.derivative().at(r3),Q(27,119168))
    xr=X.derivative().at(r3)/R.derivative().at(r3)
    check('triple_branch_X_response',xr,Q(81,208544))
    formal_xr=Q(15,56)/(Q(14,3)**3)
    check('formal_square_gap_second_coefficient',(formal_xr-xr)/2,Q(6561,5839232))

    # Sharp comparison on the entire symmetric triple family, not all S.
    dx=X-Q(1,8)
    check('triple_X_excess',dx,RF(Q(3,8))*(8*r-1)**2)
    C=(1-eta)/dx
    check('triple_ratio_formula',C,4*(3+80*r-576*r*r)/(3-16*r)**2)
    check('sharp_restricted_ratio_square',RF(Q(208,9))-C,4*(136*r-21)**2/(9*(3-16*r)**2))
    Rstar=-Q(208,9);rstar=Q(21,136)
    check('restricted_crossing_stationarity',R.at(rstar),Rstar)
    check('restricted_crossing_value_difference',Rstar*dx+1-eta,
          -(8*r-1)**2*(136*r-21)**2/(6*(3-16*r)**2))
    check('stationary_comparison_difference',R*dx+1-eta,
          -3*(8*r-1)**3*(136*r-21)/(2*(16*r-3)**3))

    # Complete rational positivity certificate for an explicit local-stability band.
    lo=Q(21,136);hi=Q(161,1000)
    polynomials={'split':[Q(213),-Q(2384),Q(6592)],
                 'even':[ -Q(57),Q(544),-Q(1088)],
                 'odd':[-Q(243),-Q(103176),Q(1855104),-Q(10310656),Q(14127104),Q(21331968)]}
    expected={'split':[Q(594,289),Q(386,425),Q(738,15625)],
              'even':[Q(18,17),Q(218,125),Q(37218,15625)],
              'odd':[Q(248832,1419857),Q(14093568,10440125),Q(155555328,76765625),
                     Q(260172544,112890625),Q(47655108608,20751953125),Q(64853688576,30517578125)]}
    for name,poly in polynomials.items():
        b=bernstein(poly,lo,hi);check(name+'_full_Bernstein_certificate',b,expected[name])
        require(all(x>0 for x in b),name+' sign certificate failed')
    check('explicit_local_band_R_endpoints',[R.at(lo),R.at(hi)],[Rstar,-Q(1129232,148877)])

    # Different exact calculation of the cubic formal-equality collision.
    b=RF([0,1]);Y=Q(9,56)
    H=Y**4-Y**3/2+15*(4-3*b)*Y*Y/(448*(2-b))-15*(4-3*b)**2*Y/(12544*(2-b)*(4-b))+15*(4-3*b)**3/(11239424*(2-b)*(4-b))
    kappa=H.derivative().at(-Q(8,3))
    check('formal_cubic_collision_derivative',kappa,Q(2187,172103680))
    cprime=kappa/(Q(9,56)-Q(1,56))
    check('cubic_cluster_constant_derivative',cprime,Q(2187,24586240))
    check('cubic_cluster_discriminant_leading',-27*cprime*cprime,-Q(129140163,604483197337600))
    return records


def damage_controls():
    rejected=0
    tests=[lambda: RF(1,0),lambda: RF(1)/RF(0),lambda: (1/(RVAR-1)).at(Q(1)),
           lambda: require(RF(Q(208,9))-4*(3+80*RVAR-576*RVAR**2)/(3-16*RVAR)**2
                           ==-4*(136*RVAR-21)**2/(9*(3-16*RVAR)**2),'damaged comparison sign')]
    for test in tests:
        try:test()
        except ValueError:rejected+=1
    require(rejected==len(tests),'damage control did not reject')
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',action='store_true',help='maintainer fixture generation')
    args=parser.parse_args();records=verify()
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if args.write_expected:args.expected.write_text(json.dumps(records,sort_keys=True,indent=2)+'\n')
    require(json.loads(args.expected.read_text())==records,'expected fixture differs')
    print(json.dumps({'status':'all exact checks passed','checks':len(records),'damage_controls':damage_controls(),'record_sha256':digest},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,json.JSONDecodeError) as error:
        print('verification failed: '+str(error),file=sys.stderr);raise SystemExit(1)
