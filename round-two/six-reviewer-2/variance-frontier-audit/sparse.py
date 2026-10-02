"""Sparse Q[q,k] arithmetic reused from own9508, sourcee9513705; not author code."""
from fractions import Fraction as F
from linear import need
def poly(v):return {(0,0):F(v)} if v else {}
def add(*terms):
 out={}
 for term in terms:
  for key,val in term.items():out[key]=out.get(key,F(0))+val
 return {key:val for key,val in out.items()if val}
def mul(a,b):
 out={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+v*w
 return {key:val for key,val in out.items()if val}
def scale(a,c):return mul(a,poly(c))
def power(a,n):
 out=poly(1)
 for unused in range(n):out=mul(out,a)
 return out
def evalp(a,x,y):return sum(v*x**i*y**j for(i,j),v in a.items())
def serial(a):return [[i,j,str(v)]for(i,j),v in sorted(a.items())]
def eq(a,b,why):need(a==b,why);return {'identity':why,'lhs':serial(a),'rhs':serial(b)}
x={(1,0):F(1)};y={(0,1):F(1)}
def e(q,k):return scale(add(power(q,2),mul(add(poly(13),scale(k,-6)),q),scale(power(k,2),2),scale(k,-10),poly(14)),F(1,2))
def b0(q,k):return scale(add(power(q,2),mul(add(poly(7),scale(k,-6)),q),scale(power(k,2),2),scale(k,-12),poly(8)),F(1,2))
def db(k):return add(scale(power(k,2),28),scale(k,-36),poly(17))
def pellreduce(a):
 out={}
 # Replace every p² by7u²+1 using exact polynomial division.
 for (i,j),v in a.items():
  powerpoly=power(add(scale(power(y,2),7),poly(1)),i//2)
  term=mul({(i%2,j):v},powerpoly);out=add(out,term)
 return out

