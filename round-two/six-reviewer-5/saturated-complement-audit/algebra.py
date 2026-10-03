"""Fresh exact polynomial and symmetric-elimination arithmetic; no producer imports."""
from fractions import Fraction as F

def require(ok, why):
    if not ok:
        raise ValueError(why)

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    out=[0]*max(len(a),len(b))
    for i,c in enumerate(a):out[i]+=c
    for i,c in enumerate(b):out[i]+=c
    return trim(out)

def scale(a,c):return trim([c*v for v in a])

def mul(*args):
    out=[1]
    for a in args:
        nxt=[0]*(len(out)+len(a)-1)
        for i,x in enumerate(out):
            for j,y in enumerate(a):nxt[i+j]+=x*y
        out=trim(nxt)
    return out

def evaluate(a,x):
    v=0
    for c in reversed(a):v=v*x+c
    return v

def psd(a):
    """Exact rational symmetric Schur elimination, including zero pivots."""
    b=[[F(v) for v in row] for row in a];n=len(b)
    require(all(len(row)==n for row in b),'square')
    require(all(b[i][j]==b[j][i] for i in range(n) for j in range(n)),'symmetric')
    piv=[]
    for k in range(n):
        d=b[k][k]
        if d<0:return False,piv+[d]
        if d==0:
            if any(b[k][j]!=0 for j in range(k+1,n)):return False,piv+[d]
            piv.append(d);continue
        piv.append(d)
        for i in range(k+1,n):
            for j in range(i,n):
                b[j][i]=b[i][j]=b[i][j]-b[i][k]*b[k][j]/d
    return True,piv

def dot(v,a,w):
    return sum(v[i]*a[i][j]*w[j] for i in range(len(v)) for j in range(len(w)))

def pascal(n):
    row=[1]
    for _ in range(n):row=[1]+[row[i]+row[i+1] for i in range(len(row)-1)]+[1]
    return row
