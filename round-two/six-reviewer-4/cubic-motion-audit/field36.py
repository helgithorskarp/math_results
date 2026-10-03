"""Fresh rational single-generator Phi36 arithmetic; no target imports."""
from fractions import Fraction as F
def need(ok,why):
 if not ok:raise ValueError(why)
class K:
 def __init__(self,v=0):
  self.a=tuple(v.a)if isinstance(v,K)else(tuple(F(x)for x in v)+(F(0),)*12)[:12]if isinstance(v,(list,tuple))else(F(v),)+(F(0),)*11
 def __add__(self,o):
  o=K(o);return K([x+y for x,y in zip(self.a,o.a,strict=True)])
 __radd__=__add__
 def __neg__(self):return K([-x for x in self.a])
 def __sub__(self,o):return self+-K(o)
 def __rsub__(self,o):return K(o)+-self
 def __mul__(self,o):
  o=K(o);v=[F(0)]*23
  for i,x in enumerate(self.a):
   for j,y in enumerate(o.a):
    if x and y:v[i+j]+=x*y
  for i in range(22,11,-1):v[i-6]+=v[i];v[i-12]-=v[i]
  return K(v[:12])
 __rmul__=__mul__
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  v=K(1);a=self
  while n:
   if n&1:v=v*a
   a=a*a;n//=2
  return v
 def inverse(self):
  # Rational multiplication-column solve, distinct from reader's tower norm.
  columns=[(self*K([0]*j+[1])).a for j in range(12)]
  rows=[[columns[j][i]for j in range(12)]+[F(i==0)]for i in range(12)]
  for j in range(12):
   p=next((i for i in range(j,12)if rows[i][j]),None);need(p is not None,'field nonzero inverse');rows[j],rows[p]=rows[p],rows[j];t=rows[j][j];rows[j]=[x/t for x in rows[j]]
   for i in range(12):
    if i!=j:
     t=rows[i][j]
     if t:rows[i]=[x-t*y for x,y in zip(rows[i],rows[j],strict=True)]
  v=K([r[-1]for r in rows]);need(self*v==K(1),'whole inverse identity');return v
 def __truediv__(self,o):return self*K(o).inverse()
 def __rtruediv__(self,o):return K(o)*self.inverse()
 def __eq__(self,o):return self.a==K(o).a
 def conj(self):
  q=K([0,1]);return sum((x*q**((-j)%36)for j,x in enumerate(self.a)),K(0))
 def encode(self):return list(map(str,self.a))
z=K([0,1]);I=z**9;w=z**4;c=(z**2+z**34)/2
need(z**12-z**6+1==0 and z**18==-1 and I*I==-1 and w**9==1,'whole defining relations')
need(8*c**3-6*c-1==0,'selected real cubic');need(c.conj()==c,'real c')
def real_coeff(a):
 # Exact three-dimensional c-basis extraction, all12 coordinates retained.
 a=K(a);base=[K(1),c,c*c];rows=[[v.a[i]for v in base]+[a.a[i]]for i in range(12)];j=0
 for col in range(3):
  p=next((i for i in range(j,12)if rows[i][col]),None);need(p is not None,'independent real basis');rows[j],rows[p]=rows[p],rows[j];t=rows[j][col];rows[j]=[x/t for x in rows[j]]
  for i in range(12):
   if i!=j:
    t=rows[i][col]
    if t:rows[i]=[x-t*y for x,y in zip(rows[i],rows[j],strict=True)]
  j+=1
 need(all(not any(r[:3])and not r[3]for r in rows[3:]),'entire real cubic field membership')
 return [str(r[3])for r in rows[:3]]
