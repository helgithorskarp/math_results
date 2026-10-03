"""Fresh Q(c)[s,i] reader: c^3=(6c+1)/8, s^2=1-c^2, i^2=-1."""
from fractions import Fraction as F
from itertools import product
def need(ok,why):
 if not ok:raise ValueError(why)
basis=list(product(range(3),range(2),range(2)))
class T:
 def __init__(self,v=0):
  self.a=dict(v.a)if isinstance(v,T)else{k:F(x)for k,x in v.items()if x}if isinstance(v,dict)else({(0,0,0):F(v)}if v else{})
 def __add__(self,o):
  o=T(o);d=dict(self.a)
  for k,v in o.a.items():d[k]=d.get(k,F(0))+v
  return T(d)
 __radd__=__add__
 def __neg__(self):return T({k:-x for k,x in self.a.items()})
 def __sub__(self,o):return self+-T(o)
 def __rsub__(self,o):return T(o)+-self
 def __mul__(self,o):
  o=T(o);d={}
  def put(a,b,j,v):
   if not v:return
   if j>=2:return put(a,b,j-2,-v)
   if b>=2:put(a,b-2,j,v);put(a+2,b-2,j,-v);return
   if a>=3:put(a-2,b,j,3*v/4);put(a-3,b,j,v/8);return
   key=(a,b,j);d[key]=d.get(key,F(0))+v
  for (a,b,j),x in self.a.items():
   for (e,f,k),y in o.a.items():put(a+e,b+f,j+k,x*y)
  return T(d)
 __rmul__=__mul__
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  out=T(1);v=self
  while n:
   if n&1:out*=v
   v*=v;n//=2
  return out
 def flip(self,b=False,i=False):return T({(a,e,j):(-1)**(e*int(b)+j*int(i))*v for (a,e,j),v in self.a.items()})
 def inverse(self):
  # Successive quadratic conjugate norms, then cubic Euclidean elimination.
  conj=self.flip(i=True);q=self*conj;need(all(j==0 for a,b,j in q.a),'first norm in real tower')
  real=q*q.flip(b=True);need(all(b==j==0 for a,b,j in real.a),'second norm in cubic field')
  # Extended Euclid in Q[c] against 8c^3-6c-1.
  def trim(v):
   while v and not v[-1]:v.pop()
   return v
  def sub(a,b):return trim([(a[k]if k<len(a)else F(0))-(b[k]if k<len(b)else F(0))for k in range(max(len(a),len(b)))])
  def mul(a,b):
   v=[F(0)]*max(0,len(a)+len(b)-1)
   for k,x in enumerate(a):
    for l,y in enumerate(b):v[k+l]+=x*y
   return trim(v)
  def div(a,b):
   a=a[:];v=[F(0)]*max(0,len(a)-len(b)+1)
   while a and len(a)>=len(b):
    k=len(a)-len(b);x=a[-1]/b[-1];v[k]=x;a=sub(a,[F(0)]*k+[x*y for y in b])
   return trim(v),a
  r0=[F(-1),F(-6),F(0),F(8)];r1=trim([real.a.get((k,0,0),F(0))for k in range(3)]);u0=[];u1=[F(1)]
  while r1:qv,rem=div(r0,r1);r0,r1=r1,rem;u0,u1=u1,sub(u0,mul(qv,u1))
  need(len(r0)==1 and r0[0]!=0,'nonzero cubic norm')
  inv=T({(k,0,0):v/r0[0]for k,v in enumerate(u0)});v=conj*q.flip(b=True)*inv;need(v*self==T(1),'whole tower inverse');return v
 def __truediv__(self,o):return self*T(o).inverse()
 def __rtruediv__(self,o):return T(o)*self.inverse()
 def __eq__(self,o):return self.a==T(o).a
 def encode(self):return [str(self.a.get(k,F(0)))for k in basis]
c=T({(1,0,0):1});s=T({(0,1,0):1});I=T({(0,0,1):1});w=(c+I*s)**2
# z36=cos10+i sin10, reconstructed from sin80 and cos80.
z=4*s*c*(2*c*c-1)+I*(2*(2*c*c-1)**2-1)
need(z**12-z**6+1==0 and z**9==I and z**4==w and z**2==c+I*s,'all12-dimensional field bridge relations')
z_powers=[z**j for j in range(12)]
def read_field(coords):
 need(type(coords)is list and len(coords)==12 and all(type(x)is str for x in coords),'whole typed twelve coordinates')
 return sum((F(x)*q for x,q in zip(coords,z_powers,strict=True)),T(0))
