"""Small exact sparse polynomial ring used for universal algebraic identities.

Coefficients are supplied by the caller. No evaluation or floating arithmetic
is involved in an identity check. Variables are independent real indeterminates.
"""

class Ring:
    def __init__(self, coefficient_type, variables):
        self.Q = coefficient_type
        self.n = variables
        self.zero = {}
        self.one = self.constant(1)

    def constant(self, value):
        value = self.Q(value)
        return {} if value == 0 else {(0,) * self.n: value}

    def variable(self, index):
        e = [0] * self.n
        e[index] = 1
        return {tuple(e): self.Q(1)}

    def add(self, *polynomials):
        out = {}
        for p in polynomials:
            for e, c in p.items():
                out[e] = out.get(e, self.Q()) + c
        return {e: c for e, c in out.items() if c != 0}

    def scale(self, factor, polynomial):
        return {e: factor * c for e, c in polynomial.items() if factor * c != 0}

    def neg(self, polynomial):
        return self.scale(-1, polynomial)

    def subtract(self, left, right):
        return self.add(left, self.neg(right))

    def multiply(self, left, right):
        out = {}
        for e, c in left.items():
            for f, d in right.items():
                g = tuple(x + y for x, y in zip(e, f))
                out[g] = out.get(g, self.Q()) + c * d
        return {e: c for e, c in out.items() if c != 0}

    def dot(self, left, right):
        return self.add(*(self.multiply(x, y) for x, y in zip(left, right)))

    def vector_add(self, *vectors):
        return tuple(self.add(*(v[k] for v in vectors)) for k in range(3))

    def vector_scale(self, scalar, vector):
        return tuple(self.multiply(scalar, x) for x in vector)

    def vector(self, values):
        return tuple(self.constant(x) for x in values)

    def cross(self, a, b):
        m = self.multiply
        s = self.subtract
        return (s(m(a[1], b[2]), m(a[2], b[1])),
                s(m(a[2], b[0]), m(a[0], b[2])),
                s(m(a[0], b[1]), m(a[1], b[0])))

    def determinant2(self, a, b):
        return self.subtract(self.multiply(a[0], b[1]),
                             self.multiply(a[1], b[0]))

    def terms(self, polynomial):
        return [(list(e), c) for e, c in sorted(polynomial.items())]
