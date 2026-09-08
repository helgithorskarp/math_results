"""Explicit additive F_3 colourings of every cyclotomic integer ring.

Only the Python standard library is required. Vertices are INTEGER power-basis
coefficient lists. This API deliberately rejects rational denominators.
"""
from functools import lru_cache
from itertools import product

def require(condition, message):
    if not condition: raise ValueError(message)

def factors(n):
    require(type(n) is int and n >= 1, 'positive integer conductor required')
    answer=[]; p=2
    while p*p<=n:
        if n%p==0:
            q=1
            while n%p==0: n//=p; q*=p
            answer.append((p,q))
        p+=1
    if n>1: answer.append((n,n))
    return answer

def phi(n): return __import__('math').prod(q-q//p for p,q in factors(n))

def divide_monic(a,b):
    a=list(a); out=[0]*(len(a)-len(b)+1)
    require(b[-1]==1 and len(a)>=len(b),'invalid monic division')
    for k in range(len(out)-1,-1,-1):
        out[k]=a[k+len(b)-1]
        for j,c in enumerate(b): a[k+j]-=out[k]*c
    require(not any(a),'nonzero polynomial remainder')
    return tuple(out)

@lru_cache(None)
def cyclotomic(n):
    factors(n)
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: a=divide_monic(a,cyclotomic(d))
    return tuple(a)

def root_weight(n,j):
    """tau_n(zeta_n**j); the CRT tensor formula in PROOF.md."""
    answer=1
    for p,q in factors(n):
        exponent=(j*pow(n//q,-1,q))%q
        block=exponent//(q//p)
        answer*=1 if block<(2*p)%3 else -1
    return answer%3

def functional(n): return [root_weight(n,j) for j in range(phi(n))]

def colour(n, coefficients):
    require(len(coefficients)==phi(n),'wrong power-basis dimension')
    require(all(type(a) is int for a in coefficients),'integral coefficients required')
    return sum(a*b for a,b in zip(coefficients,functional(n)))%3

def reduce_poly(a,modulus):
    a=list(a); d=len(modulus)-1
    if len(a)<d: a.extend([0]*(d-len(a)))
    for k in range(len(a)-1,d-1,-1):
        top=a[k]
        if top:
            for j,c in enumerate(modulus): a[k-d+j]-=top*c
    return tuple(a[:d])

def mul(a,b,modulus):
    out=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        if u:
            for j,v in enumerate(b):
                if v: out[i+j]+=u*v
    return reduce_poly(out,modulus)

def roots(n):
    f=cyclotomic(n); d=len(f)-1
    z=(1,)+(0,)*(d-1); answer=[]
    for _ in range(n):
        answer.append(z); z=reduce_poly((0,)+z,f)
    require(z==answer[0],'root period failed')
    return answer

def fixture():
    n=30; f=cyclotomic(n); rr=roots(n); d=len(f)-1
    points=list(product((0,1),repeat=d))
    def conjugate(z):
        return tuple(sum(z[j]*rr[-j%n][k] for j in range(d)) for k in range(d))
    one=rr[0]; edges=[]
    for i,u in enumerate(points):
        for j in range(i+1,len(points)):
            delta=tuple(a-b for a,b in zip(u,points[j]))
            if mul(delta,conjugate(delta),f)==one: edges.append([i,j])
    word=[colour(n,z) for z in points]
    require(all(word[i]!=word[j] for i,j in edges),'fixture colour conflict')
    return {'conductor':n,'points':[list(z) for z in points],
            'edges':edges,'colouring':word,'functional':functional(n)}
