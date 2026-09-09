"""Exact Q(omega) univariate arithmetic; omega^2=omega-1."""
from fractions import Fraction as Q
ZERO=(Q(0),Q(0)); ONE=(Q(1),Q(0))
def val(a):return Q(a[0]),Q(a[1])
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def mul(a,b):
 x,y=a;u,v=b
 return x*u-y*v,x*v+y*u+y*v
def inv(a):
 x,y=a;n=x*x+x*y+y*y
 if not n:raise ValueError('zero inverse')
 return (x+y)/n,-y/n
def trim(p):
 p=list(p)
 while p and p[-1]==ZERO:p.pop()
 return p
def pmul(p,q):
 out=[ZERO]*(len(p)+len(q)-1) if p and q else []
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]=add(out[i+j],mul(a,b))
 return trim(out)
def divmod_poly(p,q):
 if not q:raise ValueError('zero polynomial divisor')
 r=trim(p);out=[ZERO]*max(0,len(r)-len(q)+1);lc=inv(q[-1])
 while r and len(r)>=len(q):
  k=len(r)-len(q);a=mul(r[-1],lc);out[k]=a
  for j,b in enumerate(q):r[k+j]=add(r[k+j],neg(mul(a,b)))
  r=trim(r)
 return trim(out),r
def monic(p):return [mul(x,inv(p[-1])) for x in p] if p else []
def gcd_poly(p,q):
 while q:_,r=divmod_poly(p,q);p,q=q,r
 return monic(p)
def derivative(p):return trim([(a[0]*i,a[1]*i) for i,a in enumerate(p)][1:])
def simple_root_factor(p):
 p=trim(list(map(val,p)))
 g=gcd_poly(p,derivative(p));sf,r=divmod_poly(p,g)
 if r:raise ValueError('squarefree division')
 repeated=gcd_poly(sf,derivative(p));simple,r=divmod_poly(sf,repeated)
 if r:raise ValueError('simple-root division')
 return monic(simple)
