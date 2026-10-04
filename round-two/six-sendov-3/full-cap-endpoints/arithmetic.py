"""Small exact cubic field and named-monomial polynomial kernel.

Physical embedding c=cos(pi/9), 8c^3-6c-1=0, c in(939/1000,940/1000).
New implementation for a deduction from explicitly credited written parents.
No other research package, expected output, or generated record is imported.
"""
from fractions import Fraction as F


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


class C:
    __slots__ = ('v',)

    def __init__(self, a=0, b=0, c=0):
        if isinstance(a, C):
            self.v = a.v
        else:
            self.v = (F(a), F(b), F(c))

    def __add__(self, other):
        if not isinstance(other,(C,int,F)):
            return NotImplemented
        other = C(other)
        return C(*(a+b for a,b in zip(self.v,other.v)))

    __radd__ = __add__

    def __neg__(self):
        return C(*(-a for a in self.v))

    def __sub__(self, other):
        if not isinstance(other,(C,int,F)):
            return NotImplemented
        return self+-C(other)

    def __rsub__(self, other):
        return C(other)+-self

    def __mul__(self, other):
        if not isinstance(other,(C,int,F)):
            return NotImplemented
        other = C(other)
        out = [F(0)]*5
        for i,a in enumerate(self.v):
            for j,b in enumerate(other.v):
                out[i+j] += a*b
        for k in (4,3):
            out[k-3] += out[k]/8
            out[k-2] += 3*out[k]/4
        return C(*out[:3])

    __rmul__ = __mul__

    def inverse(self):
        require(bool(self),'zero field divisor')
        columns = [(self*C(*(int(i==j) for i in range(3)))).v for j in range(3)]
        rows = [[columns[j][i] for j in range(3)]+[F(int(i==0))] for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j,3) if rows[i][j]),None)
            require(pivot is not None,'singular cubic field multiplication')
            rows[j],rows[pivot] = rows[pivot],rows[j]
            z = rows[j][j]
            rows[j] = [a/z for a in rows[j]]
            for i in range(3):
                if i != j:
                    z = rows[i][j]
                    rows[i] = [a-z*b for a,b in zip(rows[i],rows[j])]
        answer = C(*(rows[i][3] for i in range(3)))
        require(self*answer == C(1),'entire inverse product')
        return answer

    def __truediv__(self, other):
        return self*C(other).inverse()

    def __rtruediv__(self, other):
        return C(other)*self.inverse()

    def __pow__(self, n):
        require(type(n) is int and n>=0,'nonnegative power required')
        out = C(1)
        for _ in range(n):
            out *= self
        return out

    def __eq__(self, other):
        return isinstance(other,(C,int,F)) and self.v == C(other).v

    def __bool__(self):
        return any(self.v)

    def record(self):
        return [str(a) for a in self.v]


class P:
    """Sparse real polynomial. A monomial is a sorted tuple (name,degree)."""
    __slots__ = ('d',)

    def __init__(self, value=0):
        if isinstance(value,P):
            self.d = dict(value.d)
        elif isinstance(value,dict):
            self.d = {m:C(a) for m,a in value.items() if C(a)}
        else:
            self.d = {():C(value)} if C(value) else {}

    @classmethod
    def variable(cls, name):
        require(type(name) is str and name,'polynomial variable name')
        return cls({((name,1),):C(1)})

    def __add__(self, other):
        out = dict(self.d)
        for m,a in P(other).d.items():
            out[m] = out.get(m,C(0))+a
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({m:-a for m,a in self.d.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for m,a in self.d.items():
            for n,b in P(other).d.items():
                powers = dict(m)
                for name,k in n:
                    powers[name] = powers.get(name,0)+k
                key = tuple(sorted(powers.items()))
                out[key] = out.get(key,C(0))+a*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self*C(other).inverse()

    def __pow__(self, n):
        require(type(n) is int and n>=0,'nonnegative polynomial power')
        out = P(1)
        for _ in range(n):
            out *= self
        return out

    def __eq__(self, other):
        return self.d == P(other).d

    def coefficient(self, variable, degree):
        out = {}
        for m,a in self.d.items():
            powers = dict(m)
            if powers.pop(variable,0) == degree:
                key = tuple(sorted(powers.items()))
                out[key] = out.get(key,C(0))+a
        return P(out)

    def record(self):
        return [{'monomial':[[n,k] for n,k in m],'cubic':a.record()} for m,a in sorted(self.d.items())]


def cubic_root_interval(steps=64):
    lo,hi = F(939,1000),F(940,1000)
    f = lambda z:8*z**3-6*z-1
    require(f(lo)<0<f(hi) and 24*lo*lo-6>0,'physical embedding bracket')
    for _ in range(steps):
        mid = (lo+hi)/2
        if f(mid)<0:
            lo = mid
        else:
            hi = mid
    require(f(lo)<0<f(hi),'strict final embedding bracket')
    return lo,hi


def interval(a, bracket):
    lo,hi = bracket
    # c is positive: each monomial interval is exact, then coefficient signs.
    lower = upper = F(0)
    for k,z in enumerate(C(a).v):
        l,h = lo**k,hi**k
        lower += z*(l if z>=0 else h)
        upper += z*(h if z>=0 else l)
    return lower,upper
