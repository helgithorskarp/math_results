"""Sparse exact Q(i,sqrt(2),sqrt(3),sqrt(5),sqrt(11),sqrt(13)) arithmetic."""
from fractions import Fraction as Q

RAD = (-1, 2, 3, 5, 11, 13)
E_BASIS = {0, 4 | 16, 1 | 4, 1 | 16}
EXTENDED_BASIS = E_BASIS | {m | 2 for m in E_BASIS}


def require(ok, message):
    if not ok:
        raise ValueError(message)


class A:
    def __init__(self, value=0):
        if isinstance(value, A):
            value = value.terms
        if not isinstance(value, dict):
            value = {0: Q(value)}
        self.terms = {m: Q(c) for m, c in value.items() if c}

    def __add__(self, other):
        out = self.terms.copy()
        for m, c in A(other).terms.items():
            out[m] = out.get(m, 0)+c
        return A(out)

    __radd__ = __add__

    def __neg__(self):
        return A({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -A(other)

    def __rsub__(self, other):
        return A(other) + -self

    def __mul__(self, other):
        out = {}
        for m, c in self.terms.items():
            for n, d in A(other).terms.items():
                factor = 1
                for k, p in enumerate(RAD):
                    if (m & n) & (1 << k):
                        factor *= p
                out[m ^ n] = out.get(m ^ n, 0)+factor*c*d
        return A(out)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == A(other).terms

    def __hash__(self):
        return hash(tuple(sorted(self.terms.items())))

    def bar(self):
        return A({m: (-c if m & 1 else c) for m, c in self.terms.items()})

    def norm(self):
        return self*self.bar()

    def in_field(self, extended=False):
        return set(self.terms) <= (EXTENDED_BASIS if extended else E_BASIS)

    def rational(self):
        require(set(self.terms) <= {0}, 'not a rational element')
        return self.terms.get(0, Q(0))


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def matpower(a, n):
    out = [[1, 0], [0, 1]]
    for _ in range(n):
        out = matmul(out, a)
    return out
