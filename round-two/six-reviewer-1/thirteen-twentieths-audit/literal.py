"""Separate exact Gaussian original-root/channel and perturbation controls.

No author modules, no arithmetic.py and no cover/expected record imports.
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


def main():
    controls=[]
    for a in [Q(5,8),Q(13,20)]:
        controls.append(original(a,[g(Q(1,4)),g(-Q(1,4)),g(0,Q(1,3)),g(0,-Q(1,3)),
                                    g(Q(1,2),Q(1,4)),g(Q(1,2),-Q(1,4)),g(-Q(1,3)),g(-Q(1,3))]))
        controls.append(original(a,[g(1),g(-1),g(0,1),g(0,-1),g(0),g(0),g(0,Q(1,2)),g(0,-Q(1,2))]))
    # All-equal marked multiplicity: derivative at the original zero vanishes.
    a=Q(13,20);p=[g(1)]
    for _ in range(9):p=pmul(p,[g(-a),g(1)])
    insist(peval([gs(p[i],i)for i in range(1,10)],g(a))==g(0),'multiple marked zero/pole branch')
    lower=Q(51,80);mu=Q(19,20);a=Q(13,20)
    insist(8*mu>=Q(37,5) and mu*mu>lower*lower,'synchronized beta is NOT actual norm')
    envelope=(1-a*lower)**2;actual=(1-a*mu)**2
    insist(envelope-actual==a*(mu-lower)*(2-a*(mu+lower))>0,'actual synchronized quadratic identity')
    eps=Q(1,2**22);m=1/(1+a)
    r=[m]+[(8+eps-m)/7]*7;rp=[m]+[(8-m)/7]*7
    insist(min(rp)>=m and sum(rp)==8 and sum(r)-sum(rp)==eps and
           sum(abs(x-y)for x,y in zip(r,rp))==eps,'actual radius-floor-preserving mass clipping')
    for z in [Q(0),Q(1,3),Q(1)]:
        for j in range(8):
            others=sum(r)-r[j]
            insist(a+(1-a*a)*z*others/7<2 and 1+a*z*others/7<2,'all seven factors in Lipschitz domain')
    insist(1-64*eps>Q(19999,20000) and 1+578*eps<Q(4097,4096)and Q(9,8)**8<3,
           'exact annular channel-gap constants')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'literal_original_channels':controls,'marked_collision_branch':True,
            'actual_mean_norm_counterexample':{'mu':str(mu),'actual_norm_square':str(mu*mu),
                'synchronized_coefficient':str(lower*lower),'beta_minus_actual':str(envelope-actual)},
            'radius_floor_clipping':True,'annular_epsilon':str(eps),'J_Lipschitz':64,'O_Lipschitz':576}


if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
