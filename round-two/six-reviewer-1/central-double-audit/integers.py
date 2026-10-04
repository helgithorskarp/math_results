"""Independent sparse integer polynomials, with exact whole coefficient gates."""
from math import comb
from fractions import Fraction as Q
Z=(0,0,0)

def constant(c):return {Z:c}if c else {}
def add(a,b):
    c=a.copy()
    for e,v in b.items():
        c[e]=c.get(e,0)+v
        if not c[e]:del c[e]
    return c
def scale(a,v):return {e:c*v for e,c in a.items()if c*v}
def mul(a,b):
    c={}
    for (i,j,k),v in a.items():
        for (p,q,r),w in b.items():
            e=(i+p,j+q,k+r);c[e]=c.get(e,0)+v*w
    return {e:v for e,v in c.items()if v}
def power(a,n):
    c=constant(1)
    for _ in range(n):c=mul(c,a)
    return c
def derivative(a,axis):
    c={}
    for e,v in a.items():
        if e[axis]:f=list(e);f[axis]-=1;c[tuple(f)]=e[axis]*v
    return c
def degree(a):return tuple(max((e[i]for e in a),default=0)for i in range(3))
def shift(a,e):return {tuple(i+j for i,j in zip(k,e)):v for k,v in a.items()}
def listpoly(poly):return [[list(e),str(v)]for e,v in sorted(poly.items())]
def exact_divide_axis(poly,divisor,axis):
    groups={}
    for e,v in poly.items():
        key=e[:axis]+e[axis+1:];groups.setdefault(key,{})[e[axis]]=v
    out={};d=max(divisor)
    for key,coeff in groups.items():
        quot={}
        while coeff and max(coeff)>=d:
            n=max(coeff)-d;top=coeff[n+d]
            if top%divisor[d]:raise ValueError('nonintegral full factor division')
            c=top//divisor[d];quot[n]=c
            for k,v in divisor.items():
                coeff[n+k]=coeff.get(n+k,0)-c*v
                if not coeff[n+k]:del coeff[n+k]
        if coeff:raise ValueError('whole polynomial factor remainder')
        for n,c in quot.items():e=list(key);e.insert(axis,n);out[tuple(e)]=c
    return out

def original():
    # a,D,u ring; all polynomials are exactly 64 times their monic versions.
    a={(1,0,0):1};D={(0,1,0):1};u={(0,0,1):1}
    a2=mul(a,a);a4=mul(a2,a2)
    q=[add(add(scale(a4,192),scale(a2,-64)),add(constant(6),scale(D,-16))),{},add(scale(a2,128),constant(-32)),{},constant(64)]
    k=[add(add(scale(a4,64),scale(a2,-24)),add(constant(3),scale(D,-8))),{},add(scale(a2,64),constant(-24)),{},constant(64)]
    def zmul(p,q):
        out=[{}for _ in range(len(p)+len(q)-1)]
        for i,v in enumerate(p):
            for j,w in enumerate(q):out[i+j]=add(out[i+j],mul(v,w))
        return out
    Qfull=zmul([a2,scale(a,2),constant(1)],q);Qfull[0]=add(Qfull[0],scale(u,256))
    H=zmul([{},a,constant(1)],k);H[0]=add(H[0],scale(u,64))
    f=zmul([a2,scale(a,-2),constant(1)],Qfull)
    fd=[scale(f[i],i)for i in range(1,len(f))];want=zmul([scale(a,-1),constant(1)],H)
    if fd!=[scale(v,8)for v in want]:raise ValueError('whole original derivative identity')
    r=[{}]+[scale(v,8)for v in H]
    rhs=zmul([scale(a,-1),constant(1)],Qfull)
    for i,v in enumerate(rhs):r[i]=add(r[i],scale(v,-8))
    while r and not r[-1]:r.pop()
    if len(r)!=6 or r[-1]!=constant(64):raise ValueError('complete degree-five norm-one residue')
    return H,r,f,Qfull

def bezout(H,g):
    # Direct antisymmetric monomials and geometric-series exact division.
    B=[[{}for _ in range(6)]for _ in range(6)]
    for i in range(1,7):
        for j in range(i):
            c=add(mul(H[i],g[j]if j<len(g)else{}),scale(mul(H[j],g[i]if i<len(g)else{}),-1))
            for t in range(i-j):B[i-1-t][j+t]=add(B[i-1-t][j+t],c)
    if any(B[i][j]!=B[j][i]for i in range(6)for j in range(6)):raise ValueError('whole Bezout symmetry')
    return B

