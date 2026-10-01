"""Exact reflected-light origin kernel and mean-loss maps.

Author six-sendov-1, researcher, 2026-10-01. Q[b,r,x,t],
U=x+iY, Y^2=r^2-x^2, s=4-3r, t=sc. Generic complex/Horner
patterns retain prior source attribution in LITERATURE.md.
No previous theorem or sign tensor is imported.
"""
from fractions import Fraction as F
from math import comb

def cmul(A,p,q,Y2):
    return (A.add(A.mul(p[0],q[0]),A.scale(A.mul(Y2,A.mul(p[1],q[1])),-1)),
            A.add(A.mul(p[0],q[1]),A.mul(p[1],q[0])))
def cpower(A,p,n,Y2):
    out=(A.ONE,{})
    for _ in range(n):out=cmul(A,out,p,Y2)
    return out
def csum(A,items):return tuple(A.add(*(p[i] for p in items)) for i in range(2))
def cscale(A,p,v):return tuple(A.scale(q,v) for q in p)
def cmulreal(A,p,v):return tuple(A.mul(q,v) for q in p)

def substitute(A,p,axis,num):
    pw=[A.power(num,j) for j in range(max(e[axis] for e in p)+1)]
    out=[]
    for e,v in p.items():
        f=list(e);f[axis]=0
        out.append({tuple(i+j for i,j in zip(f,k)):v*c for k,c in pw[e[axis]].items()})
    return A.add(*out)

def horner(A,p,axis,num,den):
    degree=max(e[axis] for e in p);groups=[{} for _ in range(degree+1)]
    for e,v in p.items():
        f=list(e);f[axis]=0;groups[e[axis]][tuple(f)]=v
    out=groups[degree];dp=[A.power(den,j) for j in range(degree+1)]
    for k in range(degree-1,-1,-1):
        out=A.add(A.mul(out,num),A.mul(groups[k],dp[degree-k]))
    return out,degree

def build(A,require):
    b,r,x,t=[A.variable(i) for i in range(4)]
    s=A.add(A.scale(A.ONE,4),A.scale(r,-3));s2=A.power(s,2)
    r2=A.power(r,2);Y2=A.add(r2,A.scale(A.power(x,2),-1))
    moments=[]
    for l in range(3):
        moments.append(csum(A,[cscale(A,cmulreal(A,cpower(A,(x,A.ONE),j,Y2),A.power(b,j+l)),
                       F(9*(-1)**j*comb(6,j),j+l+1)) for j in range(7)]))
    H=(A.add(A.ONE,A.scale(A.mul(b,x),-1)),A.scale(b,-1))
    hp=[cpower(A,H,j,Y2) for j in range(7)]
    endpoint=[cscale(A,csum(A,hp),F(9,7)),
       cscale(A,cmulreal(A,csum(A,[cscale(A,p,j+1) for j,p in enumerate(hp)]),b),F(9,56)),
       cscale(A,cmulreal(A,csum(A,[cscale(A,p,(j+1)*(j+2)) for j,p in enumerate(hp)]),A.power(b,2)),F(1,56))]
    require(endpoint==moments,'Complete endpoint/binomial moments disagree')
    II=csum(A,[moments[0],cmulreal(A,moments[1],A.scale(t,-2)),cmulreal(A,moments[2],s2)])
    # A separate coefficient expansion of the full eight-factor integrand.
    light=[A.ONE,A.scale(t,2),s2];terms=[]
    for j in range(7):
        for l in range(3):
            weight=F(9*(-1)**(j+l)*comb(6,j),j+l+1)
            terms.append(cscale(A,cmulreal(A,cpower(A,(x,A.ONE),j,Y2),
                         A.mul(A.power(b,j+l),light[l])),weight))
    require(csum(A,terms)==II,'Complete direct eight-factor moment identity fails')
    R=A.mul(A.power(r,12),A.power(s,4))
    raw=A.add(A.power(II[0],2),A.mul(Y2,A.power(II[1],2)),A.scale(R,-1))
    # Independent real-part recurrence for all coefficient cross-products.
    real=[A.ONE,x]
    for j in range(2,7):
        real.append(A.add(A.scale(A.mul(x,real[-1]),2),A.scale(A.mul(r2,real[-2]),-1)))
    cross=[]
    for j in range(7):
      for l in range(3):
       for k in range(7):
        for m in range(3):
            weight=F(81*(-1)**(j+l+k+m)*comb(6,j)*comb(6,k),(j+l+1)*(k+m+1))
            basis=A.mul(A.power(b,j+l+k+m),A.mul(A.mul(light[l],light[m]),
                         A.mul(A.power(r,2*min(j,k)),real[abs(j-k)])))
            cross.append(A.scale(basis,weight))
    require(A.add(*cross,A.scale(R,-1))==raw,'Full Chebyshev/direct squared norm disagrees')
    eps=A.add(A.ONE,A.scale(b,-1))
    X=A.add(r,A.scale(A.mul(eps,x),F(-4,3)))
    phase=substitute(A,raw,2,X)
    tn=A.add(s,A.scale(A.mul(eps,A.mul(A.add(A.ONE,A.scale(x,-1)),t)),-4))
    loss=substitute(A,phase,3,tn)
    den=A.add(A.ONE,b);dp=[A.power(den,j) for j in range(17)]
    charts={}
    for label,ratio in [('nearer',F(1,3)),('farther',F(-1))]:
        rn=A.add(den,A.scale(A.mul(b,r),ratio))
        mapped,clear=horner(A,loss,1,rn,den)
        require(clear==16,'Wrong exact radius denominator clearing')
        rp=[A.power(rn,j) for j in range(17)]
        direct=[]
        for e,v in loss.items():
            basis=A.mul(rp[e[1]],dp[16-e[1]]);shift=(e[0],0,e[2],e[3])
            direct.append({tuple(i+j for i,j in zip(shift,k)):v*c for k,c in basis.items()})
        require(mapped==A.add(*direct),'Complete homogeneous/Horner radius identity fails')
        margin=A.add(mapped,A.scale(A.mul(eps,dp[16]),-1))
        charts[label]={'mapped':mapped,'margin':margin,'clear':clear}
    return {'moments':moments,'I':II,'R':R,'raw':raw,'phase':phase,'loss':loss,'charts':charts}
