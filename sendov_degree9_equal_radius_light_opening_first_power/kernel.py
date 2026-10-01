"""Exact reflection opening kernel over Q[b,r,x,z].

Author six-sendov-1, researcher, 2026-10-01. x=Re(U), |U|=r,
Im(U)^2=r^2-x^2. Moment/transform patterns retain a729b0d provenance
listed in LITERATURE.md. All new coefficients and signs regenerate.
"""
from fractions import Fraction as F
from math import comb

def horner(A,p,axis,num,den):
    degree=max(e[axis] for e in p);groups=[{} for _ in range(degree+1)]
    for e,v in p.items():
        f=list(e);f[axis]=0;groups[e[axis]][tuple(f)]=v
    out=groups[degree];dp=[A.power(den,j) for j in range(degree+1)]
    for k in range(degree-1,-1,-1):
        out=A.add(A.mul(out,num),A.mul(groups[k],dp[degree-k]))
    return out,degree

def substitute(A,p,axis,num):
    pw=[A.power(num,j) for j in range(max(e[axis] for e in p)+1)]
    out=[]
    for e,v in p.items():
        f=list(e);f[axis]=0
        out.append({tuple(i+j for i,j in zip(f,k)):v*c for k,c in pw[e[axis]].items()})
    return A.add(*out)

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

def build(A,require):
    b,r,x,z=[A.variable(i) for i in range(4)]
    r2=A.power(r,2);Y2=A.add(r2,A.scale(A.power(x,2),-1))
    real=[A.ONE,x]
    for j in range(2,7):
        real.append(A.add(A.scale(A.mul(x,real[-1]),2),A.scale(A.mul(r2,real[-2]),-1)))
    moments=[];coeffs=[]
    for l in range(3):
        coeff=[F(9*(-1)**j*comb(6,j),j+l+1) for j in range(7)];coeffs.append(coeff)
        moments.append(csum(A,[cscale(A,cmulreal(A,cpower(A,(x,A.ONE),j,Y2),A.power(b,j+l)),coeff[j])
                              for j in range(7)]))
    H=(A.add(A.ONE,A.scale(A.mul(b,x),-1)),A.scale(b,-1))
    powers=[cpower(A,H,j,Y2) for j in range(7)]
    endpoint=[cscale(A,csum(A,powers),F(9,7)),
      cscale(A,cmulreal(A,csum(A,[cscale(A,p,j+1) for j,p in enumerate(powers)]),b),F(9,56)),
      cscale(A,cmulreal(A,csum(A,[cscale(A,p,(j+1)*(j+2)) for j,p in enumerate(powers)]),A.power(b,2)),F(1,56))]
    require(endpoint==moments,'Complete endpoint/binomial complex moment identity fails')
    def gaussian(p,q):return A.add(A.mul(p[0],q[0]),A.mul(Y2,A.mul(p[1],q[1])))
    def chebyshev(l,m):
        return A.add(*(A.scale(A.mul(A.power(b,j+k+l+m),
             A.mul(A.power(r,2*min(j,k)),real[abs(j-k)])),coeffs[l][j]*coeffs[m][k])
             for j in range(7) for k in range(7)))
    grams=[]
    for l,m in [(1,0),(1,1),(1,2)]:
        g=chebyshev(l,m)
        require(g==gaussian(moments[l],moments[m]),'Complete Chebyshev/Gaussian Gram identity fails')
        grams.append(g)
    s=A.add(A.scale(A.ONE,4),A.scale(r,-3))
    T=A.add(grams[0],A.scale(A.mul(s,grams[1]),-2),A.mul(A.power(s,2),grams[2]))
    I1=csum(A,[moments[0],cmulreal(A,moments[1],A.scale(s,-2)),cmulreal(A,moments[2],A.power(s,2))])
    require(T==gaussian(moments[1],I1),'Complete opening Gram identity fails')
    require(all(e[0]>0 for e in T),'Missing exact b factor')
    tb={(e[0]-1,*e[1:]):v for e,v in T.items()}
    X=A.add(r,A.scale(A.mul(A.add(A.ONE,A.scale(b,-1)),A.add(A.ONE,A.scale(z,-1))),-1))
    phase,n=horner(A,tb,2,X,A.ONE)
    require(phase==substitute(A,tb,2,X),'Complete phase Horner/substitution identity fails')
    phase={(e[0],e[1],e[3],0):v for e,v in phase.items()}
    D=A.add(A.ONE,b);RN=A.add(D,A.scale(A.mul(b,A.variable(1)),F(1,3)))
    mapped,clear=horner(A,phase,1,RN,D)
    require(clear==14,'Wrong exact denominator clearing')
    rp=[A.power(RN,j) for j in range(clear+1)];dp=[A.power(D,j) for j in range(clear+1)]
    direct=[]
    for e,v in phase.items():
        basis=A.mul(rp[e[1]],dp[clear-e[1]]);shift=(e[0],0,e[2],0)
        direct.append({tuple(i+j for i,j in zip(shift,k)):v*c for k,c in basis.items()})
    require(mapped==A.add(*direct),'Complete homogeneous/Horner radius identity fails')
    margin=A.add(mapped,A.scale(A.power(D,clear),F(-1,128)))
    return {'moments':moments,'grams':grams,'T':T,'T_over_b':tb,'phase':phase,
            'mapped':mapped,'margin':margin,'clear':clear}
