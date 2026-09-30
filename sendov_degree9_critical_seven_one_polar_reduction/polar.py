"""Exact paired polar upper bound for critical7+1 over Q[a,v,theta,tau].

Author six-sendov-1, researcher. The fourth axis is integrated out.
Adapted from author source d02716775d595df93bb338e533323db8717b3185.
All multiplicity-dependent constants and the new paired upper bound
are regenerated. The proof's radius/real-mean saturation and monotonicity are external
ordinary mathematical deductions, explicitly written in PROOF.md.
"""
from fractions import Fraction as F
from math import factorial

def quadratics(A):
    a,v,h,t=[A.variable(i) for i in range(4)]
    o=A.ONE;eps=A.add(o,A.scale(a,-1))
    R=A.add(o,A.scale(A.mul(a,v),F(8,7)))
    S=A.add(o,A.scale(A.mul(a,A.add(o,A.scale(v,-1))),8))
    heavy=[A.power(a,2),
      A.add(A.scale(A.mul(A.mul(a,eps),R),2),
        A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(o,a)),h),F(-16,7))),
      A.power(A.mul(eps,R),2)]
    light=[A.power(a,2),
      A.add(A.scale(A.mul(A.mul(a,eps),S),2),
        A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(o,a)),A.add(o,A.scale(h,-1))),-16)),
      A.power(A.mul(eps,S),2)]
    return heavy,light

def integral(A):
    heavy,light=quadratics(A);tau=A.variable(3)
    X=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(heavy)))
    Y=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(light)))
    raw=A.scale(A.add(A.power(X,4),A.mul(A.power(X,3),Y)),F(1,2))
    return A.add(*[{(e[0],e[1],e[2],0):f/F(e[3]+1)} for e,f in raw.items()])

def alternate_integral(A):
    """Independent direct multinomial expansion of both fourth-degree terms."""
    X,Y=quadratics(A);out={}
    for heavy_power,light_power in [(4,0),(3,1)]:
      for i in range(heavy_power+1):
        for j in range(heavy_power+1-i):
          k=heavy_power-i-j
          heavy=A.mul(A.power(X[0],i),A.mul(A.power(X[1],j),A.power(X[2],k)))
          for ell in (range(3) if light_power else [0]):
            light=Y[ell] if light_power else A.ONE
            weight=F(factorial(heavy_power),2*factorial(i)*factorial(j)*factorial(k)*(j+2*k+ell+1))
            out=A.add(out,A.scale(A.mul(heavy,light),weight))
    return out

def divide_defect(A,p):
    eps=A.add(A.ONE,A.scale(A.variable(0),-1))
    work=dict(p);out={}
    while work and max(e[0] for e in work)>=2:
      n=max(e[0] for e in work)
      part={(n-2,e[1],e[2],e[3]):v for e,v in work.items() if e[0]==n}
      out=A.add(out,part);work=A.add(work,A.scale(A.mul(part,A.power(eps,2)),-1))
    if work:raise ArithmeticError('Nonzero polar division remainder')
    return out

def certify(A,B,require,digest,tensor_hash):
    H=integral(A)
    require(H==alternate_integral(A),'Two paired polar expansions differ')
    W=divide_defect(A,A.add(A.ONE,A.scale(H,-1)))
    vals,den,degrees=B.bernstein(W)
    require((len(H),len(W))==(286,237),'Wrong paired polar inventory')
    require(degrees==(14,8,4,0) and len(vals)==675,'Incomplete polar tensor')
    require(B.invert(vals,den,degrees)==W,'Full polar inverse identity fails')
    require(min(vals)>0 and F(min(vals),den)==F(8,9),'Wrong positive polar bound')
    v=A.variable(1)
    at_one=A.add(*[{(0,e[1],e[2],0):f} for e,f in W.items()])
    expected=A.add(A.scale(A.ONE,F(8,3)),
      A.scale(A.power(A.add(A.scale(A.ONE,F(-1,2)),A.scale(v,F(4,7))),2),F(-16,3)))
    require(at_one==expected,'Paired boundary variance identity fails')
    controls=[]
    for av in [F(0),F(1,2),F(1)]:
      for vv in [F(0),F(1,3),F(1)]:
        for hv in [F(0),F(2,5),F(1)]:
          raw=A.evaluate(H,[av,vv,hv,F(0)])
          value=A.evaluate(W,[av,vv,hv,F(0)])
          require(1-raw==(1-av)**2*value and value>=F(8,9),'Polar rational control fails')
          controls.append([str(z) for z in [av,vv,hv,raw,value]])
    Q=F(81,49);P=F(9);L=Q**2*(4*Q+3*P)/7
    gamma=F(2,9)/L
    require(L==F(10805967,823543) and gamma==F(1647086,97253703),
      'Uniform derivative and mean-gap constants differ')
    return {'degrees':list(degrees),'coefficients':len(vals),'minimum':'8/9',
      'integral_monomials':len(H),'defect_monomials':len(W),
      'sha256':tensor_hash(vals,den),'power_sha256':digest(A.canonical(W)),
      'boundary_variance_identity_checked':True,'rational_controls':len(controls),
      'controls_sha256':digest(controls),'uniform_L':str(L),'uniform_gamma':str(gamma)}