def determinant_first_three(B,R):
    # Complete multilinear row expansion; w degree >2 cannot affect 0,1,2.
    states={0:[constant(1),{},{}]}
    for i in range(6):
        fresh={}
        for mask,coeff in states.items():
            for j in range(6):
                if mask&(1<<j):continue
                sign=(-1)**((mask>>(j+1)).bit_count());key=mask|(1<<j)
                dest=fresh.setdefault(key,[{},{},{}])
                for k in range(3):
                    dest[k]=add(dest[k],scale(mul(coeff[k],B[i][j]),sign))
                    if k:dest[k]=add(dest[k],scale(mul(coeff[k-1],R[i][j]),sign))
        states=fresh
    return states[63]

def half_a(poly):
    if any(e[0]%2 for e in poly):raise ValueError('whole reflection parity')
    return {(e[0]//2,e[1],e[2]):v for e,v in poly.items()}

def spectral_maps():
    H,r,f,Qfull=original();Hp=[scale(H[i],i)for i in range(1,7)]
    B=bezout(H,Hp);R=bezout(H,r);det=determinant_first_three(B,R)
    if det[1]!=det[0]:raise ValueError('complete determinant first mass coefficient')
    Delta=half_a(det[0]);N=half_a(det[2]);P=add(scale(shift(Delta,(0,1,0)),47),scale(N,-4))
    if [len(x)for x in [Delta,N,P]]!=[166,227,228]or any(degree(x)[2]!=5 for x in [Delta,N,P]):raise ValueError('whole original map census')
    return H,r,f,Qfull,B,R,Delta,N,P

def cap(P,kappa):
    I=degree(P)[0];S={}
    for (i,j,k),c in P.items():
        # Independent clearing of A=(1+8qt)/8,D=24q^2,u=v*d^3/(k*A*l).
        for a in range(i+5-k+1):
            ca=comb(i+5-k,a)*8**a
            for b in range(5-k+1):
                cb=comb(5-k,b)*3**(5-k-b)*5**b
                for z in range(3*k+1):
                    e=(10+4*k+2*j+a,a+2*b+2*z,k)
                    coeff=c*ca*cb*comb(3*k,z)*(-1)**z*kappa**(5-k)*2**(5-k)*6**(3*k)*24**j*8**(I-i+k)
                    S[e]=S.get(e,0)+coeff
    S={e:c for e,c in S.items()if c};whole_cleared=S.copy()
    if any(e[0]<20 for e in S):raise ValueError('entire q20 factor')
    S={(e[0]-20,e[1],e[2]):c for e,c in S.items()}
    S=exact_divide_axis(S,{0:1,2:-2,4:1},1)
    if degree(S)!=(12,28,5):raise ValueError('whole reduced cap degree')
    if shift(mul(S,{(0,0,0):1,(0,2,0):-2,(0,4,0):1}),(20,0,0))!=whole_cleared:raise ValueError('complete reverse cap-factor identity')
    return S,64**12*8**(I+5)

def affine(poly,ql,qr,tl,tr):
    out={}
    for (i,j,k),c in poly.items():
        for a in range(i+1):
            qa=comb(i,a)*ql**(i-a)*(qr-ql)**a
            for b in range(j+1):
                v=c*qa*comb(j,b)*tl**(j-b)*(tr-tl)**b
                if v:e=(a,b,k);out[e]=out.get(e,Q(0))+v
    return {e:v for e,v in out.items()if v}

def tensor(poly):
    degrees=(12,28,5);a={e:Q(v)for e,v in poly.items()}
    for axis,n in enumerate(degrees):
        b={}
        for e,v in a.items():
            for k in range(e[axis],n+1):
                f=list(e);f[axis]=k;f=tuple(f)
                b[f]=b.get(f,Q(0))+v*Q(comb(k,e[axis]),comb(n,e[axis]))
        a={e:v for e,v in b.items()if v}
    if len(a)!=13*29*6 or any(v<=0 for v in a.values()):raise ValueError('every tensor Bernstein coefficient strictly positive')
    controls=a
    b=a
    for axis,n in enumerate(degrees):
        a={}
        for e,v in b.items():
            for k in range(e[axis],n+1):
                f=list(e);f[axis]=k;f=tuple(f)
                a[f]=a.get(f,Q(0))+v*comb(n,k)*comb(k,e[axis])*(-1)**(k-e[axis])
        b={e:v for e,v in a.items()if v}
    if b!=poly:raise ValueError('entire reverse tensor coefficient identity')
    return controls
