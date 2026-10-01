"""Polynomial equations and literal eta-scaled parameter derivatives."""
from fractions import Fraction as F
from math import comb


def system(eta,variables,c):
    S=type(eta)
    x,y,opening,xi3,xi4,omega=variables
    r=eta*x;delta=eta*(x-y);B=delta*delta+eta*opening
    shift=[S(1)];anchor=[S(1)]
    for j in range(1,10):
        shift.append(shift[-1]*(-r))
        anchor.append(anchor[-1]*(1-eta))

    def primitive(terms):
        poly=[S(0) for _ in range(10)]
        for n,multiplier in terms:
            for j in range(n+1):
                poly[j]+=multiplier*comb(n,j)*shift[n-j]
        # Q(z-r)-Q(a-r): its constant coefficient is -sum_{j>=1} b_j a^j.
        # The unanchored b_0 cancels; retaining it would misplace the marked root.
        poly[0]=-sum((poly[j]*anchor[j] for j in range(1,10)),S(0))
        return poly

    poly=primitive([(9,S(1)),(8,delta*F(9,4)),(7,B*F(9,7))])
    partials=[primitive([(8,S(-F(27,4))),(7,-F(108,7)*delta),(6,-9*B)]),
              primitive([(8,S(-F(9,4))),(7,-F(18,7)*delta)]),
              primitive([(7,S(F(9,7)))])]
    phases=[S(-F(1,2))+eta*xi3,S(-c)+eta*xi4]
    imag=[];real=[];normals=[];phase_derivatives=[]
    for t in phases:
        U=[S(1),2*t];Up=[S(0),S(2)]
        T=[S(1),t];Tp=[S(0),S(1)]
        for j in range(2,10):
            Up.append(2*U[-1]+2*t*Up[-1]-Up[-2])
            Tp.append(2*T[-1]+2*t*Tp[-1]-Tp[-2])
            U.append(2*t*U[-1]-U[-2])
            T.append(2*t*T[-1]-T[-2])
        I=sum((poly[j]*U[j-1] for j in range(1,10)),S(0))
        R=sum((poly[j]*T[j] for j in range(10)),S(0))
        It=sum((poly[j]*Up[j-1] for j in range(1,10)),S(0))
        Rt=sum((poly[j]*Tp[j] for j in range(10)),S(0))
        row=[]
        for derivative in partials:
            iv=sum((derivative[j]*U[j-1] for j in range(1,10)),S(0))
            rv=sum((derivative[j]*T[j] for j in range(10)),S(0))
            row.append(rv*It-Rt*iv)
        imag.append(I);real.append(R);normals.append(row);phase_derivatives.append(It)
    A=1-eta*(1+x);D=1-eta*(1+y);W=1+eta*omega
    P=[6*W**3,2*D*A**2,-A**2]
    u,v,w=P,normals[0],normals[1]
    station=u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])
    equations=[imag[0],imag[1],real[0],real[1],W*W-D*D-eta*opening,station]
    return equations,dict(poly=poly,partials=partials,phases=phases,
                          normals=normals,phase_derivatives=phase_derivatives,A=A,D=D,W=W)
