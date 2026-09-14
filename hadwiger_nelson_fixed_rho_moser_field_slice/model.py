"""Exact Q(sqrt5,sqrt33) + i sqrt3 Q(sqrt5,sqrt33) arithmetic."""
from fractions import Fraction as F
from math import isqrt,gcd,lcm
from functools import lru_cache
from itertools import combinations

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,s):return tuple(x*s for x in a)
def mul(a,b):
    n=len(a)
    if n==1:return (a[0]*b[0],)
    h=n//2;d={2:5,4:33,8:-3}[n]
    x,y=a[:h],a[h:];u,v=b[:h],b[h:]
    return add(mul(x,u),scale(mul(y,v),d))+add(mul(x,v),mul(y,u))
def inv(a):
    if len(a)==1:
        if not a[0]:raise ZeroDivisionError
        return (1/F(a[0]),)
    h=len(a)//2;d={2:5,4:33,8:-3}[len(a)];x,y=a[:h],a[h:]
    z=inv(sub(mul(x,x),scale(mul(y,y),d)))
    return mul(x,z)+neg(mul(y,z))
def div(a,b):return mul(a,inv(b))
def conj(a):return a[:4]+neg(a[4:])
def norm(a):return add(mul(a[:4],a[:4]),scale(mul(a[4:],a[4:]),3))
def z(a=0):return (F(a),F(0),F(0),F(0))
def c(a=0):return z(a)+z()

@lru_cache(None)
def square_root(a):
    """A square root in the totally real tower, or None; exhaustive recursion."""
    if not any(a):return a
    n=len(a)
    if n==1:
        q=F(a[0])
        if q<0:return None
        p,r=isqrt(q.numerator),isqrt(q.denominator)
        return (F(p,r),) if p*p==q.numerator and r*r==q.denominator else None
    h=n//2;d={2:5,4:33}[n];A,B=a[:h],a[h:];zero=(F(0),)*h
    if not any(B):
        x=square_root(A)
        if x is not None:return x+zero
        y=square_root(scale(A,F(1,d)))
        return zero+y if y is not None else None
    t=square_root(sub(mul(A,A),scale(mul(B,B),d)))
    if t is None:return None
    for u in (t,neg(t)):
        x=square_root(scale(add(A,u),F(1,2)))
        if x is not None and any(x):
            y=div(B,scale(x,2));r=x+y
            if mul(r,r)==a:return r
    return None

def construction():
    one=c(1);omega=scale(add(one,z()+z(1)),F(1,2))
    eta=z(F(5,6))+(F(0),F(0),F(1,18),F(0))
    M=[c(),one,omega,add(one,omega),eta,mul(eta,omega),mul(eta,add(one,omega))]
    rho=z(F(7,8))+(F(0),F(1,8),F(0),F(0))
    if norm(rho)!=z(1):raise ValueError('rho not unit')
    B=sorted(set(add(a,mul(rho,b)) for a in M for b in M))
    den=lcm(*(x.denominator for p in M+B for x in p))
    Mi=[tuple(int(x*den)for x in p)for p in M]
    Bi=[tuple(int(x*den)for x in p)for p in B]
    return den,Mi,Bi

def primitive(row):
    vals=sum(row,());g=0
    for x in vals:g=gcd(g,x)
    if not g:return None
    if next(x for x in vals if x)<0:g=-g
    return tuple(tuple(x//g for x in a)for a in row)

def encode(p):return [[F(x).numerator,F(x).denominator]for x in p]
def decode(p):return tuple(F(a,b)for a,b in p)

def inventory(progress=None):
    den,M,B=construction();addresses=[(a,b)for a in B for b in M]
    generic=[];lines={};collisions={};pairs=0
    for i,j in combinations(range(len(addresses)),2):
        a=sub(addresses[i][0],addresses[j][0]);b=sub(addresses[i][1],addresses[j][1]);pairs+=1
        na,nb=norm(a),norm(b)
        if not any(a) or not any(b):
            if add(na,nb)==(den*den,0,0,0):generic.append((i,j))
            continue
        cc=mul(conj(a),b);S=sub(add(na,nb),(den*den,0,0,0))
        key=primitive((scale(cc[:4],2),scale(cc[4:],-6),S))
        if key not in lines:lines[key]={'a':a,'b':b,'c':cc,'S':S,'na':na,'nb':nb,'pairs':[]}
        lines[key]['pairs'].append((i,j))
        if na==nb:
            phase=neg(div(a,b));collisions.setdefault(phase,[]).append((i,j))
    phases={p:{'edges':set(),'collisions':ps}for p,ps in collisions.items()}
    nr=0
    for count,(key,r)in enumerate(sorted(lines.items())):
        nc=mul(r['na'],r['nb']);delta=sub(scale(nc,4),mul(r['S'],r['S']))
        root=square_root(scale(delta,F(1,3)))
        if root is not None:
            nr+=1;ci=conj(r['c']);ni=scale(inv(nc),F(1,2));factor=mul(ci,ni+z())
            for s in set([root,neg(root)]):
                v=mul(neg(r['S'])+s,factor)
                if norm(v)!=z(1):raise ValueError('bad unit root')
                if any(add(add(scale(mul(v[:4],r['c'][:4]),2),scale(mul(v[4:],r['c'][4:]),-6)),r['S'])):raise ValueError('bad contact root')
                phases.setdefault(v,{'edges':set(),'collisions':[]})['edges'].update(r['pairs'])
        if progress and count%1000==0:progress({'lines_done':count,'lines':len(lines),'phases':len(phases),'sqrt_cache':square_root.cache_info()._asdict()})
    return den,M,B,addresses,generic,lines,phases,{'pairs':pairs,'line_count':len(lines),'lines_with_K_roots':nr,'phases':len(phases),'collision_phases':len(collisions),'generic_edges':len(generic),'B_points':len(B),'M_points':len(M)}

def merged_graph(n,edges,collisions):
    parent=list(range(n))
    def find(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for a,b in collisions:
        x,y=find(a),find(b)
        if x!=y:parent[max(x,y)]=min(x,y)
    roots=sorted({find(v)for v in range(n)});idx={r:i for i,r in enumerate(roots)};labels=[idx[find(v)]for v in range(n)]
    E=sorted({tuple(sorted((labels[a],labels[b])))for a,b in edges})
    if any(a==b for a,b in E):raise ValueError('unit collision')
    return labels,E
