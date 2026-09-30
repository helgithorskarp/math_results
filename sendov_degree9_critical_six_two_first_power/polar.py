"""Fresh exact even-multiplicity polar modulus over Q[a,v,theta,tau].

Author six-sendov-1, researcher. The fourth axis is integrated out.
The proof's radius/real-mean saturation and monotonicity are external
ordinary mathematical deductions, explicitly written in PROOF.md.
"""
from fractions import Fraction as F
from math import factorial

def quadratics(A):
    a,v,h,t=[A.variable(i) for i in range(4)]
    o=A.ONE;eps=A.add(o,A.scale(a,-1))
    R=A.add(o,A.scale(A.mul(a,v),F(4,3)))
    S=A.add(o,A.scale(A.mul(a,A.add(o,A.scale(v,-1))),4))
    heavy=[A.power(a,2),
      A.add(A.scale(A.mul(A.mul(a,eps),R),2),
        A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(o,a)),h),F(-8,3))),
      A.power(A.mul(eps,R),2)]
    light=[A.power(a,2),
      A.add(A.scale(A.mul(A.mul(a,eps),S),2),
        A.scale(A.mul(A.mul(A.mul(a,A.power(eps,2)),A.add(o,a)),A.add(o,A.scale(h,-1))),-8)),
      A.power(A.mul(eps,S),2)]
    return heavy,light

def integral(A):
    heavy,light=quadratics(A);tau=A.variable(3)
    X=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(heavy)))
    Y=A.add(*(A.mul(p,A.power(tau,j)) for j,p in enumerate(light)))
    raw=A.mul(A.power(X,3),Y)
    return A.add(*[{(e[0],e[1],e[2],0):f/F(e[3]+1)} for e,f in raw.items()])

def alternate_integral(A):
    """Direct multinomial heavy triple and a single light quadratic."""
    X,Y=quadratics(A);out={}
    for i in range(4):
      for j in range(4-i):
        k=3-i-j
        heavy=A.mul(A.power(X[0],i),A.mul(A.power(X[1],j),A.power(X[2],k)))
        for ell in range(3):
          weight=F(factorial(3),factorial(i)*factorial(j)*factorial(k)*(j+2*k+ell+1))
          out=A.add(out,A.scale(A.mul(heavy,Y[ell]),weight))
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
    require(H==alternate_integral(A),'Two polar integral constructions differ')
    W=divide_defect(A,A.add(A.ONE,A.scale(H,-1)))
    vals,den,degrees=B.bernstein(W)
    require(len(H)==271 and len(W)==225,'Wrong exact polar inventory')
    require(degrees==(14,8,4,0) and len(vals)==675,'Wrong complete polar tensor')
    require(B.invert(vals,den,degrees)==W,'Complete polar tensor inversion fails')
    require(min(vals)>0 and F(min(vals),den)==F(8,9),'Polar positive bound differs')
    # The quotient polynomial is defined at a=1 without a division there.
    a,v,theta=[A.variable(i) for i in range(3)]
    at_one=A.add(*[{(0,e[1],e[2],0):f} for e,f in W.items()])
    radius=A.add({(0,0,0,0):F(1,2)},A.scale(v,F(2,3)))
    variance=A.scale(A.power(A.add(radius,A.scale(A.ONE,-1)),2),3)
    expected=A.add(A.scale(A.ONE,F(8,3)),A.scale(variance,F(16,3)))
    require(at_one==expected,'Retained polar variance boundary identity fails')
    controls=[]
    for av in [F(0),F(1,2),F(1)]:
      for vv in [F(0),F(1,3),F(1)]:
        for hv in [F(0),F(2,5),F(1)]:
          value=A.evaluate(W,[av,vv,hv,F(0)])
          raw=A.evaluate(H,[av,vv,hv,F(0)])
          require(1-raw==(1-av)**2*value and value>=F(8,9),'Polar rational control fails')
          controls.append([str(z) for z in [av,vv,hv,raw,value]])
    return {'degrees':list(degrees),'coefficients':len(vals),'minimum':'8/9',
      'integral_monomials':len(H),'defect_monomials':len(W),
      'sha256':tensor_hash(vals,den),'power_sha256':digest(A.canonical(W)),
      'boundary_variance_identity_checked':True,'rational_controls':len(controls),
      'controls_sha256':digest(controls),'mean_gap_constant':'1/288'}
