"""Author six-sendov-1, researcher: generic exact four-variable arithmetic.

Copied with attribution from 4c04ae6fa05920f3f749ffec6ecb1f8aa3ad219a,
radial sixfold source. Earlier transform provenance is in LITERATURE.md.
No theorem or numerical signs are imported.
"""
from fractions import Fraction as F
from math import comb,lcm,prod,gcd
from collections import defaultdict

def bernstein(p,degrees=None):
    if degrees is None:
        degrees=tuple(max(e[i] for e in p) for i in range(4))
    shape=tuple(d+1 for d in degrees)
    stride=tuple(prod(shape[i+1:]) for i in range(4))
    initial=lcm(*(v.denominator for v in p.values()))
    data=[0]*prod(shape)
    for e,v in p.items():data[sum(e[i]*stride[i] for i in range(4))]=int(v*initial)
    denominator=initial
    for axis,n in enumerate(degrees):
        norm=lcm(*(comb(n,k) for k in range(n+1)))
        weights=[[comb(i,k)*(norm//comb(n,k)) for k in range(i+1)] for i in range(n+1)]
        out=[0]*len(data);step=stride[axis];block=step*(n+1)
        for outer in range(0,len(data),block):
            for inner in range(step):
                offset=outer+inner
                for i,w in enumerate(weights):
                    out[offset+i*step]=sum(data[offset+k*step]*v for k,v in enumerate(w))
        data=out;denominator*=norm
    return data,denominator,degrees

from kernel import require

Z=(0,)*4;ONE={Z:1}
def add(*polys):
 out=defaultdict(int)
 for p in polys:
  for e,v in p.items():out[e]+=v
 return {e:v for e,v in out.items() if v}
def scale(p,k):return {e:v*k for e,v in p.items() if v*k}
def mul(p,q):
 out=defaultdict(int)
 for e,v in p.items():
  for f,w in q.items():out[tuple(e[j]+f[j] for j in range(4))]+=v*w
 return {e:v for e,v in out.items() if v}
def power(p,n):
 out=ONE
 while n:
  if n&1:out=mul(out,p)
  n//=2
  if n:p=mul(p,p)
 return out
def var(j):
 e=list(Z);e[j]=1;return {tuple(e):1}
def primitive(p):
 d=0
 for v in p.values():d=gcd(d,v)
 require(d>0,'Zero input kernel')
 return ({e:v//d for e,v in p.items()},d)
def horner(p,axis,num,den):
 n=max(e[axis] for e in p);groups=[{} for _ in range(n+1)]
 for e,v in p.items():
  f=list(e);f[axis]=0;groups[e[axis]][tuple(f)]=v
 dp=[power(den,j) for j in range(n+1)]
 out=groups[-1]
 for j in range(n-1,-1,-1):out=add(mul(out,num),mul(groups[j],dp[n-j]))
 return out,n

def inverse_identity(values,den,degrees,p):
 shape=[d+1 for d in degrees];stride=[prod(shape[j+1:]) for j in range(4)];data=values.copy()
 for axis,n in enumerate(degrees):
  step=stride[axis];block=step*(n+1);out=[0]*len(data)
  for outer in range(0,len(data),block):
   for inner in range(step):
    off=outer+inner
    for k in range(n+1):out[off+k*step]=comb(n,k)*sum((-1)**(k-j)*comb(k,j)*data[off+j*step] for j in range(k+1))
  data=out
 seen=0
 for k,v in enumerate(data):
  if v:
   e=tuple((k//stride[j])%shape[j] for j in range(4));require(v==p.get(e,0)*den,'Entire integer inverse identity differs');seen+=1
 require(seen==len(p),'Integer inverse omitted a polynomial term')

def cube(raw,chart,progress=None):
 d=lcm(*(v.denominator for v in raw.values()))
 p={e:int(v*d) for e,v in raw.items()};p,g=primitive(p);factor=F(d,g)
 b,r,v,w=[var(j) for j in range(4)];eps=add(ONE,scale(b,-1));den=add(ONE,b);s=add(scale(ONE,4),scale(r,-3))
 X=add(scale(r,3),scale(mul(eps,v),-4))
 p,px=horner(p,2,X,scale(ONE,3));p,g=primitive(p);factor*=F(3**px,g)
 if progress:progress('phase loss',p)
 T=add(s,scale(mul(eps,mul(add(ONE,scale(v,-1)),w)),-4))
 p,pt=horner(p,3,T,ONE);p,g=primitive(p);factor/=g
 if progress:progress('light loss',p)
 if chart=='nearer':num=add(scale(den,3),mul(b,r));dd=scale(den,3);c=3
 elif chart=='farther':num=add(den,scale(mul(b,r),-1));dd=den;c=1
 else:raise ValueError(chart)
 p,pr=horner(p,1,num,dd);p,g=primitive(p);factor*=F(c**pr,g)
 if progress:progress('radius',p)
 p,pb=horner(p,0,add(scale(ONE,7),b),scale(ONE,8));p,g=primitive(p);factor*=F(8**pb,g)
 if progress:progress('b interval',p)
 return p,factor,pr


def affine_cell(p,axis,low,high):
    out=defaultdict(F)
    for e,v in p.items():
        for j in range(e[axis]+1):
            f=list(e);f[axis]=j
            out[tuple(f)]+=v*comb(e[axis],j)*low**(e[axis]-j)*(high-low)**j
    return {e:v for e,v in out.items() if v}

def affine_cell_integer(p,axis,low,high):
    """The full affine power transform with one shared integer denominator.

    For low=P/Q, high-low=R/Q, an exponent e contributes
    binom(e,j)*P**(e-j)*R**j*Q**(n-e) at index j. Division by Q**n
    is deferred until all integer sums finish. The Fraction reference
    above is retained and compared on a complete nontrivial margin cell.
    """
    low,high=F(low),F(high)
    if not low<high:raise ValueError('Invalid affine interval')
    n=max(e[axis] for e in p)
    base=lcm(*(v.denominator for v in p.values()))
    span=high-low;Q=lcm(low.denominator,span.denominator)
    P=int(low*Q);R=int(span*Q)
    weights=[[comb(e,j)*P**(e-j)*R**j*Q**(n-e) for j in range(e+1)] for e in range(n+1)]
    out=defaultdict(int)
    for e,v in p.items():
        coeff=v.numerator*(base//v.denominator)
        for j,w in enumerate(weights[e[axis]]):
            if w:
                f=list(e);f[axis]=j;out[tuple(f)]+=coeff*w
    den=base*Q**n
    return {e:F(v,den) for e,v in out.items() if v}
