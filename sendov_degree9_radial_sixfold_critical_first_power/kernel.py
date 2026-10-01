"""Radial critical6+1+1 origin polynomials over Q[b,r,s,q].

Author six-sendov-1, researcher, 2026-10-01. q=Re(v), |v|=1;
t=8-6r-s. The heavy normalized reciprocal is positive real r.
All four parameters and both complete closed cells are specified in
PROOF.md. Integer grouping changes execution only. No external data.
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb,lcm

def shift(p,e,weight=F(1)):
    return {tuple(x+y for x,y in zip(e,f)):v*weight for f,v in p.items() if v*weight}

def moments(A):
    b,r=[A.variable(i) for i in range(2)]
    powers=[A.scale(A.power(A.mul(b,r),j),F((-1)**j*comb(6,j))) for j in range(7)]
    return [A.scale(A.mul(A.power(b,k),A.add(*(A.scale(p,F(1,j+k+1))
            for j,p in enumerate(powers)))),9) for k in range(3)]

def endpoint_moments(A):
    """Independent endpoint sums in h=1-br, including b=0 by identity."""
    b,r=[A.variable(i) for i in range(2)]
    h=A.add(A.ONE,A.scale(A.mul(b,r),-1));pw=[A.power(h,j) for j in range(7)]
    return [A.scale(A.add(*pw),F(9,7)),
      A.scale(A.mul(b,A.add(*(A.scale(p,F(j+1)) for j,p in enumerate(pw)))),F(9,56)),
      A.scale(A.mul(A.power(b,2),A.add(*(A.scale(p,F((j+1)*(j+2)))
          for j,p in enumerate(pw)))),F(1,56))]

def data(A):
    b,r,s,q=[A.variable(i) for i in range(4)]
    AA,BB,CC=moments(A)
    t=A.add(A.scale(A.ONE,8),A.scale(r,-6),A.scale(s,-1))
    PA=A.add(A.power(AA,2),A.mul(A.power(s,2),A.power(BB,2)),
            A.scale(A.mul(s,A.mul(AA,A.mul(BB,q))),-2))
    PJ=A.add(A.power(BB,2),A.mul(A.power(s,2),A.power(CC,2)),
            A.scale(A.mul(s,A.mul(BB,A.mul(CC,q))),-2))
    R=A.mul(A.power(r,12),A.mul(A.power(s,2),A.power(t,2)))
    L=A.add(PA,A.mul(A.power(t,2),PJ),A.scale(R,-1))
    FF=A.add(A.power(L,2),A.scale(A.mul(A.power(t,2),A.mul(PA,PJ)),-4))
    # H is evaluated at q=1; L(q)>=L(1) on physical q<=1.
    h=A.add(L,A.scale(R,F(-1,8)))
    H=A.add(*[{(e[0],e[1],e[2],0):v} for e,v in h.items()])
    z=A.variable(3)
    T0=A.add(A.ONE,A.scale(A.power(s,2),-1),A.mul(A.power(b,2),A.power(s,2)))
    Td=A.add(T0,A.mul(A.add(A.scale(A.mul(b,s),2),A.scale(T0,-1)),z))
    return {'moments':[AA,BB,CC],'PA':PA,'PJ':PJ,'R':R,'L':L,'F':FF,'H':H,'Td':Td}

def check_kernel(A,d,require):
    require(d['moments']==endpoint_moments(A),'Complete endpoint/binomial moments differ')
    b,r,s,q=[A.variable(i) for i in range(4)]
    AA,BB,CC=d['moments'];t=A.add(A.scale(A.ONE,8),A.scale(r,-6),A.scale(s,-1))
    y=A.add(A.ONE,A.scale(A.power(q,2),-1))
    PA=A.add(A.power(A.add(AA,A.scale(A.mul(s,A.mul(BB,q)),-1)),2),
             A.mul(A.power(A.mul(s,BB),2),y))
    PJ=A.add(A.power(A.add(BB,A.scale(A.mul(s,A.mul(CC,q)),-1)),2),
             A.mul(A.power(A.mul(s,CC),2),y))
    require(PA==d['PA'] and PJ==d['PJ'],'Complete Gaussian norm identities differ')
    alt=A.add(A.power(A.add(PA,A.scale(A.mul(A.power(t,2),PJ),-1),
                            A.scale(d['R'],-1)),2),
              A.scale(A.mul(d['R'],A.mul(A.power(t,2),PJ)),-4))
    require(alt==d['F'],'Complete alternate discriminant identity differs')

def phase(A,p,T):
    """Disk q=T/(2bs); all denominator powers cancel monomial by monomial."""
    powers=[A.power(T,j) for j in range(max(e[3] for e in p)+1)]
    parts=[]
    for (i,j,k,l),v in p.items():
        if min(i-l,k-l)<0:raise ArithmeticError('Phase cancellation fails')
        parts.append(shift(powers[l],(i-l,j,k-l,0),v/2**l))
    return A.add(*parts)

def horner(A,p,axis,num,den):
    """Independent homogeneous coefficient-group Horner substitution."""
    degree=max(e[axis] for e in p);groups=[{} for _ in range(degree+1)]
    for e,v in p.items():
        f=list(e);f[axis]=0;groups[e[axis]][tuple(f)]=v
    out=groups[degree];dp=[A.power(den,j) for j in range(degree+1)]
    for k in range(degree-1,-1,-1):
        out=A.add(A.mul(out,num),A.mul(groups[k],dp[degree-k]))
    return out,degree

def radial(A,p):
    """Clear (1+b)^M and group identical radial powers; exact integers."""
    clear=max(e[1]+e[2] for e in p);groups=defaultdict(list)
    for (i,j,k,l),v in p.items():groups[(j,k)].append((i,l,v))
    b,x,y=[A.variable(i) for i in range(3)]
    D=A.add(A.ONE,b);RN=A.add(A.ONE,A.scale(A.mul(b,x),F(4,3)))
    SN=A.add(A.ONE,A.scale(A.mul(A.mul(b,A.add(A.ONE,A.scale(x,-1))),y),4))
    rp=[A.power(RN,j) for j in range(max(j for j,k in groups)+1)]
    sp=[A.power(SN,k) for k in range(max(k for j,k in groups)+1)]
    dp=[A.power(D,j) for j in range(clear+1)]
    vd=lcm(*(v.denominator for v in p.values()));rd=3**max(j for j,k in groups)
    out=defaultdict(int)
    for (j,k),terms in groups.items():
        basis=A.mul(rp[j],A.mul(sp[k],dp[clear-j-k]))
        ints=[(e,int(v*rd)) for e,v in basis.items()]
        if any(F(v,rd)!=basis[e] for e,v in ints):raise ArithmeticError('Radial denominator fails')
        for i,l,v in terms:
            coeff=int(v*vd)
            if F(coeff,vd)!=v:raise ArithmeticError('Input denominator fails')
            for (ei,ej,ek,el),w in ints:out[(ei+i,ej,ek,el+l)]+=coeff*w
    return {e:F(v,vd*rd) for e,v in out.items() if v},clear

def mapped(A,d,require,progress=None):
    b,s=A.variable(0),A.variable(2)
    phased=phase(A,d['F'],d['Td'])
    den=A.scale(A.mul(b,s),2)
    ref,degree=horner(A,d['F'],3,d['Td'],den)
    require(ref==A.mul(A.power(den,degree),phased),'Complete disk phase Horner identity fails')
    out={}
    b,x,y=[A.variable(i) for i in range(3)]
    D=A.add(A.ONE,b);RN=A.add(A.ONE,A.scale(A.mul(b,x),F(4,3)))
    SN=A.add(A.ONE,A.scale(A.mul(A.mul(b,A.add(A.ONE,A.scale(x,-1))),y),4))
    for name,p in [('H',d['H']),('disk',phased)]:
        transformed,clear=radial(A,p)
        ref,j=horner(A,p,1,RN,D)
        ref,k=horner(A,ref,2,SN,D)
        require(j+k>=clear and ref==A.mul(transformed,A.power(D,j+k-clear)),
                'Complete radial nested Horner identity fails '+name)
        out[name]=(transformed,clear)
        if progress:progress('complete phase/radial identities '+name)
    return out
