"""Closed finite mixed-profile Gram/full-frame forms for exact bridge controls.

Rational coefficient domain, q>=4 and integer r,l>=1, r+l<q. The
r=l=1 prior seed is excluded from these mean-orthogonal forms. Positivity
is checked separately; these formulas are not an all-count cap theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import require, matvec, dot, vecadd, scale, unit, zero, psd_rank

def parameters(q,r,l,mean_recipe='legacy'):
    require(q>=4 and type(r) is int and type(l) is int and r>=1 and l>=1
            and 3<=r+l<q,'two-class reduced domain')
    require(mean_recipe in ('legacy','cap-min','cap-harmonic'),'mean recipe')
    q=F(q);s=q+3;w=q+2;m=3*r+l;ell=m+1;N=2*q+6*r+2*l;t=r+l-1
    rho=(q-1)/(q+1);d=3*(q-ell-1)/(ell*q);g=(q-ell+1)/(ell*w)
    D=d;Fp=-g/rho;A=(-D-F(l,r)*Fp)/2
    a=A if r==1 else -d/3
    ast=(r*a-A)/(r-1) if r>1 else F(0)
    dst=d;gst=g
    # On absent class standard spaces, their coefficient does not matter.
    c=(a-d)*q/s; E2=q/(3*r)+rho*rho*w/l
    Di2=q*(r-1)/(3*r); Lj2=w*(l-1)/l;K2=ell*q+2-6*r
    common=K2/(ell*ell)
    etaL=w-common-A*A*E2-ast*ast*Di2-2*s*c*c/3
    etaF=w-common-D*D*E2-dst*dst*Di2-2*s*c*c*(r-1)/(3*t*t)
    etaP=w-common-Fp*Fp*E2-gst*gst*Lj2-2*s*c*c*r/(3*t*t)
    R=-1-common-A*D*E2-ast*dst*Di2
    mu=(2*R+etaF)/3;alpha=2*(2*etaL-R-etaF);beta=etaF-mu
    if r==1: cross=3*mu/l
    elif l==1: cross=etaP/(3*r)
    else:
        first=3*r*mu/l;second=l*etaP/(3*r)
        if mean_recipe=='legacy':cross=min(first,second)/2
        elif mean_recipe=='cap-min':cross=min(first,second,q/m)/2
        else:cross=1/(2*(1/first+1/second+m/q))
    a_mean=(l*cross-3*mu)/(3*(r-1)) if r>1 else None
    b_mean=(3*r*cross-etaP)/(l-1) if l>1 else None
    nuT=mu-a_mean if r>1 else None;nuL=etaP-b_mean if l>1 else None
    return locals()

def frame(G,updates,old=None):
    S=zero(len(G)) if old is None else [row[:] for row in old]
    for count,v in updates:
        image=matvec(G,v)
        for i in range(len(G)):
            for j in range(len(G)):S[i][j]+=count*image[i]*image[j]
    return S

def reduced(q,r,l,mean_recipe='legacy'):
    p=parameters(q,r,l,mean_recipe);q=p['q'];s=p['s'];N=p['N'];rho=p['rho'];t=p['t']
    A=p['A'];D=p['D'];Fp=p['Fp'];c=p['c'];beta=p['beta'];ell=p['ell']
    # Fixed8: gp,h0,sum Atri,sum Alight,sum Ts,sum Z,sum WF,sum Mtri.
    G=zero(8);diag=[q-1,F(3),3*r*(q-r),3*l*(q-l),6*r*s,F(2*l,3)*s,
                  r*beta,F(r*l,3)*p['cross']]
    for i,z in enumerate(diag):G[i][i]=z
    G[2][3]=G[3][2]=F(-3*r*l)
    h=scale(F(1,3),vecadd(unit(8,1),scale(F(1,r),unit(8,2))))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    E=vecadd(h,scale(-rho,v))
    K=vecadd(unit(8,0),scale(F(3*r+l-3,3),unit(8,1)),unit(8,2),scale(F(1,3),unit(8,3)),unit(8,5))
    common=scale(F(-1,ell),K)
    vmL=vecadd(h,scale(F(1,6*r),unit(8,4)))
    vmF=vecadd(h,scale(F(-1,3*r),unit(8,4)))
    upL=vecadd(common,scale(A,E),scale(c/(6*r),unit(8,4)),
               scale(F(1,r),unit(8,7)),scale(F(-1,2*r),unit(8,6)))
    upF=vecadd(common,scale(D,E),scale(-c*(r-1)/(3*r*t),unit(8,4)),
               scale(F(1,r),unit(8,7)),scale(F(1,r),unit(8,6)))
    upP=vecadd(common,scale(Fp,E),scale(-c/(3*t),unit(8,4)),scale(F(-3,l),unit(8,7)))
    old=zero(8);old[0][0]=q*q-1;old[0][1]=old[1][0]=3*(q-1);old[1][1]=F(9)
    for i in (2,3):
        for j in (2,3):old[i][j]=6*G[i][j]
    S=frame(G,[(2*r,vmL),(r,vmF),(l,v),(2*r,upL),(r,upF),(l,upP),(1,common)],old)
    out={'fixed':(G,S)}
    # A single leaf flip, with all other sectors orthogonal.
    G=zero(2);G[0][0]=2*s;G[1][1]=p['alpha']
    S=frame(G,[(F(1,2),[F(1),F(0)]),(F(1,2),[-c,F(1)])])
    out['anti']=(G,S)
    if r>1:
        G=zero(4)
        for i,z in enumerate([6*q,12*s,2*p['nuT'],2*beta]):G[i][i]=z
        old=zero(4);old[0][0]=6*G[0][0]
        S=frame(G,[(4,[F(1,6),F(1,12),F(0),F(0)]),
                   (2,[F(1,6),F(-1,6),F(0),F(0)]),
                   (4,[p['ast']/6,c/12,F(1,2),F(-1,4)]),
                   (2,[p['dst']/6,c/(6*t),F(1,2),F(1,2)])],old)
        out['triangle_standard']=(G,S)
    if l>1:
        G=zero(3)
        for i,z in enumerate([6*q,F(4,3)*s,2*p['nuL']]):G[i][i]=z
        old=zero(3);old[0][0]=6*G[0][0]
        S=frame(G,[(2,[F(1,6),F(1,2),F(0)]),
                   (2,[p['gst']/6,p['gst']/2,F(1,2)])],old)
        out['pendant_standard']=(G,S)
    return out,p

def check_reduced(q,r,l,mean_recipe='legacy'):
    sectors,p=reduced(q,r,l,mean_recipe)
    for label,(G,S) in sectors.items():
        require(psd_rank(G)==len(G),'positive Gram '+label)
        B=[[(p['N']-1)*G[i][j]-S[i][j] for j in range(len(G))] for i in range(len(G))]
        require(psd_rank(B)==len(G),'strict cap1 '+label)
    return sectors,p
