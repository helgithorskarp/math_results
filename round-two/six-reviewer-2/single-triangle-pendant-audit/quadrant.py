"""New reviewer bivariate rational ring and tensor-Newton determinant checker.

No target implementation. Extends the reviewer's older one-variable
Gaussian/Newton method, explicitly credited in the accompanying proof.
All denominators must be products of coefficient-positive polynomials.
Fixed guards: 512 monomials, separate degree<=180, identity grid<=4096.
"""
from fractions import Fraction as F
from math import gcd,lcm
from linear import need,digest

FACTORS=[]
INDEX={}
def clean(p):
 p={k:F(v)for k,v in p.items()if v};need(len(p)<=512,'fixed512 monomial guard');return p
def constant(x):return clean({(0,0):x})
def padd(p,q):
 z=dict(p)
 for k,v in q.items():z[k]=z.get(k,F(0))+v
 return clean(z)
def pmul(p,q):
 z={}
 for (i,j),a in p.items():
  for (k,h),b in q.items():z[i+k,j+h]=z.get((i+k,j+h),F(0))+a*b
 return clean(z)
def pdiv(p,q):
 """Exact lexicographic multivariate long division, no modular oracle."""
 need(q,'nonzero polynomial divisor');r=dict(p);z={};lead=max(q);b=q[lead]
 while r:
  a=max(r);d=(a[0]-lead[0],a[1]-lead[1])
  if min(d)<0:return None
  v=r[a]/b;z[d]=z.get(d,F(0))+v
  for (i,j),w in q.items():
   k=(i+d[0],j+d[1]);r[k]=r.get(k,F(0))-v*w
   if not r[k]:del r[k]
 return clean(z)
def positive(p):return p.get((0,0),F(0))>0 and all(v>0 for v in p.values())
def normalize(p):
 d=lcm(*(v.denominator for v in p.values()));g=0
 for v in p.values():g=gcd(g,int(v*d))
 scale=F(g,d);return {k:v/scale for k,v in p.items()},scale
def register(p):
 need(positive(p),'every denominator has positive constant and nonnegative coefficients')
 p,scale=normalize(p);key=tuple(sorted(p.items()))
 if key not in INDEX:INDEX[key]=len(FACTORS);FACTORS.append(p)
 return INDEX[key],scale
def times_factors(p,e):
 for i,k in sorted(e.items()):
  for _ in range(k):p=pmul(p,FACTORS[i])
 return p
def peval(p,u,v):
 if not p:return F(0)
 a=[F(1)];b=[F(1)]
 for _ in range(max(i for i,j in p)):a.append(a[-1]*u)
 for _ in range(max(j for i,j in p)):b.append(b[-1]*v)
 return sum(x*a[i]*b[j]for (i,j),x in p.items())
def precord(p):return [[i,j,str(v)]for (i,j),v in sorted(p.items())]

class R:
 def __init__(self,p=0,e=None):
  if isinstance(p,R):self.p=p.p;self.e=p.e;return
  p=clean(p if isinstance(p,dict)else constant(p));e={k:v for k,v in (e or {}).items()if v}
  need(all(type(k)is int and 0<=k<len(FACTORS)and type(v)is int and v>0 for k,v in e.items()),'registered positive denominators')
  if not p:e={}
  else:
   for i in sorted(tuple(e)):
    while e.get(i,0):
     q=pdiv(p,FACTORS[i])
     if q is None:break
     p=q;e[i]-=1
     if not e[i]:del e[i]
  self.p=p;self.e=e
 def __add__(a,b):
  b=R(b);e={i:max(a.e.get(i,0),b.e.get(i,0))for i in a.e.keys()|b.e.keys()}
  p=times_factors(a.p,{i:k-a.e.get(i,0)for i,k in e.items()})
  q=times_factors(b.p,{i:k-b.e.get(i,0)for i,k in e.items()})
  return R(padd(p,q),e)
 __radd__=__add__
 def __neg__(a):return R({k:-v for k,v in a.p.items()},a.e)
 def __sub__(a,b):return a+-R(b)
 def __rsub__(a,b):return R(b)+-a
 def __mul__(a,b):
  b=R(b);e={i:a.e.get(i,0)+b.e.get(i,0)for i in a.e.keys()|b.e.keys()};return R(pmul(a.p,b.p),e)
 __rmul__=__mul__
 def __truediv__(a,b):
  b=R(b);need(b.p,'nonzero rational divisor')
  if len(b.p)==1 and (0,0)in b.p:return R({k:v/b.p[0,0]for k,v in times_factors(a.p,b.e).items()},a.e)
  i,scale=register(b.p);e=dict(a.e);e[i]=e.get(i,0)+1
  return R({k:v/scale for k,v in times_factors(a.p,b.e).items()},e)
 def __rtruediv__(a,b):return R(b)/a
 def __pow__(a,k):
  need(type(k)is int and k>=0,'nonnegative integer power');z=R(1)
  for _ in range(k):z=z*a
  return z
 def __eq__(a,b):return not (a-R(b)).p
 def value(a,u,v):return peval(a.p,u,v)/peval(times_factors(constant(1),a.e),u,v)
 def record(a):return {'numerator':precord(a.p),'denominator':[[i,k]for i,k in sorted(a.e.items())]}

