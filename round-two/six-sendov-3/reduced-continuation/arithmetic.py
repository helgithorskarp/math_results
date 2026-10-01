"""Exact cubic and quadratic-Gaussian arithmetic.

K and Z copied with attribution from six-sendov-3 analytic-boundary/algebra.py,
source ac6099018ea9e0e8e3092122db6ff24d549ebf32. No prior claim checker,
fixture or theorem is imported. The cubic field is Q[cos(pi/9)].
"""
from fractions import Fraction as F

class AlgebraError(RuntimeError):
    pass


def require(ok, label):
    if not ok:
        raise AlgebraError(label)


class K:
    """Q[c]/(c^3-3c/4-1/8), normal form (1,c,c^2)."""

    def __init__(self, value=0):
        if isinstance(value, K):
            self.a = value.a
        elif isinstance(value, (tuple, list)):
            require(len(value) == 3, 'cubic normal form length')
            self.a = tuple(map(F, value))
        else:
            self.a = (F(value), F(0), F(0))

    def __add__(self, other):
        other = K(other)
        return K(tuple(a+b for a, b in zip(self.a, other.a)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-a for a in self.a))

    def __sub__(self, other):
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        other = K(other)
        a = [F(0)]*5
        for i, x in enumerate(self.a):
            for j, y in enumerate(other.a):
                a[i+j] += x*y
        for i in (4, 3):
            a[i-2] += F(3, 4)*a[i]
            a[i-3] += F(1, 8)*a[i]
        return K(tuple(a[:3]))

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative field power')
        ans = K(1)
        for _ in range(n):
            ans *= self
        return ans

    def inv(self):
        columns = [(self*K(tuple(int(i == j) for i in range(3)))).a
                   for j in range(3)]
        rows = [[columns[j][i] for j in range(3)] + [F(i == 0)]
                for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j, 3) if rows[i][j]), None)
            require(pivot is not None, 'invertible cubic field element')
            rows[j], rows[pivot] = rows[pivot], rows[j]
            q = rows[j][j]
            rows[j] = [v/q for v in rows[j]]
            for i in range(3):
                if i != j:
                    q = rows[i][j]
                    rows[i] = [v-q*w for v, w in zip(rows[i], rows[j])]
        return K(tuple(rows[i][3] for i in range(3)))

    def __truediv__(self, other):
        return self*K(other).inv()

    def __rtruediv__(self, other):
        return K(other)*self.inv()

    def __eq__(self, other):
        return self.a == K(other).a

    def record(self):
        return [str(a) for a in self.a]

    def interval(self, lo, hi):
        # Here 0 < lo < hi, so powers preserve the ordered endpoints.
        lower = upper = self.a[0]
        for i in (1, 2):
            ends = self.a[i]*lo**i, self.a[i]*hi**i
            lower += min(ends)
            upper += max(ends)
        return lower, upper


class Z:
    """K[s,i]/(s^2-q,i^2+1), with conjugation fixing the real s."""

    def __init__(self, value=0, *, q=None):
        if isinstance(value, Z):
            self.q, self.a = value.q, value.a
        else:
            require(q is not None, 'quadratic extension specified')
            self.q = K(q)
            vals = value if isinstance(value, (list, tuple)) else (value, 0, 0, 0)
            require(len(vals) == 4, 'quadratic Gaussian length')
            self.a = tuple(K(v) for v in vals)

    def coerce(self, other):
        ans = other if isinstance(other, Z) else Z(other, q=self.q)
        require(ans.q == self.q, 'same quadratic extension')
        return ans

    def __add__(self, other):
        other = self.coerce(other)
        return Z(tuple(a+b for a, b in zip(self.a, other.a)), q=self.q)

    __radd__ = __add__

    def __neg__(self):
        return Z(tuple(-a for a in self.a), q=self.q)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        a, b, c, d = self.a
        e, f, g, h = other.a
        q = self.q
        return Z((a*e+b*f*q-c*g-d*h*q,
                  a*f+b*e-c*h-d*g,
                  a*g+b*h*q+c*e+d*f*q,
                  a*h+b*g+c*f+d*e), q=q)

    __rmul__ = __mul__

    def __truediv__(self, other):
        # Only real-field scalar divisions occur in this checker.
        return self*K(other).inv()

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative extension power')
        ans = Z(1, q=self.q)
        for _ in range(n):
            ans *= self
        return ans

    def conj(self):
        a, b, c, d = self.a
        return Z((a, b, -c, -d), q=self.q)

    def real_field(self):
        require(self.a[1] == 0, 'real part descends to cubic field')
        return self.a[0]

    def __eq__(self, other):
        return self.a == self.coerce(other).a

    def record(self):
        return [a.record() for a in self.a]

