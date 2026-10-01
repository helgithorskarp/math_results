"""Independent rational-pair arithmetic; signs use exact dyadic root enclosures."""

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


@dataclass(frozen=True)
class Q:
    a: F = F(0)
    b: F = F(0)
    d: int = 5

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))
        if self.d < 2 or isqrt(self.d) ** 2 == self.d:
            raise ValueError("a positive nonsquare radicand is required")

    def coerce(self, other):
        if not isinstance(other, Q):
            return Q(other, 0, self.d)
        if other.d == self.d:
            return other
        if not other.b:
            return Q(other.a, 0, self.d)
        raise ValueError("incompatible fields")

    def __add__(self, other):
        other = self.coerce(other)
        return Q(self.a + other.a, self.b + other.b, self.d)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Q(self.a * other.a + self.d * self.b * other.b,
                 self.a * other.b + self.b * other.a, self.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        norm = other.a ** 2 - self.d * other.b ** 2
        if not norm:
            raise ZeroDivisionError("zero algebraic denominator")
        return self * Q(other.a / norm, -other.b / norm, self.d)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("nonnegative integer powers only")
        result = Q(1, 0, self.d)
        for _ in range(power):
            result *= self
        return result

    def zero(self):
        return not self.a and not self.b

    def sign(self):
        if self.zero():
            return 0
        if not self.b:
            return 1 if self.a > 0 else -1
        for bits in (8, 16, 32, 64, 128, 256):
            denominator = 1 << bits
            floor = isqrt(self.d << (2 * bits))
            low, high = F(floor, denominator), F(floor + 1, denominator)
            ends = (self.a + self.b * low, self.a + self.b * high)
            if min(ends) > 0:
                return 1
            if max(ends) < 0:
                return -1
        raise ArithmeticError("sign enclosure unresolved; no sign inferred")

    def record(self):
        return {"a": str(self.a), "b": str(self.b), "radicand": self.d}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def equal(left, right):
    return (left - right).zero()


def psd_rank(matrix):
    """Complete symmetric Schur elimination, including every zero-pivot row."""
    n = len(matrix)
    require(n and all(len(row) == n for row in matrix), "matrix shape")
    d = next((x.d for row in matrix for x in row if isinstance(x, Q)), 5)
    a = [[Q(0, 0, d).coerce(x) for x in row] for row in matrix]
    require(all(equal(a[i][j], a[j][i]) for i in range(n) for j in range(n)),
            "matrix symmetry")
    rank, pivots = 0, []
    while a:
        signs = [a[i][i].sign() for i in range(len(a))]
        require(all(s >= 0 for s in signs), "negative diagonal Schur pivot")
        positive = [i for i, s in enumerate(signs) if s > 0]
        if not positive:
            require(all(x.zero() for row in a for x in row), "nonzero zero-pivot block")
            return rank, pivots, len(a)
        p = positive[-1]
        indices = [i for i in range(len(a)) if i != p]
        pivot = a[p][p]
        pivots.append(pivot.record())
        a = [[a[i][j] - a[i][p] * a[p][j] / pivot for j in indices]
             for i in indices]
        rank += 1
    return rank, pivots, 0
