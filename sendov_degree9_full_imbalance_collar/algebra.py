"""Exact Q[a,m,c,x,q] polynomial arithmetic for the affine-skew norm.

Single process, standard-library arbitrary-precision rationals.
The coefficient ring and variable order are fixed throughout.
"""
from fractions import Fraction as F
from math import comb, factorial
from collections import defaultdict

ZERO=(0,)*5
ONE={ZERO:F(1)}

def add(*items):
    out=defaultdict(F)
    for p in items:
        for e,k in p.items():out[e]+=k
    return {e:k for e,k in out.items() if k}

def scale(p,k):
    return {e:k*v for e,v in p.items() if k*v}

def mul(p,r):
    out=defaultdict(F)
    for e,k in p.items():
        for f,v in r.items():out[tuple(a+b for a,b in zip(e,f))]+=k*v
    return {e:k for e,k in out.items() if k}

def power(p,n):
    out=ONE
    while n:
        if n&1:out=mul(out,p)
        p=mul(p,p);n//=2
    return out

def variable(i):
    e=list(ZERO);e[i]=1
    return {tuple(e):F(1)}

def shifted_axis(p,axis):
    """Substitute the corresponding variable by 1 minus a new variable."""
    out=defaultdict(F)
    for e,k in p.items():
        for j in range(e[axis]+1):
            f=list(e);f[axis]=j
            out[tuple(f)]+=k*comb(e[axis],j)*(-1)**j
    return {e:k for e,k in out.items() if k}

