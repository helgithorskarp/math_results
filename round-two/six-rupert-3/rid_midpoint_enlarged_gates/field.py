"""Exact Q(phi) arithmetic; phi=(1+sqrt(5))/2, phi^2=phi+1.

The representation and sign algorithm follow the team's published
rhombicosidodecahedron_mirror_cluster_obstruction/verify.py. This is a
standalone copy of the elementary arithmetic interface, not a new claim.
Python 3.11+, standard library only.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class F:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "a", Fraction(self.a))
        object.__setattr__(self, "b", Fraction(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, F) else F(x)

    def __add__(self, other):
        q = self.coerce(other)
        return F(self.a+q.a, self.b+q.b)

    __radd__ = __add__

    def __neg__(self):
        return F(-self.a, -self.b)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        q = self.coerce(other)
        return F(self.a*q.a+self.b*q.b,
                 self.a*q.b+self.b*q.a+self.b*q.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a+self.a*self.b-self.b*self.b
        if not norm:
            raise ZeroDivisionError("zero in Q(phi)")
        return F((self.a+self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*self.coerce(other).inverse()

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("nonnegative integer exponent required")
        result = F(1)
        for _ in range(n):
            result *= self
        return result

    def sign(self):
        # 2(a+b*phi)=(2a+b)+b*sqrt(5); all decisions are rational.
        A, B = 2*self.a+self.b, self.b
        if not B:
            return (A>0)-(A<0)
        if not A:
            return (B>0)-(B<0)
        if A>0 and B>0:
            return 1
        if A<0 and B<0:
            return -1
        delta = A*A-5*B*B
        if not delta:
            raise ArithmeticError("unexpected rational square root of five")
        return (1 if delta>0 else -1) * (1 if A>0 else -1)

    def __abs__(self):
        return self*self.sign()

    def __lt__(self, other):
        return (self-other).sign()<0

    def __le__(self, other):
        return (self-other).sign()<=0

    def __gt__(self, other):
        return (self-other).sign()>0

    def __ge__(self, other):
        return (self-other).sign()>=0

    def encode(self):
        return [str(self.a), str(self.b)]


ZERO, ONE, PHI = F(), F(1), F(0, 1)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(v, w):
    require(len(v)==len(w), "dot-product dimensions differ")
    return sum((a*b for a,b in zip(v,w)), ZERO)


def cross(v, w):
    return (v[1]*w[2]-v[2]*w[1], v[2]*w[0]-v[0]*w[2],
            v[0]*w[1]-v[1]*w[0])


def sub(v, w):
    return tuple(a-b for a,b in zip(v,w))


def neg(v):
    return tuple(-x for x in v)


def key(v):
    return tuple((x.a, x.b) for x in v)


def encode(v):
    return [x.encode() for x in v]


def ray(v):
    pivot = next((x for x in v if x != ZERO), None)
    require(pivot is not None, "zero does not define a projective ray")
    return tuple(x/pivot for x in v)


def vertices():
    V = set()
    for seed in ((ONE,ONE,PHI**3),(PHI**2,PHI,2*PHI),
                 (2+PHI,ZERO,PHI**2)):
        for signs in product((-1,1), repeat=3):
            v = tuple(s*x for s,x in zip(signs, seed))
            for k in range(3):
                V.add(v[k:]+v[:k])
    return sorted(V, key=key)


def matmul(A, B):
    return tuple(tuple(dot(row,col) for col in zip(*B)) for row in A)


def act(A, v):
    return tuple(dot(row,v) for row in A)


def determinant(A):
    return dot(A[0], cross(A[1],A[2]))
