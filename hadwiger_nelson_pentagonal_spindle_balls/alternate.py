"""Independent tensor field Q(zeta5,alpha,beta), alpha^2=-3,beta^2=-11."""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
Z=(F(0),)*16
ONE=(F(1),)+(F(0),)*15
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,s):return tuple(x*s for x in a)
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    out=[F(0)]*16
    for i,x in enumerate(a):
        if not x:continue
        e,k=divmod(i,4)
        for j,y in enumerate(b):
            if not y:continue
            f,l=divmod(j,4);t=k+l;v=x*y*((-3) if e&f&1 else 1)*((-11) if e&f&2 else 1);o=(e^f)*4
            if t==4:
                for h in range(4):out[o+h]-=v
            else:out[o+(t%5)]+=v
    return tuple(out)
def basis(i):return tuple(F(j==i) for j in range(16))
ROOT=basis(1);ALPHA=basis(4);BETA=basis(8)
POW=[ONE]
for _ in range(5):POW.append(mul(POW[-1],ROOT))
RHO=scale(add(ONE,ALPHA),F(1,2));ETA=scale(add(scale(ONE,5),BETA),F(1,6))
SQRT5=add(ONE,scale(add(POW[1],POW[4]),2));W=scale(add(scale(ONE,7),mul(ALPHA,SQRT5)),F(1,8))
RP=[ONE]
for _ in range(5):RP.append(mul(RP[-1],RHO))
def integer(a):
    row=[96*x for x in a]
    if any(x.denominator!=1 for x in row):raise ValueError('nonintegral denominator96')
    return tuple(int(x) for x in row)
def host():
    orbits=[[mul(mul(POW[j],ETA if h else ONE),r) for r in RP] for h in range(2) for j in range(5)]
    U=[p for row in orbits for p in row];P=sorted({integer(add(a,b)) for a,b in combinations_with_replacement(U,2)})
    return P,orbits
def dyadics():
    out=[]
    for j,h,l in product(range(1,5),range(2),range(2)):
        extra=mul(mul(POW[j],ETA if h else ONE),W if l else ONE)
        U=[mul(u,r) for u in (ONE,ETA,W,mul(ETA,W),extra) for r in RP]
        Q=[integer(Z)]+[integer(add(a,b)) for a,b in combinations_with_replacement(U,2) if a!=scale(b,-1)]
        out.append(((j,h,l),Q))
    return out
def source_map():
    z15=scale(mul(RHO,POW[2]),-1);ps=[ONE]
    for _ in range(7):ps.append(mul(ps[-1],z15))
    columns=ps+[mul(ETA,p) for p in ps]
    def convert(z,den):
        out=Z
        for a,b in zip(z[0]+z[1],columns):
            if a:out=add(out,scale(b,F(a,den)))
        return integer(out)
    return convert
def moser():return [integer(z) for z in (Z,ONE,RHO,add(ONE,RHO),ETA,mul(ETA,RHO),mul(ETA,add(ONE,RHO)))]
