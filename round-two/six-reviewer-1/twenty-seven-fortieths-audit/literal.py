"""Exact Gaussian channels, whole centered expansion, quartic and clipping controls.

Adapted openly from own10250 literal engine; no current author modules, no
arithmetic.py or cover/expected record imports.
The general Gauss--Lucas and analytic Lipschitz bridges are ordinary proofs.
"""
from fractions import Fraction as Q
from math import comb
import json


def insist(p,label):
    if not p:raise ValueError(label)


def g(x,y=0):return Q(x),Q(y)
def ga(z,w):return z[0]+w[0],z[1]+w[1]
def gm(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def gs(z,k):return z[0]*k,z[1]*k
def norm(z):return z[0]*z[0]+z[1]*z[1]
def gd(z,w):
    insist(norm(w)>0,'Gaussian nonzero denominator')
    return gs(gm(z,(w[0],-w[1])),1/norm(w))
def prod(values):
    a=g(1)
    for v in values:a=gm(a,v)
    return a
def pmul(p,q):
    r=[g(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):r[i+j]=ga(r[i+j],gm(x,y))
    return r
def peval(p,z):
    r=g(0)
    for x in p[::-1]:r=ga(gm(r,z),x)
    return r


def original(a,others):
    roots=[g(a)]+others
    insist(len(roots)==9 and all(norm(z)<=1 for z in roots),'all nine exact original roots')
    p=[g(1)]
    for z in roots:p=pmul(p,[gs(z,-1),g(1)])
    dp=[gs(p[i],i)for i in range(1,10)]
    at=peval(dp,g(a));insist(norm(at)>0,'simple marked zero')
    # p'(a+x)/p'(a)=prod(all8)(1+x q_j), so all nine e_k are literal.
    es=[gd(tuple(sum(dp[j][r]*comb(j,k)*a**(j-k)for j in range(k,9))for r in range(2)),at)for k in range(9)]
    insist(es[0]==g(1)and es[8]==gd(g(9),at),'all eight critical multiplicities')
    O=g(0);J=g(0);b=1-a*a
    for k,e in enumerate(es):
        O=ga(O,gs(e,9*(-a)**k/Q(k+1)))
        J=ga(J,gs(e,a**(8-k)*b**k/Q(k+1)))
    originalO=gm(prod(others),gd(g(9),at))
    originalJ=prod([gd(ga(g(1),gs(z,-a)),ga(g(a),gs(z,-1)))for z in others])
    insist(O==originalO and J==originalJ,'entire original communication identities')
    for z in others:
        insist(norm(ga(g(1),gs(z,-a)))-norm(ga(g(a),gs(z,-1)))==(1-a*a)*(1-norm(z))>=0,
               'whole polar original-disk payment')
    return {'a':str(a),'all9originals':[[str(t)for t in z]for z in roots],
            'all9reciprocal_elementary_coefficients':[[str(t)for t in z]for z in es],
            'O':list(map(str,O)),'J':list(map(str,J))}


def elementary(z):
    e=[g(1)]
    for x in z:
        out=[g(0)]*(len(e)+1)
        for k,v in enumerate(e):out[k]=ga(out[k],v);out[k+1]=ga(out[k+1],gm(v,x))
        e=out
    return e


def quartic(z):
    insist(len(z)==8,'eight centered entries')
    insist(tuple(sum(v[i]for v in z)for i in range(2))==g(0),'exact complex centering')
    p2=tuple(sum(gm(v,v)[i]for v in z)for i in range(2))
    p4=tuple(sum(gm(gm(v,v),gm(v,v))[i]for v in z)for i in range(2))
    S=sum(norm(v)for v in z);M4=sum(norm(v)**2 for v in z)
    e=elementary(z);X=[ga(gm(v,v),gs(p2,-Q(1,8)))for v in z]
    sumX2=tuple(sum(gm(v,v)[i]for v in X)for i in range(2))
    insist(sumX2==ga(p4,gs(gm(p2,p2),-Q(1,8))),'whole complex fourth variance identity')
    insist(sum(norm(v)for v in X)==M4-norm(p2)/8,'whole Hermitian variance identity')
    insist(e[4]==ga(gs(gm(p2,p2),Q(3,32)),gs(sumX2,-Q(1,4))),'full Newton fourth identity')
    insist(norm(e[4])<=(Q(3,16)*S*S)**2,'literal sufficient quartic amplitude')
    x=[g(v[0])for v in z];y=[g(v[1])for v in z]
    # Enumerate all subset choices in P(x+t y), independently of Newton's identity.
    import itertools
    coefficients=[Q(0)]*5
    for inds in itertools.combinations(range(8),4):
        p=[Q(1)]
        for j in inds:
            q=[Q(0)]*(len(p)+1)
            for k,v in enumerate(p):q[k]+=v*x[j][0];q[k+1]+=v*y[j][0]
            p=q
        coefficients=[a+b for a,b in zip(coefficients,p)]
    insist(e[4]==g(coefficients[0]-coefficients[2]+coefficients[4],coefficients[1]-coefficients[3]),
           'all five complexification coefficients, including both odd terms')
    return {'entries':[[str(a)for a in v]for v in z],'all9_elementary':[[str(a)for a in v]for v in e],
            'all5_complexification':list(map(str,coefficients)),'S':str(S),'p2':list(map(str,p2)),
            'p4':list(map(str,p4)),'full_X':[[str(a)for a in v]for v in X]}


def centered_product(q,a):
    mu=tuple(sum(v[i]for v in q)/8 for i in range(2))
    z=[ga(v,gs(mu,-1))for v in q];es=elementary(z)
    actual=[g(1)]
    for v in q:actual=pmul(actual,[g(1),gs(v,-a)])
    reconstructed=[g(0)]*9
    for k in range(9):
        poly=[g(1)]
        for _ in range(8-k):poly=pmul(poly,[g(1),gs(mu,-a)])
        for j,v in enumerate(poly):reconstructed[k+j]=ga(reconstructed[k+j],gs(gm(es[k],v),(-a)**k))
    insist(actual==reconstructed and es[1]==g(0),'all9 coefficients of centered origin product')
    return {'a':str(a),'mu':list(map(str,mu)),'entries':[[str(a)for a in v]for v in q],
            'all9_product':[[str(a)for a in v]for v in actual]}


def main():
    controls=[]
    for a in [Q(2,3),Q(27,40)]:
        controls.append(original(a,[g(Q(1,4)),g(-Q(1,4)),g(0,Q(1,3)),g(0,-Q(1,3)),
                                    g(Q(1,2),Q(1,4)),g(Q(1,2),-Q(1,4)),g(-Q(1,3)),g(-Q(1,3))]))
        controls.append(original(a,[g(1),g(-1),g(0,1),g(0,-1),g(0),g(0),g(0,Q(1,2)),g(0,-Q(1,2))]))
    a=Q(27,40);p=[g(1)]
    for _ in range(9):p=pmul(p,[g(-a),g(1)])
    insist(peval([gs(p[i],i)for i in range(1,10)],g(a))==g(0),'multiple marked zero/pole branch')
    zs=[[g(1)]*4+[g(-1)]*4,[g(7)]+[g(-1)]*7]
    seed=[g(Q(j,13),Q((j*j)%5,17))for j in range(7)]
    seed.append(gs(tuple(sum(v[i]for v in seed)for i in range(2)),-1));zs.append(seed)
    zs.append([gm(v,g(Q(3,5),Q(4,5)))for v in seed])
    quartics=[quartic(z)for z in zs]
    insist(elementary(zs[0])[4]==g(6) and sum(norm(v)for v in zs[0])==8,'exact sharp real norm3/32')
    products=[centered_product([ga(v,g(Q(3,4),Q(1,7)))for v in seed],a)for a in [Q(2,3),Q(27,40)]]
    lower=Q(51,80);mu=Q(19,20);a=Q(27,40)
    insist(8*mu>=Q(37,5)and mu*mu>lower*lower,'synchronized beta is not actual norm')
    envelope=(1-a*lower)**2;actual=(1-a*mu)**2
    insist(envelope-actual==a*(mu-lower)*(2-a*(mu+lower))>0,'whole synchronized quadratic identity')
    eps=Q(1,2**19);m=1/(1+a)
    r=[m]+[(8+eps-m)/7]*7;theta=(8-8*m)/(sum(r)-8*m);rp=[m+theta*(v-m)for v in r]
    insist(min(rp)>=m and sum(rp)==8 and sum(abs(x-y)for x,y in zip(r,rp))==eps,
           'continuous radius-floor-preserving mass clipping')
    P=Q(1);Pp=Q(1)
    for x,y in zip(r,rp):P*=x;Pp*=y
    ratios=[x/y for x,y in zip(r,rp)]
    mmin=Q(40,67)
    insist(P/Pp<=(Q(1)+eps/(8*mmin))**8,
           'all eight radial ratio AMGM factors')
    # Independently multiply every exact ratio and its original/clipped products.
    from functools import reduce
    insist(reduce(lambda x,y:x*y,ratios,Q(1))==P/Pp and Pp<=1,
           'whole actual-versus-clipped radial product')
    # More than one nonuniform radius configuration, including an unchanged floor.
    shifted=[Q(1)+eps/8]*8
    for a0 in [Q(2,3),Q(27,40)]:
        floor=1/(1+a0)
        for rs in [[floor]+[(8+eps-floor)/7]*7,shifted]:
            hs=[eps*(x-floor)/(sum(rs)-8*floor)for x in rs]
            rp0=[x-h for x,h in zip(rs,hs)]
            insist(sum(hs)==eps and sum(rp0)==8 and min(rp0)>=floor,
                   'every literal floor-preserving clipping identity')
            insist(all(0<=h<=x-floor for x,h in zip(rs,hs)),
                   'all eight displacement domains')
    lj=Q(5,18)*(Q(27,40)+Q(5,9)*(8+eps)/7)**7
    lo=Q(9)*Q(27,40)/2*(1+Q(27,40)*(8+eps)/7)**7
    insist(lj<2 and lo<171 and 1-2*eps>Q(49,50),
           'fresh full seven-factor annular clipping bounds')
    L,U,W=Q(2,3),Q(7,8),Q(1,16)
    for u in [L,(L+U)/2,U]:
        insist(u*u+W<=(u+W/(2*L))**2,'positive actual linear norm denominator')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','literal_original_channels':controls,
            'marked_collision_branch':True,'quartic_controls':quartics,'whole_centered_products':products,
            'actual_norm_distinction':{'actual_norm_square':str(mu*mu),'synchronized_coefficient':str(lower*lower),
                                      'beta_minus_actual':str(envelope-actual)},
            'clipping':{'epsilon':str(eps),'radii':list(map(str,r)),'clipped':list(map(str,rp))},
            'J_Lipschitz':2,'O_Lipschitz':171,'eight_factor_product_ratio':str(P/Pp)}

if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
