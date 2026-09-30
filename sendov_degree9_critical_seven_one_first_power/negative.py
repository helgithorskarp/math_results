"""Fresh opposite-order sign reduction over Q[b,r,chi,unused].

Generic polynomial and arc primitives are credited to author source
2831f4c23f848429d95b23310e57fb109705409d. New substitutions, independent
Horner identities and sign targets are generated here, with exact domains.
"""
from fractions import Fraction as F

def shift(p,e,weight=F(1)):
 return {tuple(a+b for a,b in zip(e,f)):v*weight for f,v in p.items() if v*weight}

def endpoint_factors(A):
 """Independent endpoint geometric sums in T=1-br*u."""
 b,r,chi=[A.variable(i) for i in range(3)]
 Y=A.add(A.ONE,A.scale(A.power(chi,2),-1))
 T=(A.add(A.ONE,A.scale(A.mul(b,A.mul(r,chi)),-1)),A.scale(A.mul(b,r),-1))
 powers=[A.pairpower(T,j,Y) for j in range(8)]
 Ar=A.scale(A.add(*(p[0] for p in powers)),F(9,8))
 Ai=A.scale(A.add(*(p[1] for p in powers)),F(9,8))
 Br=A.mul(b,A.add(*(A.scale(p[0],F(j+1,8)) for j,p in enumerate(powers))))
 Bi=A.mul(b,A.add(*(A.scale(p[1],F(j+1,8)) for j,p in enumerate(powers))))
 return [Ar,Ai,Br,Bi]

def data(A,ARC):
 factors=ARC.data(A)
 b,r,z=[A.variable(i) for i in range(3)]
 s=A.add(A.scale(A.ONE,8),A.scale(r,-7))
 R=A.mul(A.power(r,14),A.power(s,2))
 PA,PB,P,Q=factors['gram']
 L=A.add(PA,A.mul(A.power(s,2),PB),A.scale(R,-1))
 H=A.add(L,A.scale(R,F(-9,32)))
 F0=A.add(A.power(L,2),A.scale(A.mul(A.power(s,2),A.mul(PA,PB)),-4))
 Tmean=A.add(r,A.scale(z,F(-8,7)),A.scale(A.mul(b,z),F(8,7)))
 Tdisk=A.add(A.ONE,A.scale(A.power(r,2),-1),A.mul(A.power(b,2),A.power(r,2)))
 G=A.add(A.scale(A.ONE,-1),A.power(r,2),A.scale(A.mul(A.power(b,2),A.power(r,2)),-1),
  A.scale(A.mul(b,r),2))
 Tdisk=A.add(Tdisk,A.mul(G,z))
 return {'factors':factors['factors'],'gram':factors['gram'],'R':R,'L':L,
  'targets':{'H':H,'mean':F0,'disk':F0},
  'numerators':{'H':Tmean,'mean':Tmean,'disk':Tdisk}}

def phase_substitution(A,p,T,disk):
 """Expand chi=T/r (mean) or chi=T/(2br) (disk) exactly."""
 powers=[A.power(T,i) for i in range(max(e[2] for e in p)+1)]
 out=[]
 for (i,j,k,l),v in p.items():
  if l or min(i-int(disk)*k,j-k)<0:
   raise ArithmeticError('Unexpected negative power in phase substitution')
  out.append(shift(powers[k],(i-int(disk)*k,j-k,0,0),v/(2**k if disk else 1)))
 return A.add(*out)

def physical_substitution(A,p):
 """b=(1-r+(2r-1)y)/r; return polynomial and exact clearing power."""
 r=A.variable(1);y=A.variable(0)
 h=A.add(A.ONE,A.scale(r,-1),A.scale(y,-1),A.scale(A.mul(r,y),2))
 degree=max(e[0] for e in p);powers=[A.power(h,j) for j in range(degree+1)]
 clear=max(0,max(e[0]-e[1] for e in p))
 out=[]
 for (i,j,k,l),v in p.items():
  out.append(shift(powers[i],(0,j-i+clear,k,l),v))
 return A.add(*out),clear

def homogenized_horner(A,p,axis,numerator,denominator):
 """Independent coefficient-group Horner, avoiding monomial cancellation."""
 degree=max(e[axis] for e in p);groups=[{} for _ in range(degree+1)]
 for e,v in p.items():
  f=list(e);f[axis]=0
  groups[e[axis]][tuple(f)]=v
 out=groups[degree];denpowers=[A.power(denominator,j) for j in range(degree+1)]
 for k in range(degree-1,-1,-1):
  out=A.add(A.mul(out,numerator),A.mul(groups[k],denpowers[degree-k]))
 return out,degree

def mapped(A,p,T,disk,require):
 b,r,y=[A.variable(i) for i in range(3)]
 phase=phase_substitution(A,p,T,disk)
 denominator=A.scale(A.mul(b,r),2) if disk else r
 reference,degree=homogenized_horner(A,p,2,T,denominator)
 require(reference==A.mul(A.power(denominator,degree),phase),
  'Complete phase-substitution/Horner coefficient identity fails')
 physical,clear=physical_substitution(A,phase)
 # Variable0 becomes y; its numerator contains the same variable0 by design.
 yy=A.variable(0)
 numerator=A.add(A.ONE,A.scale(r,-1),A.scale(yy,-1),A.scale(A.mul(r,yy),2))
 reference,degree=homogenized_horner(A,phase,0,numerator,r)
 require(shift(physical,(0,degree,0,0))==shift(reference,(0,clear,0,0)),
  'Complete radial-substitution/Horner coefficient identity fails')
 return physical,clear
