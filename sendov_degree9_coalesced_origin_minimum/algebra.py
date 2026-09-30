"""Exact Q[a,m,c,x,q] polynomial arithmetic for the affine-skew norm.

The arithmetic and norm constructors are adapted from six-sendov-1's
sendov_degree9_full_imbalance_collar/algebra.py at source commit
af7a8476734433a6afde3a6ca2d4377542f66e66.
Parent file SHA256: 1148bfbf09b63b6e2a60f72b19159609b143d5e094b00dcd5fbf17ceb6102580
The new reference and grouping routines below supply this extension.
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

def reference_polynomial():
    """Unshifted a^2 times the coalesced norm minus one, by Chebyshev."""
    a,x=variable(0),variable(3)
    T=[ONE,x]
    for _ in range(8):
        T.append(add(scale(mul(x,T[-1]),2),scale(T[-2],-1)))
    real=add(*(scale(mul(power(a,k),T[k]),comb(9,k)*(-1)**k)
               for k in range(10)))
    distance=add(ONE,scale(mul(a,x),-2),power(a,2))
    return add(scale(real,-2),power(distance,9))

def diagonal(p):
    """Set chi=delta in a polynomial containing only delta and chi."""
    out=defaultdict(F)
    for e,v in p.items():
        if e[1] or e[2] or e[4]:
            raise ArithmeticError('Not a pure coalesced polynomial')
        f=list(ZERO);f[0]=e[0]+e[3]
        out[tuple(f)]+=v
    return {e:v for e,v in out.items() if v}

def difference_quotient(p):
    """Exact quotient (F(delta,chi)-F(delta,delta))/(chi-delta)."""
    out=defaultdict(F)
    for e,v in p.items():
        if e[1] or e[2] or e[4]:
            raise ArithmeticError('Not a pure coalesced polynomial')
        for j in range(e[3]):
            f=list(ZERO);f[0]=e[0]+j;f[3]=e[3]-1-j
            out[tuple(f)]+=v
    return {e:v for e,v in out.items() if v}

def coefficient_certificate(P,J):
    """Partition every shifted coefficient and construct finite majorants."""
    shifted=P;skew=J
    for axis in range(4):
        shifted=shifted_axis(shifted,axis)
        skew=shifted_axis(skew,axis)
    weights=(1,1,4,4);t0=F(1,100);q0=F(1,4);eps=F(1,16384)
    Mq=Me=Mg=Lq=L1=F(0)
    base=defaultdict(F);gradient=[F(0)]*4;pure={}
    groups=defaultdict(int)
    for e,v in shifted.items():
        d=sum(e[:4]);k=e[4]
        weight=__import__('functools').reduce(lambda s,z:s*z,
                      (F(weights[i])**e[i] for i in range(4)),F(1))
        if d==0:
            base[k]+=v;groups['base']+=1
        elif k:
            Mq+=abs(v)*weight*t0**(d-1)*q0**(k-1);groups['mixed_q']+=1
        elif d==1:
            gradient[e[:4].index(1)]+=v;groups['gradient']+=1
        elif e[1]:
            Me+=abs(v)*weight*t0**(d-2);groups['mixed_e']+=1
        elif e[2]:
            Mg+=abs(v)*(weight/4)*t0**(d-2);groups['mixed_gamma']+=1
        else:
            if d<5:raise ArithmeticError('Pure tail has degree below five')
            pure[e]=v;groups['pure_tail']+=1
    for e,v in skew.items():
        d=sum(e[:4]);k=e[4]
        weight=__import__('functools').reduce(lambda s,z:s*z,
                      (F(weights[i])**e[i] for i in range(4)),F(1))
        if d==0:
            if k==0:raise ArithmeticError('Nonzero constant skew')
            Lq+=abs(v)*q0**(k-1)
        else:L1+=abs(v)*weight*t0**(d-1)*q0**k
    quotient=difference_quotient(pure)
    S=sum(abs(v)*t0**(sum(e)-5) for e,v in quotient.items() if sum(e)>=5)
    M=sum(abs(v)*4**e[3]*t0**(sum(e)-4) for e,v in quotient.items())
    T=sum(abs(v)*t0**(sum(e)-5) for e,v in pure.items())
    leading={e[3]:v for e,v in quotient.items() if sum(e)==4}
    bounds={'Mq':Mq,'Me':Me,'M_gamma':Mg,'Lq':Lq,'L1':L1,
            'Jmax':Lq/4+L1*eps,'S':S,'M':M,'T':T}
    cert={'epsilon':'1/16384','majorant_anchor':'1/100',
          'base_coefficients':[str(base[j]) for j in range(9)],
          'first_variation':[str(v) for v in gradient],
          'coefficient_groups':dict(groups),
          'bounds':{k:str(v) for k,v in bounds.items()},
          'leading_quotient':[str(leading.get(j,F(0))) for j in range(5)],
          'pure_minimum_degree':min(sum(e) for e in pure),
          'quotient_minimum_degree':min(sum(e) for e in quotient),
          'shifted_P_terms':len(shifted),'shifted_J_terms':len(skew),
          'pure_tail_terms':len(pure),'quotient_terms':len(quotient)}
    return cert,shifted,skew,pure,quotient
