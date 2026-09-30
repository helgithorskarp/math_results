"""Independent exact arithmetic over Q[m,a,c,z,q,x,y,R,E,A,Y]."""
from fractions import Fraction as Q

NAMES = ('m','a','c','z','q','x','y','R','E','A','Y')
ZERO = (0,) * len(NAMES)


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.t = dict(value.t)
        elif isinstance(value, dict):
            self.t = {e: Q(c) for e,c in value.items() if c}
        else:
            self.t = {ZERO: Q(value)} if value else {}

    @classmethod
    def variable(cls, name):
        e = list(ZERO); e[NAMES.index(name)] = 1
        return cls({tuple(e): Q(1)})

    def __add__(self, other):
        out = dict(self.t)
        for e,c in P(other).t.items(): out[e] = out.get(e,Q(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self): return P({e:-c for e,c in self.t.items()})
    def __sub__(self, other): return self + -P(other)
    def __rsub__(self, other): return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e,c in self.t.items():
            for f,d in P(other).t.items():
                g = tuple(i+j for i,j in zip(e,f))
                out[g] = out.get(g,Q(0)) + c*d
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, k):
        if not isinstance(k,int) or k < 0: raise ValueError('Nonnegative power required')
        out,base = P(1),self
        while k:
            if k & 1: out = out*base
            base = base*base; k >>= 1
        return out

    def __eq__(self, other): return self.t == P(other).t

    def degree(self, name):
        i = NAMES.index(name)
        return max((e[i] for e in self.t),default=0)

    def coefficient(self, name, k):
        i = NAMES.index(name); out = {}
        for e,c in self.t.items():
            if e[i] == k:
                f = list(e); f[i] = 0; out[tuple(f)] = c
        return P(out)

    def diff(self, name):
        i = NAMES.index(name); out = {}
        for e,c in self.t.items():
            if e[i]:
                f = list(e); f[i] -= 1; out[tuple(f)] = c*e[i]
        return P(out)

    def substitute(self, name, value):
        return sum((self.coefficient(name,k)*P(value)**k
                    for k in range(self.degree(name)+1)),P(0))

    def rational_substitution(self, name, numerator, denominator):
        """Return den^degree * self(name=num/den); no cancellation assumptions."""
        n = self.degree(name)
        return sum((self.coefficient(name,k)*numerator**k*denominator**(n-k)
                    for k in range(n+1)),P(0)),denominator**n


class G:
    """Gaussian rational; never converts to Python float or complex."""
    def __init__(self, real=0, imag=0):
        if isinstance(real,G): self.r,self.i = real.r,real.i
        else: self.r,self.i = Q(real),Q(imag)

    def __add__(self, other):
        other=G(other); return G(self.r+other.r,self.i+other.i)
    __radd__=__add__
    def __neg__(self): return G(-self.r,-self.i)
    def __sub__(self, other): return self+-G(other)
    def __rsub__(self, other): return G(other)+-self
    def __mul__(self, other):
        other=G(other)
        return G(self.r*other.r-self.i*other.i,self.r*other.i+self.i*other.r)
    __rmul__=__mul__
    def __truediv__(self, real): return G(self.r/Q(real),self.i/Q(real))
    def __eq__(self, other):
        other=G(other); return (self.r,self.i)==(other.r,other.i)


def mm(A,B):
    n=len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(n)),G())
             for j in range(n)] for i in range(n)]


def trace(A): return sum((A[i][i] for i in range(len(A))),G())