def norm_polynomials():
    a,m,c,x,q=[variable(j) for j in range(5)]
    alpha=mul(m,c);B=mul(q,add(ONE,scale(power(c,2),-1)))
    R=add(power(m,2),scale(q,-1))
    ap=[power(alpha,j) for j in range(5)]
    bp=[power(scale(B,-1),j) for j in range(3)]
    rp=[power(R,j) for j in range(9)]
    aa=[power(a,j) for j in range(9)]
    P=[{} for _ in range(9)];Q=[{} for _ in range(9)]
    for n1 in range(5):
        for n2 in range(5-n1):
            n0=4-n1-n2;k=n1+2*n2
            coefficient=F(9*(-2)**n1*factorial(4),
                          (k+1)*factorial(n0)*factorial(n1)*factorial(n2))
            common=scale(mul(aa[k],rp[n2]),coefficient)
            for l in range(n1+1):
                term=scale(mul(common,mul(ap[n1-l],bp[l//2])),comb(n1,l))
                if l%2:Q[k]=add(Q[k],term)
                else:P[k]=add(P[k],term)
    T=[ONE,x];U=[ONE,scale(x,2)]
    for _ in range(7):
        T.append(add(scale(mul(x,T[-1]),2),scale(T[-2],-1)))
        U.append(add(scale(mul(x,U[-1]),2),scale(U[-2],-1)))
    even={};odd={}
    for k in range(9):even=add(even,mul(P[k],P[k]),mul(B,mul(Q[k],Q[k])))
    for j in range(9):
        for k in range(j):
            product=add(mul(P[j],P[k]),mul(B,mul(Q[j],Q[k])))
            even=add(even,scale(mul(product,T[j-k]),2))
            skew=add(mul(Q[j],P[k]),scale(mul(P[j],Q[k]),-1))
            odd=add(odd,scale(mul(skew,U[j-k-1]),2))
    delta=add(even,scale(rp[8],-1))
    return delta,odd,P,Q

def canonical(p):
    return [[list(e),str(v)] for e,v in sorted(p.items())]

def evaluate(p,values):
    return sum(v*__import__('functools').reduce(lambda a,b:a*b,
                 (values[i]**e[i] for i in range(5)),F(1)) for e,v in p.items())

def certificate(delta,odd):
    for axis in range(4):
        delta=shifted_axis(delta,axis)
        odd=shifted_axis(odd,axis)
    weights=(1,1,4,4)
    Kq=F(0);K2=F(0);Lq=F(0);L1=F(0)
    base=defaultdict(F);gradient=[F(0)]*4
    for e,v in delta.items():
        degree=sum(e[:4]);qdegree=e[4]
        weight=__import__('functools').reduce(lambda a,b:a*b,
                 (F(weights[i])**e[i] for i in range(4)),F(1))
        if degree==0:base[qdegree]+=v
        elif degree==1 and qdegree==0:
            gradient[e[:4].index(1)]+=v
        elif degree==1:
            Kq+=abs(v)*weight*F(1,4)**(qdegree-1)
        else:
            K2+=abs(v)*weight*F(1,100)**(degree-2)*F(1,4)**qdegree
    for e,v in odd.items():
        degree=sum(e[:4]);qdegree=e[4]
        weight=__import__('functools').reduce(lambda a,b:a*b,
                 (F(weights[i])**e[i] for i in range(4)),F(1))
        if degree==0:
            if qdegree==0 and v:raise ArithmeticError('Nonzero corner skew')
            Lq+=abs(v)*F(1,4)**(qdegree-1)
        else:
            L1+=abs(v)*weight*F(1,100)**(degree-1)*F(1,4)**qdegree
    K=max(Kq+2*Lq,K2+2*L1)
    N=0
    while 2**N<max(F(100),K):N+=1
    return {'base_coefficients':[str(base[j]) for j in range(9)],
            'first_variation':[str(v) for v in gradient],
            'Kq':str(Kq),'K2':str(K2),'Lq':str(Lq),'L1':str(L1),
            'K':str(K),'epsilon_power_two':N,
            'delta_shifted_terms':len(delta),'skew_shifted_terms':len(odd)},delta,odd

def alternate_integral_coefficients():
    """Four direct polynomial convolutions in Q[a,m,c,x,q][i beta]."""
    a,m,c,x,q=[variable(j) for j in range(5)]
    B=mul(q,add(ONE,scale(power(c,2),-1)))
    R=add(power(m,2),scale(q,-1))
    factors=[(ONE,{}),(scale(mul(a,mul(m,c)),-2),scale(a,-2)),
             (mul(power(a,2),R),{})]
    coefficients=[(ONE,{})]
    for _ in range(4):
        out=[({},{}) for _ in range(len(coefficients)+2)]
        for j,(p,r) in enumerate(coefficients):
            for k,(s,t) in enumerate(factors):
                real=add(mul(p,s),scale(mul(B,mul(r,t)),-1))
                imag=add(mul(p,t),mul(r,s))
                out[j+k]=(add(out[j+k][0],real),add(out[j+k][1],imag))
        coefficients=out
    return ([scale(z[0],F(9,k+1)) for k,z in enumerate(coefficients)],
            [scale(z[1],F(9,k+1)) for k,z in enumerate(coefficients)])

def alternate_norm(P,Q):
    """Square the real and imaginary integral parts, then reduce lambda^2."""
    x=variable(3);q=variable(4);c=variable(2)
    B=mul(q,add(ONE,scale(power(c,2),-1)))
    Y=add(ONE,scale(power(x,2),-1))
    T=[ONE,x];U=[ONE,scale(x,2)]
    for _ in range(7):
        T.append(add(scale(mul(x,T[-1]),2),scale(T[-2],-1)))
        U.append(add(scale(mul(x,U[-1]),2),scale(U[-2],-1)))
    A=add(*(mul(P[k],T[k]) for k in range(9)))
    G=add(*(mul(Q[k],T[k]) for k in range(9)))
    D=add(*(mul(Q[k],U[k-1]) for k in range(1,9)))
    H=add(*(mul(P[k],U[k-1]) for k in range(1,9)))
    even=add(mul(A,A),mul(B,mul(G,G)),mul(Y,add(mul(H,H),mul(B,mul(D,D)))))
    skew=scale(add(mul(A,D),scale(mul(G,H),-1)),2)
    return even,skew
