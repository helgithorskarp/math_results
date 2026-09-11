"""Packing-sensitive spanning-forest union bounds; all arithmetic exact."""
from math import comb,factorial
from fractions import Fraction as F
from functools import lru_cache
from bounds import M

def C(n,k):return comb(n,k) if 0<=k<=n else 0

def pair_tail(N,L,r,i):
 R=N-L;union=2*r-i
 same=C(N-union,L-union)+C(N-union,L)
 cross=2*C(N-2*r,L-r) if i==0 else 0
 return F(same+cross,C(N,L))

@lru_cache(None)
def component_cap(N,r,t):
 # Bound a family of r-subsets with pairwise intersection at most t-1.
 best=C(N,t)//C(r,t)
 return max(c for c in range(1,best+1) if (lambda qr:N*qr[0]*(qr[0]-1)//2+qr[1]*qr[0])(divmod(c*r,N))<=(t-1)*c*(c-1)//2)

@lru_cache(None)
def tail(N,L,r,m):
 if not m:return F(0)
 single=F(C(L,r)+C(N-L,r),C(N,r))
 ps=[pair_tail(N,L,r,i) for i in range(r)]
 base=min(ps);ans=m*single-(m-1)*base
 prev=base
 for t in range(1,r):
  val=min(ps[t:])
  if val>prev:
   K=component_cap(N,r,t)
   ans-=max(0,m-K)*(val-prev)
   prev=val
 return ans

def star_bound(v,m,d,r=5):
 N=v-1;L=N//2;R=N-L
 e=(r-1)*d-N
 T=d*(d-1)-2*((e+r-3)//(r-2))
 pp=F(M.fall(L,r-1)*M.fall(R,r-1)*factorial(N-2*(r-1)),factorial(N))
 qq=min(F(M.fall(L,r-1)*M.fall(R,2*(r-1))*factorial(N-3*(r-1)),factorial(N)),F(M.fall(L,2*(r-1))*M.fall(R,r-1)*factorial(N-3*(r-1)),factorial(N)))
 pivot=T*pp-max(0,T-d)*qq
 p_single=d*F(C(L,r-1),C(N,r-1))
 return tail(N,L,r,m-d)+min(pivot,p_single)
