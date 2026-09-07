"""Generate dyadic enclosures, using Machin's formula and integer Taylor bounds."""
import argparse
from fractions import Fraction
Q=1<<160
S=1<<48
def mul(a,b):
 p=[x*y for x in a for y in b]
 return min(p)//Q,-(-max(p)//Q)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def div(a,d):return a[0]//d,-(-a[1]//d)
def atan_bounds(d,count):
 v=sum((Fraction((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(count)),Fraction())
 t=Fraction((-1)**count,(2*count+1)*d**(2*count+1))
 return min(v,v+t),max(v,v+t)
a,b=atan_bounds(5,40);c,d=atan_bounds(239,12)
p=(16*a-4*d,16*b-4*c)
PI=(int(p[0]*Q),-(-p[1].numerator*Q//p[1].denominator))
def trig(m,n):
 x=(PI[0]*m//n,-(-PI[1]*m//n));xx=mul(x,x)
 st=x;ct=(Q,Q);ss=st;cc=ct
 for j in range(1,20):
  st=neg(div(mul(st,xx),(2*j)*(2*j+1)))
  ct=neg(div(mul(ct,xx),(2*j-1)*(2*j)))
  ss=add(ss,st);cc=add(cc,ct)
 # For |x|<2, the first omitted term is <2^-110 for both series.
 err=1<<50
 def down(z):return ((z[0]-err)*S//Q,-(-(z[1]+err)*S//Q))
 return down(ss),down(cc)
def generate(maxn):
 print(maxn,S)
 for n in range(3,maxn+1):
  vals={m:trig(m,n) for m in range(n//2+1)}
  for m in range(2*n):
   a=m;sy=1;cx=1
   if a>n:a=2*n-a;sy=-1
   if 2*a>n:a=n-a;cx=-1
   s,c=vals[a]
   if m in (0,n):s=(0,0)
   if 2*m in (n,3*n):c=(0,0)
   if m==0:c=(S,S)
   if m==n:c=(-S,-S);cx=1
   if sy<0:s=neg(s)
   if cx<0:c=neg(c)
   print(n,m,*s,*c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=254);a=p.parse_args();generate(a.max_n)
