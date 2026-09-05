from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,comb
from collections import defaultdict,Counter
import importlib.util,json,time
from hashlib import sha256
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
p=ROOT/'hadwiger_nelson_dense506_origin_attachment/controls.py'
if sha256(p.read_bytes()).hexdigest()!='b73d839cdfd72ed8020e0122124f7768cc62852289f1e4d6db74079add47a1c4':raise ValueError('source geometry pin mismatch')
s=importlib.util.spec_from_file_location('C',p);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
D=2592
ZERO=(0,)*4;ONE=(1,0,0,0);L=(-408,72)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,n):return tuple(n*x for x in a)
def rm(a,b):return (a[0]*b[0]+33*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def mul(a,b):
 x=rm(a[:2],b[:2]);y=rm(rm(a[2:],b[2:]),L);z=add(rm(a[:2],b[2:]),rm(a[2:],b[:2]))
 return add(x,y)+z
def inv(a):
 x=sub(rm(a[:2],a[:2]),rm(rm(a[2:],a[2:]),L));d=x[0]*x[0]-33*x[1]*x[1]
 if not d:raise ZeroDivisionError
 ri=(Q(x[0],d),Q(-x[1],d));return rm(a[:2],ri)+neg(rm(a[2:],ri))
def norm(x,y):return add(mul(x,x),scale(mul(y,y),3))
def canonical(x,y,den):
 D=lcm(*(Q(a,den).denominator for a in x+y));nums=tuple(int(Q(a,den)*D) for a in x+y);g=gcd(D,*nums)
 return (D//g,)+tuple(a//g for a in nums)
def host():
 A,V=C.read(159),C.read(214);t=(15,3,15,-1,0,0,0,0);u=(-18,-6,-30,6,3,0,6,1)
 B=list(dict.fromkeys(A+[C.add(C.conjugate(a),t) for a in A]));H=[C.add(v,C.scale(V[10],-1)) for v in V]
 points=[C.scale(b,72) for b in B]+[C.multiply(u,H[j]) for j in range(214) if j!=10]
 assert len(points)==len(set(points))==506
 return [(tuple(v[i] for i in (0,1,4,5)),tuple(v[i] for i in (2,3,6,7))) for v in points]
def embedding(p,z,r,v):return (v[0]+z*v[1]+r*v[2]+z*r*v[3])%p

def distances(P):
 n=len(P);ds=[[None]*n for _ in P];adj=[0]*n;edges=[]
 for i,(x,y) in enumerate(P):
  for j in range(i+1,n):
   X,Y=P[j];d=norm(sub(x,X),sub(y,Y));ds[i][j]=ds[j][i]=d
   if d==scale(ONE,2592**2):edges.append((i,j));adj[i]|=1<<j;adj[j]|=1<<i
 assert len(edges)==2389
 return ds,adj,edges

def screen(P,ds,adj,p,z,r,limit=None):
 n=len(P) if limit is None else limit;mod=[[0]*n for _ in range(n)];deninv=pow(2592**2,-1,p)
 for i in range(n):
  for j in range(i+1,n):mod[i][j]=mod[j][i]=embedding(p,z,r,ds[i][j])*deninv%p
 rows=[];known=0
 for i in range(n):
  for j in range(i+1,n):
   a=mod[i][j];a2=a*a;common=adj[i]&adj[j]
   for k in range(j+1,n):
    if common&adj[k]:known+=1;continue
    b=mod[i][k];c=mod[j][k]
    if (a*b*c-2*(a*b+a*c+b*c)+a2+b*b+c*c)%p==0:rows.append((i,j,k))
 return rows,{'prime':p,'z':z,'r':r,'triples':comb(n,3),'known_host_centre_triples':known,'survivors':len(rows),'survivor_sha256':digest(rows)}


def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def candidates(P,ds,adj):
 p,z,r=10007,283,6718
 if z*z%p!=33 or r*r%p!=(-408+72*z)%p:raise ValueError('bad modular map')
 rows,summary=screen(P,ds,adj,p,z,r)
 centres=defaultdict(list);positive=[];actual={canonical(x,y,D) for x,y in P}
 for i,j,k in rows:
  a,b,c=ds[i][j],ds[i][k],ds[j][k]
  heron=sub(scale(add(add(mul(a,b),mul(a,c)),mul(b,c)),2),add(add(mul(a,a),mul(b,b)),mul(c,c)))
  if mul(mul(a,b),c)!=scale(heron,D**2):continue
  dx,dy=sub(P[j][0],P[i][0]),sub(P[j][1],P[i][1]);ex,ey=sub(P[k][0],P[i][0]),sub(P[k][1],P[i][1]);det=sub(mul(dx,ey),mul(ex,dy))
  if det==ZERO:raise ValueError('collinear unit-circle triple')
  v=inv(scale(det,6));xx=mul(scale(sub(mul(a,ey),mul(b,dy)),3),v);yy=mul(sub(mul(dx,b),mul(ex,a)),v)
  h=canonical(add(P[i][0],xx),add(P[i][1],yy),D)
  if h in actual:raise ValueError('host-centre removal failed')
  positive.append((i,j,k));centres[h].append((i,j,k))
 points=sorted(centres);neighbors=[sorted(set(x for t in centres[h] for x in t)) for h in points]
 if not all(len(centres[h])==comb(len(nn),3) for h,nn in zip(points,neighbors)):raise ValueError('incomplete triple incidences')
 return points,neighbors,positive,summary

def unit(h,k):
 dh,dk=h[0],k[0];dx=tuple(h[i]*dk-k[i]*dh for i in range(1,5));dy=tuple(h[i]*dk-k[i]*dh for i in range(5,9))
 return norm(dx,dy)==scale(ONE,(dh*dk)**2)
def modpoint(h):
 p,z,r=10007,283,6718
 if h[0]%p==0:return None
 invd=pow(h[0],-1,p);return (embedding(p,z,r,h[1:5])*invd%p,embedding(p,z,r,h[5:])*invd%p)
def maybe(h,k):
 if h is None or k is None:return True
 return ((h[0]-k[0])**2+3*(h[1]-k[1])**2-1)%10007==0

def graph(P,points,neighbors):
 hostpts=[canonical(x,y,D) for x,y in P];mh=list(map(modpoint,hostpts));mc=list(map(modpoint,points));test=0;rebuild=[]
 for a,ma in zip(points,mc):
  neigh=[]
  for j,(h,mh0) in enumerate(zip(hostpts,mh)):
   if maybe(ma,mh0):
    test+=1
    if unit(a,h):neigh.append(j)
  rebuild.append(neigh)
 if neighbors!=rebuild:raise ValueError('incorrect candidate-host adjacency')
 cedges=[];cp=0
 for i in range(len(points)):
  for j in range(i+1,len(points)):
   if maybe(mc[i],mc[j]):
    cp+=1
    if unit(points[i],points[j]):cedges.append((i,j))
 return cedges,{'host_candidate_pairs':len(points)*len(P),'exact_host_candidate_tests_after_screen':test,'candidate_pairs':comb(len(points),2),'exact_candidate_pair_tests_after_screen':cp,'noninvertible_candidate_denominators':sum(x is None for x in mc)}
