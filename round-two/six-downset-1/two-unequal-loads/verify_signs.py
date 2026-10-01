"""Independent standard-library QQ[Q,T,B] certificate reconstruction.

Multiplication uses bounded integer Kronecker packing; every cancellation
is verified by exact polynomial division. The supplied small factors are
only optimization hints. Full determinants use signed permutation sums.
No CAS, floating point, interpolation, or assertion-dependent checks.
"""
from fractions import Fraction as F
from itertools import permutations
from math import gcd,lcm
from pathlib import Path
import argparse,heapq,json,resource,signal,time

ZERO=(0,0,0);LIMIT=30000
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
                    k=tuple(i[z]+j[z] for z in range(3));a[k]=a.get(k,0)+x*y
            return P(a,self.den*b.den)
        bounds=[max(k[z] for k in self.a)+max(k[z] for k in b.a) for z in range(3)]
        radix=max(bounds)+1
        bound=sum(map(abs,self.a.values()))*sum(map(abs,b.a.values()))
        width=((2*bound).bit_length()+7)//8;beta=1<<(8*width)
        require(beta>2*bound,'balanced coefficient bound')
        def pack(a):
            slots={k[0]+radix*k[1]+radix*radix*k[2]:v for k,v in a.items()}
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
                ex=(k%radix,(k//radix)%radix,k//(radix*radix))
                require(all(ex[z]<=bounds[z] for z in range(3)),'packed exponent bound')
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
        return sum(v*pow(point[0],k[0],prime)*pow(point[1],k[1],prime)*pow(point[2],k[2],prime) for k,v in self.a.items())%prime
    def exact_div(self,b):
        b=P(b);require(bool(b),'nonzero polynomial divisor')
        if not self:return P()
        lead=max(b.a);lc=b.a[lead];rem={k:F(v) for k,v in self.a.items()};quot={}
        heap=[tuple(-x for x in k) for k in rem];heapq.heapify(heap)
        while rem:
            while heap and tuple(-x for x in heap[0]) not in rem:heapq.heappop(heap)
            require(bool(heap),'division heap exhaustion')
            k=tuple(-x for x in heapq.heappop(heap));ex=tuple(k[z]-lead[z] for z in range(3))
            if min(ex)<0:return None
            v=rem[k]/lc;quot[ex]=quot.get(ex,F(0))+v
            for m,c in b.a.items():
                e=tuple(m[z]+ex[z] for z in range(3));new=rem.get(e,F(0))-v*c
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
        for z in sorted(range(3),key=lambda j:max(k[j] for k in factor.a)):
            if not max(k[z] for k in factor.a):continue
            for fix in [(1,2),(3,5),(7,11)]:
                point=[0,0,0];others=[j for j in range(3) if j!=z]
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
        b=R(b);d=dict(self.den)
        for k,e in b.den.items():d[k]=d.get(k,0)+e
        return R(self.num*b.num,d)
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
            k=tuple(i[z]+j[z] for z in range(3));out[k]=out.get(k,0)+x*y
    return P(out,a.den*b.den)
def multiplication_controls():
    import random
    rng=random.Random(20261001)
    for size in [2,18,40]:
        for repeat in range(6):
            a=P({tuple(rng.randrange(7) for _ in range(3)):rng.randrange(-(1<<70),1<<70) for _ in range(size)},7)
            b=P({tuple(rng.randrange(7) for _ in range(3)):rng.randrange(-10000,10001) for _ in range(size)},11)
            require(a*b==reference_mul(a,b),'packed/reference multiplication')
    require(P()*P(1)==P() and P(-1)*P(-1)==P(1),'zero and negative controls')

def formulas():
    q=R(P({(1,0,0):1}))+2;t=R(P({(0,1,0):1}))+1;D=t+R(P({(0,0,1):1}))+1
    M=D+t;w=q+D-1;h=2*q+2*M-1
    ch=M*(w-D-M-1)/((M+1)*((M-1)*w-1+D))
    cl=M*(w-t-M-1)/((M+1)*((M-1)*w-1+t))
    normK=w+M*(q+D)-D**2-t**2-2*M
    ky=t/M*(ch*(q-1)-cl*(w-t))
    y2=t**2/M**2*(ch**2*q/D+cl**2*(q+D-t)/t)
    eh=w-normK/(M+1)**2-y2-ch**2*(q+D)*(1-1/D)+2*ky/(M+1)
    el=w-normK/(M+1)**2-D**2/t**2*y2-cl**2*(q+D)*(1-1/t)-2*D/t*ky/(M+1)
    totaleta=D*eh+t*el
    zh=M/(M-2)*(eh-totaleta/(M*(M-1)));zl=M/(M-2)*(el-totaleta/(M*(M-1)))
    signs={'zeta_heavy':zh,'zeta_light':zl,'heavy_within_slack':1-ch**2*(q+D)/(h-q-D)-zh/h,'light_within_slack':1-cl**2*(q+D)/(h-q-D)-zl/h}
    alpha=t*(t*zh+D*zl)/(D*M**2);d0=(h-q-1)*(h-D)-D*(q-1)
    metric=[[R() for _ in range(6)] for _ in range(6)]
    metric[0][0]=(q-1)*(h-D)/d0;metric[0][1]=metric[1][0]=D*(q-1)/d0;metric[1][1]=D*(h-q-1)/d0
    for i in [2,3]:
        for j in [2,3]:metric[i][j]=D*(q*int(i==j)-1)/(h-2*D)
    metric[4][4]=(q+D)*(1/t-1/D)/h;metric[5][5]=alpha/h
    vectors=[[R(),R(1),R(1),R(),R(),R()], [R(),1/D,R(),1/D,R(1),R()], [R(1),t/D,R(1),t/D,t,R()], [R(),t*(ch-cl)/(M*D),t*ch/(M*D),-t*cl/(M*D),-t*cl/M,R(1)]]
    inverse_weights=[D,1/t,M+1,t/(D*M)]
    budget=[[inverse_weights[i]*int(i==j)-sum((vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)),R()) for j in range(4)] for i in range(4)]
    return signs,budget,{'ch':ch,'cl':cl,'eta_heavy':eh,'eta_light':el}

FACTOR_HINTS=[[[[0,0,0],"1"],[[0,1,0],"1"]],[[[0,0,0],"9"],[[0,0,1],"2"],[[0,1,0],"4"],[[1,0,0],"2"]],[[[0,0,0],"5"],[[0,1,0],"2"],[[1,0,0],"2"]],[[[0,0,0],"40"],[[0,0,1],"19"],[[0,0,2],"2"],[[0,1,0],"45"],[[0,1,1],"10"],[[0,2,0],"12"],[[1,0,0],"17"],[[1,0,1],"4"],[[1,1,0],"10"],[[2,0,0],"2"]],[[[0,0,0],"2"],[[0,0,1],"1"],[[0,1,0],"1"]],[[[0,0,0],"1"],[[0,0,1],"1"],[[0,1,0],"2"]],[[[0,0,0],"2"],[[0,0,1],"1"],[[0,1,0],"2"]],[[[0,0,0],"3"],[[0,0,1],"1"],[[0,1,0],"2"]],[[[0,0,0],"4"],[[0,0,1],"1"],[[0,1,0],"2"]],[[[0,0,0],"6"],[[0,0,1],"5"],[[0,0,2],"1"],[[0,1,0],"9"],[[0,1,1],"3"],[[0,2,0],"2"],[[1,0,0],"2"],[[1,0,1],"1"],[[1,1,0],"2"]],[[[0,0,0],"7"],[[0,0,1],"6"],[[0,0,2],"1"],[[0,1,0],"9"],[[0,1,1],"3"],[[0,2,0],"2"],[[1,0,0],"2"],[[1,0,1],"1"],[[1,1,0],"2"]]]

def stable(record):
    return {k:v for k,v in record.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic()
    signal.alarm(60);multiplication_controls()
    for hint in FACTOR_HINTS:atom(P.decode(hint))
    signs,budget,scalars=formulas();signal.alarm(0)
    for k in range(1,5):
        signal.alarm(60);signs['symmetric_minor_'+str(k)]=det([row[:k] for row in budget[:k]]);signal.alarm(0)
    rows=[]
    for name,value in signs.items():
        den=denominator(value.den)
        require(value.num.positive() and den.positive(),'strict positive polynomial certificate '+name)
        rows.append({'name':name,'numerator_terms':len(value.num.a),'denominator_terms':len(den.a),'numerator_degree':value.num.degree(),'denominator_degree':den.degree(),'numerator_constant':str(F(value.num.a[ZERO],value.num.den)),'denominator_constant':str(F(den.a[ZERO],den.den)),'numerator_sha256':value.num.fingerprint(),'denominator_sha256':den.fingerprint(),'positive_constants_and_nonnegative_coefficients':True})
    final=signs['symmetric_minor_4'].num
    changed=final+1
    negative=dict(final.a);negative[ZERO]=-1
    require(changed.fingerprint()!=final.fingerprint(),'changed-coefficient fingerprint rejection')
    require(not P(negative,final.den).positive(),'negative-coefficient rejection')
    out={'agent':'six-downset-1','role':'researcher','domain':'QQ[Q,T,B] and its fraction field','substitution':'q=Q+2,t=T+1,D=t+B+1; Q,T,B>=0','positive_functions':rows,'positive_rational_functions':len(rows),'determinant_permutations':[1,2,6,24],'multiplication_controls':18,'changed_coefficient_rejected':True,'negative_coefficient_rejected':True,'CAS_imports':False,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:
        expected=json.loads(args.expected.read_text())['signs']
        require(stable(out)==stable(expected),'frozen exact coefficient certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
