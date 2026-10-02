"""Independent exact sparse Laurent arithmetic; no producer imports.

Q[B,E,r,s,t,F,G,J], allowing only t negative before the chart change.
After change the first five slots mean q,E,r,x,u. All identity checks
are complete coefficient comparisons, with exceptions rather than assert.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, lcm

N = 8
ZERO = (0,) * N


class P:
    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.d = terms.d.copy()
        elif isinstance(terms, dict):
            self.d = {k: Q(v) for k, v in terms.items() if v}
        else:
            self.d = {ZERO: Q(terms)} if terms else {}

    def __add__(self, other):
        other = P(other)
        d = self.d.copy()
        for k, v in other.d.items():
            d[k] = d.get(k, Q(0)) + v
            if not d[k]:
                del d[k]
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) - self

    def __mul__(self, other):
        other = P(other)
        d = {}
        for a, v in self.d.items():
            for b, w in other.d.items():
                k = tuple(x + y for x, y in zip(a, b))
                d[k] = d.get(k, Q(0)) + v * w
        return P(d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = P(other)
        if len(other.d) != 1:
            raise ValueError('only scalar/monomial division')
        (b, w), = other.d.items()
        return P({tuple(x-y for x,y in zip(a,b)):v/w for a,v in self.d.items()})

    def __pow__(self, n):
        if n < 0:
            return P(1) / (self ** (-n))
        a, b = P(1), self
        while n:
            if n & 1:
                a = a * b
            b = b * b
            n //= 2
        return a

    def __eq__(self, other):
        return self.d == P(other).d

    def degree(self, slot):
        return max((k[slot] for k in self.d), default=-1)

    def coeff(self, slot, degree):
        return P({tuple(0 if i == slot else e for i,e in enumerate(k)):v
                  for k,v in self.d.items() if k[slot] == degree})

    def sub(self, slot, value):
        value = P(value)
        powers = {n: value ** n for n in {k[slot] for k in self.d}}
        return sum((P({tuple(0 if i == slot else e for i,e in enumerate(k)):v})
                    * powers[k[slot]] for k,v in self.d.items()), P())

    def diff(self, slot):
        return P({tuple(e-1 if i == slot else e for i,e in enumerate(k)):v*k[slot]
                  for k,v in self.d.items() if k[slot]})

    def serial(self):
        return [[list(k), v.numerator, v.denominator] for k,v in sorted(self.d.items())]

    def primitive(self):
        den = lcm(*(v.denominator for v in self.d.values()))
        numer = gcd(*(int(v*den) for v in self.d.values()))
        if not numer:
            raise ValueError('primitive zero')
        content = Q(numer, den)
        return content, self / content


def var(slot):
    k = list(ZERO)
    k[slot] = 1
    return P({tuple(k): 1})


def identity(a, b, label, log):
    if a != b:
        raise ValueError('coefficient identity: '+label)
    log[label] = P(a).serial()


def add(a, b):
    return [(a[i] if i<len(a) else P())+(b[i] if i<len(b) else P())
            for i in range(max(len(a),len(b)))]


def scale(a, c):
    return [v*c for v in a]


def mul(a, b):
    d = [P() for _ in range(len(a)+len(b)-1)]
    for i,v in enumerate(a):
        for j,w in enumerate(b):
            d[i+j] = d[i+j]+v*w
    return d


def deriv(a):
    return [i*a[i] for i in range(1,len(a))] or [P()]


def rem(a, h):
    a = list(a)
    if h[-1] != 1:
        raise ValueError('monic divisor')
    for i in range(len(a)-1,len(h)-2,-1):
        c = a[i]
        for j in range(len(h)):
            a[i-len(h)+1+j] = a[i-len(h)+1+j]-c*h[j]
    return a[:len(h)-1]+[P()] * max(0,len(h)-1-len(a))


def newton(h, top=6):
    n = len(h)-1
    tau = [P(n)]
    for k in range(1,top+1):
        tau.append(-sum((h[n-j]*tau[k-j] for j in range(1,k)), P())-k*h[n-k])
    return tau


def adj(a, h):
    if len(a)>7:
        raise ValueError('adjoint requires reduced representative')
    tau = newton(h)
    out = [P() for _ in range(7)]
    for k in range(1,len(a)):
        for j in range(k):
            out[k-1-j] = out[k-1-j]+a[k]*tau[j]
        out[k-1] = out[k-1]-k*a[k]
    return out


def ode_kernel(h, p, q):
    ode = add(add(mul(p,deriv(deriv(h))),mul(add(deriv(p),scale(q,-1)),deriv(h))),
              mul(add([P(64)],scale(deriv(q),-1)),h))
    kernel = add(add(scale(p,-16),scale(adj(adj(rem(mul(p,p),h),h),h),Q(-1,4))),
                 scale(adj(rem(mul(p,add(q,scale(deriv(p),-1))),h),h),Q(1,4)))
    return ode, kernel


def assembly(log):
    B,E,r,s,t,F,G,J = (var(i) for i in range(8))
    p2 = 8+t*(5*B/7-27*s/56-r*s)
    p0 = -Q(5,7)+t*(3*B*r/7+75*B/392+4*E*s/7+5*F/7+3*r*s/28+9*s/784)
    p1 = 128*B/5+t*(-8*B**2/7-4*B*r*s+4*B*s/7+16*E*r/3+3*E+20*F*s/3+8*G-3*r/8-Q(9,64))
    def build(f=F,g=G,j=J):
        h=[j,g,f,E,B,P(Q(-3,8)),P(),P(1)]
        pc=[p0.sub(5,f),p1.sub(5,f).sub(6,g),p2,r*t,s*t,t]
        qc=[7*pc[1]+t*(3*r/4-3*B*s+Q(9,32)-4*E),64+t*(2*B-21*s/8-7*r*s),t*(7*r+Q(3,4)),7*s*t,7*t]
        return h,pc,qc,*ode_kernel(h,pc,qc)
    h,p,q,o,k=build()
    for name,poly in [('O5',o[5]),('O4',o[4]),('K5',k[5])]:
        identity(poly,0,'fixed-'+name,log)
    a=k[4].sub(6,0)
    identity(k[4],24*t**2*G+a,'G-pivot',log)
    g0=-a/(24*t**2)
    k3=k[3].sub(6,g0)
    b=k3.sub(5,0)
    identity(k3,-Q(15,14)*t**2*F+b,'F-pivot',log)
    fs=14*b/(15*t**2)
    gs=g0.sub(5,fs)
    h,p,q,o,k=build(fs,gs)
    c=o[3].sub(7,0)
    identity(o[3],-28*t*J+c,'J-pivot',log)
    js=c/(28*t)
    h,p,q,o,k=build(fs,gs,js)
    for d in range(3,len(o)):
        identity(o[d],0,'full-O'+str(d),log)
    for d in range(3,len(k)):
        identity(k[d],0,'full-K'+str(d),log)
    residual=[t*o[2],t*o[1],t*o[0],k[1],k[0]+4]
    if [len(v.d) for v in residual] != [43,54,71,29,44]:
        raise ValueError('complete pencil term counts')
    if any(min(z[4] for z in v.d)<0 or v.degree(4)>2 or any(z[i] for i in [5,6,7]) for v in residual for z in v.d):
        raise ValueError('entire polynomial pencil')
    f=scale(add(mul(q,h),scale(mul(p,deriv(h)),-1)),Q(1,8))
    fd=add(deriv(f),scale(h,-8))
    for i in range(max(len(fd),len(o))):
        identity(fd[i] if i<len(fd) else P(),-o[i]/8 if i<len(o) else P(),'original-derivative-'+str(i),log)
    return residual, {'h':[v.serial() for v in h], 'p':[v.serial() for v in p],
                      'Q':[v.serial() for v in q], 'gamma':(k[2]/4).serial()}


def chart(a, s_power):
    d={}
    for k,v in (a*var(3)**s_power).d.items():
        b,e,r,s,t,f,g,j=k
        power=b+s-t
        if power<0 or power%2 or f or g or j:
            raise ValueError('chart parity/nonnegative power')
        n=(b,e,r,power//2,t,0,0,0)
        d[n]=d.get(n,Q(0))+v
    return P(d)


def to_v(a):
    # q^d u^e = v^d u^(e-d); polynomial only, never hides u inversion.
    d={}
    for k,v in a.d.items():
        if k[4]<k[0]:
            raise ValueError('hidden negative u')
        n=tuple(k[i]-k[0] if i==4 else k[i] for i in range(8))
        d[n]=d.get(n,Q(0))+v
    return P(d)


def sylvester(a,b,slot):
    m,n=a.degree(slot),b.degree(slot)
    rows=[]
    for poly,size in [(a,n),(b,m)]:
        for shift in range(size-1,-1,-1):
            p=poly*var(slot)**shift
            rows.append([p.coeff(slot,j) for j in range(m+n-1,-1,-1)])
    return rows


def det_permutation(rows):
    # Direct Leibniz sum, not author interpolation/Bareiss/Gaussian.
    n=len(rows); total=P()
    for order in permutations(range(n)):
        value=P(1)
        for i,j in enumerate(order):
            value=value*rows[i][j]
            if not value.d:
                break
        sign=-1 if sum(order[i]>order[j] for i in range(n) for j in range(i+1,n))%2 else 1
        total=total+sign*value
    return total


def ff_trim(a):
    while a and not a[-1]:
        a.pop()
    return a


def ff_add(a,b,p):
    return ff_trim([((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p
                    for i in range(max(len(a),len(b)))])


def ff_mul(a,b,p):
    c=[0]*max(0,len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):
            c[i+j]=(c[i+j]+v*w)%p
    return ff_trim(c)


def ff_div(a,b,p):
    a=a.copy();q=[0]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        d=len(a)-len(b);c=a[-1]*pow(b[-1],-1,p)%p;q[d]=c
        a=ff_add(a,[0]*d+[-c*v%p for v in b],p)
    return ff_trim(q),a


def bezout(a,b,p):
    old,r=a.copy(),b.copy();s,ss=[1],[];t,tt=[],[1]
    while r:
        q,new=ff_div(old,r,p)
        old,r=r,new
        s,ss=ss,ff_add(s,[-v%p for v in ff_mul(q,ss,p)],p)
        t,tt=tt,ff_add(t,[-v%p for v in ff_mul(q,tt,p)],p)
    if len(old)!=1:
        raise ValueError('nonunit gcd')
    z=pow(old[0],-1,p)
    return [z*v%p for v in s],[z*v%p for v in t]
