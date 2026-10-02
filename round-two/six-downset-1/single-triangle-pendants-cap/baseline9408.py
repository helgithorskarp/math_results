"""Literal original-set capped seed for a triangle facet and pendant.

The finite n<=6,N<=80 guards control validation, not the uniform proof.
The complete all-n construction is given in PROOF.md.
"""
from fractions import Fraction as F
from exact import gram, dot, matvec, vecadd, scale, unit, psd_rank, require, lift, check

def build(n):
    require(type(n) is int and 3 <= n <= 6, 'literal cube guard')
    q=1 << (n-1); s=q+3; w=F(s-1); N=2*q+8
    require(N <= 80, 'literal matrix guard')
    old=list(range(1,2*q)); oldN=len(old); full=2*q-1; m=oldN+4
    C0=[[F(s*(a==b)+(q-3)*(a^b==full)-1) for b in old] for a in old]
    H=[[-F(bool(a & (1 << j))) for a in old] for j in range(2)]
    marks=[0,0,0,1]
    co=[unit(oldN,j) for j in range(oldN)]+[scale(F(1,3),H[j]) for j in marks]
    residual=[[F(0)]*m for _ in range(m)]
    for i in range(4):
        for j in range(4):
            if marks[i]==marks[j]:residual[oldN+i][oldN+j]=F(s)*((i==j)-F(1,3))
    B=gram(C0,co,residual)
    G=[F(i<oldN) for i in range(m)]
    V=[unit(m,oldN+i) for i in range(4)]
    h=scale(F(1,3),vecadd(*V[:3])); T=[vecadd(v,scale(-1,h)) for v in V[:3]]
    K=vecadd(G,*V)
    d=F(3*(q-6),5*q)
    g=F(q-4,5*(q+2))
    b=(d*(q-1)/(q+1)-g)/2
    a=-b*(q+1)/(q-1);f=-2*a-d;e=-g-2*b;c=(a-d)*q/s
    common=vecadd(scale(F(-1,5),K),scale(a,h),scale(b,V[3]))
    P=[vecadd(common,scale(c,T[1])),vecadd(common,scale(c,T[0])),
       vecadd(scale(F(-1,5),K),scale(d,h),scale(e,V[3])),
       vecadd(scale(F(-1,5),K),scale(f,h),scale(g,V[3]),scale(c,T[2]))]
    Pgram=gram(B,P,[[F(0)]*4 for _ in range(4)])
    eta=[w-Pgram[i][i] for i in range(4)]
    require(eta[0]==eta[1], 'u/v symmetry')
    r=-1-Pgram[0][2]
    require(r==-1-Pgram[1][2], 'both facet intersections')
    t=(eta[2]+2*r-eta[3])/2
    W=[[F(0)]*4 for _ in range(4)]
    for i in range(4):W[i][i]=eta[i]
    W[0][2]=W[2][0]=W[1][2]=W[2][1]=r
    W[0][3]=W[3][0]=W[1][3]=W[3][1]=t
    W[2][3]=W[3][2]=-eta[2]-2*r
    W[0][1]=W[1][0]=-eta[0]-r-t
    require(all(sum(row)==0 for row in W),'complete residual row-zero')
    family=list(range(2*q)); u=1<<n; v=1<<(n+1); bmask=1<<(n+2)
    family.extend([u,1|u,v,1|v,u|v,1|u|v,bmask,2|bmask])
    coeff=[unit(m,i) for i in range(oldN)]
    for i in range(4):coeff.extend([P[i],V[i]])
    totalres=[[F(0)]*(N-1) for _ in range(N-1)]
    for i in range(4):
        for j in range(4):totalres[oldN+2*i][oldN+2*j]=W[i][j]
    C=gram(B,coeff,totalres)
    require([C[i][i] for i in range(N-1)]==[w]*(N-1),'all actual norms')
    for i,A in enumerate(family[1:]):
        for j,Bmask in enumerate(family[1:]):
            if i!=j and A&Bmask:require(C[i][j]==-1,'mandatory Gram intersection')
    require(sum(map(sum,C))==F(5*q-4,25),'actual empty squared norm')
    return family,s,C,W,{'n':n,'q':q,
                        'eta':[str(z) for z in eta], 'residual':[[str(z) for z in row] for row in W]}