def clear(A):
 B=[];records=[]
 for row in A:
  keys=set().union(*(x.e.keys()for x in row));e={i:max(x.e.get(i,0)for x in row)for i in keys}
  ps=[times_factors(x.p,{i:k-x.e.get(i,0)for i,k in e.items()})for x in row]
  d=lcm(*(v.denominator for p in ps for v in p.values()));B.append([{k:v*d for k,v in p.items()}for p in ps]);records.append({'integer':d,'factors':sorted(e.items())})
 return B,records
def det(A):
 B=[list(map(F,r))for r in A];n=len(B);z=F(1)
 for j in range(n):
  k=next((i for i in range(j,n)if B[i][j]),None)
  if k is None:return F(0)
  if k!=j:B[j],B[k]=B[k],B[j];z=-z
  pivot=B[j][j];z*=pivot
  for i in range(j+1,n):
   x=B[i][j]/pivot
   for k in range(j+1,n):B[i][k]-=x*B[j][k]
 return z
def newton(values):
 d=[];a=list(values)
 while a:d.append(a[0]);a=[y-x for x,y in zip(a,a[1:])]
 p={};basis=constant(1)
 for j,x in enumerate(d):
  p=padd(p,{k:x*v for k,v in basis.items()});basis={k:v/F(j+1)for k,v in pmul(basis,{(0,0):-j,(1,0):1}).items()}
 return p
def reconstruct(A):
 # Each Leibniz product chooses one entry per row. These separate row
 # maximum degree sums therefore prove complete bounds before evaluations.
 du=sum(max((i for p in row for i,j in p),default=0)for row in A)
 dv=sum(max((j for p in row for i,j in p),default=0)for row in A)
 need(max(du,dv)<=180 and (du+1)*(dv+1)<=4096,'fixed180degree/4096grid guard')
 values=[[det([[peval(p,u,v)for p in row]for row in A])for v in range(dv+1)]for u in range(du+1)]
 # Interpolate v first, then each coefficient independently in u.
 vp=[newton(row)for row in values];out={}
 for j in range(dv+1):
  up=newton([p.get((j,0),F(0))for p in vp])
  for (i,z),a in up.items():need(z==0,'univariate coefficient reconstruction');out[i,j]=a
 out=clean(out)
 need(all(x.denominator==1 for x in out.values()),'integer determinant coefficients')
 need(all(peval(out,u,v)==values[u][v]for u in range(du+1)for v in range(dv+1)),'ALL complete grid identities')
 return out,(du,dv),values
def certificate(A,name):
 need(all(A[i][j]==A[j][i]for i in range(len(A))for j in range(len(A))),'original rational symmetry')
 B,scaling=clear(A);records=[]
 for k in range(1,len(A)+1):
  p,bounds,values=reconstruct([r[:k]for r in B[:k]]);need(positive(p),'complete coefficient-positive leading determinant')
  records.append({'order':k,'separate_degree_bounds':bounds,'coefficients':precord(p),'whole_coefficients_sha256':digest(precord(p)),'coefficient_count':len(p),'full_grid_points':(bounds[0]+1)*(bounds[1]+1),'whole_grid_sha256':digest(values)})
 return {'name':name,'matrix':[[x.record()for x in row]for row in A],'positive_row_clearings':scaling,'leading_minors':records}
