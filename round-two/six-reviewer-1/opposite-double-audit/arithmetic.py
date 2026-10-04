"""Independent rational sparse and companion arithmetic, reused from our REVIEW10244. No target implementation or EXPECTED access."""
from fractions import Fraction as F
from math import comb
def need(ok,msg):
    if not ok:raise ValueError(msg)
class P(dict):
    def __add__(a,b):
        if not isinstance(b,P):b=const(b)
        o=P(a)
        for k,v in b.items():
            o[k]=o.get(k,F(0))+v
            if not o[k]:del o[k]
        return o
    __radd__=__add__
    def __neg__(a):return P({k:-v for k,v in a.items()})
    def __sub__(a,b):return a+-aspoly(b)
    def __rsub__(a,b):return aspoly(b)+-a
    def __mul__(a,b):
        b=aspoly(b);o=P()
        for (i,j),v in a.items():
            for (k,l),w in b.items():
                key=(i+k,j+l);o[key]=o.get(key,F(0))+v*w
        return P({k:v for k,v in o.items()if v})
    __rmul__=__mul__
    def __truediv__(a,b):return a*F(1,b)
    def __pow__(a,n):
        o=const(1)
        for _ in range(n):o=o*a
        return o
def aspoly(x):return x if isinstance(x,P)else const(x)
def const(x):return P({(0,0):F(x)})if x else P()
one=const(1);zero=P();p=P({(1,0):F(1)});t=P({(0,1):F(1)})
def matrix(n):return [[P()for _ in range(n)]for _ in range(n)]
def eye(n):
    a=matrix(n)
    for i in range(n):a[i][i]=one
    return a
def add(a,b):return [[x+y for x,y in zip(ar,br)]for ar,br in zip(a,b)]
def scale(a,v):return [[x*v for x in row]for row in a]
def multiply(a,b):
    n=len(a);o=matrix(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):o[i][j]=o[i][j]+a[i][k]*b[k][j]
    return o
def trace(a):return sum((a[i][i]for i in range(len(a))),P())
def det(a):
    n=len(a);dp={0:one}
    for mask in range(1,1<<n):
        row=mask.bit_count()-1;o=P()
        for j in range(n):
            if mask>>j&1:o=o+dp[mask^(1<<j)]*a[row][j]*(-1)**((mask>>(j+1)).bit_count())
        dp[mask]=o
    return dp[(1<<n)-1]
def adj(a):
    n=len(a);o=matrix(n)
    for i in range(n):
        for j in range(n):o[i][j]=det([[a[k][l]for l in range(n)if l!=i]for k in range(n)if k!=j])*(-1)**(i+j)
    return o
def evalm(c,a):
    out=matrix(len(a));unit=eye(len(a))
    for v in c[::-1]:out=add(multiply(out,a),scale(unit,v))
    return out
def zmul(a,b):
    o=[P()for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):o[i+j]=o[i+j]+x*y
    return o
def zdiff(c):return [c[i]*i for i in range(1,len(c))]

def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,P):return [[i,j,str(v)]for (i,j),v in sorted(x.items())]
    if isinstance(x,list):return [encode(v)for v in x]
    if isinstance(x,dict):return {k:encode(v)for k,v in x.items()}
    return x
def decode(rows):
    need(type(rows)is list and bool(rows),'nonempty coefficient list');out=P()
    for row in rows:
        need(type(row)is list and len(row)==3,'entire sparse row')
        i,j,v=row
        need(type(i)is int and type(j)is int and 0<=i<=128 and 0<=j<=32,'typed bounded exponents')
        need(type(v)is str and str(F(v))==v and F(v)!=0,'canonical nonzero coefficient')
        need((i,j)not in out,'unique coefficient')
        out[(i,j)]=F(v)
    return out
def degree(q):return (max(i for i,j in q),max(j for i,j in q))
def compose(q,x,y):
    xp=[const(1)];yp=[const(1)]
    for i in range(degree(q)[0]):xp.append(xp[-1]*x)
    for j in range(degree(q)[1]):yp.append(yp[-1]*y)
    return sum((xp[i]*yp[j]*v for(i,j),v in q.items()),P())
def evalz(c,z):
    out=P()
    for v in c[::-1]:out=out*z+v
    return out
def newton(c,kmax):
    n=len(c)-1;out=[const(n)]
    for k in range(1,kmax+1):
        out.append(-sum((c[n-j]*out[k-j]for j in range(1,min(k,n+1))),P())-(k*c[n-k]if k<=n else P()))
    return out
