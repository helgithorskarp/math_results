"""Exact implementation of the original original deficit reduction.

No solver or floating point decides a scalar identity or sign here.
The written proof, not bounded validation, supplies all-order coverage.
"""
from fractions import Fraction as Q
from math import comb,isqrt

def require(test,message):
 if not test:raise ValueError(message)

def parameters(n,k):
 require(type(n) is int and n>=6,'Original order n>=6')
 require(type(k) is int and 2<=k<=(n-2)//2,'Proper support cutoff')
 N=2**n-n-1;s=2**(n-1)-n;h=N-s;r=n-1
 A=sum(a*a*comb(n,a) for a in range(2,k+1))
 constant=Q(n*h-n*(n-1)*s)+Q(h*h-s*s,h)*A
 return N,s,h,r,constant

def check_deficit(n,z):
 s=2**(n-1)-n
 require(type(z) is Q and 0<=z<=2*s-2,'Original complement pair bounds')

def phi(n,a,z,odd=True):
 check_deficit(n,z);N=2**n-n-1;r=n-1;x=Q(a)-Q(n,2)
 require(r+z>0 and N-z>=n+1,'Strict uniform denominators')
 if odd:return Q(n*n*r,4)*z/(r+z)-Q(N)*x*x*z/(N-z)
 return Q(n*n*r,4)*z/(r+z)-x*x*z

def optimizer(n,a,z):
 check_deficit(n,z);N=2**n-n-1;r=n-1;x=Q(a)-Q(n,2)
 return Q(n,2)*z/(r+z),-z*x/(N-z)

def sqrt_bracket(value,denominator=10**12):
 require(type(value) is Q and value>=0 and type(denominator) is int and denominator>0,'Rational sqrt bracket')
 numerator=isqrt(value.numerator*denominator*denominator//value.denominator)
 low=Q(numerator,denominator);high=Q(numerator+1,denominator)
 require(low*low<=value<high*high,'Exact square-root bracket')
 return low,high

def rational_profile(n,k,lam,denominator=10**12):
 N,s,h,r,c=parameters(n,k)
 require(type(lam) is Q and lam>=0,'Nonnegative exact dual multiplier')
 profiles=[]
 for a in range(k+1,n-k):
  x=Q(a)-Q(n,2);low,high=sqrt_bracket(lam+x*x,denominator)
  v=max(Q(0),Q(n,2)-low)
  w=(Q(a)-v)*(Q(n-a)-v)
  require(0<=v<=Q(n,2) and w<=lam,'Rational profile preserves coefficient bound')
  profiles.append((a,v,w))
 bound=c+lam*(4*s-4)+r*sum(comb(n,a)*v*v for a,v,w in profiles)
 return bound,profiles
