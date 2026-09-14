"""Q(zeta_15,eta), Phi15(z)=0, 3eta^2-5eta+3=0; integer point coefficients."""
import json,hashlib
from itertools import combinations_with_replacement,combinations
from pathlib import Path
Z=(0,)*8;ONE=(1,)+(0,)*7
# Phi15=x^8-x^7+x^5-x^4+x^3-x+1.
PHI=(1,-1,0,1,-1,1,0,-1,1)
def require(c,msg):
    if not c:raise ValueError(msg)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,s):return tuple(s*x for x in a)
def mul(a,b):
    c=[0]*15
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    for k in range(14,7,-1):
        x=c[k]
        if x:
            for j in range(8):c[k-8+j]-=x*PHI[j]
    return tuple(c[:8])
ROOT=(0,1,0,0,0,0,0,0)
POW=[ONE]
for _ in range(15):POW.append(mul(POW[-1],ROOT))
require(POW[15]==ONE and all(POW[d]!=ONE for d in (1,3,5)),'root order')
def conj(a):
    out=Z
    for i,x in enumerate(a):out=add(out,scale(POW[(-i)%15],x))
    return out
def pa(a,b):return (add(a[0],b[0]),add(a[1],b[1]))
def ps(a,b):return (sub(a[0],b[0]),sub(a[1],b[1]))
def pneg(a):return (neg(a[0]),neg(a[1]))
def norm3(p):
    x,y=p;xb=mul(x,conj(y));yb=mul(y,conj(x))
    return (add(scale(add(mul(x,conj(x)),mul(y,conj(y))),3),scale(xb,5)),scale(sub(yb,xb),3))
def unit(p):return norm3(p)==(scale(ONE,3),Z)
def make():
    rho=add(ONE,POW[5]);r=[ONE]
    for _ in range(6):r.append(mul(r[-1],rho))
    require(r[6]==ONE,'rho order')
    orbits=[]
    for h in range(2):
        for j in range(5):
            orbit=[]
            for k in range(6):
                a=mul(POW[3*j],r[k]);orbit.append((Z,a) if h else (a,Z))
            orbits.append(orbit)
    U=sorted({p for row in orbits for p in row});require(len(U)==60 and all(unit(p) for p in U),'unit directions')
    P=sorted({pa(a,b) for a,b in combinations_with_replacement(U,2)})
    require(len(P)==1801,'host point count');where={p:i for i,p in enumerate(P)}
    families=[]
    for orb in combinations(range(10),5):
        us=[p for i in orb for p in orbits[i]];ids=sorted({where[pa(a,b)] for a,b in combinations_with_replacement(us,2)})
        require(len(ids)==451,'target point count');families.append((orb,ids))
    return P,orbits,families
def isprime(n):return n>=2 and all(n%d for d in range(2,__import__('math').isqrt(n)+1))
def projection(p,r,t):
    require(isprime(p) and pow(r,15,p)==1 and all(pow(r,d,p)!=1 for d in (1,3,5)) and (3*t*t-5*t+3)%p==0,'bad ring projection')
    def ev(a):return sum(x*pow(r,i,p) for i,x in enumerate(a))%p
    def point(a):return (ev(a[0])+t*ev(a[1]))%p
    def bar(a):return (ev(conj(a[0]))+pow(t,-1,p)*ev(conj(a[1])))%p
    return point,bar
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
