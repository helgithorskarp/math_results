#!/usr/bin/env python3
"""Independent original set indexing, physical Gram, principal inverse and lift."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from audit import scalar_data
from poly import require,tick

def plus(*vs):
 out={}
 for v in vs:
  for k,x in v.items():out[k]=out.get(k,F())+x
 return {k:x for k,x in out.items() if x}
def times(v,c):return {k:x*c for k,x in v.items() if x*c}
def atom(k):return {k:F(1)}

def build(h):
 d=scalar_data(F(h));s=d['s'];ell=d['ell'];w=s-1
 gp,h0,A,Y=[atom((k,)) for k in ('g','h0','A','Y')]
 k=plus(gp,times(h0,F(1,h)),times(A,F(h-1,h)),times(Y,3));z=times(k,-1/ell)
 e=plus(times(h0,(1-d['rho'])/(3*h)),times(A,(1+d['rho'])/(3*h)),times(Y,-d['rho']))
 B=lambda i:atom(('B',i));T=lambda i,a:atom(('T',i,a));Wf=lambda i:atom(('F',i));Wa=lambda i:atom(('D',i));Mean=lambda i:atom(('M',i))
 def wd(i,a):
  if a==0:return plus(Mean(i),times(Wa(i),F(1,2)),times(Wf(i),-F(1,2)))
  if a==1:return plus(Mean(i),times(Wa(i),-F(1,2)),times(Wf(i),-F(1,2)))
  return plus(Mean(i),Wf(i))
 def inner_atom(a,b):
  if a[0] in ('g','h0','A','Y'):
   return {'g':F(1),'h0':F(3*h),'A':F(3*h),'Y':d['b2']}[a[0]] if a==b else F()
  if a[0]!=b[0]:return F()
  typ=a[0]
  if typ=='B':return s/3*(int(a[1]==b[1])-F(1,h))
  if typ=='T':return s*(int(a[2]==b[2])-F(1,3)) if a[1]==b[1] else F()
  if typ in ('D','F'):
   return d[('ah' if a[1]<h else 'al') if typ=='D' else ('bh' if a[1]<h else 'bl')] if a[1]==b[1] else F()
  if typ=='M':
   i,j=a[1],b[1]
   if i==h and j==h:return d['ml']
   if i==h or j==h:return -d['ml']/h
   return d['mh'] if i==j else (d['ml']/h-d['mh'])/(h-1)
  raise ValueError('atom')
 def inner(v,u):return sum((x*y*inner_atom(a,b) for a,x in v.items() for b,y in u.items()),F())
 sets=[frozenset(),frozenset([0]),frozenset([1]),frozenset([0,1])];rows=[times(k,-1/ell),plus(gp,times(A,-1)),plus(gp,A),times(plus(gp,h0),-1)]
 ids={}
 for i in range(h+1):
  mark=0 if i<h else 1;aa=2+2*i;bb=aa+1
  base=times(plus(h0,times(A,1 if i<h else -1)),F(1,3*h))
  base=plus(base,B(i)) if i<h else plus(base,Y)
  for a,st in enumerate(([mark,aa],[mark,bb],[mark,aa,bb])):
   sets.append(frozenset(st));rows.append(plus(base,T(i,a)))
  if i<h:
   pl=plus(z,times(e,d['a0']),times(B(i),d['a']))
   pp=[plus(pl,times(T(i,1),d['ch'])),plus(pl,times(T(i,0),d['ch'])),plus(z,times(B(i),d['b']),times(plus(*(T(j,2) for j in range(h) if j!=i)),d['ch']/(h-1)),times(T(h,2),d['cl']/h))]
  else:pp=[plus(z,times(e,d['f']),times(T(i,1),d['cl'])),plus(z,times(e,d['f']),times(T(i,0),d['cl'])),plus(z,times(e,d['g']))]
  for a,st in enumerate(([aa],[bb],[aa,bb])):
   ids[i,a]=len(rows);sets.append(frozenset(st));rows.append(plus(pp[a],wd(i,a)))
 N=len(rows);require(N==6*h+10 and len(set(sets))==N,'original family/index')
 Q=[[inner(a,b) for b in rows] for a in rows]
 for i in range(N):
  require(not sum(Q[i]),'actual full empty lift')
  if i:require(Q[i][i]==s-1,'all original nonempty diagonal')
  for j in range(N):
   if sets[i]&sets[j] and i!=j:require(Q[i][j]==-1,'every original intersecting entry')
 require(Q[0][0]==d['c0'],'actual empty loop')
 stars={v:sum(v in st for st in sets) for v in range(2*h+4)}
 require(stars[0]==s and stars[1]==5 and all(stars[v]==4 for v in range(2,2*h+4)),'all physical point stars')
 return d,sets,Q,ids

def ldl(a,positive=False):
 a=[list(r) for r in a];n=len(a);rank=0;pivots=[]
 for k in range(n):
  p=a[k][k];require(p>=0,'negative LDL pivot')
  if positive:require(p>0,'not positive definite')
  if not p:require(all(not a[k][j] for j in range(k,n)),'nonzero null-pivot row');continue
  rank+=1;pivots.append(str(p))
  for i in range(k+1,n):
   for j in range(i,n):a[i][j]-=a[i][k]*a[k][j]/p;a[j][i]=a[i][j]
  tick()
 return rank,pivots

def solve(a,b):
 a=[list(r)+[v] for r,v in zip(a,b)];n=len(a)
 for k in range(n):
  p=a[k][k];require(p>0,'principal positive Gaussian pivot')
  for i in range(k+1,n):
   c=a[i][k]/p
   for j in range(k+1,n+1):a[i][j]-=c*a[k][j]
 out=[F()]*n
 for i in range(n-1,-1,-1):out[i]=(a[i][-1]-sum(a[i][j]*out[j] for j in range(i+1,n)))/a[i][i]
 return out

def run(h):
 d,sets,Q,ids=build(h);N=len(Q);s=d['s'];C=[r[1:] for r in Q[1:]]
 seed_core=ldl(C)[0];seed_L=ldl([[q+1 for q in r] for r in Q])[0]
 # Complete original cap restriction by differences e_i-e_empty.
 P=lambda i,j:F(int(i==j))-F(1,N)
 def caprank(q,c):
  a=[[c*P(i,j)-q[i][j] for j in range(N)] for i in range(N)]
  diff=[[a[i][j]-a[i][0]-a[0][j]+a[0][0] for j in range(1,N)] for i in range(1,N)]
  return ldl(diff,True)[0]
 require(seed_core==N-3 and seed_L==N-2 and caprank(Q,N-1)==N-1,'original seed PSD/rank/cap')
 deleted=ids[h,2];keep=[i for i in range(1,N) if i not in (1,deleted)];aa=[[Q[i][j] for j in keep] for i in keep];ldl(aa,True)
 zz=[F(-1) if i in ids.values() else -3*(h+1)/d['ell'] if 1 in sets[i] and 0 not in sets[i] else F() for i in keep]
 col=[Q[i][deleted] for i in keep]
 require(all(sum(aa[i][j]*zz[j] for j in range(len(keep)))==col[i] for i in range(len(keep))),'original deleted column')
 require(sum(zz[i]*col[i] for i in range(len(keep)))==Q[deleted][deleted],'zero seed Schur')
 rr=[F(int(i in [ids[0,a] for a in range(3)])) for i in keep];v=solve(aa,rr);kappa=sum(x*y for x,y in zip(rr,v));pred=F(h-1,h)/d['nu']+1/d['ml']+4/d['bl']
 require(kappa==pred and sum(x*y for x,y in zip(rr,zz))==-3,'original principal inverse energies')
 records=[]
 for delta,label in ((1/(4*(8+kappa)),'author delta'),(1/(8+kappa),'fourfold rational repair')):
  new=[list(r) for r in Q]
  for i in [ids[0,a] for a in range(3)]:
   new[i][deleted]+=delta;new[deleted][i]+=delta;new[0][i]-=delta;new[i][0]-=delta;new[0][deleted]-=delta;new[deleted][0]-=delta;new[0][0]+=2*delta
  require(all(not sum(r) for r in new),'recomputed actual empty row')
  for i in range(N):
   for j in range(N):
    if sets[i]&sets[j]:require(new[i][j]==Q[i][j],'original intersecting support preserved')
  kp=[col[i]+delta*rr[i] for i in range(len(keep))];u=solve(aa,kp);schur=Q[deleted][deleted]-sum(x*y for x,y in zip(kp,u));require(schur==6*delta-kappa*delta*delta and schur>0,'exact original Schur')
  L=[[v+1 for v in r] for r in new];rank=ldl(L)[0];require(rank==N-1 and caprank(new,N)==N-1,'whole repaired PSD/rank/cap')
  star=[F(int(0 in st))-s/N for st in sets];require(all(not sum(x*y for x,y in zip(r,star)) for r in L),'exact centered largest-star kernel')
  # M row and zero diagonal on nonempty are algebraic consequences of L.
  M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)];require(all(sum(r)==1 for r in M),'original H row sums')
  records.append({'label':label,'delta':str(delta),'schur':str(schur),'lower_rank':rank,'cap_rank':N-1,'guaranteed_scaled_gap':str(1-8*delta)})
 raw=json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()
 return {'h':h,'N':N,'s':str(s),'all_original_pairs':N*N,'original_seed_gram_sha256':hashlib.sha256(raw).hexdigest(),'seed_core_rank':seed_core,'seed_lower_rank':seed_L,'kappa':str(kappa),'deleted_principal_size':len(keep),'repairs':records}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,required=True);ap.add_argument('--output',required=True);ap.add_argument('--check');a=ap.parse_args();require(2<=a.h<=10,'fixed literal bound');o=run(a.h)
 if a.check:require(json.dumps(json.loads(Path(a.check).read_text()),sort_keys=True,separators=(',',':'))==json.dumps(o,sort_keys=True,separators=(',',':')),'whole literal record')
 Path(a.output).write_text(json.dumps(o,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':'PASS','h':a.h,'N':o['N'],'kappa':o['kappa']}))
