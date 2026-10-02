"""New reviewer arithmetic; only CPython standard library. No author imports."""
from fractions import Fraction as F
from math import comb
import json,hashlib
COUNTS={}
def need(ok,tag):
 COUNTS[tag]=COUNTS.get(tag,0)+1
 if not ok:raise ValueError(tag)
def text(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):text(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [text(y) for y in x]
 return x
def canonical(x):return json.dumps(text(x),sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def mv(a,x):return [dot(r,x) for r in a]
def energy(a,x):return dot(x,mv(a,x))
def polyadd(a,b):
 c=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 while len(c)>1 and c[-1]==0:c.pop()
 return c
def scale(a,s):return [x*s for x in a]
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return polyadd(c,[0])
def shift(a,s):
 return [sum(F(a[j])*comb(j,i)*s**(j-i) for j in range(i,len(a))) for i in range(len(a))]
def gauss_null(a):
 """RREF full homogeneous constraint matrix, free columns ascending."""
 a=[[F(x) for x in r] for r in a];rows=len(a);cols=len(a[0]);piv=[];i=0
 for j in range(cols):
  h=next((h for h in range(i,rows) if a[h][j]),None)
  if h is None:continue
  a[i],a[h]=a[h],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
  for h in range(rows):
   if h!=i and a[h][j]:
    v=a[h][j];a[h]=[x-v*y for x,y in zip(a[h],a[i])]
  piv.append(j);i+=1
  if i==rows:break
 free=[j for j in range(cols) if j not in piv];out=[]
 for j in free:
  v=[F(0)]*cols;v[j]=1
  for h,p in enumerate(piv):v[p]=-a[h][j]
  out.append(v)
 return piv,free,out
