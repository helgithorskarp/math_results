"""Exact sparse-primitive/Chebyshev boundary continuation equations."""
from fractions import Fraction as F
from math import comb

from series import series_ring, binomial_series

from arithmetic import K, require


def constants():
    c=K((0,1,0));d=2*c*c-1
    y=1/(3*(1+c));H=14*y;U=-8*(F(2,3)-y)
    rho=(c-5)/3;uz=(U+rho*H)/8;up=uz-rho*H/2
    alpha=K((-F(9914,243),-F(902885,3888),F(23464,81)))
    return dict(c=c,d=d,H=H,U=U,uz=uz,up=up,alpha=alpha)


def polynomial(eta,u0,u1,T):
    S=type(eta)
    r=eta*u0
    delta=eta*(u0-u1)
    B=delta*delta+eta*T
    coefficients=[S(0) for _ in range(10)]
    powers=[(-r)**j for j in range(10)]
    for n,multiplier in [(9,S(1)),(8,delta*F(9,4)),(7,B*F(9,7))]:
        for j in range(n+1):
            coefficients[j] += multiplier*powers[n-j]*comb(n,j)
    A=1-eta-r
    coefficients[0] -= A**9+delta*A**8*F(9,4)+B*A**7*F(9,7)
    return coefficients


def circle(coefficients,t):
    S=type(t)
    U=[S(1),2*t]
    T=[S(1),t]
    for j in range(2,10):
        U.append(2*t*U[-1]-U[-2])
        T.append(2*t*T[-1]-T[-2])
    imag=sum((coefficients[j]*U[j-1] for j in range(1,10)),S(0))
    real=sum((coefficients[j]*T[j] for j in range(10)),S(0))
    return imag,real


def solve(order,u0coeff,coefficient=K,audit=None):
    check = audit.check if audit is not None else require
    S=series_ring(order,coefficient)
    eta=S([0,1])
    C=constants()
    u0=S(u0coeff)
    u1=S((coefficient(C['U'])-6*u0.a[0])/2)
    T=S(C['H']/2)
    abscissas=[coefficient(-F(1,2)),coefficient(-C['c'])]
    t=[S(x) for x in abscissas]
    A=[coefficient(F(3,2)),coefficient(1+C['c'])]
    B=[coefficient(F(3,2)),coefficient(1-C['d'])]
    M=[[a*F(9,4),-b*F(9,7)] for a,b in zip(A,B)]
    determinant=M[0][0]*M[1][1]-M[0][1]*M[1][0]
    check(determinant != 0,'two-normal leading Jacobian')
    phase_derivative=[coefficient(-9)/(1-x*x) for x in abscissas]
    trace=[]
    for j in range(1,order+1):
        p=polynomial(eta,u0,u1,T)
        residual=[circle(p,t[k])[1].a[j] for k in range(2)]
        if j==1:
            check(all(x==0 for x in residual),'leading saturated roots')
        else:
            du=(-residual[0]*M[1][1]+residual[1]*M[0][1])/determinant
            dT=(-M[0][0]*residual[1]+M[1][0]*residual[0])/determinant
            u1=u1.with_coefficient(j-1,du)
            T=T.with_coefficient(j-1,dT)
            p=polynomial(eta,u0,u1,T)
        for k in range(2):
            imaginary=circle(p,t[k])[0].a[j]
            t[k]=t[k].with_coefficient(j,-imaginary/phase_derivative[k])
        p=polynomial(eta,u0,u1,T)
        for k in range(2):
            ii,rr=circle(p,t[k])
            check(all(ii.a[n]==0 for n in range(j+1)),'exact phase constraint order '+str(j))
            check(all(rr.a[n]==0 for n in range(j+1)),'exact radial constraint order '+str(j))
        trace.append({'order':j,'u1':u1.a[j-1].record(),'T':T.a[j-1].record(),
            't3':t[0].a[j].record(),'t4':t[1].a[j].record()})
    A=1-eta*(1+u0)
    pair_distance=(1-eta*(1+u1))**2+eta*T
    objective=6*A.inv()+2*binomial_series(pair_distance,F(-1,2))
    return objective,dict(u0=u0,u1=u1,T=T,t3=t[0],t4=t[1]),trace

