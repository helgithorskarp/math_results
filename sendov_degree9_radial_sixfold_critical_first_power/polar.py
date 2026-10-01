"""Full complex critical6+1+1 polar estimate in Q[a,v,theta,tau].

Author six-sendov-1, researcher, 2026-10-01. The envelope uses the
light-radius variance maximum, not equality of the two light radii.
All geometric monotonicity and derivative deductions are in PROOF.md.
"""
from fractions import Fraction as F
from math import factorial

def quadratics(A):
    a,v,h,t=[A.variable(i) for i in range(4)];eps=A.add(A.ONE,A.scale(a,-1))
    R=A.add(A.ONE,A.scale(A.mul(a,v),F(4,3)))
    S=A.add(A.ONE,A.scale(A.mul(a,A.add(A.ONE,A.scale(v,-1))),8))
    heavy=[A.power(a,2),
      A.add(A.scale(A.mul(A.mul(a,eps),R),2),
       A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(A.ONE,a)),h),F(-8,3))),
      A.power(A.mul(eps,R),2)]
    light=[A.scale(A.power(a,2),2),
      A.add(A.scale(A.mul(A.mul(a,eps),A.add(A.ONE,S)),2),
       A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(A.ONE,a)),
                         A.add(A.ONE,A.scale(h,-1))),-16)),
      A.mul(A.power(eps,2),A.add(A.ONE,A.power(S,2)))]
    return heavy,light

def integral(A):
    heavy,light=quadratics(A);tau=A.variable(3)
    X=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(heavy)))
    Y=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(light)))
    raw=A.scale(A.mul(A.power(X,3),Y),F(1,2))
    return A.add(*[{(e[0],e[1],e[2],0):f/F(e[3]+1)} for e,f in raw.items()])

def alternate_integral(A):
    """Independent complete multinomial moment construction."""
    X,Y=quadratics(A);out={}
    for i in range(4):
      for j in range(4-i):
        k=3-i-j
        heavy=A.mul(A.power(X[0],i),A.mul(A.power(X[1],j),A.power(X[2],k)))
        for ell in range(3):
            weight=F(factorial(3),2*factorial(i)*factorial(j)*factorial(k)*(j+2*k+ell+1))
            out=A.add(out,A.scale(A.mul(heavy,Y[ell]),weight))
    return out

def divide(A,p):
    """Exact division by (1-a)^2; remainder must vanish."""
    eps=A.add(A.ONE,A.scale(A.variable(0),-1));work=dict(p);out={}
    while work and max(e[0] for e in work)>=2:
        n=max(e[0] for e in work)
        part={(n-2,e[1],e[2],e[3]):v for e,v in work.items() if e[0]==n}
        out=A.add(out,part);work=A.add(work,A.scale(A.mul(part,A.power(eps,2)),-1))
    if work:raise ArithmeticError('Polar quotient has nonzero remainder')
    return out

def certify(A,B,require,digest,tensor_hash):
    I=integral(A);require(I==alternate_integral(A),'Complete polar integral constructions differ')
    eps=A.add(A.ONE,A.scale(A.variable(0),-1));defect=A.add(A.ONE,A.scale(I,-1))
    W=divide(A,defect)
    require(A.mul(A.power(eps,2),W)==defect,'Complete polar quotient multiplication fails')
    vals,den,deg=B.bernstein(W)
    require(deg==(14,8,4,0) and len(vals)==675,'Incomplete polar tensor')
    require(B.invert(vals,den,deg)==W,'Complete polar inverse fails')
    require(min(vals)>0 and F(min(vals),den)==F(8,9),'Wrong polar sign bound')
    require((len(I),len(W))==(287,237),'Wrong polar polynomial inventory')
    rows=[]
    for a in [F(0),F(1,2),F(1)]:
      for v in [F(0),F(1,3),F(1)]:
       for h in [F(0),F(2,5),F(1)]:
        raw=A.evaluate(I,[a,v,h,F(0)]);q=A.evaluate(W,[a,v,h,F(0)])
        require(1-raw==(1-a)**2*q and q>=F(8,9),'Polar rational defect control fails')
        rows.append(list(map(str,[a,v,h,raw,q])))
    Q=F(16,9);P=F(9);L=Q**2*P;gamma=F(2,9)/L
    require(L==F(256,9) and gamma==F(1,128),'Uniform polar mean-gap constants differ')
    return {'degrees':list(deg),'coefficients':len(vals),'minimum':'8/9',
      'integral_monomials':len(I),'quotient_monomials':len(W),
      'sha256':tensor_hash(vals,den),'power_sha256':digest(A.canonical(W)),
      'complete_integral_routes':2,'complete_quotient_and_inverse':True,
      'rational_controls':len(rows),'rational_controls_sha256':digest(rows),
      'uniform_L':str(L),'uniform_gamma':str(gamma)}
