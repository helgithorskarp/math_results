"""Exact original-variable identities in the reviewer's Fraction polynomial ring.
No CAS/author imports. Ordinary domain and representation bridges remain in proof.
"""
from fractions import Fraction as F
from ring import R
from forms import arrow
from linear import need,digest,canonical
import json,signal

def bilinear(A,a,b):
 return sum(a[i]*A[i][j]*b[j] for i in range(len(a)) for j in range(len(b)))
def mm(A,B):
 return [[sum(a*B[k][j] for k,a in enumerate(row)) for j in range(len(B[0]))] for row in A]
def run():
 r=R({(1,0,0):1});l=R(1);q=R({(0,0,1):1});s=q+3;m=3*r+l;ell=m+1;N=2*q+2*m;H=N-1;rho=(q-1)/(q+1)
 G=[[R(0) for _ in range(5)] for _ in range(5)];dg=[q-1,3,3*r*(q-r),3*l*(q-l),2*l*s/3]
 for i in range(5):G[i][i]=R(dg[i])
 G[2][3]=G[3][2]=-3*r*l;old=[[R(0) for _ in range(5)] for _ in range(5)];old[0][0]=q*q-1;old[0][1]=old[1][0]=3*(q-1);old[1][1]=R(9)
 for i in [2,3]:
  for j in [2,3]:old[i][j]=6*G[i][j]
 B=[[H*G[i][j]-old[i][j] for j in range(5)] for i in range(5)];D=N-7;A0=N-q-2;J=A0*(N-4)-3*(q-1)
 def I0(a,b):return ((q-1)*(N-4)*a[0]*b[0]+3*(q-1)*(a[0]*b[1]+a[1]*b[0])+3*A0*a[1]*b[1])/J+3*(r*(q-r)*a[2]*b[2]-r*l*(a[2]*b[3]+a[3]*b[2])+l*(q-l)*a[3]*b[3])/D+2*l*s*a[4]*b[4]/(3*H)
 units=[[R(i==j) for j in range(5)] for i in range(5)];J0=[[I0(a,b) for b in units] for a in units]
 Gi=[[R(0) for _ in range(5)] for _ in range(5)]
 for i in [0,1,4]:Gi[i][i]=1/G[i][i]
 determinant=G[2][2]*G[3][3]-G[2][3]*G[3][2];Gi[2][2]=G[3][3]/determinant;Gi[3][3]=G[2][2]/determinant;Gi[2][3]=Gi[3][2]=-G[2][3]/determinant
 need(mm(mm(B,Gi),J0)==G,'ENTIRE25 rational inverse witness positions B G^-1 I0=G')
 hb=[R(0),R(F(1,3)),1/(3*r),R(0),R(0)];vb=[R(0),R(F(1,3)),R(0),1/(3*l),1/l];K=[R(1),(m-3)/3,R(1),R(F(1,3)),R(1)];E=[a-rho*b for a,b in zip(hb,vb)];cols=[hb,vb,K];dg=[1/(3*r),1/l,ell];S=[[(dg[i] if i==j else 0)-I0(cols[i],cols[j]) for j in range(3)] for i in range(3)];b=[I0(x,E) for x in cols];Tb=m/(3*r*l);aug=[S[i]+[b[i]] for i in range(3)]+[b+[Tb-I0(E,E)]]
 # Columns, not rows: first shear, then the full invertible class change.
 shear=[[R(1),R(0),R(0),R(0)],[R(0),R(1),R(0),R(0)],[R(0),R(0),R(1),R(0)],[R(1),-rho,R(0),R(1)]]
 shifted=[[bilinear(aug,a,b) for b in shear] for a in shear];change=[[R(1),R(-1),R(0),R(0)],[3*r,l,R(0),R(0)],[-3*r,-l,R(1),R(0)],[R(0),R(0),R(0),R(1)]];observed=[[bilinear(shifted,a,b) for b in change] for a in change]
 need(observed==arrow(r,l,q),'ENTIRE16 original-variable augmented congruence identities')
 return {'inverse_witness_positions':25,'augmented_congruence_positions':16,'coefficient_domain':'QQ(r,q), characteristic0, own Fraction sparse arithmetic','no_CAS_imports':True}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s bridge phase')));signal.alarm(60);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
