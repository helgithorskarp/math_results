"""Complete rational-norm, square-class-five contact census for (L+M)+vM."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import isqrt
import geometry as g

def rational_norm(a):
 n=g.norm(a)
 return n[0] if not any(n[1:]) else None

def rational_sqrt(q):
 if q<0:return None
 a=isqrt(q.numerator);b=isqrt(q.denominator)
 return F(a,b) if a*a==q.numerator and b*b==q.denominator else None

def sources():
 L,M=g.atoms()
 P=sorted({g.add(a,b)for a,b in product(L,M)})
 return L,M,P

def phases():
 L,M,P=sources()
 da={g.sub(a,b)for a,b in product(P,repeat=2)if a!=b}
 db={g.sub(a,b)for a,b in product(M,repeat=2)if a!=b}
 da={a:rational_norm(a)for a in da};da={a:n for a,n in da.items()if n is not None}
 db={a:rational_norm(a)for a in db};db={a:n for a,n in db.items()if n is not None}
 found=Counter()
 for a,na in da.items():
  for b,nb in db.items():
   S=na+nb-1;delta=4*na*nb-S*S
   q=rational_sqrt(F(delta,5))
   if q is None or not q:continue
   c=g.mul(g.conj(a),b)
   x=g.scale(g.conj(c),-S/(2*na*nb))
   y=g.scale(g.mul(g.make(y={0:1}),g.conj(c)),q/(2*na*nb))
   for sign in (-1,1):found[x,g.scale(y,sign)]+=1
 return sorted(found),{'rational_P_differences':len(da),'rational_M_differences':len(db),
                       'phases':len(found),'equation_multiplicities':dict(sorted(Counter(found.values()).items()))}

def construct(phase):
 L,M,P=sources();x,y=phase
 v=g.add(x,g.mul(g.make({4:1}),y))
 if g.norm(v)!=(1,)+(0,)*15:raise ValueError('nonunit phase')
 points=[g.add(p,g.mul(v,m))for p,m in product(P,M)]
 if len(set(points))!=len(points):raise ValueError('physical collision')
 den,points=g.integral(points)
 ids={'L':[P.index(p)*7 for p in L],
      'first_M':[P.index(p)*7 for p in M],
      'last_M':[P.index(g.ZERO)*7+i for i in range(7)]}
 return den,points,ids
