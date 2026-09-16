"""Exact paired-circle boundary in pairwise quadratic extensions of Q(sqrt(3))."""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
import hashlib,json
Z=(F(0),F(0));O=(F(1),F(0));S=(F(0),F(1))
def need(p,m):
 if not p:raise ValueError(m)
def k(a=0,b=0):return F(a),F(b)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[0],-x[1]
def sub(x,y):return add(x,neg(y))
def mul(x,y):return x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def scale(x,n):return x[0]*n,x[1]*n
def inv(x):
 n=x[0]*x[0]-3*x[1]*x[1];need(n!=0,'nonzero inverse');return x[0]/n,-x[1]/n
def div(x,y):return mul(x,inv(y))
def sign(x):
 a,b=x
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if (a>0)==(b>0):return 1 if a>0 else -1
 c=a*a-3*b*b;return ((c>0)-(c<0))*(1 if a>0 else -1)
def rational_sqrt(x):
 if x<0:return None
 n,d=isqrt(x.numerator),isqrt(x.denominator)
 return F(n,d) if n*n==x.numerator and d*d==x.denominator else None

def square_root(x):
 """Return positive sqrt(x) in K if it exists, otherwise None."""
 if sign(x)<0:return None
 if x==Z:return Z
 a,b=x
 if not b:
  s=rational_sqrt(a)
  if s is not None:return k(s)
  s=rational_sqrt(a/3)
  return k(0,s) if s is not None else None
 n=rational_sqrt(a*a-3*b*b)
 if n is None:return None
 for t in (n,-n):
  u=rational_sqrt((a+t)/2)
  if u:
   y=(u,b/(2*u))
   need(mul(y,y)==x,'square identity')
   return y if sign(y)>0 else neg(y)
 return None

CZ=(Z,Z);CO=(O,Z)
def ca(x,y):return add(x[0],y[0]),add(x[1],y[1])
def cn(x):return neg(x[0]),neg(x[1])
def cs(x,y):return ca(x,cn(y))
def cm(x,y):return sub(mul(x[0],y[0]),mul(x[1],y[1])),add(mul(x[0],y[1]),mul(x[1],y[0]))
def ck(x,s):return mul(x[0],s),mul(x[1],s)
def dot(x,y):return add(mul(x[0],y[0]),mul(x[1],y[1]))
def norm(x):return dot(x,x)
def J(x):return neg(x[1]),x[0]

class Geometry:
 def __init__(self):self.roots=[]
 def point(self,a,b=CZ,s=None):
  if s is None or b==CZ:return a,CZ,-1
  need(sign(s)>0,'positive physical radical')
  u=square_root(s)
  if u is not None:return ca(a,ck(b,u)),CZ,-1
  for i,t in enumerate(self.roots):
   u=square_root(div(s,t))
   if u is not None:return a,ck(b,u),i
  self.roots.append(s);return a,b,len(self.roots)-1
 def equations(self,p,q,target):
  a=cs(p[0],q[0]);terms={}
  for b,i in [(p[1],p[2]),(cn(q[1]),q[2])]:
   if i>=0:terms[i]=ca(terms.get(i,CZ),b)
  terms=[(i,b) for i,b in sorted(terms.items()) if b!=CZ]
  constant=sub(norm(a),k(target));rest=[]
  for i,b in terms:
   constant=add(constant,mul(self.roots[i],norm(b)));rest.append(scale(dot(a,b),2))
  for (i,b),(j,c) in combinations(terms,2):rest.append(scale(dot(b,c),2))
  return [constant]+rest
 def equal_norm(self,p,q,target):return all(x==Z for x in self.equations(p,q,target))
 def roots_of_circles(self,a,b):
  d=cs(b,a);q=norm(d);need(sign(q)>0,'distinct circle centres')
  if sign(sub(q,k(4)))>0:return []
  m=ck(ca(a,b),k(F(1,2)))
  if q==k(4):return [self.point(m)]
  delta=div(sub(k(4),q),q);off=ck(J(d),k(F(1,2)))
  return [self.point(m,off,delta),self.point(m,cn(off),delta)]

