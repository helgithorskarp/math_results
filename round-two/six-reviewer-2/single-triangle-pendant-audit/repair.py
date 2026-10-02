"""Fresh whole-original lift calculation; no target code or oracle."""
from fractions import Fraction as F
import json,signal
from linear import need,canonical,digest,psd

def lift_change(N,t):
 need(type(N)is int and 2<=N<=160,'fixed literal N2..160');need(type(t)is int and 1<=t<=N-2,'disjoint star endpoints')
 x=[F(-t)]+[F(i<t)for i in range(N-1)];y=[F(-1)]+[F(i==t)for i in range(N-1)];A=[[x[i]*y[j]+y[i]*x[j]for j in range(N)]for i in range(N)];return x,y,A

def run():
 cases=[]
 for N,t in[(5,3),(18,3),(26,3),(28,3),(46,3),(74,3),(80,3),(120,3),(160,3),(8,1),(8,2),(12,6)]:
  x,y,A=lift_change(N,t);xx=sum(a*a for a in x);yy=sum(b*b for b in y);xy=sum(a*b for a,b in zip(x,y));need((xx,yy,xy)==(t*(t+1),2,t),'ENTIRE lifted Gram identity');need(all(sum(row)==0 for row in A),'EVERY original perturbation row');need(all(A[i][j]==A[j][i]for i in range(N)for j in range(N)),'whole symmetry');need(sum(A[i][i]for i in range(N))==2*t,'trace');need(sum(v*v for row in A for v in row)==2*(3*t*t+2*t),'complete trace-square')
  # Matrix annihilates orthogonal complement of span{x,y}; its 2-action
  # has characteristic lambda^2-2t lambda-t(t+2).
  coeff=[[xy,yy],[xx,xy]];need(coeff[0][0]+coeff[1][1]==2*t and coeff[0][0]*coeff[1][1]-coeff[0][1]*coeff[1][0]==-t*(t+2),'both nonzero characteristic coefficients')
  if t==3:
   # Prove exact norm<8 without floating point or eigenvalue oracle.
   # sqrt24<5, giving 3+sqrt24<8; same entire whole bound.
   need(xx*yy==24 and 24<25,'exact norm upper8');gap=[[F(8*(i==j))-A[i][j]for j in range(N)]for i in range(N)];negative=[[F(8*(i==j))+A[i][j]for j in range(N)]for i in range(N)];need(psd(gap)['rank']==N and psd(negative)['rank']==N,'ENTIRE original two-sided strict norm8')
  cases.append({'N':N,'t':t,'entire_original_change_sha256':digest(A),'whole_positions':N*N,'gram':[xx,yy,xy],'nonzero_eigenvalue_polynomial':[1,-2*t,-t*(t+2)]})
 # Deleted-balanced residual uses a distinct exact Schur reconstruction.
 # All entries of A_res chosen explicitly, original W1=0; any t actual private rows.
 residual=[]
 for m,t in[(5,3),(6,3),(8,3),(9,6)]:
  a=[[F(i==j)*(i+2)+F(1)for j in range(m-1)]for i in range(m-1)];from linear import inverse,mv
  u=[F(i<t)for i in range(m-1)];kappa=sum(u[i]*v for i,v in enumerate(mv(inverse(a),u)));delta=1/(4*(8+kappa));col=[-sum(row)+delta*u[i]for i,row in enumerate(a)];bottom=sum(sum(row)for row in a);W=[a[i]+[col[i]]for i in range(m-1)]+[col+[bottom]];need(psd(W)['rank']==m,'whole repaired residual positive');schur=bottom-sum(col[i]*v for i,v in enumerate(mv(inverse(a),col)));need(schur==2*t*delta-kappa*delta**2>0,'EXACT full residual Schur and larger delta');need(8*delta<=F(1,4)and kappa*delta<F(1,4),'entire norm and Schur margins');residual.append({'m':m,'t':t,'kappa':kappa,'delta':delta,'whole_W_sha256':digest(W),'exact_schur':schur})
 damages=[]
 def reject(name,f):
  try:f()
  except(ValueError,TypeError):damages.append(name);return
  raise ValueError('damage accepted '+name)
 x,y,A=lift_change(18,3)
 reject('omit actual empty loop',lambda:need(A[0][0]==0,'actual loop is6, not0'))
 reject('retain balanced empty row after repair',lambda:need(all(v==0 for v in A[0]),'actual empty row changes'))
 reject('core norm sqrt3 treated as full lift norm',lambda:need(sum(v*v for row in A for v in row)==6,'actual whole norm not core norm'))
 reject('wrong lifted Gram cross0',lambda:need(sum(a*b for a,b in zip(x,y))==0,'cross is3'))
 reject('false universal norm bound7',lambda:psd([[F(7*(i==j))-A[i][j]for j in range(18)]for i in range(18)]))
 reject('unsafe star endpoint overlap',lambda:lift_change(5,4))
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','all_whole_lift_controls':cases,'all_deleted_residual_controls':residual,'damages':damages,'scope':'Independent complete original lift and residual Schur algebra. Conditional on a proved seed gap1 and balanced residual; NOT a full9641 seed/decomposition/uniform-sign verdict.'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s whole repair controls')));signal.alarm(45);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
