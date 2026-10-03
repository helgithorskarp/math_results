"""Independent determinant expansion and exact five-direction dual identities."""
from itertools import permutations
from exact import P,R,F,need

def determinant(A):
 n=len(A);out=P(0)
 for perm in permutations(range(n)):
  s=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=P(s)
  for i,j in enumerate(perm):term*=A[i][j]
  out+=term
 return out

def derive():
 q=P([0,1]);s=3*q+4;S=s-2
 M=[[6*q+1,-P(1),-P(3),-3*q],[-P(1),3*q+3,-P(1),2*q+2],[-P(3),-P(1),3*q+3,-q],[-3*q,2*q+2,-q,2*q*q+4*q]]
 Ds=[determinant([r[:k] for r in M[:k]]) for k in range(1,5)]
 stated=[6*q+1,18*q*q+21*q+2,54*q**3+117*q*q+36*q-28,3*(3*q*q+3*q-2)*(12*q**3+19*q*q+4*q-4)]
 need(Ds==stated,'entire four independently expanded determinant polynomials')
 shifts=[d.shifted(4) for d in Ds];need(all(all(x>0 for x in d.c) for d in shifts),'all coefficients positive on real q>=4')
 den=3*(12*q**3+19*q*q+4*q-4)
 theta=[R(27*q**3+39*q*q+4*q-12,den),R(-(3*q-2)*(6*q*q+11*q+6),den),R(4*q*(3*q+4),den),R((3*q+2)**2,den),R((3*q-2)*(3*q+2),den)]
 b=[3*q,-P(2),-P(2),-2*q]
 for i,row in enumerate(M):need(sum((R(a)*t for a,t in zip(row,theta[1:])),R(0))==-R(b[i]),'whole four-direction stationary equation')
 need(theta[0]==(1-theta[1])/2,'eliminated first variable')
 G=[[4*S,2*S,P(0),P(0),P(0)],[2*S,3*(s-3),-P(1),-P(3),-3*q],[P(0),-P(1),s-1,-P(1),2*q+2],[P(0),-P(3),-P(1),s-1,-q],[P(0),-3*q,2*q+2,-q,q*(s-q)]]
 linear=[-2*S,-P(2),-P(2),-P(2),-2*q]
 energy=R(2*S)+2*sum((R(a)*t for a,t in zip(linear,theta)),R(0))+sum((theta[i]*R(G[i][j])*theta[j] for i in range(5) for j in range(5)),R(0))
 c=R((3*q+2)*(3*q+4)*(3*q*q+3*q-2),den)
 need(energy==2*c,'complete five-dimensional minimized lower energy')
 # Balanced-face monotonicity and all-count denominator/sign proof.
 A=q*q+6;need((F(1,2)*q*(q+1)*A*A-4*q).shifted(4).c[0]>0,'balanced monotonicity base')
 need(all(x>0 for x in (F(1,2)*q*(q+1)*A*A-4*q).shifted(4).c),'entire balanced monotonicity polynomial')
 return {'leading_determinants':[x.record() for x in Ds],'positive_q4_shifts':[x.record() for x in shifts],'theta':[x.record() for x in theta],'lower_c':c.record(),'five_direction_energy':energy.record(),'balanced_monotonicity_shift':(F(1,2)*q*(q+1)*A*A-4*q).shifted(4).record()}
