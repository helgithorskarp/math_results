"""Four-variable adaptation of the credited9005 exact polynomial engine.

Multiplication uses bounded integer Kronecker packing; every cancellation
is verified by exact polynomial division. The supplied small factors are
only optimization hints. Full determinants use signed permutation sums.
No CAS, floating point, interpolation, or assertion-dependent checks.
"""
from fractions import Fraction as F
from itertools import permutations
from math import gcd,lcm,prod
from pathlib import Path
import argparse,heapq,json,resource,signal,time

DIM=4;ZERO=(0,)*DIM;LIMIT=30000
def require(p,msg):
    if not p:raise ValueError(msg)
def alarm(signum,frame):raise TimeoutError('stage60s guard reached')
signal.signal(signal.SIGALRM,alarm)

class P:
    def __init__(self,a=0,den=1):
        if isinstance(a,P):self.a,self.den=a.a,a.den;return
        if not isinstance(a,dict):
            f=F(a);a={ZERO:f.numerator} if f else {};den=f.denominator
        a={k:v for k,v in a.items() if v}
        require(all(type(v) is int for v in a.values()) and den>0,'integer polynomial representation')
        require(all(type(k) is tuple and len(k)==DIM and all(type(e) is int and e>=0 for e in k) for k in a),'four-variable exponent representation')
        g=den
        for v in a.values():g=gcd(g,abs(v))
        self.a={k:v//g for k,v in a.items()};self.den=den//g
        require(len(self.a)<=LIMIT,'polynomial term guard')
    @staticmethod
    def fractions(a):
        d=1
        for v in a.values():d=lcm(d,F(v).denominator)
        return P({k:int(F(v)*d) for k,v in a.items()},d)
    @staticmethod
    def decode(a):return P.fractions({tuple(k):F(v) for k,v in a})
    def __bool__(self):return bool(self.a)
    def __eq__(self,b):
        b=P(b);return self.a==b.a and self.den==b.den
    def __neg__(self):return P({k:-v for k,v in self.a.items()},self.den)
    def __add__(self,b):
        b=P(b);d=lcm(self.den,b.den);a={k:v*(d//self.den) for k,v in self.a.items()}
        for k,v in b.a.items():a[k]=a.get(k,0)+v*(d//b.den)
        return P(a,d)
    __radd__=__add__
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        b=P(b)
        if not self or not b:return P()
        if len(self.a)*len(b.a)<=256:
            a={}
            for i,x in self.a.items():
                for j,y in b.a.items():
                    k=tuple(i[z]+j[z] for z in range(DIM));a[k]=a.get(k,0)+x*y
            return P(a,self.den*b.den)
        bounds=[max(k[z] for k in self.a)+max(k[z] for k in b.a) for z in range(DIM)]
        radix=max(bounds)+1
        bound=sum(map(abs,self.a.values()))*sum(map(abs,b.a.values()))
        width=((2*bound).bit_length()+7)//8;beta=1<<(8*width)
        require(beta>2*bound,'balanced coefficient bound')
        def pack(a):
            slots={sum(k[z]*radix**z for z in range(DIM)):v for k,v in a.items()}
            size=(max(slots)+1)*width
            require(size<=32*1024*1024,'packing byte guard')
            pos=bytearray(size);neg=bytearray(size)
            for k,v in slots.items():
                target=pos if v>0 else neg;target[k*width:(k+1)*width]=abs(v).to_bytes(width,'little')
            return int.from_bytes(pos,'little')-int.from_bytes(neg,'little')
        value=pack(self.a)*pack(b.a);sgn=1 if value>=0 else -1;value=abs(value)
        data=value.to_bytes((value.bit_length()+7)//8,'little');a={};carry=0
        count=(len(data)+width-1)//width
        for k in range(count+1):
            digit=int.from_bytes(data[k*width:(k+1)*width],'little')+carry
            if digit>=beta//2:digit-=beta;carry=1
            else:carry=0
            if digit:
                ex=tuple((k//radix**z)%radix if z<DIM-1 else k//radix**z for z in range(DIM))
                require(all(ex[z]<=bounds[z] for z in range(DIM)),'packed exponent bound')
                a[ex]=sgn*digit
        require(carry==0,'balanced decode completion')
        return P(a,self.den*b.den)
    __rmul__=__mul__
    def __pow__(self,n):
        require(type(n) is int and n>=0,'polynomial exponent');a=P(1);b=self
        while n:
            if n%2:a=a*b
            n//=2
            if n:b=b*b
        return a
    def value_mod(self,point,prime):
        # The coefficient denominator is immaterial for rejecting divisibility.
        return sum(v*prod(pow(point[z],k[z],prime) for z in range(DIM)) for k,v in self.a.items())%prime
    def exact_div(self,b):
        b=P(b);require(bool(b),'nonzero polynomial divisor')
        if not self:return P()
        lead=max(b.a);lc=b.a[lead];rem={k:F(v) for k,v in self.a.items()};quot={}
        heap=[tuple(-x for x in k) for k in rem];heapq.heapify(heap)
        while rem:
            while heap and tuple(-x for x in heap[0]) not in rem:heapq.heappop(heap)
            require(bool(heap),'division heap exhaustion')
            k=tuple(-x for x in heapq.heappop(heap));ex=tuple(k[z]-lead[z] for z in range(DIM))
            if min(ex)<0:return None
            v=rem[k]/lc;quot[ex]=quot.get(ex,F(0))+v
            for m,c in b.a.items():
                e=tuple(m[z]+ex[z] for z in range(DIM));new=rem.get(e,F(0))-v*c
                if new:
                    if e not in rem:heapq.heappush(heap,tuple(-x for x in e))
                    rem[e]=new
                else:rem.pop(e,None)
        return P.fractions({k:v*F(b.den,self.den) for k,v in quot.items()})
    def positive(self):return self.a.get(ZERO,0)>0 and all(v>=0 for v in self.a.values())
    def degree(self):return max(map(sum,self.a),default=-1)
    def constant(self):return F(self.a.get(ZERO,0),self.den) if set(self.a)<=set([ZERO]) else None
    def fingerprint(self):
        from hashlib import sha256
        return sha256(json.dumps({'den':self.den,'terms':sorted((list(k),str(v)) for k,v in self.a.items())},separators=(',',':')).encode()).hexdigest()

ATOMS={};PROBES={};DEN_CACHE={}
def atom(p):
    # Primitive integer normalization with positive lexicographic leader.
    require(bool(p),'nonzero factor');content=0
    for v in p.a.values():content=gcd(content,abs(v))
    if p.a[max(p.a)]<0:content=-content
    key=tuple(sorted((k,v//content) for k,v in p.a.items()))
    if key not in ATOMS:
        factor=P(dict(key));ATOMS[key]=factor;probes=[];prime=1009
        for z in sorted(range(DIM),key=lambda j:max(k[j] for k in factor.a)):
            if not max(k[z] for k in factor.a):continue
            for fix in [(1,2,3),(3,5,7),(7,11,13)]:
                point=[0]*DIM;others=[j for j in range(DIM) if j!=z]
                for j,x in zip(others,fix):point[j]=x
                for x in range(prime):
                    point[z]=x
                    if factor.value_mod(point,prime)==0:probes.append((tuple(point),prime));break
                if len(probes)>=2:break
            if len(probes)>=2:break
        PROBES[key]=probes
    return key,F(content,p.den)
def div_if_possible(p,key):
    if any(p.value_mod(point,prime)!=0 for point,prime in PROBES[key]):return None
    return p.exact_div(ATOMS[key])
def denominator(d):
    key=tuple(sorted(d.items()))
    if key not in DEN_CACHE:
        p=P(1)
        for a,e in key:p=p*ATOMS[a]**e
        DEN_CACHE[key]=p
    return DEN_CACHE[key]
def factor(p):
    require(bool(p),'rational division by zero');d={}
    for key in tuple(ATOMS):
        while p.constant() is None:
            out=div_if_possible(p,key)
            if out is None:break
            d[key]=d.get(key,0)+1;p=out
    if p.constant() is None:
        key,unit=atom(p);d[key]=d.get(key,0)+1
    else:unit=p.constant()
    return d,unit

class R:
    def __init__(self,num=0,den=None):
        if isinstance(num,R) and den is None:self.num,self.den=num.num,num.den;return
        self.num=P(num);self.den=dict(den or {})
        if not self.num:self.den={};return
        for key in tuple(self.den):
            while self.den[key]:
                out=div_if_possible(self.num,key)
                if out is None:break
                self.num=out;self.den[key]-=1
            if not self.den[key]:del self.den[key]
    def __add__(self,b):
        b=R(b);den=dict(self.den)
        for k,e in b.den.items():den[k]=max(den.get(k,0),e)
        left={k:e-self.den.get(k,0) for k,e in den.items() if e>self.den.get(k,0)}
        right={k:e-b.den.get(k,0) for k,e in den.items() if e>b.den.get(k,0)}
        return R(self.num*denominator(left)+b.num*denominator(right),den)
    __radd__=__add__
    def __neg__(self):return R(-self.num,self.den)
    def __sub__(self,b):return self+-R(b)
    def __rsub__(self,b):return R(b)+-self
    def __mul__(self,b):
        b=R(b);left=self.num;right=b.num
        ld=dict(self.den);rd=dict(b.den)
        # Cancel across the product BEFORE expanding its numerator.
        # Each removal is separately justified by exact polynomial division.
        for key in tuple(rd):
            while rd[key]:
                out=div_if_possible(left,key)
                if out is None:break
                left=out;rd[key]-=1
            if not rd[key]:del rd[key]
        for key in tuple(ld):
            while ld[key]:
                out=div_if_possible(right,key)
                if out is None:break
                right=out;ld[key]-=1
            if not ld[key]:del ld[key]
        d=ld
        for k,e in rd.items():d[k]=d.get(k,0)+e
        return R(left*right,d)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=R(b);d,unit=factor(b.num)
        return self*R(denominator(b.den)*P(1/unit),d)
    def __rtruediv__(self,b):return R(b)/self
    def __pow__(self,n):
        require(type(n) is int and n>=0,'rational exponent');return R(self.num**n,{k:e*n for k,e in self.den.items()})

def det(a):
    result=R()
    for order in permutations(range(len(a))):
        sign=(-1)**sum(order[i]>order[j] for i in range(len(a)) for j in range(i+1,len(a)))
        term=R(sign)
        for i,j in enumerate(order):term=term*a[i][j]
        result=result+term
    return result
def reference_mul(a,b):
    out={}
    for i,x in a.a.items():
        for j,y in b.a.items():
            k=tuple(i[z]+j[z] for z in range(DIM));out[k]=out.get(k,0)+x*y
    return P(out,a.den*b.den)
def multiplication_controls():
    import random
    rng=random.Random(20261001)
    for size in [2,18,40]:
        for repeat in range(6):
            a=P({tuple(rng.randrange(7) for _ in range(DIM)):rng.randrange(-(1<<70),1<<70) for _ in range(size)},7)
            b=P({tuple(rng.randrange(7) for _ in range(DIM)):rng.randrange(-10000,10001) for _ in range(size)},11)
            require(a*b==reference_mul(a,b),'packed/reference multiplication')
    require(P()*P(1)==P() and P(-1)*P(-1)==P(1),'zero and negative controls')
