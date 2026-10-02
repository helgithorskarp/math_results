"""Independent literal adaptive certificate phases, q4/7/12 only.

Unchanged own affine/linear primitives; no new9195 author imports.
All whole records/ordinary universal proof must be sealed before oracle.
"""
from fractions import Fraction as F
from math import isqrt
from itertools import combinations
import json,signal,sys
from affine import matrices,table,repair,quad,pair,family
from linear import need,psd,mv,digest,canonical,inverse

def alarm(*unused):raise TimeoutError('fixed60s phase guard; incomplete is not exclusion')
signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
def scalars(q,k):
 need(type(q)is int and type(k)is int and q>=4 and 1<=k<=q,'exact all-order scalar domain')
 N=F(q*q+13*q+16,2)-k;s=3*q+4;g=N-2*s;h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h;B=N-s-k;B0=N-(k+1)*s+k*(k-1)
 D=2*k*g*(1-h)+(alpha-2*k+2)*B;E=k*g*(1-h)**2+(alpha-k+1)*B
 need(g>0 and B>0 and D>0 and E>0 and N*D>E,'universal positive scalar bounds')
 need(B0==F(q*q+(7-6*k)*q+2*k*k-12*k+8,2),'exact original sufficient polynomial')
 need(B0>0,'this construction requires positive B0')
 kap=min(F(1,8),N*B0/(2*D));chi=k*g*(N-kap+kap*h)**2-((k-1)*(N-kap)+kap*alpha)*(N-kap)*B
 need(chi==N*N*B0-kap*N*D+kap*kap*E and chi>=N*N*B0/2>0,'adaptive sufficient numerator exact and positive')
 gamma=g*chi/(N*(N-kap)**2*B);old=min(kap/24,gamma/4);new=min(k*kap/(8*(2*k+1)),2*gamma/7)
 need(new>=old and(k==1 or new>old),'guaranteed rational repair improvement')
 return locals()

def original(q,k,mode):
 need((q,k)in [(4,1),(7,2),(12,3)]and mode in ['old','new'],'fixed finite literal phases')
 P=scalars(q,k);kap=P['kap'];t=P[mode];gamma=P['gamma'];g=P['g'];h=P['h'];N=int(P['N']);s=P['s']
 S,Z,C,D,R,U=matrices(q,k);non=S[1:];n=N-1
 CC=[[C[i][j]+kap*D[i][j]+t*R[i][j]for j in range(n)]for i in range(n)]
 UU=[[F(N*(i==j)-1)-CC[i][j]-gamma*F(i==j)/2 for j in range(n)]for i in range(n)]
 lower=psd(CC);upper=psd(UU);need(lower['rank']==n-1 and upper['rank']==n,'whole nonempty lower and capped projected strict rank/floor')
 sa=[F(bool(A&1))for A in non];need(not any(mv(CC,sa)),'whole original greatest lower kernel')
 # Independently derive all empty entries through omitted deleted-column sums.
 Q=table(q,kap);rowR={1:F(2),3:F(-1),5:F(-1)};closedrows=[]
 for A in non:
  r=F(1)if A&7==0 else h if(A&7).bit_count()<3 else -3*(q+1)*h
  hits=k if A&6 else(A&Z).bit_count()
  if hits==k:deleted=-k
  else:
   key=tuple(sorted((((A&7).bit_count(),(A&~7).bit_count()),(2,1))))
   deleted=-hits+(k-hits)*(Q[key]-1)
  closedrows.append(kap*r-deleted+t*rowR.get(A,F(0)))
 rows=[sum(row)for row in CC];need(rows==closedrows,'every original row versus independent omitted-column formula')
 T=sum(rows);need(T==kap*P['alpha']-2*k*kap*h+k*(s-k),'full actual empty energy')
 L=[[F(1)+T]+[F(1)-v for v in rows]]+[[F(1)-rows[i]]+[F(1)+v for v in row]for i,row in enumerate(CC)]
 M=[[(L[i][j]-s*F(i==j))/(N-s)for j in range(N)]for i in range(N)]
 for i,A in enumerate(S):
  need(sum(M[i])==1,'whole empty-retaining row normalization')
  for j,Bb in enumerate(S):
   need(M[i][j]==M[j][i],'whole symmetry')
   if A&Bb:need(M[i][j]==0,'whole intersection support')
 centered=[F(0)]+sa;centered=[v-F(s,N)for v in centered];need(not any(mv(L,centered)),'actual whole centered star kernel')
 # Finite whole rank/floor bridges: E injective, 1 orthogonal; psd is literal n-space,
 # and NI-L=E(NI-J-CC)E'. E'E=I+J>=I => projected whole cap floor gamma/2.
 return {'q':q,'k':k,'mode':mode,'N':N,'kappa':kap,'repair':t,'tau_old':P['old'],'tau_new':P['new'],'gamma':gamma,'nonempty_lower_rank':lower['rank'],'nonempty_upper_shifted_rank':upper['rank'],'whole_lower_rank':1+lower['rank'],'whole_upper_rank':upper['rank'],'whole_projected_upper_gap':gamma/2,'full_ordered_entries_checked':N*N,'M_sha256':digest(M),'C_sha256':digest(CC),'empty_M':M[0][0],'whole_centered_kernel_sha256':digest(centered),'scope':'actual original finite certificate; real full interval by ordinary repaired-floor proof, not samples'}