def enc_k(x):return [[a.numerator,a.denominator] for a in x]
def enc_c(x):return [enc_k(t) for t in x]
def enc_point(p):return [enc_c(p[0]),enc_c(p[1]),p[2]]
def raw(x):return (json.dumps(x,separators=(',',':'),sort_keys=True)+'\n').encode()
def sha(x):return hashlib.sha256(raw(x)).hexdigest()

def construct():
 g=Geometry();omega=(k(F(1,2)),k(0,F(1,2)));r=(k(F(3,5)),k(F(4,5)));t=cm(cs(CO,r),omega)
 centres=[CZ,CO,t,ca(t,r)];need(len(set(centres))==4,'four distinct centres')
 need(norm(cs(centres[1],centres[0]))==O and norm(cs(centres[3],centres[2]))==O,'unit centre pairs')
 need(all(norm(cs(omega,c))==O for c in centres),'common unit neighbour')
 u=[CO]
 for _ in range(5):u.append(cm(u[-1],omega))
 dirs=set(u+[cm(r,v) for v in u]);need(len(dirs)==12,'two distinct direction orbits')
 P=sorted(set(ca(c,v) for c in centres for v in dirs));need(set(centres)<=set(P) and len(P)<=48,'kernel cap')
 # Common neighbour supplies both intersections by reflection for every cross slot.
 cross=[]
 for i in (0,1):
  for j in (2,3):
   roots=[omega,cs(ca(centres[i],centres[j]),omega)]
   need(len(set(roots))==2 and all(norm(cs(z,centres[i]))==O and norm(cs(z,centres[j]))==O for z in roots),'complete mixed roots')
   need(all(z in P for z in roots),'mixed roots in kernel');cross.append(norm(cs(centres[j],centres[i])))
 expected=[k(F(4,5)),k(F(7,5),F(4,5)),k(F(7,5),-F(4,5)),k(F(4,5))];need(cross==expected,'cross distances')
 # Actual signed exceptional incidence x=y=omega, 00 -> 11, k=1.
 need(cs(omega,CO)==cm(omega,omega),'exceptional direction incidence')
 d=t;e=cs(ca(t,r),CO);v=cm((omega[0],neg(omega[1])),e)
 q,w,H=norm(d),norm(e),dot(d,v)
 factor=add(mul(mul(q,w),sub(sub(add(q,w),scale(H,2)),k(4))),scale(mul(H,H),4))
 need(factor==Z and d==v,'singular exceptional factor')
 points={g.point(x) for x in P};routes=[];rootcounts={0:0,1:0,2:0}
 for x in P:
  if x in centres:continue
  for h,c in enumerate(centres):
   roots=g.roots_of_circles(x,c);rootcounts[len(roots)]+=1
   for z in roots:
    need(g.equal_norm(z,g.point(x),1) and g.equal_norm(z,g.point(c),1),'promised circle contacts')
    points.add(z);routes.append((P.index(x),h,z))
 points=sorted(points);need(len(points)<=400,'predeclared cap')
 ids={x:i for i,x in enumerate(points)};Pids=[ids[g.point(x)] for x in P]
 edges=[(i,j) for i,j in combinations(range(len(points)),2) if g.equal_norm(points[i],points[j],1)]
 data={'roots':[enc_k(x) for x in g.roots],'points':[enc_point(x) for x in points],'edges':edges}
 summary={'vertices':len(points),'edges':len(edges),'kernel_vertices':len(P),'kernel_edges':sum(i in set(Pids) and j in set(Pids) for i,j in edges),'boundary_added_vertices':len(points)-len(P),'base_radical_classes':len(g.roots),'all_pairs':len(points)*(len(points)-1)//2,'circle_pair_counts':rootcounts,'boundary_root_incidences':len(routes),'centres':[ids[g.point(x)] for x in centres],'common_neighbour':ids[g.point(omega)],'kernel_ids':Pids,'coordinate_sha256':sha({'roots':data['roots'],'points':data['points']}),'edge_sha256':sha(edges),'exact_exceptional_factor_zero':True,'proved_support_cap':400}
 return g,points,edges,summary
