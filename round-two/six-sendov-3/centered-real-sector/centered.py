"""Exact split forcing and one covered centered-real curvature enclosure.

Ordinary coverage and Hessian interpretation are proved in PROOF.md.
The box and precision are exactly those already certified in source7bb2d1.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import K,require
from series import series_ring
from initial import constants,inverse
from system import system
import interval as iv
from interval import I,J


def forcing(eta,variables,c):
    S=type(eta);x,y,T,xi3,xi4,omega=variables
    r=eta*x;Delta=eta*(x-y);B=Delta*Delta+eta*T;a=1-eta
    poly=[S(0) for _ in range(8)]
    for n,m in ((7,S(-F(9,7))),(6,-3*Delta),(5,-F(9,5)*B)):
        for j in range(n+1):poly[j]+=m*comb(n,j)*(-r)**(n-j)
    poly[0]=-sum((poly[j]*a**j for j in range(1,8)),S(0))
    out=[]
    for t in (S(-F(1,2))+eta*xi3,S(-c)+eta*xi4):
        U=[S(1),2*t];V=[S(1),t]
        for _ in range(2,8):U.append(2*t*U[-1]-U[-2]);V.append(2*t*V[-1]-V[-2])
        out.append((sum((poly[j]*U[j-1] for j in range(1,8)),S(0)),
                    sum((poly[j]*V[j] for j in range(8)),S(0))))
    return [out[0][0],out[1][0],out[0][1],out[1][1],S(0)],poly


def exact():
    c,d,values=constants();Dual=series_ring(1,K);S=series_ring(2,Dual);eta=S([0,1]);columns=[]
    for axis in range(1,6):
        eq,_=system(eta,[S(Dual([v,int(axis==j)])) for j,v in enumerate(values)],c)
        columns.append([[f.a[n].a[1] for f in eq[:5]] for n in (1,2)])
    B0=[list(row) for row in zip(*(col[0] for col in columns))]
    B1=[list(row) for row in zip(*(col[1] for col in columns))];Y=inverse(B0)
    # General first-order primitive: z^9-1+eta*[9+b8(z^8-1)+b7(z^7-1)],
    # b8=-9(3x+y)/4, b7=9T/7. Hence H_first5(0,v) is affine for every v.
    formula_imag=[];formula_real=[];formula_U=[]
    for t in (K(-F(1,2)),-c):
        u=[K(1),2*t];up=[K(0),K(2)];v=[K(1),t]
        for _ in range(2,10):
            up.append(2*u[-1]+2*t*up[-1]-up[-2])
            u.append(2*t*u[-1]-u[-2]);v.append(2*t*v[-1]-v[-2])
        require(u[8]==0,'fixed phases are ninth roots')
        formula_imag.append((-F(9,4)*u[7],F(9,7)*u[6],up[8]))
        formula_real.append((-F(9,4)*(v[8]-1),F(9,7)*(v[7]-1)))
        formula_U.append((-F(9,7)*u[6],-F(9,7)*(v[7]-1)))
    formula_B=[
        [*formula_imag[0][:2],formula_imag[0][2],K(0),K(0)],
        [*formula_imag[1][:2],K(0),formula_imag[1][2],K(0)],
        [*formula_real[0],K(0),K(0),K(0)],
        [*formula_real[1],K(0),K(0),K(0)],
        [K(2),K(-1),K(0),K(0),K(2)]]
    require(B0==formula_B,'all25 entries of affine first-order constraint formula')
    E=series_ring(1,K);u,_=forcing(E([0,1]),[E(v) for v in values],c)
    U0=[f.a[0] for f in u];U1=[f.a[1] for f in u]
    require(U0==[formula_U[0][0],formula_U[1][0],formula_U[0][1],formula_U[1][1],K(0)],
            'all5 entries of universal initial split forcing')
    w0=[K(0),K(1),K(0),K(0),K(F(1,2))]
    require(all(sum((a*b for a,b in zip(row,w0)),K(0))+u==0 for row,u in zip(B0,U0)),
            'complete initial forcing response')
    rhs=[-u-sum((a*b for a,b in zip(row,w0)),K(0)) for row,u in zip(B1,U1)]
    w1=[sum((a*b for a,b in zip(row,rhs)),K(0)) for row in Y]
    ell=6*(1+values[0])+2*values[5]-2*w1[-1]
    require(ell==K((-F(4441,540),F(7046,135),-F(2288,45))),
            'exact centered curvature reproduces reviewed9033/9080 coefficient')
    return values,Y,w0,w1,{'initial_five_block':[[v.record() for v in row] for row in B0],
        'initial_five_block_eta_derivative':[[v.record() for v in row] for row in B1],
        'initial_five_block_inverse':[[v.record() for v in row] for row in Y],
        'initial_forcing':[v.record() for v in U0],
        'initial_forcing_eta_derivative':[v.record() for v in U1],
        'initial_response':[v.record() for v in w0],
        'initial_response_eta_derivative':[v.record() for v in w1],'reviewed_ell':ell.record()}


def embedding():
    lo,hi=F(3,4),F(1);f=lambda t:8*t*t*t-6*t-1
    require(f(lo)<0<f(hi),'embedding bracket')
    for _ in range(160):
        mid=(lo+hi)/2
        if f(mid)<0:lo=mid
        else:hi=mid
    require(f(lo)<0<f(hi) and 24*lo*lo>6,'unique real embedding')
    return I.bounds(lo,hi)


def enclose(k,c):return I(k.a[0])+I(k.a[1])*c+I(k.a[2])*c.square()
def matvec(a,v):return [sum((x*y for x,y in zip(row,v)),I(0)) for row in a]
def norm(a):return F(max(sum(v.absmax() for v in row) for row in a),iv.DEN)


def certify(values,Yexact,w0exact,w1exact,damage=None):
    c=embedding();e=F(1,65536);rho=F(1,1024)
    center=[enclose(v,c) for v in values]
    box=[v+I.bounds(-rho,rho) for v in center]
    eta=J.eta(I.bounds(0,e));v=[J.parameter(b,i) for i,b in enumerate(box)]
    G,aux=system(eta,v,c);U,_=forcing(eta,v,c)
    B=[[f.g[1][j] for j in range(1,6)] for f in G[:5]]
    B1=[[f.g[2][j] for j in range(1,6)] for f in G[:5]]
    if damage=='lost-second-mixed':B1=[[I(0) for _ in row] for row in B1]
    U1=[f.f[1] for f in U]
    Y=[[enclose(t,c) for t in row] for row in Yexact]
    w0=[enclose(t,c) for t in w0exact];w1=[enclose(t,c) for t in w1exact]
    defect=[[I(int(i==j))-sum((Y[i][k]*B[k][j] for k in range(5)),I(0)) for j in range(5)] for i in range(5)]
    beta=norm(defect);require(beta<F(1,50),'five-constraint inverse defect below1/50')
    # B1 encloses (Bactual-B0)/eta by its normalized integral of G_eta_eta_v.
    # U1 encloses (Uactual-U0)/eta by its integral of U_eta.
    rhs=[-u-v for u,v in zip(U1,matvec(B1,w0))]
    residual=[r-b for r,b in zip(rhs,matvec(B,w1))]
    pre=matvec(Y,residual)
    error=F(max(t.absmax() for t in pre),iv.DEN)/(1-beta)
    require(error<F(9,20),'centered response error below9/20')
    actual_w1=[t+I.bounds(-error,error) for t in w1]
    A=aux['A'].f[0];W=aux['W'].f[0];et=eta.f[0];alpha=1+box[0];omega=box[5]
    require(A.lo>0 and W.lo>0,'positive curvature denominators')
    L=2*alpha*(3-3*et*alpha+et.square()*alpha.square())/(A**3)+omega*(2+et*omega)/W.square()-2*actual_w1[-1]/W.square()
    if damage=='curvature-sign':L=2*alpha*(3-3*et*alpha+et.square()*alpha.square())/(A**3)+omega*(2+et*omega)/W.square()+2*actual_w1[-1]/W.square()
    require(L.lo>I(-5).hi and L.hi<I(-3).lo,'strict centered-real relative-curvature window(-5,-3)')
    return {'precision_bits':iv.BITS,'eta_interval':['0',str(e)],'parameter_radius':str(rho),
        'c_interval':c.record(),'center':[v.record() for v in center],
        'five_block_enclosure':[[v.record() for v in row] for row in B],
        'five_block_eta_difference_quotient_enclosure':[[v.record() for v in row] for row in B1],
        'forcing_eta_difference_quotient_enclosure':[v.record() for v in U1],
        'five_block_defect':[[v.record() for v in row] for row in defect],
        'five_block_beta':str(beta),'preconditioned_response_residual':[v.record() for v in pre],
        'response_error':str(error),'response_next_eta_coefficient_enclosure':[v.record() for v in actual_w1],
        'relative_curvature_difference_quotient':L.record(),
        'target_minus5_minus3':L.lo>I(-5).hi and L.hi<I(-3).lo}
