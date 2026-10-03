"""Reviewer-written formal affine counting; no native executable imports."""
from math import comb, factorial
from fractions import Fraction


def C(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def add(x, y):
    return [a+b for a,b in zip(x,y)]


def scale(c, x):
    return [c*a for a in x]


def dimensions(n):
    return 2**n-n-1, 2**(n-1)-n, 2**(n-1)-1


def labels():
    proper = [(a,b) for a in range(8,19) for b in range(a,19) if a+b<26]
    return ['d'+str(a) for a in range(8,14)]+['t%d_%d'%p for p in proper], proper


def table():
    n=26; N,s,h=dimensions(n); names,pairs=labels(); width=1+len(names)
    zero=lambda:[0]*width
    const=lambda v:[v]+[0]*(width-1)
    B=[[zero() for b in range(n-1)] for a in range(n-1)]
    for a in range(2,14):
        x=const(s)
        if a>=8: x[1+a-8]=-1
        B[a][n-a]=x[:]; B[n-a][a]=x[:]
    for j,(a,b) in enumerate(pairs,7):
        x=zero(); x[j]=1; B[a][b]=x[:]; B[b][a]=x[:]
    for a in range(2,n-1):
        x=const(s)
        for b in range(2,n-1): x=add(x,scale(-C(n-a-1,b-1),B[a][b]))
        B[a][1]=x[:]; B[1][a]=x[:]
    x=const(s)
    for b in range(2,n-1): x=add(x,scale(-C(n-2,b-1),B[1][b]))
    B[1][1]=x
    e=[zero() for a in range(n-1)]
    for a in range(1,n-1):
        e[a]=const(h)
        for b in range(1,n-1): e[a]=add(e[a],scale(-C(n-a,b),B[a][b]))
    ell=const(N)
    for a in range(1,n-1): ell=add(ell,scale(-C(n,a),e[a]))
    return B,e,ell


def numeric_table(x):
    """Independent numeric recovery using a marked-point proportion."""
    n=26;N,s,h=dimensions(n);_,pairs=labels()
    B=[[Fraction(0) for b in range(n-1)] for a in range(n-1)]
    for a in range(2,14): B[a][n-a]=B[n-a][a]=s-(x[a-8] if a>=8 else 0)
    for j,(a,b) in enumerate(pairs,6): B[a][b]=B[b][a]=x[j]
    for a in range(2,n-1):
        B[a][1]=B[1][a]=s-sum(Fraction(b*C(n-a,b),n-a)*B[a][b] for b in range(2,n-1))
    B[1][1]=s-sum(Fraction(b*C(n-1,b),n-1)*B[1][b] for b in range(2,n-1))
    e=[Fraction(0)]+[h-sum(C(n-a,b)*B[a][b] for b in range(1,n-1)) for a in range(1,n-1)]
    ell=N-sum(C(n,a)*e[a] for a in range(1,n-1))
    return B,e,ell


def energy_ordered(B,z):
    n=26;_,s,_=dimensions(n)
    out=[2*s*sum(C(n-2,a-1)*z[a-1]**2 for a in range(1,n-1))]+[0]*36
    for a in range(1,n-1):
        for b in range(1,n-1):
            out=add(out,scale(-2*C(n-2,a-1)*C(n-a-1,b-1)*z[a-1]*z[b-1],B[a][b]))
    return out


def energy_unordered(B,z):
    n=26;_,s,_=dimensions(n)
    out=[2*s*sum(C(n-2,a-1)*z[a-1]**2 for a in range(1,n-1))]+[0]*36
    for a in range(1,n-1):
        for b in range(a,n-1):
            if a+b>n:continue
            count=factorial(n-2)//(factorial(a-1)*factorial(b-1)*factorial(n-a-b))
            out=add(out,scale((-2 if a==b else -4)*count*z[a-1]*z[b-1],B[a][b]))
    return out


def det(A):
    A=[[Fraction(x) for x in row] for row in A]; answer=Fraction(1)
    for j in range(len(A)):
        k=next((k for k in range(j,len(A)) if A[k][j]),None)
        if k is None:return Fraction(0)
        if k!=j:A[j],A[k]=A[k],A[j];answer=-answer
        pivot=A[j][j];answer*=pivot
        for k in range(j+1,len(A)):
            q=A[k][j]/pivot
            for l in range(j+1,len(A)):A[k][l]-=q*A[j][l]
    return answer


def sigma(n,a,b):
    return Fraction(n,max(C(n-a-1,b-1),C(n-b-1,a-1)))
