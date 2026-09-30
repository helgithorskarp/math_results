"""Exact arithmetic reused from six-reviewer-1 nine-point audit.
No author mathematical code is imported.
"""
import hashlib,json,math
from fractions import Fraction as Q

def check(ok, message):
    if not ok:
        raise ValueError(message)

def vertex(points):
    return sum(1 << p for p in points)

def digest(matrix):
    return hashlib.sha256(json.dumps([[str(Q(x)) for x in row] for row in matrix],
                                    separators=(',',':')).encode()).hexdigest()

def product(a,b):
    check(not a or len(a[0])==len(b),'matrix product dimension')
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def image(a,v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]

def quadratic(a,v):
    return sum(x*y for x,y in zip(v,image(a,v)))

def inverse(a):
    n=len(a)
    check(all(len(r)==n for r in a),'inverse shape')
    work=[[Q(x) for x in r]+[Q(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        i=next((i for i in range(j,n) if work[i][j]),None)
        check(i is not None,'singular inverse')
        work[j],work[i]=work[i],work[j]
        p=work[j][j]
        work[j]=[x/p for x in work[j]]
        for i in range(n):
            if i!=j and work[i][j]:
                c=work[i][j]
                work[i]=[x-c*y for x,y in zip(work[i],work[j])]
    result=[r[n:] for r in work]
    check(product(a,result)==[[Q(i==j) for j in range(n)] for i in range(n)],
          'inverse identity')
    return result

def psd_rank(a, operation_cap=5_000_000):
    """Integer Bareiss Schur elimination, valid under symmetric pivoting.

    After positive pivots the current block is a positive multiple of the
    Schur complement. A zero diagonal with nonzero row is indefinite.
    All divisions are required exact. Exceeding a cap raises INCOMPLETE.
    """
    n=len(a)
    check(all(len(r)==n for r in a),'PSD shape')
    check(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'PSD symmetry')
    scale=math.lcm(*(Q(x).denominator for r in a for x in r)) if n else 1
    b=[[int(Q(x)*scale) for x in r] for r in a]
    previous=1
    rank=0
    operations=0
    for k in range(n):
        for i in range(k,n):
            check(b[i][i]>=0,'negative Schur diagonal')
            if not b[i][i]:
                check(not any(b[i][j] for j in range(k,n)),'zero diagonal nonzero row')
        p=next((i for i in range(k,n) if b[i][i]),None)
        if p is None:
            return rank
        if p!=k:
            b[k],b[p]=b[p],b[k]
            for r in b:
                r[k],r[p]=r[p],r[k]
        pivot=b[k][k]
        for i in range(k+1,n):
            for j in range(i,n):
                operations+=1
                if operations>operation_cap:
                    raise RuntimeError('INCOMPLETE integer PSD operation cap')
                value,remainder=divmod(pivot*b[i][j]-b[i][k]*b[k][j],previous)
                check(not remainder,'nonexact Bareiss division')
                b[i][j]=b[j][i]=value
        previous=pivot
        rank+=1
    return rank

def span_rank(columns):
    if not columns:
        return 0
    a=[[Q(v) for v in row] for row in zip(*columns)]
    rank=0
    for col in range(len(columns)):
        i=next((i for i in range(rank,len(a)) if a[i][col]),None)
        if i is None:
            continue
        a[rank],a[i]=a[i],a[rank]
        p=a[rank][col]
        a[rank]=[x/p for x in a[rank]]
        for j in range(rank+1,len(a)):
            if a[j][col]:
                c=a[j][col]
                a[j]=[x-c*y for x,y in zip(a[j],a[rank])]
        rank+=1
    return rank