def zero():
 S,Z,C,D,R,U=matrices(4,0);n=len(S)-1;s=16
 lower=psd(C);upper=psd([[2*s*F(i==j)-C[i][j]for j in range(n)]for i in range(n)])
 need(lower['rank']==36 and n==41,'literal zero nullity5')
 non=S[1:]
 ker=[[F(bool(A&(1<<j)))for A in non]for j in range(3)]+[[F((A&7).bit_count()>=2)for A in non],[F(1)]*n]
 need(all(not any(mv(C,v))for v in ker),'all five literal zero kernel columns')
 G=[[sum(x*y for x,y in zip(v,w))for w in ker]for v in ker];need(psd(G)['rank']==5,'literal kernel independence')
 return {'q':4,'N0':len(S),'nonempty':n,'lower_rank':lower['rank'],'nullity':n-lower['rank'],'upper_shifted_rank':upper['rank'],'whole_kernel_columns':5,'literal_matrix_sha256':digest(C)}

def repair_check():
 pts=[1,2,4,5,3];R=[[repair(a,b)for b in pts]for a in pts];R2=[[sum(R[i][m]*R[m][j]for m in range(5))for j in range(5)]for i in range(5)]
 r=psd([[3*F(i==j)-R2[i][j]for j in range(5)]for i in range(5)]);v=[F(0),F(1),F(1),F(0),F(0)]
 need(mv(R2,v)==[3*z for z in v]and r['rank']==3,'exact sqrt3 repair norm, not norm2 bound')
 samples=[]
 for k in [1,2,3,7,100000]:
  YY=[[F(3)+F(1,k),F(1)+F(1,k)],[F(1)+F(1,k),F(3)+F(1,k)]];c=F(4)+F(2,k)
  need(psd([[c*F(i==j)-YY[i][j]for j in range(2)]for i in range(2)])['rank']==1,'exact two-column repair energy bound')
  samples.append({'k':k,'Y_Gram':YY,'largest_eigenvalue':c,'lower_interval_denominator':16+F(8,k)})
 return {'R':R,'R_squared':R2,'sqrt3_norm_squared':3,'equality_vector':v,'rational_cap_norm_bound':'sqrt3<7/4','Y_calibrations':samples,'unbounded_bridge':'Y eigenvalues2 and4+2/k by explicit diagonalization, not these samples'}
if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='original':out=original(int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
 elif cmd=='zero':out=zero()
 elif cmd=='repair':out=repair_check()
 else:raise ValueError('fixed mathematical phase')
 print(json.dumps(canonical(out),sort_keys=True,separators=(',',':')))
