"""Complete original finite controls; ordinary uniform bridge in PROOF.md."""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from fractions import Fraction as F
from pathlib import Path
import sys,json,signal,time,resource
from model import construct
from exact import require,psd_rank,dot,matvec,unit,scale,vecadd,zero,lift,fingerprint,check
from linear import solve

def whole_lift(C):
 sums=[sum(row) for row in C];return [[sum(sums)]+[-z for z in sums]]+ [[-sums[i]]+row for i,row in enumerate(C)]

def build(n):
 require(3<=n<=6,'literal n6 guard');q=1<<(n-1);N=2*q+18;require(N<=80,'literal N80 guard')
 p,G,S,cap,vec=construct(q,'mean',F(0),F(-2,5));size=N-1;old=list(range(1,2*q));marked=[];priv=[]
 for i in range(3):
  mask=[1<<(n+2*i),1<<(n+2*i+1),3<<(n+2*i)];priv+=mask;mark=1<<(0 if i<2 else 1);marked +=[mark|T for T in mask]
 family=[0]+old+marked+priv;require(len(set(family))==N,'distinct actual sets')
 C=zero(size,size);full=2*q-1
 for i,A in enumerate(old):
  for j,B in enumerate(old):C[i][j]=p['s']*(A==B)+(q-6)*(A^B==full)-1
 newvec=vec['V']+vec['U'];images=[matvec(G,z) for z in newvec]
 for i,A in enumerate(old):
  for j,z in enumerate(newvec):
   pairing=z[0]+6*z[2]*(1-2*bool(A&1))+6*z[3]*(1-2*bool(A&2)) if A!=full else -(q-1)*z[0]-6*z[1]
   C[i][len(old)+j]=C[len(old)+j][i]=pairing
 for i,z in enumerate(newvec):
  for j,x in enumerate(newvec):C[len(old)+i][len(old)+j]=dot(z,images[j])
 Q=whole_lift(C);M=lift(C,p['s']);seed=check(family,M,p['s']);require(psd_rank(C)==N-3,'seed entire core rank')
 P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
 require(psd_rank([[(N-1)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE original seed cap floor1')
 require(Q[0][0]==p['common'],'actual seed empty energy and vector')
 # Reconstruct ALL20 physical basis vectors independently as actual core-row combinations.
 def ec(i):return unit(size,i)
 oldG=vecadd(*(ec(i) for i in range(len(old))));oldf=ec(len(old)-1)
 gp=scale(F(1,2),vecadd(oldG,scale(-1,oldf)));h0=scale(F(-1,2),vecadd(oldG,oldf))
 Hx=scale(-1,vecadd(*(ec(i) for i,A in enumerate(old) if A&1)));Hy=scale(-1,vecadd(*(ec(i) for i,A in enumerate(old) if A&2)))
 basis=[gp,h0,vecadd(Hx,scale(-1,h0)),vecadd(Hy,scale(-1,h0))]
 V=[ec(len(old)+i) for i in range(9)];U=[ec(len(old)+9+i) for i in range(9)]
 hx=scale(F(1,6),Hx);hy=scale(F(1,6),Hy)
 B1=vecadd(scale(F(1,3),vecadd(*V[:3])),scale(-1,hx));B2=scale(-1,B1)
 basis += [B1,vecadd(V[0],scale(-1,hx),scale(-1,B1)),vecadd(V[1],scale(-1,hx),scale(-1,B1)),
           vecadd(V[3],scale(-1,hx),scale(-1,B2)),vecadd(V[4],scale(-1,hx),scale(-1,B2))]
 Y=vecadd(scale(F(1,3),vecadd(*V[6:])),scale(-1,hy));basis +=[Y,vecadd(V[6],scale(-1,hy),scale(-1,Y)),vecadd(V[7],scale(-1,hy),scale(-1,Y))]
 for i in range(8):
  projection=vecadd(*(scale(a,b) for a,b in zip(vec['P'][i][:12],basis[:12])))
  basis.append(vecadd(U[i],scale(-1,projection)))
 images_basis=[matvec(C,z) for z in basis]
 actualG=[[dot(a,z) for z in images_basis] for a in basis];require(actualG==G,'EVERY400 reconstructed physical Gram position')
 pairings=[[-sum(z)]+z for z in images_basis]
 actualS=[[dot(a,b) for b in pairings] for a in pairings];require(actualS==S,'EVERY400 full actual frame position incl empty')
 # The complete complement directions on the actual matrix.
 pairs=[A for A in old if A<full^A];base=pairs[0];high=[]
 for A in pairs[1:]:
  v=[F(0)]*N;v[A]=v[full^A]=1;v[base]=v[full^base]=-1
  require(matvec(Q,v)==scale(2*q,v),'full untouched symmetric action');high.append(v)
 signs=[[F(1-2*bool(A&bit)) for A in pairs] for bit in [1,2]]
 a=[row[:] for row in signs];pivots=[];row=0
 for col in range(len(pairs)):
  pivot=next((i for i in range(row,2) if a[i][col]),None)
  if pivot is None:continue
  a[row],a[pivot]=a[pivot],a[row];d=a[row][col];a[row]=[z/d for z in a[row]]
  for i in range(2):
   if i!=row:
    t=a[i][col];a[i]=[x-t*y for x,y in zip(a[i],a[row])]
  pivots.append(col);row+=1
  if row==2:break
 require(len(pivots)==2,'both old mark sign constraints independent')
 low=[]
 for free in [j for j in range(len(pairs)) if j not in pivots]:
  coeff=[F(0)]*len(pairs);coeff[free]=1
  for i,col in enumerate(pivots):coeff[col]=-a[i][free]
  v=[F(0)]*N
  for A,t in zip(pairs,coeff):v[A]=t;v[full^A]=-t
  require(matvec(Q,v)==scale(12,v),'full untouched antisymmetric action');low.append(v)
 require(len(high)==q-2 and len(low)==q-3,'ENTIRE untouched dimension count')
 require(len(basis)+len(high)+len(low)==N-3,'complete seed nonzero space')
 # Exact deleted inverse and credited sharp whole repair.
 W8=[row[:8] for row in vec['W'][:8]];rhs=[F(i<3) for i in range(8)];kappa=dot(rhs,solve(W8,rhs))
 require(kappa==1/(2*p['nu'])+1/p['muL']+4/p['betaL'],'whole deleted inverse kappa formula')
 delta=1/(4*(8+kappa));require(6*delta-kappa*delta*delta>0,'repaired residual Schur')
 sharp=[row[:] for row in C];offset=len(old)+9;last=offset+8
 for i in range(offset,offset+3):sharp[i][last]+=delta;sharp[last][i]+=delta
 MS=lift(sharp,p['s']);QS=whole_lift(sharp);sharp_status=check(family,MS,p['s'])
 require(psd_rank(sharp)==N-2,'repaired greatest original core rank');require(sharp_status['lower_rank']==N-1,'greatest original lower rank')
 pu=[F(0)]*N;v=[F(0)]*N;pu[0]=-3;v[0]=-1;v[1+last]=1
 for i in range(offset,offset+3):pu[1+i]=1
 require(dot(pu,pu)==12 and dot(v,v)==2 and dot(pu,v)==3 and sum(pu)==sum(v)==0,'whole repair vector norms')
 require(all(QS[i][j]-Q[i][j]==delta*(pu[i]*v[j]+v[i]*pu[j]) for i in range(N) for j in range(N)),'EVERY whole rank-two repair position')
 floor=1-8*delta;require(floor>F(3,4),'whole repaired floor')
 require(psd_rank([[N*P[i][j]-QS[i][j]-floor*P[i][j] for j in range(N)] for i in range(N)])==N-1,'EVERY original sharp cap floor position')
 star=[F(bool(A&1))-F(p['s'],N) for A in family]
 L=[[(N-p['s'])*MS[i][j]+p['s']*(i==j) for j in range(N)] for i in range(N)]
 require(not any(matvec(L,star)),'unique heavy maximum-star kernel')
 return family,C,MS,{'n':n,'q':q,'N':N,'s':str(p['s']),'seed':seed,'sharp':sharp_status,'seed_core_sha256':fingerprint(C),'sharp_matrix_sha256':fingerprint(MS),'seed_rank':N-2,'sharp_rank':N-1,'cap_rank':N-1,'floor':str(floor),'kappa':str(kappa),'delta':str(delta),'original_positions':N*N,'physical_Gram_positions':400,'physical_frame_positions':400,'untouched_high':len(high),'untouched_low':len(low),'all_whole_repair_entries':N*N}
