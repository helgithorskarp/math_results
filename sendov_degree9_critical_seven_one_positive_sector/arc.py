"""Light-phase elimination, with exact identities over Q[b,r,chi,unused].

This module does not assert the unresolved scalar origin lower bound.
The elementary circle-arc optimization is proved in PROOF.md section 5.
"""
from fractions import Fraction as F
from math import comb

def data(A):
 b=A.variable(0);r=A.variable(1);chi=A.variable(2)
 T,U=A.chebyshev()
 weights=[A.scale(A.power(A.mul(b,r),j),9*(-1)**j*comb(7,j))
   for j in range(8)]
 Ar=A.add(*(A.scale(A.mul(weights[j],T[j]),F(1,j+1)) for j in range(8)))
 Ai=A.add(*(A.scale(A.mul(weights[j],U[j-1]),F(1,j+1)) for j in range(1,8)))
 Br=A.mul(b,A.add(*(A.scale(A.mul(weights[j],T[j]),F(1,j+2)) for j in range(8))))
 Bi=A.mul(b,A.add(*(A.scale(A.mul(weights[j],U[j-1]),F(1,j+2)) for j in range(1,8))))
 Y=A.add(A.ONE,A.scale(A.power(chi,2),-1))
 PA=A.add(A.power(Ar,2),A.mul(Y,A.power(Ai,2)))
 PB=A.add(A.power(Br,2),A.mul(Y,A.power(Bi,2)))
 ZR=A.add(A.mul(Ar,Br),A.mul(Y,A.mul(Ai,Bi)))
 ZI=A.add(A.mul(Ar,Bi),A.scale(A.mul(Ai,Br),-1))
 return {'factors':[Ar,Ai,Br,Bi],'gram':[PA,PB,ZR,ZI]}

def alternate(A):
 """Multiply seven linear factors in tau, then integrate separately."""
 br=A.scale(A.mul(A.variable(0),A.variable(1)),-1)
 coefficients=[A.ONE]
 for _ in range(7):
  out=[{} for _ in range(len(coefficients)+1)]
  for j,p in enumerate(coefficients):
   out[j]=A.add(out[j],p)
   out[j+1]=A.add(out[j+1],A.mul(br,p))
  coefficients=out
 T,U=A.chebyshev();parts=[]
 for shift in [1,2]:
  real=A.add(*(A.scale(A.mul(p,T[j]),F(9,j+shift))
     for j,p in enumerate(coefficients)))
  imag=A.add(*(A.scale(A.mul(p,U[j-1]),F(9,j+shift))
     for j,p in enumerate(coefficients) if j))
  if shift==2:
   real=A.mul(A.variable(0),real);imag=A.mul(A.variable(0),imag)
  parts.extend([real,imag])
 return parts

def support_controls(require,gmul,gnorm):
 """Rational branch/endpoint controls, not a substitute for the arc proof."""
 cases=[
  ((F(3),F(4)),F(0),F(1),(F(3,5),F(-4,5)),F(5),'free'),
  ((F(3),F(4)),F(3,5),F(4,5),(F(3,5),F(-4,5)),F(5),'switch'),
  ((F(3),F(4)),F(4,5),F(3,5),(F(4,5),F(-3,5)),F(24,5),'boundary'),
  ((F(-3),F(4)),F(0),F(1),(F(0),F(-1)),F(4),'boundary'),
  ((F(3),F(-4)),F(4,5),F(3,5),(F(4,5),F(3,5)),F(24,5),'negative-imag'),
  ((F(3),F(4)),F(1),F(0),(F(1),F(0)),F(3),'ell-one'),
  ((F(-3),F(4)),F(-1),F(0),(F(-3,5),F(-4,5)),F(5),'ell-minus-one'),
  ((F(-3),F(0)),F(3,5),F(4,5),(F(3,5),F(4,5)),F(-9,5),'real-negative'),
  ((F(0),F(0)),F(3,5),F(4,5),(F(1),F(0)),F(0),'zero')]
 for z,ell,edge,optimum,maximum,label in cases:
  require(ell*ell+edge*edge==1 and edge>=0,'Bad rational arc endpoint')
  require(gnorm(optimum)==1 and optimum[0]>=ell,'Bad rational arc optimizer')
  require(gmul(z,optimum)[0]==maximum,'Rational arc support objective mismatch')
  if gnorm(z)==0:
   require(maximum==0,'Zero arc support mismatch')
  else:
   norm=F(5) if gnorm(z)==25 else F(3)
   require(norm*norm==gnorm(z),'Bad rational support norm')
   if z[0]/norm>=ell:
    require(maximum==norm,'Free arc support formula fails')
   else:
    require(maximum==z[0]*ell+abs(z[1])*edge,'Boundary arc support formula fails')
  for v in [(F(1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),
    (F(0),F(1)),(F(0),F(-1)),(F(-3,5),F(4,5)),(F(-1),F(0))]:
   if v[0]>=ell:require(gmul(z,v)[0]<=maximum,'Arc support finite comparison fails')
 return {'count':len(cases),'branches':[row[-1] for row in cases]}
