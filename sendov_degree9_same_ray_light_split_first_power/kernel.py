"""Exact heavy-moment dominance kernel over Q[b,r,x,z].

Actual author six-sendov-1, researcher, 2026-10-01. x=Re(U),
|U|=r. The fourth variable is eliminated after the mean substitution.
No input certificate, floating sign or imported theorem enters this code.
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
    norms=[];moments=[]
    for l in range(3):
        coeff=[F(9*(-1)**j*comb(6,j),j+l+1) for j in range(7)]
        norms.append(A.add(*(A.scale(A.mul(A.power(b,j+k+2*l),
            A.mul(A.power(r,2*min(j,k)),real[abs(j-k)])),coeff[j]*coeff[k])
            for j in range(7) for k in range(7))))
        moments.append(csum(A,[cscale(A,cmulreal(A,cpower(A,(x,A.ONE),j,Y2),A.power(b,j+l)),coeff[j])
                              for j in range(7)]))
    # Independent endpoint sums, T=1-bU, in the same quadratic extension.
    T=(A.add(A.ONE,A.scale(A.mul(b,x),-1)),A.scale(b,-1))
    powers=[cpower(A,T,j,Y2) for j in range(7)]
    endpoint=[cscale(A,csum(A,powers),F(9,7)),
      cscale(A,cmulreal(A,csum(A,[cscale(A,p,j+1) for j,p in enumerate(powers)]),b),F(9,56)),
      cscale(A,cmulreal(A,csum(A,[cscale(A,p,(j+1)*(j+2)) for j,p in enumerate(powers)]),A.power(b,2)),F(1,56))]
    require(endpoint==moments,'Complete binomial/endpoint complex moments differ')
    for norm,p in zip(norms,moments):
        square=A.add(A.power(p[0],2),A.mul(Y2,A.power(p[1],2)))
        require(square==norm,'Complete Chebyshev/Gaussian norm identity differs')
    S=A.add(A.scale(A.ONE,8),A.scale(r,-6))
    E=A.add(norms[0],A.scale(A.mul(A.power(S,2),norms[1]),-2),
            A.scale(A.mul(A.power(S,4),norms[2]),F(-1,8)))
    X=A.add(r,A.scale(A.mul(A.add(A.ONE,A.scale(b,-1)),A.add(A.ONE,A.scale(z,-1))),F(-4,3)))
    mean,n=horner(A,E,2,X,A.ONE)
    require(mean==substitute(A,E,2,X),'Complete heavy mean Horner/substitution identity differs')
    mean={(e[0],e[1],e[3],0):v for e,v in mean.items()}
    D=A.add(A.ONE,b);RN=A.add(D,A.scale(A.mul(b,A.variable(1)),F(1,3)))
    mapped,clear=horner(A,mean,1,RN,D)
    require(clear==16,'Wrong denominator clearing')
    # Independent direct homogeneous substitution of r=RN/D.
    rp=[A.power(RN,j) for j in range(clear+1)];dp=[A.power(D,j) for j in range(clear+1)]
    direct=[]
    for e,v in mean.items():
        basis=A.mul(rp[e[1]],dp[clear-e[1]])
        shift=(e[0],0,e[2],0)
        direct.append({tuple(i+j for i,j in zip(shift,k)):v*c for k,c in basis.items()})
    require(mapped==A.add(*direct),'Complete homogeneous/Horner radius identity differs')
    margin=A.add(mapped,A.scale(A.power(D,clear),F(-1,128)))
    return {'moments':moments,'norms':norms,'E':E,'mean':mean,'mapped':mapped,
            'margin':margin,'clear':clear}
