"""Fresh exact full original-set Gram, basis, principal and two repairs."""
from fractions import Fraction as F
import hashlib,json,sys,resource
from sectors import params,matrices

def require(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def scale(c,v):return [c*x for x in v]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def transpose(A):return list(map(list,zip(*A)))
def multiply(A,B):
 cols=transpose(B);return [[dot(row,col)for col in cols]for row in A]
def matrixadd(A,B):return [add(a,b)for a,b in zip(A,B)]
def digest(v):
 raw=json.dumps(v,default=str,separators=(',',':'),sort_keys=True).encode()
 return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def inertia(A):
 W=[r[:]for r in A];rank=0
 for k in range(len(W)):
  require(W[k][k]>=0,'negative PSD pivot')
  if not W[k][k]:require(all(W[k][j]==0 for j in range(k,len(W))),'zero PSD pivot with nonzero row');continue
  z=W[k][k];rank+=1
  for i in range(k+1,len(W)):
   for j in range(i,len(W)):
    W[i][j]-=W[i][k]*W[k][j]/z;W[j][i]=W[i][j]
 return rank

def solve(A,b):
 W=[row[:]+[v]for row,v in zip(A,b)];n=len(A)
 for k in range(n):
  require(W[k][k]>0,'principal non-SPD');z=W[k][k]
  for i in range(k+1,n):
   t=W[i][k]/z
   for j in range(k+1,n+1):W[i][j]-=t*W[k][j]
 y=[F(0)]*n
 for k in range(n-1,-1,-1):y[k]=(W[k][-1]-sum(W[k][j]*y[j]for j in range(k+1,n)))/W[k][k]
 require([dot(r,y)for r in A]==b,'principal solution binding');return y

def audit(n,h):
 require(type(n)is int and type(h)is int and 3<=n<=5 and 2<=h<=3,'literal fixture guard')
 q=2**(n-1);p=params(F(h),F(q));N=int(p['N']);require(N<=56,'literal N guard')
 D,s,w,ell,alpha,beta,mu,nu,a,b,c=[p[k]for k in('D','s','w','ell','alpha','beta','mu','nu','a','b','c')]
 old=2*q-1;facets=2*h;dim=old+14*h
 def v():return [F(0)]*dim
 def e(k):r=v();r[k]=F(1);return r
 def index(group,i,j=0):
  start={'B':old,'T':old+2*h,'M':old+8*h,'WA':old+10*h,'WF':old+12*h}[group]
  return start+(3*i+j if group=='T'else i)
 H=[[F(0)]*dim for _ in range(dim)]
 for A in range(1,2*q):
  for B in range(1,2*q):H[A-1][B-1]=s*(A==B)+(q-D)*(A+B==2*q-1)-1
 for i in range(facets):
  for j in range(facets):
   H[index('B',i)][index('B',j)]=(s/3)*(F(i==j)-F(1,h))if i//h==j//h else F(0)
   H[index('M',i)][index('M',j)]=mu if i==j else -mu/(2*h-1)
  for x in range(3):
   for y in range(3):H[index('T',i,x)][index('T',i,y)]=s*(F(x==y)-F(1,3))
  H[index('WA',i)][index('WA',i)]=alpha;H[index('WF',i)][index('WF',i)]=beta
 g={A:e(A-1)for A in range(1,2*q)};G=v()
 for row in g.values():G=add(G,row)
 HX=[]
 for bit in[1,2]:
  r=v()
  for A,row in g.items():
   if A&bit:r=sub(r,row)
  HX.append(r)
 K=add(G,add(*HX));z=scale(-1/ell,K)
 basis_old=[sub(G,g[2*q-1]),add(G,g[2*q-1]),add(add(*HX),add(G,g[2*q-1])),sub(*HX)]
 transforms=lambda x:multiply([x],H)[0]
 phys=lambda x,y:dot(transforms(x),y)
 require([phys(x,x)for x in basis_old]==[4*(q-1),4*D,2*D*(q-2),2*q*D],'old metric')
 sets=[0]+list(range(1,2*q));rows=[z]+[g[A]for A in range(1,2*q)];marked={};private={}
 for i in range(facets):
  mark=1 if i<h else 2;pairbits=[1<<(n+2*i),1<<(n+2*i+1)]
  for j in range(3):
   mask=pairbits[0]if j==0 else pairbits[1]if j==1 else pairbits[0]|pairbits[1]
   tt=e(index('T',i,j));mr=add(scale(1/D,HX[i//h]),add(e(index('B',i)),tt));marked[i,j]=mr
   sets.append(mask|mark);rows.append(mr)
  for j in range(3):
   if j<2:pr=add(z,add(scale(a,e(index('B',i))),scale(c,e(index('T',i,1-j)))))
   else:
    ts=v()
    for k in range((i//h)*h,(i//h+1)*h):
     if k!=i:ts=add(ts,e(index('T',k,2)))
    pr=add(z,add(scale(b,e(index('B',i))),scale(c/(h-1),ts)))
   wr=e(index('M',i))
   if j<2:wr=add(wr,add(scale(F(1 if j==0 else -1,2),e(index('WA',i))),scale(F(-1,2),e(index('WF',i)))))
   else:wr=add(wr,e(index('WF',i)))
   private[i,j]=add(pr,wr);mask=pairbits[0]if j==0 else pairbits[1]if j==1 else pairbits[0]|pairbits[1]
   sets.append(mask);rows.append(private[i,j])
 require(len(rows)==N and len(set(sets))==N,'literal family census')
 total=v()
 for row in rows:total=add(total,row)
 require(transforms(total)==v(),'actual empty and total row sum in physical metric')
 transformed=multiply(rows,H);Q=multiply(transformed,transpose(rows));C=[r[1:]for r in Q[1:]]
 for i in range(N):
  require(sum(Q[i])==0,'whole seed row sum')
  if i:require(Q[i][i]==w,'nonempty diagonal')
  for j in range(N):
   if sets[i]&sets[j] and i!=j:require(Q[i][j]==-1,'every literal intersection')
 require(Q[0][0]==p['c0'],'actual loop norm')
 require(inertia(Q)==N-4,'seed Gram rank');J=[[F(1)]*N for _ in range(N)];P=[[F(i==j)-F(1,N)for j in range(N)]for i in range(N)]
 require(inertia(matrixadd(Q,J))==N-3,'seed lower rank')
 require(inertia([[ (N-1)*P[i][j]-Q[i][j]for j in range(N)]for i in range(N)])==N-1,'seed cap floor')
 # Entire orthogonal physical basis and all Gram/frame positions.
 Bs=[];spec=[];forms=matrices(p)
 def group(vectors,metric,S,label):
  start=len(Bs);Bs.extend(vectors);spec.append((start,len(Bs),metric,S,label))
 for i in range(facets):group([sub(e(index('T',i,0)),e(index('T',i,1))),e(index('WA',i))],*forms['leaf'],'leaf'+str(i))
 def TS(i):return sub(add(e(index('T',i,0)),e(index('T',i,1))),scale(2,e(index('T',i,2))))
 for mark in range(2):
  for k in range(1,h):
   t=[1]*k+[-k]+[0]*(h-k-1);coords=[]
   for kind in['B','TS','WF','M']:
    r=v()
    for i,u in enumerate(t):r=add(r,scale(u,TS(mark*h+i)if kind=='TS'else e(index(kind,mark*h+i))))
    coords.append(r)
   fac=F(k*(k+1),2);gm,S=forms['standard'];group(coords,[fac*x for x in gm],[[fac*x for x in row]for row in S],'standard'+str(mark)+'-'+str(k))
 trace=[v(),v()];oddtrace=[v(),v(),v()]
 for i in range(facets):
  trace[0]=add(trace[0],TS(i));trace[1]=add(trace[1],e(index('WF',i)))
  sg=1 if i<h else -1
  for j,r in enumerate([TS(i),e(index('WF',i)),e(index('M',i))]):oddtrace[j]=add(oddtrace[j],scale(sg,r))
 group(basis_old[:3]+trace,*forms['even'],'even');group([basis_old[3]]+oddtrace,*forms['odd'],'odd')
 pairs=[(A,2*q-1-A)for A in range(1,q)];pv=[add(g[A],g[B])for A,B in pairs];dv=[sub(g[A],g[B])for A,B in pairs]
 for k in range(1,q-1):
  r=v()
  for i in range(k):r=add(r,pv[i])
  r=sub(r,scale(k,pv[k]));norm=4*q*k*(k+1);group([r],[F(norm)],[[F(2*q*norm)]],'oldplus'+str(k))
 rc=[F(1-bool(A&1)-bool(A&2))for A,B in pairs];ac=[F(bool(A&2)-bool(A&1))for A,B in pairs];rr=dot(rc,rc);aa=dot(ac,ac);ds=[]
 for j in range(q-1):
  t=[F(int(i==j))for i in range(q-1)];t=sub(t,add(scale(t[j]*rc[j]/rr,rc),scale(t[j]*ac[j]/aa,ac)))
  for prev in ds:t=sub(t,scale(dot(t,prev)/dot(prev,prev),prev))
  if any(t):ds.append(t)
 require(len(ds)==q-3,'entire old minus complement')
 for j,t in enumerate(ds):
  r=v()
  for coef,dvrow in zip(t,dv):r=add(r,scale(coef,dvrow))
  norm=4*D*dot(t,t);group([r],[norm],[[2*D*norm]],'oldminus'+str(j))
 require(len(Bs)==N-4,'whole physical dimension')
 BH=multiply(Bs,H);Gamma=multiply(BH,transpose(Bs));inner=multiply(transformed,transpose(Bs));S=multiply(transpose(inner),inner)
 gg=[[F(0)]*(N-4)for _ in Bs];ss=[[F(0)]*(N-4)for _ in Bs]
 for lo,hi,gm,frame,label in spec:
  for i in range(lo,hi):
   gg[i][i]=gm[i-lo]
   for j in range(lo,hi):ss[i][j]=frame[i-lo][j-lo]
 require(Gamma==gg and S==ss,'complete physical forms, including all cross entries')
 require(all(Gamma[i][i]>0 for i in range(N-4)),'physical independent basis')
 deleted=[sets.index(1),sets.index(2),sets.index((1<<(n+2*(facets-1)))|(1<<(n+2*(facets-1)+1)))];last=deleted[2];keep=[i for i in range(1,N)if i not in deleted]
 A=[[Q[i][j]for j in keep]for i in keep];r=[F(int(i in [sets.index(1<<n),sets.index(1<<(n+1)),sets.index((1<<n)|(1<<(n+1)))]))for i in keep]
 require(len(A)==N-4 and inertia(A)==N-4,'retained original principal')
 inverse=solve(A,r);kappa=dot(r,inverse);require(kappa==2/nu+4/beta,'full principal inverse energy')
 coeff=[-F(1)if i in [sets.index(mask)for f in range(facets)for mask in[1<<(n+2*f),1<<(n+2*f+1),(1<<(n+2*f))|(1<<(n+2*f+1))]]else -6*h/ell*(1-int(bool(sets[i]&1))-int(bool(sets[i]&2)))if sets[i]<(1<<n)else F(0)for i in keep]
 require([dot(row,coeff)for row in A]==[Q[i][last]for i in keep]and dot(r,coeff)==-3 and dot(coeff,[Q[i][last]for i in keep])==w,'deleted complete coefficient and Schur')
 repairs=[]
 for name,delta,bound in [('original',1/(4*(8+kappa)),F(8)),('credited_larger',1/(4*(F(79,10)+kappa/6)),F(79,10))]:
  Core=[row[:]for row in C]
  for i in [sets.index(1<<n),sets.index(1<<(n+1)),sets.index((1<<n)|(1<<(n+1)))]:Core[i-1][last-1]+=delta;Core[last-1][i-1]+=delta
  Qr=[[F(0)]*N for _ in range(N)]
  for i in range(1,N):
   for j in range(1,N):Qr[i][j]=Core[i-1][j-1]
   Qr[i][0]=Qr[0][i]=-sum(Core[i-1])
  Qr[0][0]=sum(sum(row)for row in Core)
  u=[F(0)]*N;vlast=[F(0)]*N;u[0]=-3;vlast[0]=-1;vlast[last]=1
  for i in [sets.index(1<<n),sets.index(1<<(n+1)),sets.index((1<<n)|(1<<(n+1)))]:u[i]=1
  require(all(Qr[i][j]-Q[i][j]==delta*(u[i]*vlast[j]+vlast[i]*u[j])for i in range(N)for j in range(N)),'whole empty lift perturbation')
  L=matrixadd(Qr,J);M=[[(L[i][j]-s*(i==j))/(N-s)for j in range(N)]for i in range(N)]
  for i in range(N):
   require(sum(M[i])==1,'whole M row sum')
   for j in range(N):
    if sets[i]&sets[j]:require(M[i][j]==0,'all M support including diagonals')
  for bit in [1,2]:
   star=[F(bool(mask&bit))-s/N for mask in sets];require(all(dot(row,star)==0 for row in L),'both centered star kernels')
  floor=1-bound*delta;schur=6*delta-kappa*delta*delta;require(floor>F(3,4)and schur>0,'strict cap/Schur bounds')
  lr=inertia(L);cr=inertia([[N*P[i][j]-Qr[i][j]for j in range(N)]for i in range(N)]);fr=inertia([[(N-floor)*P[i][j]-Qr[i][j]for j in range(N)]for i in range(N)])
  require((lr,cr,fr)==(N-2,N-1,N-1),'both repair ranks and uniform floor')
  repairs.append(dict(name=name,delta=str(delta),floor=str(floor),schur=str(schur),lower_rank=lr,cap_rank=cr,whole_M=digest(M),whole_Q=digest(Qr)))
 return dict(n=n,h=h,q=q,N=N,s=str(s),span=N-4,physical_coordinate_dimension=dim,original_positions=N*N,metric_positions=(N-4)**2,frame_positions=(N-4)**2,principal_size=len(A),kappa=str(kappa),seed_Gram=digest(Q),whole_Gram_metric=digest(Gamma),whole_frame=digest(S),whole_basis=digest(Bs),repairs=repairs,all_original_support_rows_empty_stars=True,all_physical_internal_cross_entries=True)
if __name__=='__main__':print(json.dumps(audit(int(sys.argv[1]),int(sys.argv[2])),sort_keys=True,separators=(',',':')))
