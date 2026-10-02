"""Exact cubic arithmetic, restricted to the kernel needed here.

K copied with attribution from six-sendov-3 analytic-boundary/algebra.py,
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
